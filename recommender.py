# recommender.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import streamlit as st

TMDB_API_KEY = "3d98ee51d91d5b894ababc4e75119f08"  # <-- Replace with your TMDB API key

# Load movies
columns = ['movieId', 'title', 'release_date', 'video_release_date', 'IMDb_URL',
           'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
           'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
           'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

movies = pd.read_csv('u.item', sep='|', names=columns, encoding='latin-1')

# Combine genre flags
genre_cols = columns[5:]
movies['genres'] = movies[genre_cols].apply(lambda x: ' '.join([g for g, v in zip(genre_cols, x) if v == 1]), axis=1)
movies['year'] = movies['release_date'].str[-4:]  # Extract release year
movies = movies[['movieId', 'title', 'genres', 'year']]

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# Cached poster fetch function
@st.cache_data
def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    results = response.get('results')
    if results:
        poster_path = results[0]['poster_path']
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None


# Recommendation function
def recommend_movies(title, cosine_sim=cosine_sim, movies=movies):
    if title not in movies['title'].values:
        return pd.DataFrame(columns=['title', 'poster_url', 'year'])

    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]

    recommended = movies.iloc[movie_indices][['title', 'year']].copy()
    recommended['poster_url'] = recommended['title'].apply(fetch_poster)
    return recommended.reset_index(drop=True)

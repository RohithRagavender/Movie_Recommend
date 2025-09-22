# app.py

import streamlit as st
from recommender import recommend_movies, movies

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
<style>
/* Responsive container */
.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    padding: 20px;
}

/* Movie card styling */
.movie-card {
    background-color: #1c1c1e;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeIn 0.6s ease-in-out;
}
.movie-card:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 20px rgba(0,0,0,0.8);
}

/* Movie title and year */
.movie-title {
    color: #ffca28;
    font-size: 20px;
    font-weight: 600;
    margin-top: 10px;
}
.movie-year {
    color: #90a4ae;
    font-size: 14px;
    margin-top: 4px;
}

/* Fade-in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Title styling */
.title {
    font-size: 56px;
    font-weight: 700;
    color: #00bcd4;
    text-align: center;
    text-shadow: 1px 1px 8px rgba(0,0,0,0.7);
    margin-top: 30px;
}

/* Subtitle styling */
.subtitle {
    font-size: 22px;
    color: #b0bec5;
    text-align: center;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)


# Title and subtitle
st.markdown('<h1 class="title">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Find movies you will love!</h3>', unsafe_allow_html=True)
st.write("---")

# Movie dropdown
selected_movie = st.selectbox("Choose your favorite movie:", movies['title'].values)

if st.button("Show Recommendations"):
    recommendations = recommend_movies(selected_movie)

    st.subheader("Top 5 Recommendations")

    # Display in columns
    # Inside your columns loop in app.py

    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(recommendations):
            poster = recommendations['poster_url'][i]
            title = recommendations['title'][i]
            year = recommendations['year'][i]

            # Check if poster exists
            if poster:
                col.markdown(f"""
                    <div class="movie-card">
                        <img src="{poster}" width="150"><br>
                        <div class="movie-title">{title}</div>
                        <div class="movie-year">({year})</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Show "Poster not available" message
                col.markdown(f"""
                    <div class="movie-card">
                        <div style="height:150px; display:flex; align-items:center; justify-content:center; color:#ff6f61; font-weight:bold;">
                            Poster not available
                        </div>
                        <div class="movie-title">{title}</div>
                        <div class="movie-year">({year})</div>
                    </div>
                """, unsafe_allow_html=True)

import streamlit as st
import joblib
from recommender import get_recommendations
from streamlit_searchbox import st_searchbox
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title("🎬 Movie Recommender System")
st.write("Start typing a movie name and pick from suggestions:")


@st.cache_resource
def load_data():
    df = joblib.load("../Models/movie_dataframe.joblib")
    tfidf_matrix = joblib.load("../Models/tfidf_matrix.joblib")
    movie_list = df['original_title'].sort_values().unique()
    return df, tfidf_matrix, movie_list

df, tfidf_matrix, movie_list = load_data()

def get_poster_url(movie_title):
    api_key = "31c6b2a4fab808900e946b36af001a51" 
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"

    try:
        response= requests.get(search_url)
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def search_movies(search_term: str):
    if not search_term:
        return []
    return [m for m in movie_list if search_term.lower() in m.lower()][:10]

user_input = st_searchbox(
    search_movies,
    key="movie_search",
    placeholder="Enter Movie Name",
)

top_n = st.slider("Number of recommendations", 5, 20, 10)

if st.button("Recommend"):
    if not user_input:
        st.error("Please select a movie from suggestions!")
    else:
        results = get_recommendations(user_input, df, tfidf_matrix, top_n)

        if results.empty:
            st.error("No recommendations found for this movie!")
        else:
            st.success("Recommended Movies:")
            cols = st.columns(5)

            for i, row in results.reset_index().iterrows():
                with cols[i % 5]:
                    poster_url = get_poster_url(row['original_title'])
                    st.image(poster_url, use_container_width=True)
                    st.write(f"**{row['original_title'].title()}**")
                    st.caption(f"⭐ {row['vote_average']}")
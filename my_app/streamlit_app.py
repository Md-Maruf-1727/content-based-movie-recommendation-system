import streamlit as st
import joblib
from recommender import get_recommendations
from streamlit_searchbox import st_searchbox

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title("🎬 Movie Recommender System")
st.write("Start typing a movie name and pick from suggestions:")

# Load data (cached for speed)
@st.cache_resource
def load_data():
    df = joblib.load("../Models/movie_dataframe.joblib")
    tfidf_matrix = joblib.load("../Models/tfidf_matrix.joblib")
    movie_list = df['original_title'].sort_values().unique()
    return df, tfidf_matrix, movie_list

df, tfidf_matrix, movie_list = load_data()

# --------------------------
# Auto-suggestion input (top 10 only)
# --------------------------
def search_movies(search_term: str):
    if not search_term:
        return []
    return [m for m in movie_list if search_term.lower() in m.lower()][:10]

# UI-তে ব্যবহার
user_input = st_searchbox(
    search_movies,
    key="movie_search",
    placeholder="Enter Movie Name",
)

# Number of recommendations
top_n = st.slider("Number of recommendations", 5, 20, 10)

# Button trigger
if st.button("Recommend"):
    if not user_input:
        st.error("Please select a movie from suggestions!")
    else:
        results = get_recommendations(user_input, df, tfidf_matrix, top_n)
        if results.empty:
            st.error("No recommendations found for this movie!")
        else:
            st.success("Recommended Movies:")
            for i, row in results.iterrows():
                st.write(f"**{row['original_title']}** ⭐ {row['vote_average']}")
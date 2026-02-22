import streamlit as st
import joblib
from recommender import get_recommendations

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

st.title("🎬 Movie Recommmendation System")
st.write("Type a movie name & get similiar recommendations.")

@st.cache_resource
def load_data():
    df = joblib.load("../Models/movie_dataframe.joblib")
    tfidf_matrix = joblib.load("../Models/tfidf_matrix.joblib")
    return df, tfidf_matrix
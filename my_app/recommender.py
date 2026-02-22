import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from thefuzz import process

tfidf = joblib.load('../Models/tfidf_vectorizer.joblib')
tfidf_matrix = joblib.load('../Models/tfidf_matrix.joblib')
df = joblib.load('../Models/movie_dataframe.joblib')


def get_recommendations(user_input_titles, df, tfidf_matrix, top_n = 10):
    if isinstance(user_input_titles, str):
        user_input_titles = [user_input_titles]

    indices = pd.Series(df.index, index=df['original_title']).to_dict()

    matched_indices = []
    all_movie_titles = df['original_title'].tolist()

    for title in user_input_titles:
        best_match = process.extractOne(title, all_movie_titles)

        if best_match[1] > 80:
            matched_movie_name = best_match[0]
            idx = indices[matched_movie_name]
            matched_indices.append(idx)
            print(f'"{title}" Matched to {matched_movie_name}')
        else:
            print(None)
    if not matched_indices:
        print("Movie Not Found")
    
    sim_matrix = cosine_similarity(tfidf_matrix[matched_indices], tfidf_matrix)
    avg_sim = sim_matrix.mean(axis=0)

    for idx in matched_indices:
        avg_sim[idx] = -1

    top_indices = avg_sim.argsort()[::-1][:25]

    qualified = df.iloc[top_indices].copy()
    qualified = qualified.sort_values('score', ascending=False)

    return qualified[['original_title', 'vote_average', 'vote_count', 'score']].head(top_n)
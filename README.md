# 🎬 Content-Based Movie Recommendation System

A content-based movie recommendation system built on 45,000+ movies from the TMDB dataset.
Uses TF-IDF vectorization and cosine similarity to find movies similar to what you love.
Includes a fully deployed Streamlit web app with fuzzy search and live movie posters.

---

## 🚀 Live Demo

<!-- ADD GIF: static/demo.gif here -->

---

## 📌 How It Works

1. User types a movie name (supports typos — fuzzy matching handles it)
2. System matches it to the closest movie in the database
3. TF-IDF finds movies with the most similar descriptions and genres
4. Results are ranked using a weighted rating score (not just raw votes)
5. Movie posters are fetched live from the TMDB API

---

## 📊 Dataset

- **Source:** TMDB Movies Metadata Dataset
- **Original Size:** 45,466 movies × 24 columns
- **After Cleaning:** 41,917 movies × 6 columns
- **Features Used:** Movie overview (plot) + Genres combined

---

## 🗂️ Project Structure
```
content-based-movie-recommendation-system/
│
├── Data/
│   ├── Raw/
│   │   └── movies_metadata.csv          # Original TMDB dataset
│   └── processed/
│       └── cleaned_dataset.csv          # Cleaned & preprocessed data
│
├── Models/
│   ├── tfidf_vectorizer.joblib          # Saved TF-IDF vectorizer
│   ├── tfidf_matrix.joblib              # Saved TF-IDF matrix (41917 × 20000)
│   └── movie_dataframe.joblib           # Saved movie dataframe
│
├── Notebooks/
│   ├── 01_data_overview.ipynb           # Data exploration & understanding
│   ├── 02_data_cleaning.ipynb           # Cleaning & text preprocessing
│   ├── 03_recommendation_model.ipynb    # Model building & testing
│   └── 04_evaluation_model.ipynb        # Model evaluation
│
├── my_app/
│   ├── static/
│   │   └── demo.gif                     # App demo
│   ├── recommender.py                   # Recommendation logic
│   └── streamlit_app.py                 # Streamlit web app
│
├── requirements.txt
└── README.md
````
---

## ⚙️ What I Did — Step by Step

### Step 1 — Data Overview (`01_data_overview.ipynb`)

Explored the raw TMDB dataset to understand structure and quality issues:

- Dataset: 45,466 movies, 24 columns
- Identified key issues:
  - 14,562 movies with fewer than 5 votes (unreliable ratings)
  - 1,258 movies with suspiciously high ratings but almost no votes
  - 954 missing overviews
  - 1,158 duplicate overviews
  - Genres stored as raw JSON strings — needed parsing

---

### Step 2 — Data Cleaning (`02_data_cleaning.ipynb`)

- Dropped 19 irrelevant columns — kept only: `genres`, `original_title`, `overview`, `vote_average`, `vote_count`
- Filled missing overviews with empty string
- Parsed genres from JSON format → plain text (e.g. `"Animation Comedy Family"`)
- Created `description` column = overview + genres combined
- Removed movies with fewer than 5 votes AND rating ≥ 8 (noise/unreliable data)
- Removed duplicate titles
- Applied full text cleaning pipeline:
  - Lowercased all text
  - Removed special characters
  - Removed stopwords (NLTK)
  - Applied lemmatization (WordNetLemmatizer)
- Removed 237 rows with empty descriptions after cleaning
- **Final dataset: 41,917 movies**

<!-- ADD IMAGE: sample of cleaned dataset here -->

---

### Step 3 — Recommendation Model (`03_recommendation_model.ipynb`)

#### TF-IDF Vectorization
- Used `TfidfVectorizer` with:
  - `max_features = 20,000`
  - `ngram_range = (1, 3)` — captures single words, pairs, and triplets
  - `stop_words = 'english'`
- Result: **41,917 × 20,000 TF-IDF matrix**

#### Weighted Rating Score
To rank results fairly (not just by raw votes):
score = (v / (v + m) × R) + (m / (v + m) × C)

- `v` = movie's vote count
- `m` = minimum votes threshold (75th percentile)
- `R` = movie's average rating
- `C` = overall average rating across all movies

This prevents a movie with 1 vote and 10/10 from outranking a movie with 5,000 votes and 7.7/10.

#### Cosine Similarity + Fuzzy Matching
- Calculates similarity between movies using cosine similarity on TF-IDF vectors
- Supports multiple input movies — averages their similarity scores
- Uses `thefuzz` library for fuzzy title matching (handles typos)
- If match confidence > 60%, accepts the match

#### Example Output
Input: "toy sto"
Matched to: "toy story 2"
Results:

Toy Story          ⭐ 7.7  (5415 votes)
Toy Story 3        ⭐ 7.6  (4710 votes)
Toy Story of Terror ⭐ 7.3 (246 votes)
...


<!-- ADD IMAGE: recommendation output screenshot here -->

---

### Step 4 — Streamlit Web App (`my_app/streamlit_app.py`)

Built a fully interactive web application:

- **Live search box** — autocomplete as you type
- **Fuzzy matching** — works even with typos
- **Adjustable results** — slider to choose 5–20 recommendations
- **Movie posters** — fetched live from TMDB API
- **Grid layout** — 5 columns display with rating shown below each poster

<!-- ADD IMAGE: streamlit app screenshot here -->

---

## 🛠️ Tools & Libraries

| Category | Tools |
|---|---|
| Language | Python |
| Data Manipulation | Pandas, NumPy |
| NLP & ML | Scikit-learn (TF-IDF, Cosine Similarity), NLTK |
| Fuzzy Matching | thefuzz |
| Web App | Streamlit, streamlit-searchbox |
| Movie Posters | TMDB API |
| Model Saving | Joblib |
| Environment | Jupyter Notebook |

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Md-Maruf-1727/content-based-movie-recommendation-system.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download NLTK data (first time only)
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# 4. Run notebooks in order to generate model files
# 01 → 02 → 03

# 5. Launch the Streamlit app
cd my_app
streamlit run streamlit_app.py
```

---

## 📈 Key Features

- ✅ Works with 41,000+ movies
- ✅ Handles typos and partial titles
- ✅ Supports multi-movie input for blended recommendations
- ✅ Weighted scoring prevents low-vote movies from dominating results
- ✅ Live movie posters via TMDB API
- ✅ Clean interactive web UI

---

## 👤 Author

**Md. Maruf**
GitHub: [github.com/Md-Maruf-1727](https://github.com/Md-Maruf-1727)

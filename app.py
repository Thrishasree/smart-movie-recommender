import streamlit as st
import requests
import os
import pandas as pd
import random
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Page config must be first Streamlit command
st.set_page_config(page_title="Smart Movie Recommender", layout="centered")

# Load API key
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Session state
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []
if "df" not in st.session_state:
    st.session_state["df"] = None
if "similarity" not in st.session_state:
    st.session_state["similarity"] = None
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# 🌙 Half‑moon toggle button
if st.button("🌙 Toggle Theme"):
    st.session_state["dark_mode"] = not st.session_state["dark_mode"]

# Apply background color based on toggle
if st.session_state["dark_mode"]:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: black;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- Functions ----------------
def fetch_movies_by_keyword(keyword, max_pages=5):
    movies = []
    for page in range(1, max_pages+1):
        url = f"http://www.omdbapi.com/?s={keyword}&type=movie&page={page}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                for item in data["Search"]:
                    movies.append(item["Title"])
    return movies

def fetch_movie_details(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "Title": data["Title"],
                "Genre": data.get("Genre", ""),
                "Plot": data.get("Plot", ""),
                "Poster": data.get("Poster", "")
            }
    return None

def build_similarity_matrix(movie_list):
    details = []
    for m in movie_list:
        data = fetch_movie_details(m)
        if data:
            details.append(data)
    if not details:
        return None, None
    df = pd.DataFrame(details)
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["Genre"] + " " + df["Plot"])
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return df, similarity

def recommend(movie_title, df, similarity, top_n=5):
    if movie_title not in df["Title"].values:
        return []
    idx = df[df["Title"] == movie_title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recommendations = [df.iloc[i[0]] for i in scores[1:top_n+1]]
    return recommendations

# ---------------- UI ----------------
st.title("🎬 Smart Movie Recommender")

# Keyword input
keyword = st.text_input("Enter a keyword or year (e.g., 'action', 'love', '1999'):")

if st.button("Fetch Movies"):
    movie_list = fetch_movies_by_keyword(keyword, max_pages=5)
    if movie_list:
        df, similarity = build_similarity_matrix(movie_list)
        if df is not None:
            st.session_state["df"] = df
            st.session_state["similarity"] = similarity
            st.success(f"Loaded {len(df)} movies for recommendations!")
        else:
            st.error("Could not build dataset. Try another keyword.")
    else:
        st.error("No movies found for that keyword.")

# Recommend from dropdown
if st.session_state["df"] is not None:
    selected_movie = st.selectbox("Select a movie:", st.session_state["df"]["Title"].values)
    if st.button("Recommend"):
        recs = recommend(selected_movie, st.session_state["df"], st.session_state["similarity"], top_n=5)
        st.subheader("Top Recommendations:")
        for idx, r in enumerate(recs):
            st.write(f"**{r['Title']}**")
            st.write(r["Plot"])
            if r["Poster"] and r["Poster"] != "N/A":
                st.image(r["Poster"], width=200)
            else:
                st.text("Poster not available")
            if st.button(f"❤️ Save {r['Title']} to Favorites", key=f"fav_{idx}"):
                st.session_state["favorites"].append(r["Title"])
                st.success(f"Added {r['Title']} to favorites!")

# Surprise Me (safe)
if st.session_state["df"] is not None and st.button("Surprise Me 🎲"):
    if len(st.session_state["df"]) == 0:
        st.error("⚠️ No movies available. Please fetch movies first with a keyword or year.")
    else:
        random_movie = random.choice(st.session_state["df"]["Title"].tolist())
        st.info(f"Randomly selected: **{random_movie}**")
        recs = recommend(random_movie, st.session_state["df"], st.session_state["similarity"], top_n=5)
        st.subheader("Top Recommendations:")
        for idx, r in enumerate(recs):
            st.write(f"**{r['Title']}**")
            st.write(r["Plot"])
            if r["Poster"] and r["Poster"] != "N/A":
                st.image(r["Poster"], width=200)
            else:
                st.text("Poster not available")
            if st.button(f"❤️ Save {r['Title']} to Favorites", key=f"surprise_{idx}"):
                st.session_state["favorites"].append(r["Title"])
                st.success(f"Added {r['Title']} to favorites!")

# Favorites section
if st.session_state["favorites"]:
    st.subheader("⭐ Your Favorites")
    for fav in st.session_state["favorites"]:
        st.write(f"- {fav}")

# Footer
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>Developed by KOTTURI THRISHA SREE ❤️</h4>", unsafe_allow_html=True)
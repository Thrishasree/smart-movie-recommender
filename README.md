# 🎬 Smart Movie Recommender (OMDb)

A Streamlit web app that recommends movies based on keywords or years, shows posters and plots from the **OMDb API**, and lets you save favorites.  
Includes a **favorites system**, **theme toggle (🌙 half‑moon)**, and **download options** for saving liked movies.

---

## ✨ Features

- 🔍 **Search movies** by keyword or year (via OMDb API)  
- 🎬 **Movie details**: title, genre, plot, poster  
- 🎲 **Surprise Me**: random movie recommendations  
- ❤️ **Favorites**: save movies you like  
- 📄 **Download favorites** as `.txt` or `.csv`  
- 🌙 **Half‑moon toggle**: switch background between black and white  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — interactive Python web apps  
- [OMDb API](https://www.omdbapi.com/) — movie metadata  
- Python libraries:  
  - `requests`  
  - `pandas`  
  - `scikit-learn` (TF‑IDF + cosine similarity)  
  - `python-dotenv`  

---

## ⚙️ Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/smart-movie-recommender.git
   cd smart-movie-recommender
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(or manually: `pip install streamlit requests python-dotenv scikit-learn pandas`)*

3. **Create a `.env` file** in the project root:
   ```
   OMDB_API_KEY=your_api_key_here
   ```

   You can get a free OMDb API key from omdbapi.com [(omdbapi.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwww.omdbapi.com%2Fapikey.aspx").

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```
---

## 🚀 Future Improvements

- Add more advanced filtering (genre, rating)  
- Integrate trailers (YouTube API)  
- User authentication for personalized favorites  

---


import os
import pickle
import gdown
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_URL = "https://drive.google.com/uc?export=download&id=1sGPdOb3SJLy7TzSn5ULYVKQplsR0tLpk"
MODEL_PATH = "model.pkl"

# ---- Step 1: Download model.pkl if not exists ----
if not os.path.exists(MODEL_PATH):
    print("Downloading model.pkl...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    print("model.pkl downloaded.")

# ---- Step 2: Load model.pkl ----
with open(MODEL_PATH, "rb") as f:
    model_data = pickle.load(f)

# ---- Step 3: Extract data and similarity matrix ----
try:
    data = model_data["data"]               # Pandas DataFrame with 'title' and 'cleaned_text'
    similarity = model_data["similarity"]   # Similarity matrix (e.g., cosine similarity)
except (KeyError, TypeError):
    raise ValueError("model.pkl does not contain expected keys: 'data', 'similarity'.")

# ---- Step 4: Recommend similar movies ----
def recommend_movies(movie_title, top_n=5):
    movie_title = movie_title.lower()
    if movie_title not in data['title'].str.lower().values:
        return []

    index = data[data['title'].str.lower() == movie_title].index[0]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended_indices = [i[0] for i in similarity_scores[1:top_n+1]]
    recommended_titles = data.iloc[recommended_indices]['title'].tolist()
    return recommended_titles

# ---- API Routes ----
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "API running successfully 🚀"}), 200

@app.route("/recommend", methods=["POST"])
def recommend():
    req_data = request.get_json()
    movie_title = req_data.get("movie")

    if not movie_title:
        return jsonify({"error": "Missing 'movie' field in request body"}), 400

    recommendations = recommend_movies(movie_title)
    if not recommendations:
        return jsonify({"error": "Movie not found in database"}), 404

    return jsonify({"recommended": recommendations})

# ---- Entry point for local dev (optional) ----
if __name__ == "__main__":
    app.run(debug=True)

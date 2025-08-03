import os
import pickle
import gdown
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity

# ---- Auto-download model.pkl if not present ----
MODEL_URL = "https://drive.google.com/uc?export=download&id=1sGPdOb3SJLy7TzSn5ULYVKQplsR0tLpk"
MODEL_PATH = "model.pkl"

if not os.path.exists("model.pkl"):
    print("Downloading model.pkl...")
    gdown.download(MODEL_URL, "model.pkl", quiet=False)
    print("model.pkl downloaded.")

# ---- Load model ----
with open(MODEL_PATH, "rb") as f:
    model_data = pickle.load(f)

data = model_data["data"]               # pandas DataFrame with 'title' and 'cleaned_text'
tfidf_matrix = model_data["matrix"]    # TF-IDF matrix

# ---- Setup Flask ----
app = Flask(__name__)
CORS(app)

# ---- Recommendation function ----
def recommend_movies(movie_name, top_n=5):
    idx = data[data['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        return []

    idx = idx[0]
    sim_scores = list(enumerate(cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Skip the movie itself

    movie_indices = [i[0] for i in sim_scores]
    return data[['title']].iloc[movie_indices].to_dict(orient="records")

# ---- API Route ----
@app.route("/recommend", methods=["POST"])
def recommend():
    data_in = request.get_json()
    movie_title = data_in.get("title", "")
    
    if not movie_title:
        return jsonify({"error": "No movie title provided"}), 400

    recommendations = recommend_movies(movie_title)
    
    if not recommendations:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify(recommendations)

# ---- Run locally ----
if __name__ == "__main__":
    app.run(debug=True)

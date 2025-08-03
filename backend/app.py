from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
import gdown
import difflib


MODEL_URL = "https://drive.google.com/uc?export=download&id=1sGPdOb3SJLy7TzSn5ULYVKQplsR0tLpk"
MODEL_PATH = "model.pkl"

# Download model if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading model.pkl...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    print("model.pkl downloaded.")

# Load the tuple model
with open(MODEL_PATH, "rb") as f:
    similarity, data = pickle.load(f)  # tuple unpacking

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "*"}})




@app.route("/recommend", methods=["POST"])
def recommend():
    req = request.get_json()
    movie_input = req.get("movie", "").strip().lower()

    if not movie_input:
        return jsonify({"error": "Missing 'movie' field"}), 400

    # Create a lowercase title series for comparison
    data["title_lower"] = data["title"].str.strip().str.lower()

    # Try to find the closest match using difflib
    close_matches = difflib.get_close_matches(movie_input, data["title_lower"], n=1, cutoff=0.6)

    if not close_matches:
        return jsonify({"error": f"Movie '{movie_input}' not found"}), 404

    matched_movie = close_matches[0]
    idx = data[data["title_lower"] == matched_movie].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = data.iloc[[i[0] for i in sim_scores]]["title"].tolist()

    return jsonify({"recommendations": recommendations})
@app.route("/")
def home():
    return "Movie Recommender API is running."

if __name__ == "__main__":
    app.run(debug=True)

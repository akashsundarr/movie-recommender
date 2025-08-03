from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
import gdown

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
CORS(app)

@app.route("/recommend", methods=["POST"])
def recommend():
    req = request.get_json()
    movie = req.get("movie")

    if not movie:
        return jsonify({"error": "Missing 'movie' field"}), 400

    if movie not in data['title'].values:
        return jsonify({"error": f"Movie '{movie}' not found"}), 404

    idx = data[data['title'] == movie].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = data.iloc[[i[0] for i in sim_scores]]['title'].tolist()

    return jsonify({"recommendations": recommendations})

@app.route("/")
def home():
    return "Movie Recommender API is running."

if __name__ == "__main__":
    app.run(debug=True)

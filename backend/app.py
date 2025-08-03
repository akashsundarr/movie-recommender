from flask import Flask, request, jsonify
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Load the saved model and data (ensure model.pkl is present)
with open("model.pkl", "rb") as f:
    cosine_sim, data = pickle.load(f)

def recommend_movies(movie_name, top_n=5):
    idx = data[data['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        return []
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices].tolist()

@app.route("/recommend", methods=["POST"])
def recommend():
    content = request.get_json()
    movie = content.get("movie", "")
    if not movie:
        return jsonify({"error": "No movie title provided"}), 400
    recommendations = recommend_movies(movie)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)

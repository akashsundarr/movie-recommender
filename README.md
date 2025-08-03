
# 🎬 Movie Recommendation System

A fullstack web application that provides movie recommendations based on content-based filtering.

## ✨ Overview

This project leverages Python for its recommendation engine, exposing an API via Flask, and presents recommendations through a modern React user interface.

## 🚀 Key Technologies

### Backend 🐍
* **Python**
* **Flask** 🧪
* **pandas** 🐼
* **scikit-learn** 🧠
* **Render** ☁️ (for deployment)

### Frontend ⚛️
* **React** ⚛️
* **Vite** ⚡
* **Tailwind CSS** 🎨
* **Vercel** 🚀 (for hosting)
* **OMDb API** 🎥 (for movie data)

## 📁 Project Structure


movie-recommender/
├── backend/                  \# Flask API for recommendations
├── movie-app/                \# React user interface
└── Movie\_recommendation\_system.ipynb  \# Jupyter Notebook for ML model development


## ▶️ How to Run

1.  **Backend**: Navigate to `backend/` and run the Flask app.
2.  **Frontend**: Navigate to `movie-app/` and start the Vite React app.
3.  **Notebook**: Open `Movie_recommendation_system.ipynb` in Google Colab for model details.

*(Detailed instructions for each can be found in their respective `README.md` files.)*

## 🔗 Links

Live Demo (Frontend): https://movie-recommender-nu-three.vercel.app

Backend API Base URL: https://movie-recommender-bit5.onrender.com

ML Model (.pkl) on Google Drive: https://drive.google.com/file/d/1sGPdOb3SJLy7TzSn5ULYVKQplsR0tLpk/view

Note: The backend automatically downloads this model using gdown on deployment/startup.

## 🚧 Struggles & Solutions 🚧

* **GitHub's 100MB File Limit**
    * **Problem**: `model.pkl` too large for GitHub.
    * **Solution**: Uploaded to Google Drive, auto-downloaded with `gdown` in Flask app.
* **Incorrect `.pkl` Structure**
    * **Problem**: Tried to access tuple like a dictionary.
    * **Solution**: Unpacked correctly: `similarity, data = pickle.load(f)`.
* **CORS Policy Blocking Frontend**
    * **Problem**: Frontend blocked by backend due to CORS.
    * **Solution**: Implemented `flask_cors.CORS(app)`.
* **404 / 405 Errors on `/recommend`**
    * **Problem**: Flask endpoint inaccessible or "Method Not Allowed".
    * **Solution**: Ensured `methods=["POST"]` and verified URL; used Postman for testing.
* **Case Sensitivity in Input**
    * **Problem**: Strict movie title matching failed on case/hyphens.
    * **Solution**: Normalized input with `.lower()` and implemented fuzzy matching (`difflib`).
* **CORS Working in Postman but Not in Browser**
    * **Problem**: Browser enforced CORS, Postman didn't.
    * **Solution**: Ensured `CORS(app)` was called before any route definition.
* **Frontend `.map()` Error**
    * **Problem**: Backend response not in expected shape for `.map()`.
    * **Solution**: Ensured backend returned `{"recommendations": [...]}` and destructured correctly.
* **Hosting Integration & Debugging**
    * **Problem**: Silent failures on Vercel, debugging deployment issues.
    * **Solution**: Used browser DevTools, console logs, and verified main branch deployments.

## 🌐 Deployment

* **Backend**: Render
* **Frontend**: Vercel



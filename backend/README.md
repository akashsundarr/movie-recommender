
# 🐍 Movie Recommender Backend

This is the Flask backend for the Movie Recommendation System. It serves a REST API that provides movie recommendations using a pre-trained machine learning model.

## 🚀 Tech Stack

* **Language**: Python

* **Web Framework**: Flask 🧪

* **Libraries**: `scikit-learn` 🧠, `pandas` 🐼, `pickle`, `gdown`

* **Deployment**: Render ☁️

## ⚙️ How to Run Locally

1. Navigate to the `backend/` directory:

```

cd movie-recommender/backend

```

2. Install dependencies from `requirements.txt`:

```

pip install -r requirements.txt

```

3. Run the Flask application:

```

python app.py

```

The API will be available at `http://127.0.0.1:5000`. The `model.pkl` file will be automatically downloaded from Google Drive if it doesn't exist.

## 🌐 Live Link

* **Backend API Base URL**: <https://movie-recommender-bit5.onrender.com>

## 🔧 API Endpoint

The backend provides a single endpoint for recommendations:

* **Endpoint**: `POST /recommend`

* **Request Body**:

```

{
"movie": "Iron Man"
}

```

* **Response Body**:

```

{
"recommendations": [
"Movie Title 1",
"Movie Title 2",
"Movie Title 3",
"Movie Title 4",
"Movie Title 5"
]
}

```
```

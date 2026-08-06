# Spam Detection System

A complete machine learning-powered Spam Detection System built from scratch. It uses a modern React frontend and a FastAPI backend, coupled with a Scikit-learn model trained on the SMS Spam Collection dataset.

## Features
- **Machine Learning**: TF-IDF Vectorization and Multinomial Naive Bayes classification (97.4% accuracy).
- **Backend**: FastAPI providing blazing fast endpoints.
- **Database**: SQLite tracking all predictions and confidence scores for historical reference.
- **Frontend**: A sleek, dynamic, glassmorphism-inspired React interface built with Vite.

## Tech Stack
- **Frontend**: React, Vite, Axios, Vanilla CSS
- **Backend**: FastAPI, Uvicorn, SQLAlchemy
- **Machine Learning**: Scikit-learn, Pandas, Joblib
- **Database**: SQLite

---

## Getting Started

### 1. Backend Setup

1. **Activate the Virtual Environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Train the Model** (Only required once, already completed):
   ```powershell
   python backend\train.py
   ```
   *This downloads the dataset, trains the Naive Bayes model, and saves `model.pkl` and `vectorizer.pkl`.*

3. **Run the FastAPI Server**:
   ```powershell
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://localhost:8000`. You can view the interactive Swagger docs at `http://localhost:8000/docs`.

### 2. Frontend Setup

1. **Navigate to the frontend directory**:
   ```powershell
   cd frontend
   ```

2. **Run the React Development Server**:
   ```powershell
   npm run dev
   ```
   The UI will be available at `http://localhost:5173`.

---

## API Endpoints
- `POST /predict`: Submit `{"text": "your message"}` to receive a Spam/Ham prediction and confidence score.
- `GET /history`: Retrieve a list of all historical predictions stored in the database.
Testing GitHub Actions

import os
import joblib
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spam Detection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


VECTORIZER = None
MODEL = None
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

@app.on_event("startup")
def load_model():
    global VECTORIZER, MODEL
    vectorizer_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    
    if os.path.exists(vectorizer_path) and os.path.exists(model_path):
        VECTORIZER = joblib.load(vectorizer_path)
        MODEL = joblib.load(model_path)
    else:
        print("Warning: Model files not found. Please train the model first.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict", response_model=schemas.PredictionResponse)
def predict_spam(request: schemas.PredictionCreate, db: Session = Depends(get_db)):
    if VECTORIZER is None or MODEL is None:
        raise HTTPException(status_code=500, detail="Machine learning models are not loaded.")

    text = request.text
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    
    text_vec = VECTORIZER.transform([text])
    pred_val = MODEL.predict(text_vec)[0]
    probs = MODEL.predict_proba(text_vec)[0]
    confidence = max(probs)
    
    
    result_label = "Spam" if pred_val == "spam" else "Ham"

    
    db_prediction = models.Prediction(
        text=text,
        prediction=result_label,
        confidence=float(confidence)
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return db_prediction

@app.get("/history", response_model=List[schemas.PredictionResponse])
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    predictions = db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).offset(skip).limit(limit).all()
    return predictions

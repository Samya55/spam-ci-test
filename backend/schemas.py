from pydantic import BaseModel
from datetime import datetime

class PredictionCreate(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    id: int
    text: str
    prediction: str
    confidence: float
    timestamp: datetime

    class Config:
        from_attributes = True

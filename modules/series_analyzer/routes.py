from fastapi import APIRouter
from pydantic import BaseModel
from modules.series_analyzer import service

router = APIRouter()

class SeriesInput(BaseModel):
    sequence: list[int]

@router.get("/")
def home():
    return {"message": "Welcome to Number Series Predictor API 🔢"}

@router.post("/predict")
def predict_next(data: SeriesInput):
    """
    Predict the next term in a number series.
    Works for simple (arithmetic, geometric, Fibonacci, square, cube)
    and complex patterns using ML-like heuristics.
    """
    return service.predict_next_term(data.sequence)

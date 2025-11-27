from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .model_loader import stock_ann

router = APIRouter(
    prefix="/stock",
    tags=["Stock Price Predictor (ANN - Trained on Real Data)"]
)

class PriceInput(BaseModel):
    previous_prices: list[float]

@router.post("/predict")
async def predict_stock_price(data: PriceInput):
    if len(data.previous_prices) != 5:
        raise HTTPException(status_code=400, detail="Send exactly 5 previous close prices")

    next_price = stock_ann.predict_next(data.previous_prices)

    return {
        "next_day_prediction": next_price
    }

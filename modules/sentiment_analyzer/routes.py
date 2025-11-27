# app/modules/sentiment_analyzer/routes.py

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .model_loader import sentiment_analyzer


router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment Analysis (Neural ANN Application)"]
)


class SentimentRequest(BaseModel):
    """
    Request body for sentiment analysis.

    You can send:
    - text: single sentence/string
    OR
    - texts: list of multiple sentences/strings
    """
    text: Optional[str] = Field(
        default=None,
        description="Single text to analyze."
    )
    texts: Optional[List[str]] = Field(
        default=None,
        description="Multiple texts to analyze as a batch."
    )

    def get_texts(self) -> List[str]:
        """
        Helper to normalize the input:
        - If both provided -> error
        - If one provided -> return list of texts
        """
        if self.text and self.texts:
            raise ValueError("Provide either 'text' or 'texts', not both.")
        if self.text:
            return [self.text]
        if self.texts:
            if len(self.texts) == 0:
                raise ValueError("'texts' cannot be an empty list.")
            return self.texts
        raise ValueError("You must provide 'text' or 'texts'.")  # nothing provided


@router.get(
    "/",
    summary="Sentiment Analysis API Overview",
    description=(
        "Landing endpoint for the Sentiment Analysis (Neural ANN) service. "
        "Explains how to use the /sentiment/analyze endpoint with examples."
    ),
)
async def sentiment_home():
    return {
        "service": "Sentiment Analysis (Neural ANN Application)",
        "description": (
            "This service classifies text as POSITIVE or NEGATIVE using "
            "a pre-trained neural network (DistilBERT)."
        ),
        "use_cases": [
            "Product review analysis",
            "Social media / tweet classification",
            "Customer feedback monitoring",
            "Movie / app review dashboards",
        ],
        "how_to_use": {
            "single_text": {
                "method": "POST",
                "url": "/sentiment/analyze",
                "content_type": "application/json",
                "body_example": {
                    "text": "FastAPI makes backend development really enjoyable!"
                },
            },
            "batch_text": {
                "method": "POST",
                "url": "/sentiment/analyze",
                "content_type": "application/json",
                "body_example": {
                    "texts": [
                        "I love this product.",
                        "This service is terrible.",
                        "The UI is okay but could be better."
                    ]
                },
            },
        },
        "testing": {
            "swagger_ui": "/docs",
            "redoc_ui": "/redoc",
        },
        "integration_hint": (
            "From your frontend, send a POST request with JSON body "
            "to /sentiment/analyze and read back 'label' and 'score' "
            "for each text."
        ),
    }


@router.post(
    "/analyze",
    summary="Analyze sentiment for given text(s)",
    description=(
        "Send a single 'text' field or a list of 'texts' in the request body. "
        "Returns POSITIVE / NEGATIVE label with a confidence score (0-1)."
    ),
)
async def analyze_sentiment(payload: SentimentRequest):
    # Validate and normalize input
    try:
        texts = payload.get_texts()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Single text
    if len(texts) == 1:
        result = sentiment_analyzer.analyze_one(texts[0])
        return {
            "input": texts[0],
            "sentiment": result["label"],
            "confidence": result["score"],
        }

    # Batch of texts
    results = sentiment_analyzer.analyze_batch(texts)
    return {
        "inputs": texts,
        "results": [
            {
                "sentiment": r["label"],
                "confidence": r["score"],
            }
            for r in results
        ],
    }

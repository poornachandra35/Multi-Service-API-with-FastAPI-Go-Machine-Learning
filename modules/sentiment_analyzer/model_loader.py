# app/modules/sentiment_analyzer/model_loader.py

from typing import List, Dict, Any

from transformers import pipeline


class SentimentAnalyzer:
    """
    Wrapper around a pre-trained neural sentiment model.
    Uses DistilBERT fine-tuned on SST-2 (positive/negative).
    """

    def __init__(self) -> None:
        # This will download the model on first run (if not cached).
        self._pipeline = pipeline(
            task="sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def analyze_one(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of a single text."""
        result = self._pipeline(text)[0]  # [{'label': 'POSITIVE', 'score': 0.99}]
        return {
            "label": result["label"],
            "score": float(result["score"]),
        }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze sentiment of a list of texts in batch."""
        raw_results = self._pipeline(texts)
        return [
            {"label": r["label"], "score": float(r["score"])}
            for r in raw_results
        ]


# Single shared instance used by the FastAPI routes
sentiment_analyzer = SentimentAnalyzer()

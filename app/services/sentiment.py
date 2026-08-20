import asyncio
from typing import Final, Literal

from pydantic import BaseModel, Field

SentimentLabel = Literal["positive", "negative", "neutral"]


class SentimentPrediction(BaseModel):
    label: SentimentLabel
    score: float = Field(ge=0.0, le=1.0)


class PredictionError(RuntimeError):
    pass


POSITIVE_KEYWORDS: Final[frozenset[str]] = frozenset(
    {"good", "great", "love", "happy", "棒", "喜歡", "開心"}
)
NEGATIVE_KEYWORDS: Final[frozenset[str]] = frozenset(
    {"bad", "hate", "sad", "terrible", "爛", "討厭", "難過"}
)


def _count_hits(normalized_text: str, keywords: frozenset[str]) -> int:
    return sum(normalized_text.count(keyword) for keyword in keywords)


def _confidence(diff: int) -> float:
    return min(0.95, 0.6 + 0.1 * diff)


def _classify(text: str) -> SentimentPrediction:
    normalized = text.lower()
    positive_hits = _count_hits(normalized, POSITIVE_KEYWORDS)
    negative_hits = _count_hits(normalized, NEGATIVE_KEYWORDS)

    if positive_hits > negative_hits:
        diff = positive_hits - negative_hits
        return SentimentPrediction(label="positive", score=_confidence(diff))

    if negative_hits > positive_hits:
        diff = negative_hits - positive_hits
        return SentimentPrediction(label="negative", score=_confidence(diff))

    return SentimentPrediction(label="neutral", score=0.5)


async def predict_sentiment(text: str) -> SentimentPrediction:
    stripped = text.strip()
    if not stripped:
        raise PredictionError("text is empty")

    await asyncio.sleep(0)
    return _classify(stripped)

from fastapi import APIRouter, HTTPException

from app.api.schemas import PredictRequest, PredictResponse
from app.services.sentiment import PredictionError, predict_sentiment

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest) -> PredictResponse:
    try:
        prediction = await predict_sentiment(payload.text)
    except PredictionError as exc:
        raise HTTPException(status_code=500, detail="prediction_failed") from exc

    return PredictResponse(label=prediction.label, score=prediction.score)

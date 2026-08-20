from pydantic import BaseModel, Field, StrictStr, field_validator

from app.services.sentiment import SentimentLabel


class PredictRequest(BaseModel):
    text: StrictStr = Field(min_length=1, max_length=500)

    @field_validator("text")
    @classmethod
    def validate_text_not_empty_after_strip(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("text must not be empty after stripping whitespace")
        return stripped


class PredictResponse(BaseModel):
    label: SentimentLabel
    score: float = Field(ge=0.0, le=1.0)

import pytest
from pydantic import ValidationError

from app.api.schemas import PredictRequest, PredictResponse


def test_predict_request_strips_text() -> None:
    payload = PredictRequest(text="  hello ")

    assert payload.text == "hello"


def test_predict_request_requires_text() -> None:
    with pytest.raises(ValidationError):
        PredictRequest.model_validate({})


def test_predict_request_rejects_empty_string() -> None:
    with pytest.raises(ValidationError):
        PredictRequest(text="")


def test_predict_request_rejects_whitespace_only() -> None:
    with pytest.raises(ValidationError):
        PredictRequest(text="   ")


def test_predict_request_rejects_non_string() -> None:
    with pytest.raises(ValidationError):
        PredictRequest.model_validate({"text": 123})


def test_predict_request_rejects_too_long_text() -> None:
    with pytest.raises(ValidationError):
        PredictRequest(text="a" * 501)


def test_predict_request_accepts_boundary_length_text() -> None:
    payload = PredictRequest(text="a" * 500)

    assert len(payload.text) == 500


def test_predict_response_accepts_valid_payload() -> None:
    payload = PredictResponse(label="positive", score=0.9)

    assert payload.label == "positive"
    assert payload.score == 0.9


def test_predict_response_rejects_invalid_label() -> None:
    with pytest.raises(ValidationError):
        PredictResponse.model_validate({"label": "angry", "score": 0.5})


def test_predict_response_rejects_score_above_one() -> None:
    with pytest.raises(ValidationError):
        PredictResponse(label="positive", score=1.1)


def test_predict_response_rejects_negative_score() -> None:
    with pytest.raises(ValidationError):
        PredictResponse(label="positive", score=-0.1)

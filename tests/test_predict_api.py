from unittest.mock import AsyncMock

from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.services.sentiment import PredictionError, SentimentPrediction


async def test_predict_success_returns_label_and_score(
    client: AsyncClient,
    mocker: MockerFixture,
) -> None:
    prediction = SentimentPrediction(label="positive", score=0.9)
    mock_predict = AsyncMock(return_value=prediction)
    mocker.patch("app.api.routes.predict_sentiment", new=mock_predict)

    response = await client.post("/predict", json={"text": "  great "})

    assert response.status_code == 200
    assert response.json() == {"label": "positive", "score": 0.9}
    mock_predict.assert_awaited_once_with("great")


async def test_predict_uses_stripped_text(
    client: AsyncClient,
    mocker: MockerFixture,
) -> None:
    prediction = SentimentPrediction(label="neutral", score=0.5)
    mock_predict = AsyncMock(return_value=prediction)
    mocker.patch("app.api.routes.predict_sentiment", new=mock_predict)

    response = await client.post("/predict", json={"text": "\n hello \n"})

    assert response.status_code == 200
    mock_predict.assert_awaited_once_with("hello")


async def test_predict_service_error_returns_500(
    client: AsyncClient,
    mocker: MockerFixture,
) -> None:
    mock_predict = AsyncMock(side_effect=PredictionError("boom"))
    mocker.patch("app.api.routes.predict_sentiment", new=mock_predict)

    response = await client.post("/predict", json={"text": "hello"})

    assert response.status_code == 500
    assert response.json() == {"detail": "prediction_failed"}
    mock_predict.assert_awaited_once_with("hello")


async def test_predict_integration_with_builtin_mock_model(
    client: AsyncClient,
) -> None:
    response = await client.post("/predict", json={"text": "I love this"})

    assert response.status_code == 200

    payload = response.json()
    assert payload["label"] == "positive"
    assert 0.0 <= payload["score"] <= 1.0


async def test_missing_text_returns_422(client: AsyncClient) -> None:
    response = await client.post("/predict", json={})

    assert response.status_code == 422


async def test_empty_text_returns_422(client: AsyncClient) -> None:
    response = await client.post("/predict", json={"text": ""})

    assert response.status_code == 422


async def test_whitespace_text_returns_422_and_does_not_call_service(
    client: AsyncClient,
    mocker: MockerFixture,
) -> None:
    mock_predict = AsyncMock()
    mocker.patch("app.api.routes.predict_sentiment", new=mock_predict)

    response = await client.post("/predict", json={"text": "   "})

    assert response.status_code == 422
    mock_predict.assert_not_awaited()


async def test_too_long_text_returns_422(client: AsyncClient) -> None:
    response = await client.post("/predict", json={"text": "a" * 501})

    assert response.status_code == 422


async def test_boundary_length_text_returns_200(
    client: AsyncClient,
    mocker: MockerFixture,
) -> None:
    prediction = SentimentPrediction(label="neutral", score=0.5)
    mock_predict = AsyncMock(return_value=prediction)
    mocker.patch("app.api.routes.predict_sentiment", new=mock_predict)
    text = "a" * 500

    response = await client.post("/predict", json={"text": text})

    assert response.status_code == 200
    mock_predict.assert_awaited_once_with(text)


async def test_non_string_text_returns_422(client: AsyncClient) -> None:
    response = await client.post("/predict", json={"text": 123})

    assert response.status_code == 422

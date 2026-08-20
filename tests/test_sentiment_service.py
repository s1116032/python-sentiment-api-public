import pytest

from app.services.sentiment import PredictionError, predict_sentiment


async def test_positive_text_returns_positive() -> None:
    result = await predict_sentiment("I love this great feature")

    assert result.label == "positive"
    assert 0.0 <= result.score <= 1.0


async def test_negative_text_returns_negative() -> None:
    result = await predict_sentiment("This is bad and sad")

    assert result.label == "negative"
    assert 0.0 <= result.score <= 1.0


async def test_neutral_text_returns_neutral() -> None:
    result = await predict_sentiment("The meeting is scheduled tomorrow")

    assert result.label == "neutral"
    assert result.score == 0.5


async def test_positive_chinese_text_returns_positive() -> None:
    result = await predict_sentiment("這個功能很棒")

    assert result.label == "positive"
    assert 0.0 <= result.score <= 1.0


async def test_negative_chinese_text_returns_negative() -> None:
    result = await predict_sentiment("這個設計很爛")

    assert result.label == "negative"
    assert 0.0 <= result.score <= 1.0


async def test_case_insensitive_positive_text() -> None:
    result = await predict_sentiment("GOOD Love")

    assert result.label == "positive"


async def test_equal_positive_and_negative_hits_return_neutral() -> None:
    result = await predict_sentiment("good bad")

    assert result.label == "neutral"
    assert result.score == 0.5


async def test_score_is_capped_at_0_95() -> None:
    result = await predict_sentiment("good " * 20)

    assert result.label == "positive"
    assert result.score == 0.95


async def test_empty_text_raises_prediction_error() -> None:
    with pytest.raises(PredictionError):
        await predict_sentiment("")


async def test_whitespace_only_text_raises_prediction_error() -> None:
    with pytest.raises(PredictionError):
        await predict_sentiment("   ")

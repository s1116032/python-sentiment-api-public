from app.main import app


def test_app_has_predict_route() -> None:
    paths = app.openapi().get("paths", {})

    assert "/predict" in paths

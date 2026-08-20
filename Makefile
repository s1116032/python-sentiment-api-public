.PHONY: install format lint typecheck test check ci

install:
	uv sync --all-extras

format:
	uv run ruff check --fix .
	uv run black .

lint:
	uv run ruff check .
	uv run black --check .

typecheck:
	uv run mypy .

test:
	uv run pytest

check: lint typecheck test

ci: lint typecheck test
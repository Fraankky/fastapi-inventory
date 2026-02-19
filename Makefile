format:
	uv run ruff check --fix --unsafe-fixes

lint:
 	uv run ruff check

dev: 
	uv run uvicorn app.main:app --reload
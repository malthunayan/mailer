pre-commit: format lint test

format:
	poetry run isort .
	poetry run black .
lint:
	poetry run mypy .
	poetry run pylint mailer/ tests/
test:
	poetry run pytest

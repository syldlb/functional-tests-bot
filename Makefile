.PHONY: pytest
pytest:
	pytest

.PHONY: black
black:
	black .

.PHONY: black-check
black-check:
	black --check .

.PHONY: flake8
flake8:
	flake8

.PHONY: tests
tests: pytest black-check flake8

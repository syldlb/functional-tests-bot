.PHONY: pytest
pytest:
	pytest --cov=helpers

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

.PHONE: coverage
coverage:
	coverage run --source main.py helpers.py -m pytest

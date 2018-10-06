init:
	pip install -r requirements.txt && pip install -e .

test:
	pytest --cov-report term-missing --cov=ac tests

.PHONY: init test

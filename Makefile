init:
	pip install -r requirements.txt | pip install -e .

test:
	pytest tests

.PHONY: init test

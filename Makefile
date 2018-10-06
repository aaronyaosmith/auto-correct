init:
	pip install -r requirements.txt && pip install -e .

test:
	pytest --cov-report term-missing --cov=ac tests

run:
	export FLASK_APP='ac/ac.py' && flask run

.PHONY: init test

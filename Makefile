install:
	pip install -r requirements.txt

format:
	black */*.py
	isort */*.py


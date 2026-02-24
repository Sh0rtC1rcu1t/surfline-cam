<<<<<<< Updated upstream
# Convenience Makefile
.PHONY: serve test

serve:
	uvicorn server.main:app --reload

test:
	pytest -q
=======
.PHONY: help install dev test lint clean

help:
	@echo "Surfline Camera API - Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make dev        Run development server"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linting checks"
	@echo "  make clean      Remove cache files"

install:
	python3 -m pip install -r requirements.txt

dev:
	python3 -m uvicorn main:app --reload

test:
	python3 -m pytest test_main.py -v

lint:
	@echo "Running linting checks..."
	@python3 -m py_compile main.py test_main.py
	@echo "All files compiled successfully"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
>>>>>>> Stashed changes

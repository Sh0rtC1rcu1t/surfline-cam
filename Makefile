# Dev Makefile for Agent Assistance service
SHELL := /bin/sh

PYTHON ?= python3
UVICORN ?= uvicorn

# Auto-detect the app module: prefer server/main.py -> server.main:app, else main.py -> main:app
APP_MODULE ?= $(shell if [ -f server/main.py ]; then echo server.main:app; elif [ -f main.py ]; then echo main:app; else echo main:app; fi)

.PHONY: help install dev serve test lint clean
.DEFAULT_GOAL := help

help:
	@echo "Agent Assistance - Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make dev        Run development server (auto-reload)"
	@echo "  make serve      Alias for dev"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linting/compile checks"
	@echo "  make clean      Remove cache files"

install:
	@if [ -f requirements.txt ]; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "requirements.txt not found. Skipping dependency install."; \
	fi

dev: serve

serve:
	$(UVICORN) $(APP_MODULE) --reload

test:
	@if [ -f test_main.py ]; then \
		$(PYTHON) -m pytest test_main.py -v; \
	else \
		$(PYTHON) -m pytest -q; \
	fi

lint:
	@echo "Running linting checks..."
	@$(PYTHON) - <<'PY'
import compileall, sys
ok = compileall.compile_dir('.', quiet=1)
sys.exit(0 if ok else 1)
PY
	@echo "All files compiled successfully"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage

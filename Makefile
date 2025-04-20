.PHONY: install test lint format clean build run deploy

# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8
MYPY = mypy
NPM = npm

# Installation
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	pre-commit install
	cd frontend && $(NPM) install

# Testing
test:
	$(PYTEST) tests/ --cov=src --cov-report=term-missing

# Linting
lint:
	$(FLAKE8) src tests
	$(MYPY) src tests
	cd frontend && $(NPM) run lint

# Formatting
format:
	$(BLACK) src tests
	$(ISORT) src tests
	cd frontend && $(NPM) run format

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	cd frontend && $(NPM) run clean

# Building
build:
	$(PYTHON) setup.py sdist bdist_wheel
	cd frontend && $(NPM) run build

# Running
run:
	uvicorn src.api.main:app --reload

# Deployment
deploy:
	docker-compose up --build -d

# Database
migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1

# Documentation
docs:
	cd docs && make html

# Development
dev:
	make install
	make format
	make lint
	make test

# All
all: clean install test lint format build 
# Variables
PYTHON = .venv/bin/python
PIP = .venv/bin/pip

.PHONY: help venv install dev test run build clean docker-build docker-run lint lint-fix

help:
	@echo "Available commands:"
	@echo "  make venv          - Create a fresh .venv"
	@echo "  make install       - Install terraflow-agro in editable mode into .venv"
	@echo "  make dev           - Install terraflow-agro + dev dependencies"
	@echo "  make test          - Run unit tests"
	@echo "  make run           - Run example workflow"
	@echo "  make build         - Build wheel + sdist"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker image"
	@echo "  make release       - Bump version, tag, and push"

# ---------------------------
# Environment setup
# ---------------------------

venv:
	python3 -m venv .venv
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -e .

dev: venv
	$(PIP) install -e ".[dev]"

# ---------------------------
# Testing & Running
# ---------------------------

test:
	$(PYTHON) -m pytest -v

# ---------------------------
# Build & Release
# ---------------------------

build:
	$(PIP) install --upgrade build
	$(PYTHON) -m build

clean:
	rm -rf build dist *.egg-info
	find . -name "__pycache__" -exec rm -rf {} +

lint:
	ruff check trialflow_agro tests
	black --check trialflow_agro tests

lint-fix:
	ruff check trialflow_agro tests --fix
	black trialflow_agro tests
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: clean build build-dev test run

build:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	$(PIP) install .

build-dev:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements_dev.txt
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

test:
	$(VENV)/bin/pytest
	$(VENV)/bin/flake8 app tests
	$(VENV)/bin/mypy app

run:
	$(PYTHON) app/main.py

clean:
	rm -rf .venv
	rm -rf build/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf __pycache__/

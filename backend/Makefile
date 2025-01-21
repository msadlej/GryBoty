VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: clean build build-dev test run

all: build-dev test run

build:
	@echo "Building the project..."
	@python3 -m venv $(VENV)
	@$(PIP) install .
	@echo "Successfully built the project."

build-dev:
	@echo "Building the project in development mode..."
	@python3 -m venv $(VENV)
	@$(PIP) install -e .[testing]
	@echo "Successfully built the project in development mode."

test:
	$(VENV)/bin/pytest
	$(VENV)/bin/flake8 src/app tests
	$(VENV)/bin/mypy src/app

run:
	$(PYTHON) src/app/main.py

clean:
	rm -rf .venv
	rm -rf build/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf __pycache__/

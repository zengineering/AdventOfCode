VENV_NAME := aoc.venv
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip

.PHONY: all
all: venv test format

venv: $(VENV_NAME)/bin/activate.fish

$(VENV_NAME)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created. Activate it with 'source $(VENV_NAME)/bin/activate'."

.PHONY: format
format: venv
	@echo "Formatting code with ruff..."
	$(PYTHON) -m ruff format .
	@echo "Code formatting completed."

.PHONY: lint
lint: venv
	@echo "Linting code with ruff..."
	$(PYTHON) -m ruff check .
	@echo "Code linting completed."

.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	@echo "Cleanup completed."

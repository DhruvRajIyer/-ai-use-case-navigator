# Makefile for AI Use Case Navigator

.PHONY: setup install run clean help

# Configuration
VENV_NAME := .venv
PYTHON := python3
PIP := pip
REQUIREMENTS := requirements.txt
APP := app.py

help:
	@echo "AI Use Case Navigator - Available commands:"
	@echo "  make setup      - Create virtual environment and install dependencies"
	@echo "  make install    - Install dependencies in the current environment"
	@echo "  make run        - Run the Streamlit application"
	@echo "  make clean      - Remove virtual environment and cached files"
	@echo "  make help       - Show this help message"

setup:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@echo "Activating virtual environment and installing dependencies..."
	@. $(VENV_NAME)/bin/activate && $(PIP) install -r $(REQUIREMENTS)
	@echo "Setup complete. Use 'make run' to start the application."

install:
	@echo "Installing dependencies..."
	@$(PIP) install -r $(REQUIREMENTS)
	@echo "Installation complete."

run:
	@echo "Starting Streamlit application..."
	@streamlit run $(APP)

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV_NAME)
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@rm -rf .streamlit
	@echo "Clean complete."

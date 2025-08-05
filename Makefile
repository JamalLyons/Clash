# Clash Project Makefile
# This Makefile provides convenient commands for managing the Clash project

.PHONY: help install run clean venv venv-activate venv-deactivate test setup

# Default target
help:
	@echo "Clash Project - Available Commands:"
	@echo ""
	@echo "Environment Management:"
	@echo "  make venv          - Create a new Python virtual environment"
	@echo "  make venv-activate - Activate the virtual environment"
	@echo "  make venv-deactivate - Deactivate the virtual environment"
	@echo ""
	@echo "Dependencies:"
	@echo "  make install       - Install project dependencies"
	@echo "  make setup         - Create venv and install dependencies"
	@echo ""
	@echo "Running the Project:"
	@echo "  make run           - Run the main clash.py script"
	@echo "  make test          - Run the tester.py script"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         - Remove virtual environment and cache files"
	@echo ""

# Virtual environment name
VENV_NAME = venv

# Create virtual environment
venv:
	@echo "Creating Python virtual environment..."
	python3 -m venv $(VENV_NAME)
	@echo "Virtual environment created successfully!"
	@echo "To activate it, run: make venv-activate"

# Activate virtual environment
venv-activate:
	@echo "Activating virtual environment..."
	@echo "Run this command in your shell:"
	@echo "source $(VENV_NAME)/bin/activate"
	@echo ""
	@echo "Or use: make venv-activate-exec"

# Activate and execute a command in the virtual environment
venv-activate-exec:
	@echo "Activating virtual environment and executing command..."
	@source $(VENV_NAME)/bin/activate && $(CMD)

# Deactivate virtual environment
venv-deactivate:
	@echo "To deactivate the virtual environment, run:"
	@echo "deactivate"

# Install dependencies
install:
	@echo "Installing project dependencies..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "Virtual environment not found. Creating one first..."; \
		make venv; \
	fi
	@source $(VENV_NAME)/bin/activate && pip install --upgrade pip
	@source $(VENV_NAME)/bin/activate && pip install -r requirements.txt
	@echo "Dependencies installed successfully!"

# Setup project (create venv and install dependencies)
setup: venv install
	@echo "Project setup complete!"
	@echo "To run the project: make run"

# Run the main clash.py script
run:
	@echo "Running Clash project..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "Virtual environment not found. Please run 'make setup' first."; \
		exit 1; \
	fi
	@source $(VENV_NAME)/bin/activate && python src/clash.py

# Run the tester script
test:
	@echo "Running tester script..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "Virtual environment not found. Please run 'make setup' first."; \
		exit 1; \
	fi
	@source $(VENV_NAME)/bin/activate && python src/tester.py

# Clean up virtual environment and cache files
clean:
	@echo "Cleaning up project..."
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "Removing virtual environment..."; \
		rm -rf $(VENV_NAME); \
	fi
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@echo "Cleanup complete!"

# Quick start - setup and run
quick-start: setup run

# Development mode - setup and run with auto-restart
dev: setup
	@echo "Starting development mode..."
	@echo "Press Ctrl+C to stop"
	@while true; do \
		source $(VENV_NAME)/bin/activate && python src/clash.py; \
		echo "Restarting in 3 seconds..."; \
		sleep 3; \
	done 
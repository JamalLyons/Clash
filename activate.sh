#!/bin/bash

# Clash Project Virtual Environment Activator
# This script activates the Python virtual environment for the Clash project

VENV_NAME="venv"

echo "Clash Project - Virtual Environment Activator"
echo "============================================="

# Check if virtual environment exists
if [ ! -d "$VENV_NAME" ]; then
    echo "Virtual environment not found!"
    echo "Creating virtual environment and installing dependencies..."
    make setup
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

echo ""
echo "Virtual environment activated successfully!"
echo "You can now run:"
echo "  - python src/clash.py    (main script)"
echo "  - python src/tester.py   (tester script)"
echo ""
echo "To deactivate, run: deactivate"
echo ""

# Start an interactive shell with the activated environment
exec "$SHELL" 
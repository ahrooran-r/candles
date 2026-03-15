#!/bin/bash

# Ensure script runs from the project root
cd "$(dirname "$0")" || exit

VENV_DIR=".venv"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment (.venv)..."
    uv venv
fi

# Verify activation script exists
if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    echo "Error: Activation script not found: $ACTIVATE_SCRIPT" >&2
    exit 1
fi

# Activate environment
echo "Activating virtual environment..."
source "$ACTIVATE_SCRIPT"

# Install dependencies if lock file exists
if [ -f "uv.lock" ]; then
    echo "Syncing dependencies from uv.lock..."
    uv sync
else
    echo "No uv.lock found. Skipping dependency sync."
fi
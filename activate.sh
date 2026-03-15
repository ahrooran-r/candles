#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment (.venv)..."
    uv venv
fi

if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    echo "Error: Activation script not found: $ACTIVATE_SCRIPT" >&2
    return 1 2>/dev/null || exit 1
fi

if [ -f "uv.lock" ]; then
    echo "Syncing dependencies from uv.lock..."
    uv sync
else
    echo "No uv.lock found. Skipping dependency sync."
fi

echo "Activating virtual environment..."
source "$ACTIVATE_SCRIPT"
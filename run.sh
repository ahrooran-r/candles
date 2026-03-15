#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# I did not want to simply fastapi dev main.py because I wanted to control the server port from config file.
uv run python -m app.main
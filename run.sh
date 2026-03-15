#!/bin/bash

cd "$(dirname "$0")" || exit

# I did not want to simply fastapi dev main.py because I wanted to control the server port from config file.
uv run python -m app.main
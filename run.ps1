# The script is generated with the help of ChatGPT

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# I did not want to simply fastapi dev main.py because I wanted to control the server port from config file.
uv run python -m app.main
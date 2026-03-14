from pathlib import Path

# Source - https://stackoverflow.com/a/25389715
# __file__ is the path of current python file
# As per ChatGPT, I should not define shared constants in main.py file.
# But here now I must be careful not to change the file path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_DIR = PROJECT_ROOT / "config"

SERVER_ENV_FILE = ENV_DIR / "server.env"
DB_ENV_FILE = ENV_DIR / "db.env"
ALPHAVANTAGE_ENV_FILE = ENV_DIR / "alphavantage.env"

DB_SCHEMA = ENV_DIR / "schema.sql"

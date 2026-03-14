import sqlite3
from logging import getLogger, Logger
from pathlib import Path
from sqlite3 import Connection, Row

from app.config import db_settings
from app.util.PathUtils import PROJECT_ROOT

log: Logger = getLogger(__name__)


class Database:

    def __init__(self):
        self.db_path: Path = PROJECT_ROOT / db_settings.file_location

    def create_database(self) -> None:

        if self.db_path.exists():
            log.info("Database already exists at %s", self.db_path)

        else:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            log.info("Database initialized at %s", self.db_path)

    def get_connection(self) -> Connection:
        conn = sqlite3.connect(self.db_path)

        # Without setting row_factory, query results are returned as tuples.
        # When using Row, SQLite returns dictionary-like objects.
        conn.row_factory = Row

        return conn


# Singleton ? How to prevent creating new Database object?
database: Database = Database()

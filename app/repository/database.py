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

        # https://sqlite.org/pragma.html#pragma_journal_mode

        # 10MB cache
        conn.execute("PRAGMA cache_size = -10240")

        # similar to Postgres
        conn.execute("PRAGMA journal_mode = WAL")

        # This is supposed to be a read through cache.
        # Coupled with WAL, this is enough. As its said in the docs.
        conn.execute("PRAGMA synchronous = NORMAL")

        # No need to create transactions. the with clause auto commits / rollbacks
        # https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager
        return conn


# Singleton ? How to prevent creating new Database object?
database: Database = Database()

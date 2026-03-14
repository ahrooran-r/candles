from logging import getLogger, Logger
from pathlib import Path

from app.repository import database
from app.util.PathUtils import DB_SCHEMA

log: Logger = getLogger(__name__)


class Repository:

    def __init__(self) -> None:
        self.database = database

    def create_table_if_not_exists(self) -> None:
        schema_path: Path = Path(DB_SCHEMA)
        schema_sql = schema_path.read_text()

        # This is like a try with resources in Java
        with self.database.get_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()
            log.info("Executed schema script at: %s", schema_path)

repository: Repository = Repository()
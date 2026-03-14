from logging import getLogger, Logger
from pathlib import Path
from sqlite3 import Row, Cursor

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
        with self.database.get_connection() as connection:
            connection.executescript(schema_sql)
            connection.commit()
            log.info("Executed schema script at: %s", schema_path)

    def get_monthly_candles(self, symbol: str, year: int) -> list[Row] | None:
        symbol = symbol.upper()
        self._validate_year(year)

        query_template: str = "select * from ohlc_monthly where symbol = ? and year = ? order by month"

        with self.database.get_connection() as connection:
            cursor: Cursor = connection.execute(query_template, (symbol, year))
            rows: list[Row] = cursor.fetchall()
            return rows


repository: Repository = Repository()

from logging import getLogger, Logger
from pathlib import Path
from sqlite3 import Row, Cursor

from app.models import MonthlyCandle
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
            log.info("Executed schema script at: %s", schema_path)

    def get_monthly_candles(self, symbol: str, year: int) -> list[MonthlyCandle]:
        query_template: str = "select * from ohlc_monthly where symbol = ? and year = ? order by month"

        with self.database.get_connection() as connection:
            cursor: Cursor = connection.execute(query_template, (symbol, year))
            rows: list[Row] = cursor.fetchall()

            candles: list[MonthlyCandle] = []

            for row in rows:
                dictionary: dict = dict(row)
                candle: MonthlyCandle = MonthlyCandle.model_validate(dictionary)
                candles.append(candle)

            return candles

    def upsert_ohlc(self, candles: list[MonthlyCandle]) -> None:
        query_template: str = "insert into ohlc_monthly (symbol, year, month, last_trading_date, high, low, volume) values (:symbol, :year, :month, :last_trading_date, :high, :low, :volume) on conflict (symbol, year, month) do update set last_trading_date = excluded.last_trading_date, high = excluded.high, low = excluded.low, volume = excluded.volume"
        values: list[dict[str, str]] = [
            {
                **candle.model_dump(),
                "last_trading_date": candle.last_trading_date.isoformat(),
            }
            for candle in candles
        ]

        with self.database.get_connection() as connection:
            connection.executemany(query_template, values)


repository: Repository = Repository()

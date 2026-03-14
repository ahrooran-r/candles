from sqlite3 import Row

from app.models import Candle


class CandleAggregator:

    def __init__(self, rows: list[Row]):
        self.rows: list[Row] = rows
        self.high: float = 0.0
        self.low: float = 0.0
        self.volume: int = 0

    def aggregate(self) -> Candle:
        for row in self.rows:
            self.aggregate_row(row)

        candle: Candle = Candle(high=self.high, low=self.low, volume=self.volume)
        return candle

    def aggregate_row(self, row: Row) -> None:

        high: float = row["high"]
        if high > self.high:
            self.high = high

        low: float = row["low"]
        if low < self.low:
            self.low = low

        volume: int = row["volume"]
        self.volume += volume

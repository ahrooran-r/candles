from sqlite3 import Row

from app.models import YearlyCandle


class CandleAggregator:

    def __init__(self, rows: list[Row]):
        if not rows:
            raise ValueError("rows must not be empty")

        self.rows: list[Row] = rows
        self.high: float = self.rows[0]["high"]
        self.low: float = self.rows[0]["low"]
        self.volume: int = self.rows[0]["volume"]

    def aggregate(self) -> YearlyCandle:
        for row in self.rows[1:]:
            self.aggregate_row(row)

        candle: YearlyCandle = YearlyCandle(high=self.high, low=self.low, volume=self.volume)
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

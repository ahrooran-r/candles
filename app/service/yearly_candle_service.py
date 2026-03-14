from sqlite3 import Row

from app.models import Candle
from candle_aggregator import CandleAggregator
from app.repository import repository


class CandleService:

    def __init__(self, symbol: str, year: int):
        self.symbol = symbol
        self.year = year

    def get_yearly_candle(self) -> Candle:
        monthly_candles: list[Row] = repository.get_monthly_candles(self.symbol, self.year)

        aggregator: CandleAggregator = CandleAggregator(monthly_candles)
        yearly_candle: Candle = aggregator.aggregate()

        return yearly_candle

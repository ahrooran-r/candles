from sqlite3 import Row

from app.models import YearlyCandle, MonthlyCandle
from app.service.candle_aggregator import CandleAggregator
from app.repository import repository
from app.external import AlphavantageConnector


class CandleService:

    def __init__(self, symbol: str, year: int):
        self.symbol = symbol
        self.year = year

    def get_yearly_candle(self) -> YearlyCandle:
        monthly_candles: list[Row] = repository.get_monthly_candles(self.symbol, self.year)

        aggregator: CandleAggregator = CandleAggregator(monthly_candles)
        yearly_candle: YearlyCandle = aggregator.aggregate()

        return yearly_candle

    def update_db(self) -> None:
        connector: AlphavantageConnector = AlphavantageConnector(self.symbol)
        candles: list[MonthlyCandle] = connector.get_monthly_candles()
        repository.insert_ohlc(candles)

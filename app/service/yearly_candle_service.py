from logging import Logger, getLogger

from app.external import AlphavantageConnector
from app.models import YearlyCandle, MonthlyCandle
from app.repository import repository
from app.service.candle_aggregator import CandleAggregator

log: Logger = getLogger(__name__)


class CandleService:

    def __init__(self, symbol: str, year: int):
        self.symbol = symbol
        self.year = year

    def get_yearly_candle(self) -> YearlyCandle:
        # get monthly candle from DB for the provided symbol and year
        monthly_candles: list[MonthlyCandle] = repository.get_monthly_candles(self.symbol, self.year)

        if not monthly_candles:
            # if its not there, get from alpha vantage and update db

            log.warn(f"Unable to find candles for symbol: {self.symbol}, year: {self.year}. "
                     f"Will fetch from Alphavantage instead.")

            connector: AlphavantageConnector = AlphavantageConnector(self.symbol)
            monthly_candles: list[MonthlyCandle] = connector.get_monthly_candles()
            repository.upsert_ohlc(monthly_candles)

        log.debug(f"Found candles for symbol: {self.symbol}, year: {self.year} in local database.")

        # calculate the yearly candle from monthly candles
        aggregator: CandleAggregator = CandleAggregator(
            symbol=self.symbol,
            year=self.year,
            monthly_candles=monthly_candles
        )
        yearly_candle: YearlyCandle = aggregator.aggregate()

        return yearly_candle

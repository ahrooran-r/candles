from datetime import date, datetime
from logging import Logger, getLogger
from typing import Callable

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
        request_from_alphavantage: bool = False

        # check whether user requesting data for current year
        current_year: int = datetime.now().year
        is_current_year: bool = self.year == current_year

        # get monthly candle from DB for the provided symbol and year
        monthly_candles: list[MonthlyCandle] = repository.get_monthly_candles(self.symbol, self.year)

        if not monthly_candles:
            log.warning(f"Unable to find candles for symbol: {self.symbol}, year: {self.year}. Will fetch from Alphavantage instead.")

            request_from_alphavantage = True

        elif is_current_year:
            last_trading_date: date = self._get_last_trading_date(monthly_candles)
            is_last_updated_today: bool = last_trading_date == date.today()

            if not is_last_updated_today:
                log.warning(f"User requesting current year: {self.year} for symbol: {self.symbol}. The cache was updated on: {last_trading_date}. Will request latest data from Alphavantage and provide updated data")

                request_from_alphavantage = True

        if request_from_alphavantage:
            connector: AlphavantageConnector = AlphavantageConnector(self.symbol)

            monthly_candles: list[MonthlyCandle]
            if is_current_year:
                filter_current_year: Callable[[MonthlyCandle], bool] = lambda monthly_candle: monthly_candle.year == current_year
                monthly_candles = connector.get_monthly_candles(filter_current_year)
            else:
                monthly_candles = connector.get_monthly_candles()

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

    def _get_last_trading_date(self, monthly_candles: list[MonthlyCandle]) -> date:
        dates = [monthly_candle.last_trading_date for monthly_candle in monthly_candles]
        return max(dates)

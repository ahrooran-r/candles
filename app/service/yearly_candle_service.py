from collections.abc import Callable
from datetime import date, datetime, timedelta
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
        current_year: int = datetime.now().year
        is_current_year: bool = self.year == current_year

        monthly_candles: list[MonthlyCandle] = repository.get_monthly_candles(self.symbol, self.year)

        if not monthly_candles:
            log.warning(f"Unable to find candles for symbol: {self.symbol}, year: {self.year}. Will fetch from Alphavantage instead.")

            connector = AlphavantageConnector(self.symbol)
            monthly_candles: list[MonthlyCandle] = connector.get_monthly_candles()
            repository.upsert_ohlc(monthly_candles)

        elif is_current_year:
            last_updated_date: date = self._get_last_updated_date(monthly_candles)
            last_trading_date: date = self._get_last_trading_day()

            if last_updated_date != last_trading_date:
                log.warning(f"Current year: {self.year} cache is not up-to date for symbol: {self.symbol}. Cache updated on: {last_updated_date}. Last trading date: {last_trading_date}. Will only refresh for current year")

                connector = AlphavantageConnector(self.symbol)
                filter_current_year: Callable[[MonthlyCandle], bool] = lambda monthly_candle: monthly_candle.year == current_year
                monthly_candles: list[MonthlyCandle] = connector.get_monthly_candles(filter_current_year)
                repository.upsert_ohlc(monthly_candles)

        else:
            log.debug(f"Found candles for symbol: {self.symbol}, year: {self.year} in local database.")

        # calculate the yearly candle from monthly candles
        aggregator: CandleAggregator = CandleAggregator(
            symbol=self.symbol,
            year=self.year,
            monthly_candles=monthly_candles,
        )
        yearly_candle: YearlyCandle = aggregator.aggregate()

        return yearly_candle

    def _get_last_updated_date(self, monthly_candles: list[MonthlyCandle]) -> date:
        dates = [monthly_candle.last_trading_date for monthly_candle in monthly_candles]
        return max(dates)

    def _get_last_trading_day(self) -> date:
        today: date = date.today()
        weekday: int = today.weekday()

        # I am assuming Saturday and Sunday are weekends
        # I am used to exchanges having weekends in Friday and Saturday.
        # But now, assuming only American region, its okay to hardcode this
        if weekday == 5:
            return today - timedelta(days=1)

        if weekday == 6:
            return today - timedelta(days=2)

        return today

from collections.abc import Callable
from datetime import date, datetime, timedelta
from logging import Logger, getLogger

from app.exceptions import CandlesNotFoundError
from app.external import AlphavantageConnector
from app.models import YearlyCandle, MonthlyCandle, SymbolStatistics
from app.repository import repository
from app.service.candle_aggregator import CandleAggregator

log: Logger = getLogger(__name__)


class CandleService:

    def __init__(self, symbol: str, year: int):
        self.symbol = symbol

        # its not possible for year > datetime.now().year
        self.year = year

    def get_yearly_candle(self) -> YearlyCandle:
        current_year: int = datetime.now().year

        monthly_candles: list[MonthlyCandle] = repository.get_monthly_candles(self.symbol, self.year)
        data_available_in_cache: bool = bool(monthly_candles)

        if not data_available_in_cache:

            # user requesting for a previous year
            if self.year < current_year:
                # let's check earliest available date for this symbol
                statistics: SymbolStatistics = repository.get_earliest_available_year(self.symbol)

                # the only reason there is no data in sqlite is either symbol is not there or earliest_year > requested year (this.year)

                if not statistics.symbol:
                    log.warning(f"Unable to find candles for symbol: {self.symbol}, year: {self.year}. Will fetch from Alphavantage instead.")
                    monthly_candles = self._update_sqlite()

                else:
                    # if symbol is there, then only reason would be user requesting an earlier year than what is available
                    exception: CandlesNotFoundError = CandlesNotFoundError.requesting_earlier_year(self.symbol, self.year, statistics.earliest_year)
                    log.error(msg=str(exception), exc_info=exception)
                    raise exception

            else:
                log.warning(f"Unable to find candles for symbol: {self.symbol}, year: {self.year}. Will fetch from Alphavantage instead.")
                monthly_candles = self._update_sqlite()

        if data_available_in_cache and self.year == current_year:
            # if data available in SQLite, and if its current year -> then the data may be stale

            last_updated_date: date = self._get_last_updated_date(monthly_candles)
            last_trading_date: date = self._get_last_trading_day()

            if last_updated_date != last_trading_date:
                log.warning(f"Current year: {self.year} cache is not up-to date for symbol: {self.symbol}. Cache updated on: {last_updated_date}. Last trading date: {last_trading_date}. Will only refresh for current year")

                # TODO: This needs to be optimized. Maybe instead of relying on their last refreshed date, I should keep my last query time as well
                monthly_candles = self._update_sqlite(lambda monthly_candle: monthly_candle.year == current_year)

            else:
                log.debug(f"Found candles for symbol: {self.symbol}, year: {self.year} in cache.")

        else:
            log.debug(f"Found candles for symbol: {self.symbol}, year: {self.year} in cache.")

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

    def _update_sqlite(self, filter: Callable[[MonthlyCandle], bool] = lambda candle: True) -> list[MonthlyCandle]:
        connector = AlphavantageConnector(self.symbol)
        monthly_candles: list[MonthlyCandle] = connector.get_monthly_candles(filter)
        repository.upsert_ohlc(monthly_candles)
        return monthly_candles

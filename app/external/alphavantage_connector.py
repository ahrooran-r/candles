from collections.abc import Callable
from datetime import date
from typing import Any

import httpx
from httpx import Response

from app.config import alphavantage_settings
from app.models import MonthlyCandle


class AlphavantageConnector:
    """
    I am not adding retry mechanisms here. This class basically reacts on incoming request.
    Adding retry would slow down the response / error handling.
    Just fail fast

    I am also not adding rate limiting. Basically let Alphavantage return error message and throw exception.
    """

    def __init__(self, symbol: str) -> None:
        self.symbol: str = symbol
        self.url = f"https://{alphavantage_settings.domain}/query"

    def get_monthly_candles(
            self,
            filter: Callable[[MonthlyCandle], bool] = lambda candle: True
    ) -> list[MonthlyCandle]:
        response_body: dict[str, Any] = self._request_timeseries_monthly()
        monthly_candles: list[MonthlyCandle] = self._process_monthly_candles(response_body, filter)
        return monthly_candles

    def _process_monthly_candles(
            self,
            body: dict[str, Any],
            filter: Callable[[MonthlyCandle], bool]
    ) -> list[MonthlyCandle]:
        monthly_time_series: dict[str, dict[str, str]] = body["Monthly Time Series"]

        rows: list[MonthlyCandle] = []

        for _trading_date, ohlc in monthly_time_series.items():
            trading_date: date = date.fromisoformat(_trading_date)

            _high: str = ohlc["2. high"]
            high: float = float(_high)

            _low: str = ohlc["3. low"]
            low: float = float(_low)

            _volume: str = ohlc["5. volume"]
            volume: int = int(_volume)

            monthly_candle: MonthlyCandle = MonthlyCandle(
                symbol=self.symbol,
                year=trading_date.year,
                month=trading_date.month,
                last_trading_date=trading_date,
                high=high,
                low=low,
                volume=volume,
            )

            if filter(monthly_candle):
                rows.append(monthly_candle)

        return rows

    def _request_timeseries_monthly(self) -> dict[str, Any]:
        query_params: dict[str, str] = {
            "function": "TIME_SERIES_MONTHLY",
            "symbol": self.symbol,
            "apikey": alphavantage_settings.api_key,
        }

        # https://www.python-httpx.org/advanced/timeouts/
        timeout = httpx.Timeout(alphavantage_settings.request_timeout, connect=alphavantage_settings.connect_timeout)

        response: Response = httpx.get(url=self.url, params=query_params)
        response.raise_for_status()

        body: dict = response.json()
        return body

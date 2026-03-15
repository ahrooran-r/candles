from datetime import date
from typing import Any

import httpx
from httpx import Response

from app.config import alphavantage_settings

from app.models import MonthlyCandle


class AlphavantageConnector:

    def __init__(self, symbol: str) -> None:
        self.symbol: str = symbol
        self.function = "TIME_SERIES_MONTHLY"
        self.url = f"https://{alphavantage_settings.domain}/query"

    def get_monthly_candles(self) -> list[MonthlyCandle]:
        response_body: dict[str, Any] = self._request_monthly_candles()
        monthly_candles: list[MonthlyCandle] = self._process_monthly_candles(response_body)
        return monthly_candles

    def _process_monthly_candles(self, body: dict[str, Any]) -> list[MonthlyCandle]:
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

            row = MonthlyCandle(
                symbol=self.symbol,
                year=trading_date.year,
                month=trading_date.month,
                last_trading_date=trading_date,
                high=high,
                low=low,
                volume=volume,
            )

            rows.append(row)

        return rows

    def _request_monthly_candles(self) -> dict[str, Any]:
        query_params: dict[str, str] = {
            "function": self.function,
            "symbol": self.symbol,
            "apikey": alphavantage_settings.api_key,
        }
        response: Response = httpx.get(url=self.url, params=query_params)
        response.raise_for_status()

        body: dict = response.json()
        return body

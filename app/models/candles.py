from datetime import date

from pydantic import BaseModel


class YearlyCandle(BaseModel):
    high: float
    low: float
    volume: int


class MonthlyCandle(BaseModel):
    symbol: str
    year: int
    month: int
    last_trading_date: date

    high: float
    low: float
    volume: int

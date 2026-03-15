from datetime import date

from pydantic import BaseModel


class MonthlyCandle(BaseModel):
    symbol: str
    year: int
    month: int
    last_trading_date: date

    high: float
    low: float
    volume: int

    def get_last_trading_date(self) -> str:
        last_trading_date_string: str = self.last_trading_date.isoformat()
        return last_trading_date_string

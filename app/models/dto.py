from pydantic import BaseModel


class YearlyCandle(BaseModel):
    high: float
    low: float
    volume: int

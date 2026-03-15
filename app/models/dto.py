from pydantic import BaseModel


class YearlyCandle(BaseModel):
    high: str
    low: str
    volume: str
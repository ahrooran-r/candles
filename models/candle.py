from pydantic import BaseModel

class Candle(BaseModel):
    high: float
    low: float
    volume: int

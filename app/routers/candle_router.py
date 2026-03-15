from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path

from app.config import alphavantage_settings
from app.models import YearlyCandle
from app.service import CandleService

router = APIRouter()


@router.get("/symbols/{symbol}/annual/{year}")
def yearly_candle(
        symbol: Annotated[str, Path(min_length=1, max_length=50)],
        year: Annotated[int, Path(ge=alphavantage_settings.historical_depth, le=datetime.now().year)],
) -> YearlyCandle:
    """
    :param symbol: The name of the equity of your choice. For example: symbol=IBM
    :param year: should be between historical depth and current year
    :return: Candle for the given symbol and given year
    """

    symbol = symbol.upper()

    candle_service: CandleService = CandleService(symbol, year)
    candle: YearlyCandle
    try:
        candle = candle_service.get_yearly_candle()
    except ValueError as e:
        candle_service.update_db()
        candle = candle_service.get_yearly_candle()

    return candle

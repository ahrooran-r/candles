from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import AfterValidator

from app.config import alphavantage_settings
from app.models import YearlyCandle
from app.service import CandleService
from app.util import strip_to_none

router = APIRouter()


def validate_symbol(value: str) -> str:
    if value.strip() == "":
        raise ValueError("symbol cannot be blank")
    return value


@router.get("/symbols/{symbol}/annual/{year}")
def yearly_candle(
        # there is no way to detect blank strings. so I have to do this nested validation method
        # I hate it
        symbol: Annotated[Annotated[str, AfterValidator(validate_symbol)], Path(min_length=1, max_length=50,
                                                                                description="Stock symbol")],
        year: Annotated[int, Path(ge=datetime.now().year - alphavantage_settings.historical_depth, le=datetime.now().year)],
) -> YearlyCandle:
    """
    :param symbol: The name of the equity of your choice. For example: symbol=IBM
    :param year: should be between historical depth and current year
    :return: Candle for the given symbol and given year
    """

    symbol = strip_to_none(symbol)
    symbol = symbol.upper()

    candle_service: CandleService = CandleService(symbol, year)
    candle: YearlyCandle = candle_service.get_yearly_candle()
    return candle

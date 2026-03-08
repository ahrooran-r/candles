from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path
from models import Candle

router = APIRouter()


@router.get("/symbols/{symbol}/annual/{year}")
def yearly_candle(
        symbol: Annotated[str, Path(min_length=1, max_length=50)],
        year: Annotated[int, Path(ge=1900, le=datetime.now().year)],
) -> Candle:
    """
    :param symbol: The name of the equity of your choice. For example: symbol=IBM
    :param year: should be <= current year
    :return: Candle for the given symbol and given year
    """

    # LEARN: pydantic requires named arguments ?
    return Candle(high=23.0, low=12.4, volume=120)

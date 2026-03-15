import secrets
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import AfterValidator

from app.config import alphavantage_settings, server_settings
from app.models import YearlyCandle
from app.service import CandleService
from app.util import strip_to_none

router = APIRouter()

security = HTTPBasic()


def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)], ) -> str:
    """
    https://fastapi.tiangolo.com/advanced/security/http-basic-auth/?utm_source=chatgpt.com#check-the-username
    """

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = server_settings.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def validate_symbol(value: str) -> str:
    if value.strip() == "":
        raise ValueError("symbol cannot be blank")
    return value


@router.get("/symbols/{symbol}/annual/{year}")
def yearly_candle(
        username: Annotated[str, Depends(get_current_username)],

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

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import CandlesNotFoundError


def register_exception_handlers(app):
    @app.exception_handler(CandlesNotFoundError)
    async def candles_not_found_handler(request: Request, exc: CandlesNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "message": str(exc),
            },
        )

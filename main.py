from fastapi import FastAPI

from routers.candle_router import router as candle_router

app = FastAPI()

# LEARN: we must manually register routers
app.include_router(candle_router, tags=["candle"])

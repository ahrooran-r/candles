from app.exceptions import CandlesNotFoundError
from app.models import YearlyCandle, MonthlyCandle


class CandleAggregator:

    def __init__(self, symbol: str, year: int, monthly_candles: list[MonthlyCandle]) -> None:
        self.symbol: str = symbol
        self.year: int = year

        if not monthly_candles:
            raise CandlesNotFoundError.not_found_for_year(symbol=symbol, year=year)

        monthly_candles = [candle for candle in monthly_candles if candle.year == year]

        if not monthly_candles:
            raise CandlesNotFoundError.not_found_for_year(symbol=symbol, year=year)

        self.monthly_candles: list[MonthlyCandle] = monthly_candles
        self.high: float = self.monthly_candles[0].high
        self.low: float = self.monthly_candles[0].low
        self.volume: int = self.monthly_candles[0].volume

    def aggregate(self) -> YearlyCandle:
        for monthly_candle in self.monthly_candles[1:]:

            if monthly_candle.symbol != self.symbol or monthly_candle.year != self.year:
                # avoid any faulty record
                continue

            self._aggregate_row(monthly_candle)

        yearly_candle: YearlyCandle = YearlyCandle(high=str(self.high), low=str(self.low), volume=str(self.volume))
        return yearly_candle

    def _aggregate_row(self, candle: MonthlyCandle) -> None:
        high: float = candle.high
        if high > self.high:
            self.high = high

        low: float = candle.low
        if low < self.low:
            self.low = low

        volume: int = candle.volume
        self.volume += volume

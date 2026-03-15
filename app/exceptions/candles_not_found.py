class CandlesNotFoundError(Exception):

    def __init__(self, symbol: str, year: int):
        self.symbol: str = symbol
        self.year: int = year
        super().__init__(f"Candles not found for symbol={symbol}, year={year}")

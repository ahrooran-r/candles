class CandlesNotFoundError(Exception):

    # Unlike Java, we can't overload constructor
    def __init__(self, message: str):
        super().__init__(message)

    # So we have a class level static method in Python that sort of returns a different instance of actual class
    # Kind of combining static method + enums ?
    # This is cheap. Why no overloaded constructors?
    @classmethod
    def not_found_for_year(cls, symbol: str, year: int):
        return cls(f"Candles not found for symbol={symbol}, year={year}")

    @classmethod
    def requesting_earlier_year(cls, symbol: str, year: int, earliest_year: int):
        return cls(f"We only have candles since {earliest_year} for symbol={symbol}. You are requesting for year={year}. Oops! Sorry :(")

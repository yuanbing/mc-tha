class DataItem:
    def __init__(self, ts: float, exchange: str, pair: str, price: float) -> None:
        self._ts = ts
        self._exchange = exchange
        self._pair = pair
        self._price = price
    
    @property
    def ts(self) -> float:
        return self._ts

    @property
    def exchange(self) -> str:
        return self._exchange

    @property
    def pair(self) -> str:
        return self._pair

    @property
    def price(self) -> float:
        return self._price

from typing import Callable
from model.item import DataItem
import requests
import time

class Downloader:
    """
    This is the downloader that collects the price data from the provider.
    For the MVP, we hard-code the provider URL. For the production, however, the URL
    shall be generated by the provider.
    """

    MARKET_DATA_PROVIDER: str = "https://api.cryptowat.ch/markets/{exchange}/{pair}/price"
    
    def __init__(self, exchange: str, pair: str) -> None:
        self._exchange  = exchange
        self._pair = pair
    
    @property
    def id(self) -> str:
        return f"{self._exchange}_{self._pair}"

    def execute(self, on_complete: Callable[[DataItem], None]) -> None:
        source_url = self.MARKET_DATA_PROVIDER.format(exchange=self._exchange, pair=self._pair)
        print(f"start downloading price data for {self._pair} of exchange {self._exchange}")
        response = requests.get(source_url)
        if response.status_code != 200:
            # when the download fails, let's assume it's transient
            print("Failed to download price data from {} with status code {}".format(source_url, response.status_code))
        else:
            item = self._process_response(response.json()['result'])
            print(f"calling back with price data for {self._pair} of exchange {self._exchange}")
            on_complete(item)
            
    def _process_response(self, result: any) -> DataItem:
        # supprisingly, the provider API doesn't return timestamp in the response.
        # but there is one in the response header, should I use that?
        # the provider API is lacking documentation badly!
        return DataItem(time.time(), self._exchange, self._pair, result['price'])
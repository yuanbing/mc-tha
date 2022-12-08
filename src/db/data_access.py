from statistics import stdev
from typing import List, Optional, Set, Tuple
from db.in_memory_db import InMemoryDB
from model.item import DataItem
from model.volatility_rank import VolatilityRank as Rank

INVALID_RANK:int = -1


class DataAccess:

    def __init__(self) -> None:
        self._db: InMemoryDB = InMemoryDB(1440)
    
    def collect_price_data(self, exchange: str, pair: str) -> None:
        print(f"start collecting price data for pair {pair} of exchange {exchange}")
        table_name = f"{exchange}_{pair}"
        self._db.add_table(table_name)

    def append_price_data(self, price_data: DataItem) -> None:
        print(f"appending latest price {price_data.price} for pair {price_data.pair} of exchange {price_data.exchange}")
        exchange = price_data.exchange
        pair = price_data.pair

        table_name = f"{exchange}_{pair}"
        self._db.append_to_table(table_name, price_data)

    def get_latest_price(self, exchange: str, pair: str) -> Optional[float]:
        table_name = f"{exchange}_{pair}"
        item = self._db.get_last_item(table_name)
        if item:
            return item.price
        else:
            return None

    def rank_volatility(self, exchange: str, pairs: Set[str]) -> List[Rank]:
        """
        this may be the most complicated method. My instinction tells me that it might
        be way more efficient to calculate the list of rankings in SQL engine. Since I don't have SQL DB,
        at least I'm not familiar with any, I choose to do it at the application layer. It's OK, I think, 
        for MVP. But for production, it's definitely not.
        """
        list_of_stdevs: List[Tuple(float, str)] = []
        ranks: List[Rank] = []

        for pair in pairs:
            table_name = f"{exchange}_{pair}"
            items = self._db.get_table_items(table_name)
            if len(items):
                prices = [item.price for item in items]
                price_stdev = stdev(prices)
                list_of_stdevs.append((price_stdev, pair))
            else:
                print(f"no price data for {pair}")
                ranks.append(Rank(pair=pair))
        
        list_of_stdevs.sort(reverse=True)
        
        rank:int = 1
        for price_stdev in list_of_stdevs:
            ranks.append(Rank(pair=price_stdev[1], stdev=price_stdev[0], rank=rank))
            rank = rank + 1

        return ranks
        
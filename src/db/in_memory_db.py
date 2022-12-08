from collections import deque
from typing import Dict, Deque, Optional, List
from model.item import DataItem

class InMemoryDB:
    """
    this is a cheat for MVP. Ideally I should use some time series DB as 
    storage backend. But it turns out that I'm UNFAMILIAR with any Python-DB interaction
    at all. In the end I've decided to choose this in-memory approach instead of hopping amongst
    all sorts of tutorials without any perfect match of usage pattern.
    """
    def __init__(self, max_table_size: int) -> None:
        self._max_table_size: int = max_table_size
        self._data: Dict[str, Deque[DataItem]] = {}

    def add_table(self, table_name: str) -> bool:
        if not table_name in self._data:
            self._data[table_name] = deque()
            return True
        else:
            print(f"Warning: the table {table_name} already exists")
            return False

    def append_to_table(self, table_name: str, item: DataItem) -> None:
        if table_name in self._data:
            self._data[table_name].append(item)
            self._may_purge_table(table_name)
        else:
            print(f"Warning: unknown table name: {table_name}")

    def _may_purge_table(self, table_name: str) -> None:
        if len(self._data[table_name]) > self._max_table_size:
            # this is definitely not the most efficient way to shrink the queue
            self._data[table_name].pop_left()

    def get_last_item(self, table_name: str) -> Optional[DataItem]:
        if table_name in self._data:
            if len(self._data[table_name]):
                return self._data[table_name][-1]
            else:
                print(f"No data for table {table_name}")
                return None
        else:
            print(f"Warning: table {table_name} doesn't exist")
            return None
    
    def get_table_items(self, table_name: str) -> List[DataItem]:
        print(f"get the data for table {table_name}")
        if table_name in self._data:
            return list(self._data[table_name])
        else:
            return []
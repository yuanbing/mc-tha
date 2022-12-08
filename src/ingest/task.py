from typing import Any, Callable, Iterable
from ingest.downloader import Downloader
from ingest.repeat_timer import RepeatableTimer
from model.item import DataItem

class RepeatableTask:
    """
    it represents a single repeatable task. 
    the repeat interval is in second.
    """
    def __init__(self, repeat_interval: int, function: Any, args: Iterable[Any]) -> None:
        self._timer = RepeatableTimer(repeat_interval, function, args)
    
    def start(self) -> None:
        if self._timer:
            self._timer.start()
        else:
            print("Warning: the task has been finished")
    
    def cancel(self) -> None:
        if self._timer:
            self._timer.cancel()
        else:
            print("Warning: the task has been canceled")

DEFAULT_INTERVAL = 60 # in second

def schedule_download(exchange: str, pair: str, on_complete: Callable[[DataItem], None]) -> RepeatableTask:
    downloader = Downloader(exchange, pair)
    print("Scheduling download for {}:{}".format(exchange, pair))
    task = RepeatableTask(DEFAULT_INTERVAL, downloader.execute, [on_complete])
    task.start()
    return task
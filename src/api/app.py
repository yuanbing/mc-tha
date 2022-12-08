from typing import Dict, List
from fastapi import FastAPI

from db.data_access import DataAccess
from ingest.task import RepeatableTask, schedule_download
from model.volatility_rank import VolatilityRank
from api.request.const import DEFAULT_EXCHANGE, INVALID_PRICE
from api.request.data_collection_request import DataCollectionRequest
from api.request.rank_request import RankRequest


def create_app() -> FastAPI:
    data_provider = DataAccess()
    price_data_collecting_tasks: Dict[str, RepeatableTask] = {}

    app = FastAPI(
        title="prices",
        description="Simple API to query the info about crypto currencies",
        version="1.0",
    )

    @app.get("/health")
    async def health() -> str:
        print("hello world!")
        return "ok"

    @app.get("/prices/binance-us/{pair_name}/price")
    async def get_price(pair_name: str) -> float:
        print(f"getting the latest price for {pair_name}")
        price = data_provider.get_latest_price(DEFAULT_EXCHANGE, pair_name)
        if price:
            return price
        else:
            return INVALID_PRICE

    @app.put("/prices/collect")
    async def collect_price_data(price_collection_request: DataCollectionRequest) -> str:
        print(
            f"start collecting price for {price_collection_request.pair} at exchange {price_collection_request.exchange}")
        download_task_id = f"{price_collection_request.exchange}_{price_collection_request.pair}"
        if download_task_id not in price_data_collecting_tasks:
            data_provider.collect_price_data(exchange=price_collection_request.exchange, pair=price_collection_request.pair)
            price_data_collecting_tasks[download_task_id] = schedule_download(
                exchange=price_collection_request.exchange, pair=price_collection_request.pair, on_complete=data_provider.append_price_data)
            print(f"scheduled data collection task for {download_task_id}")
            return "scheduled"
        else:
            print(f"download task {download_task_id} already exists")
            return "existed"

    @app.post("/prices/rank")
    async def rank_volatility(rank_request: RankRequest) -> List[VolatilityRank]:
        print("Ranking price volatility")
        return data_provider.rank_volatility(DEFAULT_EXCHANGE, rank_request.pairs)

    @app.on_event("shutdown")
    def shutdown_event():
        print("service is shutting down...")
        for table_name, task in price_data_collecting_tasks.items():
            print(f"canceling downloading task for table {table_name}")
            task.cancel()

    return app

from pydantic import BaseModel, Field

from api.request.const import DEFAULT_EXCHANGE


class DataCollectionRequest(BaseModel):
    """
    it represents a price data collection request
    """
    exchange: str = Field(default=DEFAULT_EXCHANGE, title="The exchange name where the pair is traded at")
    pair: str = Field(title="the name or symbol of the pair")
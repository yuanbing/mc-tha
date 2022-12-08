from typing import Set
from pydantic import BaseModel, Field

from api.request.const import DEFAULT_EXCHANGE


class RankRequest(BaseModel):

    exchange: str = Field(default=DEFAULT_EXCHANGE, title="The exchange name where the pair is traded at")
    pairs: Set[str] = Field(title="a set of pairs to rank the standard deviation")
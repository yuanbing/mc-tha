from pydantic import BaseModel, Field

class VolatilityRank(BaseModel):
    pair: str = Field(title="the name or symbol of the pair")
    stdev: float = Field(default=0.0, title="standard deviation the last 24 hours")
    rank: int = Field(default=-1, title="the rank amongst the list of pairs")
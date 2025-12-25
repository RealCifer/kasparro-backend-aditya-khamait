from pydantic import BaseModel
from datetime import datetime


class AssetResponse(BaseModel):
    id: int
    symbol: str
    name: str
    price: float
    source: str
    updated_at: datetime

    class Config:
        orm_mode = True

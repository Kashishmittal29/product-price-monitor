from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class PriceHistoryBase(BaseModel):
    price: float
    timestamp: datetime

class PriceHistoryResponse(PriceHistoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    source: str
    source_product_id: str
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    current_price: float
    currency: str = "USD"

class ProductCreate(ProductBase):
    id: str

class ProductResponse(ProductBase):
    id: str
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductDetailResponse(ProductResponse):
    price_history: List[PriceHistoryResponse] = []

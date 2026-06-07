from pydantic import BaseModel
from typing import List, Optional

class ItemAdd(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    price_at_addition: float
    item_total: float  # <-- Now fetching from DB
    class Config: from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: Optional[float] = None  # <-- Shows null until checkout
    items: List[CartItemResponse] = []
    class Config: from_attributes = True
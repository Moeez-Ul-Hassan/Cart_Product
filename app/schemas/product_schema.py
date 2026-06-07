from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase): pass
class StockUpdate(BaseModel): stock: int

class ProductResponse(ProductBase):
    id: int
    class Config: from_attributes = True
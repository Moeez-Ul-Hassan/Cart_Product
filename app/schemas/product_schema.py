from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase): pass
class StockUpdate(BaseModel): stock: int

class ProductResponse(ProductBase):
    id: int
    class Config: from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
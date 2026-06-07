from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    price = Column(Float)
    stock = Column(Integer)
    reserved_stock = Column(Integer, default=0)  # <-- The new enterprise column
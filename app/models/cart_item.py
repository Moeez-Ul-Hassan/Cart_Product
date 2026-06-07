from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_addition = Column(Float)
    item_total = Column(Float)  # <-- New Column
    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
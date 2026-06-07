from sqlalchemy.orm import Session
from models.product import Product
from schemas.product_schema import ProductCreate

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def create_product(db: Session, data: ProductCreate):
    product = Product(name=data.name, price=data.price, stock=data.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_stock(db: Session, product: Product, stock: int):
    product.stock = stock
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()

# Add this new function to lock the row during transactions
def get_product_for_update(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).with_for_update().first()
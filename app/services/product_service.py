from sqlalchemy.orm import Session
from repositories import product_repository
from schemas.product_schema import ProductCreate, StockUpdate
from repositories import product_repository, cart_repository
from validators.validators import validate_price, validate_stock
from exceptions.custom_exceptions import ResourceNotFoundError

def create_product(db: Session, data: ProductCreate):
    validate_price(data.price)
    validate_stock(data.stock)
    return product_repository.create_product(db, data)

def get_products(db: Session):
    return product_repository.get_all_products(db)

def get_product(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product: raise ResourceNotFoundError("Product")
    return product

def update_stock(db: Session, product_id: int, data: StockUpdate):
    validate_stock(data.stock)
    
    try:
        product = product_repository.get_product_for_update(db, product_id)
        if not product: 
            raise ResourceNotFoundError("Product")

        new_stock = data.stock
        
        # Scenario: We are lowering stock below what is currently reserved in active carts
        if product.reserved_stock > new_stock:
            deficit = product.reserved_stock - new_stock
            
            # Fetch items from newest to oldest
            active_items = cart_repository.get_active_cart_items_by_product_desc(db, product.id)
            
            for item in active_items:
                if deficit <= 0: 
                    break # We have recovered enough stock
                
                # If this user's cart has fewer or equal items than we need to recover, delete their item entirely
                if item.quantity <= deficit:
                    deficit -= item.quantity
                    db.delete(item)
                
                # If this user has more items than the deficit, just reduce their quantity
                else:
                    item.quantity -= deficit
                    item.item_total = item.quantity * item.price_at_addition
                    db.add(item)
                    deficit = 0
            
            # The reserved stock is now safely capped at the new maximum stock
            product.reserved_stock = new_stock
            
        product.stock = new_stock
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
        
    except Exception as e:
        db.rollback()
        raise e

def delete_product(db: Session, product_id: int):
    try:
        product = product_repository.get_product_for_update(db, product_id)
        if not product: 
            raise ResourceNotFoundError("Product")
        
        # Scenario: Complete product deletion
        # Forcefully remove this product from every active cart in the system
        active_items = cart_repository.get_active_cart_items_by_product_desc(db, product.id)
        for item in active_items:
            db.delete(item)
            
        # Delete the product (Note: In a true 10/10 system, you would set product.is_deleted = True here instead)
        db.delete(product)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
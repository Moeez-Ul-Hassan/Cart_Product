from sqlalchemy.orm import Session
from models.cart import Cart
from models.cart_item import CartItem

def get_active_cart_by_user(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "active").first()

def get_cart_by_id(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.id == cart_id).first()

def create_cart(db: Session, user_id: int):
    cart = Cart(user_id=user_id, status="active")
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def update_cart_status(db: Session, cart: Cart, status: str):
    cart.status = status
    db.commit()
    return cart

def add_item(db: Session, cart_id: int, product_id: int, qty: int, price: float):
    item = CartItem(cart_id=cart_id, product_id=product_id, quantity=qty, price_at_addition=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Add this new function to check for existing items to merge
def get_cart_item_by_product(db: Session, cart_id: int, product_id: int):
    return db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id).first()

# Add this below your existing functions
def get_active_cart_items_by_product_desc(db: Session, product_id: int):
    return (
        db.query(CartItem)
        .join(Cart, CartItem.cart_id == Cart.id)
        .filter(CartItem.product_id == product_id, Cart.status == "active")
        .order_by(CartItem.id.desc())
        .with_for_update() # Lock these rows so they can't be checked out while we edit them
        .all()
    )
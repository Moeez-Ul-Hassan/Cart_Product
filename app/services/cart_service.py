from sqlalchemy.orm import Session
from repositories import cart_repository, user_repository, product_repository
from schemas.cart_schema import ItemAdd
from models.cart_item import CartItem
from validators.validators import validate_quantity
from exceptions.custom_exceptions import ResourceNotFoundError, BusinessRuleViolation

def create_cart(db: Session, user_id: int):
    if not user_repository.get_user_by_id(db, user_id):
        raise ResourceNotFoundError("User")
    if cart_repository.get_active_cart_by_user(db, user_id):
        raise BusinessRuleViolation("User already has an active cart.")
    return cart_repository.create_cart(db, user_id)

def get_cart(db: Session, cart_id: int):
    cart = cart_repository.get_cart_by_id(db, cart_id)
    if not cart: raise ResourceNotFoundError("Cart")
    return cart

def add_item_to_cart(db: Session, cart_id: int, item: ItemAdd):
    validate_quantity(item.quantity)
    cart = get_cart(db, cart_id)
    if cart.status != "active": raise BusinessRuleViolation("Cart is not active.")
    
    try:
        product = product_repository.get_product_for_update(db, item.product_id)
        if not product: raise ResourceNotFoundError("Product")
        
        available_stock = product.stock - (product.reserved_stock or 0)
        if available_stock < item.quantity: 
            raise BusinessRuleViolation(f"Insufficient stock. Only {available_stock} units available.")
        
        product.reserved_stock = (product.reserved_stock or 0) + item.quantity
        
        # Check if item exists to merge
        existing_item = cart_repository.get_cart_item_by_product(db, cart_id, product.id)
        if existing_item:
            existing_item.quantity += item.quantity
            # Recalculate item_total upon merge
            existing_item.item_total = existing_item.quantity * existing_item.price_at_addition
            db.add(existing_item)
            result_item = existing_item
        else:
            # Calculate initial item_total for new items
            calc_item_total = item.quantity * product.price
            new_item = CartItem(
                cart_id=cart_id, 
                product_id=product.id, 
                quantity=item.quantity, 
                price_at_addition=product.price,
                item_total=calc_item_total # <-- Save to DB
            )
            db.add(new_item)
            result_item = new_item
            
        db.commit()
        db.refresh(result_item)
        return result_item

    except Exception as e:
        db.rollback()
        raise e

def checkout_cart(db: Session, cart_id: int):
    cart = get_cart(db, cart_id)
    if cart.status != "active": raise BusinessRuleViolation("Cart is not active.")
    if not cart.items: raise BusinessRuleViolation("Cannot checkout empty cart.")
    
    try:
        final_bill_total = 0.0  # Initialize the cart total counter
        
        for item in cart.items:
            product = product_repository.get_product_for_update(db, item.product_id)
            
            product.stock -= item.quantity
            product.reserved_stock -= item.quantity
            db.add(product)
            
            # Add this item's total to the final bill
            final_bill_total += item.item_total
            
        # Finalize the Cart Invoice
        cart.status = "checked_out"
        cart.total_amount = final_bill_total  # <-- Save the final bill to DB
        
        db.add(cart)
        db.commit()
        
        return {
            "message": "Checkout successful. Invoice generated.",
            "total_billed": final_bill_total
        }
        
    except Exception as e:
        db.rollback()
        raise e

def delete_cart(db: Session, cart_id: int):
    cart = get_cart(db, cart_id)
    if cart.status != "active": raise BusinessRuleViolation("Only active carts can be deleted.")
    
    try:
        # Restoration on Cart Delete: Give the reserved stock back to the warehouse
        for item in cart.items:
            product = product_repository.get_product_for_update(db, item.product_id)
            product.reserved_stock -= item.quantity
            db.add(product)
            
        cart.status = "deleted"
        db.add(cart)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
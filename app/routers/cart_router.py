from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas import cart_schema
from services import cart_service

router = APIRouter(prefix="/cart", tags=["Carts"])

@router.post("/users/{user_id}/", response_model=cart_schema.CartResponse, status_code=status.HTTP_201_CREATED)
def create_cart(user_id: int, db: Session = Depends(get_db)):
    return cart_service.create_cart(db, user_id)

@router.get("/{cart_id}", response_model=cart_schema.CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    return cart_service.get_cart(db, cart_id)

@router.post("/{cart_id}/items/", response_model=cart_schema.CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(cart_id: int, item: cart_schema.ItemAdd, db: Session = Depends(get_db)):
    return cart_service.add_item_to_cart(db, cart_id, item)

@router.post("/{cart_id}/checkout")
def checkout_cart(cart_id: int, db: Session = Depends(get_db)):
    return cart_service.checkout_cart(db, cart_id)

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_service.delete_cart(db, cart_id)
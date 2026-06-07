from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas import product_schema
from services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=product_schema.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)

@router.get("/", response_model=list[product_schema.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)

@router.get("/{product_id}", response_model=product_schema.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)

@router.patch("/{product_id}/stock", response_model=product_schema.ProductResponse)
def update_stock(product_id: int, data: product_schema.StockUpdate, db: Session = Depends(get_db)):
    return product_service.update_stock(db, product_id, data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, product_id)
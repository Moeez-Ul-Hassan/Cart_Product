from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas import user_schema
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)

@router.get("/", response_model=list[user_schema.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/{user_id}", response_model=user_schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)

@router.put("/{user_id}", response_model=user_schema.UserResponse)
def update_user(user_id: int, data: user_schema.UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
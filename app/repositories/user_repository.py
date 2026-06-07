from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data: UserCreate):
    db_user = User(email=user_data.email, name=user_data.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: User, name: str, email: str):
    user.name = name
    user.email = email
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
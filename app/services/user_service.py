from sqlalchemy.orm import Session
from repositories import user_repository
from schemas.user_schema import UserCreate, UserUpdate
from validators.validators import validate_name
from exceptions.custom_exceptions import ResourceNotFoundError, BusinessRuleViolation

def create_user(db: Session, user_data: UserCreate):
    validate_name(user_data.name)
    if user_repository.get_user_by_email(db, user_data.email):
        raise BusinessRuleViolation("Email already registered.")
    return user_repository.create_user(db, user_data)

def get_users(db: Session):
    return user_repository.get_all_users(db)

def get_user(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)
    if not user: raise ResourceNotFoundError("User")
    return user

def update_user(db: Session, user_id: int, data: UserUpdate):
    validate_name(data.name)
    user = get_user(db, user_id)
    return user_repository.update_user(db, user, data.name, data.email)

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_repository.delete_user(db, user)
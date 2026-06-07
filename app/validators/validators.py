import re
from exceptions.custom_exceptions import ValidationException

def validate_name(name: str):
    if len(name) > 100: raise ValidationException("Name cannot exceed 100 characters.")
    if not re.fullmatch(r"[A-Za-z ]+", name): raise ValidationException("Name must contain only alphabetic characters.")

def validate_price(price: float):
    if price < 0: raise ValidationException("Price cannot be negative.")

def validate_stock(stock: int):
    if stock < 0: raise ValidationException("Stock cannot be negative.")

def validate_quantity(quantity: int):
    if quantity <= 0: raise ValidationException("Quantity must be greater than zero.")
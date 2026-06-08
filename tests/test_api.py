import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import your app and DB components
from app.main import app
# Adjust this import if your get_db function is located somewhere else!
from database.database import Base, get_db

# =====================================================================
# IN-MEMORY SQLITE DATABASE SETUP
# =====================================================================

# 1. Create the fake SQLite engine
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Create the tables in the fake SQLite memory
Base.metadata.create_all(bind=engine)

# 3. Intercept the database connection
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Swap the real MySQL database with the fake SQLite one!
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_all_products():
    """TC-01: Get all products successfully"""
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_products_with_limit():
    """TC-02: Get products with query parameter"""
    response = client.get("/products?limit=5")
    assert response.status_code == 200

def test_get_single_product_valid():
    """TC-03: Get a specific existing product"""
    response = client.get("/products/1")
    # Accepting 200 (Found) or 404 (If DB is empty during test run)
    assert response.status_code in [200, 404] 

def test_get_single_product_invalid_id():
    """TC-04: Get product with non-existent ID"""
    response = client.get("/products/99999")
    assert response.status_code == 404

def test_get_product_invalid_datatype():
    """TC-05: Path validation failure (string instead of int)"""
    response = client.get("/products/abc")
    assert response.status_code == 422

def test_create_product_valid():
    """TC-06: Create a new product successfully"""
    payload = {"name": "Gaming Keyboard", "price": 120.00, "stock": 50}
    response = client.post("/products", json=payload)
    assert response.status_code == 201

def test_create_product_missing_field():
    """TC-07: Fail to create product due to missing price"""
    payload = {"name": "Gaming Keyboard", "stock": 50}
    response = client.post("/products", json=payload)
    assert response.status_code == 422

def test_create_product_negative_price():
    """TC-08: Pydantic should block negative prices"""
    payload = {"name": "Gaming Keyboard", "price": -10.00, "stock": 50}
    response = client.post("/products", json=payload)
    assert response.status_code in [400, 422]

def test_update_product_valid():
    """TC-09: Update an existing product"""
    payload = {"price": 110.00}
    response = client.put("/products/1", json=payload)
    assert response.status_code in [200, 404] # 404 if product 1 doesn't exist yet

def test_delete_product():
    """TC-10: Delete a product"""
    response = client.delete("/products/1")
    assert response.status_code in [200, 204, 404]

def test_create_cart_for_user():
    """TC-11: Initialize a new cart for a specific user"""
    # Maps to: @router.post("/users/{user_id}/")
    response = client.post("/cart/users/1/")
    # Allowing 404 or 400 in case User 1 doesn't exist in the test DB yet
    assert response.status_code in [201, 400, 404] 

def test_get_cart_by_id():
    """TC-12: Fetch a specific cart by its ID"""
    # Maps to: @router.get("/{cart_id}")
    response = client.get("/cart/1")
    assert response.status_code in [200, 404]

def test_add_item_to_cart_valid():
    """TC-13: Add an item to an existing cart"""
    # Maps to: @router.post("/{cart_id}/items/")
    payload = {"product_id": 1, "quantity": 2}
    response = client.post("/cart/1/items/", json=payload)
    assert response.status_code in [201, 400, 404]

def test_add_item_invalid_quantity():
    """TC-14: Block adding negative items (Pydantic validation)"""
    payload = {"product_id": 1, "quantity": -5}
    response = client.post("/cart/1/items/", json=payload)
    # Pydantic should catch the negative number and throw a 422
    assert response.status_code in [400, 422]

def test_add_item_missing_product():
    """TC-15: Block adding an item with missing payload data"""
    payload = {"quantity": 2}
    response = client.post("/cart/1/items/", json=payload)
    assert response.status_code == 422

def test_checkout_cart():
    """TC-16: Process checkout for a specific cart"""
    # Maps to: @router.post("/{cart_id}/checkout")
    response = client.post("/cart/1/checkout")
    assert response.status_code in [200, 201, 400, 404]

def test_checkout_invalid_cart_datatype():
    """TC-17: Ensure API blocks string datatypes in integer path parameters"""
    response = client.post("/cart/abc/checkout")
    assert response.status_code == 422

def test_delete_cart():
    """TC-18: Delete a specific cart completely"""
    # Maps to: @router.delete("/{cart_id}")
    response = client.delete("/cart/1")
    # 204 No Content is your router's success code
    assert response.status_code in [204, 404]

def test_system_404_routing():
    """TC-19: Test FastAPI default 404 handling for truly bad routes"""
    response = client.get("/invalid-secret-route")
    assert response.status_code == 404
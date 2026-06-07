# Enterprise E-Commerce Cart & Inventory API

A highly resilient, production-grade E-Commerce API built with **FastAPI** and **SQLAlchemy**. This project goes beyond basic CRUD operations to implement true enterprise-level backend architecture, specifically designed to solve complex e-commerce challenges like race conditions, cart abandonment, and inventory reconciliation.

## Tech Stack
* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Database:** MySQL
* **Data Validation:** Pydantic (v2)
* **Server:** Uvicorn
* **Testing:** Postman (Data-Driven Test Suite)

## Enterprise Features Implemented

### 1. Pessimistic Concurrency Control (Row Locking)
Implemented `with_for_update()` in the repository layer to mathematically eliminate race conditions. If 1,000 users try to buy the last GPU at the exact same millisecond, the database handles them sequentially, guaranteeing stock is never oversold.

### 2. Advanced Inventory State Management
Split standard product stock into `available_stock` and `reserved_stock`. When a user adds an item to their cart, it is temporarily reserved. This protects the business from promising out-of-stock items while accommodating users who abandon their carts.

### 3. ACID Transactions & Rollbacks
All multi-table operations (e.g., checking out a cart, which updates Carts, Cart Items, and Products simultaneously) are wrapped in `try/except` transaction blocks. If any step fails, `db.rollback()` executes, ensuring the database never enters a corrupted or partially-updated state.

### 4. LIFO Inventory Eviction Policy
If warehouse administrators reduce overall global stock to a level below what is currently held in active user carts, the system executes a "Last-In-First-Out" revocation algorithm. It safely removes items from the most recently created carts to balance the deficit while protecting "First Come, First Serve" customers.

### 5. Unified Global Exception Handling
Overrode FastAPI's default error responses to guarantee a strict, standardized JSON envelope for the frontend. Whether it is a `404 Not Found`, a `422 Pydantic Validation Error`, or a `400 Business Rule Violation`, the response format remains perfectly consistent.

## Architecture (SOLID Principles)
The codebase is structured into distinct, isolated layers to ensure maintainability and separation of concerns:

```text
app/
├── core/            # App configurations, logging, and global exception handlers
├── database/        # Database engine and session management
├── exceptions/      # Custom business logic exceptions
├── models/          # SQLAlchemy database models
├── repositories/    # Direct database access and queries
├── routers/         # API endpoint definitions
├── schemas/         # Pydantic models for request/response validation
├── services/        # Core business logic and calculations
├── validators/      # Reusable data validation rules
└── main.py          # FastAPI application entry point
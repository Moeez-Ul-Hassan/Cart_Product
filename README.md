# Enterprise E-Commerce Cart & Inventory API

A highly resilient, production-grade E-Commerce API built with **FastAPI** and **SQLAlchemy**. This project goes beyond basic CRUD operations to implement true enterprise-level backend architecture, specifically designed to solve complex e-commerce challenges like race conditions, cart abandonment, and inventory reconciliation.

## Tech Stack
* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Database:** MySQL 8.0
* **Containerization:** Docker & Docker Compose
* **Cloud Infrastructure:** AWS EC2 (Ubuntu Linux)
* **Data Validation:** Pydantic (v2)
* **Server:** Uvicorn

---

## System Architecture & Data Flow

The application runs in an isolated, containerized environment within an AWS cloud infrastructure.

```text
[ Client Request ] 
       │
       ▼ (Port 8000)
[ AWS Security Group Firewall ]
       │
       ▼
[ FastAPI Container (Uvicorn) ] ──(SQLAlchemy ORM)──► [ MySQL 8.0 Container ]
                                 (Port 3306 Inside Bridge)       │
                                                                 ▼
                                                    [ Persistent EBS Volume ]


app/
├── core/         # App configurations, logging, and global exception handlers
├── database/     # Database engine, session management, and Base definitions
├── exceptions/   # Custom business logic exceptions
├── models/       # SQLAlchemy database models
├── repositories/ # Direct database access and queries
├── routers/      # API endpoint definitions (Routes)
├── schemas/      # Pydantic models for request/response validation
├── services/     # Core business logic and calculations
├── validators/   # Reusable data validation rules
└── main.py       # FastAPI application entry point
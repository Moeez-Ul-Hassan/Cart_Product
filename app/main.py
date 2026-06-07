from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from routers import user_router, product_router, cart_router
from core.exception_handlers import global_exception_handler
from core.logging import logger
from fastapi.exceptions import RequestValidationError
from core.exception_handlers import global_exception_handler, validation_exception_handler

# 1. Initialize DB Tables
Base.metadata.create_all(bind=engine)

# 2. Initialize App
app = FastAPI(title="Cart Service API")

# 3. Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status {response.status_code}")
    return response

# 4. Global Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 5. Routers
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)

@app.get("/")
def health_check():
    return {"status": "Running smoothly."}
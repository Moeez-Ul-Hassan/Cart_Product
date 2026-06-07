from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions.custom_exceptions import ResourceNotFoundError, BusinessRuleViolation, ValidationException
from core.logging import logger

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Add this new handler for Pydantic validation errors
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the first error message and the field name
    errors = exc.errors()
    field = errors[0]["loc"][-1] if errors[0]["loc"] else "unknown"
    error_msg = errors[0]["msg"]
    
    logger.warning(f"Validation Error on {field}: {error_msg}")
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": f"Validation Failed: '{field}' - {error_msg}",
            "data": None
        }
    )
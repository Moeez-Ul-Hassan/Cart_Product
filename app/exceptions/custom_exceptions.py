from fastapi import HTTPException

class ResourceNotFoundError(HTTPException):
    def __init__(self, resource: str):
        super().__init__(status_code=404, detail=f"{resource} not found.")

class BusinessRuleViolation(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class ValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
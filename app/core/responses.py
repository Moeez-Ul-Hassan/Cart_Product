# Optional wrapper for standardizing JSON responses if needed
def success_response(data: dict, message: str = "Success"):
    return {"message": message, "data": data}
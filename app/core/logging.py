import logging
import sys
import os

# Create a logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("cart_api")
logger.setLevel(logging.INFO)

# The format for our log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 1. Console Handler (Prints live to your Uvicorn terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 2. File Handler (Saves permanently to a file)
file_handler = logging.FileHandler("logs/cart_enterprise.log")
file_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
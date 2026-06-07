# --- Step 1: Build dependency wheels ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed to compile certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Build wheels to speed up compilation and minimize final size
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Step 2: Final lightweight runtime image ---
FROM python:3.11-slim

WORKDIR /app

# Copy only the compiled wheels from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the pre-compiled wheels cleanly without bringing build tools along
RUN pip install --no-cache /wheels/*

# Copy your actual application code
COPY ./app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
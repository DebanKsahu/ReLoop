FROM python:3.12-slim

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv==0.7.12

# Copy all files
COPY . .

# Install dependencies into .venv
RUN uv sync --frozen && uv cache prune --ci

# Run FastAPI with uv + shell expansion of $PORT
CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port $PORT"]

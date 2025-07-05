FROM python:3.12-slim

# Install system dependencies (libgl1 added)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libpq-dev \
    gcc \
    libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv==0.7.12

# Copy project files
COPY . .

# Install Python deps using uv
RUN uv sync --frozen && uv cache prune --ci

# Run FastAPI via uv and uvicorn (with env variable support)
CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port $PORT"]


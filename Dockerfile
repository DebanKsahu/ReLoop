# Use slim Python base image
FROM python:3.12-slim

# Install required system libraries
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv (Python package manager)
RUN pip install uv==0.7.12

# Copy project files into Docker container
COPY . .

# Install dependencies from lock file
RUN uv sync --frozen && uv cache prune --ci


# Start FastAPI app with dynamic port
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]

# Use slim Python base image
FROM python:3.12-slim

# Install system-level packages
RUN apt-get update && apt-get install -y libzbar0

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv==0.7.12

# Copy project files
COPY . .

# Install Python dependencies
RUN uv sync --frozen && uv cache prune --ci

# Use dynamic port from environment (Render sets $PORT)
EXPOSE 8000

# Start FastAPI app using the dynamic $PORT
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]

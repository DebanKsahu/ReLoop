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

# Install uv package manager
RUN pip install uv==0.7.12

# Copy all project files
COPY . .

# Sync dependencies into isolated .venv
RUN uv sync --frozen && uv cache prune --ci


# Use uv to run uvicorn from the environment
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
# Use Python slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY sandbox/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy sandbox code
COPY sandbox /app

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the sandbox service
CMD ["python", "main.py"]
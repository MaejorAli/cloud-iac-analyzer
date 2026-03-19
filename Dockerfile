# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies with retries
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt || \
    (echo "Retrying..." && pip install --no-cache-dir --default-timeout=100 -r requirements.txt)

# Copy the rest of the app
COPY . .

# Default command
CMD ["python3", "main.py"]
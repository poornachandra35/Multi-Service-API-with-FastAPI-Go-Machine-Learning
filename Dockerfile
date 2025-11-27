# Use lightweight Python image
FROM python:3.10-slim

# Set work directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy ONLY requirements from this folder (your current folder = app/)
COPY requirements.txt ./

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy ENTIRE project (inside app/)
COPY . .

# FastAPI port
EXPOSE 8000

# 🔥 MOST IMPORTANT FIX 🔥
# main.py is directly inside /app, so "main:app" is correct
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

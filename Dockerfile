FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        python3-dev \
        musl-dev \
        libpq-dev \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create scripts directory and copy entrypoint
RUN mkdir -p /scripts
COPY scripts/entrypoint.sh /scripts/
RUN chmod +x /scripts/entrypoint.sh

ENTRYPOINT ["/scripts/entrypoint.sh"]
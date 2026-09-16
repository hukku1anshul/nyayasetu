# Production Dockerfile for NyayaSetu & CardSmart Platform
# Python 3.12 Slim Linux Container
FROM python:3.12-slim

# Set working directory & environment
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install essential system utilities and security certs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code, static frontend, and modules
COPY nyayasetu/ ./nyayasetu/
COPY static/ ./static/
COPY tests/ ./tests/
COPY README.md .

# Create non-privileged user for security compliance
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose target port
EXPOSE 8000

# Health check to monitor container responsiveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Launch application using production uvicorn worker
CMD ["sh", "-c", "uvicorn nyayasetu.api:app --host 0.0.0.0 --port ${PORT:-8000}"]

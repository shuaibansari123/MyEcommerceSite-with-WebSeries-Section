# ==============================================================================
# ShopEase E-commerce Platform - Production Dockerfile
# Multi-stage build for optimized production deployment
# ==============================================================================

# Build stage - for building and preparing the application
FROM python:3.11-slim-bullseye as builder

# Set environment variables for build stage
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /build

# Copy requirements first for better layer caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# ==============================================================================
# Production stage - minimal runtime image
FROM python:3.11-slim-bullseye as production

# Metadata
LABEL maintainer="shuaib@shopease.com" \
      version="1.0.0" \
      description="ShopEase E-commerce Platform" \
      org.opencontainers.image.source="https://github.com/shuaibansari123/MyEcommerceSite-with-WebSeries-Section"

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=mac.settings \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    libpng16-16 \
    libwebp6 \
    libffi7 \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r shopease && useradd -r -g shopease shopease

# Create application directories
RUN mkdir -p /app /app/staticfiles /app/media /var/log/shopease /var/run/shopease \
    && chown -R shopease:shopease /app /var/log/shopease /var/run/shopease

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Set work directory
WORKDIR /app

# Copy application code
COPY --chown=shopease:shopease . .

# Copy configuration files
COPY --chown=shopease:shopease docker/nginx.conf /etc/nginx/sites-available/default
COPY --chown=shopease:shopease docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY --chown=shopease:shopease docker/entrypoint.sh /entrypoint.sh

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

# Create gunicorn configuration
RUN echo 'bind = "0.0.0.0:8000"' > /app/gunicorn.conf.py && \
    echo 'workers = 4' >> /app/gunicorn.conf.py && \
    echo 'worker_class = "gevent"' >> /app/gunicorn.conf.py && \
    echo 'worker_connections = 1000' >> /app/gunicorn.conf.py && \
    echo 'max_requests = 1000' >> /app/gunicorn.conf.py && \
    echo 'max_requests_jitter = 100' >> /app/gunicorn.conf.py && \
    echo 'timeout = 30' >> /app/gunicorn.conf.py && \
    echo 'keepalive = 2' >> /app/gunicorn.conf.py && \
    echo 'preload_app = True' >> /app/gunicorn.conf.py && \
    echo 'accesslog = "/var/log/shopease/gunicorn-access.log"' >> /app/gunicorn.conf.py && \
    echo 'errorlog = "/var/log/shopease/gunicorn-error.log"' >> /app/gunicorn.conf.py && \
    echo 'loglevel = "info"' >> /app/gunicorn.conf.py

# Switch to non-root user
USER shopease

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health/ || exit 1

# Expose port
EXPOSE 80

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"] 
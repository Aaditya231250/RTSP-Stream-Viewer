# =============================================================================
# STAGE 1: Builder Stage
# =============================================================================
FROM python:3.11-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    linux-headers

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Remove build dependencies
RUN apk del .build-deps

# =============================================================================
# STAGE 2: Runtime Stage
# =============================================================================
FROM python:3.11-alpine as runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=streamviewer.settings

# Install runtime dependencies
RUN apk add --no-cache \
    ffmpeg \
    bash \
    sqlite \
    netcat-openbsd \
    && rm -rf /var/cache/apk/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN adduser -D -u 1000 app

WORKDIR /app

# Copy entrypoint with proper permissions
COPY --chown=app:app entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy application code
COPY --chown=app:app . .

# CRITICAL: Create database directory with proper permissions
RUN mkdir -p /app/data && \
    chown -R app:app /app && \
    chown -R app:app /app/data && \
    chmod -R 755 /app && \
    chmod -R 755 /app/data

# Create temp directory for streams
RUN mkdir -p /tmp/stream_temp && \
    chown -R app:app /tmp/stream_temp

USER app

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

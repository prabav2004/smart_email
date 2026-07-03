# ── Stage 1: dependency installation ──────────────────────
FROM python:3.11-slim AS builder

WORKDIR /install

# Install only what's needed to compile packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
 && pip install --prefix=/install/packages --no-cache-dir -r requirements.txt


# ── Stage 2: runtime image ─────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL maintainer="SmartEmail.ai"
LABEL description="AI Smart Email Assistant — FastAPI + LangGraph"

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install/packages /usr/local

# Copy application source
COPY app/     ./app/
COPY frontend/ ./frontend/

# Environment defaults (overridden by .env or docker-compose)
ENV PORT=8000 \
    HOST=0.0.0.0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Drop to non-root user
USER appuser

EXPOSE 8000

# Health check so orchestrators know when the service is ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

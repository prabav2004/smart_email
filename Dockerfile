# ==========================================================
# AI Smart Email Assistant
# FastAPI + LangGraph + Hugging Face
# ==========================================================

FROM python:3.11-slim

LABEL maintainer="SmartEmail.ai"
LABEL description="AI Smart Email Assistant — FastAPI + LangGraph"

# Prevent Python cache files and enable immediate logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    HF_HOME=/tmp/huggingface

WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install all dependencies directly into the runtime image
RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ ./app/
COPY frontend/ ./frontend/

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')" || exit 1

# Start FastAPI
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
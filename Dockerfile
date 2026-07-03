# ==========================================================
# Stage 1 - Install Dependencies
# ==========================================================
FROM python:3.11-slim AS builder

WORKDIR /install

# Install build tools required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel --no-cache-dir && \
    pip install --prefix=/install/packages --no-cache-dir -r requirements.txt


# ==========================================================
# Stage 2 - Runtime Image
# ==========================================================
FROM python:3.11-slim

LABEL maintainer="SmartEmail.ai"
LABEL description="AI Smart Email Assistant using FastAPI + LangGraph"

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /install/packages /usr/local

# Copy application source
COPY app/ app/
COPY frontend/ frontend/

# Environment Variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Hugging Face cache directory
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface

# Expose application port
EXPOSE 8000

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')" || exit 1

# Switch to non-root user
USER appuser

# Start FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
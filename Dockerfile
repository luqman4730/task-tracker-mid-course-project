# syntax=docker/dockerfile:1

# ---------- Stage 1: builder ----------
# Builds dependencies into an isolated virtualenv so the runtime stage
# never needs pip caches, compilers, or build metadata.
FROM python:3.11-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Non-root runtime user.
RUN useradd --create-home --uid 10001 app

WORKDIR /srv

# Dependencies only - no build toolchain, no pip cache.
COPY --from=builder /opt/venv /opt/venv

# Runtime source only. Tests, docs, and tooling stay out of the image.
COPY --chown=app:app app/ ./app/
COPY --chown=app:app frontend/ ./frontend/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()"

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

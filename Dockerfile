# ─── Stage 1: build Python dependencies ──────────────────────────────────────
FROM python:3.13-slim AS builder
WORKDIR /deps
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─── Stage 2: development (live-reload via volume mount) ──────────────────────
FROM python:3.13-slim AS development
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /install /usr/local
# src/ is mounted as a volume at runtime for live reload
COPY src/ .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ─── Stage 3: production (minimal image) ──────────────────────────────────────
FROM python:3.13-slim AS production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ .
# Collect static files at build time (requires a dummy SECRET_KEY)
RUN SECRET_KEY=build-collect-static python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "backend.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

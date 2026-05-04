# Docker Setup Notes — FEMR Web App

**Tested:** 2026-05-04 ✅  
**Environment:** Rootless Docker, production stack

---

## Quick Reference — Commands

### First-time setup
```bash
# 1. Create prod env file
cp .env.example .env.prod
# Edit .env.prod with actual values (see below)

# 2. Build and start all containers
docker compose -f docker-compose.prod.yml up -d --build

# 3. Run database migrations (first time only)
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Daily operations
```bash
# Check all containers are running
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs web
docker compose -f docker-compose.prod.yml logs celery_worker
docker compose -f docker-compose.prod.yml logs -f celery_worker   # follow live

# Restart after server reboot
docker compose -f docker-compose.prod.yml up -d

# Stop everything
docker compose -f docker-compose.prod.yml down
```

### After a code update
```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## What Runs in Docker

| Container | Image | Role |
|-----------|-------|------|
| `shoma-web-1` | Built from Dockerfile (production) | Django + Gunicorn web server |
| `shoma-celery_worker-1` | Built from Dockerfile (production) | Background job processor |
| `shoma-db-1` | postgres:16-alpine | PostgreSQL database |
| `shoma-redis-1` | redis:7-alpine | Message broker for Celery |

---

## Ports

| Service | Port |
|---------|------|
| Web app | `8000` (external) |
| PostgreSQL | Internal only (not exposed) |
| Redis | Internal only (not exposed) |

---

## Environment File — `.env.prod`

All configuration lives in `.env.prod`. Never hardcode values in compose files.

```ini
SECRET_KEY=<50+ character random string>
DEBUG=False
ALLOWED_HOSTS=<server-ip-or-domain>

CELERY_BROKER_URL=redis://redis:6379/0
FEMR_REPO_ROOT=/repo

# Django DB connection
DB_NAME=shoma
DB_USER=shoma
DB_PASSWORD=<strong password>
DB_HOST=db
DB_PORT=5432

# Postgres container credentials (must match DB_* above)
POSTGRES_DB=shoma
POSTGRES_USER=shoma
POSTGRES_PASSWORD=<same strong password>

# Oracle API credentials
ORACLE_CLIENT_ID=<from Josh Grapani>
ORACLE_SECRET_KEY=<from Josh Grapani>

DJANGO_LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=50
```

Generate a SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Volumes (persistent data)

| Volume | Contents |
|--------|----------|
| `shoma_postgres_prod` | Database — all job history, transform jobs |
| `shoma_media_prod` | Uploaded input files + generated output Excel files |
| `shoma_logs_prod` | FEMR export job logs |

> **Important:** Do not run `docker compose down --volumes` in production — this deletes all data.

---

## Rootless Docker — Important Notes

- Do **not** add `user:` directive to any service in the compose file
- Rootless Docker remaps container UIDs to the host user automatically
- If bind-mount permission errors occur: `chmod -R 755 src scripts docs`

---

## Known Issues Fixed

| Issue | Fix |
|-------|-----|
| `scripts/` not found during build | Removed `scripts/` from `.dockerignore` |
| Script path `/scripts/...` wrong in container | Set `FEMR_REPO_ROOT=/repo` in `.env.prod` |
| Permission errors on startup | Removed `user: "${UID}:${GID}"` — not needed with rootless Docker |

---

## Verified Test Results (2026-05-04)

```
All 4 containers: Up ✅
Migrations applied: 11 (including transform.0002_transformjob_output_format) ✅
HTTP response on port 8000: 200 OK ✅
```

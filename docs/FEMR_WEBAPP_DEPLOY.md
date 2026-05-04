# FEMR Web App — Server Deployment Guide

**Client:** NextFlex  
**Prepared by:** Daden.dev (Atul Kumar)  
**Date:** May 2026  

---

## What the Web App Does

Provides a browser-based interface for two workflows:

1. **FEMR Export** — Select a reporting group (WFD, Internal, Comml, OGA, ADP), run the export script in the background, monitor live logs, and download the generated Excel files when complete.
2. **FEMR Transform** — Upload a FEMR Funds Excel file, transform it to long-format data, and download the result as Excel or CSV.

The app runs entirely on the server — no Python installation required on end-user machines.

---

## Prerequisites

The server must have the following installed before setup:

- **Docker** (rootless mode is supported)
- **Docker Compose** (v2 — included with modern Docker installs)
- **Git** (to clone the repository) or access to copy the project folder

Verify:
```bash
docker --version
docker compose version
```

---

## Setup (One-Time)

### 1. Get the project files

Clone the repository or copy the project folder to the server:

```bash
git clone <repository-url> /opt/shoma
cd /opt/shoma
```

The folder structure should look like:

```
shoma/
├── docker-compose.prod.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── scripts/
│   └── femr_netsuite_report_16.py
├── docs/
│   └── Re_ FEMR /
│       └── GROUP MAPPING.xlsx
└── src/
    └── (Django application)
```

---

### 2. Create the production environment file

Copy the example file:

```bash
cp .env.example .env.prod
```

Open `.env.prod` and fill in all values:

```ini
# Django
SECRET_KEY=<generate a long random string — at least 50 characters>
DEBUG=False
ALLOWED_HOSTS=<server-ip-or-domain>

# Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0

# Script path inside Docker
FEMR_REPO_ROOT=/repo

# PostgreSQL — Django connection
DB_NAME=shoma
DB_USER=shoma
DB_PASSWORD=<choose a strong password>
DB_HOST=db
DB_PORT=5432

# PostgreSQL — database container credentials (must match DB_* above)
POSTGRES_DB=shoma
POSTGRES_USER=shoma
POSTGRES_PASSWORD=<same strong password as DB_PASSWORD>

# Oracle APEX OAuth credentials — obtain from Josh Grapani
ORACLE_CLIENT_ID=<client id>
ORACLE_SECRET_KEY=<secret key>
```

> **Keep `.env.prod` private.** It contains credentials — do not share or commit it.

To generate a secure `SECRET_KEY`:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

### 3. Build and start the containers

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

This starts four containers:
- `redis` — message broker for background jobs
- `db` — PostgreSQL database
- `web` — Django web server (Gunicorn)
- `celery_worker` — background job processor for export runs

---

### 4. Run database migrations

```bash
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

This creates all the required database tables. Only needed on first setup and after updates.

---

### 5. Verify everything is running

```bash
docker compose -f docker-compose.prod.yml ps
```

All four containers should show status `Up`:

```
NAME              STATUS
shoma-redis-1     Up
shoma-db-1        Up
shoma-web-1       Up
shoma-celery...   Up
```

Open a browser and go to `http://<server-ip>:8000` — you should see the application home page.

---

## Daily Operation

The containers start automatically when Docker starts (all services have `restart: unless-stopped`).

### Check container status
```bash
docker compose -f docker-compose.prod.yml ps
```

### View logs
```bash
# Web server logs
docker compose -f docker-compose.prod.yml logs web

# Background worker logs
docker compose -f docker-compose.prod.yml logs celery_worker

# Follow live logs
docker compose -f docker-compose.prod.yml logs -f celery_worker
```

### Restart after a server reboot
```bash
cd /opt/shoma
docker compose -f docker-compose.prod.yml up -d
```

---

## Updating the Application

When a new version of the script or application is available:

```bash
cd /opt/shoma

# Pull latest code (if using git)
git pull

# Rebuild and restart
docker compose -f docker-compose.prod.yml up -d --build

# Run migrations if there are database changes
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## Updating the Group Mapping File

When Taylor Bui (NetSuite admin) provides an updated `GROUP MAPPING.xlsx`:

1. Replace the file at `docs/Re_ FEMR /GROUP MAPPING.xlsx` on the server.
2. No restart required — the script reads the file at runtime.

> **Important:** Do not rename the file or the folder (`Re_ FEMR ` has a trailing space — keep it exactly as-is).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Browser shows "connection refused" | Containers not running — run `docker compose -f docker-compose.prod.yml up -d` |
| Export job fails immediately | Check `ORACLE_CLIENT_ID` and `ORACLE_SECRET_KEY` are set correctly in `.env.prod` |
| Export job fails with "No such file" | `GROUP MAPPING.xlsx` missing or renamed — check `docs/Re_ FEMR /GROUP MAPPING.xlsx` exists |
| Database error on startup | Run `docker compose -f docker-compose.prod.yml exec web python manage.py migrate` |
| Container exits repeatedly | Check logs: `docker compose -f docker-compose.prod.yml logs web` |
| Permission errors on startup | Ensure Docker is running in rootless mode — do not add `user:` to compose services |

---

## Port Reference

| Service | Internal port | External port |
|---------|--------------|---------------|
| Web app | 8000 | 8000 |
| PostgreSQL | 5432 | not exposed |
| Redis | 6379 | not exposed |

---

# FEMR Export Web App — Implementation Plan

**Date:** 2026-04-28  
**Stack:** Django 6 + Celery + Redis + Docker  
**Scope:** New Django app `femr_export` inside existing `src/` project  
**Log strategy:** File per job + JS polling (Option A)

---

## Overview

Users visit `/femr/`, select a group (WFD / Internal / Comml / OGA / ADP / All),
click Run. The app checks if that group is already running — if yes, shows a
notice with a link to the active job. If no, creates a job record, dispatches a
Celery task, and redirects to the job detail page where live logs stream via
polling and download buttons appear when done.

---

## Step 1 — Docker: Add Redis + Celery Worker

### `docker-compose.yml` (dev)
Add two new services:
```yaml
  redis:
    image: redis:7-alpine
    restart: unless-stopped

  celery_worker:
    build:
      context: .
      target: development
    volumes:
      - ./src:/app
      - ./src/media:/app/media
    user: "${UID}:${GID}"
    env_file: .env
    environment:
      DEBUG: "True"
    depends_on:
      - redis
    command: celery -A backend worker --loglevel=info --concurrency=5
```

### `docker-compose.prod.yml` (prod)
Add:
```yaml
  redis:
    image: redis:7-alpine
    restart: unless-stopped

  celery_worker:
    build:
      context: .
      target: production
    env_file: .env.prod
    volumes:
      - media_prod:/app/media
      - logs_prod:/app/logs
    depends_on:
      - redis
    restart: unless-stopped
    command: celery -A backend worker --loglevel=info --concurrency=5
```

Both `web` and `celery_worker` get `depends_on: redis`.

---

## Step 2 — requirements.txt

Add:
```
celery==5.4.0
redis==5.2.1
```

---

## Step 3 — Celery Config in `backend/settings.py`

Add at the bottom:
```python
# ─── Celery ───────────────────────────────────────────────────────────────────
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = TIME_ZONE

# FEMR export output directory
FEMR_OUTPUT_DIR = BASE_DIR / 'media' / 'femr_outputs'
FEMR_LOG_DIR = BASE_DIR / 'logs' / 'femr_jobs'
```

Add `femr_export` to `INSTALLED_APPS`.

Add logging config for `femr_export` logger (same pattern as `transform`).

---

## Step 4 — `backend/celery.py` (new file)

Standard Celery app setup:
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Update `backend/__init__.py` to import the celery app so it loads with Django.

---

## Step 5 — New App: `src/femr_export/`

### Files to create:
```
src/femr_export/
├── __init__.py
├── apps.py
├── models.py
├── tasks.py
├── views.py
├── urls.py
├── admin.py
└── migrations/
    └── __init__.py
```

---

## Step 6 — `femr_export/models.py`

```python
class FemrJob(models.Model):
    STATUS_PENDING  = 'pending'
    STATUS_RUNNING  = 'running'
    STATUS_DONE     = 'done'
    STATUS_FAILED   = 'failed'

    GROUP_CHOICES = [
        ('WFD',      'WFD'),
        ('Internal', 'Internal'),
        ('Comml',    'Comml'),
        ('OGA',      'OGA'),
        ('ADP',      'ADP'),
        ('All',      'All Groups'),
    ]

    group           = models.CharField(max_length=20, choices=GROUP_CHOICES)
    status          = models.CharField(max_length=20, default=STATUS_PENDING)
    celery_task_id  = models.CharField(max_length=255, blank=True)
    log_file        = models.CharField(max_length=500, blank=True)   # absolute path
    output_prefix   = models.CharField(max_length=500, blank=True)   # e.g. femr_v15_wfd
    started_at      = models.DateTimeField(null=True, blank=True)
    finished_at     = models.DateTimeField(null=True, blank=True)
    error_message   = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # Lifecycle helpers: mark_running(), complete(), fail()
    # Property: is_active → status in (pending, running)
    # Property: output_files → glob media/femr_outputs/femr_v15_<group>*.xlsx
```

---

## Step 7 — `femr_export/tasks.py`

```python
@shared_task(bind=True)
def run_femr_export(self, job_id: int):
    job = FemrJob.objects.get(pk=job_id)
    job.mark_running(celery_task_id=self.request.id)

    # Build command: venv/shoma/bin/python -u scripts/femr_netsuite_report_15.py
    #   --group <group> -o <output_prefix> --workers 40
    # Stream stdout+stderr line-by-line to job.log_file
    # On completion: job.complete()
    # On exception: job.fail(str(e))
```

Key points:
- Use `subprocess.Popen` with `stdout=PIPE, stderr=STDOUT` to capture logs in real time
- Write each line to the job's log file immediately (unbuffered)
- Script path: relative to Django `BASE_DIR` → `BASE_DIR.parent / 'scripts' / 'femr_netsuite_report_15.py'`
- Python path: `BASE_DIR.parent / 'venv' / 'shoma' / 'bin' / 'python'`
- Output prefix written to `settings.FEMR_OUTPUT_DIR`

---

## Step 8 — `femr_export/views.py`

### `RunView` (POST `/femr/run/`)
```
1. Get group from POST data
2. Check: FemrJob.objects.filter(group=group, status__in=['pending','running']).first()
3. If found → redirect to job detail with "already running" message
4. If not → create FemrJob, dispatch run_femr_export.delay(job.id), redirect to detail
```

### `JobDetailView` (GET `/femr/jobs/<id>/`)
- Renders job detail page with status, log panel, download buttons
- Download buttons only shown when status=done

### `LogPollView` (GET `/femr/jobs/<id>/log/?offset=<N>`)
- Opens job.log_file, seeks to byte offset N
- Returns JSON: `{"lines": "...", "offset": <new_offset>, "done": true/false}`
- JS calls this every 3s, appends lines to log panel, stops when done=true

### `DownloadView` (GET `/femr/jobs/<id>/download/<filename>`)
- Serves the xlsx file as attachment
- Only if job.status == done

---

## Step 9 — Templates

### `templates/femr_export/index.html`
- Extends `base.html`
- Group dropdown (WFD, Internal, Comml, OGA, ADP, All)
- Run button → POST to `/femr/run/`
- Recent jobs table (last 10): group, status, started_at, link to detail

### `templates/femr_export/job_detail.html`
- Status badge (colour-coded: running=blue, done=green, failed=red)
- Log panel: `<pre>` with monospace text, auto-scrolls to bottom
- JS polling: fetch `/femr/jobs/<id>/log/?offset=N` every 3s
  - Appends new lines, updates offset
  - Stops polling when `done=true`
  - On done: reload page to show download buttons
- Download section (hidden until done): one button per output file

---

## Step 10 — `backend/urls.py`

Add:
```python
path('femr/', include('femr_export.urls', namespace='femr_export')),
```

### `femr_export/urls.py`
```
GET  /femr/                      → index (group selection + recent jobs)
POST /femr/run/                  → RunView
GET  /femr/jobs/<id>/            → JobDetailView
GET  /femr/jobs/<id>/log/        → LogPollView
GET  /femr/jobs/<id>/download/<filename>/ → DownloadView
```

---

## Build Order

| # | Step | Files touched |
|---|------|--------------|
| 1 | Docker: add redis + celery_worker | `docker-compose.yml`, `docker-compose.prod.yml` |
| 2 | Dependencies | `requirements.txt` |
| 3 | Celery app | `backend/celery.py`, `backend/__init__.py` |
| 4 | Settings | `backend/settings.py` |
| 5 | Model + migration | `femr_export/models.py`, migration |
| 6 | Celery task | `femr_export/tasks.py` |
| 7 | Views | `femr_export/views.py` |
| 8 | URLs | `femr_export/urls.py`, `backend/urls.py` |
| 9 | Templates | `index.html`, `job_detail.html` |
| 10 | Admin | `femr_export/admin.py` |
| 11 | Test single run locally | smoke test WFD group |

---

## Environment Variables to Add

| Variable | Dev default | Purpose |
|----------|-------------|---------|
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Celery broker + result backend |

Add to `.env` and `.env.prod`.

---

## Notes / Constraints

- Script path in Docker: the `src/` dir is `/app` inside the container. The scripts dir is one level up at `../scripts/` relative to `BASE_DIR`. Need to confirm this path is accessible inside the container — may need to mount `scripts/` as a volume or copy into the image.
- The v15 script uses `venv/shoma/bin/python` — inside Docker the venv is not present; the container uses the system Python from the image. Task should call `sys.executable` or `python` directly, not the venv path.
- `--workers 40` is fine on the server; inside Docker verify the container has enough CPU/RAM.
- SQLite + Celery: SQLite handles concurrent reads fine but can lock under concurrent writes. Since each job writes its own row and log file, this should be safe. If issues arise, switch to PostgreSQL later.

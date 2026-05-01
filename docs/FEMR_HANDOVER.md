# FEMR Tools — IT Handover Guide

**Client:** NextFlex  
**Prepared by:** Daden.dev (Atul Kumar)  
**Date:** April 2026  

---

## Overview

This package contains two tools:

| Tool | What it does |
|------|-------------|
| **FEMR Export** | Pulls financial data from the Oracle APEX API and generates multi-tab Excel workbooks — one tab per project sequence — for all reporting groups (WFD, Internal, Comml, OGA, ADP) |
| **FEMR Transform** | Takes a raw FEMR Funds Excel file and reshapes it into a normalized long-format output for use in Power BI / Tableau |

Both tools run as a single web application accessible via browser. No terminal knowledge is required to operate them after initial setup.

---

## Prerequisites

The server running these tools needs:

- **Docker** (version 20+)
- **Docker Compose** (version 2+)
- Internet access to reach the Oracle APEX API
- At least **4 GB RAM** and **20 GB disk space** (ADP runs generate ~1.5 GB of Excel files)
- **Oracle API credentials** (client ID and secret) — obtain from Josh Grapani before setup

To check if Docker is installed:
```bash
docker --version
docker compose version
```

---

## Setup (One-Time)

### 1. Get the files

Copy the entire project folder onto your server. The structure should look like:

```
femr-pipeline/
├── docker-compose.prod.yml
├── Dockerfile
├── requirements.txt
├── scripts/
│   └── femr_netsuite_report_16.py   ← FEMR Export script
├── docs/
│   └── Re_ FEMR /
│       └── GROUP MAPPING.xlsx        ← sequence-to-group mapping (do not delete)
└── src/                              ← web application code
```

### 2. Create the environment file

```bash
cp .env.example .env.prod
```

Open `.env.prod` and set these values:

```ini
# Required — generate a random string (e.g. openssl rand -hex 32)
SECRET_KEY=your-long-random-secret-key-here

# Set to False for production
DEBUG=False

# Your server's IP address or domain name (comma-separated if multiple)
ALLOWED_HOSTS=your-server-ip,your-domain.com

# Celery broker — leave as-is if using the included Docker Redis
CELERY_BROKER_URL=redis://redis:6379/0

# Path to the project root inside Docker — leave as-is
FEMR_REPO_ROOT=/repo

# Oracle APEX API credentials — required for FEMR Export to work
# Obtain from Josh Grapani (NextFlex tech lead)
ORACLE_CLIENT_ID=your-client-id-here
ORACLE_SECRET_KEY=your-secret-key-here

# Leave defaults below
UID=1000
GID=1000
DJANGO_LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=50
```

> **Important:** The `ORACLE_CLIENT_ID` and `ORACLE_SECRET_KEY` values are required. Without them the export script will fail immediately with a credentials error. Get these values from Josh Grapani before running any export.

### 3. Build and start

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

This starts three containers: `web` (Django), `redis` (message broker), `celery_worker` (background job runner).

### 4. Run the database migration (first time only)

```bash
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### 5. Open the app

Visit `http://your-server-ip:8000` in a browser.

---

## Using the FEMR Export Tool

### Access
Navigate to `http://your-server-ip:8000/femr/`

### Running an export

1. Select a **Group** from the dropdown:
   - **WFD** — Workforce Development (~28 tabs, ~2 hours)
   - **Internal** — Internal projects (~37 tabs, ~2.5 hours)
   - **Comml** — Commercial (~41 tabs, ~3 hours)
   - **OGA** — Other Government Agency (~47 tabs, ~3.5 hours)
   - **ADP** — ADP projects (~247 tabs across 5 files, ~8–9 hours)
   - **All Groups** — runs all of the above overnight

2. Click **Run Export**.

3. The app checks whether that group is already running. If a job is already in progress, you will see a notice with a link to that job — do not start a duplicate.

4. You are redirected to the **Job Detail** page where you can watch live logs as the export runs.

5. When complete, **Download** buttons appear — one per output file. Click to download each Excel file.

### Job history
The index page (`/femr/`) shows the last 20 jobs with their status, start time, and duration.

### Important notes
- The ADP group generates 5 separate Excel files (001–050, 051–100, etc.) — download all 5.
- Runs pull live data from the Oracle APEX API each time. If the API is unavailable the job will fail — check the log for error details.
- Do not run the same group twice simultaneously.

---

## Using the FEMR Transform Tool

### Access
Navigate to `http://your-server-ip:8000/` (the home page)

### Running a transform

1. Upload an `.xlsx` file containing the `FEMR Funds` sheet.
2. The app processes it and redirects to a result page.
3. Download the transformed output file.

---

## Expected Output Files

After a successful FEMR Export run, you will receive:

| Group | Files | Tabs per file |
|-------|-------|--------------|
| WFD | `femr_v16_wfd.xlsx` | 28 |
| Internal | `femr_v16_internal.xlsx` | 37 |
| Comml | `femr_v16_comml.xlsx` | 41 |
| OGA | `femr_v16_oga.xlsx` | 47 |
| ADP | `femr_v16_adp_001-050.xlsx` | 50 |
| ADP | `femr_v16_adp_051-100.xlsx` | 50 |
| ADP | `femr_v16_adp_101-150.xlsx` | 50 |
| ADP | `femr_v16_adp_151-200.xlsx` | 50 |
| ADP | `femr_v16_adp_201-246.xlsx` | 46 |

Each tab contains one project sequence with:
- Header section (project name, group, rollup number, contacts)
- Quarterly financial data (Actuals, Budget, Contracting) from FY2020 to current quarter
- Cumulative section with running totals from FY2016
- Line chart showing all five financial metrics over time

---

## Updating the Group Mapping

When new sequences are added to NetSuite or groups change, the mapping file must be updated:

1. Replace `docs/Re_ FEMR /GROUP MAPPING.xlsx` with the updated file from Taylor Bui (NetSuite admin).
2. Restart the celery worker to pick up the change:
   ```bash
   docker compose -f docker-compose.prod.yml restart celery_worker
   ```
3. Re-run the affected groups.

---

## Rotating API Credentials

If the Oracle API credentials are ever changed by the NextFlex IT/Oracle team:

1. Open `.env.prod` and update `ORACLE_CLIENT_ID` and `ORACLE_SECRET_KEY` with the new values.
2. Restart both services to pick up the new credentials:
   ```bash
   docker compose -f docker-compose.prod.yml restart web celery_worker
   ```
3. Run a single-sequence test to confirm the new credentials work before starting a full group run.

---

## Stopping and Restarting

```bash
# Stop all containers
docker compose -f docker-compose.prod.yml down

# Start again
docker compose -f docker-compose.prod.yml up -d

# Restart a single service (e.g. after code update)
docker compose -f docker-compose.prod.yml restart web
docker compose -f docker-compose.prod.yml restart celery_worker
```

---

## Monitoring and Logs

### View live logs for a running container
```bash
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f celery_worker
```

### Application log files (inside the container)
```bash
docker compose -f docker-compose.prod.yml exec web tail -f logs/app.log
```

### Job-specific logs
Each export job writes its own log file. These are visible in the browser on the Job Detail page. They are stored at `src/logs/femr_jobs/job_<id>.log` inside the container.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| `/femr/` shows database error | Migration not run | `docker compose exec web python manage.py migrate` |
| Job stays in "Pending" forever | Celery worker not running | `docker compose -f docker-compose.prod.yml up -d celery_worker` |
| Job fails with "ORACLE_CLIENT_ID and ORACLE_SECRET_KEY must be set" | Credentials missing from `.env.prod` | Add `ORACLE_CLIENT_ID` and `ORACLE_SECRET_KEY` to `.env.prod`, then restart containers |
| Job fails with "HTTP Error 401" | API credentials are wrong or expired | Check credential values with Josh Grapani, update `.env.prod`, restart containers |
| Job fails with "Script exited with code 1" | API unreachable or script error | Check job log in the browser for the exact error |
| Download button shows but file is empty | Run was interrupted mid-way | Re-run the group |
| "Already running" but no active job visible | Job stuck in running state | Go to `/admin/`, find the job, set status to `failed` manually |
| Tab count less than expected | Transient API failure for one sequence | Re-run the affected group |

---

## Contact

For script issues, data questions, or API access:  
**Daden.dev** — Atul Kumar  

For NetSuite data corrections (rollup/sequence mapping):  
**Taylor Bui** — NextFlex NetSuite Admin  

For report requirements and business questions:  
**Josh Grapani** — NextFlex Tech Lead  
**Shoma Sinha** — NextFlex PM  

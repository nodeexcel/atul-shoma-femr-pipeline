# FEMR Transform

A Django web application that reshapes **FEMR Funds** Excel data from wide format into a long-format quarterly output, ready for reporting tools (Power BI, Tableau, etc.).

---

## What it does

Reads the `FEMR Funds` sheet from an uploaded `.xlsx` workbook and writes a normalized `Output` sheet with one row per `(Sequence, Quarter, Type)`:

| Sequence | Qtr Date   | Type           | Amount     |
|----------|------------|----------------|------------|
| 2ADP001  | 06/30/2020 | Committed      | 0          |
| 2ADP001  | 06/30/2020 | Obligated      | 0          |
| 2ADP001  | 06/30/2020 | Expended       | 0          |
| 2ADP001  | 06/30/2020 | Remaining Cash | 0          |
| 2ADP001  | 09/30/2020 | Committed      | 27,100,000 |
| …        | …          | …              | …          |

- **26 quarters** tracked: FY20 Q3 (Jun 2020) → FY26 Q4 (Sep 2026)
- **134 sequences** per quarter × **4 types** = **13,936 output rows**
- Sequences appearing on multiple input rows are automatically **summed**

---

## Project Structure

```
shoma/
├── Dockerfile                  # Multi-stage build (development + production)
├── docker-compose.yml          # Local development
├── docker-compose.prod.yml     # Production
├── .env.example                # Environment variable template
├── requirements.txt
├── TODO.md                     # Task tracking
├── scripts/
│   └── femr_transform.py       # Standalone CLI version of the transform
└── src/
    ├── manage.py
    ├── backend/                # Django project settings
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── transform/              # Transform app
    │   ├── models.py           # TransformJob
    │   ├── forms.py            # UploadForm
    │   ├── services.py         # Core transform logic
    │   ├── views.py            # Upload, detail, download
    │   ├── urls.py
    │   └── admin.py
    ├── templates/
    │   ├── base.html
    │   └── transform/
    │       ├── upload.html
    │       ├── job_detail.html
    │       └── _status_badge.html  # Reusable component
    └── logs/
        ├── system.log          # Django / project-level logs
        └── app.log             # Transform app logs
```

---

## Environment Variables

Copy `.env.example` to `.env` (local) or `.env.prod` (production) and fill in:

| Variable             | Default     | Description                              |
|----------------------|-------------|------------------------------------------|
| `SECRET_KEY`         | insecure dev key | Django secret key — **change in prod** |
| `DEBUG`              | `True`      | Set to `False` in production             |
| `ALLOWED_HOSTS`      | `*`         | Comma-separated list of allowed hostnames |
| `DJANGO_LOG_LEVEL`   | `INFO`      | Log level for Django internals           |
| `MAX_UPLOAD_SIZE_MB` | `50`        | Maximum upload file size in MB           |

---

## Logging

Two separate log files under `src/logs/`:

| File         | What it captures                         |
|--------------|------------------------------------------|
| `system.log` | Django internals, requests, errors       |
| `app.log`    | Transform app activity (upload, processing, download) |

Both rotate at 10 MB, keeping 5 backups. Console output is always active.

To use the app logger in any module:

```python
import logging
logger = logging.getLogger('transform.your_module')
```

---

## Running Locally (without Docker)

```bash
# 1. Create and activate virtual environment
python -m venv venv/shoma
source venv/shoma/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Apply migrations
cd src
python manage.py migrate

# 5. Start dev server
python manage.py runserver
```

Open `http://localhost:8000`.

---

## Running with Docker

### Local development (live reload)

```bash
cp .env.example .env
docker compose up
```

Source code is mounted as a volume — changes to `src/` are reflected immediately without rebuilding.

### Production

```bash
cp .env.example .env.prod
# Edit .env.prod: set DEBUG=False, SECRET_KEY, ALLOWED_HOSTS

docker compose -f docker-compose.prod.yml up -d
```

The production image uses a **multi-stage build** to minimize image size:
1. **builder** — installs all Python dependencies
2. **development** — copies deps + mounts source for live reload
3. **production** — copies deps + source, runs `collectstatic`, serves via Gunicorn

---

## URL Reference

| URL                      | Name                    | Description                  |
|--------------------------|-------------------------|------------------------------|
| `/`                      | `transform:upload`      | Upload form + recent jobs    |
| `/jobs/<pk>/`            | `transform:job_detail`  | Job status and result        |
| `/jobs/<pk>/download/`   | `transform:download`    | Download output file         |
| `/admin/`                | —                       | Django admin                 |

---

## Transform Logic (services.py)

The core pipeline in `src/transform/services.py`:

```
run_transform(input_path)
  └── _read_sequences()       # get ordered sequence list (from Output template or input)
  └── _aggregate_data()       # sum quarterly values per sequence (handles multi-row seqs)
  └── _build_output_rows()    # expand to long format: seq × quarter × 4 types
  └── _write_output_sheet()   # write rows into Output tab, clear stale rows
  └── return xlsx bytes
```

The standalone CLI script (`scripts/femr_transform.py`) remains unchanged and can be run independently:

```bash
python scripts/femr_transform.py --input path/to/input.xlsx --output path/to/output.xlsx
```

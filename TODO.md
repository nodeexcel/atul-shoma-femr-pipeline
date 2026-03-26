# TODO

Track all pending, in-progress, and completed work here.
Update this file as tasks are started or finished.

---

## Legend
- `[ ]` Pending
- `[~]` In progress
- `[x]` Done

---

## Setup & Infrastructure
- [x] Add `gunicorn` and `whitenoise` to `requirements.txt`
- [x] Configure `settings.py` — env vars, whitenoise, media/static, logging
- [x] Multi-stage `Dockerfile` (builder → development → production)
- [x] `docker-compose.yml` — local dev with volume mount for live reload
- [x] `docker-compose.prod.yml` — production with named volumes and restart policy
- [x] `.env.example` — document all required environment variables
- [x] `.dockerignore`

## Django App — Transform
- [x] `TransformJob` model — status lifecycle (pending → processing → done / failed)
- [x] `UploadForm` — `.xlsx` validation and size limit
- [x] `services.py` — reusable FEMR transform pipeline (read → aggregate → build → write)
- [x] `UploadView` — file upload, triggers transform, redirects to result
- [x] `JobDetailView` — shows job status and download link
- [x] `download_output` view — streams output file as attachment
- [x] `transform/urls.py` — namespaced URLs
- [x] `TransformJobAdmin` — admin registration with list display and filters
- [x] Initial migration (`0001_initial`)

## Templates
- [x] `base.html` — Bootstrap 5, navbar, flash messages
- [x] `transform/upload.html` — upload form + recent jobs table
- [x] `transform/job_detail.html` — status display, download button, error output
- [x] `transform/_status_badge.html` — reusable status badge component

## Documentation
- [x] `README.md` — project overview, setup, usage, structure, env vars

---

## Backlog / Future Work
- [ ] Async processing — offload transform to Celery + Redis (needed if files are large)
- [ ] Job auto-cleanup — delete uploaded/output files after N days
- [ ] Progress polling — JS polling or WebSocket for live status on job detail page
- [ ] Input validation — verify required sheets (`FEMR Funds`) exist before processing
- [ ] Multiple transform types — support additional pipeline configs beyond FEMR
- [ ] User authentication — restrict upload/download to logged-in users
- [ ] Nginx reverse proxy — add nginx service to docker-compose.prod.yml
- [ ] Health check endpoint — `GET /health/` for container orchestration
- [ ] CI/CD pipeline — GitHub Actions for lint, test, and Docker build
- [ ] Unit tests — cover `services.py` (safe_float, aggregate, build_output_rows)

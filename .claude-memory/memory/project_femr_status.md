---
name: FEMR project status and architecture
description: Current state of FEMR NetSuite Report Generator — script versions, what's done, what's pending, key technical decisions
type: project
originSessionId: 03ce2e1b-d66e-4c61-9283-53647745d1bc
---
## Project: FEMR NetSuite Multi-Tab Excel Report Generator

**Client:** NextFlex (Shoma Sinha PM, Josh Grapani tech lead, Taylor Bui NetSuite admin)
**Developer:** Atul Kumar (via Daden.dev)
**Claude sessions managed by:** Rahul (rahul@daden.dev)
**Goal:** Python ETL that pulls financial data from Oracle APEX REST API and generates multi-tab Excel workbooks matching the FEMR Export Template.

---

## Script Versions

| Version | Key Changes | Status |
|---------|-------------|--------|
| v1–v11 | Early iterations through file splitting | Archived |
| v12 | Chart axis labels fix, pre-FY2020 cumulative seeding, non-breaking space labels, dynamic chart width | Archived |
| v13 | Local JSON cache with quarter-based invalidation (`--cache-dir`, `--force-refresh`) | **PERMANENTLY SHELVED** — Josh rejected (data refreshes daily) |
| v14 | v12 + legend→right + catAx crosses=min (x-axis stays bottom when Y negative) | Archived |
| v15 | v14 + legend outside plot area (overlay=False) + quarter labels below grid (tickLblPos="low") | Archived |
| v16 | v15 + OAuth Bearer token auth on all API requests | Archived — bug found in MV path |
| **v17** | v16 + OAuth header added to `_fetch_mv_by_identifier()` (MV path was missing auth — caused 2ADP099 R1099 empty tabs) | **ACTIVE — tested 2026-05-05** |

**IMPORTANT:** v13 cache concept was **REJECTED by Josh (2026-04-29)** — data refreshes daily so caching would be stale. v13 is permanently shelved. v16 is current.

---

## v16 — OAuth Auth (2026-04-29)

| Item | Detail |
|------|--------|
| Token endpoint | `BASE_URL/oauth/token` |
| Grant type | `client_credentials` |
| Credentials | `ORACLE_CLIENT_ID` + `ORACLE_SECRET_KEY` in `.env` |
| Token lifetime | 3600s (confirmed from Oracle response) |
| Auto-refresh | Yes — refreshes when within 300s of expiry (safe for 8-9h ADP runs) |
| Scope | Both `_http_get()` and `_fetch_netamount()` send `Authorization: Bearer <token>` |
| Test | `--sequence 2ADP001 -o test_v16.xlsx --skip-preload` — completed successfully 2026-04-29 |
| `.env` typo fixed | `ORABLE_SECRET_KEY` → `ORACLE_SECRET_KEY` |

**Credential setup for server:** copy `.env.example` to `.env`, fill in `ORACLE_CLIENT_ID` and `ORACLE_SECRET_KEY` from Josh. Load with `set -a && source .env && set +a` before running.

---

## v16 Full Run Status — COMPLETE ✅ (2026-04-29 14:33 → 2026-04-30 ~08:00)

| Group | Expected tabs | Got | Status | Notes |
|-------|--------------|-----|--------|-------|
| ADP (all 5 files) | 246 | 247 | ✅ | 2ADP099 has 2 tabs (R1099 + RCore099) — known invalid rollup, both empty |
| Comml | 41 | 41 | ✅ | |
| Internal | 37 | 37 | ✅ | |
| OGA | 47 | 47 | ✅ | |
| WFD | 28 | 28 | ✅ | EWD014 first tab, correct |

**Available Funds verification (Josh's list — 27 sequences):** All match to the cent ✅
**2ADP061 G&A 5991 Budgeted FY2026:** Blank ✅ (Josh's concern already resolved in v16)
**2ADP099:** 2 tabs generated (R1099 + RCore099), both empty due to 401s — known issue, Taylor to clean up Rollup 1099 in NetSuite
**2ADP083:** Josh listed twice with conflicting values ($0 and $14,695.00) — awaiting clarification

**Files downloaded to local:** all 9 femr_v16_*.xlsx files in project root

---

## v15 Run Status (as of 2026-04-29) — ALL COMPLETE ✅

| Group | Expected tabs | Status | Output file | Notes |
|-------|--------------|--------|-------------|-------|
| WFD | 28 | ✅ Verified | femr_v15_wfd.xlsx | chart fixes ✅ |
| Internal | 37 | ✅ Verified | femr_v15_internal.xlsx | chart fixes ✅ |
| Comml | 41 | ✅ Verified | femr_v15_comml.xlsx | chart fixes ✅ |
| OGA | 47 | ✅ Verified | femr_v15_oga.xlsx | chart fixes ✅ |
| ADP | 247 (5 files) | ✅ Verified | femr_v15_adp_*.xlsx | All 5 files, 247 tabs ✅ |

**Verification results (verify_v15.py — 2026-04-29):**
- Chart XML: legend=r, overlay=0, crosses=min, tickLblPos=low, Y-axis visible — all 5 spot-checked files ✅
- Group mapping: EWD014 in WFD not OGA ✅, OGA047 in OGA ✅, CC007 = 1 tab ✅
- 2ADP022: non-zero financial data ✅
- 2ADP001 G&A: present ✅
- Header fields: correct (NextFlex, sequence names, contacts) ✅
- Open question: EWD014 has no financial data — needs Josh confirmation if expected for this sequence

---

## Josh Feedback — All Addressed

| Issue | Fix | Version |
|-------|-----|---------|
| Legend overlaps X-axis quarter labels | `chart.legend.position = "r"` | v14 |
| X-axis labels jump to top when Y is negative | `<crosses val="min" />` in `_patch_chart_axes()` | v14 |
| CC007 1 tab vs 2 | Confirmed by Josh: 960011 is child of 4006, 1 tab correct | v14 |
| 2ADP001 G&A missing | Not a bug — data present in quarters with spend | v14 |
| 2ADP022 empty | Transient API failure in original run — re-run fixed it | v14 |
| Quarter labels sit on zero line inside grid | `tickLblPos="low"` in catAx XML patch | v15 |
| Legend floating inside chart plot area | `chart.legend.overlay = False` | v15 |

---

## Web App — BUILT (2026-04-28/29)

**Framework:** Django (same project as contracting transform app in `src/`)
**Background jobs:** Celery + Redis (Redis as broker)
**Log streaming:** File-based per job + JS polling every 3s
**Docker:** `redis` + `celery_worker` services added to docker-compose files
**Django app:** `src/femr_export/`

**Pages:**
- `/femr/` — group selection + Run button + last 20 jobs
- `/femr/jobs/<id>/` — live log panel, status badge, download buttons when done
- `/femr/jobs/<id>/log/?offset=N` — polling endpoint
- `/femr/jobs/<id>/download/<filename>/` — file download

**Status:** Built and DB migrated. Pending end-to-end test with a real group run.

---

## Handover Package — UPDATED (2026-05-01)

**Shoma's request (2026-04-29):** Upload script + docs to external shared folder, clean handover documentation.

**Current zip:** `femr_handover_v16.zip` (3.0 MB) in project root — rebuilt 2026-05-01.

**Contents:**
```
femr-pipeline/
├── FEMR_SCRIPT_GUIDE.md          ← updated: v16, credential setup, no contact block
├── requirements_script.txt        ← pip install -r this (openpyxl only)
├── scripts/
│   └── femr_netsuite_report_16.py ← active script with OAuth auth
├── docs/
│   └── Re_ FEMR /
│       └── GROUP MAPPING.xlsx     ← required at runtime
└── output/
    └── femr_v16_*.xlsx            ← all 9 verified v16 output files ✅
```

**Also created:** `femr_transform_handover.zip` (8 KB) — separate zip for contracting transformation script.

**Doc convention going forward:** No contact block at end of documentation files.

**Note:** v17 is now active. Handover zip still contains v16 script — rebuild with v17 after ADP run completes and is verified.

---

## v17 ADP Run — IN PROGRESS (2026-05-05)

**Server:** Ubuntu server, user `pythonai`, project dir `~/atul-shoma-femr-pipeline`
**Command:**
```bash
nohup python -u scripts/femr_netsuite_report_17.py --group ADP -o /app/media/femr_outputs/femr_v17 --workers 40 &
```
**Started:** ~07:58 UTC 2026-05-05
**Log:** `nohup.out` in project root on server
**OAuth token:** fetched OK ✅
**Expected duration:** ~8-9 hours
**Expected output:** 5 files — `femr_v17_adp_001-050.xlsx` … `femr_v17_adp_201-246.xlsx`

**Server `.env` note:** credentials were manually exported (`export ORACLE_CLIENT_ID=...`). For future runs, add to `.env` and use `set -a && source .env && set +a`.

**Monitor:**
```bash
tail -f nohup.out
ps aux | grep femr_netsuite_report | grep -v grep
```

---

## Deployment Plan (agreed 2026-04-28)

- **Handover package** goes into external shared folder (Jason Peabody's invite — Atul has access)
- **Running the script** requires a local machine or virtual server with Python — NOT the shared folder itself
- NextFlex IT team handles actual hosting/deployment decision
- Web app deployable on AWS EC2 or similar

---

## Access Status (as of 2026-04-28)

| System | Status |
|--------|--------|
| Oracle APEX REST API | ✅ Access — no auth required (yet) |
| NetSuite production | ✅ Josh gave Atul production access during 2026-04-28 meeting |
| External shared folder (Jason Peabody) | ✅ Atul accepted invite, created account |
| Oracle platform (for API auth setup) | ✅ Done — Josh secured endpoints, shared client ID + secret, Atul tested and confirmed access token works (2026-04-29) |

---

## Handover Upload Status (2026-05-01) ✅

All v16 files uploaded to NextFlex shared folder:
- All 9 `femr_v16_*.xlsx` output files ✅
- `femr_handover_v16.zip` (v16 script + FEMR_SCRIPT_GUIDE.md + GROUP MAPPING + requirements) ✅
- `femr_transform_handover.zip` (transform script + FEMR_TRANSFORM_GUIDE.md) ✅

---

## Transformation Script v2 — COMPLETE ✅ (2026-05-03)

**Script:** `scripts/femr_transform_2.py`

Changes from v1 (requested in May 1 meeting with Josh + Shoma):
1. **Strip input tabs** — output Excel contains ONLY the Output tab (no FEMR Funds, SF270 CA2, etc.)
2. **CSV support** — `--format excel` (default) or `--format csv`
3. **Auto-derive output filename** — `output_<input_name>.<ext>` in same folder as input; `--output` still works as explicit override
4. Dead code removed (`copy_sheet_with_formatting`, `write_output_sheet`)

Tested: 134 sequences × 22 quarters × 4 types = 11,792 rows. Both formats verified ✅

---

## Web App Transform Pipeline — UPDATED ✅ (2026-05-03)

Files changed:
- `src/transform/services.py` — `run_transform(input_path, fmt)`: Output-only Excel or CSV bytes; `_write_output_sheet` removed
- `src/transform/forms.py` — `output_format` radio field (Excel / CSV)
- `src/transform/models.py` — `output_format` field; `complete()` uses `output_<stem>.xlsx` or `.csv`
- `src/transform/views.py` — passes `output_format` to `create()` and `run_transform()`
- `src/templates/transform/upload.html` — radio buttons for format selection
- `src/transform/migrations/0002_transformjob_output_format.py` — migration applied ✅

Django check: 0 issues. Service smoke test: both formats correct ✅

---

## Docker Setup — WORKING ✅ (2026-05-04)

Fixes applied:
1. `src/backend/settings.py` — script `femr_netsuite_report_15.py` → `_16.py`
2. `src/femr_export/tasks.py` — output prefix `femr_v15_*` → `femr_v16_*`
3. `docker-compose.yml` + `docker-compose.prod.yml` — added `FEMR_REPO_ROOT: "/repo"` to web + celery_worker
4. **PostgreSQL added** — `postgres:16-alpine` service (`db`), named volumes `postgres_dev` / `postgres_prod`
5. **Rootless Docker fix** — removed `user: "${UID}:${GID}"` from web + celery_worker (rootless Docker remaps UIDs automatically; explicit user directive causes permission errors)
6. `requirements.txt` — added `psycopg2-binary==2.9.10`
7. `settings.py` — DB switched from SQLite to PostgreSQL, reads `DB_NAME/USER/PASSWORD/HOST/PORT` from env
8. `.env.example` — added `DB_*` vars, removed `UID`/`GID`

**Server is rootless Docker** — never use `user:` directive in compose files for this project.

Dev postgres port: `5436:5432` (user changed from default 5432 to avoid conflicts).

To run migrations after bringing up containers:
```bash
docker compose exec web python manage.py migrate
```

---

## IT Server Setup — COMPLETE ✅ (2026-05-05)

**Server:** Windows Server 2025
**IT team:** Andy + Jason (Jason Peabody)
**Setup done:**
- Python 3.14 installed ✅
- Docker Desktop installed (had elevation issue — fixed by deleting ProgramData/Docker folder and re-running full installer) ✅
- WSL updated ✅
- `femr_webapp_handover.zip` extracted on server desktop (user `jpbody`) ✅
- `.env.prod` file created with credentials ✅

**NOT run yet** — Shoma decided to wait for Taylor's confirmed final data files before running. Don't want incorrect data going to government.

**Next run meeting:** Tuesday 2026-05-06 or Wednesday 2026-05-07 — depends on when Taylor confirms data.

**Two commands to start the app when ready:**
```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## Pending Items — Next Session START HERE

| # | Item | Priority |
|---|------|----------|
| 1 | Wait for Taylor's confirmed final data files — Shoma chasing Taylor | **HIGHEST — blocked on Taylor** |
| 2 | Monitor ADP v17 run on server — check nohup.out, verify 2ADP099 R1099 has data when complete | **IN PROGRESS — running on server since ~07:58 UTC** |
| 3 | Attend Tuesday 2026-05-06 script run meeting (Atul + Josh) | High |
| 4 | After re-run: flag changes in new output vs v16 to Shoma | High (after re-run) |
| 5 | Note: 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 will have values in next run — expected, NOT a bug | Note |
| 6 | Test web app transform end-to-end (both Excel and CSV formats) | Medium |
| 7 | Future feature: sequence-level selection (Diane's request via Josh 2026-04-29) | Low — after handover |
| 8 | Josh to add NSAW upload process to handover docs | Awaiting Josh |

---

## Key Technical Decisions (permanent record)

1. **API architecture**: `/femr/netamount/` for financial data, `/mv_femr_report/` for metadata.
2. **netamount API silently ignores rollup filter** — use MV for multi-identifier sequences.
3. **Orphan identification**: `class='Orphan'` → use `project_number` as Rollup# display.
4. **SERVICE field**: use `display_type_c`, not `service`.
5. **Cumulative formulas**: `=C45` first quarter, `=D45+B52` pattern. Pre-FY2020 seeded as literal.
6. **Remaining Cash**: `=Obligated - Expended` per quarter.
7. **Dynamic mapping**: from `docs/Re_ FEMR /GROUP MAPPING.xlsx` SEQUENCE sheet.
8. **File splitting**: 50 tabs per file for large groups.
9. **Quarter range**: auto-detected from MV. Currently Q4 FY2026.
10. **Excel Online ignores chart label rotation** — `bodyPr rot` ineffective.
11. **_patch_chart_axes()**: post-processor after every `wb.save()`.
12. **Non-breaking space in `_q_label()`**: prevents Excel multi-level axis grouping.
13. **Dynamic chart width**: `max(25, num_quarters * 1.5)` cm.
14. **v13 cache**: quarter-key invalidation, `--cache-dir`, `--force-refresh`. NOT IN PRODUCTION YET.
15. **Chart legend**: must be on RIGHT (`"r"`) — Josh confirmed 2026-04-27.
16. **catAx crosses**: must be `"min"` — keeps x-axis at bottom when Y is negative.
17. **catAx tickLblPos**: must be `"low"` — pushes quarter labels outside/below plot area. Josh confirmed 2026-04-28.
18. **chart.legend.overlay**: must be `False` — forces legend outside the chart plot area. Confirmed 2026-04-28.
19. **API authentication**: currently none on Oracle endpoints. Must be added at Oracle platform level (not script). Pending follow-up meeting.
20. **Delivery**: files go to external shared folder (not email). Handover zip includes script + docs + output files.
24. **OAuth auth (v16)**: `_fetch_oauth_token()` uses HTTP Basic Auth (client_id:secret) to POST `grant_type=client_credentials` to token endpoint. `_get_auth_header()` is thread-safe (Lock), returns `Authorization: Bearer <token>`, auto-refreshes 300s before expiry. Both `_http_get()` and `_fetch_netamount()` call it.
21. **Cumulative section formulas**: openpyxl data_only=True returns None for formula cells — expected, NOT a bug. Cells contain =C45, =D45+B52 etc. pattern.
22. **Docker venv**: Docker container has no venv — use sys.executable in Celery task, not hardcoded venv path.
23. **Script --mapping default path**: `docs/Re_ FEMR /GROUP MAPPING.xlsx` (trailing space in folder name). Handover zip preserves this exact path.

---

## API Details

- Base URL: `https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user`
- `/femr/netamount/` — fast, single-identifier sequences only
- `/mv_femr_report/` — full MV (~2M rows), use for multi-identifier and metadata
- ~836 API calls per sequence (756 main + 80 pre-FY2020)
- **Authentication**: OAuth client credentials — Josh secured endpoints 2026-04-29. Token endpoint: `BASE_URL/oauth/token`. Credentials: `ORACLE_CLIENT_ID` + `ORACLE_SECRET_KEY` in `.env`. Token lifetime 3600s, auto-refreshed at 300s before expiry. **Implemented and tested in v16.**

---

## How to apply

When starting a new session: read this file, then `project_data_issues.md`, then `docs/client_communications_log.md`. Check Known Blockers in CLAUDE.md before doing anything.

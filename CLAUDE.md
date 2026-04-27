# CLAUDE.md — FEMR NetSuite Report Generator

## Project Context

Python ETL that pulls financial data from Oracle APEX REST API and generates
multi-tab Excel workbooks matching the FEMR Export Template.

**Client:** NextFlex (Shoma Sinha PM, Josh Grapani tech lead, Taylor Bui NetSuite admin)
**Dev:** Atul Kumar (Daden.dev) — Claude sessions managed by Rahul (rahul@daden.dev)
**Active script:** `scripts/femr_netsuite_report_14.py`

**NOTE:** v13 exists (local JSON cache feature) but is NOT yet in production — needs dedicated testing. v14 is built from v12 + chart fixes and is the current production script. Do NOT use v13 for client runs until explicitly promoted.

---

## NEW SESSION STARTUP — DO THIS FIRST, EVERY TIME

Before writing any code or answering any question, read these files in order:

1. `memory/project_femr_status.md` — current script version, run status, pending items
2. `memory/project_data_issues.md` — known data issues (don't re-investigate these)
3. `memory/project_people.md` — who Josh/Shoma/Taylor are and what they own
4. `docs/client_communications_log.md` — all email/meeting history with clients
5. `NOTES.md` — QA checklist, lessons learned, pre/post-run verification rules
6. Check Known Blockers section below before doing anything

Do not rely on memory or prior session summaries alone. Read the actual files.
The files are the source of truth. Summaries can be wrong or incomplete.

---

## THE CARDINAL RULES

### 1. Never Assume — Verify Everything
- **Never assume a feature works because it was written.** Run a test that would catch it if it were broken.
- **Never assume a data issue is a script bug** without checking `project_data_issues.md` first.
- **Never assume the GROUP MAPPING file hasn't changed.** Re-read it when starting a new run.
- **Never assume a previous session's context is complete.** Read the files above.
- **Never assume a log saying "Done" means the output is correct.** Open the Excel file and verify.
- When unsure about any API field, data value, or client decision — find the documented source. If no source exists, note it as unknown and flag it, don't invent an answer.

### 2. Client Communications — Save Immediately
- **Any email or message shared in the chat must be saved to `docs/client_communications_log.md` immediately.**
  Do not summarize — paste key quotes and decisions verbatim. Conversation context is lost when compacted.
- After saving, update the Thread Index table at the top of that file.
- Also update `memory/project_femr_status.md` and `memory/project_data_issues.md` if the email contains new decisions or data issues.

### 3. Feature Verification — Mandatory Before Marking Any Task Complete
- Every feature must have a specific test that **would fail if the feature were broken**.
- Run that test. Check the actual output file — not just the log.
- **File splitting:** run `--group WFD --split-size 5`, count output files, verify naming pattern.
- **Currency format:** open file, check Available Funds row (row 29) shows `$` format.
- **Chart:** open file, click chart — check legend position, colors, no axis titles.
- **Multi-identifier:** run `--sequence 2ADP099`, verify 2 tabs are produced.
- **Tab counts:** after any full group run, count tabs against expected. See NOTES.md.
- **Never mark a task complete because "the code looks right."** Verify the actual output.

### 4. Memory and Task List — Keep Current
- After any session where decisions are made, data issues are found, or client feedback arrives:
  update `memory/project_femr_status.md`, `memory/project_data_issues.md`.
- Keep the task list (TaskCreate/TaskUpdate) current. Mark tasks complete immediately when done.
- When a data issue is confirmed as a data problem (not a script bug): mark the task complete,
  document the finding in `project_data_issues.md`, so we don't re-investigate next session.

### 5. Script Versioning
- Never edit a working version in place. Copy to `_12.py`, `_13.py`, etc. for each change.
- The current active script is always the highest-numbered file in `scripts/`.
- Update the module docstring with a "Changes from vN-1" section and update the version string.
- Run the full pre-run checklist in `NOTES.md` before promoting any new version.

### 6. Data Source of Truth
- Sequence-to-group mapping: `docs/Re_ FEMR /GROUP MAPPING.xlsx` SEQUENCE sheet
- Template layout: `docs/Re_ FEMR /FEMR Export Template 041526.xlsx`
- Never hardcode sequence overrides — wait for Taylor to update GROUP MAPPING.xlsx
- Never override client decisions without written confirmation from Josh or Shoma.

---

## Known Blockers (check before each run)

| Issue | Status | Action |
|-------|--------|--------|
| EWD014 group | **RESOLVED** — moved to WFD in GROUP MAPPING, WFD re-run done (28 tabs) | Done |
| OGA047 missing | **RESOLVED** — added to GROUP MAPPING, OGA re-run done (47 tabs) | Done |
| 2ADP099 R1099 | Invalid per Taylor | Will be cleaned up in NetSuite — not a script bug |
| Pre-FY2020 cumulative | **IMPLEMENTED in v12+** — fetches FY2016-2019, seeds Q1 FY20 | Done |
| CC007 R960011 tab | **RESOLVED** — Josh confirmed 960011 is now child of rollup 4006. 1 tab correct. | Done |
| Chart legend overlap | **FIXING IN v14** — legend → right, x-axis stays bottom when Y negative | In progress |
| ADP 151-200 incomplete | Died mid-run (132K file). ADP 201-246 missing. | Re-run needed with v14 |

---

## Client Contacts

| Person | Role | What they handle |
|--------|------|-----------------|
| Josh Grapani | Tech lead | Data fields, template layout, API questions, report logic |
| Shoma Sinha | PM | Business decisions, scope, what to include/exclude |
| Taylor Bui | NetSuite admin | Rollup/orphan/sequence data quality in NetSuite |

---

## Python Environment

Always use `venv/shoma/bin/python` — never system Python.

---

## Run Commands (v14 — current)

```bash
# Single sequence test (always run first before a group run)
venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py --sequence 2ADP001 -o test_v14_2ADP001.xlsx --skip-preload

# Single group
venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py --group WFD -o femr_v14 --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py --group Internal -o femr_v14 --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py --group Comml -o femr_v14 --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py --group OGA -o femr_v14 --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py --group ADP -o femr_v14 --workers 40

# All groups overnight
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_14.py -o femr_v14 --workers 40 > /tmp/v14_full.log 2>&1 &

# Monitor a background run
tail -f /tmp/v14_full.log
ps aux | grep femr_netsuite_report | grep -v grep
```

---

## API Reference

- Base URL: `https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user`
- `/femr/netamount/` — fast, single-identifier sequences only (silently ignores rollup filter param)
- `/mv_femr_report/` — full MV (~2M rows), use for multi-identifier sequences and all metadata

---

## Expected Tab Counts (verify after every run)

| Group | Expected tabs | Files | Notes |
|-------|--------------|-------|-------|
| WFD | 28 | 1 | EWD014 now included (mapping fixed 2026-04-24) |
| Internal | 37 | 1 | |
| Comml | ~42 | 1 | CC007 = 1 tab now (R960011 gone — confirm with Josh) |
| OGA | 47 | 1 | OGA047 now included (mapping fixed 2026-04-24) |
| ADP | ~246 | 5 | 001-050, 051-100, 101-150, 151-200, 201-246 |

If tab count is off by more than 2, investigate before sending to client.

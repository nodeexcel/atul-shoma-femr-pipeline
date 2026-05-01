# FEMR Export Script — Setup & Run Guide

**Client:** NextFlex  
**Prepared by:** Daden.dev (Atul Kumar)  
**Script:** `femr_netsuite_report_16.py`  
**Date:** April 2026  

---

## What the Script Does

Connects to the Oracle APEX API, pulls financial data for all project sequences, and generates multi-tab Excel workbooks — one tab per sequence — grouped by reporting type (WFD, Internal, Comml, OGA, ADP).

Each output Excel file contains:
- Project header (name, group, rollup number, contacts)
- Quarterly financial data from FY2020 to current quarter
- Cumulative totals seeded from FY2016 historical data
- Line chart with five financial metrics

---

## Prerequisites

- **Python 3.10 or higher** — download from [python.org](https://www.python.org/downloads/)
- **Internet access** to reach the Oracle APEX API
- **Oracle API credentials** — client ID and secret (obtain from Josh Grapani)
- **Windows, Mac, or Linux** — the script runs on all platforms

To check your Python version:
```bash
python --version
```

---

## Setup (One-Time)

### 1. Get the files

Copy the project folder onto your machine. You need at minimum:

```
femr-pipeline/
├── scripts/
│   └── femr_netsuite_report_16.py
├── docs/
│   └── Re_ FEMR /
│       └── GROUP MAPPING.xlsx        ← do not move or rename
├── requirements_script.txt
└── .env                              ← you will create this in step 3
```

### 2. Create a virtual environment

Open a terminal (Command Prompt or PowerShell on Windows, Terminal on Mac/Linux) and navigate to the project folder:

```bash
cd femr-pipeline
```

Create the virtual environment:
```bash
python -m venv venv
```

Activate it:
```bash
# Mac / Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your terminal prompt.

### 3. Install dependencies

```bash
pip install -r requirements_script.txt
```

This installs all required Python packages. Only needed once (or after a Python update).

### 4. Set up API credentials

The Oracle APEX API requires authentication. You need a client ID and secret from Josh Grapani (NextFlex tech lead).

Create a file named `.env` in the `femr-pipeline/` folder with the following contents:

```ini
ORACLE_CLIENT_ID=your-client-id-here
ORACLE_SECRET_KEY=your-secret-key-here
```

Replace the placeholder values with the actual credentials Josh provides.

> **Keep this file private.** Do not share it or commit it to version control.

---

## Running the Script

### Step 1 — Activate the virtual environment

```bash
# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

### Step 2 — Load credentials

```bash
# Mac / Linux
set -a && source .env && set +a

# Windows (Command Prompt) — set each variable manually
set ORACLE_CLIENT_ID=your-client-id-here
set ORACLE_SECRET_KEY=your-secret-key-here
```

### Step 3 — Run a single group

```bash
# WFD group
python -u scripts/femr_netsuite_report_16.py --group WFD -o femr_v16 --workers 40

# Internal group
python -u scripts/femr_netsuite_report_16.py --group Internal -o femr_v16 --workers 40

# Commercial group
python -u scripts/femr_netsuite_report_16.py --group Comml -o femr_v16 --workers 40

# OGA group
python -u scripts/femr_netsuite_report_16.py --group OGA -o femr_v16 --workers 40

# ADP group
python -u scripts/femr_netsuite_report_16.py --group ADP -o femr_v16 --workers 40
```

### Run all groups at once (overnight)

**Mac / Linux:**
```bash
nohup bash -c 'set -a && source .env && set +a && python -u scripts/femr_netsuite_report_16.py -o femr_v16 --workers 40' > femr_run.log 2>&1 &
echo "Running in background. Check femr_run.log for progress."
```

**Windows (run in a terminal you can leave open):**
```bash
python -u scripts/femr_netsuite_report_16.py -o femr_v16 --workers 40
```

### Test with a single sequence (recommended before a full run)

```bash
python -u scripts/femr_netsuite_report_16.py --sequence 2ADP001 -o test_output.xlsx --skip-preload
```

Open `test_output.xlsx` and verify: one tab named `2ADP001`, data present, chart visible.

---

## Monitoring Progress

The script prints progress to the terminal as it runs:

```
12:35:47 INFO === FEMR NetSuite Report Generator (v16) ===
12:35:48 INFO OAuth token (re)fetched — valid for 3600s
12:35:49 INFO [1/28] EWD014 (WFD)
12:35:49 INFO   [single-id] EWD014 → tab EWD014
12:38:17 INFO [2/28] EWD001 (WFD)
...
12:41:33 INFO Saved femr_v16_wfd.xlsx (total tabs: 28)
Done! 28 total tabs across 1 files.
```

The `OAuth token (re)fetched` line confirms credentials are working. If you see an error about missing credentials instead, check your `.env` file.

For background runs (Mac/Linux), monitor progress:
```bash
tail -f femr_run.log
```

---

## Output Files

Files are saved in the folder where you run the script:

| Group | File(s) | Tabs | Approx. time |
|-------|---------|------|-------------|
| WFD | `femr_v16_wfd.xlsx` | 28 | ~2 hours |
| Internal | `femr_v16_internal.xlsx` | 37 | ~2.5 hours |
| Comml | `femr_v16_comml.xlsx` | 41 | ~3 hours |
| OGA | `femr_v16_oga.xlsx` | 47 | ~3.5 hours |
| ADP | `femr_v16_adp_001-050.xlsx` | 50 | ~8–9 hours total |
| ADP | `femr_v16_adp_051-100.xlsx` | 50 | (all 5 files together) |
| ADP | `femr_v16_adp_101-150.xlsx` | 50 | |
| ADP | `femr_v16_adp_151-200.xlsx` | 50 | |
| ADP | `femr_v16_adp_201-246.xlsx` | 46 | |

> **Note:** ADP is split into 5 files of ~50 tabs each. Download all 5.

---

## Updating the Group Mapping

When Taylor Bui (NetSuite admin) adds or changes project sequences:

1. Replace `docs/Re_ FEMR /GROUP MAPPING.xlsx` with the updated file.
2. Re-run the affected group(s).

Do not rename or move this file — the script reads it automatically.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `RuntimeError: ORACLE_CLIENT_ID and ORACLE_SECRET_KEY must be set` | Credentials not loaded — run `set -a && source .env && set +a` before running the script |
| `HTTP Error 401: Unauthorized` | Credentials are wrong or expired — check `.env` values with Josh |
| `ModuleNotFoundError` | Virtual environment not activated — run `source venv/bin/activate` first |
| `python: command not found` | Use `python3` instead of `python` on some Mac/Linux systems |
| Script stops mid-run with network error | Re-run the same group — the script restarts from the beginning of the group |
| Output file has fewer tabs than expected | A sequence had a transient API error — re-run the group |
| `GROUP MAPPING.xlsx` not found | Make sure you are running the script from the `femr-pipeline/` folder, not from inside `scripts/` |
| Tab opens but all values are zero | Transient API failure — re-run the group |

---

## Command Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--group` | Which group to run | `--group WFD` |
| `-o` | Output file prefix | `-o femr_v16` |
| `--workers` | Parallel API threads (default 40) | `--workers 40` |
| `--sequence` | Run a single sequence only | `--sequence 2ADP001` |
| `--skip-preload` | Skip bulk metadata load (use with `--sequence`) | `--skip-preload` |

---


# FEMR NetSuite Report — Full Project Handoff Document

**Project:** FEMR NetSuite Multi-Tab Excel Report Generator
**Client:** NextFlex (Shoma Sinha)
**Developer:** Atul Kumar
**Date:** April 14, 2026
**Status:** Phase 1 Complete — CA2 ADP tabs generated, pending client review and open questions

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Background & Discovery](#2-background--discovery)
3. [Data Source — Oracle APEX API](#3-data-source--oracle-apex-api)
4. [MV_FEMR_REPORT Materialized View](#4-mv_femr_report-materialized-view)
5. [ADP Registry — All 224 Sequences](#5-adp-registry--all-224-sequences)
6. [Excel Output Structure](#6-excel-output-structure)
7. [Script Architecture](#7-script-architecture)
8. [Output Files](#8-output-files)
9. [Existing Repo — FEMR Funds Transform](#9-existing-repo--femr-funds-transform)
10. [Open Questions for Josh](#10-open-questions-for-josh)
11. [Known Gaps & Missing Data](#11-known-gaps--missing-data)
12. [Running the Script](#12-running-the-script)
13. [Verification Checklist](#13-verification-checklist)

---

## 1. Project Overview

NextFlex runs a **FEMR (Flexible Electronics Manufacturing Readiness) report** that tracks financial data for all ADP (Advanced Development Project) contracts. The report currently lives in NSCW (NetSuite Analytics Workbook) but has a limitation: NSCW cannot export to multiple Excel tabs natively.

**Goal:** Build a Python ETL script that:
- Pulls financial data from the Oracle APEX REST API (backed by NetSuite)
- Generates a multi-tab `.xlsx` workbook — one tab per ADP project
- Matches the exact layout of the `FEMR_for_NetSuite.xlsx` template provided by the client
- Splits output into multiple files, max 50 ADP tabs per file

**Two separate pipelines exist in this project:**

| Pipeline | Input | Output | Status |
|---|---|---|---|
| FEMR Funds Transform | FEMR Funds `.xlsx` (wide format) | Long-format Output tab (for Power BI/Tableau) | ✅ Complete (Django web app) |
| FEMR NetSuite Report | Oracle APEX REST API | Multi-tab `.xlsx` (one tab per ADP) | ✅ Phase 1 complete |

---

## 2. Background & Discovery

### Loom Call Transcripts Summary

Three calls were analyzed:
- **Call 1:** Initial data review — Atul learning the data flow, where data comes from, what the expected output looks like
- **Call 2:** Understanding input vs output — confirmed the report needs to be exported to Excel with ~50 tabs
- **Call 3:** Josh explaining the FEMR report structure — built from a SQL/materialized view in NetSuite, four visualizations (info table, people table, quarterly cumulative budget vs actuals, chart)

### Key Business Context
- Fiscal year starts **October 1** (e.g. FY2020 = Oct 2019 – Sep 2020)
- Quarter definitions: Q1=Oct–Dec, Q2=Jan–Mar, Q3=Apr–Jun, Q4=Jul–Sep
- Projects are filtered to: **Type A = CA1 or CA2** AND **Type B contains "ADP"**
- Historical data starts from **10/01/2019** (FY2020)
- `FEMR_for_NetSuite.xlsx` was provided as the exact output template

### Reference Files
- `FEMR_for_NetSuite.xlsx` — output template (sheets: New report, ADP 62, ADP 33, ADP 116, Sheet1-4, Lists)
- `2026.03 FEMR funds.xlsx` — input file for the existing FEMR Funds Transform pipeline
- GitHub repo: `nodeexcel/atul-shoma-femr-pipeline` (existing Django transform app)

---

## 3. Data Source — Oracle APEX API

### Base URL
```
https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user
```

### Confirmed Endpoints

#### `/femr/netamount/` — Primary data endpoint
Returns a single aggregated value per combination of parameters.

**Query parameters (all required):**
| Parameter | Example | Notes |
|---|---|---|
| `display_sequence` | `2ADP001` | ADP sequence identifier |
| `fiscal_year_end` | `FYE 9/30/2020` | Must use exact format with space |
| `fiscal_quarter` | `Q4` | Q1, Q2, Q3, or Q4 |
| `segment` | `ACTUALS` | ACTUALS, BUDGETED, or CONTRACTING |
| `account_name` | `5001 DIR : Direct Labor` | Must use exact string — see account list below |

**Response format:**
```json
{
  "items": [{"total_netamount": 26427.52}],
  "hasMore": false,
  "count": 1
}
```

**Example calls:**
```bash
# Actuals
curl "https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user/femr/netamount/?display_sequence=2ADP001&fiscal_year_end=FYE%209/30/2020&fiscal_quarter=Q4&segment=ACTUALS&account_name=5001%20DIR%20:%20Direct%20Labor"

# Budgeted
curl "...&segment=BUDGETED&account_name=5001%20DIR%20:%20Direct%20Labor"

# Contracting
curl "...&segment=CONTRACTING&account_name=Committed"
```

**Verified test values:**
- `2ADP001` + `FYE 9/30/2020` + `Q4` + `CONTRACTING` + `Committed` = **27,100,000** ✅
- `2ADP001` + `FYE 9/30/2020` + `Q4` + `ACTUALS` + `5001 DIR : Direct Labor` = **26,427.52** ✅
- `2ADP001` + `FYE 9/30/2020` + `Q4` + `BUDGETED` + `5001 DIR : Direct Labor` = **123,790.60** ✅

#### `/mv_femr_report/` — Raw materialized view
Full dataset, ~2,070,000 rows. Too large to paginate per run (~100 min). Used only for discovery.

#### `/open-api-catalog/femr/` — OpenAPI spec
```bash
curl "https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user/open-api-catalog/femr/"
```

### Confirmed Account Name Strings

These are the **exact strings** to use in the `account_name` parameter:

**ACTUALS & BUDGETED segments:**
| Row Label | API Account Name |
|---|---|
| Labor Hours statistical account | `null` (no API data) |
| Labor Cost 5001 | `5001 DIR : Direct Labor` |
| Fringe 5990 | `5990 ALLO : Allo Fringe` |
| Travel 5004 | `5004 DIR : Direct Travel` |
| Subcontracting 5005 | `5005 DIR : Subrecipient Costs` |
| Consulting 5002 | `5002 DIR : Direct Consulting` |
| Equipment 5010 | `5010 DIR : EQ & Materials (NO OH)` |
| Equipment 5008 | `5008 DIR : Direct Equipment` |
| Other Direct Costs 5009 | `5009 DIR : Direct Other Costs` |
| Material 5003 | `5003 DIR : Direct Materials` |
| Sub K Overhead 5992 | `5992 ALLO : Allo SubK OH` |
| Sub K Overhead 5993 | `5993 ALLO : DNU ALLO G and A OH WFD` |
| G&A 5991 | `5991 ALLO : Allo G and A` |

**CONTRACTING segment:**
| Row Label | API Account Name |
|---|---|
| Committed | `Committed` |
| Obligated | `Obligated` |
| Expended | `Expended` |

### Confirmed Fiscal Year Range
`FYE 9/30/2018` through `FYE 9/30/2025` (8 fiscal years × 4 quarters = 32 time periods)

---

## 4. MV_FEMR_REPORT Materialized View

### Key Fields Discovered
```json
{
  "display_sequence": "2ADP001",
  "display_adp": 1,
  "display_project_legalname": "CA2 ADP1 ESI Laser",
  "display_project_shortname": "CA2 ADP1 ESI Laser",
  "display_type_b": "ADP-Tech, ADP-Tech Subk",
  "display_type_c": "Other DOD",
  "display_rollup_num": "1001",
  "display_acrn": null,
  "display_outside_approver_1": null,
  "fiscal_year_end": "FYE 9/30/2020",
  "fiscal_quarter": "Q1",
  "quarter_fy": "Q1 FY20",
  "account_name": "5001 DIR : Direct Labor",
  "account_number": "5001",
  "segment": "ACTUALS",
  "metric": "Budgeted Plan",
  "metric_quarter_amount": 0,
  "netamount": 0
}
```

### Why We Don't Use the MV Directly
- ~2,070,000 rows total (~207 pages × 10,000 rows)
- Takes ~100 minutes to paginate fully
- `netamount` API endpoint returns pre-aggregated values, making per-row MV reads unnecessary
- MV was used only for initial discovery of sequences and account names

---

## 5. ADP Registry — All 224 Sequences

Discovered by striding through the MV at offset intervals of 2,000.

### Summary
| Category | Count |
|---|---|
| CA1 ADP sequences | 61 (1ADP001–1ADP061, with 1ADP033 missing) |
| CA1 PC sequences | 54 (1PC001–1PC054) |
| CA2 ADP sequences | 110 (2ADP001–2ADP114, with gaps) |
| **Total** | **224** |

### CA2 ADP Sequences (used for current report)
```
2ADP001  CA2 ADP1 ESI Laser                    rollup: 1001
2ADP002  CA2 ADP2 BMNT NSIN                    rollup: 1002
2ADP003  CA2 ADP3 Reliability Ph1              rollup: 1003
2ADP004  CA2 ADP4 DPiX Flex xray               rollup: 1004
2ADP005  CA2 ADP5                               rollup: None
2ADP006  CA2 ADP6 CCDC AC2 nd SubKs            rollup: 1006
2ADP007  CA2 ADP7                               rollup: None
2ADP008  CA2 ADP8 BMNT Collab                  rollup: 1008
2ADP009  CA2 ADP9 Palo Alto Research Center    rollup: 1009
2ADP010  CA2 ADP10                              rollup: None
2ADP011  CA2 ADP11 WFD Project                 rollup: 1011
2ADP012–2ADP031  (various, some with rollups)
2ADP033  CA2 ADP33 WFD Training               rollup: 1033
2ADP034–2ADP072  (various)
2ADP073–2ADP114  (various, with gaps at 105, 108, 111)
```

### Missing CA2 ADP Numbers (gaps)
`2ADP032`, `2ADP105`, `2ADP108`, `2ADP111` — these do not exist in the MV

---

## 6. Excel Output Structure

### Tab Layout (per ADP, matches template exactly)

```
Row 1      : NextFlex
Row 2      : ADP | {number} | Rollup (col C, if applicable)
Row 3      : Project Name | {value}
Row 4      : Type B | {value}
Row 5      : Type C | {value}
Row 6      : Color of Money | (blank — not in API)
Row 7      : ACRNs | {rollup number}
Row 8      : (blank)
Row 9      : (blank) | (blank) | FYE 9/30/2018 [merged x4] | FYE 9/30/2019 [merged x4] | ...
Row 10     : (blank) | (blank) | Q1 | Q2 | Q3 | Q4 | Q1 | Q2 | Q3 | Q4 | ...
Row 11–24  : ACTUALS section (A11:A24 merged = "Actuals")
             Col B = account name, Col C onwards = quarterly data
Row 25–38  : BUDGETED section (A25:A38 merged = "Budgeted")
Row 39–41  : CONTRACTING section (A39:A41 merged = "Contracting", yellow fill)
             Committed / Obligated / Expended
Row 42     : (blank)
Row 43     : (blank) | govt awards
Row 44     : (blank) | govt obligated
Row 45     : (blank) | cash collected
Row 46     : add calc field | remaining cash
Row 47     : (blank)
Row 48     : formulas | (blank) | Q1 FY18 | Q2 FY18 | ... | Q4 FY25
Row 49     : (blank) | Total Committed   | =C39 | =D39 | ...
Row 50     : (blank) | Total Obligated   | =C40 | =D40 | ...
Row 51     : (blank) | Total Expended    | =C41 | =D41 | ...
Row 52     : (blank) | Budgeted Plan     | =C38 | =D38 | ...
Row 53     : (blank) | Revised Plan      | (blank — source TBD)
Row 54     : (blank) | Actual            | =C24 | =D24 | ...
Row 59     : source: bible
Row 60     : source: project bud vs actual
Row 61     : source: SF270 needs to be put NSAW
```

### Column Layout
- **Col A**: Section sidebar labels (merged)
- **Col B**: Account row labels
- **Col C onwards**: Quarterly data (C=Q1 FY18, D=Q2 FY18, ..., 32 data columns + Total)

### Formatting
- Contracting sidebar: Yellow fill (`F4F169`)
- Merged cells: A11:A24 (Actuals), A25:A38 (Budgeted), A39:A41 (Contracting)
- FYE headers: merged across 4 quarter columns each
- Numbers: `#,##0.00` format with dollar sign

---

## 7. Script Architecture

### File: `scripts/femr_netsuite_report.py`

```
run()
  └── _chunk_sequences_by_adp_range()   # split sequences into 50-ADP range files
      └── for each chunk:
          └── for each sequence:
              └── fetch_sequence_data()  # concurrent API calls via ThreadPoolExecutor
                  └── _fetch_netamount() # single API call with retry logic
              └── build_adp_sheet()      # write one Excel tab
                  ├── header block (rows 1-7)
                  ├── _write_col_headers() (rows 9-10)
                  ├── actuals section (rows 11-24) with merged A sidebar
                  ├── budgeted section (rows 25-38) with merged A sidebar
                  ├── contracting section (rows 39-41) with merged A sidebar
                  ├── govt awards rows (43-46)
                  ├── _write_formulas_section() (rows 48-54)
                  └── source notes (rows 59-61)
          └── wb.save(chunk_filename)
```

### Key Constants
```python
FISCAL_YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
CHUNK_SIZE = 50  # max ADP range per output file
WORKERS = 20     # concurrent API threads per sequence
```

### API Call Volume
- Per sequence: 864 API calls
  - 8 FYEs × 4 quarters × 12 accounts × 2 segments (ACTUALS + BUDGETED) = 768
  - 8 FYEs × 4 quarters × 3 contracting accounts = 96
- CA2 only (110 sequences): ~95,040 total calls
- Runtime: ~82 seconds per sequence at 30 workers = ~2.5 hours for CA2

### File Splitting Logic
Sequences are split by ADP number range, not by count:
- File 1: ADP numbers 1–50 (whatever exists in that range)
- File 2: ADP numbers 51–100
- File 3: ADP numbers 101–150
- Missing ADP numbers simply skip — no empty tabs

Output filenames: `femr_ca2_report_adp001-050.xlsx`, `femr_ca2_report_adp051-100.xlsx`, etc.

### Dependencies
```
openpyxl==3.1.5   # Excel writing
Python 3.13       # concurrent.futures, urllib (stdlib only — no requests needed)
```

---

## 8. Output Files

### Current CA2 Report (generated April 12, 2026)
| File | Tabs | ADP Range |
|---|---|---|
| `femr_ca2_report_adp001-050.xlsx` | 49 tabs | ADP 1–50 (ADP 32 missing) |
| `femr_ca2_report_adp051-100.xlsx` | 50 tabs | ADP 51–100 |
| `femr_ca2_report_adp101-150.xlsx` | 11 tabs | ADP 101–114 (gaps: 105, 108, 111) |

### Data Present in Each Tab
- ✅ Actuals — real transaction data per GL account per quarter
- ✅ Budgeted — budget plan figures per GL account per quarter
- ✅ Contracting — Committed, Obligated, Expended per quarter
- ✅ Summary formulas — Total Committed, Obligated, Expended, Budgeted Plan, Actual
- ⬜ Labor Hours — always 0 (statistical account, needs separate Oracle setup)
- ⬜ Color of Money — blank (not available in netamount API)
- ⬜ Revised Plan — blank (source not yet confirmed by Josh)
- ⬜ govt awards / obligated / cash collected / remaining cash — blank (needs "bible" source file)

### Note on Formula Cells
The formulas section (rows 49–54) uses Excel cell references (e.g. `=C39`). These display correctly in Excel. In Google Sheets, go to **File → Spreadsheet settings → Calculation → On change** to force recalculation.

---

## 9. Existing Repo — FEMR Funds Transform

**Repo:** `nodeexcel/atul-shoma-femr-pipeline` (GitHub)

This is a **separate, completed pipeline** — a Django web application:

### What it does
Reads the `FEMR Funds` sheet from an uploaded `.xlsx` workbook and reshapes it into a long-format `Output` sheet with one row per `(Sequence, Quarter, Type)`.

### Stack
- Django 6.0.3 + Gunicorn + Whitenoise
- openpyxl for Excel processing
- Docker + docker-compose for deployment
- SQLite database for job tracking

### Running locally
```bash
cp .env.example .env
cd src
python manage.py migrate
python manage.py runserver
# Open http://localhost:8000
```

### Running with Docker
```bash
docker compose up                              # development
docker compose -f docker-compose.prod.yml up  # production
```

### CLI script (standalone)
```bash
python scripts/femr_transform.py \
  --input files/2026.03_FEMR_funds.xlsx \
  --output files/output.xlsx
```

### URL Reference
| URL | Name | Description |
|---|---|---|
| `/` | `transform:upload` | Upload form + recent jobs |
| `/jobs/<pk>/` | `transform:job_detail` | Job status and result |
| `/jobs/<pk>/download/` | `transform:download` | Download output file |

---

## 10. Open Questions for Josh

These need answers before the report can be considered fully complete:

1. **Date range** — Should the report start from FY2020 (10/01/2019) only, or include FY2018 and FY2019 historical data as well?

2. **Scope** — Should the report include only ADP sequences (CA1 + CA2), or PC sequences as well?

3. **Revised Plan** — The template has a "Revised Plan" row in the formulas section. Is this a separate segment available in the API, or does it come from another source?

4. **Account 5993** — This is flagged as "Do Not Use" (DNU) in NetSuite. Should it still appear as a row in the report (just with zero values), or be excluded?

5. **Other data sources** — The template notes say "we need to import sheets as well, not just NS." Is there another file or system (the "bible" file?) we need to pull govt awards / cash collected data from?

6. **Contracting data for CA1** — Do CA1 projects have Committed/Obligated/Expended figures in the API, or is Contracting data only for CA2?

---

## 11. Known Gaps & Missing Data

| Field | Status | Reason |
|---|---|---|
| Labor Hours | Always 0 | Statistical account — needs separate Oracle setup per template note |
| Color of Money | Blank | Not returned by netamount API |
| Revised Plan | Blank | Source not confirmed by Josh |
| govt awards | Blank | Needs "bible" source file (separate from NetSuite) |
| govt obligated | Blank | Same as above |
| cash collected | Blank | Same as above |
| remaining cash | Blank | Calculated field (Obligated − Expended) — needs govt data first |
| Chart (rows 58+) | Not generated | Template has a scatter plot — needs Josh to clarify data source |

---

## 12. Running the Script

### Installation
```bash
pip install openpyxl
# No other dependencies — uses Python stdlib urllib for HTTP
```

### Commands

```bash
# Test single ADP (fast, ~2 min)
python3 scripts/femr_netsuite_report.py --sequence 2ADP001 --output test.xlsx

# CA2 only — generates 3 split files (~2.5 hours)
python3 scripts/femr_netsuite_report.py --ca2-only --workers 30 --output femr_ca2_report.xlsx

# All 224 sequences — generates multiple split files (~8+ hours)
python3 scripts/femr_netsuite_report.py --workers 30 --output femr_full_report.xlsx

# Tune workers for speed vs API load
python3 scripts/femr_netsuite_report.py --ca2-only --workers 50 --output femr_ca2_report.xlsx
```

### CLI Arguments
| Argument | Default | Description |
|---|---|---|
| `--output` / `-o` | `femr_netsuite_report.xlsx` | Base output filename (range suffix added automatically) |
| `--sequence` / `-s` | None | Single ADP sequence for testing (e.g. `2ADP001`) |
| `--ca2-only` | False | Only generate CA2 ADP tabs |
| `--workers` / `-w` | 20 | Concurrent API threads per sequence |
| `--chunk-size` / `-c` | 50 | ADP number range per output file |

### Output File Naming
Running with `--output femr_ca2_report.xlsx` produces:
```
femr_ca2_report_adp001-050.xlsx
femr_ca2_report_adp051-100.xlsx
femr_ca2_report_adp101-150.xlsx
```

### Checkpoints
The script saves the current workbook every 10 tabs. If interrupted, restart — it will regenerate that file's tabs from scratch (no partial resume yet).

---

## 13. Verification Checklist

After each run, verify these known values:

| ADP | FYE | Quarter | Segment | Account | Expected Value |
|---|---|---|---|---|---|
| 2ADP001 | FYE 9/30/2020 | Q4 | CONTRACTING | Committed | 27,100,000 |
| 2ADP001 | FYE 9/30/2020 | Q4 | CONTRACTING | Obligated | 27,100,000 |
| 2ADP001 | FYE 9/30/2020 | Q4 | ACTUALS | 5001 DIR : Direct Labor | 26,427.52 |
| 2ADP001 | FYE 9/30/2020 | Q4 | BUDGETED | 5001 DIR : Direct Labor | 123,790.60 |

Quick curl test:
```bash
curl "https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user/femr/netamount/?display_sequence=2ADP001&fiscal_year_end=FYE%209/30/2020&fiscal_quarter=Q4&segment=CONTRACTING&account_name=Committed"
# Expected: {"items":[{"total_netamount":27100000}],...}
```

---

## Appendix — Template Notes (from New Report sheet)

From the `FEMR_for_NetSuite.xlsx` "New report" tab (Atul's working notes):

```
1. Filter: Project Type A = CA1 and CA2, Type B contains "ADP"
2. Date range: Starting from 10/01/2019
3. Historical: FY ended 09/2020
4. Q1=Oct-Dec, Q2=Jan-Mar, Q3=Apr-Jun, Q4=Jul-Sep
5. Account 5993 is DNU in NetSuite
6. "We need to import sheets as well; not just NS?"
7. "What is Revised Plan?"
```

Source notes found in template:
- `source: bible` — govt awards data comes from a "bible" file
- `source: project bud vs actual` — budgeted figures source
- `source: SF270 needs to be put NSAW` — SF270 form data needs to be in NSAW

---

*Document generated: April 14, 2026*
*Next review: After Josh responds to open questions*

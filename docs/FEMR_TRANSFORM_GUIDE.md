# FEMR Funds Transformation Script — Setup & Run Guide

**Client:** NextFlex  
**Prepared by:** Daden.dev (Atul Kumar)  
**Script:** `femr_transform_2.py`  
**Date:** May 2026  

---

## What the Script Does

Takes a raw **FEMR Funds** Excel file and reshapes its data into a normalized long-format output, ready for use in Power BI, Tableau, or NSAW uploads.

**Input:** An `.xlsx` file with a `FEMR Funds` sheet containing quarterly financial data by sequence.

**Output:** A new file containing only the transformed data — either an Excel file with a single `Output` sheet, or a CSV file. The original input file is never modified. Output columns:

| Column | Description |
|--------|-------------|
| Sequence | Project sequence code (e.g. `2ADP001`) |
| Qtr Date | Quarter end date (e.g. `09/30/2020`) |
| Type | One of: `Committed`, `Obligated`, `Expended`, `Remaining Cash` |
| Amount | Dollar value for that sequence, quarter, and type |

For each quarter, the output contains four blocks of rows (one per type), covering every sequence in order. Quarters are discovered automatically from row 4 of the `FEMR Funds` sheet — no configuration needed.

---

## Prerequisites

- **Python 3.10 or higher** — download from [python.org](https://www.python.org/downloads/)
- **No internet access required** — runs entirely offline against the local Excel file
- **Windows, Mac, or Linux**

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
│   └── femr_transform_2.py
└── requirements_script.txt
```

### 2. Create a virtual environment

Open a terminal and navigate to the project folder:

```bash
cd femr-pipeline
```

Create and activate the virtual environment:
```bash
# Mac / Linux
python -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your terminal prompt.

### 3. Install dependencies

```bash
pip install -r requirements_script.txt
```

---

## Running the Script

### Always activate the virtual environment first

```bash
# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

### Run the transformation

The output filename is derived automatically from the input — you do not need to specify it. The output file is saved in the same folder as the input, prefixed with `output_`.

**Excel output (default):**
```bash
python -u scripts/femr_transform_2.py --input "2026_03_FEMR_funds.xlsx"
# Saves: output_2026_03_FEMR_funds.xlsx
```

**CSV output:**
```bash
python -u scripts/femr_transform_2.py --input "2026_03_FEMR_funds.xlsx" --format csv
# Saves: output_2026_03_FEMR_funds.csv
```

**Specifying an explicit output path (optional):**
```bash
python -u scripts/femr_transform_2.py --input "2026_03_FEMR_funds.xlsx" --output "my_output.xlsx"
```

The script prints progress as it runs:

```
Reading input file...
Parsing FEMR Funds input...
  Quarters discovered: 22
    06/30/2020  (col 10)
    09/30/2020  (col 13)
    ...
  Sequences: 134
  Expected output rows: 11792
Writing output file (excel)...
Saved: output_2026_03_FEMR_funds.xlsx
Total data rows written: 11792
```

### What to check in the output

**Excel:** Open the output file — it contains a single `Output` sheet (no original tabs):
- Column A: sequence codes (e.g. `2ADP001`)
- Column B: quarter end dates
- Column C: type — `Committed`, `Obligated`, `Expended`, or `Remaining Cash`
- Column D: dollar amounts
- Row count matches "Total data rows written" from the terminal

**CSV:** Open in Excel or a text editor — same four columns, one row per data point.

---

## Input File Requirements

The input Excel file must contain a sheet named exactly **`FEMR Funds`** (case-sensitive).

- **Row 4** must contain quarter labels in the format `QE M/D/YY` (e.g. `QE 6/30/20`, `QE 9/30/20`). The script reads these to discover all quarters automatically.
- **Rows 7 onward** contain sequence data. Column D must contain the sequence code.
- Annual total columns (e.g. `FY20 Total`, `Total`) are skipped automatically.

If the file also contains an **`Output`** sheet (from a previous run or template), the script uses its sequence order as a guide — sequences in the template appear first, any new sequences are appended at the end.

---

## Running via the Web App

The transformation is also available through the web application (no terminal required):

1. Navigate to `http://your-server-ip:8000/` (the home page)
2. Upload the FEMR Funds `.xlsx` file
3. Select output format: **Excel (.xlsx)** or **CSV (.csv)**
4. The app processes it and shows a result page
5. Click **Download** to get the output file

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Virtual environment not activated — run `source venv/bin/activate` first |
| `KeyError: 'FEMR Funds'` | Input file does not contain a sheet named `FEMR Funds` — check the exact sheet name |
| `python: command not found` | Use `python3` on some Mac/Linux systems |
| Output has 0 quarters | Row 4 of `FEMR Funds` does not have `QE M/D/YY` labels — check the input file format |
| Output has 0 sequences | No data found in rows 7–306 of `FEMR Funds` — check column D contains sequence codes |
| `Remaining Cash` is negative | Expected — it is calculated as `Obligated − Expended`, which can be negative |

---

## Command Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--input` | Path to the input FEMR Funds `.xlsx` file (required) | `--input FEMR_funds.xlsx` |
| `--format` | Output format: `excel` (default) or `csv` | `--format csv` |
| `--output` | Output file path (optional — auto-derived if omitted) | `--output my_output.xlsx` |

---

# FEMR Funds Transformation Script — Setup & Run Guide

**Client:** NextFlex  
**Prepared by:** Daden.dev (Atul Kumar)  
**Script:** `femr_transform.py`  
**Date:** April 2026  

---

## What the Script Does

Takes a raw **FEMR Funds** Excel file and reshapes its data into a normalized long-format **Output** sheet, ready for use in Power BI, Tableau, or NSAW uploads.

**Input:** An `.xlsx` file with a `FEMR Funds` sheet containing quarterly financial data by sequence.

**Output:** The same file saved with an updated `Output` sheet containing four columns:

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
│   └── femr_transform.py
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

```bash
python -u scripts/femr_transform.py --input path/to/FEMR_Funds.xlsx --output path/to/output.xlsx
```

**Example:**
```bash
python -u scripts/femr_transform.py --input "2026_03_FEMR_funds.xlsx" --output "2026_03_FEMR_funds_output.xlsx"
```

The script prints progress as it runs:

```
Reading input file...
Parsing FEMR Funds input...
  Quarters discovered: 24
    09/30/2020  (col 5)
    12/31/2020  (col 8)
    ...
  Sequences: 247
  Expected output rows: 23712
Writing output file...
Saved: 2026_03_FEMR_funds_output.xlsx
Total data rows written: 23712
```

### What to check in the output

Open the output file and verify the `Output` sheet:
- Column A: sequence codes (e.g. `2ADP001`)
- Column B: quarter end dates in `MM/DD/YYYY` format
- Column C: type — must be exactly `Committed`, `Obligated`, `Expended`, or `Remaining Cash`
- Column D: dollar amounts
- Row count should match "Total data rows written" from the terminal

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
3. The app processes it and shows a result page
4. Click **Download** to get the output file

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
| `--input` | Path to the input FEMR Funds `.xlsx` file | `--input FEMR_funds.xlsx` |
| `--output` | Path for the generated output `.xlsx` file | `--output output.xlsx` |

---

## Contact

For script issues:  
**Atul Kumar** — Developer

For data questions (input file format, sequence mapping):  
**Josh Grapani** — NextFlex Tech Lead  
**Shoma Sinha** — NextFlex PM

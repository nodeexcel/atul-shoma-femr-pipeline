# FEMR NetSuite Report — Meeting Summary (April 15, 2026)

**Attendees:** Atul Kumar, Josh Grapani
**Context:** Josh's answers to the 14 questions + new files (`GROUP MAPPING.xlsx`, `FEMR Export Template 041526.xlsx`)
**Outcome:** All blockers resolved. Ready to build script v5.

---

## 1. Answers to the 14 Questions

### Q1. Project Legal Name
**Answer:** Field is `display_project_legal_name` in the data source (API). **ALWAYS use this field** — regardless of whether the project is an orphan or a rollup. The earlier logic about "short name vs legal name" is outdated. The latest logic: **Project Name row = Project Legal Name, always.**

### Q2. Technical Point of Contact
**Answer:** Field is `display_technical_point_of_contact` in the API data source. Fetch along with legal name.

### Q3. ACRN
**Answer:** Field is `display_acrn` in the API data source. Fetch along with legal name.

### Q4. Available Funds
**Answer:** Field is `available_funds` in the API data source. Fetch directly from API. Example from sample files: most projects show `0`, but `EWD001` shows `-345,752` — so this IS a real live field, not always zero.

### Q5. Remaining Cash Formula
**Answer confirmed:** `Remaining Cash = Obligated − Expended` **per quarter** (not cumulative). Negative values are expected when expended exceeds obligated in a quarter.

### Q6. Dynamic Columns
**Answer:**
- Always show from **FYE 9/30/2020** up to the **latest quarter that has data**
- **Zero-value quarters are still shown** (if a quarter exists, display it — do not hide even if all values are 0)
- Currently data goes up to **Q2 FY2026** because that's what NSAW has
- As new postings come in (e.g., Q3 FY2026), new columns should appear automatically
- **Script must auto-extend** the quarter range — don't hardcode FY2026 as the endpoint

### Q7. Reporting Group — Type A
**Answer:** This is the **TOP-level** project classification, not CA1/CA2 distinction.

**The 5 reporting groups are:**
| Reporting Group | Type A Project Categories (sub-level, not shown on tab) |
|----------------|----------------------------------------------------------|
| **ADP** | CA1, CA2 (and future CA3) |
| **Comml** | Comml |
| **Internal** | Internal |
| **OGA** | OGA EWD Fedl, OGA EWD State, OGA Fedl |
| **WFD** | EWD |

**Critical:** For ALL sequences under ADP (1ADP, 2ADP, 1PC — yes, PC is under ADP!), the Reporting Group row value is `"ADP"`. Not "CA1", "CA2", or "PC".

**Script must be dynamic:** When CA3 is eventually added, it should automatically appear under ADP without code changes. This means **use the mapping file as the source of truth**, not hardcoded logic.

### Q8. Color of Money
**Answer:** **Leave blank for now.** Data is not in NetSuite yet. Row stays in template.

### Q9. Labor Hours
**Answer:** **Leave blank for now.** Statistical account not created yet. Row stays in template.

### Q10. Revised Plan
**Answer:** **Removed.** Do NOT include this row. Cumulative section is now 5 rows only (Total Committed, Total Obligated, Total Expended, Budgeted Plan, Actual).

### Q11. CA1 and PC Scope
**Answer:** **Include ALL reporting group types.** Generate tabs for every sequence in the mapping file:
- ADP (includes CA1 + CA2 + all PC sequences) — ~247 unique sequences
- Comml — ~41 unique sequences
- Internal — ~37 unique sequences
- OGA — ~48 unique sequences
- WFD — ~27 unique sequences
- **Total: ~400 unique sequences**

### Q12. Account 5993 (Do Not Use)
**Answer:** **Keep it.** Row stays in report even though it's DNU.

### Q13. Govt Awards / Bible File
**Answer:** **Dropped permanently.** Remove these rows:
- govt awards
- govt obligated
- cash collected
- remaining cash (the old one — NEW Remaining Cash is inside Contracting section)

### Q14. SF270 Data
**Answer:** Handled separately — it's part of the existing FEMR Funds Transform pipeline (the Django app). Not relevant to this script.

---

## 2. NEW Requirements from the Meeting

### A. Rollup as Identifier (IMPORTANT)
Some sequences have **multiple rollups** representing different projects that share the same sequence number. Example:
- `OGA001` exists twice — once with rollup `2001`, once with rollup `73001012`
- These are **different projects** and must produce **separate tabs**

**Implication for the script:**
- Change API call signature from `(sequence)` to `(sequence, rollup)`
- Add `display_rollup` as a parameter to `/femr/netamount/`
- Fetch data per **(sequence, rollup) pair**, not per sequence
- Generate one tab per unique (sequence, rollup) combination

**Why this changed:** Josh said NetSuite recently changed the sequence format, and now multiple projects can share a sequence number. Rollup is the only truly unique identifier.

### B. File Splitting Pattern
Same pattern as current CA2 output (50 ADPs per file):

| Reporting Group | Sequence Count | Files |
|-----------------|----------------|-------|
| ADP — CA2 | 110 | 3 files (001-050, 051-100, 101-150) |
| ADP — CA1 ADP | 61 | 2 files (001-050, 051-100) |
| ADP — CA1 PC | 54 | 1-2 files |
| Comml | 42 | 1 file |
| Internal | 37 | 1 file |
| OGA | 48 | 1 file |
| WFD | 27 | 1 file |

Josh: *"If there are new sequences added, they should be automatically included."* → Use mapping file dynamically, don't hardcode sequence lists.

### C. Project Name Correction
**IMPORTANT:** Josh corrected his earlier statement. The latest logic: **Project Name = Project Legal Name, always.** No more logic around "orphan vs rollup" — just use `display_project_legal_name`.

### D. Graph
**Confirmed needed.** Josh wants the line chart in every tab. Specs already captured from the template:
- LineChart with 5 series, circle markers
- Series names: "Funds Committed", "Obligated Funds", "Pre-Bill Expenditures", "Budgeted Spend", "Actual Expenditures"
- Data source: rows 52-56 (cumulative section)
- X-axis: row 51 (Q labels)
- Position: below cumulative data

---

## 3. Files Received from Josh

### `GROUP MAPPING.xlsx` — 2 sheets

**Sheet 1: GROUP MAPPING**
Lookup table of all valid (Reporting Group Type A → Type A Project Category → Type B Project Type) combinations. 36 rows total.

**Sheet 2: SEQUENCE**
Full list of **616 rows** with columns:
- `REPORTING_GROUP_TYPE_A`
- `TYPE_A_PROJECT_CATEGORY`
- `TYPE_B_PROJECT_TYPE`
- `SEQUENCE`

Note: 616 rows but only ~400 unique sequences because some sequences have multiple Type B values (shown as separate rows in this mapping file).

Counts:
- ADP: 435 rows / 247 unique sequences
- Comml: 42 rows / 41 unique sequences
- Internal: 37 rows / 37 unique sequences
- OGA: 70 rows / 48 unique sequences
- WFD: 32 rows / 27 unique sequences

**This file IS the source of truth** for what to generate. Replace the hardcoded `ADP_REGISTRY` in the script with this file.

### `FEMR Export Template 041526.xlsx` — 8 sample sheets

One example tab per reporting group / variation:
1. `2ADP001` — CA2 ADP example (full data)
2. `1ADP001` — CA1 ADP example
3. `1PC034` — CA1 PC example
4. `OGA001` — OGA example
5. `CC032` — Comml example
6. `COR001` — Internal example (no project name, no ACRN)
7. `NX009` — Internal example
8. `EWD001` — WFD example (has negative Available Funds: -345,752)

**All sheets use the same layout:**
- Header block rows 1-11
- Blank rows 12-14
- Row 15: FYE merged headers
- Row 16: Q1-Q4 headers
- Rows 17-29: Actuals section (Labor Hours at row 17)
- Row 30: ACTUALS Total
- Rows 31-43: Budgeted section
- Row 44: BUDGETED Total
- Rows 45-48: Contracting (Committed, Obligated, Expended, Remaining Cash)
- Rows 49-50: blank gap
- Row 51: Q labels (Q1 FY20 ...)
- Rows 52-56: Cumulative (Total Committed, Obligated, Expended, Budgeted Plan, Actual)
- Chart below (anchored rows 59-73 for the 2ADP001 sheet)

All 8 sheets have 1 chart each.

### Field mappings confirmed from samples

| Template Row | API/MV Field |
|--------------|--------------|
| REPORTING GROUP - TYPE A | From GROUP MAPPING file (lookup by sequence) |
| SEQUENCE | `display_sequence` |
| ROLLUP # | `display_rollup` |
| PROJECT NAME | `display_project_legal_name` |
| TECHNICAL POINT OF CONTACT | `display_technical_point_of_contact` |
| PROJECT TYPE | `display_type_b` (or from mapping file — multi-value support) |
| SERVICE | `display_type_c` |
| COLOR OF MONEY | Not available yet |
| ACRN | `display_acrn` |
| AVAILABLE FUNDS | `available_funds` |

---

## 4. Action Items

### For Atul (Developer)
1. Build script v5 with new layout (11-row header, cumulative section at rows 51-56, chart below)
2. Add rollup as an API parameter — fetch by (sequence, rollup) pair
3. Replace hardcoded `ADP_REGISTRY` with dynamic loading from `GROUP MAPPING.xlsx`
4. Add per-sequence metadata fetch (legal name, TPOC, ACRN, available funds) — separate lightweight API call
5. Implement line chart in openpyxl with 5 series
6. Split output by reporting group + chunk size (50 per file for large groups)
7. Make quarter range dynamic — extend based on latest data, not hardcoded FY2026

### For Josh (Client)
- Already sent the group mapping and 8 sample files — no further action needed until v5 is ready for review
- Will clarify later: file splitting pattern for CA1 ADP (61 sequences) — 50+11 vs 30+31

---

## 5. Open Items for Future

- **Color of Money** — blocked until NetSuite team adds the field
- **Labor Hours** — blocked until statistical account is created
- **Dynamic reporting groups (CA3)** — script should handle automatically since it reads from mapping file

---

*Document generated: April 15, 2026*

# FEMR NetSuite Report — Remaining Gaps & Open Items

**Updated:** April 15, 2026
**Script version:** `femr_netsuite_report_4.py`
**Status:** Script produces correct output for all available data. Remaining gaps require external data sources or client decisions.

---

## 1. Labor Hours Statistical Account

**What it is:**
Row 11 (Actuals) and Row 25 (Budgeted) — "Labor Hours statistical account". This tracks the number of labor hours spent on each ADP project per quarter. It's a count of hours, not a dollar amount.

**Current state:**
Always blank (0). The row exists in the output per Shoma's instruction ("keep it blank, don't skip").

**Why it's missing:**
The `account_name` for Labor Hours is `None` in the script — there is no corresponding GL account in the NetSuite `/femr/netamount/` API. The template itself has a note: *"We will create a statistical account for this later."*

Statistical accounts in NetSuite are separate from financial GL accounts. They track non-monetary quantities (hours, headcount, etc.) and require a separate Oracle/NetSuite configuration to expose via the API.

**What's needed to fix:**
- Josh or the NetSuite admin needs to create the statistical account in NetSuite
- Once created, they need to expose it through the APEX REST API (either via the existing `/femr/netamount/` endpoint with a new `account_name` value, or a new endpoint)
- Then we add the `account_name` string to `ACTUALS_BUDGET_ACCOUNTS[0]` in the script

**Who owns this:** Josh / NetSuite admin team

---

## 2. Color of Money

**What it is:**
Row 7 in the header block. Indicates the funding type for the project — values like `RDT&E` (Research, Development, Test & Evaluation) or `O&M` (Operations & Maintenance). This is a US government contract classification that determines how the money can be spent.

**Current state:**
Always blank.

**Why it's missing:**
The `/femr/netamount/` API does not return this field. It's not in the API parameters or response. The template ADP 62 shows `RDT&E` as an example value and has a note: *"Keep it Blank"* — suggesting Josh knew it wasn't available at the time.

The materialized view (`MV_FEMR_REPORT`) does not have a `color_of_money` field either. It may live in a different NetSuite record/table that isn't part of the current view.

**Possible values** (from the template "Lists" sheet):
- `RDT&E` — Research, Development, Test & Evaluation
- `O&M` — Operations & Maintenance

**What's needed to fix:**
- Determine where Color of Money is stored in NetSuite (likely on the Project record itself, not on transactions)
- Either add it to the MV/API response, or provide a separate lookup table (CSV/Excel mapping ADP sequence → Color of Money)
- Update the script to populate row 7

**Who owns this:** Josh — needs to identify the NetSuite field and expose it

---

## 3. External Approver 1 (Technical Point of Contact)

**What it is:**
Row 4 in the header block. The external (government) approver or technical point of contact for each ADP project. Josh specifically called out this as missing in his feedback: *"The 1st table is missing some columns for project information, e.g. Technical Point of Contact."*

**Current state:**
Always blank.

**Why it's missing:**
The MV has a field `display_outside_approver_1` which was discovered during initial data exploration, but it was `null` for the sequences we checked. The `/femr/netamount/` API doesn't return project metadata — it only returns financial amounts.

**What's needed to fix:**
Option A: If `display_outside_approver_1` is populated in the MV for some sequences, we could make one API call per sequence to `/mv_femr_report/` to fetch just the metadata (approver, etc.). This would add ~224 API calls total (one per sequence) — negligible compared to the ~95K financial data calls.

Option B: Josh provides a mapping file (CSV/Excel) with sequence → approver name.

Option C: A new lightweight API endpoint that returns project metadata for a given `display_sequence`.

**Who owns this:** Josh — needs to confirm if the MV field is populated, or provide the data another way

---

## 4. Revised Plan

**What it is:**
Row 53 in the formulas section (cumulative running totals area). It's supposed to show a revised budget plan — the updated budget after mid-project adjustments. It sits between "Budgeted Plan" (original budget) and "Actual" (what was actually spent).

**Current state:**
Always blank. The template also has it blank with a note from Atul: *"What is revised plan?"*

**Why it's missing:**
Nobody has confirmed what data source feeds this row. It's one of the open questions for Josh (#3 in the handoff doc). Possibilities:
- It could be a separate `segment` value in the API (like "REVISED" alongside ACTUALS/BUDGETED/CONTRACTING)
- It could come from a different NetSuite record (e.g., a revised budget journal)
- It could be manually maintained in a separate spreadsheet

**What's needed to fix:**
- Josh needs to answer: Where does Revised Plan data come from?
- If it's in the API, we need the exact `segment` and/or `account_name` values
- If it's external, we need the source file format and how to map it to sequences/quarters
- Once known, add cumulative formulas referencing the source row (same pattern as rows 49-54)

**Who owns this:** Josh — needs to define the data source

---

## 5. Govt Awards / Govt Obligated / Cash Collected / Remaining Cash

**What it is:**
Rows 43-46 in each tab. These are government contract financial tracking fields:

| Row | Field | Meaning |
|-----|-------|---------|
| 43 | govt awards | Total dollar amount the government has awarded for this project |
| 44 | govt obligated | Amount the government has legally committed (obligated) to pay |
| 45 | cash collected | Actual cash received from the government so far |
| 46 | remaining cash | Calculated: how much cash is still expected (obligated − collected, or similar) |

These are different from the Contracting section (rows 39-41) which tracks NextFlex's internal view. The govt rows track the government's side of the contract.

**Current state:**
All blank. Row 46 has label "add calc field" in column A, indicating it's a calculated field that depends on the other rows.

**Why it's missing:**
The template has a source note: *"source: bible"*. The "bible" is an internal NextFlex file (likely a master Excel workbook) that tracks government contract data. This data is NOT in NetSuite and NOT in the APEX API.

**What's needed to fix:**
- Josh needs to provide the "bible" file or explain its format
- We need to understand the mapping: how does the bible file map to ADP sequences and quarters?
- Once we have the file, we add a second data source to the script that reads from the bible file and populates rows 43-46
- Row 46 (remaining cash) likely needs a formula like `=govt_obligated - cash_collected` or similar — Josh needs to confirm the calculation

**Who owns this:** Josh — needs to provide the "bible" source file and field mapping

---

## 6. Chart / Graph (Visualization 4)

**What it is:**
A scatter/line chart embedded in each tab that visualizes the cumulative running totals from rows 49-54. It plots:
- Total Committed (line)
- Total Obligated (line)
- Total Expended (line)
- Budgeted Plan (line)
- Revised Plan (line, if available)
- Actual (line)

All plotted over time (quarters on x-axis, cumulative dollars on y-axis). This is the 4th visualization Josh described in the Loom call.

**Current state:**
Not implemented. No chart is generated.

**Why it's missing:**
Charts in openpyxl are possible but were deferred because:
1. The cumulative formulas were wrong until v4 — the chart would have shown incorrect data
2. Josh hasn't specified exact chart formatting preferences (colors, axis labels, chart type)
3. Some source data rows (Revised Plan, govt fields) are still blank

**What's needed to fix:**
- Cumulative formulas are now correct in v4 — chart data source is ready
- Need Josh to confirm: Is it a line chart or scatter plot? What colors for each series?
- Implementation: Use `openpyxl.chart.LineChart` or `ScatterChart`, add data series from rows 49-54, set quarter labels from row 48 as x-axis
- The chart should be placed around row 56-57 (between the formulas section and the source notes at row 59)

**Effort to implement:** Low — once chart preferences are confirmed, this is ~30 lines of openpyxl code per tab

**Who owns this:** 
- Josh: confirm chart type and formatting preferences
- Developer: implement once confirmed

---

## 7. Account 5993 — "Do Not Use" Question

**What it is:**
Row with label "Sub K Overhead 5993" — account `5993 ALLO : DNU ALLO G and A OH WFD`. The "DNU" stands for "Do Not Use" in NetSuite.

**Current state:**
The row exists in the output and pulls data from the API. If data exists for this account, it shows; if not, it's blank.

**Why it's an open question:**
The template notes: *"What is this GL corresponding in NetSuite - in NS 5993 is DNU."* It's flagged as Do Not Use in NetSuite, which means no new transactions should post to it, but historical data may exist.

**Decision needed from Josh:**
- Should this row remain in the report (showing any historical values)?
- Or should it be hidden/excluded?
- Per Shoma's directive ("keep it blank, don't skip"), it's currently included

**Current approach:** Keep it. Shoma said don't skip any rows.

---

## 8. CA1 ADP and PC Sequences — Scope

**What it is:**
The script has 224 sequences registered:
- 61 CA1 ADP sequences (1ADP001–1ADP061)
- 54 CA1 PC sequences (1PC001–1PC054)
- 110 CA2 ADP sequences (2ADP001–2ADP114)

Currently only CA2 ADP tabs have been generated (`--ca2-only` flag).

**Decision needed from Josh:**
- Should the report include CA1 ADP sequences? (Open question #2 in handoff doc)
- Should PC sequences be included?
- Do CA1 projects have Contracting data (Committed/Obligated/Expended)?
- Are CA1 and PC projects tracked in the same template layout, or do they have a different format?

**Impact:** If all 224 sequences are included, it's ~2.5x more API calls (~170K total) and ~4-5 output files instead of 3.

---

## 9. SF270 Data

**What it is:**
The template has a source note: *"source: SF270 needs to be put NSAW."* SF-270 is a US government form (Request for Advance or Reimbursement) used to request payment from the government. It tracks cash requests and disbursements.

**Current state:**
Not in the API. Not in the report.

**Why it's mentioned:**
This likely feeds into the "cash collected" field (row 45) or relates to the govt awards section. The note suggests this data needs to be imported into NSAW (NetSuite Analytics Workbook) first before it can appear in the report.

**What's needed:** Josh needs to confirm whether SF270 data has been loaded into NSAW, and if so, whether it's now accessible via the API.

---

## Summary — Action Items by Owner

### Josh (Client)
1. **Labor Hours** — Create statistical account in NetSuite, expose via API
2. **Color of Money** — Identify NetSuite field, provide mapping or API access
3. **External Approver 1** — Confirm if MV field is populated, or provide mapping
4. **Revised Plan** — Define the data source (API segment? External file?)
5. **Bible file** — Provide the govt awards source file and field mapping
6. **Chart preferences** — Confirm chart type and formatting
7. **Account 5993** — Keep or exclude?
8. **CA1/PC scope** — Should these be in the report?
9. **SF270** — Has this been loaded into NSAW?

### Developer (Atul)
1. **Chart implementation** — Ready to build once Josh confirms preferences (~30 lines)
2. **Bible file integration** — Build second data reader once file is provided
3. **Metadata API call** — Add approver/color-of-money fetch once data source is confirmed
4. **CA1/PC generation** — Run full report once scope is confirmed

---

*Document generated: April 15, 2026*
*Reference: femr_netsuite_report_4.py, FEMR_for_NetSuite.xlsx template*

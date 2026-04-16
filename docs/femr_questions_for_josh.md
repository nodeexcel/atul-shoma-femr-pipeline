# FEMR Export Template — Questions for Josh (Detailed Reference)

**Date:** April 15, 2026
**Context:** Josh sent an updated export template (`FEMR Export Template.xlsx`) with a redesigned layout. These questions need answers before we can build the updated script.

---

## Q1. Project Legal Name

**What we're asking:**
The template shows `"Strategic Innovation Project Ph2"` as the project name for 2ADP001. But the data we currently pull from the API/MV uses the short name `"CA2 ADP1 ESI Laser"`. These are two different fields in NetSuite:

- `display_project_shortname` = "CA2 ADP1 ESI Laser" (what we use now)
- `display_project_legalname` = "Strategic Innovation Project Ph2" (what Josh wants)

**Why it matters:**
We need to know where to get the legal name for all 224 sequences. The `/femr/netamount/` API only returns dollar amounts — it doesn't return project metadata like names.

**Possible answers:**
- "It's in the materialized view (`/mv_femr_report/`) under `display_project_legalname`" → We can make one API call per sequence to fetch it, but paginating the full MV is slow (~100 min). We'd need a filtered endpoint or a batch approach.
- "I'll send you a mapping file" → Josh provides an Excel/CSV with sequence → legal name for all projects.
- "Use the existing NSAW API with a new endpoint" → A lightweight metadata endpoint that returns project info for a given sequence.

**What we need:** Either API access to the legal name field, or a static mapping file.

---

## Q2. Technical Point of Contact

**What we're asking:**
The template has a new row "TECHNICAL POINT OF CONTACT" showing `"Aman S Gahoonia"` for 2ADP001. This is the external (government) approver or technical lead assigned to each ADP project.

**Why it matters:**
This field exists in the materialized view as `display_outside_approver_1`, but when we checked it during initial development, it was `null` for the sequences we tested. Josh's template now shows it populated, so either:
- The MV has been updated since then
- The data comes from a different source

**Possible answers:**
- "It's in the MV now under `display_outside_approver_1`" → We fetch it along with legal name.
- "It comes from a different NetSuite field/record" → Josh tells us which one.
- "I'll include it in a mapping file" → Same file as legal name.

**What we need:** Confirm data source — MV field, separate API, or mapping file.

---

## Q3. ACRN

**What we're asking:**
ACRN stands for **Accounting Classification Reference Number**. It's a code used in US government contracts to link funding to specific contract line items. The template shows `"AC"` for 2ADP001.

Our current script puts the rollup number (e.g., "1001") in the ACRNs row. But the new template has ROLLUP # as a separate row (row 4) and ACRN as its own row (row 10) with a different value entirely.

**Why it matters:**
The MV has a field `display_acrn`, but it was `null` when we checked. Josh's template now shows a real value ("AC"), so we need to know where this comes from.

**Possible answers:**
- "It's in the MV under `display_acrn`" → Same fetch as legal name and TPOC.
- "It's on the Project record in NetSuite" → May need a different API.
- "I'll include it in a mapping file" → Same file as other metadata.

**What we need:** Confirm data source.

---

## Q4. Available Funds

**What we're asking:**
Row 11 in the new template shows "AVAILABLE FUNDS" with a value of `0` for 2ADP001. This is a brand new field that wasn't in any previous template.

**Why it matters:**
We don't know what this field represents or where the data comes from. It could be:
- Remaining budget (Budgeted Total minus Actuals Total)
- Unobligated balance on the government contract
- A field from a different NetSuite record
- A calculated field (formula based on other rows)

**Possible answers:**
- "It's a calculated field: X minus Y" → We write a formula.
- "It comes from field Z in NetSuite" → We fetch it from the API/MV.
- "It's from the bible file / contract data" → Separate data source.
- "Leave it as 0 for now, I'll clarify later" → We keep the row with value 0.

**What we need:** Definition of the field and its data source or formula.

---

## Q5. Remaining Cash Calculation

**What we're asking:**
The new template adds "Remaining Cash" to the Contracting section (row 49). Looking at the data for 2ADP001:

| Quarter | Obligated | Expended | Remaining Cash |
|---------|-----------|----------|---------------|
| Q4 FY20 | 27,100,000 | 0 | 27,100,000 |
| Q1 FY21 | 0 | 5,500,000 | -5,500,000 |
| Q2 FY21 | 0 | 21,600,000 | -21,600,000 |

This pattern looks like: **Remaining Cash = Obligated − Expended** for each individual quarter (not cumulative).

**Why it matters:**
We need to confirm the exact formula so we can generate it correctly for all sequences. Negative values (like -5,500,000) suggest this is per-quarter, not a running balance.

**Possible answers:**
- "Yes, Remaining Cash = Obligated − Expended per quarter" → We write `=B47-B48` style formulas.
- "No, it should be cumulative: Total Obligated − Total Expended" → Different formula.
- "The formula is something else" → Josh specifies.

**What we need:** Confirm the exact formula.

---

## Q6. Dynamic Columns

**What we're asking:**
Josh said: *"The quarter columns should not be fixed and should be dynamic in case new postings come in."*

Currently our script hardcodes fiscal years FY2020–FY2026 (28 quarter columns). "Dynamic" could mean:

**Option A:** Show all quarters from FY2020 to the latest fiscal year that has any data. If a new posting appears in FY2027, a new column automatically shows up.

**Option B:** Only show quarters where at least one account has a non-zero value. Empty quarters are hidden entirely.

**Option C:** Always start from FY2020, but extend the end date based on the current date (e.g., always include the current fiscal year + 1).

**Why it matters:**
Option A is the simplest and most future-proof. Option B would make each tab have different column counts (messy). Option C is predictable but requires updating logic.

**Possible answers:**
- "Option A — show all quarters from FY2020 to the latest year with data" → Simple to implement.
- "Option B — only show quarters with data" → More complex, each tab may differ.
- "Always FY2020 to current FY+1" → We calculate based on today's date.

**What we need:** Which approach Josh wants.

---

## Q7. Reporting Group — Type A

**What we're asking:**
Row 2 in the new template shows `"REPORTING GROUP - TYPE A"` with value `"ADP"`. Our data has three types of sequences:

| Sequence prefix | Type A | Example |
|-----------------|--------|---------|
| 2ADP___ | CA2 | 2ADP001 = CA2 ADP project |
| 1ADP___ | CA1 | 1ADP001 = CA1 ADP project |
| 1PC___ | CA1 | 1PC001 = CA1 PC (Project Call) |

**Why it matters:**
We need to know what value to put in this row for each type. The template only shows one example (2ADP001 = "ADP").

**Possible answers:**
- "For 2ADP sequences, show 'ADP'. For 1ADP, show 'ADP'. For PC, show 'PC'" → Simple prefix logic.
- "The Type A value comes from the `display_type_a` field in the MV" → We fetch it.
- "Only generate CA2 ADP tabs, so it's always 'ADP'" → We skip CA1/PC entirely.

**What we need:** The mapping rule or data source for this field.

---

## Q8. Color of Money

**What we're asking:**
Row 9 "COLOR OF MONEY" is blank in both the old and new templates. Color of Money is a US government term for the type of funding appropriation:

- **RDT&E** = Research, Development, Test & Evaluation funds
- **O&M** = Operations & Maintenance funds

The old template's "Lists" sheet had these as dropdown options, but no project actually had a value filled in.

**Why it matters:**
If the data exists somewhere in NetSuite, we should pull it. If it doesn't exist yet, we leave the row blank.

**Possible answers:**
- "Leave it blank for now" → No change needed.
- "It's on the Project record in NetSuite, field name is X" → We can fetch it.
- "I'll add it to the mapping file" → Include in the metadata file.

**What we need:** Is this data available anywhere today, or is it a future item?

---

## Q9. Labor Hours

**What we're asking:**
"Labor Hours statistical account" is the first row in both Actuals and Budgeted sections. It tracks the number of hours worked (not dollars). It's always blank/zero because there's no corresponding account in the NetSuite API.

The old template had a note: *"We will create a statistical account for this later."*

**Why it matters:**
Statistical accounts in NetSuite are different from financial GL accounts. They track non-monetary quantities (hours, headcount). Someone on the NetSuite admin side needs to create this account and expose it through the API.

**Possible answers:**
- "Keep the row blank for now, we haven't created it yet" → No change.
- "The statistical account has been created, the account name is X" → We add it to the script.
- "We'll use a different data source for hours" → Josh specifies.

**What we need:** Has the account been created? If yes, what's the `account_name` string?

---

## Q10. Revised Plan

**What we're asking:**
The old template (`FEMR for NetSuite.xlsx`) had a "Revised Plan" row in the cumulative formulas section — it sat between "Budgeted Plan" and "Actual". It was always blank.

The new template (`FEMR Export Template.xlsx`) does NOT have a Revised Plan row at all. The cumulative section goes: Total Committed → Total Obligated → Total Expended → Budgeted Plan → Actual (5 rows, no Revised Plan).

**Why it matters:**
If Revised Plan is dropped, we don't include it — simpler. If it's coming back later, we should keep a blank row as a placeholder.

**Possible answers:**
- "Revised Plan is dropped, don't include it" → We remove it.
- "Keep a blank row for it, we'll add data later" → We include an empty row.
- "It will come from source X" → We build it in.

**What we need:** Is Revised Plan permanently removed or temporarily missing?

---

## Q11. CA1 and PC Scope

**What we're asking:**
Our script has 224 sequences registered:

| Category | Count | Sequences |
|----------|-------|-----------|
| CA2 ADP | 110 | 2ADP001 – 2ADP114 |
| CA1 ADP | 61 | 1ADP001 – 1ADP061 |
| CA1 PC | 54 | 1PC001 – 1PC054 |

So far we've only generated CA2 ADP tabs (110 sequences, 3 output files). The new template example is also CA2 (2ADP001).

**Why it matters:**
Including all 224 sequences means ~2.5x more API calls and runtime. CA1 and PC projects may have different data characteristics (e.g., no Contracting data, different project types).

**Possible answers:**
- "Only CA2 ADPs for now" → We keep using `--ca2-only`.
- "Include CA1 ADPs too, but not PC" → We add a filter.
- "Include everything — CA1, CA2, and PC" → Full run.

**What we need:** Which sequences should be in the report.

---

## Q12. Account 5993 (Do Not Use)

**What we're asking:**
Account 5993 is `"5993 ALLO : DNU ALLO G and A OH WFD"`. The "DNU" means **Do Not Use** — it's been deactivated in NetSuite, meaning no new transactions should post to it.

The row appears in both old and new templates but is always blank (no data). Shoma previously said: *"keep it blank, don't skip any row even if there is no data."*

**Why it matters:**
If there's no data and never will be data (because the account is DNU), including it adds a permanently empty row. But Shoma wants it there.

**Possible answers:**
- "Keep it, even if always blank" → Current approach, no change.
- "Remove it, it's truly dead" → We drop the row.
- "There might be historical data for some sequences" → We keep it and let the API populate it.

**What we need:** Final decision — keep or remove?

---

## Q13. Govt Awards / Bible File

**What we're asking:**
The old template had these rows (between Contracting and the formulas section):
- **govt awards** — Total dollar amount the government awarded
- **govt obligated** — Amount the government legally committed to pay
- **cash collected** — Actual cash received from the government
- **remaining cash** — Calculated leftover

The source note said: *"source: bible"* — referring to an internal NextFlex master file that tracks government contract data outside of NetSuite.

The new template removed all of these rows. Instead, "Remaining Cash" moved into the Contracting section as `Obligated − Expended`.

**Why it matters:**
If these rows are permanently gone, we remove them from the script. If they're coming back later (once the bible file is integrated), we should know so we can plan for it.

**Possible answers:**
- "Dropped permanently — the new Remaining Cash in Contracting replaces this" → We remove the old rows.
- "Coming back later once we integrate the bible file" → We note it as a future task.
- "We still need them, I forgot to include them" → We add them back.

**What we need:** Are the govt awards rows permanently removed?

---

## Q14. SF270 Data

**What we're asking:**
The old template had a source note: *"source: SF270 needs to be put NSAW."*

**SF-270** is a US government form called **"Request for Advance or Reimbursement"**. Organizations use it to request payment from the government for work performed. It tracks:
- How much was requested
- How much was disbursed
- Outstanding reimbursement balance

The note suggested this data needed to be imported into NSAW (NetSuite Analytics Workbook) before it could appear in the report.

**Why it matters:**
If SF270 data has been loaded into NSAW, it might now be available through the API and could feed into the cash collected / govt awards fields. If it hasn't been loaded, this is still a future item.

**Possible answers:**
- "Not loaded yet, it's a future item" → No action needed now.
- "It's been loaded, it feeds into field X" → We integrate it.
- "It's no longer relevant with the new template" → We drop it entirely.

**What we need:** Is SF270 data in NSAW now, and does it affect the current report?

---

## Summary — What's Blocking the v5 Script

| Priority | Questions | Impact |
|----------|-----------|--------|
| **Must have** | Q1 (Legal Name), Q2 (TPOC), Q3 (ACRN), Q4 (Available Funds) | Can't populate header rows without answers |
| **Must have** | Q5 (Remaining Cash formula), Q6 (Dynamic columns) | Affects data layout |
| **Should have** | Q7 (Type A), Q11 (Scope) | Affects what sequences to generate |
| **Nice to have** | Q8-Q10, Q12-Q14 | Mostly "keep blank or remove" decisions |

If Josh can answer Q1-Q6 first, we can build the v5 script immediately. The rest can be handled as follow-ups.

---

*Document generated: April 15, 2026*

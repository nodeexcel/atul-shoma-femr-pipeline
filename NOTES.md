# FEMR Script — Development & QA Notes

Last updated: 2026-04-17

---

## Starting a New Session

Read these files in order before doing anything:
1. `memory/project_femr_status.md` — current version, run status, pending items
2. `memory/project_data_issues.md` — known data issues (don't re-investigate)
3. `docs/client_communications_log.md` — all client email/meeting history
4. `CLAUDE.md` Known Blockers section
5. This file (NOTES.md) — QA checklist and lessons learned

Then check: what is the highest-numbered script in `scripts/`? That is the active version.
Then check: are there any background runs? `ps aux | grep femr_netsuite_report | grep -v grep`

---

## The Core Rules

**Never assume a feature works because it was written. Run a test that would catch it if broken.**
The 50-tab split was coded in v3, dropped silently in v5, and we only caught it because we ran ADP today.

**Never assume a data issue is a script bug.** Check `project_data_issues.md` first.

**Never assume a log saying "Done" means the output is correct.** Open the Excel file and check.

**Never assume prior session context is complete.** Read the files — don't rely on summaries.

---

## Before Writing a New Version

1. **Read the previous version's docstring** — understand what changed and why before touching anything.
2. **Read the template** (`docs/Re_ FEMR /FEMR Export Template 041526.xlsx`) — the layout is the source of truth, not memory.
3. **Read GROUP MAPPING.xlsx SEQUENCE sheet** — source of truth for which sequences belong to which group.
4. **Check CLAUDE.md Known Blockers section** — some issues are data gaps (not script bugs); don't re-investigate.
5. **List every feature the new version must preserve** — write it down before you start editing.

---

## After Writing a New Version — Pre-Run Checklist

Run through this before any full-group run:

### 1. Single Sequence Test (always)
```bash
venv/shoma/bin/python scripts/femr_netsuite_report_XX.py --sequence 2ADP001 -o test_vXX_2ADP001.xlsx --skip-preload
```
- Open the file. Check: correct number of tabs, header layout, data in cells, chart present.

### 2. Test Every New Feature in Isolation
For each feature added or changed in this version, write a test that **would fail if the feature were broken**:

| Feature | How to test |
|---------|-------------|
| File splitting | Run a small group with `--split-size 5`. Count files and tabs per file. |
| Dynamic quarter detection | Check log output shows correct latest quarter. |
| Chart aesthetic | Open output, click chart, check colors/legend position/no titles. |
| Currency format (Available Funds) | Open output, check row 29 shows `$` format, not plain number. |
| Multi-identifier sequences | Run `--sequence 2ADP099` — should produce 2 tabs. |

### 3. Spot-Check a Multi-Identifier Sequence
```bash
venv/shoma/bin/python scripts/femr_netsuite_report_XX.py --sequence 2ADP099 -o test_vXX_2ADP099.xlsx --skip-preload
```
Verify 2 tabs are produced (R1099 + RCore099).

### 4. Tab Count Verification (after full group run)
Before sending ANY file to Josh:
```
WFD:      ~27 tabs  (1 file)
Internal: ~37 tabs  (1 file)
Comml:    ~42 tabs  (1 file, including CC007 with 2 tabs)
OGA:      ~46 tabs  (1 file, OGA047 missing — data gap, not bug)
ADP:      ~247 tabs (5 files × 50 tabs — check ALL 5 files)
```
If tab count is off by more than 2, investigate before sending.

### 5. File Naming Check
After a group run, verify file names follow the expected pattern:
- Single file groups: `femr_vXX_wfd_wfd.xlsx`
- Split groups (ADP): `femr_vXX_adp_adp_001-050.xlsx`, `femr_vXX_adp_adp_051-100.xlsx`, etc.

---

## Features That Have Been Lost Between Versions (historical failures)

| Feature | Lost in | Root cause | Fix |
|---------|---------|------------|-----|
| 50-tab file split | v5 (rewrote from v3) | Full rewrite didn't carry over the chunking logic | v11 reinstates it |
| Available Funds currency format | unknown | `chart.y_axis.number_format` silently ignored | use `numFmt` in v8 |
| Chart legend position | v5+ | Default legend position not set | v8 moves to right, v10 to bottom |
| Dynamic quarter range | v1-v9 | Hardcoded `FY2020-2026` | v9 auto-detects from MV |

**Pattern:** features are most often lost during full rewrites or when adding a new feature changes the structure of a function. After any structural change, re-verify all existing features.

---

## Known Data Issues (not script bugs — do not re-investigate)

| Issue | Status | Notes |
|-------|--------|-------|
| OGA047 missing | Data gap | Not in GROUP MAPPING SEQUENCE sheet. Goes OGA001-OGA046 then None. Josh/Taylor must add it. |
| EWD014 group | Blocked | GROUP MAPPING says OGA, Josh says WFD. Wait for Taylor's updated mapping (post 2026-04-22). |
| 2ADP099 R1099 tab | Expected | Taylor confirmed R1099 is invalid. Only RCore099 (orphan) is real. Will fix in NetSuite. |
| Pre-FY2020 cumulative | Pending | Q1 FY20 starts at 0 instead of FY2016-2019 historical balance. Needs Josh to clarify data source. |

---

## API Gotchas

1. **`/femr/netamount/` ignores rollup filter param** — it silently returns wrong data for multi-identifier sequences. Always use MV tight-filter (`/mv_femr_report/?q=...`) for those.
2. **`chart.y_axis.number_format`** — non-standard, silently ignored. Use `chart.y_axis.numFmt`.
3. **`chart.y_axis.auto`** — AttributeError (NumericAxis has no 'auto' attribute). Don't use it.
4. **MV has ~2M rows** — always filter with `q=` JSON filter. Never paginate the full table.
5. **Metadata preload 5-page cap** — if a sequence hits the cap, it falls back to per-sequence query. Check logs for `WARNING: metadata hit 5-page safety cap`.

---

## Script Versioning Rules

- **Never edit a working version in place.** Copy to `_XX.py` first.
- **Update the module docstring** with a "Changes from vN-1" section.
- **Update the version string** in the docstring and in the `logger.info("=== FEMR ... (vXX)")` line.
- **Run the pre-run checklist above** before promoting a new version to "active".
- The highest-numbered script in `scripts/` is always the active version.

---

## Run Commands (current active: v12)

```bash
# Single sequence test
venv/shoma/bin/python -u scripts/femr_netsuite_report_12.py --sequence 2ADP001 -o test_v12_2ADP001.xlsx --skip-preload

# Single group
venv/shoma/bin/python -u scripts/femr_netsuite_report_12.py --group WFD -o femr_v12 --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_12.py --group ADP -o femr_v12 --workers 40

# All groups (overnight)
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_12.py -o femr_v12 --workers 40 > /tmp/v12_full.log 2>&1 &

# Split-size test (verify chunking logic with small group)
venv/shoma/bin/python -u scripts/femr_netsuite_report_12.py --group WFD -o /tmp/test_split --split-size 5 --workers 40
```

### Monitoring a background run
```bash
tail -f /tmp/v12_full.log
ps aux | grep femr_netsuite_report | grep -v grep
watch -n 30 'ls -lah femr_v12*.xlsx 2>/dev/null'
```

---

## Before Sending Files to Josh

1. Run tab count check (see above).
2. Spot-open each file — confirm chart renders, data is not all zeros, Available Funds shows `$`.
3. Confirm ADP is split into 5 files (not 1 giant file).
4. Note any known gaps (OGA047, EWD014) in the message to Josh so he's not surprised.
5. Ask Josh to spot-check 2-3 tabs from different groups against NetSuite directly.

---

## Lessons Learned

- **"Written" ≠ "working."** A feature that isn't tested after each version bump should be assumed broken until proven otherwise.
- **Full rewrites lose features.** When creating a new version from scratch (not incremental), explicitly list every feature from the previous version and verify each one.
- **Log output is not enough.** A successful run with no errors does not mean the output is correct. Always open the Excel file and eyeball the key sections.
- **Tab counts catch structural bugs.** If the tab count is wrong, something structural is broken (splitting, multi-id detection, group filtering). Fix before moving on.
- **Excel Online does not render chart label rotation.** `bodyPr rot="-60000000"` in catAx txPr is ignored by Excel Online even when XML matches a Desktop Excel template exactly. Do not spend time fixing axis label rotation for Excel Online — it won't work via openpyxl XML surgery.
- **Excel Online multi-level category axis grouping:** When X-axis labels like "Q1 FY20", "Q2 FY20" repeat the "FY20" token, Excel groups them into two stacked rows regardless of `noMultiLvlLbl` setting. This is an Excel Online rendering behavior. Fix: use non-breaking space (` `) in `_q_label()` instead of regular space to break pattern detection.

---
name: FEMR known data issues and blockers
description: Active data issues from client feedback, NetSuite problems, API limitations — check before each run
type: project
originSessionId: 03ce2e1b-d66e-4c61-9283-53647745d1bc
---
## Active Data Issues (updated 2026-04-29)

### 1. Duplicate sequences (orphan + rollup under same sequence)
- **CC007**: Was 2 tabs (R4006 + R960011). Now 1 tab — Josh confirmed 960011 is now a child of rollup 4006. 1 tab is correct going forward. **RESOLVED.**
- **2ADP099**: Rollup 1099 + Orphan Core099 — Taylor confirmed rollup 1099 should NOT exist. Core099 is the only valid project. **Waiting for NetSuite fix.**

### 2. EWD014 categorization — RESOLVED
- Josh confirmed WFD (2026-04-24). GROUP MAPPING updated. WFD re-run complete (28 tabs, v15).

### 3. netamount API cannot filter by rollup
- The `/femr/netamount/` endpoint silently ignores `display_rollup_num` parameter
- For multi-identifier sequences, we use MV queries instead (slower but correct)
- **Impact**: Multi-identifier sequences take ~8 min vs ~90s for single-identifier

### 4. Pre-FY2020 cumulative starting balance — RESOLVED
- **Implemented in v12+**: fetches FY2016-2019, seeds Q1 FY2020 opening balance.

### 5. Fields still blank (by design)
- **Color of Money** — not in NetSuite yet (Josh confirmed: leave blank)
- **Labor Hours** — statistical account not created yet (Josh: leave blank)
- **TPOC** — populated for some sequences, null for most

### 6. Items permanently removed from report
- **Revised Plan** row, Govt awards rows, Source notes — Josh confirmed dropped.

### 7. OGA047 — RESOLVED
- Added to GROUP MAPPING. OGA re-run complete (47 tabs, v15). OGA047 has no financial data (new/empty sequence in NetSuite — expected).

### 8. 2ADP022 empty in original overnight run — RESOLVED
- Root cause: transient API failure during original run. v15 re-run has correct data. ✅

### 9. 2ADP001 G&A 5991 — NOT A BUG
- Budget G&A present (41,537.27/quarter from FY21+). Actuals G&A sparse (only quarters with spend).
- API returns 0 where no spend — matches NetSuite data. Not a script issue.

### 10. Chart issues (Josh feedback 2026-04-27) — FIXED IN v14 ✅
- Legend at bottom overlaps X-axis → `chart.legend.position = "r"`
- X-axis labels jump to top when Y negative → `<crosses val="min" />` in `_patch_chart_axes()`

### 11. Chart: quarter labels on zero line + legend inside plot area (Josh feedback 2026-04-28) — FIXED IN v15 ✅
- Quarter labels sat on the Y=0 zero line → `tickLblPos="low"` in catAx XML
- Legend floating inside chart plot area → `chart.legend.overlay = False`
- Both verified in test_v15.xlsx and full v15 run (2026-04-28/29) ✅

### 12. ADP run performance
- ~2 min per sequence. Full ADP run ~8-9 hours.
- v13 adds local JSON cache (quarter-based invalidation). NOT YET IN PRODUCTION — needs testing.

### 13. Cumulative section formula cells returning None — NOT A BUG
- openpyxl with `data_only=True` returns None for formula cells with no cached value.
- Cells contain correct formulas: `=C45`, `=D45+B52` etc. (cumulative pattern).
- This is expected behavior for freshly generated files — Excel hasn't cached the results.
- Do NOT re-investigate this. It is correct.

### 14. EWD014 financial data — RESOLVED (2026-04-29)
- EWD014 last posting was in 2018. No FY2020+ actuals or budget.
- Main quarterly table (FY2020–present) correctly shows no data.
- Cumulative section correctly shows historical pre-FY2020 values.
- Josh confirmed: "That's why it has no values in this one but has values on the cumulative going forward." ✅
- NOT a bug. Do not re-investigate.

### 16. Available Funds wrong on 28 ADP sequences — FULLY RESOLVED ✅ (2026-05-04)
- Josh reviewed v15 files and found Available Funds wrong on 28 ADP sequences.
- Root cause: Josh changed NetSuite logic for Available Funds mid-week; v15 ran during transition.
- **Not a script bug.** v16 re-run pulled corrected data — all 27 verifiable sequences match Josh's expected values to the cent ✅
- **2ADP083** — Josh confirmed correct value is **$0**. v16 matches ✅ FULLY RESOLVED.

### 17. 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 — RESOLVED IN v16 ✅
- Josh flagged this column had values when it should be blank.
- v16 verified: FY2026 column is None/blank. Corrected NetSuite data coming through. ✅

### 18. 2ADP099 — FIXED IN v17 ✅ (2026-05-05)
- Josh confirmed: NetSuite team will NOT change the sequence number — both Rollup 1099 and Orphan Core099 keep sequence 2ADP099. Two tabs are correct.
- Josh confirmed: data exists (project # 588627 visible in FEMR report).
- Josh confirmed: Oracle permissions are dataset-level only — NO per-rollup restrictions. The 401 is NOT an Oracle permissions issue.
- **Root cause found:** `_fetch_mv_by_identifier()` in v16 was missing the OAuth `Authorization: Bearer` header. Single-id sequences use `_fetch_netamount()` which had auth. Multi-id sequences (only 2ADP099 at this point) use the MV path — no auth → 401 on every call.
- **Fix in v17:** Added `_get_auth_header()` to the `urllib.request.Request` in `_fetch_mv_by_identifier()` — one line change.
- **Tested:** `--sequence 2ADP099 --skip-preload` → both tabs (`R1099` and `RCore099`) have data ✅
- **Full ADP run with v17 in progress.**
- Do NOT re-investigate. Fixed.

### 19. 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 — WILL HAVE VALUES IN NEXT RUN (2026-05-04)
- Previously blank in v16 (confirmed correct at the time — no budget uploaded yet).
- Josh confirmed: new budget uploads were done after v15. This field will now have values.
- **NOT a bug** — expected behavior after budget upload. Do not flag as an error in next run.

### 15. Local data caching (v13) — REJECTED by Josh (2026-04-29)
- Atul proposed caching API data locally to speed up re-runs.
- Josh rejected: actuals refresh daily from transactions; budgets change with each budget upload.
- A local cache would serve stale data. **Decision: always pull directly from Oracle APEX API.**
- **v13 cache feature should NOT be promoted to production.** Archive v13 as experimental only.

**Why:** Decisions from April 15 meeting and subsequent client emails. See `docs/client_communications_log.md`.

**How to apply:** Before generating reports or responding to client feedback, check if an issue is already known here. Don't re-investigate resolved items.

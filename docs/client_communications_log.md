# Client Communications Log — FEMR NetSuite Project

**Rule:** Every email, Slack, or meeting exchange that contains a decision, data clarification, or requirement change must be logged here immediately — before the conversation ends. Paste the key content, not just a summary.

**Why:** Claude conversation context gets compacted over time. Any email shared only in the chat is lost. This file is the permanent record.

---

## How to Use This File

When you share an email with Claude:
1. Claude pastes the key content here immediately.
2. Claude extracts decisions/action items into the relevant section.
3. Future sessions start by reading this file to pick up context.

---

## Thread Index

| Date | From | Subject / Topic | Section Link |
|------|------|-----------------|--------------|
| 2026-04-15 | Josh Grapani | Meeting answers + new files | [→ Apr 15 Meeting](#april-15-2026--josh-grapani-meeting) |
| 2026-04-16 | Taylor Bui | Sequence/Rollup data issue (CC007, 2ADP099) | [→ Taylor Thread](#april-16-2026--taylor-bui-sequence-issue-thread) |
| 2026-04-18 | Josh Grapani | Feedback on WFD/Internal/Comml files | [→ Apr 18 Feedback](#april-18-2026--josh-grapani-file-review-feedback) |
| 2026-04-22 | Josh + Taylor | Post-meeting mapping update (PENDING) | [→ Awaited](#awaited-communications) |

---

## April 15, 2026 — Josh Grapani Meeting

**Full notes:** `docs/femr_meeting_summary_apr15.md`

**Key decisions made:**
- Project Name = `display_project_legal_name` always (no orphan/rollup logic)
- Rollup is the unique identifier — one tab per (sequence, rollup) pair
- 50 sequences per file for large groups
- Dynamic quarter range — auto-extend, don't hardcode FY2026
- Remove "Revised Plan" row from cumulative section
- Color of Money + Labor Hours = leave blank (not in NetSuite yet)
- Govt Awards rows dropped permanently
- Include ALL sequences from GROUP MAPPING.xlsx dynamically
- Josh sent: `GROUP MAPPING.xlsx` + `FEMR Export Template 041526.xlsx`

---

## April 16, 2026 — Taylor Bui Sequence Issue Thread

**Full notes:** `docs/femr_taylor_sequence_issue.md`

**Participants:** Josh Grapani, Taylor Bui, Shoma Sinha, Atul Kumar, Jayaram P, Diane Baxster, Marirose Landicho-Rasay, Randy Lu

**Key decisions made:**
- 2ADP099 Rollup 1099 is **invalid** — only Core099 (orphan) is real
- CC007 Rollup 4006 + Orphan 960011 are both valid (2 tabs correct)
- Root cause: NetSuite data migration created orphan/rollup inconsistencies
- Josh + Taylor meeting scheduled: **2026-04-22 (Tuesday)**
- After meeting: may receive updated GROUP MAPPING.xlsx

**Script impact:**
- Script v7+ handles multi-identifier sequences correctly (separate tabs)
- Once Taylor fixes data, 2ADP099 will reduce to 1 tab

---

## April 18, 2026 — Josh Grapani File Review Feedback

**Type:** Email reply
**Participants:** Josh Grapani, Atul Kumar, Shoma Sinha

**Raw content / key quotes:**
> "The graphs still do not have axis labels; Axis values for both Amount and Quarter still need to be added. (Please see the attached picture as an example for your reference)."

> "Regarding your question on the cumulative section: Yes, it is still needed to pull the pre-FY2020 data, as that is required to correctly derive the cumulative values."

**Josh's chart reference image shows:**
- Y-axis: dollar values visible ($0.00, $5,000,000.00 ... $30,000,000.00)
- X-axis: quarter labels visible (Q1 FY20, Q2 FY20 ... Q2 FY26)
- Legend at bottom: Funds Committed, Obligated Funds, Pre-Bill Expenditures, Budgeted Spend, Actual Expenditures
- Both Y-axis values and X-axis labels circled in red as what's missing

**Decisions made:**
1. **Chart axis labels** — both Y-axis (dollar values) and X-axis (quarter labels) must be visible. This is NOT about axis titles — it's about the tick mark values being shown.
2. **Pre-FY2020 cumulative data** — CONFIRMED REQUIRED. Must pull FY2016–2019 historical data to correctly seed Q1 FY2020 cumulative opening balance.

**Action items:**
- [ ] Fix chart: ensure Y-axis and X-axis tick labels are visible and formatted correctly (Y: $#,##0.00, X: Q1 FY20 etc.)
- [ ] Implement pre-FY2020 data pull for cumulative section seeding
- [ ] Create v12 with both fixes

**Script impact:**
- Chart: `chart.y_axis.delete = False`, `chart.x_axis.delete = False` — axis labels must not be hidden
- Y-axis numFmt: `'$#,##0.00'` to match Josh's image
- Pre-FY2020: need additional API calls for FY2016–2019 data per sequence, feed into cumulative starting values

---

## Awaited Communications

### Post-2026-04-22 Josh+Taylor Meeting
**Expecting:**
- Updated `GROUP MAPPING.xlsx` with:
  - EWD014 moved from OGA → WFD
  - OGA047 added (currently missing from SEQUENCE sheet)
  - Any other sequence corrections from Taylor's cleanup

**Action when received:**
1. Replace `docs/Re_ FEMR /GROUP MAPPING.xlsx` with updated file
2. Re-run WFD group (gains EWD014)
3. Re-run OGA group (gains OGA047, loses EWD014)
4. Re-run ADP if any ADP sequences were affected
5. Log the update in this file

---

## Template for New Entries

```markdown
## [Date] — [Person] — [Subject]

**Type:** Email / Meeting / Slack
**Participants:** ...

**Raw content / key quotes:**
> "[paste exact quote if important]"

**Decisions made:**
- ...

**Action items:**
- [ ] Atul: ...
- [ ] Josh: ...

**Script impact:**
- ...
```

---

## Open Questions Pending Response

| # | Question | Asked | Asked by | Status |
|---|----------|-------|----------|--------|
| 1 | Pre-FY2020 cumulative starting balance | Asked 2026-04-18 | Rahul/Atul | **ANSWERED — Yes, pull pre-FY2020 data** |
| 2 | Does `/femr/netamount/` API support filtering by rollup number? (silent ignore suspected) | Not yet asked | Rahul/Atul | **Pending** |

---

*File created: 2026-04-17*
*Rule: Update this file immediately when any client email is shared in a Claude session.*

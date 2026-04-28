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
| 2026-04-24 | Josh Grapani | Confirmed EWD014→WFD and OGA047 data | [→ Apr 24 Mapping](#april-24-2026--josh-grapani-mapping-confirmation) |
| 2026-04-24 | Josh Grapani | CC007 confirmation + ADP review feedback | [→ Apr 24 ADP Feedback](#april-24-2026--josh-grapani-adp-review-feedback) |
| 2026-04-28 | Josh + Shoma + Atul | Deployment planning meeting — web app, shared folder, NetSuite, API auth, chart fix | [→ Apr 28 Meeting](#april-28-2026--deployment-planning-meeting) |

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

## April 24, 2026 — Josh Grapani Mapping Confirmation

**Type:** Email reply (in response to our v12 files)
**Participants:** Josh Grapani, Atul Kumar, Shoma Sinha

**Raw content:** Josh replied with a NetSuite data screenshot showing two rows:

| PROJ_INT_ID | DISPLAY_SEQUENCE | PROJECT_NUMBER | DISPLAY_ROLLUP_NUM | REPORTING_GROUP_TYPE_A | TYPE_A_PROJECT_CATEGORY | TYPE_B_PROJECT_TYPE |
|-------------|-----------------|----------------|-------------------|----------------------|------------------------|-------------------|
| 2915 | OGA047 | 730030 | 730030 | OGA | OGA FedI | OGA-Tech Prime |
| 693 | EWD014 | 850002 | 850002 | WFD | EWD | EWD-Non Gov |

**Decisions made:**
1. **EWD014** → REPORTING_GROUP = **WFD** (confirmed). Must move from OGA file to WFD file.
2. **OGA047** → REPORTING_GROUP = **OGA** (confirmed, exists in NetSuite). Must be added to OGA file. PROJECT_NUMBER = DISPLAY_ROLLUP_NUM = 730030 (orphan — both same).

**Action items:**
- [x] Update GROUP MAPPING.xlsx: change EWD014 from OGA → WFD
- [x] Update GROUP MAPPING.xlsx: add OGA047 as OGA
- [ ] Re-run WFD (gains EWD014)
- [ ] Re-run OGA (gains OGA047, loses EWD014)

**Script impact:**
- GROUP MAPPING.xlsx SEQUENCE sheet must be updated before re-run
- OGA047 is an orphan (PROJECT_NUMBER = DISPLAY_ROLLUP_NUM = 730030)

---

## April 24, 2026 — Josh Grapani ADP Review Feedback

**Type:** Email reply (reviewing ADP files 001–200)
**Participants:** Josh Grapani, Atul Kumar, Shoma Sinha

**Raw content / key quotes:**
> "Yes, project 960011 is now included as children of 4006, so now they are in the same rollup."

> "The charts are inconsistent. Axis labels for Quarters and Legends overlaps."

> "Axis labels are on top when the y axis value (Amount) is in negative side."

> "This one is the closest to the correct chart, but it looks like the legends are still inside the chart area. This only happens when there is only one value on the negative side of the y axis (Amount)."

> "For the charts, I suggest that the legends be placed on the right side, not parallel to the x-axis (quarters) values."

**Chart issues (with screenshots):**
- Image #2: Legend at bottom overlaps with X-axis quarter labels (positive values chart)
- Image #3: When Y values are negative, category axis (quarter labels) moves to TOP of chart because axis crosses at Y=0. Legend overlaps "Plot Area".
- Image #4: Closest to correct but legend still inside chart area

**Data issues:**
- **2ADP001** — G&A 5991 values missing for both Actuals and Budget rows. Also affects cumulative section.
- **2ADP022** — No values in either the main table or cumulative section (should have data).

**Decisions made:**
1. **CC007** — CONFIRMED: project 960011 is now a child of rollup 4006. 1 tab is correct going forward.
2. **Legend position** — Josh explicitly requests legend on the **RIGHT** side (not bottom).
3. **Negative Y-axis** — category axis must stay at BOTTOM even when all values are negative. Currently crosses at Y=0, pushing quarter labels to top.
4. **2ADP001 G&A 5991** — data missing, must investigate API response.
5. **2ADP022** — all data missing, must investigate.

**Action items:**
- [ ] Fix chart: move legend from bottom → right (`chart.legend.position = "r"`)
- [ ] Fix chart: category axis stays at bottom when Y is negative (set `crosses = "min"` not `"autoZero"` in catAx XML)
- [ ] Investigate 2ADP001 G&A 5991 missing values (check API account name mapping)
- [ ] Investigate 2ADP022 missing all values (check if sequence exists in NetSuite / API returns data)
- [ ] Create v14 with all fixes, re-run all groups

**Script impact:**
- `chart.legend.position = "r"` in `_add_line_chart()`
- In `_patch_chart_axes()`: change `<crosses val="autoZero" />` → `<crosses val="min" />` in catAx replacement XML
- 2ADP001/2ADP022: investigate before coding fix

---

## April 28, 2026 — Deployment Planning Meeting

**Type:** Video meeting
**Participants:** Josh Grapani, Shoma Sinha, Atul Kumar

**Raw content / key quotes:**
> "Convert it in that [web app] because this is too much like — they will not know."

> "For running the script they will need to run it on a system... a local machine or a virtual server."

> "The shared folder — either it is from OneDrive or from Google Drive — those places are just for placing the files. They cannot run any application in it."

> "I will fix the remaining thing in the script and I will share the script with you with a deep and detailed documentation, how to set it up and run it."

> "For the charts — the quarter values are always on the zero line... if ever we can make it like this [reference image] — it's outside the grid, so it doesn't interfere with any values of the axis."

> "For the API of the report, can we have an authentication on that? There's no authentication on the API — maybe we can set it up?"

> "Go through NetSuite — don't kill yourself — I'm confident this plan is better."

> "Share the files on the shared folder instead of sending in the email."

**Key decisions made:**

1. **Deployment plan agreed:**
   - Atul puts BOTH scripts (console + web app) + documentation in the external shared folder (Jason Peabody's invite)
   - IT team at NextFlex decides where to actually host/run from — we give them everything they need
   - Script runs on local machine or virtual server; shared folder is just storage
   
2. **Web app confirmed:** Atul will convert the script to a web app (same pattern as contracting transformation app) — user selects project type, background job runs, live logs visible, download files when done.

3. **NetSuite File Cabinet:** Just file storage, cannot run Python. Atul to do quick check but consensus is it won't work. IT team meeting is the real path.

4. **API authentication:** Oracle API endpoints currently have zero authentication. Josh wants credentials added. Must be done at Oracle platform level, not in Python script. Follow-up meeting planned — Josh to give Atul access to Oracle platform.

5. **Chart — new remaining issue:** Quarter labels sit on the zero line inside the grid area. Josh wants them pushed outside/below the grid so they don't interfere with chart content. He showed a reference image where labels are cleanly outside the plot area. (This is separate from v14 fixes: legend→right, crosses=min.)

6. **2ADP022:** Atul confirmed transient API failure; new files will have correct values. Josh to review new files in shared folder.

7. **Files delivery:** From now on, share generated Excel files in the shared folder (not email).

8. **Shared folder access:** Atul received invite from Jason Peabody, accepted, created account. ✅

9. **NetSuite production access:** Josh gave Atul production access during the meeting. ✅

**Action items:**
- [ ] Atul: Fix chart — quarter labels pushed outside/below grid area (not on zero line)
- [ ] Atul: Build web app version of the script
- [ ] Atul: Upload v14 Excel files + both scripts + documentation to shared folder
- [ ] Atul: Explore NetSuite file cabinet for Python hosting (quick check, low priority)
- [ ] Josh: Schedule follow-up meeting on Oracle API authentication
- [ ] Josh: Give Atul access to Oracle platform for authentication work

**Script impact:**
- Chart: need to push catAx (X-axis / quarter labels) below the plot area — `tickLblPos` set to `"low"` in catAx XML patch. This keeps labels outside the grid regardless of Y-axis range.
- Web app: new Flask/FastAPI wrapper around existing script logic (background job, SSE log streaming, download endpoint)

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

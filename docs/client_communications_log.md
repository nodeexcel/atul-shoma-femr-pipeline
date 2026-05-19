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
| 2026-04-29 | Shoma Sinha | Handover request — script + docs to shared folder, Josh to cover NSAW upload | [→ Apr 29 Handover](#april-29-2026--shoma-sinha-handover-request) |
| 2026-04-29 | Atul + Josh | EWD014 confirmed, v15 chart approved, caching rejected, two separate handover docs needed | [→ Apr 29 Call](#april-29-2026--atul--josh-meeting-video-call) |
| 2026-04-29 | Josh + Atul | Oracle API authentication implemented — client ID + secret shared, access token verified | [→ Apr 29 Auth](#april-29-2026--oracle-api-authentication) |
| 2026-04-29/30 | Josh + Shoma | v15 review: Available Funds wrong on 28 ADP sequences (data timing issue), 2ADP061 G&A issue, files must go to NextFlex shared space | [→ Apr 29-30 Review](#april-2930-2026--josh-v15-file-review--available-funds-issues) |
| 2026-05-01 | Josh + Shoma + Atul | Meeting: v16 files uploaded to NextFlex shared folder; Shoma backup run request; transformation script changes (output-only Excel + CSV support) | [→ May 1 Meeting](#may-1-2026--joshatulshomaatulkumar-meeting) |
| 2026-05-01/02 | Shoma Sinha | IT team has spun up a server; needs prerequisites list from Atul; Monday 10:30 PST IT meeting, Tuesday script run meeting | [→ IT Server Setup](#may-12-2026--shoma-sinha-it-server-setup) |
| 2026-05-05 | IT Setup Meeting | Andy + Jason (IT), Atul, Shoma — Docker installed on Windows Server 2025, .env.prod created, setup complete, waiting on Taylor's confirmed data files | [→ May 5 IT Meeting](#may-5-2026--it-setup-meeting) |
| 2026-05-07 | Full team thread | Budgets uploaded by Jayaram; Taylor/Randy reviewed FEMR; 3 change requests; March actuals still uploading; GL code sorting change confirmed for script; NSAW access issue | [→ May 7 Team Thread](#may-7-2026--full-team-thread) |
| 2026-05-07 | Josh → Atul | Sample file sent (FEMR Dev_QA v051326.xlsx) — exact GL code labels, Labor Hours row removed, dollar sign formatting confirmed doable in script | [→ May 7 Josh Sample File](#may-7-2026--josh-sample-file--gl-codes) |
| 2026-05-07 | Josh → All | v18 review: remove $ from Remaining Cash; March data confirmed in NSAW ✅; Shoma: do UAT with NextFlex team after unit testing | [→ May 7 v18 Review Thread](#may-7-2026--v18-review-thread) |
| 2026-05-07 | Taylor → All | v18 UAT: 3 missing GL codes found (5007, 5098, 5099) — totals don't match NSAW P&L for 2ADP001 | [→ May 7 Taylor Missing GL Codes](#may-7-2026--taylor-missing-gl-codes) |
| 2026-05-07 | Josh + Shoma → Atul | Timeline discussion for GL code additions — Josh: 1 day NSAW; Shoma asks Atul for script estimate; full re-validation required after | [→ May 7 Timeline Discussion](#may-7-2026--timeline-discussion-gl-codes) |
| 2026-05-04 | Atul → Josh | v16 files sent with verification summary, 2ADP083 clarification request, 2ADP099 explanation | [→ May 4 v16 Message](#may-4-2026--atul--josh-v16-files-message) |
| 2026-05-04 | Josh → Atul | 2ADP083 = $0 confirmed (v16 correct); 2ADP099 — keep both tabs, filter by project # not sequence # | [→ May 4 Josh Reply](#may-4-2026--josh-reply-2adp083--2adp099) |
| 2026-05-04 | Shoma → Atul | Asking if all ADP files generating correctly, needs ADP data run | [→ May 4 Shoma ADP](#may-4-2026--shoma-adp-files-query) |
| 2026-05-04 | Josh + Atul | Quick call: 2ADP099 401 debug — no Oracle permissions issue, Atul to investigate on script side | [→ May 4 2ADP099 Debug Call](#may-4-2026--atul--josh-2adp099-debug-call) |
| 2026-05-19 | Atul + Josh | GL account API discovery: 5007/5098/5099 not in API → Josh done NSAW backend → re-discovery in progress | [→ May 19 GL Discovery](#may-19-2026--gl-account-api-discovery--josh-backend-complete) |
| 2026-05-04 | Josh → Atul | 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 — new budget uploads after v15, should now have values | [→ May 4 Josh 2ADP099 Call](#may-4-2026--post-meeting-thread) |
| 2026-05-04 | Shoma → Team | Taylor sending new files; Jayaram to upload; then re-run export; Atul to flag changes | [→ May 4 Josh 2ADP099 Call](#may-4-2026--post-meeting-thread) |

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

## April 29, 2026 — Shoma Sinha Handover Request

**Type:** Email (group thread)
**Participants:** Shoma Sinha, Josh Grapani, Atul Kumar

**Raw content (verbatim):**
> Hi Guys.
>
> @Atul Kumar Pls put the script in the external folder and put the documentation on how to connect the script and run it, so the output can be generated
> @Josh Grapani; pls create script on how excel file will be stored in external folder, script run and output generated which then needs to be upload in NSAW.
>
> Lets have the clean documentation as if we are handing the process.
>
> Regards
> Shoma

**Decisions made:**
1. **Atul's deliverables** — upload to external shared folder (Jason Peabody's):
   - `femr_netsuite_report_15.py` (active script)
   - `requirements_script.txt` (dependencies)
   - `docs/FEMR_SCRIPT_GUIDE.md` (setup + run documentation)
   - All 9 v15 output Excel files
2. **Josh's deliverables** — Josh to create a process script/doc covering:
   - How the Excel file gets stored in the external folder
   - How the script is run
   - How the output is uploaded to NSAW
3. **Goal:** Clean end-to-end handover documentation as if the process is being handed off permanently.
4. **NSAW** — output Excel files are uploaded to NSAW after generation. Josh owns this step.

**Action items:**
- [x] Atul: v15 script complete
- [x] Atul: FEMR_SCRIPT_GUIDE.md written
- [ ] Atul: Upload script + requirements_script.txt + FEMR_SCRIPT_GUIDE.md to shared folder
- [ ] Atul: Upload all 9 v15 Excel files to shared folder
- [ ] Josh: Write process doc for external folder → script run → NSAW upload

---

## April 29, 2026 — Atul + Josh Meeting (video call)

**Type:** Video call
**Participants:** Josh Grapani, Atul Kumar

**Key quotes (verbatim from transcript):**

> "You said EWD014 has no data, right? No financial data. If we filter, if we check on the previous years, the posting is on 2018. There are no postings after that. That's why it has no values in this one but has values on the cumulative going forward."

> "I saw the chart and it seems okay now Atul. This is what we want. Very nice."

> "How long or how much time do they need to generate the export files? Say, the whole projects."

> "When generating export files, because this is Diane's one question, can they select dates as well as ranges of sequence number? Like, for example, I only want ADP 001 to ADP 0010. Can they do that?"

> "But my view that the data is refreshing every day. When they go live, they will have postings on transactions. So, the actuals would have postings. Also, for the budgets, when they complete the budget files upload, it will also change. So, if you save the data locally... No, it will be a stale data."

> "On Shoma's email, when we do the documentation, I need the first part on your end, which is the transformation script for the contracting file. After that, I will do my part on the load on NSAW."

> "Will you prepare it separately? Two files? One for each script?"

> "Not this export script. Because it's all yours, the export script." [referring to the contracting transform script being a separate doc]

**Key decisions / findings:**

1. **EWD014 no financial data — CONFIRMED EXPECTED**: Last posting was 2018. No FY2020+ data. The main quarterly table is empty but cumulative section correctly shows historical values from pre-FY2020 data. Not a bug. ✅

2. **v15 chart — APPROVED by Josh**: "I saw the chart and it seems okay now. This is what we want. Very nice." Chart fixes in v15 are final. ✅

3. **Run time — communicated to Josh**: ADP ~8-9 hours, each other group ~1.5-2 hours. Josh noted this may be a question from NextFlex IT team.

4. **Sequence/date range selection — NOT YET IMPLEMENTED**: Diane (NextFlex) asked if users can select a date range or sequence range (e.g. ADP001–ADP010). Currently only group-level selection exists. Atul confirmed and committed to adding sequence-level selection as a future feature.

5. **Local data caching (v13) — REJECTED by Josh**: Atul proposed caching API data locally to avoid re-pulling. Josh rejected: data refreshes daily (actuals from transactions, budgets from uploads). A local cache would be stale. **Decision: always pull directly from API. v13 cache approach should NOT be promoted to production.**

6. **Two separate handover docs required**:
   - **Doc A (Atul):** Transformation script for the contracting file (the first/pipeline task — NOT the FEMR export script)
   - **Doc B (already done):** FEMR export script guide (`FEMR_SCRIPT_GUIDE.md`)
   - **Doc C (Josh):** NSAW upload process (Josh's part — after Atul's docs)
   - Josh will review both docs from Atul before adding his NSAW section

**Action items:**
- [x] Atul: Write handover doc for the contracting transformation script — `docs/FEMR_TRANSFORM_GUIDE.md` created 2026-04-29 ✅
- [ ] Atul: Upload femr_handover_v15.zip to shared folder
- [ ] Atul: Future feature — add sequence-level selection to the web app/script
- [ ] Josh: Write NSAW upload process doc after Atul's docs are sent

---

## April 29, 2026 — Oracle API Authentication

**Type:** Follow-up to April 28 meeting (recording started late)
**Participants:** Josh Grapani, Atul Kumar

**What happened:**
- Josh secured the Oracle APEX API endpoints (previously had zero authentication)
- Josh shared the client ID and client secret with Atul
- Atul tested credentials and successfully generated an access token ✅

**Status:** Authentication is working. Script needs to be updated to include OAuth token in API requests.

**Decisions made:**
1. Oracle APEX endpoints are now OAuth-secured — unauthenticated calls will fail going forward
2. Script must obtain an access token using client credentials (client ID + secret) before making API calls
3. Credentials are NOT to be hardcoded in the script — must be passed via environment variable or config

**Action items:**
- [x] Atul: Update script to v16 — add OAuth token fetch + Bearer token header on all API requests ✅
- [x] Atul: Add ORACLE_CLIENT_ID and ORACLE_SECRET_KEY to `.env.example` ✅
- [x] Atul: Test v16 single sequence — confirmed working (test_v16.xlsx generated 2026-04-29) ✅
- [x] Atul: Update `FEMR_SCRIPT_GUIDE.md` with credential setup instructions ✅
- [x] Atul: Update `FEMR_HANDOVER.md` with credential setup for Docker deployment ✅
- [ ] Atul: Add ORACLE_CLIENT_ID + ORACLE_SECRET_KEY to docker-compose.yml + docker-compose.prod.yml env sections
- [ ] Atul: Run all groups with v16 to generate fresh output files

**Script impact:**
- New function to fetch OAuth token (POST to token endpoint with client_id + client_secret)
- All API calls to `/femr/netamount/` and `/mv_femr_report/` need `Authorization: Bearer <token>` header
- Token likely has an expiry — may need refresh logic if a full run exceeds token lifetime

---

## April 29–30, 2026 — Josh v15 File Review + Available Funds Issues

**Type:** Email thread
**Participants:** Josh Grapani, Atul Kumar, Shoma Sinha

**Thread summary (verbatim key quotes):**

> Josh: "I've reviewed the files and found some issues on the values. Most of the issues came from the Available Funds field. Earlier this week, we changed the logic for the available funds and other fields that are involved in the calculation, especially for ADPs. After the change there are some errors on the logic but were corrected immediately after. Maybe during the generation of export files, the script still uses the dataset that was not updated; that is why we have so many discrepancies."

> Josh: "If you can pls re-generate the export file for these sequences and I will check it out again."

> Josh: "for 2ADP061, pls check the G&A 5991 Budgeted FYE 9/30/2026 columns. It should not have any values."

> Josh: "Thanks Atul. Can you pls put this into our Onedrive too?"

> Shoma: "Josh, Why are u hving all files in one drive? I hv given very clear instructions tat it should be nextflex shared space. Can we pls move everything to nextflex shared space; there is a reason why we all got access."

> Josh: "I dont have any access to that drive. Please let me have access." → "Apologies. I see the folder now."

> Atul: "Sure, I'll regenerate the files and check for the issues."

**Root cause of Available Funds discrepancies:**
Josh changed the NetSuite logic for Available Funds (and related calculation fields) earlier in the week. There were temporary errors in the logic that were corrected immediately after. The v15 run pulled data during or just after this transition — some sequences still show the old/incorrect values. **This is a data timing issue, not a script bug.** Re-running with v16 will pull the corrected data.

**Affected sequences — Josh's expected values:**

| Sequence | Expected Available Funds |
|----------|------------------------|
| 2ADP001 | $0 |
| 2ADP009 | $8,391.50 |
| 2ADP020 | -$0.37 |
| 2ADP033 | $44,301.42 |
| 2ADP035 | $0 |
| 2ADP054 | $0 |
| 2ADP057 | $0 |
| 2ADP058 | $140,847.00 |
| 2ADP059 | $0 |
| 2ADP061 | $0 (+ G&A 5991 Budgeted FYE 9/30/2026 must be blank) |
| 2ADP062 | $429,519.36 |
| 2ADP064 | $515,963.00 |
| 2ADP066 | $0 |
| 2ADP068 | $0 |
| 2ADP074 | $0 |
| 2ADP078 | $0.01 |
| 2ADP080 | $0 |
| 2ADP083 | $0 (listed twice — second entry shows $14,695.00, likely a typo — clarify with Josh) |
| 2ADP087 | $0 |
| 2ADP090 | $0 |
| 2ADP092 | $0 |
| 2ADP098 | $1,265,150.33 |
| 2ADP103 | $154,183.00 |
| 2ADP110 | $0 |
| 2ADP117 | $0 |
| 2ADP119 | $7,603,614.00 |
| 2ADP125 | $0 |
| 2ADP129 | $881,152.00 |

**Decisions made:**
1. **Available Funds discrepancies** — data timing issue (NetSuite logic was mid-correction during v15 run). Fix: re-run affected sequences with v16 to pull corrected data. Not a script bug.
2. **2ADP061 G&A 5991 Budgeted FYE 9/30/2026** — must be blank. Investigate why script is pulling values there.
3. **File delivery location** — Shoma confirmed: NextFlex shared space only (not OneDrive). Josh now has access.
4. **2ADP083 conflict** — Josh listed it twice with different values ($0 and $14,695.00). Need clarification.
5. **Authentication** — set up during call, v16 script now uses OAuth Bearer token.

**Action items:**
- [x] Atul: Re-run all groups with v16 — all 9 files generated and verified ✅
- [x] Atul: Verify Available Funds for all 27 sequences — all match Josh's expected values ✅
- [x] Atul: 2ADP061 G&A 5991 Budgeted FY2026 — already blank in v16 ✅
- [x] Atul: Reply sent to Josh with results + 2ADP083 clarification request + 2ADP099 explanation ✅
- [ ] Atul: Upload all files to NextFlex shared space once Josh confirms 2ADP083
- [ ] Josh: Confirm 2ADP083 correct value ($0 or $14,695.00)

---

## May 1, 2026 — Josh/Shoma/Atul Meeting

**Type:** Video meeting (details recalled by Atul — not recorded)
**Participants:** Josh Grapani, Shoma Sinha, Atul Kumar

**Key points discussed:**

1. **v16 files uploaded to NextFlex shared folder** — Atul shared v16 zip + script during the meeting. All 9 femr_v16_*.xlsx output files + femr_handover_v16.zip are now in the NextFlex shared space. ✅

2. **Shoma's backup run request** — Shoma asked Atul to run the script as a backup so output files are available before her client meeting. Atul confirmed this is already satisfied by the v16 run completed 2026-04-30. No re-run needed.

3. **Transformation script changes requested** (femr_transform.py):
   - **Remove input tabs from output Excel** — currently the output file carries all original sheets (FEMR Funds, SF270 CA2 Source Data, etc.) alongside the Output tab. New behavior: output Excel must contain ONLY the Output tab.
   - **Add CSV output support** — script should accept a `--format` parameter (`excel` or `csv`). When `csv` is selected, output is a plain CSV file with only the transformed data.
   - **Auto-derive output filename** — instead of requiring an explicit `--output` argument, the script should derive the output filename from the input filename: same name with `output_` prefix, extension changes to match format (`.xlsx` or `.csv`). Example: `2026.03 FEMR funds 033126 2025.xlsx` → `output_2026.03 FEMR funds 033126 2025.xlsx` (Excel) or `output_2026.03 FEMR funds 033126 2025.csv` (CSV).
   - Both Excel and CSV outputs must contain ONLY the output/transformed data — no input tabs, no extra sheets.

**Decisions made:**
1. Upload of v16 files to NextFlex shared space is complete. ✅
2. Shoma's backup request is satisfied by yesterday's v16 files. No re-run.
3. Transformation script to be updated with output-only mode + CSV support + auto-derived filename.

**Action items:**
- [x] Atul: Upload v16 files to NextFlex shared folder ✅
- [x] Atul: Create femr_transform_2.py — strip input tabs, add --format excel/csv, auto-derive output filename ✅ 2026-05-03
- [x] Atul: Update web app transform pipeline (services, forms, model, views, template, migration) ✅ 2026-05-03
- [ ] Atul: Rebuild femr_transform_handover.zip with femr_transform_2.py + updated FEMR_TRANSFORM_GUIDE.md

---

## May 1/2, 2026 — Shoma Sinha IT Server Setup

**Type:** Email thread
**Participants:** Shoma Sinha, Atul Kumar, Josh Grapani

**Raw content (verbatim):**

> Hi Atul,
>
> I spoke to the IT team, they have spinned off a server for us so we can run the same there. But they need assistance as they have never done this before –
>
> We would need to tell them what is the pre requisite they need to bring up before running the script. Could you please send an email to that.
> Also, will have a meeting with the IT team on Monday to discuss this at 10.30 am pst – pls be available & Josh u too
> Once they have all this infrastructure we need- then we can have another meeting on Tuesday to get the script running – we will help them so you and Josh will need to be present.
>
> Regards
> Shoma

> Hi @Shoma Sinha, @Josh Grapani
> Sure, I'll send an email listing all the requisites for the setup.
> Regards
> Atul

**Decisions made:**
1. **Server confirmed** — NextFlex IT team has spun up a dedicated server for running the FEMR export script.
2. **Prerequisites email** — Atul to send IT team an email listing everything they need to set up before the script can run.
3. **Monday meeting (2026-05-05, 10:30 AM PST)** — Atul + Josh to meet with IT team to walk through setup.
4. **Tuesday meeting (2026-05-06)** — Atul + Josh to attend script run meeting with IT team once infrastructure is ready.

**Action items:**
- [ ] Atul: Send prerequisites email to IT team (Python version, packages, credentials, folder structure, internet access, disk space, run time expectations)
- [ ] Atul + Josh: Attend Monday 2026-05-05 10:30 AM PST IT setup meeting
- [ ] Atul + Josh: Attend Tuesday 2026-05-06 script run meeting

---

## May 4, 2026 — Josh Reply: 2ADP083 + 2ADP099

**Type:** Email reply
**Participants:** Josh Grapani → Atul Kumar, Shoma Sinha

**Raw content (verbatim):**

> Hi Atul,
>
> For sequence 2ADP083 - the correct value for available funds is $0, which is the same as v16.
>
> As for 2ADP099, the report shows values in the FEMR, and I think they will not change the sequence number for that rollup and orphan. They said it was okay to have the same sequence because they will filter by project # if a rollup and orphan have the same sequence #, so I think we should do the same.
>
> Regards,
> Josh

**Decisions made:**

1. **2ADP083** — correct Available Funds is **$0**. v16 value matches. **FULLY RESOLVED ✅**

2. **2ADP099** — two findings:
   - NetSuite team will NOT change the sequence number — both Rollup 1099 and Orphan Core099 keep sequence 2ADP099
   - The FEMR report does show values for this sequence (data exists in NetSuite)
   - Josh wants the script to filter by **project #** (not sequence #) when a rollup and orphan share the same sequence number — this is how NetSuite itself handles it
   - **Root issue:** R1099 tab is empty in v16 because the Oracle API returns 401 for Rollup 1099 identifier — this needs to be fixed at the Oracle API access level (Josh/Taylor to grant API access for Rollup 1099)
   - **Script change needed:** confirm the script already uses project # for filtering in multi-identifier sequences, and that 2ADP099 produces 2 tabs correctly once API access is fixed

**Action items:**
- [x] 2ADP083 confirmed $0 — v16 is correct, no changes needed ✅
- [ ] 2ADP099: ask Josh/Taylor to fix Oracle API access for Rollup 1099 (currently returning 401)
- [ ] 2ADP099: verify script uses project # filtering for multi-identifier sequences (confirm existing behavior)
- [ ] Once API access fixed for R1099: re-run 2ADP099 and verify both tabs have data

---

## May 4, 2026 — Atul + Josh 2ADP099 Debug Call

**Type:** Video call (transcription provided)
**Participants:** Josh Grapani, Atul Kumar

**Key quotes (verbatim):**

> Josh: "We only put the authorization on the database object. There's nothing, there's no authentication on that specific rollup or project."

> Josh: "Yeah, you can see this Atul. I can fetch. If I can see data here, it means that we can fetch, right?"

> Josh: "It's the same 588627." [project number Josh was viewing]

> Josh: "Taylor has nothing to do on the Oracle API. If we ask her, she doesn't know anything about that."

> Josh: "Maybe if they can assign another rollup [sequence number] for that, it would make our life easier."

> Atul: "I will first check on my side and give me some time. And if I'm still getting that error, I will let you know and then we can have another number assigned to it."

> Josh: "I thought you were running on sequence and rollup, right Atul?" → Atul: "Yeah."

> Josh: "They said, no, it's not a problem. We will filter if they have the same sequence, we will filter on the project number to break the tie. So I think they're set on that and we have to work on our side to fix this issue."

**Decisions / findings:**

1. **Oracle API has NO per-rollup permissions** — authorization is set at the database object level only. The 401 is NOT an Oracle permissions problem. Root cause must be on the script side.
2. **Josh can see data for the sequence** — project # 588627 has data visible in the FEMR report. Data exists.
3. **Taylor is not involved** — Oracle API is not her domain.
4. **Fallback option** — if Atul cannot fix the 401, Josh can request a different/unique sequence number for Rollup 1099 from the NetSuite team.
5. **Script runs on sequence + rollup** — confirmed. NetSuite team will filter by project # to break ties on shared sequence numbers — they are not changing the sequence.
6. **Atul to investigate the 401 on the script side** — Josh waiting for findings.

**Action items:**
- [x] Atul: Root cause found and fixed in v17 ✅ (see below)
- [ ] Atul: Report findings to Josh once ADP v17 run completes and 2ADP099 is verified

**Root cause found (2026-05-05):**
`_fetch_mv_by_identifier()` in v16 was missing the OAuth `Authorization: Bearer` header. Multi-identifier sequences use the MV endpoint path — which also requires auth — but the header was only added to `_http_get()` and `_fetch_netamount()`. 2ADP099 is the only remaining multi-identifier sequence, so it was the only one hitting this bug.

**Fix:** v17 adds `_get_auth_header()` to the MV request. Test confirmed: both `2ADP099 R1099` and `2ADP099 RCore099` tabs now have data. Full ADP run with v17 started on server 2026-05-05 ~07:58 UTC.

---

## May 7, 2026 — Timeline Discussion: GL Codes

**Type:** Email thread (separate from Taylor thread)
**Participants:** Josh Grapani, Shoma Sinha, Atul Kumar

**Josh (verbatim):**
> "Can we talk first before giving them time frame for the additional GL accounts? On my side, it would take a day to add this including some tests and validation."
> "@Atul Kumar - how long do you think you need to add such GL accounts?"
> "Also, we need to cross check and validate again all the sequences after the modifications if the NSAW Report is the same as the export files."

**Shoma (verbatim):**
> "Yep let's estimate — NSAW development n testing - 8 hrs. Atul script development n testing - [awaiting Atul's input]. Then u communicate."

**Josh estimate:** 1 day (8 hrs) for NSAW backend changes + testing
**Atul estimate needed:** script changes + single sequence test + full re-run validation

**Script change scope for Atul:**
- Find Oracle API account name strings for 5007, 5098, 5099: ~30 min
- Code changes (add 3 rows, update 8 row constants): ~30 min
- Single sequence test: ~2 hours (API calls)
- Full re-run all groups + cross-validate vs NSAW: ~1 additional day

**Atul realistic estimate: 1 day script + test; full cross-validation 1 additional day after Josh's NSAW changes**

**Atul's estimate (replied):**
- Script changes + single sequence test: ~1 day
- Full re-run + cross-validation: ~1 additional day (after Josh's NSAW changes)
- Total: 2 days, second day blocked on Josh completing NSAW side first

**Atul's reply to Josh (verbatim):**
> "For the script side:
> - Script changes + single sequence test: ~1 day (finding the API account strings, adding the 3 GL codes, updating the layout, testing with one sequence)
> - Full re-run all groups + cross-validation vs NSAW: ~1 additional day after Josh's NSAW changes are done
> So total on my end: 2 days, but the second day is dependent on Josh completing his NSAW backend changes first, so both sides are in sync before we validate.
> Happy to sync on a timeline once Josh has a date for the NSAW changes."

**Action items:**
- [x] Atul: Replied with timeline estimate ✅
- [x] Josh: Complete NSAW backend changes ✅ (confirmed 2026-05-19 — see GL Account API Discovery section below)
- [ ] Josh + Shoma: Align on timeline before communicating to Taylor
- [ ] Atul: Add 3 GL codes to v18, update row constants, re-test (unblocked — Josh done)
- [ ] Both: Full cross-validation after changes on both sides

---

## May 7, 2026 — Taylor Missing GL Codes

**Type:** Email (Taylor → Josh, Shoma, Atul, full team)
**Reference file:** `CA2 ADP 1 NS Project PnL UT.xlsx` (NSAW P&L for 2ADP001)

**Taylor (verbatim):**
> "It looks like we are missing some 5000s GL codes that apply to the older ADPs. Could you please add the following to the FEMR?
> 5007    DNU-Direct Supplies
> 5098    DNU Direct Accruals Gov
> 5099    DNU-Other Direct Costs
> The totals don't appear to match, due to these missing GL codes."

**Analysis of Taylor's P&L file (CA2 ADP 1 NS Project PnL UT.xlsx):**
- 2ADP001 (Rollup 1001) P&L across 10 sub-projects
- GL codes present in NSAW P&L but missing from FEMR script:
  - **5007 DNU - Direct Supplies:** $3,008.27 Grand Total
  - **5099 DNU - Other Direct Costs:** $23,007.46 Grand Total
  - **5098 DNU Direct Accruals Gov:** not in 2ADP001 P&L but Taylor says it applies to other older ADPs
- Accounts match FEMR script: 5001, 5002, 5003, 5005, 5008, 5009, 5990, 5991, 5992 ✅

**Decisions needed:**
1. Add 5007, 5098, 5099 to `ACTUALS_BUDGET_ACCOUNTS` in v18
2. Need exact Oracle API account name strings for these 3 codes (query API or ask Josh)
3. Row layout shifts again — 12 accounts → 15, all row constants shift down by 3

**Follow-up exchanges:**

Josh (verbatim):
> "These accounts are not in the original FEMR template. If we are to add GL accounts, could you please give us the complete list of accounts? Do we also add accounts 5501 and 5506?"

Taylor (verbatim):
> "What is the estimated time for you and your team to modify the backend and the scripts to include 5007, 5098, and 5099? These GL codes are more critical to include, as they ensure the FEMR accurately reflects direct cost actuals. I no longer think we need to add in the 5501 and 5506 since they relate to cost share and we are not tracking that in the FEMR."

Josh (verbatim):
> "I would ask the team and update you."

**Decisions confirmed:**
1. Only add **5007, 5098, 5099** — confirmed by Taylor as critical for direct cost actuals
2. **5501 and 5506 NOT needed** — cost share accounts, not tracked in FEMR
3. Josh is checking timeline with Atul — Atul needs to provide estimate

**Action items:**
- [ ] Atul: Reply with timeline estimate for adding 5007, 5098, 5099 to script
- [ ] Atul: Find exact Oracle API account name strings for 5007, 5098, 5099
- [ ] Atul: Add 3 GL codes to v18, update row constants (12→15 rows), re-test
- [ ] Josh: Update NSAW backend to add these accounts on his side

---

## May 19, 2026 — GL Account API Discovery + Josh Backend Complete

**Type:** Email thread continuation + technical discovery
**Participants:** Atul Kumar, Josh Grapani, Shoma Sinha

**Atul's API discovery message to Josh (verbatim):**
> "Quick update on the 5007, 5098, and 5099 accounts — I ran a test against the Oracle API to discover these account name strings before adding them to the script.
> The API does not return these three accounts at all for 2ADP001, even though they show values in the NSAW P&L. This means they are not currently exposed in the mv_femr_report view that the script reads from.
> So the sequence needs to be:
> 1. Josh adds 5007, 5098, 5099 to the NSAW MV report on his side first
> 2. Once they appear in the API, I re-run my discovery script to get the exact account name strings
> 3. I then add them to the export script
> On my side I'm ready to go as soon as the accounts are visible in the API. Happy to coordinate timing."

**Josh's reply (verbatim):**
> "Hi Atul, I've done the changes on the backend, pls try on your side. Here is a sample export of the updated table."
> [Josh attached a sample export file showing the updated table]

**Atul's acknowledgment (verbatim):**
> "Hi @Josh Grapani, Okay, I'll check it out and verify it on my end."

**Status:** Josh's NSAW backend changes are complete as of 2026-05-19. Re-running discovery script now to get exact API account_name strings for 5007, 5098, 5099.

**Action items:**
- [x] Josh: NSAW backend changes complete ✅
- [ ] Atul: Re-run `scripts/test_discover_gl_accounts.py` to get exact account_name strings
- [ ] Atul: Add 5007, 5098, 5099 to `ACTUALS_BUDGET_ACCOUNTS` in v18, update row constants (12→15 rows, all constants below actuals shift +3)
- [ ] Atul: Test with `--sequence 2ADP001 --skip-preload`, verify 3 new rows appear with correct values
- [ ] Both: Full re-run all groups + cross-validate vs NSAW P&L

---

## May 7, 2026 — v18 Review Thread

**Type:** Email thread
**Participants:** Josh Grapani, Shoma Sinha, Jayaram P, Atul Kumar

**Josh on v18 test file (verbatim):**
> "@Atul Kumar - The remaining cash values have a $ sign, can we remove that also?"
> "@Shoma Sinha - should we ask nextflex team for approval for this export file?"
> "@Jayaram P - can I ask for some of the projects that are included in the newest upload for March?"

**Jayaram — March upload project list (sample):**
713061, 713063, 713104, 713105, 713107, 713108, 713110, 716006, 716082, 716094, 716114, 716122, 716140, 716141, 716145, 716146, 716159, 716160

**Jayaram — March Projects file (`March Projects.xlsx`):**
- 554 posting rows across 136 unique projects
- Columns: Project External ID, Amount (Debit), Amount (Credit)
- Total Debit: $3,880,247.02 | Total Credit: $3,889,877.81
- File saved at: `/home/lap-68/Downloads/March Projects.xlsx`

**Jayaram — March Trial Balance file (`Import TB_March_2026.csv`):**
- Batch ID: 2603-TB03, Date: 3/31/2026
- 777 rows across 111 unique accounts
- Key FEMR GL accounts confirmed in upload:
  - 5001 Labor Cost: $420,852 debit
  - 5002 Consulting: $2,813 debit
  - 5003 Material: $38,969 debit
  - 5004 Travel: $4,611 debit
  - 5005 Subcontracting: $1,753,320 debit
  - 5009 Other Direct Costs: $3,440 debit
  - 5010 Equipment: $1,080 debit
  - 5990 Fringe: $229,317 debit
  - 5991 G&A: $948,389 debit
  - 5992 Sub K Overhead: $53,126 debit
- Josh confirmed batch 2603-TB03 is reflected in NSAW ✅
- File saved at: `/home/lap-68/Downloads/Import TB_March_2026.csv`

**Josh confirmed March data in NSAW (verbatim):**
> "By spot checking, I've confirmed that the March uploads (2603-TB03) are reflected in the FEMR report now."

**Shoma's decision (verbatim):**
> "Yes Josh — if we have completed our unit testing; then pls do so that they can do UAT as well."

**Atul replied:**
> "I'll look into it and try to remove the remaining $ sign."

**Decisions made:**
1. **Remaining Cash $ — remove it** — `_write_remaining_cash_row` still uses `NUM_FMT` (with $). Fix: change to `NUM_FMT_NO_DOLLAR`. Atul confirmed will fix.
2. **March data — CONFIRMED READY ✅** — Josh spot-checked, March uploads (2603-TB03) reflected in NSAW. Data is ready for full run.
3. **Next step after unit testing** — Shoma wants to share with NextFlex team for UAT (User Acceptance Testing) once Atul's unit testing is complete.

**Action items:**
- [x] Atul: Fix Remaining Cash $ in v18 ✅ — `_write_remaining_cash_row` + Grand Total of all data rows now use `NUM_FMT_NO_DOLLAR`
- [x] Atul: Re-tested v18 — all formats verified ✅
- [ ] Atul: Share updated test_v18.xlsx with Josh for sign-off
- [ ] After Josh approves: run full report all groups with v18
- [ ] After full run verified: share with NextFlex team for UAT

---

## May 7, 2026 — Josh Sample File + GL Codes

**Type:** Email (Josh → Atul, Shoma)
**File shared:** `FEMR Dev_QA v051326.xlsx`

**Raw content (verbatim):**
> Hi Atul, Here is a sample file for your reference with the sorting and new account names. Also, I think we can cater to their request on the dollar sign formatting in the export script.

**Confirmed changes for v18 (from sample file analysis):**

1. **GL code labels — exact format confirmed:**
   - `5001 Labor Cost`
   - `5002 Consulting`
   - `5003 Material`
   - `5004 Travel`
   - `5005 Subcontracting`
   - `5008 Equipment`
   - `5009 Other Direct Costs`
   - `5010 Equipment`
   - `5990 Fringe`
   - `5991 G&A`
   - `5992 Sub K Overhead`
   - `5993 Sub K Overhead`

2. **Labor Hours row REMOVED** — 12 data rows instead of 13. All subsequent row positions shift up by 1.

3. **Dollar sign formatting** — Josh confirms this can be done in the script. Taylor wants `$` only on total rows (ACTUALS Total, BUDGETED Total), not on individual data rows.

4. **NSAW access** — Josh replied separately: Taylor lost access temporarily due to changes being made. Josh re-shared access.

**Josh clarification on dollar sign (verbatim):**
> "Dollar signs also on the Grand Total Column."

**Dollar sign rule confirmed so far:**
- Individual data rows (Actuals/Budgeted): no $
- ACTUALS Total row: $ ✅
- BUDGETED Total row: $ ✅
- Grand Total column (last column): $ ✅
- Grand Total column already exists in script as =SUM() formula ✅

**Josh reply (verbatim):**
> "I am not sure about that, but the original FEMR template has dollar signs on the cumulative pivot table. Let's keep it as is for now."

**Final dollar sign rule — CONFIRMED:**
- Actuals/Budgeted individual data rows: **no $**
- ACTUALS Total row: $ ✅
- BUDGETED Total row: $ ✅
- Grand Total column: $ ✅
- Contracting rows (Committed, Obligated, Expended, Remaining Cash): **keep $ as-is**
- Cumulative section: **keep $ as-is**

**Action items:**
- [ ] Atul: Build v18 — GL code labels, Labor Hours removed, $ on total rows + Grand Total column, row layout updated
- [ ] Atul: Test v18 with a single sequence, share with Josh for review before full run

---

## May 7, 2026 — Full Team Thread

**Type:** Email thread (post 3-hour meeting, Atul not available)
**Participants:** Shoma Sinha, Josh Grapani, Taylor Bui, Randy Lu, Prathima Murthy, Marirose Landicho-Rasay, Diane Baxster (OOO), Jayaram P, Atul Kumar

**Summary of thread:**

**Budget upload:**
- Jayaram uploaded budgets to NetSuite Budget tab the previous evening
- Shoma asked Josh to spot check these project numbers: 713079 ($770,000.32), 713101 ($130,000.00), 713109 ($50,000.00), 716084 ($1,167,165.06), 716114 ($42,160.00), 716115 ($15,188,134.00)

**Taylor + Randy reviewed FEMR report in NSAW and raised 3 change requests:**

> 1. "For the Expense Type column, could we reformat it to list the GL code first, followed by the expense type, and then sort it in numerical order? Example: 5001 Labor Cost / 5002 Consulting / 5003 Materials"
> 2. "Please remove the Contracting Total row, as we don't need this row and it was not included in the original FEMR for the NetSuite template."
> 3. "Could we update the format so there is no dollar sign in front of individual amounts, and only include the '$' symbol for total rows and columns?"

**Josh's responses on each request:**
1. **GL code sorting** — "We can do the change for GL codes and sorting right now in NSAW but it will not be reflected immediately on the export files because we also need to modify the export script." → Josh has already updated NSAW sorting ✅. **Script change required from Atul.**
2. **Contracting Total row** — NSAW system limitation. Removing it would also remove Actuals and Budgets total rows. In the export files it's already designed to not show like in the sample template. **No change needed in script.**
3. **Dollar sign formatting** — NSAW system limitation. Changing currency field to numeric affects grand total. **No change in script.**

**Data status:**
- Taylor confirmed: actuals aligned with QBO through February 2026 ✅
- Budgets for ADPs extending beyond 9/30/2026 — full budget not showing, Taylor says that's okay ✅
- **March actuals: NOT ready** — Randy and Prathima still uploading March into NetSuite
- Diane Baxster is OOO — hasn't been consulted on GL codes yet

**Shoma's decisions:**
> "FEMR report is incomplete till it can be available from the script. Any change that is needed to be made has to be communicated to Atul and then once we tested and its fine — we can say that FEMR is now available."

- Do NOT run the full report yet — wait for March actuals to finish uploading
- In the meantime: implement GL code sorting change in the script
- After change is done and data is ready: test run a few sequences, then full run

**NSAW access issue:**
- Taylor lost access to FEMR report in NSAW — Josh re-shared
- Later: Taylor and Randy both can't view it again — Shoma asking Josh why
- Root cause unknown — Josh to investigate

**Also happened in May 7 meeting (Atul):**
- v17 script uploaded to NextFlex shared folder before the demo ✅
- Demo given showing how to run the script directly via Python
- Web app via Docker is NOT working on the Windows Server — root cause: nested Hyper-V virtualization not supported on the VM. Docker Desktop requires WSL2 which requires nested virtualization. Script-only method is the working path for now.

**Action items:**
- [x] Atul: Upload v17 to NextFlex shared folder ✅
- [ ] Atul: Modify export script — reformat Expense Type/account rows to show GL code first, then description, sorted numerically (e.g. "5001 Labor Cost") → this will be **v18**
- [ ] Atul: Wait for March actuals to finish uploading before running full report
- [ ] Josh: Fix NSAW access for Taylor and Randy
- [ ] Josh: Confirm GL code format in NSAW so script matches exactly
- [ ] Diane: Consult on GL codes (when back from OOO)
- [ ] Randy + Prathima: Finish uploading March actuals into NetSuite
- [ ] After GL code change + March actuals ready: test run a few sequences, verify, then full run

---

## May 5, 2026 — IT Setup Meeting

**Type:** Video meeting (transcription provided)
**Participants:** Andy, Jason (IT team), Atul Kumar, Shoma Sinha

**Key findings:**

1. **Server OS:** Windows Server 2025
2. **IT team leads:** Andy and Jason (Jason Peabody — same person who shared the external folder)
3. **Python:** Already installed — Python 3.14
4. **Docker issue:** Docker Desktop failed to install initially despite admin/elevated privileges. Error: "for security reasons must be owned by elevated account." Fix: deleted the ProgramData/Docker folder and re-ran the full installer with elevation — installed successfully.
5. **WSL:** Already installed, just needed updating to latest version.
6. **App explained by Atul:** Two methods — (1) direct Python/terminal, (2) web app via Docker. Docker method preferred — all services bundled, just run two commands and open browser.
7. **Web app zip found:** IT team located `femr_webapp_handover.zip` in NextFlex shared folder (FEMR folder).
8. **.env.prod created:** Atul walked Jason through creating the file on the server desktop (under user `jpbody`). File was created as .txt first, then renamed to remove extension. Atul sent the env contents in the meeting chat.
9. **Decision NOT to run yet:** Shoma said to wait for Taylor's confirmed final data files before running — don't want incorrect data going to government.
10. **Setup is complete** — Docker installed, .env.prod created, zip extracted on server desktop. Just need to rename the .env file correctly and run two commands.

**Decisions made:**
1. Web app setup on Windows Server 2025 is complete — ready to run once data is confirmed.
2. Preferred method: Docker web app (not direct Python script).
3. Do NOT run the script until Taylor confirms the final data files.
4. Shoma to chase Taylor for confirmed final data. Run will happen Tuesday or Wednesday depending on when clean data arrives.

**Action items:**
- [ ] Shoma: Chase Taylor to confirm final GROUP MAPPING / data files
- [ ] IT team: Rename .env file to remove .txt extension (if not already done)
- [ ] Atul + IT team + Josh: Meet again once Taylor confirms data — run two Docker commands to start the app
- [ ] Run scheduled: Tuesday 2026-05-06 or Wednesday 2026-05-07 depending on Taylor's confirmation

---

## May 4, 2026 — Post-Meeting Thread (Josh + Shoma)

**Type:** Email thread (post-IT meeting)
**Participants:** Josh Grapani, Shoma Sinha, Atul Kumar

**Email 1 — Josh on 2ADP099 (verbatim):**
> Hi Atul, Can we have a quick talk regarding 2ADP099 to check the error? Because I don't think we have set any permissions for a specific project or rollup. We set a permission for the whole dataset.

**Email 2 — Josh on 2ADP061 (verbatim):**
> Hi Atul, Regarding, 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 values, as of now, there are new budget uploads after the v15, and they should have values now.

**Email 3 — Shoma on new files (verbatim):**
> Ok Guys, Taylor will be sending us new files; so Jayaram will upload them and then we can run these. So yes- you will send me changes in the files.

**Decisions / findings:**

1. **2ADP099 — 401 root cause unknown:** Josh says permissions are set at the whole dataset level — no per-rollup or per-project restrictions exist. So the 401 on Rollup 1099 is NOT a known permissions issue. Need a quick call with Josh to debug the actual cause. Could be a data issue with the Rollup 1099 identifier in Oracle/NetSuite itself.

2. **2ADP061 G&A 5991 Budgeted FYE 9/30/2026 — NOW HAS VALUES:** New budget uploads were done after v15. This field should no longer be blank — the next re-run will pull the new budget values. Previously confirmed blank in v16 but that was before the new upload.

3. **Taylor sending new GROUP MAPPING / data files:** Jayaram (NextFlex) will upload them to the system. After upload, Atul runs the export. Atul to flag what changed between the new output and v16.

**Action items:**
- [ ] Atul: Schedule quick call with Josh to debug 2ADP099 401 error
- [ ] Atul: Wait for Taylor's new files — Jayaram uploads them
- [ ] Atul: After new files uploaded, re-run all groups with v16
- [ ] Atul: Flag changes in new output vs v16 to Shoma
- [ ] Note: 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 will have values in next run — this is expected, NOT a bug

---

## May 4, 2026 — Shoma ADP Files Query

**Type:** Email
**Participants:** Shoma Sinha → Atul Kumar, Josh Grapani

**Raw content:**
> Hi Guys, So we will need to run ADP data; are all the files generating correctly.

**Context:** Shoma asking about ADP file status after the v16 run and Josh's verification email.

**Status at time of query:**
- All 5 ADP files generated in v16 ✅ (247 tabs total)
- All 27 Available Funds values verified to the cent ✅
- 2ADP083 = $0 confirmed by Josh ✅
- 2ADP099: 2 tabs generated (R1099 empty due to Oracle API 401, Core099 correct) — pending Oracle fix

**Action items:**
- [ ] Atul: Reply to Shoma confirming ADP files are ready with one known exception (2ADP099 R1099)

---

## May 4, 2026 — Atul → Josh v16 Files Message

**Type:** Email (files already sent, message drafted)
**Participants:** Atul Kumar → Josh Grapani

**Message sent with v16 files:**

Key points covered:
1. Available Funds verified — all 27 sequences from Josh's list match expected values to the cent ✅
2. 2ADP061 G&A 5991 Budgeted FYE 9/30/2026 — confirmed blank ✅
3. Authentication complete — v16 uses OAuth Bearer token on all API calls ✅
4. **2ADP083 open question** — Josh listed it twice ($0 and $14,695.00), asked Josh to confirm correct value
5. **2ADP099 explained** — 2 tabs generated (R1099 + RCore099), both empty due to 401s on invalid Rollup 1099; awaiting Taylor's NetSuite cleanup

**Action items:**
- [ ] Josh: Confirm 2ADP083 correct Available Funds value ($0 or $14,695.00)
- [ ] Taylor: Clean up Rollup 1099 in NetSuite (2ADP099)

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

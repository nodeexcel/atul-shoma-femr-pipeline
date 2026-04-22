# Sequence/Rollup Data Issue — Email Thread (April 2026)

**Participants:** Josh Grapani, Taylor Bui, Shoma Sinha, Atul Kumar, Jayaram P, Diane Baxster, Marirose Landicho-Rasay, Randy Lu

## Summary

Josh identified that some sequences have both a Rollup and an Orphan project sharing the same sequence number in the FEMR report. Examples:
- **CC007**: Rollup 4006 + Orphan 960011
- **2ADP099**: Rollup 1099 + Orphan Core099

## Taylor's Response

> "We recently added new roll-up (parent) projects that converted several orphan projects into child projects, and at the same time we updated the sequence format to remove alphabetic characters for simplicity."

> "Regarding Sequence 2ADP099, apologies for the confusion, there should not be a roll-up project 1099. Core099 is an orphan project and is not part of a roll-up."

## Key Decisions

1. **2ADP099 Rollup 1099 is invalid** — only Core099 (orphan) is the real project
2. **Root cause**: NetSuite data migration (new rollup parents + sequence format change) created inconsistencies
3. **Meeting scheduled**: Josh + Taylor for Tuesday 2026-04-22 to walk through the impact on FEMR report

## Impact on Script

- v7 already handles multi-identifier sequences correctly (separate tabs per rollup/orphan)
- Once Taylor fixes the data, 2ADP099 will have only one identifier and generate one tab
- May receive updated GROUP MAPPING file after the Tuesday meeting

*Saved: April 16, 2026*

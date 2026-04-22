# FEMR Report — Run Commands Reference

**Current active script: v9** (`femr_netsuite_report_9.py`)

| Version | File | Status |
|---------|------|--------|
| v9 | `femr_netsuite_report_9.py` | **Active** — dynamic quarter range (auto-detects latest quarter from MV) |
| v8 | `femr_netsuite_report_8.py` | Superseded |
| v7 | `femr_netsuite_report_7.py` | Used for WFD/Internal/Comml/OGA sent to Josh |
| v5/v6 | older | Archived |

---

## V9 — Current Version

```bash
# Single sequence test
venv/shoma/bin/python -u scripts/femr_netsuite_report_9.py --sequence 2ADP001 -o test_v9_2ADP001.xlsx

# Single group
venv/shoma/bin/python -u scripts/femr_netsuite_report_9.py --group WFD -o femr_v9_wfd --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_9.py --group OGA -o femr_v9_oga --workers 40
venv/shoma/bin/python -u scripts/femr_netsuite_report_9.py --group ADP -o femr_v9_adp --workers 40

# Overnight (all groups)
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_9.py -o femr_v9 --workers 40 > /tmp/v9_full.log 2>&1 &

# Manual override if auto-detect is slow (saves ~1 min at startup)
venv/shoma/bin/python -u scripts/femr_netsuite_report_9.py --group ADP -o femr_v9_adp --fy-end 2026 --latest-quarter Q4
```

**Wait for Taylor's updated GROUP MAPPING (post 2026-04-22 meeting) before running WFD/OGA/ADP.**

---

---

## V5 — Single Reporting Group (parallel-safe output names)

### Sequential (recommended — full API bandwidth per process)

```bash
# ADP only (~247 sequences) — biggest, ~6 hours
venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group ADP --output femr_v5_adp --workers 40

# Comml only (~41 sequences) — ~1 hour
venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group Comml --output femr_v5_comml --workers 40

# Internal only (~37 sequences) — ~55 min
venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group Internal --output femr_v5_internal --workers 40

# OGA only (~48 sequences) — ~1.2 hours
venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group OGA --output femr_v5_oga --workers 40

# WFD only (~27 sequences) — ~40 min
venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group WFD --output femr_v5_wfd --workers 40
```

Output files: `femr_v5_adp_adp.xlsx`, `femr_v5_comml_comml.xlsx`, etc.
(script appends group name as suffix — suffix comes from the reporting group value in the mapping file)

### Parallel (background, with separate logs)

Drop workers to 20 each to avoid API rate limits when running in parallel:

```bash
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group Comml    --output femr_v5_comml    --workers 20 > /tmp/v5_comml.log 2>&1 &
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group Internal --output femr_v5_internal --workers 20 > /tmp/v5_internal.log 2>&1 &
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group OGA      --output femr_v5_oga      --workers 20 > /tmp/v5_oga.log 2>&1 &
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --group WFD      --output femr_v5_wfd      --workers 20 > /tmp/v5_wfd.log 2>&1 &
```

**Note:** Parallel doesn't actually speed things up — the API is bandwidth-limited. Sequential at 40 workers is faster overall. Only use parallel if you need small groups to start immediately.

### Full run (all 398 sequences)

```bash
# Overnight run — ~9-10 hours
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_5.py --output femr_v5 --workers 40 > /tmp/v5_full.log 2>&1 &
```

---

## V6 — Bulk Preload Version (faster for groups >50 sequences)

### Sequential

```bash
# ADP only — ~5.5 hours (saves ~30 min vs v5)
venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group ADP --output femr_v6_adp --workers 40

# Comml only — ~1 hour
venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group Comml --output femr_v6_comml --workers 40

# Internal only — ~55 min
venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group Internal --output femr_v6_internal --workers 40

# OGA only — ~1.2 hours
venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group OGA --output femr_v6_oga --workers 40

# WFD only — ~40 min
venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group WFD --output femr_v6_wfd --workers 40
```

### Parallel

```bash
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group Comml    --output femr_v6_comml    --workers 20 > /tmp/v6_comml.log 2>&1 &
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group Internal --output femr_v6_internal --workers 20 > /tmp/v6_internal.log 2>&1 &
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group OGA      --output femr_v6_oga      --workers 20 > /tmp/v6_oga.log 2>&1 &
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --group WFD      --output femr_v6_wfd      --workers 20 > /tmp/v6_wfd.log 2>&1 &
```

### Full run (all 398 sequences) — recommended

```bash
# Overnight — ~8.5-9 hours (saves ~1 hour vs v5 full run)
nohup venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --output femr_v6 --workers 40 > /tmp/v6_full.log 2>&1 &
```

### Single sequence test (skip preload)

```bash
# Use --skip-preload for single-sequence tests — avoids the 90s preload cost
venv/shoma/bin/python -u scripts/femr_netsuite_report_6.py --sequence 2ADP001 --output test_v6.xlsx --workers 30 --skip-preload
```

---

## Monitoring

### Tail any log

```bash
tail -f /tmp/v5_comml.log
tail -f /tmp/v6_adp.log
```

### Check all running jobs

```bash
ps aux | grep femr_netsuite_report | grep -v grep
```

### Kill a stuck job

```bash
# First find the PID
ps aux | grep femr_netsuite_report | grep -v grep

# Then kill by PID
kill <PID>
```

### Watch output files grow in real-time

```bash
watch -n 10 'ls -lah femr_v*.xlsx 2>/dev/null'
```

---

## Notes

- **Worker count rule of thumb:**
  - Sequential (1 process at a time): **40 workers**
  - 2 parallel processes: **30 workers each**
  - 3+ parallel processes: **20 workers each**
  - More concurrent connections → higher chance of API rate-limiting

- **API is the bottleneck** — running 2 processes at 30 workers doesn't double throughput. Sequential is usually faster for total wall time.

- **Checkpoints** — the script saves every 10 tabs, so if interrupted you lose at most the current file's 10 tabs (not the whole run).

- **Filename suffix** — the script appends the reporting group name (lowercase) to your `--output` prefix, producing e.g. `femr_v6_adp_adp.xlsx`.

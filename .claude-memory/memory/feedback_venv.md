---
name: Use project venv Python
description: Always use the project's venv Python interpreter, not the system Python
type: feedback
---

Use `venv/shoma/bin/python` (relative to project root `/home/lap-68/Documents/gt-atul/shoma`) to run scripts — not `python` or `python3`.

**Why:** The project has its own virtualenv with required packages (e.g. openpyxl). System Python lacks these.

**How to apply:** Whenever running a Python script in this project, prefix with `venv/shoma/bin/python` instead of `python`.

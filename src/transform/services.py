"""
FEMR Funds transformation service.

Reads the 'FEMR Funds' sheet from an uploaded workbook and reshapes it into
a long-format 'Output' sheet with one row per (Sequence, Quarter, Type).

Four types per (Sequence, Quarter):
  Committed      – Award Amount column
  Obligated      – Obligated column
  Expended       – Cash Collected column
  Remaining Cash – Obligated minus Expended
"""
import io
import logging
from collections import defaultdict
from datetime import datetime

from openpyxl import load_workbook
from openpyxl.styles import Font

logger = logging.getLogger('transform.services')

# Quarter definitions: (quarter_end_date, col_committed, col_obligated, col_expended)
# Columns are 1-indexed matching the FEMR Funds sheet.
# Annual total columns are intentionally skipped between FY blocks.
QUARTERS = [
    (datetime(2020,  6, 30), 10, 11, 12),
    (datetime(2020,  9, 30), 13, 14, 15),
    # skip FY20 Total (16–18)
    (datetime(2020, 12, 31), 19, 20, 21),
    (datetime(2021,  3, 30), 22, 23, 24),
    (datetime(2021,  6, 30), 25, 26, 27),
    (datetime(2021,  9, 30), 28, 29, 30),
    # skip FY21 Total (31–33)
    (datetime(2021, 12, 31), 34, 35, 36),
    (datetime(2022,  3, 30), 37, 38, 39),
    (datetime(2022,  6, 30), 40, 41, 42),
    (datetime(2022,  9, 30), 43, 44, 45),
    # skip FY22 Total (46–48)
    (datetime(2022, 12, 31), 49, 50, 51),
    (datetime(2023,  3, 30), 52, 53, 54),
    (datetime(2023,  6, 30), 55, 56, 57),
    (datetime(2023,  9, 30), 58, 59, 60),
    # skip FY23 Total (61–63)
    (datetime(2023, 12, 31), 64, 65, 66),
    (datetime(2024,  3, 30), 67, 68, 69),
    (datetime(2024,  6, 30), 70, 71, 72),
    (datetime(2024,  9, 30), 73, 74, 75),
    # skip FY24 Total (76–78)
    (datetime(2024, 12, 31), 79, 80, 81),
    (datetime(2025,  3, 30), 82, 83, 84),
    (datetime(2025,  6, 30), 85, 86, 87),
    (datetime(2025,  9, 30), 88, 89, 90),
    # skip FY25 Total (91–93)
    (datetime(2025, 12, 31), 94, 95, 96),
    (datetime(2026,  3, 30), 97, 98, 99),
    (datetime(2026,  6, 30), 100, 101, 102),
    (datetime(2026,  9, 30), 103, 104, 105),
    # skip FY26 Total (106–108), Grand Total (109–112)
]

_OUTPUT_TYPES = [
    ('Committed',  0),
    ('Obligated',  1),
    ('Expended',   2),
]


def safe_float(val) -> float:
    """Convert a cell value to float, returning 0.0 for None or non-numeric."""
    if val is None:
        return 0.0
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _read_sequences(ws_femr, ws_output=None) -> list[str]:
    """
    Return the ordered sequence list.
    Prefers the existing Output template (rows 2–135, first block = all sequences)
    so that output order stays consistent across runs.
    Falls back to first-seen order in FEMR Funds when no template exists.
    """
    if ws_output is not None:
        sequences = []
        for row in ws_output.iter_rows(min_row=2, max_row=135, values_only=True):
            if row[0] is not None:
                sequences.append(row[0])
        if sequences:
            return sequences

    sequences = []
    seen = set()
    for row in ws_femr.iter_rows(min_row=7, max_row=306, values_only=True):
        raw = row[3]  # Column D
        if raw is None:
            continue
        seq = str(raw).strip()
        if seq and seq not in seen:
            sequences.append(seq)
            seen.add(seq)
    return sequences


def _aggregate_data(ws_femr, sequences: list[str]) -> dict:
    """
    Aggregate (sum) quarterly financials per sequence from FEMR Funds sheet.
    Returns: { sequence -> { quarter_date -> [committed, obligated, expended] } }
    Sequences appearing on multiple rows are summed together.
    """
    seq_set = set(sequences)
    data = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0]))

    for row in ws_femr.iter_rows(min_row=7, max_row=306, values_only=True):
        raw = row[3]
        if raw is None:
            continue
        seq = str(raw).strip()
        if seq not in seq_set:
            continue
        for (qdate, cc, co, ce) in QUARTERS:
            data[seq][qdate][0] += safe_float(row[cc - 1])
            data[seq][qdate][1] += safe_float(row[co - 1])
            data[seq][qdate][2] += safe_float(row[ce - 1])

    return data


def _build_output_rows(sequences: list[str], data: dict) -> list[tuple]:
    """
    Build the flat list of output rows.
    Structure: for each quarter → Committed block, Obligated block,
               Expended block, Remaining Cash block, each with all sequences.
    """
    rows = []
    for (qdate, *_) in QUARTERS:
        for type_name, idx in _OUTPUT_TYPES:
            for seq in sequences:
                rows.append((seq, qdate, type_name, data[seq][qdate][idx]))
        for seq in sequences:
            remaining = data[seq][qdate][1] - data[seq][qdate][2]
            rows.append((seq, qdate, 'Remaining Cash', remaining))
    return rows


def _write_output_sheet(ws_out, output_rows: list[tuple], has_template: bool):
    """Write output rows into ws_out, clearing stale rows if needed."""
    if not has_template:
        bold_arial = Font(bold=True, name='Arial')
        for col, header in enumerate(['Sequence', 'Qtr Date', 'Type', 'Amount'], 1):
            ws_out.cell(row=1, column=col, value=header).font = bold_arial
        ws_out['G1'] = 'Remaining cash is a formula '
        ws_out['I1'] = 'Obligated'
        ws_out['J1'] = 'minus '
        ws_out['K1'] = 'Expended'
        ws_out['L1'] = 'for each qtr'

    for i, (seq, qdate, type_name, amount) in enumerate(output_rows, start=2):
        ws_out.cell(row=i, column=1, value=seq)
        ws_out.cell(row=i, column=2, value=qdate)
        ws_out.cell(row=i, column=3, value=type_name)
        ws_out.cell(row=i, column=4, value=amount)

    # Clear any leftover rows from a previous (larger) template
    expected_last = 1 + len(output_rows)
    if ws_out.max_row > expected_last:
        for r in range(expected_last + 1, ws_out.max_row + 1):
            for c in range(1, 5):
                ws_out.cell(row=r, column=c, value=None)


def run_transform(input_path: str) -> bytes:
    """
    Main entry point.  Read the FEMR Funds workbook at *input_path*,
    regenerate the Output sheet, and return the result as raw xlsx bytes.
    """
    logger.info("Transform started: %s", input_path)

    # Open twice: data_only for reading values, normal for preserving styles
    wb_values = load_workbook(input_path, data_only=True)
    wb_out = load_workbook(input_path)

    ws_femr = wb_values['FEMR Funds']
    ws_output_template = wb_values['Output'] if 'Output' in wb_values.sheetnames else None

    if 'Output' in wb_out.sheetnames:
        ws_out = wb_out['Output']
    else:
        ws_out = wb_out.create_sheet('Output', 1)

    sequences = _read_sequences(ws_femr, ws_output_template)
    data = _aggregate_data(ws_femr, sequences)
    output_rows = _build_output_rows(sequences, data)
    _write_output_sheet(ws_out, output_rows, has_template=ws_output_template is not None)

    logger.info(
        "Transform complete: %d sequences × %d quarters × 4 types = %d rows",
        len(sequences), len(QUARTERS), len(output_rows),
    )

    buf = io.BytesIO()
    wb_out.save(buf)
    buf.seek(0)
    return buf.read()

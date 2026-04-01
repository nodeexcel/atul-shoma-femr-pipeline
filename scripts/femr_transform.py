"""
FEMR Funds Transformation Script
Reads 'FEMR Funds' input sheet and generates 'Output' tab in the same format.

Output structure:
  For each quarter date, 4 blocks of N rows each:
    Block 1: Committed (Award Amount)
    Block 2: Obligated
    Block 3: Expended (Cash Collected)
    Block 4: Remaining Cash (= Obligated - Expended for that quarter)

Quarters are discovered dynamically from row 4 of the FEMR Funds sheet.
Row 4 contains labels like 'QE 6/30/20' for quarter end dates and
'FY20 Total' / 'Total' for annual totals (which are automatically skipped).
Each quarter at column C maps to: C=Committed, C+1=Obligated, C+2=Expended.
"""

from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, numbers
from openpyxl.utils import get_column_letter
from datetime import datetime
from collections import defaultdict
import copy
import argparse

# Fallback paths (the script is now meant to be called with CLI args)
INPUT_FILE = '/mnt/user-data/uploads/2026_03_FEMR_funds.xlsx'
OUTPUT_FILE = '/mnt/user-data/outputs/2026_03_FEMR_funds_output.xlsx'

def discover_quarters(ws):
    """
    Dynamically build the quarter list by reading row 4 of the FEMR Funds sheet.
    Cells in row 4 with a 'QE M/D/YY' label are quarter end dates; all other
    labels (e.g. 'FY20 Total', 'Total') are skipped automatically.

    Returns: list of (quarter_end_date, col_committed, col_obligated, col_expended)
             Columns are 1-indexed.
    """
    quarters = []
    for col in range(1, ws.max_column + 1):
        raw = ws.cell(row=4, column=col).value
        if raw is None:
            continue
        label = str(raw).strip()
        if not label.upper().startswith('QE '):
            continue
        date_str = label[3:].strip()   # e.g. "6/30/20"
        try:
            qdate = datetime.strptime(date_str, '%m/%d/%y')
        except ValueError:
            continue
        quarters.append((qdate, col, col + 1, col + 2))
    return quarters

def safe_float(val):
    """Convert value to float, returning 0.0 if None or not numeric."""
    if val is None:
        return 0.0
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def read_input(wb):
    """
    Read FEMR Funds sheet and aggregate values by (sequence, quarter).
    Quarters are discovered dynamically from row 4 of the FEMR Funds sheet.
    Returns:
        quarters:  list of (quarter_end_date, col_committed, col_obligated, col_expended)
        sequences: ordered list of unique sequences (from Output tab if present)
        data:      dict { sequence -> { quarter_date -> [committed, obligated, expended] } }
    """
    ws = wb['FEMR Funds']
    quarters = discover_quarters(ws)

    # Sequence order is taken from the existing Output template when present.
    if 'Output' in wb.sheetnames:
        ws_out = wb['Output']
        sequences = []
        for row in ws_out.iter_rows(min_row=2, max_row=135, values_only=True):
            if row[0] is not None:
                sequences.append(row[0])
    else:
        # Fallback: derive sequences from the FEMR Funds sheet, preserving first-seen order.
        sequences = []
        seen = set()
        for row in ws.iter_rows(min_row=7, max_row=306, values_only=True):
            raw_seq = row[3]  # Column D
            if raw_seq is None:
                continue
            seq = str(raw_seq).strip()
            if seq and seq not in seen:
                sequences.append(seq)
                seen.add(seq)

    # Aggregate input data: sequence -> quarter_date -> [committed, obligated, expended]
    data = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0]))

    for row in ws.iter_rows(min_row=7, max_row=306, values_only=True):
        raw_seq = row[3]  # Column D (1-indexed col 4, 0-indexed col 3)
        if raw_seq is None:
            continue
        seq = str(raw_seq).strip()
        if seq not in sequences:
            continue

        for (qdate, cc, co, ce) in quarters:
            # cols are 1-indexed; row tuple is 0-indexed
            data[seq][qdate][0] += safe_float(row[cc - 1])
            data[seq][qdate][1] += safe_float(row[co - 1])
            data[seq][qdate][2] += safe_float(row[ce - 1])

    return quarters, sequences, data

def generate_output(quarters, sequences, data):
    """
    Build the output as a list of rows: (sequence, qtr_date, type, amount)
    Structure: for each quarter, 4 blocks (Committed, Obligated, Expended, Remaining Cash),
               each block listing all sequences in order.
    """
    rows = []
    for (qdate, *_) in quarters:
        for type_name, idx in [('Committed', 0), ('Obligated', 1), ('Expended', 2)]:
            for seq in sequences:
                rows.append((seq, qdate, type_name, data[seq][qdate][idx]))
        for seq in sequences:
            remaining = data[seq][qdate][1] - data[seq][qdate][2]
            rows.append((seq, qdate, 'Remaining Cash', remaining))
    return rows

def copy_sheet_with_formatting(src_wb, src_sheet_name, dst_wb, dst_sheet_name):
    """Copy a sheet with its data and basic formatting to another workbook."""
    src_ws = src_wb[src_sheet_name]
    if dst_sheet_name in dst_wb.sheetnames:
        del dst_wb[dst_sheet_name]
    dst_ws = dst_wb.create_sheet(dst_sheet_name)

    for row in src_ws.iter_rows():
        for cell in row:
            dst_cell = dst_ws.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                dst_cell.font = copy.copy(cell.font)
                dst_cell.border = copy.copy(cell.border)
                dst_cell.fill = copy.copy(cell.fill)
                dst_cell.number_format = cell.number_format
                dst_cell.alignment = copy.copy(cell.alignment)

    for col in src_ws.column_dimensions:
        dst_ws.column_dimensions[col].width = src_ws.column_dimensions[col].width
    for row in src_ws.row_dimensions:
        dst_ws.row_dimensions[row].height = src_ws.row_dimensions[row].height
    return dst_ws

def write_output_sheet(wb, sequences, data):
    """Write the Output sheet with calculated data."""
    if 'Output' in wb.sheetnames:
        ws = wb['Output']
    else:
        ws = wb.create_sheet('Output')

    output_rows = generate_output(sequences, data)

    # Clear existing data rows (keep header row 1)
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)

    # Write header
    ws['A1'] = 'Sequence'
    ws['B1'] = 'Qtr Date'
    ws['C1'] = 'Type'
    ws['D1'] = 'Amount'

    # Style header
    header_font = Font(bold=True)
    for col in ['A', 'B', 'C', 'D']:
        ws[f'{col}1'].font = header_font

    # Write data rows
    date_fmt = 'MM/DD/YYYY'
    number_fmt = '#,##0.00;(#,##0.00);-'

    for i, (seq, qdate, type_name, amount) in enumerate(output_rows, start=2):
        ws.cell(row=i, column=1, value=seq)
        date_cell = ws.cell(row=i, column=2, value=qdate)
        date_cell.number_format = date_fmt
        ws.cell(row=i, column=3, value=type_name)
        amount_cell = ws.cell(row=i, column=4, value=round(amount, 2) if amount != 0 else 0)
        amount_cell.number_format = number_fmt

    # Column widths
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 16
    ws.column_dimensions['D'].width = 16

    print(f"Output sheet written: {len(output_rows)} data rows")

def main(input_file: str = INPUT_FILE, output_file: str = OUTPUT_FILE):
    print("Reading input file...")
    wb = load_workbook(input_file, data_only=True)

    print("Parsing FEMR Funds input...")
    quarters, sequences, data = read_input(wb)
    print(f"  Quarters discovered: {len(quarters)}")
    for qdate, cc, *_ in quarters:
        print(f"    {qdate.strftime('%m/%d/%Y')}  (col {cc})")
    print(f"  Sequences: {len(sequences)}")
    print(f"  Expected output rows: {len(sequences) * len(quarters) * 4}")

    # Verify a known value: 2ADP001, 9/30/20 should be 27100000 committed
    q = datetime(2020, 9, 30)
    val = data.get('2ADP001', {}).get(q, [0,0,0])
    print(f"\nVerification - 2ADP001 at 9/30/20:")
    print(f"  Committed={val[0]:,.0f}  Obligated={val[1]:,.0f}  Expended={val[2]:,.0f}")

    # 2ADP011 combined: 3175900 + (-837974) = 2337926
    val11 = data.get('2ADP011', {}).get(datetime(2020, 9, 30), [0,0,0])
    print(f"\nVerification - 2ADP011 at 9/30/20:")
    print(f"  Committed={val11[0]:,.0f}  (expected 2,337,926)")

    print("\nWriting output file...")
    out_wb = load_workbook(input_file)

    if 'Output' in out_wb.sheetnames:
        out_ws = out_wb['Output']
        # Delete all columns beyond D to remove extra template content (preserves A-D styles)
        if out_ws.max_column > 4:
            out_ws.delete_cols(5, out_ws.max_column - 4)
    else:
        out_ws = out_wb.create_sheet('Output', 1)
        headers = ['Sequence', 'Qtr Date', 'Type', 'Amount']
        for col, h in enumerate(headers, 1):
            out_ws.cell(row=1, column=col, value=h).font = Font(bold=True)

    output_rows = generate_output(quarters, sequences, data)

    for i, (seq, qdate, type_name, amount) in enumerate(output_rows, start=2):
        out_ws.cell(row=i, column=1, value=seq)
        date_cell = out_ws.cell(row=i, column=2, value=qdate)
        date_cell.number_format = 'mm-dd-yy'
        out_ws.cell(row=i, column=3, value=type_name)
        out_ws.cell(row=i, column=4, value=amount)

    # Auto-filter covering full data range
    last_row = 1 + len(output_rows)
    out_ws.auto_filter.ref = f'A1:D{last_row}'

    out_wb.save(output_file)
    print(f"Saved: {output_file}")
    print(f"Total data rows written: {len(output_rows)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FEMR Funds -> Output transformer")
    parser.add_argument(
        "--input",
        dest="input_file",
        default=INPUT_FILE,
        help="Path to input .xlsx (must include sheet `FEMR Funds` and template `Output` for sequence ordering).",
    )
    parser.add_argument(
        "--output",
        dest="output_file",
        default=OUTPUT_FILE,
        help="Path for the generated output .xlsx.",
    )
    args = parser.parse_args()
    main(args.input_file, args.output_file)

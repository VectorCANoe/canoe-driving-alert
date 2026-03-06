#!/usr/bin/env python3
"""
Markdown to Excel Converter
Converts Markdown files to Excel format, preserving tables and structure
"""

import re
import sys
import argparse
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def parse_markdown_table(lines):
    """Parse markdown table into list of rows"""
    table_lines = []
    in_table = False

    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            # Skip separator lines (e.g., |---|---|)
            if not re.match(r'\|[\s\-:]+\|', line):
                # Remove leading/trailing pipes and split
                cells = [cell.strip() for cell in line[1:-1].split('|')]
                table_lines.append(cells)
                in_table = True
        elif in_table:
            break

    return table_lines

def convert_md_to_excel(md_file, excel_file):
    """Convert Markdown file to Excel"""
    print(f"Converting: {md_file.name} -> {excel_file.name}")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    wb = Workbook()
    ws = wb.active
    ws.title = "Content"

    # Styles
    header_font = Font(bold=True, size=12, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    title_font = Font(bold=True, size=14, color="1F4E78")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    current_row = 1
    in_table = False
    table_start = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Title (# Header)
        if line.startswith('# '):
            ws.cell(row=current_row, column=1, value=line[2:])
            ws.cell(row=current_row, column=1).font = title_font
            current_row += 1

        # Subtitle (## Header)
        elif line.startswith('## '):
            ws.cell(row=current_row, column=1, value=line[3:])
            ws.cell(row=current_row, column=1).font = Font(bold=True, size=12)
            current_row += 1

        # Subheader (### Header)
        elif line.startswith('### '):
            ws.cell(row=current_row, column=1, value=line[4:])
            ws.cell(row=current_row, column=1).font = Font(bold=True, size=11)
            current_row += 1

        # Table
        elif line.startswith('|') and not in_table:
            # Collect all table lines
            table_lines = []
            j = i
            while j < len(lines):
                tline = lines[j].strip()
                if tline.startswith('|') and tline.endswith('|'):
                    # Skip separator line
                    if not re.match(r'\|[\s\-:]+\|', tline):
                        cells = [cell.strip() for cell in tline[1:-1].split('|')]
                        table_lines.append(cells)
                    j += 1
                else:
                    break

            # Write table to Excel
            if table_lines:
                # Header row
                for col_idx, cell_value in enumerate(table_lines[0], start=1):
                    cell = ws.cell(row=current_row, column=col_idx, value=cell_value)
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.border = border

                current_row += 1

                # Data rows
                for row_data in table_lines[1:]:
                    for col_idx, cell_value in enumerate(row_data, start=1):
                        cell = ws.cell(row=current_row, column=col_idx, value=cell_value)
                        cell.border = border
                        cell.alignment = Alignment(vertical='top', wrap_text=True)
                    current_row += 1

                current_row += 1  # Add spacing after table
                i = j - 1

        # Regular text
        elif line and not line.startswith('---'):
            # Remove markdown formatting
            clean_line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)  # Bold
            clean_line = re.sub(r'\*(.+?)\*', r'\1', clean_line)  # Italic
            clean_line = re.sub(r'`(.+?)`', r'\1', clean_line)  # Code

            if clean_line:
                ws.cell(row=current_row, column=1, value=clean_line)
                current_row += 1

        # Empty line
        elif not line:
            current_row += 1

        i += 1

    # Auto-adjust column widths
    for col_idx in range(1, ws.max_column + 1):
        max_length = 0
        column = get_column_letter(col_idx)

        for cell in ws[column]:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = min(max_length + 2, 80)
        ws.column_dimensions[column].width = adjusted_width

    # Save
    wb.save(excel_file)
    print(f"✓ Created: {excel_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown files in a directory to Excel files."
    )
    parser.add_argument(
        "source_dir",
        help="Directory containing markdown files (*.md).",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory for xlsx files (default: <source_dir>/excel).",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else source_dir / "excel"
    )

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Source directory not found or not a directory: {source_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all MD files
    md_files = sorted(source_dir.glob("*.md"))

    print(f"\nFound {len(md_files)} files to convert in {source_dir}:")
    for md_file in md_files:
        print(f"  - {md_file.name}")

    if not md_files:
        print("No markdown files found!")
        return

    print("\nConverting...\n")

    for md_file in md_files:
        excel_file = output_dir / f"{md_file.stem}.xlsx"
        try:
            convert_md_to_excel(md_file, excel_file)
        except Exception as e:
            print(f"✗ Error converting {md_file.name}: {e}")

    print(f"\n✅ Conversion complete! Files saved to: {output_dir}")

if __name__ == "__main__":
    main()

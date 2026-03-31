from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


SEPARATOR_RE = re.compile(r"^\s*:?-{3,}:?\s*$")


@dataclass
class TableIssue:
    path: Path
    start_line: int
    columns: int
    estimated_width: int
    max_cell_width: int
    max_row_width: int


def split_cells(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [cell.strip() for cell in raw.split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(SEPARATOR_RE.match(cell or "---") for cell in cells)


def analyze_table(lines: list[str], path: Path, start_line: int) -> TableIssue | None:
    rows = [split_cells(line) for line in lines if line.strip()]
    rows = [row for row in rows if row]
    if len(rows) < 2:
        return None

    header = rows[0]
    separator = rows[1]
    if len(header) < 2 or not is_separator_row(separator):
        return None

    col_count = max(len(row) for row in rows)
    col_max = [0] * col_count
    max_row_width = 0

    for row in rows:
        padded = row + [""] * (col_count - len(row))
        max_row_width = max(max_row_width, sum(len(cell) for cell in padded))
        for idx, cell in enumerate(padded):
            col_max[idx] = max(col_max[idx], len(cell))

    estimated_width = sum(col_max) + (3 * col_count) + 1
    max_cell_width = max(col_max) if col_max else 0
    return TableIssue(
        path=path,
        start_line=start_line,
        columns=col_count,
        estimated_width=estimated_width,
        max_cell_width=max_cell_width,
        max_row_width=max_row_width,
    )


def iter_tables(path: Path) -> list[TableIssue]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    issues: list[TableIssue] = []
    block: list[str] = []
    start_line = 0

    for lineno, line in enumerate(lines, start=1):
        if line.startswith("|"):
            if not block:
                start_line = lineno
            block.append(line)
            continue

        if block:
            issue = analyze_table(block, path, start_line)
            if issue is not None:
                issues.append(issue)
            block = []

    if block:
        issue = analyze_table(block, path, start_line)
        if issue is not None:
            issues.append(issue)

    return issues


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("..") / "source"
    max_table_width = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    max_cell_width = int(sys.argv[3]) if len(sys.argv) > 3 else 48

    issues: list[TableIssue] = []
    for path in sorted(root.rglob("*.md")):
        issues.extend(iter_tables(path))

    offenders = [
        issue
        for issue in issues
        if issue.estimated_width > max_table_width or issue.max_cell_width > max_cell_width
    ]

    print(f"[appendix-table-check] scanned_tables={len(issues)} max_table_width={max_table_width} max_cell_width={max_cell_width}")
    if not offenders:
        print("[appendix-table-check] result: PASS")
        return 0

    print("[appendix-table-check] result: FAIL")
    for issue in offenders:
        rel = issue.path.as_posix()
        print(
            f"  - {rel}:{issue.start_line} cols={issue.columns} "
            f"est_width={issue.estimated_width} max_cell={issue.max_cell_width} raw_row={issue.max_row_width}"
        )
    print("[appendix-table-check] fix: split wide tables, shorten cell text, or move detailed value dictionaries out of main tables.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

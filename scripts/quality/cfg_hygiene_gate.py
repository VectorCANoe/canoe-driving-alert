#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANOE_ROOT = ROOT / "canoe"
TEXT_EXTENSIONS = {".cfg", ".can", ".dbc", ".sysvars", ".xml"}
EXCLUDE_DIRS = {".git", ".idea", ".vscode", "__pycache__", "build", "dist", "tmp", "_pending_cleanup"}


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    rel_parts = path.relative_to(CANOE_ROOT).parts
    return not any(part in EXCLUDE_DIRS for part in rel_parts)


def scan_text(path: Path) -> tuple[list[str], list[str]]:
    abs_hits: list[str] = []
    mojibake_hits: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    for i, line in enumerate(lines, start=1):
        if re.search(r"[A-Za-z]:\\", line):
            abs_hits.append(f"{path}:{i}: {line.strip()}")
        if "���" in line or "????" in line or "\ufffd" in line:
            mojibake_hits.append(f"{path}:{i}: {line.strip()}")

    return abs_hits, mojibake_hits


def main() -> int:
    if not CANOE_ROOT.exists():
        print("[cfg-hygiene-gate] FAIL: canoe directory not found")
        return 1

    scan_files = sorted([p for p in CANOE_ROOT.rglob("*") if p.is_file() and should_scan(p)])
    if not scan_files:
        print("[cfg-hygiene-gate] FAIL: no scannable text files found under canoe/")
        return 1

    abs_all: list[str] = []
    mojibake_all: list[str] = []
    for path in scan_files:
        abs_hits, mojibake_hits = scan_text(path)
        abs_all.extend(abs_hits)
        mojibake_all.extend(mojibake_hits)

    print(f"[cfg-hygiene-gate] scanned files under canoe/: {len(scan_files)}")
    print(f"[cfg-hygiene-gate] absolute-path hits: {len(abs_all)}")
    print(f"[cfg-hygiene-gate] mojibake hits: {len(mojibake_all)}")

    if abs_all:
        print("\n[FAIL] Windows absolute paths are forbidden in committed CANoe text files:")
        for row in abs_all[:20]:
            print(f"- {row}")
        if len(abs_all) > 20:
            print(f"- ... ({len(abs_all) - 20} more)")

    if mojibake_all:
        print("\n[FAIL] Mojibake text detected in CANoe text files:")
        for row in mojibake_all[:20]:
            print(f"- {row}")
        if len(mojibake_all) > 20:
            print(f"- ... ({len(mojibake_all) - 20} more)")

    return 1 if (abs_all or mojibake_all) else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""CANoe text file hygiene gate.

Failure policy:
- FAIL : absolute Windows path in .can / .dbc / .sysvars / .xml  (agent-editable files)
- FAIL : mojibake text in .can/.dbc/.sysvars  (encoding corruption in agent-editable files)
- WARN : absolute Windows path in .cfg        (GUI-managed, expected to contain some local paths)
- SKIP : mojibake check in .cfg               (GUI may write non-UTF8 artifacts, not our concern)
- EXEMPT: lines ending with .cbf         (CANoe F8 auto-compiled binary ref, always absolute)
- EXEMPT: C:\\Users\\Public / C:\\Public  (Vector install template hints)
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANOE_ROOT = ROOT / "canoe"

# Files where an absolute path is a hard FAIL (agent-editable source files)
STRICT_EXTENSIONS = {".can", ".dbc", ".sysvars", ".xml"}
# Files where an absolute path is advisory WARN only (GUI-managed config files)
WARN_EXTENSIONS   = {".cfg"}

EXCLUDE_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__",
    "build", "dist", "tmp", "_pending_cleanup",
    ".run",
    "vector_samples_19_4_10",
    "reference",
}


def should_scan(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix not in STRICT_EXTENSIONS and suffix not in WARN_EXTENSIONS:
        return False
    rel_parts = path.relative_to(CANOE_ROOT).parts
    return not any(part in EXCLUDE_DIRS for part in rel_parts)


def scan_text(path: Path) -> tuple[list[str], list[str]]:
    abs_hits: list[str] = []
    mojibake_hits: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if re.search(r"[A-Za-z]:\\", line):
            # Vector install template path — always allowed
            if r"C:\Users\Public" in line or r"C:\Public" in line:
                continue
            # CANoe F8-compiled .cbf refs are always absolute — exempt
            if stripped.endswith(".cbf"):
                continue
            abs_hits.append(f"{path}:{i}: {stripped}")

        # Mojibake in GUI-managed .cfg is also skipped (GUI may write non-UTF8 artifacts)
        if path.suffix.lower() in WARN_EXTENSIONS:
            continue
        if "���" in line or "????" in line or "\ufffd" in line:
            mojibake_hits.append(f"{path}:{i}: {stripped}")

    return abs_hits, mojibake_hits


def _safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def main() -> int:
    if not CANOE_ROOT.exists():
        print("[cfg-hygiene-gate] FAIL: canoe directory not found")
        return 1

    scan_files = sorted([p for p in CANOE_ROOT.rglob("*") if p.is_file() and should_scan(p)])
    if not scan_files:
        print("[cfg-hygiene-gate] FAIL: no scannable text files found under canoe/")
        return 1

    strict_abs:   list[str] = []
    warn_abs:     list[str] = []
    mojibake_all: list[str] = []

    for path in scan_files:
        abs_hits, mojibake_hits = scan_text(path)
        if path.suffix.lower() in STRICT_EXTENSIONS:
            strict_abs.extend(abs_hits)
        else:
            warn_abs.extend(abs_hits)
        mojibake_all.extend(mojibake_hits)

    print(f"[cfg-hygiene-gate] scanned: {len(scan_files)} files")
    print(f"[cfg-hygiene-gate] FAIL-class abs-path hits (.can/.dbc/.sysvars): {len(strict_abs)}")
    print(f"[cfg-hygiene-gate] WARN-class abs-path hits (.cfg GUI-managed):   {len(warn_abs)}")
    print(f"[cfg-hygiene-gate] WARN-class mojibake hits:                       {len(mojibake_all)}")

    if strict_abs:
        print("\n[FAIL] Absolute Windows paths in agent-editable files (.can/.dbc/.sysvars):")
        for row in strict_abs[:20]:
            _safe_print(f"  - {row}")
        if len(strict_abs) > 20:
            print(f"  ... ({len(strict_abs) - 20} more)")

    if warn_abs:
        _safe_print("\n[WARN] Absolute paths in GUI-managed .cfg (advisory - expected from CANoe GUI save):")
        for row in warn_abs[:10]:
            _safe_print(f"  - {row}")

    if mojibake_all:
        print("\n[FAIL] Mojibake/encoding corruption in source files (.can/.dbc/.sysvars):")
        for row in mojibake_all[:10]:
            _safe_print(f"  - {row}")
        if len(mojibake_all) > 10:
            print(f"  ... ({len(mojibake_all) - 10} more)")

    if strict_abs or mojibake_all:
        print("\n[cfg-hygiene-gate] result: FAIL")
        return 1

    result = "WARN" if warn_abs else "PASS"
    print(f"\n[cfg-hygiene-gate] result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Repository text integrity gate.

Hard-fails when source-like text files contain:
- UTF-8 decode failures
- replacement character (U+FFFD)
- suspicious multi-question-mark runs
- common mojibake markers seen after bad local re-save paths

This gate is intentionally broader than cfg_hygiene_gate.py because it protects
operator docs, Python surface strings, and CAPL sources before commit/push.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SCANNED_SUFFIXES = {
    ".md",
    ".py",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".can",
    ".cin",
    ".dbc",
    ".sysvars",
}

EXCLUDE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    ".codex-tmp",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "Library",
    "Temp",
    "Logs",
    "obj",
    "bin",
    "reference",
    "site",
}

EXCLUDE_PATH_PARTS = {
    ("canoe", "tmp", "reports", "verification"),
    ("canoe", "logging", "evidence"),
    ("canoe", "cfg", ".run"),
}

EXEMPT_LITERAL_SENTINEL_FILES = {
    Path("scripts/gates/cfg_hygiene_gate.py"),
    Path("canoe/scripts/fix_cfg_paths.py"),
}

QUESTION_RUN_RE = re.compile(r"\?{3,}")
COMMON_MOJIBAKE_RE = re.compile(r"(?:Ã.|ì.|ë.|ð.){2,}")


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in SCANNED_SUFFIXES:
        return False
    parts = path.relative_to(ROOT).parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return False
    for prefix in EXCLUDE_PATH_PARTS:
        if parts[: len(prefix)] == prefix:
            return False
    return True


def iter_scan_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*") if p.is_file() and should_scan(p))


def scan_file(path: Path) -> tuple[list[str], list[str], list[str], list[str]]:
    decode_hits: list[str] = []
    replacement_hits: list[str] = []
    question_hits: list[str] = []
    mojibake_hits: list[str] = []

    rel_path = path.relative_to(ROOT)
    skip_literal_checks = rel_path in EXEMPT_LITERAL_SENTINEL_FILES

    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        decode_hits.append(f"{path}: decode-fail: {exc}")
        text = data.decode("utf-8", errors="replace")

    for index, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not skip_literal_checks and "\ufffd" in line:
            replacement_hits.append(f"{path}:{index}: {stripped}")
        if not skip_literal_checks and QUESTION_RUN_RE.search(line):
            question_hits.append(f"{path}:{index}: {stripped}")
        if not skip_literal_checks and COMMON_MOJIBAKE_RE.search(line):
            mojibake_hits.append(f"{path}:{index}: {stripped}")

    return decode_hits, replacement_hits, question_hits, mojibake_hits


def safe_print(line: str) -> None:
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode("ascii", errors="replace").decode("ascii"))


def main() -> int:
    files = iter_scan_files()
    if not files:
        print("[text-integrity-gate] FAIL: no scannable files found")
        return 1

    decode_all: list[str] = []
    replacement_all: list[str] = []
    question_all: list[str] = []
    mojibake_all: list[str] = []

    for path in files:
        decode_hits, replacement_hits, question_hits, mojibake_hits = scan_file(path)
        decode_all.extend(decode_hits)
        replacement_all.extend(replacement_hits)
        question_all.extend(question_hits)
        mojibake_all.extend(mojibake_hits)

    print(f"[text-integrity-gate] scanned: {len(files)} files")
    print(f"[text-integrity-gate] decode-fail hits:     {len(decode_all)}")
    print(f"[text-integrity-gate] replacement-char hits:{len(replacement_all)}")
    print(f"[text-integrity-gate] question-run hits:    {len(question_all)}")
    print(f"[text-integrity-gate] mojibake-pattern hits:{len(mojibake_all)}")

    failed = False
    for title, rows in [
        ("UTF-8 decode failures", decode_all),
        ("Replacement character hits", replacement_all),
        ("Suspicious question-mark runs", question_all),
        ("Common mojibake pattern hits", mojibake_all),
    ]:
        if not rows:
            continue
        failed = True
        print(f"\n[FAIL] {title}:")
        for row in rows[:20]:
            safe_print(f"  - {row}")
        if len(rows) > 20:
            print(f"  ... ({len(rows) - 20} more)")

    print(f"\n[text-integrity-gate] result: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

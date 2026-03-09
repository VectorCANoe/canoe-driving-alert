#!/usr/bin/env python3
"""Check 1:1 sync between src/capl and cfg/channel_assign CAPL files."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "canoe" / "src" / "capl"
CFG_ROOT = REPO_ROOT / "canoe" / "cfg" / "channel_assign"

EXCLUDED_SRC_DIRS = {
    "v1_legacy",
    "retired_placeholders",
}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_can_files(root: Path, *, excluded_dirs: set[str] | None = None) -> dict[str, Path]:
    files = {}
    duplicates = []
    excluded_dirs = excluded_dirs or set()
    for p in root.rglob("*.can"):
        if any(part in excluded_dirs for part in p.parts):
            continue
        key = p.name
        if key in files:
            duplicates.append(key)
        else:
            files[key] = p

    if duplicates:
        print("[FAIL] Duplicate *.can file names detected:")
        for name in sorted(set(duplicates)):
            print(f"  - {name}")
        sys.exit(2)

    return files


def main() -> int:
    src_map = collect_can_files(SRC_ROOT, excluded_dirs=EXCLUDED_SRC_DIRS)
    cfg_map = collect_can_files(CFG_ROOT)

    src_names = set(src_map.keys())
    cfg_names = set(cfg_map.keys())

    only_src = sorted(src_names - cfg_names)
    only_cfg = sorted(cfg_names - src_names)

    common = sorted(src_names & cfg_names)
    content_diff = []
    for name in common:
        if file_hash(src_map[name]) != file_hash(cfg_map[name]):
            content_diff.append(name)

    print(
        "[CAPL_SYNC] "
        f"src={len(src_map)} cfg={len(cfg_map)} "
        f"common={len(common)} only_src={len(only_src)} "
        f"only_cfg={len(only_cfg)} content_diff={len(content_diff)}"
    )

    if only_src or only_cfg or content_diff:
        if only_src:
            print("[ONLY_SRC]", ", ".join(only_src))
        if only_cfg:
            print("[ONLY_CFG]", ", ".join(only_cfg))
        if content_diff:
            print("[CONTENT_DIFF]", ", ".join(content_diff))
        return 2

    print("[PASS] src/capl and cfg/channel_assign are fully synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

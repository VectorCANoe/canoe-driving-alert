#!/usr/bin/env python3
"""Initialize UT/IT/ST evidence run folders with templates."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def copy_template_with_run_id(src: Path, dst: Path, run_id: str) -> None:
    text = src.read_text(encoding="utf-8")
    text = text.replace("<run_id>", run_id)
    dst.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create evidence run folder skeleton")
    parser.add_argument(
        "--run-id",
        default=dt.datetime.now().strftime("%Y%m%d_%H%M"),
        help="Run folder suffix (default: current timestamp)",
    )
    parser.add_argument(
        "--root",
        default="canoe/logging/evidence",
        help="Evidence root path",
    )
    args = parser.parse_args()

    root = _repo_path(Path(args.root))
    template_dir = root / "templates"
    log_tpl = template_dir / "verification_log_template.csv"
    cap_tpl = template_dir / "capture_index_template.csv"

    tiers = ["UT", "IT", "ST"]
    created = []
    for tier in tiers:
        run_dir = root / tier / args.run_id
        cap_dir = run_dir / "captures"
        run_dir.mkdir(parents=True, exist_ok=True)
        cap_dir.mkdir(parents=True, exist_ok=True)

        if log_tpl.exists():
            copy_template_with_run_id(log_tpl, run_dir / "verification_log.csv", args.run_id)
        if cap_tpl.exists():
            copy_template_with_run_id(cap_tpl, run_dir / "capture_index.csv", args.run_id)
        (run_dir / "raw_write_window.txt").write_text("", encoding="utf-8")
        created.append(run_dir)

    print("[EVIDENCE_INIT] created run folders:")
    for p in created:
        print(f"- {_rel(p)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

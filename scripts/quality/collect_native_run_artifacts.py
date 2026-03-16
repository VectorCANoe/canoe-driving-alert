#!/usr/bin/env python3
"""Collect native CANoe run artifacts for one verification tier."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ASSIGN_DIR_BY_TIER = {
    "UT": "UT_ACTIVE_BASELINE",
    "IT": "IT_ACTIVE_BASELINE",
    "ST": "ST_ACTIVE_BASELINE",
    "FULL": "FULL_ACTIVE_BASELINE",
}


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _copy_if_exists(src: Path, dst: Path) -> str | None:
    src = _repo_path(src)
    dst = _repo_path(dst)
    if not src.exists() or not src.is_file():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return _rel(dst)


def _copy_matching(src_root: Path, pattern: str, dst_root: Path) -> list[str]:
    src_root = _repo_path(src_root)
    dst_root = _repo_path(dst_root)
    copied: list[str] = []
    if not src_root.exists():
        return copied
    for src in sorted(src_root.glob(pattern)):
        if not src.is_file():
            continue
        dst = dst_root / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(_rel(dst))
    return copied


def default_raw_log_candidates(tier: str) -> list[Path]:
    canonical_base = REPO_ROOT / "canoe" / "logging" / "evidence" / "incoming"
    legacy_base = REPO_ROOT / "canoe" / "tmp" / "write_window"
    return [
        canonical_base / tier / "raw_write_window.txt",
        canonical_base / f"{tier}_ACTIVE_BASELINE_raw_write_window.txt",
        canonical_base / f"{tier}_raw_write_window.txt",
        canonical_base / "raw_write_window.txt",
        legacy_base / tier / "raw_write_window.txt",
        legacy_base / f"{tier}_ACTIVE_BASELINE_raw_write_window.txt",
        legacy_base / f"{tier}_raw_write_window.txt",
        legacy_base / "raw_write_window.txt",
    ]


def resolve_raw_log_source(tier: str, explicit: str) -> Path | None:
    if explicit:
        path = _repo_path(Path(explicit))
        return path if path.exists() and path.is_file() else None
    for candidate in default_raw_log_candidates(tier):
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect native CANoe reports and raw log for one run")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--tier", required=True, choices=["UT", "IT", "ST", "FULL"])
    parser.add_argument("--evidence-root", type=Path, default=Path("canoe/logging/evidence"))
    parser.add_argument("--cfg-root", type=Path, default=Path("canoe/cfg"))
    parser.add_argument("--assign-root", type=Path, default=Path("canoe/tests/modules/test_units/assign"))
    parser.add_argument(
        "--raw-log-source",
        default="",
        help="Optional raw Write Window source file. If omitted, standard drop paths are probed.",
    )
    parser.add_argument(
        "--allow-missing-raw-log",
        action="store_true",
        help="Do not fail when raw_write_window source is missing.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    evidence_root = _repo_path(args.evidence_root)
    cfg_root = _repo_path(args.cfg_root)
    assign_root = _repo_path(args.assign_root)
    assign_name = ASSIGN_DIR_BY_TIER[args.tier]

    run_dir = evidence_root / args.tier / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    native_dir = run_dir / "native_reports"
    native_dir.mkdir(parents=True, exist_ok=True)

    copied_summary: list[str] = []
    copied_assign_reports: list[str] = []
    copied_settings: list[str] = []

    summary_report = cfg_root / f"Report_{assign_name}.vtestreport"
    copied = _copy_if_exists(summary_report, native_dir / summary_report.name)
    if copied:
        copied_summary.append(copied)

    copied_settings.extend(
        _copy_matching(cfg_root, f"Report_{assign_name}*.settings", native_dir / "settings")
    )

    assign_dir = assign_root / assign_name
    if assign_dir.exists():
        copied_assign_reports.extend(
            _copy_matching(assign_dir, "Report_*.vtestreport", native_dir / assign_name)
        )

    raw_log_source = resolve_raw_log_source(args.tier, args.raw_log_source)
    raw_log_dest = run_dir / "raw_write_window.txt"
    raw_log_copied = None
    if raw_log_source is not None:
        raw_log_copied = _copy_if_exists(raw_log_source, raw_log_dest)
    elif not args.allow_missing_raw_log:
        print(
            "[COLLECT] FAIL: raw write window source not found. "
            "Pass --raw-log-source or configure one of the standard drop paths."
        )
        return 2

    manifest = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "run_id": args.run_id,
        "tier": args.tier,
        "assign_name": assign_name,
        "summary_reports": copied_summary,
        "assign_reports": copied_assign_reports,
        "settings_files": copied_settings,
        "raw_log_source": "" if raw_log_source is None else _rel(raw_log_source),
        "raw_log_copied": raw_log_copied or "",
    }
    manifest_path = run_dir / "native_report_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"[COLLECT] tier={args.tier} run_id={args.run_id} "
        f"summary={len(copied_summary)} assign_reports={len(copied_assign_reports)} "
        f"settings={len(copied_settings)} raw_log={'Y' if raw_log_copied else 'N'}"
    )
    print(f"[OUT] {_rel(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

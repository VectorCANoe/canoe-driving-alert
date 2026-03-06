#!/usr/bin/env python3
"""Convenience wrapper for the CANoe SIL verification evidence pipeline.

This wrapper keeps day-to-day execution simple while preserving existing tools:
  1) init_evidence_run.py
  2) build_evidence_from_write_window.py
  3) evidence_score_gate.py
  4) dev_completeness_smoke.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "canoe" / "logging" / "evidence"


def run_cmd(args: list[str]) -> int:
    print("[RUN]", " ".join(args))
    proc = subprocess.run(args, cwd=REPO_ROOT)
    return proc.returncode


def cmd_prepare(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "init_evidence_run.py"),
        "--run-id",
        args.run_id,
        "--root",
        str(args.evidence_root),
    ]
    return run_cmd(cmd)


def cmd_fill_score(args: argparse.Namespace) -> int:
    run_dir = args.evidence_root / args.tier / args.run_id
    template_csv = run_dir / "verification_log.csv"
    raw_log = run_dir / "raw_write_window.txt"
    filled_csv = run_dir / "verification_log_filled.csv"
    scored_csv = run_dir / "verification_log_scored.csv"
    scored_md = run_dir / "verification_report.md"
    scored_json = run_dir / "verification_report.json"

    fill_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "build_evidence_from_write_window.py"),
        "--template-csv",
        str(template_csv),
        "--raw-log",
        str(raw_log),
        "--output-csv",
        str(filled_csv),
        "--owner",
        args.owner,
        "--run-date",
        args.run_date,
    ]
    rc = run_cmd(fill_cmd)
    if rc != 0:
        return rc

    score_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "evidence_score_gate.py"),
        "--input",
        str(filled_csv),
        "--output-csv",
        str(scored_csv),
        "--output-md",
        str(scored_md),
        "--output-json",
        str(scored_json),
    ]
    if args.baseline_csv:
        score_cmd.extend(["--baseline-csv", str(args.baseline_csv)])
    if args.no_strict_metadata:
        score_cmd.append("--no-strict-metadata")
    if args.no_strict_axis:
        score_cmd.append("--no-strict-axis")
    return run_cmd(score_cmd)


def cmd_smoke(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "dev_completeness_smoke.py"),
        "--owner",
        args.owner,
        "--run-date",
        args.run_date,
        "--output-csv",
        str(args.output_csv),
        "--output-md",
        str(args.output_md),
    ]
    return run_cmd(cmd)


def cmd_insight(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "build_run_insight_report.py"),
        "--run-id",
        args.run_id,
        "--evidence-root",
        str(args.evidence_root),
        "--output-md",
        str(args.output_md),
        "--output-json",
        str(args.output_json),
    ]
    if args.baseline_run_id:
        cmd.extend(["--baseline-run-id", args.baseline_run_id])
    return run_cmd(cmd)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run simplified verification evidence workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare", help="Create UT/IT/ST run folder skeleton")
    p_prepare.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_prepare.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_prepare.set_defaults(func=cmd_prepare)

    p_fill = sub.add_parser("fill-score", help="Fill and score one tier run from raw Write log")
    p_fill.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_fill.add_argument("--tier", required=True, choices=["UT", "IT", "ST"])
    p_fill.add_argument("--owner", default="TBD")
    p_fill.add_argument("--run-date", default=dt.date.today().isoformat())
    p_fill.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_fill.add_argument(
        "--baseline-csv",
        type=Path,
        default=None,
        help="Optional baseline scored CSV for regression comparison",
    )
    p_fill.add_argument("--no-strict-metadata", action="store_true")
    p_fill.add_argument("--no-strict-axis", action="store_true")
    p_fill.set_defaults(func=cmd_fill_score)

    p_smoke = sub.add_parser("smoke", help="Run development completeness smoke checks via CANoe COM")
    p_smoke.add_argument("--owner", default="TBD")
    p_smoke.add_argument("--run-date", default=dt.date.today().isoformat())
    p_smoke.add_argument(
        "--output-csv",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "dev_completeness_smoke.csv",
    )
    p_smoke.add_argument(
        "--output-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "dev_completeness_smoke.md",
    )
    p_smoke.set_defaults(func=cmd_smoke)

    p_insight = sub.add_parser("insight", help="Build run-level insight report from scored UT/IT/ST logs")
    p_insight.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_insight.add_argument("--baseline-run-id", default="", help="Optional baseline run ID for trend comparison")
    p_insight.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_insight.add_argument(
        "--output-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_insight_report.md",
    )
    p_insight.add_argument(
        "--output-json",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_insight_report.json",
    )
    p_insight.set_defaults(func=cmd_insight)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

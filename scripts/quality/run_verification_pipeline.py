#!/usr/bin/env python3
"""Convenience wrapper for the CANoe SIL verification evidence pipeline.

This wrapper keeps day-to-day execution simple while preserving existing tools:
  1) init_evidence_run.py
  2) build_evidence_from_write_window.py
  3) evidence_score_gate.py
  4) dev_completeness_smoke.py
  5) build_doc_binding_bundle.py / build_doc_fill_template.py
  6) check_run_readiness.py
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


def _display_arg(value: str) -> str:
    if value == sys.executable:
        return Path(value).name
    candidate = Path(value)
    if candidate.is_absolute():
        try:
            return candidate.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return value
    return value


def run_cmd(args: list[str]) -> int:
    print("[RUN]", " ".join(_display_arg(arg) for arg in args))
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


def cmd_collect(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "collect_native_run_artifacts.py"),
        "--run-id",
        args.run_id,
        "--tier",
        args.tier,
        "--evidence-root",
        str(args.evidence_root),
    ]
    if args.raw_log_source:
        cmd.extend(["--raw-log-source", str(args.raw_log_source)])
    if args.allow_missing_raw_log:
        cmd.append("--allow-missing-raw-log")
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


def cmd_post_run(args: argparse.Namespace) -> int:
    collect_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_verification_pipeline.py"),
        "collect",
        "--run-id",
        args.run_id,
        "--tier",
        args.tier,
        "--evidence-root",
        str(args.evidence_root),
    ]
    if args.raw_log_source:
        collect_cmd.extend(["--raw-log-source", str(args.raw_log_source)])
    if args.allow_missing_raw_log:
        collect_cmd.append("--allow-missing-raw-log")
    rc = run_cmd(collect_cmd)
    if rc != 0:
        return rc

    fill_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_verification_pipeline.py"),
        "fill-score",
        "--run-id",
        args.run_id,
        "--tier",
        args.tier,
        "--owner",
        args.owner,
        "--run-date",
        args.run_date,
        "--evidence-root",
        str(args.evidence_root),
    ]
    if args.baseline_csv:
        fill_cmd.extend(["--baseline-csv", str(args.baseline_csv)])
    if args.no_strict_metadata:
        fill_cmd.append("--no-strict-metadata")
    if args.no_strict_axis:
        fill_cmd.append("--no-strict-axis")
    return run_cmd(fill_cmd)


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


def cmd_bind_doc(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "build_doc_binding_bundle.py"),
        "--run-id",
        args.run_id,
        "--evidence-root",
        str(args.evidence_root),
        "--docs-root",
        str(args.docs_root),
        "--output-csv",
        str(args.output_csv),
        "--output-json",
        str(args.output_json),
        "--output-md",
        str(args.output_md),
    ]
    return run_cmd(cmd)


def cmd_fill_template(args: argparse.Namespace) -> int:
    bind_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "build_doc_binding_bundle.py"),
        "--run-id",
        args.run_id,
        "--evidence-root",
        str(args.evidence_root),
        "--docs-root",
        str(args.docs_root),
        "--output-csv",
        str(args.binding_csv),
        "--output-json",
        str(args.binding_json),
        "--output-md",
        str(args.binding_md),
    ]
    rc = run_cmd(bind_cmd)
    if rc != 0:
        return rc

    fill_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "build_doc_fill_template.py"),
        "--binding-csv",
        str(args.binding_csv),
        "--run-id",
        args.run_id,
        "--owner-fallback",
        args.owner_fallback,
        "--date-fallback",
        args.date_fallback,
        "--output-csv",
        str(args.output_csv),
        "--output-md",
        str(args.output_md),
    ]
    return run_cmd(fill_cmd)


def _precheck_finalize_inputs(evidence_root: Path, run_id: str, tiers: list[str]) -> list[str]:
    missing: list[str] = []
    required = ("verification_log.csv", "raw_write_window.txt")
    for tier in tiers:
        run_dir = evidence_root / tier / run_id
        for name in required:
            path = run_dir / name
            if not path.exists():
                missing.append(str(path))
    return missing


def _raw_log_has_evidence_marker(raw_log_path: Path) -> bool:
    if not raw_log_path.exists():
        return False
    try:
        text = raw_log_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return "[EVIDENCE_OUT]" in text


def cmd_finalize(args: argparse.Namespace) -> int:
    tiers = [item.strip().upper() for item in args.tiers if item.strip()]
    if not tiers:
        print("[FINALIZE] no tiers selected. use --tiers UT IT ST")
        return 2

    missing = _precheck_finalize_inputs(args.evidence_root, args.run_id, tiers)
    if missing:
        print("[FINALIZE] missing required inputs (run verify prepare + save raw_write_window.txt first):")
        for item in missing:
            print(f"- {item}")
        return 2

    empty_markers: list[str] = []
    for tier in tiers:
        raw_log = args.evidence_root / tier / args.run_id / "raw_write_window.txt"
        if not _raw_log_has_evidence_marker(raw_log):
            empty_markers.append(str(raw_log))
    if empty_markers:
        print("[FINALIZE] raw logs exist but no [EVIDENCE_OUT] markers found:")
        for item in empty_markers:
            print(f"- {item}")
        print("[FINALIZE] run CANoe scenarios and export Write Window evidence lines before finalize.")
        return 2

    if not args.skip_fill_score:
        for tier in tiers:
            fill_cmd = [
                sys.executable,
                str(SCRIPT_DIR / "run_verification_pipeline.py"),
                "fill-score",
                "--run-id",
                args.run_id,
                "--tier",
                tier,
                "--owner",
                args.owner,
                "--run-date",
                args.run_date,
                "--evidence-root",
                str(args.evidence_root),
            ]
            if args.no_strict_metadata:
                fill_cmd.append("--no-strict-metadata")
            if args.no_strict_axis:
                fill_cmd.append("--no-strict-axis")
            rc = run_cmd(fill_cmd)
            if rc != 0:
                print(f"[FINALIZE] fill-score failed for tier={tier}")
                return rc

    insight_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_verification_pipeline.py"),
        "insight",
        "--run-id",
        args.run_id,
        "--evidence-root",
        str(args.evidence_root),
        "--output-md",
        str(args.insight_md),
        "--output-json",
        str(args.insight_json),
    ]
    if args.baseline_run_id:
        insight_cmd.extend(["--baseline-run-id", args.baseline_run_id])
    rc = run_cmd(insight_cmd)
    if rc != 0:
        print("[FINALIZE] insight step failed")
        return rc

    fill_template_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_verification_pipeline.py"),
        "fill-template",
        "--run-id",
        args.run_id,
        "--evidence-root",
        str(args.evidence_root),
        "--docs-root",
        str(args.docs_root),
        "--owner-fallback",
        args.owner_fallback or args.owner,
        "--date-fallback",
        args.date_fallback or args.run_date,
        "--binding-csv",
        str(args.binding_csv),
        "--binding-json",
        str(args.binding_json),
        "--binding-md",
        str(args.binding_md),
        "--output-csv",
        str(args.fill_csv),
        "--output-md",
        str(args.fill_md),
    ]
    rc = run_cmd(fill_template_cmd)
    if rc != 0:
        print("[FINALIZE] fill-template step failed")
        return rc

    print(
        f"[FINALIZE] completed run_id={args.run_id} tiers={tiers} "
        f"insight={args.insight_md} fill={args.fill_csv}"
    )
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "check_run_readiness.py"),
        "--run-id",
        args.run_id,
        "--evidence-root",
        str(args.evidence_root),
        "--output-json",
        str(args.output_json),
        "--output-md",
        str(args.output_md),
    ]
    return run_cmd(cmd)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run simplified verification evidence workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare", help="Create UT/IT/ST run folder skeleton")
    p_prepare.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_prepare.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_prepare.set_defaults(func=cmd_prepare)

    p_collect = sub.add_parser("collect", help="Collect native reports and optional raw Write log for one tier run")
    p_collect.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_collect.add_argument("--tier", required=True, choices=["UT", "IT", "ST", "FULL"])
    p_collect.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_collect.add_argument("--raw-log-source", type=Path, default=None)
    p_collect.add_argument("--allow-missing-raw-log", action="store_true")
    p_collect.set_defaults(func=cmd_collect)

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

    p_post = sub.add_parser(
        "post-run",
        help="Collect native run artifacts and immediately fill/score one tier",
    )
    p_post.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_post.add_argument("--tier", required=True, choices=["UT", "IT", "ST"])
    p_post.add_argument("--owner", default="TBD")
    p_post.add_argument("--run-date", default=dt.date.today().isoformat())
    p_post.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_post.add_argument("--raw-log-source", type=Path, default=None)
    p_post.add_argument("--allow-missing-raw-log", action="store_true")
    p_post.add_argument(
        "--baseline-csv",
        type=Path,
        default=None,
        help="Optional baseline scored CSV for regression comparison",
    )
    p_post.add_argument("--no-strict-metadata", action="store_true")
    p_post.add_argument("--no-strict-axis", action="store_true")
    p_post.set_defaults(func=cmd_post_run)

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

    p_bind = sub.add_parser("bind-doc", help="Build 05/06/07 evidence binding bundle from scored logs")
    p_bind.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_bind.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_bind.add_argument("--docs-root", type=Path, default=REPO_ROOT / "driving-alert-workproducts")
    p_bind.add_argument(
        "--output-csv",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.csv",
    )
    p_bind.add_argument(
        "--output-json",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.json",
    )
    p_bind.add_argument(
        "--output-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.md",
    )
    p_bind.set_defaults(func=cmd_bind_doc)

    p_fill = sub.add_parser(
        "fill-template",
        help="Build doc fill template for 05/06/07 (Pass/Fail/owner/date/evidence links)",
    )
    p_fill.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p_fill.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_fill.add_argument("--docs-root", type=Path, default=REPO_ROOT / "driving-alert-workproducts")
    p_fill.add_argument(
        "--binding-csv",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.csv",
    )
    p_fill.add_argument(
        "--binding-json",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.json",
    )
    p_fill.add_argument(
        "--binding-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.md",
    )
    p_fill.add_argument("--owner-fallback", default="TBD")
    p_fill.add_argument("--date-fallback", default=dt.date.today().isoformat())
    p_fill.add_argument(
        "--output-csv",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_fill_template.csv",
    )
    p_fill.add_argument(
        "--output-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_fill_template.md",
    )
    p_fill.set_defaults(func=cmd_fill_template)

    p_finalize = sub.add_parser(
        "finalize",
        help="Run fill-score(UT/IT/ST), insight, and fill-template in one command",
    )
    p_finalize.add_argument("--run-id", required=True, help="Run ID, e.g. 20260307_1030")
    p_finalize.add_argument("--tiers", nargs="+", default=["UT", "IT", "ST"], choices=["UT", "IT", "ST"])
    p_finalize.add_argument("--owner", default="TBD")
    p_finalize.add_argument("--run-date", default=dt.date.today().isoformat())
    p_finalize.add_argument("--owner-fallback", default="")
    p_finalize.add_argument("--date-fallback", default="")
    p_finalize.add_argument("--baseline-run-id", default="", help="Optional baseline run ID for insight comparison")
    p_finalize.add_argument("--no-strict-metadata", action="store_true")
    p_finalize.add_argument("--no-strict-axis", action="store_true")
    p_finalize.add_argument(
        "--skip-fill-score",
        action="store_true",
        help="Assume per-tier post-run already produced scored outputs and skip re-running fill-score",
    )
    p_finalize.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_finalize.add_argument("--docs-root", type=Path, default=REPO_ROOT / "driving-alert-workproducts")
    p_finalize.add_argument(
        "--insight-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_insight_report.md",
    )
    p_finalize.add_argument(
        "--insight-json",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_insight_report.json",
    )
    p_finalize.add_argument(
        "--binding-csv",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.csv",
    )
    p_finalize.add_argument(
        "--binding-json",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.json",
    )
    p_finalize.add_argument(
        "--binding-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_binding_bundle.md",
    )
    p_finalize.add_argument(
        "--fill-csv",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_fill_template.csv",
    )
    p_finalize.add_argument(
        "--fill-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "doc_fill_template.md",
    )
    p_finalize.set_defaults(func=cmd_finalize)

    p_status = sub.add_parser("status", help="Check run readiness for finalize workflow")
    p_status.add_argument("--run-id", required=True, help="Run ID, e.g. 20260307_1030")
    p_status.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    p_status.add_argument(
        "--output-json",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_readiness.json",
    )
    p_status.add_argument(
        "--output-md",
        type=Path,
        default=REPO_ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_readiness.md",
    )
    p_status.set_defaults(func=cmd_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

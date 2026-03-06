#!/usr/bin/env python3
"""Single entrypoint for common development scripts.

This keeps day-to-day usage simple:
  - verification workflow
  - quality gates

Low-level scripts remain in their original folders.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run_cmd(args: list[str]) -> int:
    print("[RUN]", " ".join(args))
    proc = subprocess.run(args, cwd=ROOT)
    return proc.returncode


def cmd_verify_prepare(args: argparse.Namespace) -> int:
    return run_cmd(
        [
            sys.executable,
            str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
            "prepare",
            "--run-id",
            args.run_id,
        ]
    )


def cmd_verify_smoke(args: argparse.Namespace) -> int:
    return run_cmd(
        [
            sys.executable,
            str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
            "smoke",
            "--owner",
            args.owner,
            "--run-date",
            args.run_date,
        ]
    )


def cmd_verify_fill_score(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
        "fill-score",
        "--tier",
        args.tier,
        "--run-id",
        args.run_id,
        "--owner",
        args.owner,
        "--run-date",
        args.run_date,
    ]
    if args.no_strict_metadata:
        cmd.append("--no-strict-metadata")
    if args.no_strict_axis:
        cmd.append("--no-strict-axis")
    return run_cmd(cmd)


def cmd_gate_doc_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "quality" / "doc_code_sync_gate.py")])


def cmd_gate_cfg_hygiene(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "quality" / "cfg_hygiene_gate.py")])


def cmd_gate_capl_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "quality" / "check_capl_sync.py")])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified script launcher")
    sub = parser.add_subparsers(dest="command", required=True)

    verify_prepare = sub.add_parser("verify-prepare", help="Create UT/IT/ST evidence run folders")
    verify_prepare.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    verify_prepare.set_defaults(func=cmd_verify_prepare)

    verify_smoke = sub.add_parser("verify-smoke", help="Run CANoe COM smoke checks")
    verify_smoke.add_argument("--owner", default="TBD")
    verify_smoke.add_argument("--run-date", default=dt.date.today().isoformat())
    verify_smoke.set_defaults(func=cmd_verify_smoke)

    verify_fill = sub.add_parser("verify-fill-score", help="Fill and score one tier")
    verify_fill.add_argument("--tier", required=True, choices=["UT", "IT", "ST"])
    verify_fill.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    verify_fill.add_argument("--owner", default="TBD")
    verify_fill.add_argument("--run-date", default=dt.date.today().isoformat())
    verify_fill.add_argument("--no-strict-metadata", action="store_true")
    verify_fill.add_argument("--no-strict-axis", action="store_true")
    verify_fill.set_defaults(func=cmd_verify_fill_score)

    gate_doc = sub.add_parser("gate-doc-sync", help="Run Req-Doc-Code sync gate")
    gate_doc.set_defaults(func=cmd_gate_doc_sync)

    gate_cfg = sub.add_parser("gate-cfg-hygiene", help="Run cfg text hygiene gate")
    gate_cfg.set_defaults(func=cmd_gate_cfg_hygiene)

    gate_capl = sub.add_parser("gate-capl-sync", help="Run src/capl vs cfg/channel_assign sync gate")
    gate_capl.set_defaults(func=cmd_gate_capl_sync)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

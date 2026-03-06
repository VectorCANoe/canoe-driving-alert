#!/usr/bin/env python3
"""Unified script launcher.

Canonical command contract:
  - verify prepare
  - verify smoke
  - verify fill-score
  - gate doc-sync
  - gate cfg-hygiene
  - gate capl-sync
  - package build-exe

Legacy aliases are kept for compatibility:
  - verify-prepare
  - verify-smoke
  - verify-fill-score
  - gate-doc-sync
  - gate-cfg-hygiene
  - gate-capl-sync
  - package-build-exe
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

CONTRACT_CANONICAL = [
    "python scripts/run.py verify prepare --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify smoke --owner <OWNER>",
    "python scripts/run.py verify fill-score --tier <UT|IT|ST> --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py gate doc-sync",
    "python scripts/run.py gate cfg-hygiene",
    "python scripts/run.py gate capl-sync",
    "python scripts/run.py gate cli-readiness",
    "python scripts/run.py package build-exe --mode onefolder",
]

CONTRACT_LEGACY = [
    "verify-prepare",
    "verify-smoke",
    "verify-fill-score",
    "gate-doc-sync",
    "gate-cfg-hygiene",
    "gate-capl-sync",
    "gate-cli-readiness",
    "package-build-exe",
]


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
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "doc_code_sync_gate.py")])


def cmd_gate_cfg_hygiene(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "cfg_hygiene_gate.py")])


def cmd_gate_capl_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "check_capl_sync.py")])


def cmd_gate_cli_readiness(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "cli_readiness_gate.py")])


def cmd_contract(args: argparse.Namespace) -> int:
    if args.json:
        payload = {"canonical": CONTRACT_CANONICAL, "legacy": CONTRACT_LEGACY}
        print(json.dumps(payload, indent=2))
        return 0

    print("Canonical commands:")
    for item in CONTRACT_CANONICAL:
        print(f"  {item}")
    return 0


def cmd_package_build_exe(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "release" / "build_sdv_exe.py"),
        "--mode",
        args.mode,
    ]
    if args.clean:
        cmd.append("--clean")
    return run_cmd(cmd)


def add_verify_prepare_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.set_defaults(func=cmd_verify_prepare)


def add_verify_smoke_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.set_defaults(func=cmd_verify_smoke)


def add_verify_fill_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--tier", required=True, choices=["UT", "IT", "ST"])
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--no-strict-metadata", action="store_true")
    p.add_argument("--no-strict-axis", action="store_true")
    p.set_defaults(func=cmd_verify_fill_score)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified script launcher")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="Verification pipeline commands")
    verify_sub = verify.add_subparsers(dest="verify_command", required=True)
    add_verify_prepare_args(verify_sub.add_parser("prepare", help="Create UT/IT/ST evidence run folders"))
    add_verify_smoke_args(verify_sub.add_parser("smoke", help="Run CANoe COM smoke checks"))
    add_verify_fill_args(verify_sub.add_parser("fill-score", help="Fill and score one tier"))

    gate = sub.add_parser("gate", help="Quality gate commands")
    gate_sub = gate.add_subparsers(dest="gate_command", required=True)
    gate_sub.add_parser("doc-sync", help="Run Req-Doc-Code sync gate").set_defaults(func=cmd_gate_doc_sync)
    gate_sub.add_parser("cfg-hygiene", help="Run cfg text hygiene gate").set_defaults(func=cmd_gate_cfg_hygiene)
    gate_sub.add_parser("capl-sync", help="Run src/capl vs cfg/channel_assign sync gate").set_defaults(func=cmd_gate_capl_sync)
    gate_sub.add_parser("cli-readiness", help="Run CLI readiness gate before GUI phase").set_defaults(func=cmd_gate_cli_readiness)

    package = sub.add_parser("package", help="Build/distribution commands")
    package_sub = package.add_subparsers(dest="package_command", required=True)
    pkg_build = package_sub.add_parser("build-exe", help="Build Windows exe bundle via PyInstaller")
    pkg_build.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_build.add_argument("--clean", action="store_true")
    pkg_build.set_defaults(func=cmd_package_build_exe)

    contract = sub.add_parser("contract", help="Show canonical command contract")
    contract.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    contract.set_defaults(func=cmd_contract)

    # Legacy aliases (kept for compatibility during migration)
    add_verify_prepare_args(sub.add_parser("verify-prepare", help="Legacy alias: verify prepare"))
    add_verify_smoke_args(sub.add_parser("verify-smoke", help="Legacy alias: verify smoke"))
    add_verify_fill_args(sub.add_parser("verify-fill-score", help="Legacy alias: verify fill-score"))
    sub.add_parser("gate-doc-sync", help="Legacy alias: gate doc-sync").set_defaults(func=cmd_gate_doc_sync)
    sub.add_parser("gate-cfg-hygiene", help="Legacy alias: gate cfg-hygiene").set_defaults(func=cmd_gate_cfg_hygiene)
    sub.add_parser("gate-capl-sync", help="Legacy alias: gate capl-sync").set_defaults(func=cmd_gate_capl_sync)
    sub.add_parser("gate-cli-readiness", help="Legacy alias: gate cli-readiness").set_defaults(func=cmd_gate_cli_readiness)
    pkg_build_legacy = sub.add_parser("package-build-exe", help="Legacy alias: package build-exe")
    pkg_build_legacy.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_build_legacy.add_argument("--clean", action="store_true")
    pkg_build_legacy.set_defaults(func=cmd_package_build_exe)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

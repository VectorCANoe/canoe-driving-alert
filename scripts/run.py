#!/usr/bin/env python3
"""Unified script launcher.

Canonical command contract:
  - scenario run
  - verify prepare
  - verify smoke
  - verify fill-score
  - gate doc-sync
  - gate cfg-hygiene
  - gate capl-sync
  - verify fill-template
  - verify status
  - verify finalize
  - package build-exe
  - package bundle-portable

Legacy aliases are kept for compatibility:
  - scenario-run
  - verify-prepare
  - verify-smoke
  - verify-fill-score
  - verify-fill-template
  - verify-status
  - verify-finalize
  - gate-doc-sync
  - gate-cfg-hygiene
  - gate-capl-sync
  - package-build-exe
  - package-bundle-portable
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
    "python scripts/run.py scenario run --id <0..255>",
    "python scripts/run.py verify prepare --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify smoke --owner <OWNER>",
    "python scripts/run.py verify fill-score --tier <UT|IT|ST> --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py verify insight --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify bind-doc --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify fill-template --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify status --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify finalize --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py gate doc-sync",
    "python scripts/run.py gate cfg-hygiene",
    "python scripts/run.py gate capl-sync",
    "python scripts/run.py gate multibus-dbc",
    "python scripts/run.py gate cli-readiness",
    "python scripts/run.py package build-exe --mode onefolder",
    "python scripts/run.py package bundle-portable",
]

CONTRACT_LEGACY = [
    "scenario-run",
    "verify-prepare",
    "verify-smoke",
    "verify-fill-score",
    "verify-insight",
    "verify-bind-doc",
    "verify-fill-template",
    "verify-status",
    "verify-finalize",
    "gate-doc-sync",
    "gate-cfg-hygiene",
    "gate-capl-sync",
    "gate-multibus-dbc",
    "gate-cli-readiness",
    "package-build-exe",
    "package-bundle-portable",
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
    if args.baseline_csv:
        cmd.extend(["--baseline-csv", str(args.baseline_csv)])
    return run_cmd(cmd)


def cmd_verify_insight(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
        "insight",
        "--run-id",
        args.run_id,
        "--output-md",
        str(args.output_md),
        "--output-json",
        str(args.output_json),
    ]
    if args.baseline_run_id:
        cmd.extend(["--baseline-run-id", args.baseline_run_id])
    if args.evidence_root:
        cmd.extend(["--evidence-root", str(args.evidence_root)])
    return run_cmd(cmd)


def cmd_verify_bind_doc(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
        "bind-doc",
        "--run-id",
        args.run_id,
        "--output-csv",
        str(args.output_csv),
        "--output-json",
        str(args.output_json),
        "--output-md",
        str(args.output_md),
    ]
    if args.evidence_root:
        cmd.extend(["--evidence-root", str(args.evidence_root)])
    if args.docs_root:
        cmd.extend(["--docs-root", str(args.docs_root)])
    return run_cmd(cmd)


def cmd_verify_fill_template(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
        "fill-template",
        "--run-id",
        args.run_id,
        "--owner-fallback",
        args.owner_fallback,
        "--date-fallback",
        args.date_fallback,
        "--binding-csv",
        str(args.binding_csv),
        "--binding-json",
        str(args.binding_json),
        "--binding-md",
        str(args.binding_md),
        "--output-csv",
        str(args.output_csv),
        "--output-md",
        str(args.output_md),
    ]
    if args.evidence_root:
        cmd.extend(["--evidence-root", str(args.evidence_root)])
    if args.docs_root:
        cmd.extend(["--docs-root", str(args.docs_root)])
    return run_cmd(cmd)


def cmd_verify_finalize(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
        "finalize",
        "--run-id",
        args.run_id,
        "--tiers",
        *args.tiers,
        "--owner",
        args.owner,
        "--run-date",
        args.run_date,
        "--owner-fallback",
        args.owner_fallback,
        "--date-fallback",
        args.date_fallback,
        "--insight-md",
        str(args.insight_md),
        "--insight-json",
        str(args.insight_json),
        "--binding-csv",
        str(args.binding_csv),
        "--binding-json",
        str(args.binding_json),
        "--binding-md",
        str(args.binding_md),
        "--fill-csv",
        str(args.fill_csv),
        "--fill-md",
        str(args.fill_md),
    ]
    if args.evidence_root:
        cmd.extend(["--evidence-root", str(args.evidence_root)])
    if args.docs_root:
        cmd.extend(["--docs-root", str(args.docs_root)])
    if args.baseline_run_id:
        cmd.extend(["--baseline-run-id", args.baseline_run_id])
    if args.no_strict_metadata:
        cmd.append("--no-strict-metadata")
    if args.no_strict_axis:
        cmd.append("--no-strict-axis")
    return run_cmd(cmd)


def cmd_verify_status(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "quality" / "run_verification_pipeline.py"),
        "status",
        "--run-id",
        args.run_id,
        "--output-json",
        str(args.output_json),
        "--output-md",
        str(args.output_md),
    ]
    if args.evidence_root:
        cmd.extend(["--evidence-root", str(args.evidence_root)])
    return run_cmd(cmd)


def cmd_scenario_run(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "canoe" / "send_scenario_command.py"),
        "--id",
        str(args.id),
        "--namespace",
        args.namespace,
        "--var",
        args.var,
        "--ack-var",
        args.ack_var,
        "--wait-ack-ms",
        str(args.wait_ack_ms),
        "--poll-ms",
        str(args.poll_ms),
    ]
    if args.no_ensure_running:
        cmd.append("--no-ensure-running")
    return run_cmd(cmd)


def cmd_gate_doc_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "doc_code_sync_gate.py")])


def cmd_gate_cfg_hygiene(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "cfg_hygiene_gate.py")])


def cmd_gate_capl_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "check_capl_sync.py")])


def cmd_gate_multibus_dbc(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / "gates" / "multibus_cfg_dbc_gate.py")])


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


def cmd_package_bundle_portable(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / "release" / "build_portable_bundle.py"),
    ]
    if args.clean:
        cmd.append("--clean")
    if args.rebuild_exe:
        cmd.append("--rebuild-exe")
    if args.mode:
        cmd.extend(["--mode", args.mode])
    if args.output_dir:
        cmd.extend(["--output-dir", args.output_dir])
    if args.bundle_name:
        cmd.extend(["--bundle-name", args.bundle_name])
    if args.zip_name:
        cmd.extend(["--zip-name", args.zip_name])
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
    p.add_argument("--baseline-csv", default="", help="Optional baseline scored CSV for regression comparison")
    p.add_argument("--no-strict-metadata", action="store_true")
    p.add_argument("--no-strict-axis", action="store_true")
    p.set_defaults(func=cmd_verify_fill_score)


def add_verify_insight_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--baseline-run-id", default="", help="Optional baseline run ID for trend comparison")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/run_insight_report.md",
        help="Run-level insight markdown output path",
    )
    p.add_argument(
        "--output-json",
        default="canoe/tmp/reports/verification/run_insight_report.json",
        help="Run-level insight JSON output path",
    )
    p.set_defaults(func=cmd_verify_insight)


def add_verify_bind_doc_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--docs-root",
        default="",
        help="Optional docs root path (default: driving-situation-alert)",
    )
    p.add_argument(
        "--output-csv",
        default="canoe/tmp/reports/verification/doc_binding_bundle.csv",
        help="05/06/07 doc binding CSV output path",
    )
    p.add_argument(
        "--output-json",
        default="canoe/tmp/reports/verification/doc_binding_bundle.json",
        help="05/06/07 doc binding JSON output path",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/doc_binding_bundle.md",
        help="05/06/07 doc binding markdown output path",
    )
    p.set_defaults(func=cmd_verify_bind_doc)


def add_verify_fill_template_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--docs-root",
        default="",
        help="Optional docs root path (default: driving-situation-alert)",
    )
    p.add_argument("--owner-fallback", default="TBD", help="Fallback owner for READY rows")
    p.add_argument("--date-fallback", default=dt.date.today().isoformat(), help="Fallback date for READY rows")
    p.add_argument(
        "--binding-csv",
        default="canoe/tmp/reports/verification/doc_binding_bundle.csv",
        help="Binding CSV output path",
    )
    p.add_argument(
        "--binding-json",
        default="canoe/tmp/reports/verification/doc_binding_bundle.json",
        help="Binding JSON output path",
    )
    p.add_argument(
        "--binding-md",
        default="canoe/tmp/reports/verification/doc_binding_bundle.md",
        help="Binding markdown output path",
    )
    p.add_argument(
        "--output-csv",
        default="canoe/tmp/reports/verification/doc_fill_template.csv",
        help="Doc fill template CSV output path",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/doc_fill_template.md",
        help="Doc fill template markdown output path",
    )
    p.set_defaults(func=cmd_verify_fill_template)


def add_verify_finalize_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--tiers", nargs="+", default=["UT", "IT", "ST"], choices=["UT", "IT", "ST"])
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--owner-fallback", default="")
    p.add_argument("--date-fallback", default="")
    p.add_argument("--baseline-run-id", default="", help="Optional baseline run ID for insight comparison")
    p.add_argument("--no-strict-metadata", action="store_true")
    p.add_argument("--no-strict-axis", action="store_true")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--docs-root",
        default="",
        help="Optional docs root path (default: driving-situation-alert)",
    )
    p.add_argument(
        "--insight-md",
        default="canoe/tmp/reports/verification/run_insight_report.md",
        help="Run-level insight markdown output path",
    )
    p.add_argument(
        "--insight-json",
        default="canoe/tmp/reports/verification/run_insight_report.json",
        help="Run-level insight JSON output path",
    )
    p.add_argument(
        "--binding-csv",
        default="canoe/tmp/reports/verification/doc_binding_bundle.csv",
        help="Doc binding CSV output path",
    )
    p.add_argument(
        "--binding-json",
        default="canoe/tmp/reports/verification/doc_binding_bundle.json",
        help="Doc binding JSON output path",
    )
    p.add_argument(
        "--binding-md",
        default="canoe/tmp/reports/verification/doc_binding_bundle.md",
        help="Doc binding markdown output path",
    )
    p.add_argument(
        "--fill-csv",
        default="canoe/tmp/reports/verification/doc_fill_template.csv",
        help="Doc fill template CSV output path",
    )
    p.add_argument(
        "--fill-md",
        default="canoe/tmp/reports/verification/doc_fill_template.md",
        help="Doc fill template markdown output path",
    )
    p.set_defaults(func=cmd_verify_finalize)


def add_verify_status_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument(
        "--evidence-root",
        default="",
        help="Optional evidence root path (default pipeline root is used when omitted)",
    )
    p.add_argument(
        "--output-json",
        default="canoe/tmp/reports/verification/run_readiness.json",
        help="Run readiness JSON output path",
    )
    p.add_argument(
        "--output-md",
        default="canoe/tmp/reports/verification/run_readiness.md",
        help="Run readiness markdown output path",
    )
    p.set_defaults(func=cmd_verify_status)


def add_scenario_run_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--id", type=int, required=True, help="Scenario ID (0..255)")
    p.add_argument("--namespace", default="Test", help="System variable namespace")
    p.add_argument(
        "--var",
        default="scenarioCommand",
        choices=["scenarioCommand", "testScenario"],
        help="Target sysvar name",
    )
    p.add_argument("--ack-var", default="scenarioCommandAck", help="Ack sysvar name")
    p.add_argument("--wait-ack-ms", type=int, default=1200, help="Ack wait timeout in ms")
    p.add_argument("--poll-ms", type=int, default=20, help="Ack poll interval in ms")
    p.add_argument("--no-ensure-running", action="store_true", help="Do not auto-start measurement")
    p.set_defaults(func=cmd_scenario_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified script launcher")
    sub = parser.add_subparsers(dest="command", required=True)

    scenario = sub.add_parser("scenario", help="Manual scenario trigger commands (no panel)")
    scenario_sub = scenario.add_subparsers(dest="scenario_command", required=True)
    add_scenario_run_args(scenario_sub.add_parser("run", help="Send scenario command via CANoe COM"))

    verify = sub.add_parser("verify", help="Verification pipeline commands")
    verify_sub = verify.add_subparsers(dest="verify_command", required=True)
    add_verify_prepare_args(verify_sub.add_parser("prepare", help="Create UT/IT/ST evidence run folders"))
    add_verify_smoke_args(verify_sub.add_parser("smoke", help="Run CANoe COM smoke checks"))
    add_verify_fill_args(verify_sub.add_parser("fill-score", help="Fill and score one tier"))
    add_verify_insight_args(verify_sub.add_parser("insight", help="Build run-level insight report"))
    add_verify_bind_doc_args(verify_sub.add_parser("bind-doc", help="Build 05/06/07 doc binding bundle"))
    add_verify_fill_template_args(verify_sub.add_parser("fill-template", help="Build 05/06/07 doc fill template"))
    add_verify_status_args(verify_sub.add_parser("status", help="Check run readiness before finalize"))
    add_verify_finalize_args(verify_sub.add_parser("finalize", help="Run full post-run verification bundle"))

    gate = sub.add_parser("gate", help="Quality gate commands")
    gate_sub = gate.add_subparsers(dest="gate_command", required=True)
    gate_sub.add_parser("doc-sync", help="Run Req-Doc-Code sync gate").set_defaults(func=cmd_gate_doc_sync)
    gate_sub.add_parser("cfg-hygiene", help="Run cfg text hygiene gate").set_defaults(func=cmd_gate_cfg_hygiene)
    gate_sub.add_parser("capl-sync", help="Run src/capl vs cfg/channel_assign sync gate").set_defaults(func=cmd_gate_capl_sync)
    gate_sub.add_parser("multibus-dbc", help="Run multi-bus cfg + DBC domain policy gate").set_defaults(func=cmd_gate_multibus_dbc)
    gate_sub.add_parser("cli-readiness", help="Run CLI readiness gate before GUI phase").set_defaults(func=cmd_gate_cli_readiness)

    package = sub.add_parser("package", help="Build/distribution commands")
    package_sub = package.add_subparsers(dest="package_command", required=True)
    pkg_build = package_sub.add_parser("build-exe", help="Build Windows exe bundle via PyInstaller")
    pkg_build.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_build.add_argument("--clean", action="store_true")
    pkg_build.set_defaults(func=cmd_package_build_exe)

    pkg_portable = package_sub.add_parser(
        "bundle-portable",
        help="Create portable ZIP (exe + required runtime files)",
    )
    pkg_portable.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_portable.add_argument("--clean", action="store_true")
    pkg_portable.add_argument("--rebuild-exe", action="store_true")
    pkg_portable.add_argument("--output-dir", default="")
    pkg_portable.add_argument("--bundle-name", default="")
    pkg_portable.add_argument("--zip-name", default="")
    pkg_portable.set_defaults(func=cmd_package_bundle_portable)

    contract = sub.add_parser("contract", help="Show canonical command contract")
    contract.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    contract.set_defaults(func=cmd_contract)

    add_scenario_run_args(sub.add_parser("scenario-run", help="Legacy alias: scenario run"))

    # Legacy aliases (kept for compatibility during migration)
    add_verify_prepare_args(sub.add_parser("verify-prepare", help="Legacy alias: verify prepare"))
    add_verify_smoke_args(sub.add_parser("verify-smoke", help="Legacy alias: verify smoke"))
    add_verify_fill_args(sub.add_parser("verify-fill-score", help="Legacy alias: verify fill-score"))
    add_verify_insight_args(sub.add_parser("verify-insight", help="Legacy alias: verify insight"))
    add_verify_bind_doc_args(sub.add_parser("verify-bind-doc", help="Legacy alias: verify bind-doc"))
    add_verify_fill_template_args(sub.add_parser("verify-fill-template", help="Legacy alias: verify fill-template"))
    add_verify_status_args(sub.add_parser("verify-status", help="Legacy alias: verify status"))
    add_verify_finalize_args(sub.add_parser("verify-finalize", help="Legacy alias: verify finalize"))
    sub.add_parser("gate-doc-sync", help="Legacy alias: gate doc-sync").set_defaults(func=cmd_gate_doc_sync)
    sub.add_parser("gate-cfg-hygiene", help="Legacy alias: gate cfg-hygiene").set_defaults(func=cmd_gate_cfg_hygiene)
    sub.add_parser("gate-capl-sync", help="Legacy alias: gate capl-sync").set_defaults(func=cmd_gate_capl_sync)
    sub.add_parser("gate-multibus-dbc", help="Legacy alias: gate multibus-dbc").set_defaults(func=cmd_gate_multibus_dbc)
    sub.add_parser("gate-cli-readiness", help="Legacy alias: gate cli-readiness").set_defaults(func=cmd_gate_cli_readiness)
    pkg_build_legacy = sub.add_parser("package-build-exe", help="Legacy alias: package build-exe")
    pkg_build_legacy.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_build_legacy.add_argument("--clean", action="store_true")
    pkg_build_legacy.set_defaults(func=cmd_package_build_exe)
    pkg_portable_legacy = sub.add_parser("package-bundle-portable", help="Legacy alias: package bundle-portable")
    pkg_portable_legacy.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    pkg_portable_legacy.add_argument("--clean", action="store_true")
    pkg_portable_legacy.add_argument("--rebuild-exe", action="store_true")
    pkg_portable_legacy.add_argument("--output-dir", default="")
    pkg_portable_legacy.add_argument("--bundle-name", default="")
    pkg_portable_legacy.add_argument("--zip-name", default="")
    pkg_portable_legacy.set_defaults(func=cmd_package_bundle_portable)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

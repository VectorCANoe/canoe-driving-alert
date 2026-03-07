#!/usr/bin/env python3
"""Unified script launcher.

Canonical command contract:
  - shell
  - scenario run
  - verify prepare
  - verify batch
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
  - wizard
  - interactive
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
import csv
import datetime as dt
import difflib
import json
import shlex
import subprocess
import sys
from pathlib import Path

from cliops.canoe_com import CanoeComBridge, CanoeComError
from cliops.platform_caps import canoe_runtime_check, platform_label, require_canoe_runtime

try:
    import questionary
except Exception:  # optional dependency
    questionary = None

try:
    from rich.console import Console
    from rich.panel import Panel
except Exception:  # optional dependency
    Console = None
    Panel = None


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
_RICH_CONSOLE = Console() if Console is not None else None
SHELL_HISTORY_FILE = ROOT / "canoe" / "tmp" / "reports" / "verification" / "cli_shell_history.jsonl"

CONTRACT_CANONICAL = [
    "python scripts/run.py",
    "python scripts/run.py shell",
    "python scripts/run.py start demo --id <0..255>",
    "python scripts/run.py start precheck --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py doctor",
    "python scripts/run.py capl sysvar-get --namespace <NS> --var <NAME>",
    "python scripts/run.py capl sysvar-set --namespace <NS> --var <NAME> --value <V> --value-type int",
    "python scripts/run.py canoe measure-status",
    "python scripts/run.py canoe capl-call --function-name <CAPL_FN> --args <A1> <A2>",
    "python scripts/run.py evidence status --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py release portable",
    "python scripts/run.py shell",
    "python scripts/run.py scenario run --id <0..255>",
    "python scripts/run.py verify prepare --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify batch --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
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
    "wizard",
    "interactive",
    "start",
    "doctor",
    "evidence",
    "release",
    "scenario-run",
    "verify-prepare",
    "verify-batch",
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


TOPLEVEL_COMMANDS = [
    "start",
    "doctor",
    "capl",
    "canoe",
    "shell",
    "wizard",
    "scenario",
    "verify",
    "evidence",
    "gate",
    "package",
    "release",
    "contract",
    "scenario-run",
    "interactive",
    "verify-prepare",
    "verify-batch",
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
    # Short aliases
    "go",
    "demo",
    "precheck",
    "mstart",
    "mstop",
    "mstatus",
]

SHELL_PALETTE_GROUPS: dict[str, list[tuple[str, str]]] = {
    "Operate": [
        ("/start guided", "Open guided operator menu"),
        ("/scenario 4", "Trigger default scenarioCommand=4"),
        ("/canoe measure status", "Check CANoe measurement status"),
        ("/canoe measure start", "Start CANoe measurement"),
        ("/canoe measure stop", "Stop CANoe measurement"),
    ],
    "Verify": [
        ("/start precheck", "Run gate+prepare+smoke+status precheck flow"),
        ("/verify quick", "Run verify prepare+smoke+status"),
        ("/verify status", "Check evidence readiness report"),
        ("/gate all", "Run full gate set"),
    ],
    "Inspect": [
        ("/doctor", "Run CANoe COM and sysvar readiness checks"),
        ("/capl get Core failSafeMode", "Read one sysvar via COM"),
        ("/capl set Test scenarioCommand 4 int", "Write one sysvar via COM"),
        ("/contract", "Print canonical command contract"),
        ("/history", "Show recent shell command history"),
        ("/repeat 1", "Repeat last executed command"),
    ],
    "Package": [
        ("/package portable onefolder", "Build portable bundle"),
        ("/package exe onefolder", "Build Windows exe bundle"),
    ],
    "Session": [
        ("/exit", "Exit shell"),
    ],
}


def run_cmd(args: list[str]) -> int:
    print("[RUN]", " ".join(args))
    proc = subprocess.run(args, cwd=ROOT)
    return proc.returncode


def _fail_unavailable(action_name: str) -> int:
    message = require_canoe_runtime(action_name)
    if message:
        print(f"[PLATFORM] {message}")
        print("[PLATFORM] available everywhere: gate/verify/evidence/package/report commands")
        return 2
    return 0


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


def _batch_artifact_rows(run_id: str) -> list[dict[str, object]]:
    paths = [
        f"canoe/logging/evidence/UT/{run_id}/verification_log.csv",
        f"canoe/logging/evidence/UT/{run_id}/verification_log_scored.csv",
        f"canoe/logging/evidence/IT/{run_id}/verification_log.csv",
        f"canoe/logging/evidence/IT/{run_id}/verification_log_scored.csv",
        f"canoe/logging/evidence/ST/{run_id}/verification_log.csv",
        f"canoe/logging/evidence/ST/{run_id}/verification_log_scored.csv",
        "canoe/tmp/reports/verification/dev_completeness_smoke.csv",
        "canoe/tmp/reports/verification/dev_completeness_smoke.md",
        "canoe/tmp/reports/verification/run_readiness.json",
        "canoe/tmp/reports/verification/run_readiness.md",
        "canoe/tmp/reports/verification/run_insight_report.json",
        "canoe/tmp/reports/verification/run_insight_report.md",
        "canoe/tmp/reports/verification/doc_binding_bundle.json",
        "canoe/tmp/reports/verification/doc_binding_bundle.md",
        "canoe/tmp/reports/verification/doc_fill_template.csv",
        "canoe/tmp/reports/verification/doc_fill_template.md",
    ]
    rows: list[dict[str, object]] = []
    for rel in paths:
        p = ROOT / rel
        exists = p.exists()
        size = p.stat().st_size if exists and p.is_file() else 0
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime).isoformat() if exists else ""
        rows.append(
            {
                "path": rel,
                "exists": exists,
                "size_bytes": size,
                "last_modified": mtime,
            }
        )
    return rows


def _normalize_report_formats(raw: str) -> list[str]:
    allowed = {"json", "md", "csv"}
    parts = [item.strip().lower() for item in raw.split(",") if item.strip()]
    if not parts:
        return ["json", "md"]
    out: list[str] = []
    for item in parts:
        if item not in allowed:
            raise ValueError(f"invalid report format: {item} (allowed: json,md,csv)")
        if item not in out:
            out.append(item)
    return out


def _write_batch_report(
    *,
    run_id: str,
    owner: str,
    run_date: str,
    phase: str,
    steps: list[dict[str, object]],
    report_formats: list[str],
    output_json: Path,
    output_md: Path,
    output_csv: Path,
) -> None:
    if "json" in report_formats:
        output_json.parent.mkdir(parents=True, exist_ok=True)
    if "md" in report_formats:
        output_md.parent.mkdir(parents=True, exist_ok=True)
    if "csv" in report_formats:
        output_csv.parent.mkdir(parents=True, exist_ok=True)

    pass_count = sum(1 for s in steps if s.get("rc") == 0)
    fail_count = len(steps) - pass_count
    status = "PASS" if fail_count == 0 else "FAIL"
    artifacts = _batch_artifact_rows(run_id)

    payload = {
        "run_id": run_id,
        "owner": owner,
        "run_date": run_date,
        "phase": phase,
        "status": status,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "steps": steps,
        "artifacts": artifacts,
        "generated_at": dt.datetime.now().isoformat(),
    }
    if "json" in report_formats:
        output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if "md" in report_formats:
        lines = [
            "# Dev2 Batch Verification Report",
            "",
            f"- run_id: `{run_id}`",
            f"- owner: `{owner}`",
            f"- run_date: `{run_date}`",
            f"- phase: `{phase}`",
            f"- status: `{status}`",
            f"- pass/fail: `{pass_count}/{fail_count}`",
            "",
            "## Step Results",
            "",
            "| step | rc |",
            "|---|---|",
        ]
        for step in steps:
            lines.append(f"| `{step['name']}` | `{step['rc']}` |")
        lines.extend(["", "## Artifact Snapshot", "", "| path | exists | size_bytes |", "|---|---:|---:|"])
        for row in artifacts:
            lines.append(f"| `{row['path']}` | `{str(row['exists']).lower()}` | `{row['size_bytes']}` |")
        output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if "csv" in report_formats:
        with output_csv.open("w", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(
                fp,
                fieldnames=[
                    "row_type",
                    "run_id",
                    "phase",
                    "owner",
                    "run_date",
                    "status",
                    "step_name",
                    "step_rc",
                    "artifact_path",
                    "artifact_exists",
                    "artifact_size_bytes",
                    "artifact_last_modified",
                ],
            )
            writer.writeheader()
            for step in steps:
                writer.writerow(
                    {
                        "row_type": "step",
                        "run_id": run_id,
                        "phase": phase,
                        "owner": owner,
                        "run_date": run_date,
                        "status": status,
                        "step_name": step["name"],
                        "step_rc": step["rc"],
                        "artifact_path": "",
                        "artifact_exists": "",
                        "artifact_size_bytes": "",
                        "artifact_last_modified": "",
                    }
                )
            for row in artifacts:
                writer.writerow(
                    {
                        "row_type": "artifact",
                        "run_id": run_id,
                        "phase": phase,
                        "owner": owner,
                        "run_date": run_date,
                        "status": status,
                        "step_name": "",
                        "step_rc": "",
                        "artifact_path": row["path"],
                        "artifact_exists": str(row["exists"]).lower(),
                        "artifact_size_bytes": row["size_bytes"],
                        "artifact_last_modified": row["last_modified"],
                    }
                )


def cmd_verify_batch(args: argparse.Namespace) -> int:
    try:
        report_formats = _normalize_report_formats(args.report_formats)
    except ValueError as ex:
        print(f"[VERIFY_BATCH] FAIL: {ex}")
        return 2

    steps: list[dict[str, object]] = []

    def run_step(name: str, fn) -> int:
        rc = fn()
        steps.append({"name": name, "rc": rc})
        return rc

    if args.phase in {"pre", "full"}:
        if not args.skip_gates:
            gate_steps = [
                ("gate doc-sync", lambda: cmd_gate_doc_sync(argparse.Namespace())),
                ("gate cfg-hygiene", lambda: cmd_gate_cfg_hygiene(argparse.Namespace())),
                ("gate capl-sync", lambda: cmd_gate_capl_sync(argparse.Namespace())),
                ("gate multibus-dbc", lambda: cmd_gate_multibus_dbc(argparse.Namespace())),
                ("gate cli-readiness", lambda: cmd_gate_cli_readiness(argparse.Namespace())),
            ]
            for name, fn in gate_steps:
                if run_step(name, fn) != 0 and args.stop_on_fail:
                    _write_batch_report(
                        run_id=args.run_id,
                        owner=args.owner,
                        run_date=args.run_date,
                        phase=args.phase,
                        steps=steps,
                        report_formats=report_formats,
                        output_json=args.output_json,
                        output_md=args.output_md,
                        output_csv=args.output_csv,
                    )
                    return 2

        pre_steps = [
            ("verify prepare", lambda: cmd_verify_prepare(argparse.Namespace(run_id=args.run_id))),
            ("verify smoke", lambda: cmd_verify_smoke(argparse.Namespace(owner=args.owner, run_date=args.run_date))),
            (
                "verify status",
                lambda: cmd_verify_status(
                    argparse.Namespace(
                        run_id=args.run_id,
                        evidence_root="",
                        output_json="canoe/tmp/reports/verification/run_readiness.json",
                        output_md="canoe/tmp/reports/verification/run_readiness.md",
                    )
                ),
            ),
        ]
        for name, fn in pre_steps:
            if run_step(name, fn) != 0 and args.stop_on_fail:
                _write_batch_report(
                    run_id=args.run_id,
                    owner=args.owner,
                    run_date=args.run_date,
                    phase=args.phase,
                    steps=steps,
                    report_formats=report_formats,
                    output_json=args.output_json,
                    output_md=args.output_md,
                    output_csv=args.output_csv,
                )
                return 2

    if args.phase in {"post", "full"}:
        finalize_ns = argparse.Namespace(
            run_id=args.run_id,
            tiers=["UT", "IT", "ST"],
            owner=args.owner,
            run_date=args.run_date,
            owner_fallback=args.owner,
            date_fallback=args.run_date,
            baseline_run_id="",
            no_strict_metadata=False,
            no_strict_axis=False,
            evidence_root="",
            docs_root="",
            insight_md="canoe/tmp/reports/verification/run_insight_report.md",
            insight_json="canoe/tmp/reports/verification/run_insight_report.json",
            binding_csv="canoe/tmp/reports/verification/doc_binding_bundle.csv",
            binding_json="canoe/tmp/reports/verification/doc_binding_bundle.json",
            binding_md="canoe/tmp/reports/verification/doc_binding_bundle.md",
            fill_csv="canoe/tmp/reports/verification/doc_fill_template.csv",
            fill_md="canoe/tmp/reports/verification/doc_fill_template.md",
        )
        if run_step("verify finalize", lambda: cmd_verify_finalize(finalize_ns)) != 0 and args.stop_on_fail:
            _write_batch_report(
                run_id=args.run_id,
                owner=args.owner,
                run_date=args.run_date,
                phase=args.phase,
                steps=steps,
                report_formats=report_formats,
                output_json=args.output_json,
                output_md=args.output_md,
                output_csv=args.output_csv,
            )
            return 2
        run_step(
            "verify status",
            lambda: cmd_verify_status(
                argparse.Namespace(
                    run_id=args.run_id,
                    evidence_root="",
                    output_json="canoe/tmp/reports/verification/run_readiness.json",
                    output_md="canoe/tmp/reports/verification/run_readiness.md",
                )
            ),
        )

    _write_batch_report(
        run_id=args.run_id,
        owner=args.owner,
        run_date=args.run_date,
        phase=args.phase,
        steps=steps,
        report_formats=report_formats,
        output_json=args.output_json,
        output_md=args.output_md,
        output_csv=args.output_csv,
    )
    failed = sum(1 for s in steps if s["rc"] != 0)
    return 0 if failed == 0 else 2


def cmd_scenario_run(args: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("scenario run")
    if platform_rc != 0:
        return platform_rc
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


def _prompt_with_default(label: str, default: str) -> str:
    if questionary is not None and sys.stdin.isatty() and sys.stdout.isatty():
        answer = questionary.text(f"{label}", default=default).ask()
        if answer is None:
            return default
        answer = answer.strip()
        return answer or default

    raw = input(f"{label} [{default}]: ").strip()
    return raw or default


def _is_interactive_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _ui_info(msg: str) -> None:
    if _RICH_CONSOLE is not None and _is_interactive_tty():
        _RICH_CONSOLE.print(msg)
    else:
        print(msg)


def _ui_welcome_banner() -> None:
    title = "SDV CLI"
    body = (
        "CANoe Verification Operator Console\n"
        "Menu-driven UX | Scenario trigger | Evidence status | Measurement control"
    )
    if _RICH_CONSOLE is not None and Panel is not None and _is_interactive_tty():
        _RICH_CONSOLE.print(Panel(body, title=title, border_style="cyan"))
    else:
        print("=" * 56)
        print(f"{title} - CANoe Verification Operator Console")
        print("=" * 56)


def _run_with_loading(label: str, func) -> int:
    if _RICH_CONSOLE is not None and _is_interactive_tty():
        with _RICH_CONSOLE.status(f"[bold cyan]{label}[/]"):
            return func()
    _ui_info(f"[GUIDED] running: {label}")
    return func()


def _prompt_menu_choice(default: int = 1, minimum: int = 1, maximum: int = 11) -> int:
    if questionary is not None and _is_interactive_tty():
        choices = [
            questionary.Choice("1) doctor (CANoe COM + measurement + sysvar check)", value=1),
            questionary.Choice("2) precheck (gates+prepare+smoke+status)", value=2),
            questionary.Choice("3) trigger scenario (scenarioCommand/testScenario)", value=3),
            questionary.Choice("4) evidence status (readiness report)", value=4),
            questionary.Choice("5) measurement start", value=5),
            questionary.Choice("6) measurement stop", value=6),
            questionary.Choice("7) measurement status", value=7),
            questionary.Choice("8) open slash shell", value=8),
            questionary.Choice("9) quick flow (doctor -> scenario -> status)", value=9),
            questionary.Choice("10) exit", value=10),
            questionary.Choice("11) silent exit", value=11),
        ]
        answer = questionary.select("Choose action", choices=choices, default=choices[default - 1]).ask()
        if answer is None:
            return 11
        return int(answer)

    while True:
        raw = input(f"select [{minimum}-{maximum}] (default {default}, q=silent-exit): ").strip()

        if raw.lower() in {"q", "quit", "x"}:
            return 11

        if not raw:
            return default

        try:
            value = int(raw)
        except ValueError:
            print("[GUIDED] enter a number.")
            continue

        if value < minimum or value > maximum:
            print(f"[GUIDED] value must be in range {minimum}..{maximum}.")
            continue
        return value


def _prompt_int(label: str, default: int, minimum: int, maximum: int) -> int:
    while True:
        if questionary is not None and sys.stdin.isatty() and sys.stdout.isatty():
            answer = questionary.text(label, default=str(default)).ask()
            raw = "" if answer is None else answer.strip()
        else:
            raw = input(f"{label} [{default}]: ").strip()

        if not raw:
            return default
        try:
            value = int(raw)
        except ValueError:
            print("[WIZARD] enter a valid integer.")
            continue
        if value < minimum or value > maximum:
            print(f"[WIZARD] value must be in range {minimum}..{maximum}.")
            continue
        return value


def _default_run_id() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M")


def _suggest_choice(value: str, choices: list[str]) -> str | None:
    matches = difflib.get_close_matches(value, choices, n=1, cutoff=0.5)
    return matches[0] if matches else None


def _run_gate_all() -> int:
    gates = [
        ("doc-sync", cmd_gate_doc_sync),
        ("cfg-hygiene", cmd_gate_cfg_hygiene),
        ("capl-sync", cmd_gate_capl_sync),
        ("multibus-dbc", cmd_gate_multibus_dbc),
        ("cli-readiness", cmd_gate_cli_readiness),
    ]
    failed = 0
    for gate_name, gate_fn in gates:
        print(f"[WIZARD] gate -> {gate_name}")
        rc = gate_fn(argparse.Namespace())
        if rc != 0:
            failed += 1
    if failed:
        print(f"[WIZARD] gate summary: FAIL ({failed}/{len(gates)} failed)")
        return 2
    print(f"[WIZARD] gate summary: PASS ({len(gates)}/{len(gates)})")
    return 0


def _print_shell_help() -> None:
    print("Slash commands:")
    print("  /help")
    print("  /exit")
    print("  /palette  # command palette (or press Enter on empty line in interactive mode)")
    print("  /history [N]  # recent command history (default 10)")
    print("  /repeat [N]   # repeat Nth latest command (default 1)")
    print("  /scenario [run] <id> [scenarioCommand|testScenario]")
    print("  /start guided|demo [id]|precheck [run_id] [owner]")
    print("  /go  # alias of /start guided")
    print("  /verify prepare [run_id]")
    print("  /verify batch [run_id] [owner] [pre|post|full] [json,md|json,md,csv|...]")
    print("  /verify smoke [owner] [run_date]")
    print("  /verify status [run_id]")
    print("  /verify finalize [run_id] [owner] [run_date]")
    print("  /verify quick [run_id] [owner]  # prepare + smoke + status")
    print("  /gate all|doc-sync|cfg-hygiene|capl-sync|multibus-dbc|cli-readiness")
    print("  /package portable [onefolder|onefile]")
    print("  /package exe [onefolder|onefile]")
    print("  /doctor [ensure-running]")
    print("  /capl get <Namespace> <Variable>")
    print("  /capl set <Namespace> <Variable> <Value>")
    print("  /canoe measure <status|start|stop|reset>")
    print("  /canoe capl-call <FunctionName> [arg1 arg2 ...] [--int|--float|--bool]")
    print("  /skill list")
    print("  /skill run quickstart|verify-pack|portable-release")
    print("  /contract")


def _append_shell_history(command: str, rc: int, duration_ms: int) -> None:
    try:
        SHELL_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "ts": dt.datetime.now().isoformat(timespec="seconds"),
            "command": command,
            "rc": rc,
            "duration_ms": duration_ms,
        }
        with SHELL_HISTORY_FILE.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        # History logging must never break command execution.
        pass


def _print_shell_history(session_commands: list[str], limit: int = 10) -> None:
    if limit < 1:
        limit = 1
    recent = session_commands[-limit:]
    if not recent:
        print("[SHELL] history is empty")
        return
    print("[SHELL] recent commands")
    start_idx = len(session_commands) - len(recent) + 1
    for i, item in enumerate(recent, start=start_idx):
        print(f"  {i}) {item}")


def _prompt_shell_palette_command() -> str | None:
    group_names = list(SHELL_PALETTE_GROUPS.keys())
    if questionary is not None and _is_interactive_tty():
        group_choice = questionary.select("Command group", choices=group_names).ask()
        if group_choice is None:
            return None

        items = SHELL_PALETTE_GROUPS[group_choice]
        catalog = [f"{cmd}  |  {desc}" for cmd, desc in items]
        answer = questionary.autocomplete(
            f"{group_choice} command",
            choices=catalog,
            ignore_case=True,
            match_middle=True,
        ).ask()
        if answer is None:
            return None
        answer = answer.strip()
        if not answer:
            return None
        for cmd, desc in items:
            if answer == f"{cmd}  |  {desc}":
                return cmd
        return answer

    print("[SHELL] palette")
    for idx, group_name in enumerate(group_names, start=1):
        print(f"  {idx}) {group_name}")

    while True:
        raw_group = input("group number (Enter=cancel): ").strip()
        if not raw_group:
            return None
        try:
            group_value = int(raw_group)
        except ValueError:
            print("[SHELL] enter a valid number.")
            continue
        if group_value < 1 or group_value > len(group_names):
            print(f"[SHELL] number must be 1..{len(group_names)}.")
            continue
        break

    selected_group = group_names[group_value - 1]
    items = SHELL_PALETTE_GROUPS[selected_group]
    print(f"[SHELL] {selected_group}")
    for idx, (cmd, desc) in enumerate(items, start=1):
        print(f"  {idx}) {cmd:<34} - {desc}")

    while True:
        raw = input("command number (Enter=cancel): ").strip()
        if not raw:
            return None
        try:
            value = int(raw)
        except ValueError:
            print("[SHELL] enter a valid number.")
            continue
        if value < 1 or value > len(items):
            print(f"[SHELL] number must be 1..{len(items)}.")
            continue
        return items[value - 1][0]


def _run_named_gate(gate_name: str) -> int:
    mapping = {
        "doc-sync": cmd_gate_doc_sync,
        "cfg-hygiene": cmd_gate_cfg_hygiene,
        "capl-sync": cmd_gate_capl_sync,
        "multibus-dbc": cmd_gate_multibus_dbc,
        "cli-readiness": cmd_gate_cli_readiness,
    }
    fn = mapping.get(gate_name)
    if fn is None:
        print(f"[SHELL] unknown gate: {gate_name}")
        return 2
    return fn(argparse.Namespace())


def _run_skill(skill_name: str) -> int:
    if skill_name == "quickstart":
        run_id = _prompt_with_default("Run ID", _default_run_id())
        owner = _prompt_with_default("Owner", "TBD")
        steps = [
            ("scenario run 4", lambda: cmd_scenario_run(argparse.Namespace(
                id=4,
                namespace="Test",
                var="scenarioCommand",
                ack_var="scenarioCommandAck",
                wait_ack_ms=1200,
                poll_ms=20,
                no_ensure_running=False,
            ))),
            (f"verify prepare {run_id}", lambda: cmd_verify_prepare(argparse.Namespace(run_id=run_id))),
            (f"verify smoke {owner}", lambda: cmd_verify_smoke(argparse.Namespace(owner=owner, run_date=dt.date.today().isoformat()))),
            (f"verify status {run_id}", lambda: cmd_verify_status(argparse.Namespace(
                run_id=run_id,
                evidence_root="",
                output_json="canoe/tmp/reports/verification/run_readiness.json",
                output_md="canoe/tmp/reports/verification/run_readiness.md",
            ))),
        ]
    elif skill_name == "verify-pack":
        run_id = _prompt_with_default("Run ID", _default_run_id())
        owner = _prompt_with_default("Owner", "TBD")
        run_date = _prompt_with_default("Run date", dt.date.today().isoformat())
        steps = [
            (f"verify finalize {run_id} {owner}", lambda: cmd_verify_finalize(argparse.Namespace(
                run_id=run_id,
                tiers=["UT", "IT", "ST"],
                owner=owner,
                run_date=run_date,
                owner_fallback=owner,
                date_fallback=run_date,
                baseline_run_id="",
                no_strict_metadata=False,
                no_strict_axis=False,
                evidence_root="",
                docs_root="",
                insight_md="canoe/tmp/reports/verification/run_insight_report.md",
                insight_json="canoe/tmp/reports/verification/run_insight_report.json",
                binding_csv="canoe/tmp/reports/verification/doc_binding_bundle.csv",
                binding_json="canoe/tmp/reports/verification/doc_binding_bundle.json",
                binding_md="canoe/tmp/reports/verification/doc_binding_bundle.md",
                fill_csv="canoe/tmp/reports/verification/doc_fill_template.csv",
                fill_md="canoe/tmp/reports/verification/doc_fill_template.md",
            ))),
        ]
    elif skill_name == "portable-release":
        steps = [
            ("package bundle-portable --mode onefolder --clean --rebuild-exe", lambda: cmd_package_bundle_portable(argparse.Namespace(
                mode="onefolder",
                clean=True,
                rebuild_exe=True,
                output_dir="",
                bundle_name="",
                zip_name="",
            ))),
        ]
    else:
        print(f"[SHELL] unknown skill: {skill_name}")
        return 2

    for step_name, step_fn in steps:
        print(f"[SHELL][SKILL] {step_name}")
        rc = step_fn()
        if rc != 0:
            print(f"[SHELL][SKILL] FAIL at step: {step_name}")
            return rc
    print("[SHELL][SKILL] PASS")
    return 0


def cmd_shell(_: argparse.Namespace) -> int:
    print("SDV Shell (slash mode)")
    print("Type /help, /exit")
    print("Tip: /palette for searchable command palette")
    print("Tip: keep CANoe measurement running before scenario/verify commands")
    print(f"Host: {platform_label()}")
    runtime_cap = canoe_runtime_check()
    if not runtime_cap.available:
        print(f"Note: {runtime_cap.detail}")
    session_commands: list[str] = []
    while True:
        if questionary is not None and _is_interactive_tty():
            answer = questionary.text("sdv").ask()
            if answer is None:
                return 0
            line = answer.strip()
        else:
            line = input("sdv> ").strip()

        if not line:
            if questionary is not None and _is_interactive_tty():
                selected = _prompt_shell_palette_command()
                if not selected:
                    continue
                line = selected
            else:
                continue

        if line.lower() in {"/palette", "palette", "/p", "p", "/"}:
            selected = _prompt_shell_palette_command()
            if not selected:
                continue
            line = selected

        if line.startswith("/"):
            line = line[1:].strip()
        if not line:
            continue
        try:
            tokens = shlex.split(line)
        except ValueError as ex:
            print(f"[SHELL] parse error: {ex}")
            continue
        if not tokens:
            continue
        cmd = tokens[0].lower()
        rc = 0
        started = dt.datetime.now()

        if cmd in {"exit", "quit", "q"}:
            print("[SHELL] bye")
            return 0
        if cmd == "go":
            return cmd_start_guided(argparse.Namespace())
        if cmd == "history":
            limit = 10
            if len(tokens) > 1:
                try:
                    limit = int(tokens[1])
                except ValueError:
                    print("[SHELL] usage: /history [N]")
                    continue
            _print_shell_history(session_commands, limit=limit)
            continue
        if cmd == "repeat":
            nth = 1
            if len(tokens) > 1:
                try:
                    nth = int(tokens[1])
                except ValueError:
                    print("[SHELL] usage: /repeat [N]")
                    continue
            if nth < 1 or nth > len(session_commands):
                print(f"[SHELL] repeat range: 1..{len(session_commands)}")
                continue
            replay = session_commands[-nth]
            print(f"[SHELL] repeat -> {replay}")
            line = replay[1:] if replay.startswith("/") else replay
            try:
                tokens = shlex.split(line)
            except ValueError as ex:
                print(f"[SHELL] parse error: {ex}")
                continue
            if not tokens:
                continue
            cmd = tokens[0].lower()

        if cmd in {"help", "h", "?"}:
            _print_shell_help()
            continue
        if cmd == "scenario":
            args = tokens[1:]
            if args and args[0].lower() == "run":
                args = args[1:]
            scenario_id = int(args[0]) if args else _prompt_int("Scenario ID", default=4, minimum=0, maximum=255)
            var_name = args[1] if len(args) > 1 else "scenarioCommand"
            ns = argparse.Namespace(
                id=scenario_id,
                namespace="Test",
                var=var_name,
                ack_var="scenarioCommandAck",
                wait_ack_ms=1200,
                poll_ms=20,
                no_ensure_running=False,
            )
            rc = cmd_scenario_run(ns)
        elif cmd == "start":
            sub = tokens[1].lower() if len(tokens) > 1 else "guided"
            if sub == "guided":
                return cmd_start_guided(argparse.Namespace())
            if sub == "demo":
                sid = int(tokens[2]) if len(tokens) > 2 else _prompt_int("Scenario ID", default=4, minimum=0, maximum=255)
                rc = cmd_start_demo(
                    argparse.Namespace(
                        id=sid,
                        var="scenarioCommand",
                        wait_ack_ms=1200,
                        poll_ms=20,
                        no_ensure_running=False,
                    )
                )
            elif sub == "precheck":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                owner = tokens[3] if len(tokens) > 3 else _prompt_with_default("Owner", "DEV2")
                rc = cmd_start_precheck(
                    argparse.Namespace(
                        run_id=run_id,
                        owner=owner,
                        run_date=dt.date.today().isoformat(),
                        skip_gates=False,
                        stop_on_fail=False,
                        report_formats="json,md",
                    )
                )
            else:
                suggestion = _suggest_choice(sub, ["guided", "demo", "precheck"])
                if suggestion:
                    print(f"[SHELL] unknown start subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown start subcommand: {sub}")
                continue
        elif cmd == "verify":
            if len(tokens) < 2:
                print("[SHELL] usage: /verify <prepare|batch|smoke|status|finalize|quick> ...")
                continue
            sub = tokens[1].lower()
            if sub == "prepare":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                rc = cmd_verify_prepare(argparse.Namespace(run_id=run_id))
            elif sub == "batch":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                owner = tokens[3] if len(tokens) > 3 else _prompt_with_default("Owner", "TBD")
                phase = tokens[4] if len(tokens) > 4 else "pre"
                report_formats = tokens[5] if len(tokens) > 5 else "json,md"
                if phase not in {"pre", "post", "full"}:
                    print("[SHELL] phase must be pre|post|full")
                    continue
                rc = cmd_verify_batch(
                    argparse.Namespace(
                        run_id=run_id,
                        owner=owner,
                        run_date=dt.date.today().isoformat(),
                        phase=phase,
                        skip_gates=False,
                        stop_on_fail=False,
                        report_formats=report_formats,
                        output_json=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
                        output_md=Path("canoe/tmp/reports/verification/dev2_batch_report.md"),
                        output_csv=Path("canoe/tmp/reports/verification/dev2_batch_report.csv"),
                    )
                )
            elif sub == "smoke":
                owner = tokens[2] if len(tokens) > 2 else _prompt_with_default("Owner", "TBD")
                run_date = tokens[3] if len(tokens) > 3 else _prompt_with_default("Run date", dt.date.today().isoformat())
                rc = cmd_verify_smoke(argparse.Namespace(owner=owner, run_date=run_date))
            elif sub == "status":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                rc = cmd_verify_status(argparse.Namespace(
                    run_id=run_id,
                    evidence_root="",
                    output_json="canoe/tmp/reports/verification/run_readiness.json",
                    output_md="canoe/tmp/reports/verification/run_readiness.md",
                ))
            elif sub in {"finalize", "full"}:
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                owner = tokens[3] if len(tokens) > 3 else _prompt_with_default("Owner", "TBD")
                run_date = tokens[4] if len(tokens) > 4 else _prompt_with_default("Run date", dt.date.today().isoformat())
                rc = cmd_verify_finalize(argparse.Namespace(
                    run_id=run_id,
                    tiers=["UT", "IT", "ST"],
                    owner=owner,
                    run_date=run_date,
                    owner_fallback=owner,
                    date_fallback=run_date,
                    baseline_run_id="",
                    no_strict_metadata=False,
                    no_strict_axis=False,
                    evidence_root="",
                    docs_root="",
                    insight_md="canoe/tmp/reports/verification/run_insight_report.md",
                    insight_json="canoe/tmp/reports/verification/run_insight_report.json",
                    binding_csv="canoe/tmp/reports/verification/doc_binding_bundle.csv",
                    binding_json="canoe/tmp/reports/verification/doc_binding_bundle.json",
                    binding_md="canoe/tmp/reports/verification/doc_binding_bundle.md",
                    fill_csv="canoe/tmp/reports/verification/doc_fill_template.csv",
                    fill_md="canoe/tmp/reports/verification/doc_fill_template.md",
                ))
            elif sub == "quick":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                owner = tokens[3] if len(tokens) > 3 else _prompt_with_default("Owner", "TBD")
                steps = [
                    ("verify prepare", lambda: cmd_verify_prepare(argparse.Namespace(run_id=run_id))),
                    ("verify smoke", lambda: cmd_verify_smoke(argparse.Namespace(owner=owner, run_date=dt.date.today().isoformat()))),
                    ("verify status", lambda: cmd_verify_status(argparse.Namespace(
                        run_id=run_id,
                        evidence_root="",
                        output_json="canoe/tmp/reports/verification/run_readiness.json",
                        output_md="canoe/tmp/reports/verification/run_readiness.md",
                    ))),
                ]
                for step_name, step_fn in steps:
                    print(f"[SHELL] {step_name}")
                    rc = step_fn()
                    if rc != 0:
                        break
            else:
                suggestion = _suggest_choice(sub, ["prepare", "batch", "smoke", "status", "finalize", "quick"])
                if suggestion:
                    print(f"[SHELL] unknown verify subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown verify subcommand: {sub}")
                continue
        elif cmd == "gate":
            if len(tokens) < 2:
                print("[SHELL] usage: /gate all|doc-sync|cfg-hygiene|capl-sync|multibus-dbc|cli-readiness")
                continue
            sub = tokens[1].lower()
            if sub == "all":
                rc = _run_gate_all()
            else:
                rc = _run_named_gate(sub)
        elif cmd == "package":
            if len(tokens) < 2:
                print("[SHELL] usage: /package <portable|exe> [onefolder|onefile]")
                continue
            sub = tokens[1].lower()
            mode = tokens[2].lower() if len(tokens) > 2 else "onefolder"
            if mode not in {"onefolder", "onefile"}:
                print("[SHELL] mode must be onefolder|onefile")
                continue
            if sub == "portable":
                rc = cmd_package_bundle_portable(argparse.Namespace(
                    mode=mode,
                    clean=False,
                    rebuild_exe=False,
                    output_dir="",
                    bundle_name="",
                    zip_name="",
                ))
            elif sub == "exe":
                rc = cmd_package_build_exe(argparse.Namespace(mode=mode, clean=False))
            else:
                suggestion = _suggest_choice(sub, ["portable", "exe"])
                if suggestion:
                    print(f"[SHELL] unknown package subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown package subcommand: {sub}")
                continue
        elif cmd == "doctor":
            ensure_running = len(tokens) > 1 and tokens[1].lower() in {"ensure-running", "--ensure-running"}
            rc = cmd_doctor(
                argparse.Namespace(
                    ensure_running=ensure_running,
                    output_json=Path("canoe/tmp/reports/verification/doctor_report.json"),
                    output_md=Path("canoe/tmp/reports/verification/doctor_report.md"),
                )
            )
        elif cmd == "capl":
            if len(tokens) < 2:
                print("[SHELL] usage: /capl <get|set> ...")
                continue
            sub = tokens[1].lower()
            if sub == "get":
                if len(tokens) < 4:
                    print("[SHELL] usage: /capl get <Namespace> <Variable>")
                    continue
                rc = cmd_capl_sysvar_get(
                    argparse.Namespace(
                        namespace=tokens[2],
                        var=tokens[3],
                    )
                )
            elif sub == "set":
                if len(tokens) < 5:
                    print("[SHELL] usage: /capl set <Namespace> <Variable> <Value> [int|float|bool|string]")
                    continue
                value_type = tokens[5].lower() if len(tokens) > 5 else "int"
                rc = cmd_capl_sysvar_set(
                    argparse.Namespace(
                        namespace=tokens[2],
                        var=tokens[3],
                        value=tokens[4],
                        value_type=value_type,
                    )
                )
            else:
                suggestion = _suggest_choice(sub, ["get", "set"])
                if suggestion:
                    print(f"[SHELL] unknown capl subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown capl subcommand: {sub}")
                continue
        elif cmd == "canoe":
            if len(tokens) < 3:
                print("[SHELL] usage: /canoe measure <status|start|stop|reset> | /canoe capl-call <FunctionName> [args...]")
                continue
            sub = tokens[1].lower()
            if sub == "measure":
                action = tokens[2].lower()
                if action == "status":
                    rc = cmd_canoe_measure_status(argparse.Namespace())
                elif action == "start":
                    rc = cmd_canoe_measure_start(argparse.Namespace())
                elif action == "stop":
                    rc = cmd_canoe_measure_stop(argparse.Namespace())
                elif action == "reset":
                    rc = cmd_canoe_measure_reset(argparse.Namespace())
                else:
                    print("[SHELL] measure action must be status|start|stop|reset")
                    continue
            elif sub in {"capl-call", "caplcall"}:
                function_name = tokens[2]
                arg_type = "string"
                call_args: list[str] = []
                for item in tokens[3:]:
                    if item == "--int":
                        arg_type = "int"
                    elif item == "--float":
                        arg_type = "float"
                    elif item == "--bool":
                        arg_type = "bool"
                    else:
                        call_args.append(item)
                rc = cmd_canoe_capl_call(
                    argparse.Namespace(
                        function_name=function_name,
                        args=call_args,
                        arg_type=arg_type,
                    )
                )
            else:
                suggestion = _suggest_choice(sub, ["measure", "capl-call"])
                if suggestion:
                    print(f"[SHELL] unknown canoe subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown canoe subcommand: {sub}")
                continue
        elif cmd == "skill":
            if len(tokens) < 2:
                print("[SHELL] usage: /skill list | /skill run <name>")
                continue
            sub = tokens[1].lower()
            if sub == "list":
                print("Skills:")
                print("  - quickstart")
                print("  - verify-pack")
                print("  - portable-release")
            elif sub == "run":
                if len(tokens) < 3:
                    print("[SHELL] usage: /skill run <quickstart|verify-pack|portable-release>")
                    continue
                rc = _run_skill(tokens[2].lower())
            else:
                suggestion = _suggest_choice(sub, ["list", "run"])
                if suggestion:
                    print(f"[SHELL] unknown skill subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown skill subcommand: {sub}")
                continue
        elif cmd == "contract":
            rc = cmd_contract(argparse.Namespace(json=False))
        else:
            suggestion = _suggest_choice(
                cmd,
                ["palette", "scenario", "verify", "gate", "package", "doctor", "capl", "canoe", "skill", "contract", "help", "exit"],
            )
            if suggestion:
                print(f"[SHELL] unknown command: {cmd} (did you mean '{suggestion}'?)")
            else:
                print(f"[SHELL] unknown command: {cmd}")
            print("[SHELL] type /help")
            continue

        command_for_history = f"/{line}"
        if cmd not in {"history", "repeat"}:
            session_commands.append(command_for_history)
            duration_ms = int((dt.datetime.now() - started).total_seconds() * 1000)
            _append_shell_history(command_for_history, rc, duration_ms)

        if rc == 0:
            print("[SHELL] PASS")
        else:
            print(f"[SHELL] FAIL (rc={rc})")


def cmd_wizard(args: argparse.Namespace) -> int:
    # Legacy alias: keep old entrypoint name but use shell behavior.
    return cmd_shell(args)


def _get_canoe_bridge() -> CanoeComBridge:
    return CanoeComBridge.connect()


def _coerce_cli_value(raw_value: str, value_type: str) -> object:
    if value_type == "int":
        return int(raw_value)
    if value_type == "float":
        return float(raw_value)
    if value_type == "bool":
        return 1 if raw_value.lower() in {"1", "true", "yes", "on"} else 0
    return raw_value


def _write_doctor_reports(
    checks: list[tuple[str, bool, str]],
    *,
    output_json: Path | None,
    output_md: Path | None,
) -> None:
    payload = {
        "status": "PASS" if all(ok for _, ok, _ in checks) else "FAIL",
        "generated_at": dt.datetime.now().isoformat(),
        "checks": [
            {"name": name, "status": "PASS" if ok else "FAIL", "detail": detail}
            for name, ok, detail in checks
        ],
    }
    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if output_md:
        output_md.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# SDV Doctor Report",
            "",
            f"- status: `{payload['status']}`",
            f"- generated_at: `{payload['generated_at']}`",
            "",
            "| check | status | detail |",
            "|---|---|---|",
        ]
        for row in payload["checks"]:
            lines.append(f"| `{row['name']}` | `{row['status']}` | `{row['detail']}` |")
        output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_doctor(args: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("doctor")
    if platform_rc != 0:
        return platform_rc
    checks: list[tuple[str, bool, str]] = []
    ensure_running = bool(getattr(args, "ensure_running", False))
    output_json = getattr(args, "output_json", None)
    output_md = getattr(args, "output_md", None)

    required_vars = [
        ("Test", "scenarioCommand"),
        ("Test", "scenarioCommandAck"),
        ("Test", "testScenario"),
        ("Core", "decelAssistReq"),
        ("Core", "proximityRiskLevel"),
        ("Core", "failSafeMode"),
    ]
    try:
        bridge = _get_canoe_bridge()
        checks.append(("pywin32 import", True, "ok"))
        checks.extend([(row.name, row.ok, row.detail) for row in bridge.run_doctor(required_vars, ensure_running=ensure_running)])
    except CanoeComError as ex:
        err = str(ex)
        checks.append(("CANoe COM attach" if "attach failed" in err else "pywin32 import", False, err))

    failed = [row for row in checks if not row[1]]
    print("[DOCTOR] SDV CLI environment checks")
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"- {status:4} | {name} | {detail}")

    _write_doctor_reports(
        checks,
        output_json=output_json,
        output_md=output_md,
    )

    if failed:
        print(f"[DOCTOR] FAIL ({len(failed)}/{len(checks)} failed)")
        return 2
    print(f"[DOCTOR] PASS ({len(checks)}/{len(checks)})")
    return 0


def cmd_capl_sysvar_get(args: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("capl sysvar-get")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        value = bridge.get_sysvar(args.namespace, args.var)
    except Exception as ex:
        print(f"[CAPL] FAIL: {ex}")
        return 2
    print(f"[CAPL] {args.namespace}::{args.var}={value}")
    return 0


def cmd_capl_sysvar_set(args: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("capl sysvar-set")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        readback = bridge.set_sysvar(args.namespace, args.var, _coerce_cli_value(args.value, args.value_type))
    except Exception as ex:
        print(f"[CAPL] FAIL: {ex}")
        return 2
    print(f"[CAPL] set {args.namespace}::{args.var}={readback} (ok)")
    return 0


def cmd_canoe_measure_status(_: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("canoe measure-status")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        running = bridge.measurement_running()
    except Exception as ex:
        print(f"[CANOE] FAIL: {ex}")
        return 2
    print(f"[CANOE] measurement={'running' if running else 'stopped'}")
    return 0


def cmd_canoe_measure_start(_: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("canoe measure-start")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        bridge.measurement_start()
    except Exception as ex:
        print(f"[CANOE] FAIL: {ex}")
        return 2
    print("[CANOE] measurement started")
    return 0


def cmd_canoe_measure_stop(_: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("canoe measure-stop")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        bridge.measurement_stop()
    except Exception as ex:
        print(f"[CANOE] FAIL: {ex}")
        return 2
    print("[CANOE] measurement stopped")
    return 0


def cmd_canoe_measure_reset(_: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("canoe measure-reset")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        bridge.measurement_reset()
    except Exception as ex:
        print(f"[CANOE] FAIL: {ex}")
        return 2
    print("[CANOE] measurement reset")
    return 0


def cmd_canoe_capl_call(args: argparse.Namespace) -> int:
    platform_rc = _fail_unavailable("canoe capl-call")
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = _get_canoe_bridge()
        call_args = [_coerce_cli_value(item, args.arg_type) for item in args.args]
        result = bridge.call_capl_function(args.function_name, call_args)
    except Exception as ex:
        print(f"[CANOE] FAIL: {ex}")
        return 2
    print(f"[CANOE] capl-call {args.function_name} result={result}")
    return 0


def cmd_start_demo(args: argparse.Namespace) -> int:
    return cmd_scenario_run(
        argparse.Namespace(
            id=args.id,
            namespace="Test",
            var=args.var,
            ack_var="scenarioCommandAck",
            wait_ack_ms=args.wait_ack_ms,
            poll_ms=args.poll_ms,
            no_ensure_running=args.no_ensure_running,
        )
    )


def cmd_start_precheck(args: argparse.Namespace) -> int:
    return cmd_verify_batch(
        argparse.Namespace(
            run_id=args.run_id,
            owner=args.owner,
            run_date=args.run_date,
            phase="pre",
            skip_gates=args.skip_gates,
            stop_on_fail=args.stop_on_fail,
            report_formats=args.report_formats,
            output_json=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
            output_md=Path("canoe/tmp/reports/verification/dev2_batch_report.md"),
            output_csv=Path("canoe/tmp/reports/verification/dev2_batch_report.csv"),
        )
    )


def cmd_start_preset(args: argparse.Namespace) -> int:
    return _run_skill(args.name)


def cmd_start_shell(args: argparse.Namespace) -> int:
    return cmd_shell(args)


def cmd_start_guided(_: argparse.Namespace) -> int:
    _ui_welcome_banner()
    _ui_info("SDV Guided Menu")
    _ui_info("Focus: operator workflow (number select + input prompts)")
    _ui_info(f"[GUIDED] host={platform_label()}")
    runtime_cap = canoe_runtime_check()
    if not runtime_cap.available:
        _ui_info(f"[GUIDED] note: {runtime_cap.detail}")
    if questionary is None:
        _ui_info("[GUIDED] tip: install questionary for richer prompts -> python -m pip install questionary>=2.1.1")
    if _RICH_CONSOLE is None:
        _ui_info("[GUIDED] tip: install rich for spinner/banner UX -> python -m pip install rich>=13.7.1")

    while True:
        if not (questionary is not None and _is_interactive_tty()):
            print("")
            print("1) doctor (CANoe COM + measurement + sysvar check)")
            print("2) precheck (gates+prepare+smoke+status)")
            print("3) trigger scenario (scenarioCommand/testScenario)")
            print("4) evidence status (readiness report)")
            print("5) measurement start")
            print("6) measurement stop")
            print("7) measurement status")
            print("8) open slash shell")
            print("9) quick flow (doctor -> scenario -> status)")
            print("10) exit")
            print("11) silent exit")

        choice = _prompt_menu_choice(default=1, minimum=1, maximum=11)

        if choice == 1:
            rc = _run_with_loading(
                "doctor check",
                lambda: cmd_doctor(
                    argparse.Namespace(
                        ensure_running=False,
                        output_json=Path("canoe/tmp/reports/verification/doctor_report.json"),
                        output_md=Path("canoe/tmp/reports/verification/doctor_report.md"),
                    )
                )
            )
        elif choice == 2:
            run_id = _prompt_with_default("Run ID", _default_run_id())
            owner = _prompt_with_default("Owner", "DEV2")
            rc = _run_with_loading(
                "precheck batch",
                lambda: cmd_start_precheck(
                    argparse.Namespace(
                        run_id=run_id,
                        owner=owner,
                        run_date=dt.date.today().isoformat(),
                        skip_gates=False,
                        stop_on_fail=False,
                        report_formats="json,md",
                    )
                )
            )
        elif choice == 3:
            sid = _prompt_int("Scenario ID", default=4, minimum=0, maximum=255)
            var = _prompt_with_default("Scenario variable", "scenarioCommand")
            rc = _run_with_loading(
                f"trigger scenario {sid}",
                lambda: cmd_start_demo(
                    argparse.Namespace(
                        id=sid,
                        var=var,
                        wait_ack_ms=1200,
                        poll_ms=20,
                        no_ensure_running=False,
                    )
                )
            )
        elif choice == 4:
            run_id = _prompt_with_default("Run ID", _default_run_id())
            rc = _run_with_loading(
                f"evidence status {run_id}",
                lambda: cmd_evidence_status(
                    argparse.Namespace(
                        run_id=run_id,
                        evidence_root="",
                        output_json="canoe/tmp/reports/verification/run_readiness.json",
                        output_md="canoe/tmp/reports/verification/run_readiness.md",
                    )
                )
            )
        elif choice == 5:
            rc = _run_with_loading("measurement start", lambda: cmd_canoe_measure_start(argparse.Namespace()))
        elif choice == 6:
            rc = _run_with_loading("measurement stop", lambda: cmd_canoe_measure_stop(argparse.Namespace()))
        elif choice == 7:
            rc = _run_with_loading("measurement status", lambda: cmd_canoe_measure_status(argparse.Namespace()))
        elif choice == 8:
            return cmd_shell(argparse.Namespace())
        elif choice == 9:
            sid = _prompt_int("Scenario ID", default=4, minimum=0, maximum=255)
            owner = _prompt_with_default("Owner", "DEV2")
            run_id = _prompt_with_default("Run ID", _default_run_id())
            rc1 = _run_with_loading(
                "quick-flow: doctor",
                lambda: cmd_doctor(
                    argparse.Namespace(
                        ensure_running=False,
                        output_json=Path("canoe/tmp/reports/verification/doctor_report.json"),
                        output_md=Path("canoe/tmp/reports/verification/doctor_report.md"),
                    )
                )
            )
            rc2 = _run_with_loading(
                f"quick-flow: scenario {sid}",
                lambda: cmd_start_demo(
                    argparse.Namespace(
                        id=sid,
                        var="scenarioCommand",
                        wait_ack_ms=1200,
                        poll_ms=20,
                        no_ensure_running=False,
                    )
                )
            )
            rc3 = _run_with_loading(
                f"quick-flow: evidence {run_id}",
                lambda: cmd_evidence_status(
                    argparse.Namespace(
                        run_id=run_id,
                        evidence_root="",
                        output_json="canoe/tmp/reports/verification/run_readiness.json",
                        output_md="canoe/tmp/reports/verification/run_readiness.md",
                    )
                )
            )
            _ = owner  # reserved for future ownership tagging in quick-flow reports
            rc = 0 if rc1 == 0 and rc2 == 0 and rc3 == 0 else 2
        elif choice == 10:
            _ui_info("[GUIDED] bye")
            return 0
        elif choice == 11:
            return 0
        else:
            _ui_info("[GUIDED] invalid selection")
            continue

        if rc == 0:
            _ui_info("[GUIDED] PASS")
        else:
            _ui_info(f"[GUIDED] FAIL (rc={rc})")


def cmd_evidence_status(args: argparse.Namespace) -> int:
    return cmd_verify_status(args)


def cmd_evidence_insight(args: argparse.Namespace) -> int:
    return cmd_verify_insight(args)


def cmd_evidence_finalize(args: argparse.Namespace) -> int:
    return cmd_verify_finalize(args)


def cmd_release_exe(args: argparse.Namespace) -> int:
    return cmd_package_build_exe(args)


def cmd_release_portable(args: argparse.Namespace) -> int:
    return cmd_package_bundle_portable(args)


def add_verify_prepare_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.set_defaults(func=cmd_verify_prepare)


def add_verify_batch_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", required=True, help="Run ID, e.g. 20260306_1930")
    p.add_argument("--owner", default="TBD")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--phase", choices=["pre", "post", "full"], default="pre")
    p.add_argument("--skip-gates", action="store_true", help="Skip all gate steps in pre/full phase")
    p.add_argument("--stop-on-fail", action="store_true", help="Stop immediately at first failed step")
    p.add_argument(
        "--report-formats",
        default="json,md",
        help="Comma-separated report formats: json,md,csv (default: json,md)",
    )
    p.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
        help="Batch summary JSON output path",
    )
    p.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.md"),
        help="Batch summary markdown output path",
    )
    p.add_argument(
        "--output-csv",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.csv"),
        help="Batch summary CSV output path (optional format)",
    )
    p.set_defaults(func=cmd_verify_batch)


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


def add_start_demo_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--id", type=int, default=4, help="Scenario ID (0..255), default=4")
    p.add_argument(
        "--var",
        default="scenarioCommand",
        choices=["scenarioCommand", "testScenario"],
        help="Target sysvar name",
    )
    p.add_argument("--wait-ack-ms", type=int, default=1200, help="Ack wait timeout in ms")
    p.add_argument("--poll-ms", type=int, default=20, help="Ack poll interval in ms")
    p.add_argument("--no-ensure-running", action="store_true", help="Do not auto-start measurement")
    p.set_defaults(func=cmd_start_demo)


def add_start_precheck_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--run-id", default=_default_run_id(), help="Run ID, e.g. 20260308_1900")
    p.add_argument("--owner", default="DEV2")
    p.add_argument("--run-date", default=dt.date.today().isoformat())
    p.add_argument("--skip-gates", action="store_true", help="Skip all gates in precheck")
    p.add_argument("--stop-on-fail", action="store_true", help="Stop at first failed step")
    p.add_argument(
        "--report-formats",
        default="json,md",
        help="Comma-separated formats: json,md,csv (default: json,md)",
    )
    p.set_defaults(func=cmd_start_precheck)


def add_start_preset_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "name",
        choices=["quickstart", "verify-pack", "portable-release"],
        help="Preset workflow name",
    )
    p.set_defaults(func=cmd_start_preset)


def add_doctor_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--ensure-running", action="store_true", help="Auto-start measurement if stopped")
    p.add_argument(
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doctor_report.json"),
        help="Doctor report JSON output path",
    )
    p.add_argument(
        "--output-md",
        type=Path,
        default=Path("canoe/tmp/reports/verification/doctor_report.md"),
        help="Doctor report markdown output path",
    )
    p.set_defaults(func=cmd_doctor)


def add_capl_sysvar_get_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--namespace", required=True, help="System variable namespace")
    p.add_argument("--var", required=True, help="System variable name")
    p.set_defaults(func=cmd_capl_sysvar_get)


def add_capl_sysvar_set_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--namespace", required=True, help="System variable namespace")
    p.add_argument("--var", required=True, help="System variable name")
    p.add_argument("--value", required=True, help="Target value")
    p.add_argument(
        "--value-type",
        default="int",
        choices=["int", "float", "bool", "string"],
        help="Input value type",
    )
    p.set_defaults(func=cmd_capl_sysvar_set)


def add_canoe_capl_call_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--function-name", required=True, help="CAPL function name")
    p.add_argument("--args", nargs="*", default=[], help="CAPL call args")
    p.add_argument(
        "--arg-type",
        default="string",
        choices=["int", "float", "bool", "string"],
        help="Single coercion type for all --args values",
    )
    p.set_defaults(func=cmd_canoe_capl_call)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified script launcher")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Operator-first quick entrypoints")
    start_sub = start.add_subparsers(dest="start_command")
    add_start_demo_args(start_sub.add_parser("demo", help="Trigger default demo scenario (no panel)"))
    add_start_precheck_args(start_sub.add_parser("precheck", help="Run precheck batch (gates+prepare+smoke+status)"))
    add_start_preset_args(start_sub.add_parser("preset", help="Run named preset workflow"))
    start_sub.add_parser("shell", help="Open interactive slash shell").set_defaults(func=cmd_start_shell)
    start_sub.add_parser("guided", help="Open menu-style guided operator flow").set_defaults(func=cmd_start_guided)
    start.set_defaults(func=cmd_start_guided)

    add_doctor_args(sub.add_parser("doctor", help="Check CANoe COM + measurement + required sysvars"))

    capl = sub.add_parser("capl", help="CAPL-linked sysvar access via CANoe COM")
    capl_sub = capl.add_subparsers(dest="capl_command", required=True)
    add_capl_sysvar_get_args(capl_sub.add_parser("sysvar-get", help="Read one system variable value"))
    add_capl_sysvar_set_args(capl_sub.add_parser("sysvar-set", help="Write one system variable value"))

    canoe_cmd = sub.add_parser("canoe", help="CANoe COM control plane")
    canoe_sub = canoe_cmd.add_subparsers(dest="canoe_command", required=True)
    canoe_sub.add_parser("measure-status", help="Read measurement status").set_defaults(func=cmd_canoe_measure_status)
    canoe_sub.add_parser("measure-start", help="Start measurement").set_defaults(func=cmd_canoe_measure_start)
    canoe_sub.add_parser("measure-stop", help="Stop measurement").set_defaults(func=cmd_canoe_measure_stop)
    canoe_sub.add_parser("measure-reset", help="Reset measurement (stop/start)").set_defaults(func=cmd_canoe_measure_reset)
    add_canoe_capl_call_args(canoe_sub.add_parser("capl-call", help="Call CAPL function"))

    sub.add_parser("shell", help="Interactive slash-command shell").set_defaults(func=cmd_shell)
    sub.add_parser("wizard", help="Legacy alias: shell").set_defaults(func=cmd_wizard)

    scenario = sub.add_parser("scenario", help="Manual scenario trigger commands (no panel)")
    scenario_sub = scenario.add_subparsers(dest="scenario_command", required=True)
    add_scenario_run_args(scenario_sub.add_parser("run", help="Send scenario command via CANoe COM"))

    verify = sub.add_parser("verify", help="Verification pipeline commands")
    verify_sub = verify.add_subparsers(dest="verify_command", required=True)
    add_verify_prepare_args(verify_sub.add_parser("prepare", help="Create UT/IT/ST evidence run folders"))
    add_verify_batch_args(verify_sub.add_parser("batch", help="Run Dev2 pre/post/full batch workflow"))
    add_verify_smoke_args(verify_sub.add_parser("smoke", help="Run CANoe COM smoke checks"))
    add_verify_fill_args(verify_sub.add_parser("fill-score", help="Fill and score one tier"))
    add_verify_insight_args(verify_sub.add_parser("insight", help="Build run-level insight report"))
    add_verify_bind_doc_args(verify_sub.add_parser("bind-doc", help="Build 05/06/07 doc binding bundle"))
    add_verify_fill_template_args(verify_sub.add_parser("fill-template", help="Build 05/06/07 doc fill template"))
    add_verify_status_args(verify_sub.add_parser("status", help="Check run readiness before finalize"))
    add_verify_finalize_args(verify_sub.add_parser("finalize", help="Run full post-run verification bundle"))

    evidence = sub.add_parser("evidence", help="Evidence/readout focused commands")
    evidence_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    ev_status = evidence_sub.add_parser("status", help="Alias of verify status")
    add_verify_status_args(ev_status)
    ev_status.set_defaults(func=cmd_evidence_status)
    ev_insight = evidence_sub.add_parser("insight", help="Alias of verify insight")
    add_verify_insight_args(ev_insight)
    ev_insight.set_defaults(func=cmd_evidence_insight)
    ev_finalize = evidence_sub.add_parser("finalize", help="Alias of verify finalize")
    add_verify_finalize_args(ev_finalize)
    ev_finalize.set_defaults(func=cmd_evidence_finalize)

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

    release = sub.add_parser("release", help="Distribution-focused wrappers")
    release_sub = release.add_subparsers(dest="release_command", required=True)
    rel_exe = release_sub.add_parser("exe", help="Alias of package build-exe")
    rel_exe.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    rel_exe.add_argument("--clean", action="store_true")
    rel_exe.set_defaults(func=cmd_release_exe)

    rel_portable = release_sub.add_parser("portable", help="Alias of package bundle-portable")
    rel_portable.add_argument("--mode", default="onefolder", choices=["onefolder", "onefile"])
    rel_portable.add_argument("--clean", action="store_true")
    rel_portable.add_argument("--rebuild-exe", action="store_true")
    rel_portable.add_argument("--output-dir", default="")
    rel_portable.add_argument("--bundle-name", default="")
    rel_portable.add_argument("--zip-name", default="")
    rel_portable.set_defaults(func=cmd_release_portable)

    contract = sub.add_parser("contract", help="Show canonical command contract")
    contract.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    contract.set_defaults(func=cmd_contract)

    add_scenario_run_args(sub.add_parser("scenario-run", help="Legacy alias: scenario run"))
    sub.add_parser("interactive", help="Legacy alias: shell").set_defaults(func=cmd_shell)

    # Legacy aliases (kept for compatibility during migration)
    add_verify_prepare_args(sub.add_parser("verify-prepare", help="Legacy alias: verify prepare"))
    add_verify_batch_args(sub.add_parser("verify-batch", help="Legacy alias: verify batch"))
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

    # User-friendly short aliases
    sub.add_parser("go", help="Short alias: start guided").set_defaults(func=cmd_start_guided)
    add_start_demo_args(sub.add_parser("demo", help="Short alias: start demo"))
    add_start_precheck_args(sub.add_parser("precheck", help="Short alias: start precheck"))
    sub.add_parser("mstart", help="Short alias: canoe measure-start").set_defaults(func=cmd_canoe_measure_start)
    sub.add_parser("mstop", help="Short alias: canoe measure-stop").set_defaults(func=cmd_canoe_measure_stop)
    sub.add_parser("mstatus", help="Short alias: canoe measure-status").set_defaults(func=cmd_canoe_measure_status)

    return parser


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        return cmd_shell(argparse.Namespace())
    if argv and argv[0] not in {"-h", "--help"} and argv[0] not in TOPLEVEL_COMMANDS:
        suggestion = _suggest_choice(argv[0], TOPLEVEL_COMMANDS)
        if suggestion:
            print(f"[CLI] unknown command: {argv[0]} (did you mean '{suggestion}'?)")
        else:
            print(f"[CLI] unknown command: {argv[0]}")
        print("[CLI] tip: run `python scripts/run.py` for shell + palette")
        print("[CLI] tip: run `python scripts/run.py go` for guided mode")
        return 2

    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        # Quiet close on Ctrl+C without stack trace.
        raise SystemExit(130)

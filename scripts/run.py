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
import json
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

CONTRACT_CANONICAL = [
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


def _write_batch_report(
    *,
    run_id: str,
    owner: str,
    run_date: str,
    phase: str,
    steps: list[dict[str, object]],
    output_json: Path,
    output_csv: Path,
) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
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
    output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
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
                        output_json=args.output_json,
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
                    output_json=args.output_json,
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
                output_json=args.output_json,
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
        output_json=args.output_json,
        output_csv=args.output_csv,
    )
    failed = sum(1 for s in steps if s["rc"] != 0)
    return 0 if failed == 0 else 2


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


def _prompt_with_default(label: str, default: str) -> str:
    raw = input(f"{label} [{default}]: ").strip()
    return raw or default


def _prompt_int(label: str, default: int, minimum: int, maximum: int) -> int:
    while True:
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
    print("  /scenario [run] <id> [scenarioCommand|testScenario]")
    print("  /verify prepare [run_id]")
    print("  /verify batch [run_id] [owner] [pre|post|full]")
    print("  /verify smoke [owner] [run_date]")
    print("  /verify status [run_id]")
    print("  /verify finalize [run_id] [owner] [run_date]")
    print("  /verify quick [run_id] [owner]  # prepare + smoke + status")
    print("  /gate all|doc-sync|cfg-hygiene|capl-sync|multibus-dbc|cli-readiness")
    print("  /package portable [onefolder|onefile]")
    print("  /package exe [onefolder|onefile]")
    print("  /skill list")
    print("  /skill run quickstart|verify-pack|portable-release")
    print("  /contract")


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
    print("Tip: keep CANoe measurement running before scenario/verify commands")
    while True:
        line = input("sdv> ").strip()
        if not line:
            continue
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
        if cmd in {"exit", "quit", "q"}:
            print("[SHELL] bye")
            return 0
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
                        output_json=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
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
                print(f"[SHELL] unknown package subcommand: {sub}")
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
                print(f"[SHELL] unknown skill subcommand: {sub}")
                continue
        elif cmd == "contract":
            rc = cmd_contract(argparse.Namespace(json=False))
        else:
            print(f"[SHELL] unknown command: {cmd}")
            print("[SHELL] type /help")
            continue

        if rc == 0:
            print("[SHELL] PASS")
        else:
            print(f"[SHELL] FAIL (rc={rc})")


def cmd_wizard(args: argparse.Namespace) -> int:
    # Legacy alias: keep old entrypoint name but use shell behavior.
    return cmd_shell(args)


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
        "--output-json",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
        help="Batch summary JSON output path",
    )
    p.add_argument(
        "--output-csv",
        type=Path,
        default=Path("canoe/tmp/reports/verification/dev2_batch_report.csv"),
        help="Batch summary CSV output path",
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified script launcher")
    sub = parser.add_subparsers(dest="command", required=True)

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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

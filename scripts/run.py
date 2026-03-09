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
import datetime as dt
import json
import shlex
import sys
from pathlib import Path

from cliops.common import ROOT, SCRIPTS, default_campaign_id as _default_campaign_id, default_run_id as _default_run_id
from cliops.artifact_ops import cmd_artifact_clean, cmd_artifact_list, cmd_artifact_open
from cliops.gate_ops import (
    cmd_gate_all,
    cmd_gate_capl_sync,
    cmd_gate_cfg_hygiene,
    cmd_gate_cli_readiness,
    cmd_gate_doc_sync,
    cmd_gate_multibus_dbc,
    cmd_gate_text_integrity,
    run_gate_all as _run_gate_all,
    run_named_gate as _run_named_gate,
)
from cliops.package_ops import cmd_package_build_exe, cmd_package_bundle_portable, cmd_package_clean, cmd_package_validate_contract
from cliops.operator_result import build_operator_result, clear_last_operator_result, write_last_operator_result
from cliops.parser_factory import TOPLEVEL_COMMANDS, build_parser
from cliops.platform_caps import canoe_runtime_check, platform_label
from cliops.runtime_ops import (
    cmd_canoe_capl_call,
    cmd_canoe_measure_reset,
    cmd_canoe_measure_start,
    cmd_canoe_measure_status,
    cmd_canoe_measure_stop,
    cmd_capl_sysvar_get,
    cmd_capl_sysvar_set,
    cmd_doctor,
    cmd_scenario_run,
    cmd_start_demo,
    cmd_start_precheck,
)
from cliops.shell_ui import (
    append_shell_history as _append_shell_history,
    can_launch_tui as _can_launch_tui,
    has_questionary_support as _has_questionary_support,
    has_rich_support as _has_rich_support,
    print_shell_help as _print_shell_help,
    print_shell_history as _print_shell_history,
    prompt_int as _prompt_int,
    prompt_menu_choice as _prompt_menu_choice,
    prompt_shell_palette_command as _prompt_shell_palette_command,
    prompt_with_default as _prompt_with_default,
    run_with_loading as _run_with_loading,
    suggest_choice as _suggest_choice,
    ui_info as _ui_info,
    ui_welcome_banner as _ui_welcome_banner,
)
from cliops.verify_ops import (
    cmd_verify_batch,
    cmd_verify_bind_doc,
    cmd_verify_fill_score,
    cmd_verify_fill_template,
    cmd_verify_finalize,
    cmd_verify_insight,
    cmd_verify_prepare,
    cmd_verify_quick,
    cmd_verify_smoke,
    cmd_verify_surface_bundle,
    cmd_verify_status,
)

CONTRACT_CANONICAL = [
    "python scripts/run.py",
    "python scripts/run.py gate all",
    "python scripts/run.py scenario run --id <0..255>",
    "python scripts/run.py verify quick --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py artifact list --scope staging",
    "python scripts/run.py artifact open --target batch-report",
    "python scripts/run.py artifact open --target surface-inventory",
    "python scripts/run.py artifact list --scope source",
    "python scripts/run.py artifact clean --scope staging --yes",
    "python scripts/run.py tui",
    "python scripts/run.py shell",
    "python scripts/run.py start demo --id <0..255>",
    "python scripts/run.py start precheck --run-id <YYYYMMDD_HHMM> --campaign-id <CMP_YYYYMMDD> --owner <OWNER>",
    "python scripts/run.py doctor",
    "python scripts/run.py capl sysvar-get --namespace <NS> --var <NAME>",
    "python scripts/run.py capl sysvar-set --namespace <NS> --var <NAME> --value <V> --value-type int",
    "python scripts/run.py canoe measure-status",
    "python scripts/run.py canoe capl-call --function-name <CAPL_FN> --args <A1> <A2>",
    "python scripts/run.py evidence status --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py release portable",
    "python scripts/run.py verify prepare --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify batch --run-id <YYYYMMDD_HHMM> --owner <OWNER> --phase <pre|post|full> --report-formats json,md,junit",
    "python scripts/run.py verify smoke --owner <OWNER>",
    "python scripts/run.py verify fill-score --tier <UT|IT|ST> --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py verify insight --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify bind-doc --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify fill-template --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify status --run-id <YYYYMMDD_HHMM>",
    "python scripts/run.py verify surface-bundle",
    "python scripts/run.py verify finalize --run-id <YYYYMMDD_HHMM> --owner <OWNER>",
    "python scripts/run.py gate doc-sync",
    "python scripts/run.py gate cfg-hygiene",
    "python scripts/run.py gate capl-sync",
    "python scripts/run.py gate multibus-dbc",
    "python scripts/run.py gate cli-readiness",
    "python scripts/run.py package build-exe --mode onefolder",
    "python scripts/run.py package bundle-portable",
    "python scripts/run.py package validate-contract",
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
    "verify-surface-bundle",
    "verify-finalize",
    "gate-doc-sync",
    "gate-cfg-hygiene",
    "gate-capl-sync",
    "gate-multibus-dbc",
    "gate-cli-readiness",
    "package-build-exe",
    "package-bundle-portable",
    "package-validate-contract",
    "package-clean",
]



def cmd_contract(args: argparse.Namespace) -> int:
    if args.json:
        payload = {"canonical": CONTRACT_CANONICAL, "legacy": CONTRACT_LEGACY}
        print(json.dumps(payload, indent=2))
        return 0

    print("Canonical commands:")
    for item in CONTRACT_CANONICAL:
        print(f"  {item}")
    return 0



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


def cmd_tui(_: argparse.Namespace) -> int:
    ok, reason = _can_launch_tui()
    if not ok:
        print(f"[CONSOLE] unavailable: {reason}")
        print("[CONSOLE] fallback: use `python scripts/run.py shell`")
        return 2
    try:
        from tui_app import launch_tui
    except Exception as ex:
        print(f"[CONSOLE] startup failed: {ex}")
        print("[CONSOLE] fallback: use `python scripts/run.py shell`")
        return 2
    return launch_tui()


def cmd_shell(_: argparse.Namespace) -> int:
    print("CANoe Test Verification Console - Shell fallback")
    print("Type /help, /exit")
    print("Tip: /palette for grouped command palette")
    print("Tip: /tui for the Verification Console screen")
    print("Tip: keep CANoe measurement running before scenario/verify commands")
    print(f"Host: {platform_label()}")
    runtime_cap = canoe_runtime_check()
    if not runtime_cap.available:
        print(f"Note: {runtime_cap.detail}")
    session_commands: list[str] = []
    while True:
        line = input("console> ").strip()
        if not line:
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
        if cmd == "tui":
            return cmd_tui(argparse.Namespace())
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
            scenario_id = 4
            var_name = "scenarioCommand"
            if args:
                if args[0] in {"--id", "-i"} and len(args) > 1:
                    scenario_id = int(args[1])
                    args = args[2:]
                elif not args[0].startswith("-"):
                    scenario_id = int(args[0])
                    args = args[1:]
                else:
                    scenario_id = _prompt_int("Scenario ID", default=4, minimum=0, maximum=255)
                if args:
                    if args[0] == "--var" and len(args) > 1:
                        var_name = args[1]
                    elif not args[0].startswith("-"):
                        var_name = args[0]
            else:
                scenario_id = _prompt_int("Scenario ID", default=4, minimum=0, maximum=255)
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
                campaign_id = tokens[3] if len(tokens) > 3 else _prompt_with_default("Campaign ID", _default_campaign_id())
                owner = tokens[4] if len(tokens) > 4 else _prompt_with_default("Owner", "DEV2")
                surface_scope = tokens[5] if len(tokens) > 5 else _prompt_with_default("Surface Scope", "ALL")
                repeat_count = int(tokens[6]) if len(tokens) > 6 else _prompt_int("Repeat Count", default=1, minimum=1, maximum=9999)
                duration_minutes = int(tokens[7]) if len(tokens) > 7 else _prompt_int("Duration Minutes", default=0, minimum=0, maximum=100000)
                interval_seconds = int(tokens[8]) if len(tokens) > 8 else _prompt_int("Interval Seconds", default=0, minimum=0, maximum=100000)
                rc = cmd_start_precheck(
                    argparse.Namespace(
                        run_id=run_id,
                        campaign_id=campaign_id,
                        owner=owner,
                        run_date=dt.date.today().isoformat(),
                        surface_scope=surface_scope,
                        repeat_count=repeat_count,
                        duration_minutes=duration_minutes,
                        interval_seconds=interval_seconds,
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
                print("[SHELL] usage: /verify <prepare|batch|smoke|status|surface-bundle|finalize|quick> ...")
                continue
            sub = tokens[1].lower()
            if sub == "prepare":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                rc = cmd_verify_prepare(argparse.Namespace(run_id=run_id))
            elif sub == "batch":
                run_id = tokens[2] if len(tokens) > 2 else _prompt_with_default("Run ID", _default_run_id())
                campaign_id = tokens[3] if len(tokens) > 3 else _prompt_with_default("Campaign ID", _default_campaign_id())
                owner = tokens[4] if len(tokens) > 4 else _prompt_with_default("Owner", "TBD")
                phase = tokens[5] if len(tokens) > 5 else _prompt_with_default("Phase", "pre")
                surface_scope = tokens[6] if len(tokens) > 6 else _prompt_with_default("Surface Scope", "ALL")
                repeat_count = int(tokens[7]) if len(tokens) > 7 else _prompt_int("Repeat Count", default=1, minimum=1, maximum=9999)
                duration_minutes = int(tokens[8]) if len(tokens) > 8 else _prompt_int("Duration Minutes", default=0, minimum=0, maximum=100000)
                interval_seconds = int(tokens[9]) if len(tokens) > 9 else _prompt_int("Interval Seconds", default=0, minimum=0, maximum=100000)
                report_formats = tokens[10] if len(tokens) > 10 else _prompt_with_default("Report Formats", "json,md")
                if phase not in {"pre", "post", "full"}:
                    print("[SHELL] phase must be pre|post|full")
                    continue
                rc = cmd_verify_batch(
                    argparse.Namespace(
                        run_id=run_id,
                        campaign_id=campaign_id,
                        owner=owner,
                        run_date=dt.date.today().isoformat(),
                        phase=phase,
                        surface_scope=surface_scope,
                        repeat_count=repeat_count,
                        duration_minutes=duration_minutes,
                        interval_seconds=interval_seconds,
                        skip_gates=False,
                        stop_on_fail=False,
                        report_formats=report_formats,
                        output_json=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
                        output_md=Path("canoe/tmp/reports/verification/dev2_batch_report.md"),
                        output_csv=Path("canoe/tmp/reports/verification/dev2_batch_report.csv"),
                        output_junit=Path("canoe/tmp/reports/verification/dev2_batch_report.junit.xml"),
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
            elif sub in {"surface-bundle", "surface_bundle"}:
                rc = cmd_verify_surface_bundle(argparse.Namespace(
                    inventory_json=Path("product/sdv_operator/config/surface_ecu_inventory.json"),
                    doctor_json=Path("canoe/tmp/reports/verification/doctor_report.json"),
                    readiness_json=Path("canoe/tmp/reports/verification/run_readiness.json"),
                    batch_json=Path("canoe/tmp/reports/verification/dev2_batch_report.json"),
                    output_json=Path("canoe/tmp/reports/verification/surface_evidence_bundle.json"),
                    output_md=Path("canoe/tmp/reports/verification/surface_evidence_bundle.md"),
                    surface_dir=Path("canoe/tmp/reports/verification/surface"),
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
                suggestion = _suggest_choice(sub, ["prepare", "batch", "smoke", "status", "surface-bundle", "finalize", "quick"])
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
                print("[SHELL] usage: /package <portable|exe|validate-contract> [onefolder|onefile]")
                continue
            sub = tokens[1].lower()
            if sub == "validate-contract":
                rc = cmd_package_validate_contract(argparse.Namespace())
                continue
            mode = "onefolder"
            if "--mode" in tokens:
                mode_index = tokens.index("--mode")
                if mode_index + 1 < len(tokens):
                    mode = tokens[mode_index + 1].lower()
            elif len(tokens) > 2:
                mode = tokens[2].lower()
            if mode not in {"onefolder", "onefile"}:
                print("[SHELL] mode must be onefolder|onefile")
                continue
            if sub in {"portable", "bundle-portable"}:
                rc = cmd_package_bundle_portable(argparse.Namespace(
                    mode=mode,
                    clean=False,
                    rebuild_exe=False,
                    output_dir="",
                    bundle_name="",
                    zip_name="",
                ))
            elif sub in {"exe", "build-exe"}:
                rc = cmd_package_build_exe(argparse.Namespace(mode=mode, clean=False))
            else:
                suggestion = _suggest_choice(sub, ["portable", "bundle-portable", "exe", "build-exe", "validate-contract"])
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
                print("[SHELL] usage: /capl <get|set|sysvar-get|sysvar-set> ...")
                continue
            sub = tokens[1].lower()
            if sub in {"get", "sysvar-get"}:
                if "--namespace" in tokens and "--var" in tokens:
                    namespace = tokens[tokens.index("--namespace") + 1]
                    var_name = tokens[tokens.index("--var") + 1]
                elif len(tokens) >= 4:
                    namespace = tokens[2]
                    var_name = tokens[3]
                else:
                    print("[SHELL] usage: /capl get <Namespace> <Variable>")
                    continue
                rc = cmd_capl_sysvar_get(
                    argparse.Namespace(
                        namespace=namespace,
                        var=var_name,
                    )
                )
            elif sub in {"set", "sysvar-set"}:
                if "--namespace" in tokens and "--var" in tokens and "--value" in tokens:
                    namespace = tokens[tokens.index("--namespace") + 1]
                    var_name = tokens[tokens.index("--var") + 1]
                    value = tokens[tokens.index("--value") + 1]
                    value_type = tokens[tokens.index("--value-type") + 1].lower() if "--value-type" in tokens else "int"
                elif len(tokens) >= 5:
                    namespace = tokens[2]
                    var_name = tokens[3]
                    value = tokens[4]
                    value_type = tokens[5].lower() if len(tokens) > 5 else "int"
                else:
                    print("[SHELL] usage: /capl set <Namespace> <Variable> <Value> [int|float|bool|string]")
                    continue
                rc = cmd_capl_sysvar_set(
                    argparse.Namespace(
                        namespace=namespace,
                        var=var_name,
                        value=value,
                        value_type=value_type,
                    )
                )
            else:
                suggestion = _suggest_choice(sub, ["get", "set", "sysvar-get", "sysvar-set"])
                if suggestion:
                    print(f"[SHELL] unknown capl subcommand: {sub} (did you mean '{suggestion}'?)")
                else:
                    print(f"[SHELL] unknown capl subcommand: {sub}")
                continue
        elif cmd == "canoe":
            if len(tokens) < 2:
                print("[SHELL] usage: /canoe measure <status|start|stop|reset> | /canoe capl-call <FunctionName> [args...]")
                continue
            sub = tokens[1].lower()
            if sub in {"measure-status", "measure-start", "measure-stop", "measure-reset"}:
                action = sub.split("-", 1)[1]
                if action == "status":
                    rc = cmd_canoe_measure_status(argparse.Namespace())
                elif action == "start":
                    rc = cmd_canoe_measure_start(argparse.Namespace())
                elif action == "stop":
                    rc = cmd_canoe_measure_stop(argparse.Namespace())
                else:
                    rc = cmd_canoe_measure_reset(argparse.Namespace())
            elif sub == "measure":
                if len(tokens) < 3:
                    print("[SHELL] usage: /canoe measure <status|start|stop|reset>")
                    continue
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
                suggestion = _suggest_choice(sub, ["measure", "measure-status", "measure-start", "measure-stop", "measure-reset", "capl-call"])
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
    if not _has_questionary_support():
        _ui_info("[GUIDED] tip: install questionary for richer prompt UX -> python -m pip install questionary>=2.1.1")
    if not _has_rich_support():
        _ui_info("[GUIDED] tip: install rich for spinner/banner UX -> python -m pip install rich>=14")

    while True:
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
            campaign_id = _prompt_with_default("Campaign ID", _default_campaign_id())
            owner = _prompt_with_default("Owner", "DEV2")
            surface_scope = _prompt_with_default("Surface Scope", "ALL")
            repeat_count = _prompt_int("Repeat Count", default=1, minimum=1, maximum=9999)
            duration_minutes = _prompt_int("Duration Minutes", default=0, minimum=0, maximum=100000)
            interval_seconds = _prompt_int("Interval Seconds", default=0, minimum=0, maximum=100000)
            rc = _run_with_loading(
                "precheck batch",
                lambda: cmd_start_precheck(
                    argparse.Namespace(
                        run_id=run_id,
                        campaign_id=campaign_id,
                        owner=owner,
                        run_date=dt.date.today().isoformat(),
                        surface_scope=surface_scope,
                        repeat_count=repeat_count,
                        duration_minutes=duration_minutes,
                        interval_seconds=interval_seconds,
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


PARSER_HANDLERS = {
    "cmd_start_guided": cmd_start_guided,
    "cmd_start_shell": cmd_start_shell,
    "cmd_start_demo": cmd_start_demo,
    "cmd_start_precheck": cmd_start_precheck,
    "cmd_start_preset": cmd_start_preset,
    "cmd_doctor": cmd_doctor,
    "cmd_capl_sysvar_get": cmd_capl_sysvar_get,
    "cmd_capl_sysvar_set": cmd_capl_sysvar_set,
    "cmd_canoe_measure_status": cmd_canoe_measure_status,
    "cmd_canoe_measure_start": cmd_canoe_measure_start,
    "cmd_canoe_measure_stop": cmd_canoe_measure_stop,
    "cmd_canoe_measure_reset": cmd_canoe_measure_reset,
    "cmd_canoe_capl_call": cmd_canoe_capl_call,
    "cmd_tui": cmd_tui,
    "cmd_shell": cmd_shell,
    "cmd_wizard": cmd_wizard,
    "cmd_scenario_run": cmd_scenario_run,
    "cmd_verify_prepare": cmd_verify_prepare,
    "cmd_verify_batch": cmd_verify_batch,
    "cmd_verify_smoke": cmd_verify_smoke,
    "cmd_verify_quick": cmd_verify_quick,
    "cmd_verify_fill_score": cmd_verify_fill_score,
    "cmd_verify_insight": cmd_verify_insight,
    "cmd_verify_bind_doc": cmd_verify_bind_doc,
    "cmd_verify_fill_template": cmd_verify_fill_template,
    "cmd_verify_status": cmd_verify_status,
    "cmd_verify_surface_bundle": cmd_verify_surface_bundle,
    "cmd_verify_finalize": cmd_verify_finalize,
    "cmd_evidence_status": cmd_evidence_status,
    "cmd_evidence_insight": cmd_evidence_insight,
    "cmd_evidence_finalize": cmd_evidence_finalize,
    "cmd_gate_all": cmd_gate_all,
    "cmd_gate_doc_sync": cmd_gate_doc_sync,
    "cmd_gate_text_integrity": cmd_gate_text_integrity,
    "cmd_gate_cfg_hygiene": cmd_gate_cfg_hygiene,
    "cmd_gate_capl_sync": cmd_gate_capl_sync,
    "cmd_gate_multibus_dbc": cmd_gate_multibus_dbc,
    "cmd_gate_cli_readiness": cmd_gate_cli_readiness,
    "cmd_artifact_list": cmd_artifact_list,
    "cmd_artifact_open": cmd_artifact_open,
    "cmd_artifact_clean": cmd_artifact_clean,
    "cmd_package_build_exe": cmd_package_build_exe,
    "cmd_package_bundle_portable": cmd_package_bundle_portable,
    "cmd_package_clean": cmd_package_clean,
    "cmd_package_validate_contract": cmd_package_validate_contract,
    "cmd_release_exe": cmd_release_exe,
    "cmd_release_portable": cmd_release_portable,
    "cmd_contract": cmd_contract,
}

INTERACTIVE_FUNCS = {
    cmd_tui,
    cmd_shell,
    cmd_wizard,
    cmd_start_shell,
    cmd_start_guided,
}


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        can_tui, _ = _can_launch_tui()
        if can_tui:
            return cmd_tui(argparse.Namespace())
        return cmd_shell(argparse.Namespace())
    if argv and argv[0] not in {"-h", "--help"} and argv[0] not in TOPLEVEL_COMMANDS:
        suggestion = _suggest_choice(argv[0], TOPLEVEL_COMMANDS)
        if suggestion:
            print(f"[SHELL] unknown command: {argv[0]} (did you mean '{suggestion}'?)")
        else:
            print(f"[SHELL] unknown command: {argv[0]}")
        print("[SHELL] tip: run `python scripts/run.py` for the default Verification Console")
        print("[SHELL] tip: run `python scripts/run.py shell` for the plain fallback shell")
        print("[SHELL] tip: run `python scripts/run.py go` for guided mode")
        return 2

    parser = build_parser(PARSER_HANDLERS, _default_run_id)
    args = parser.parse_args()
    if args.func in INTERACTIVE_FUNCS:
        return args.func(args)

    clear_last_operator_result()
    rc = args.func(args)
    try:
        result = build_operator_result(args, rc)
        if result is not None:
            write_last_operator_result(result)
    except Exception as ex:
        print(f"[SHELL] result envelope warning: {ex}")
        return rc


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        # Quiet close on Ctrl+C without stack trace.
        raise SystemExit(130)

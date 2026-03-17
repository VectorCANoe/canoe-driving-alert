from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path

from cliops.canoe_com import CanoeComBridge, CanoeComError
from cliops.common import ROOT, fail_unavailable, iso_today
from cliops.native_contract import NativeContractError, resolve_tier_contract
from cliops.operator_result import SCENARIO_SUMMARY_JSON, SCENARIO_SUMMARY_MD
from cliops.platform_caps import canoe_runtime_check, platform_label
from cliops.verify_ops import cmd_verify_batch


def get_canoe_bridge() -> CanoeComBridge:
    return CanoeComBridge.connect()


def _verdict_label(raw_verdict: int) -> str:
    mapping = {
        0: 'not-available',
        1: 'passed',
        2: 'failed',
        3: 'inconclusive',
        4: 'none',
    }
    return mapping.get(raw_verdict, f'value-{raw_verdict}')


def _resolve_config_name(args: argparse.Namespace) -> tuple[str, str | None]:
    config_name = (getattr(args, 'config_name', '') or '').strip()
    tier = (getattr(args, 'tier', '') or '').strip().upper()
    if config_name and tier:
        return config_name, tier
    if config_name:
        return config_name, None
    if not tier:
        raise CanoeComError('either --config-name or --tier is required')
    try:
        contract = resolve_tier_contract(tier)
    except NativeContractError as ex:
        raise CanoeComError(str(ex)) from ex
    if not contract.execute_supported or not contract.config_name:
        raise CanoeComError(f'native execute is not supported for tier: {tier}')
    return contract.config_name, tier


def _native_summary_payload(summary, *, tier: str | None = None) -> dict[str, object]:
    payload: dict[str, object] = {
        'config_name': summary.name,
        'caption': summary.caption,
        'enabled': summary.enabled,
        'running': summary.running,
        'verdict_raw': summary.verdict,
        'verdict': _verdict_label(summary.verdict),
        'test_unit_count': summary.test_unit_count,
        'type_code': summary.type_code,
    }
    if tier:
        payload['tier'] = tier
        try:
            contract = resolve_tier_contract(tier)
            payload['summary_report'] = str(contract.summary_report_path)
            payload['suite_id'] = contract.suite_id
            payload['assign_folder'] = contract.assign_folder
        except NativeContractError:
            pass
    return payload


def _prepare_native_evidence_drop(tier: str) -> None:
    contract = resolve_tier_contract(tier)
    raw_path = ROOT / contract.incoming_raw
    trace_dir = ROOT / contract.incoming_trace_dir
    logging_dir = ROOT / contract.incoming_logging_dir
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text("", encoding="utf-8")
    trace_dir.mkdir(parents=True, exist_ok=True)
    logging_dir.mkdir(parents=True, exist_ok=True)


def _clear_drop_directory(path: Path) -> None:
    if not path.exists() or not path.is_dir():
        return
    for item in path.iterdir():
        if item.name == ".gitkeep":
            continue
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            try:
                item.unlink()
            except OSError:
                pass


def _native_execute_context_path(tier: str) -> Path:
    return ROOT / "canoe" / "logging" / "evidence" / "incoming" / tier / "native_execute_context.json"


def _write_native_execute_context(tier: str, payload: dict[str, object]) -> None:
    path = _native_execute_context_path(tier)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _seed_native_execution_context(
    bridge: CanoeComBridge,
    tier: str | None,
    *,
    run_id: str | None,
    config_name: str | None,
) -> None:
    if not tier:
        return
    try:
        contract = resolve_tier_contract(tier)
        _prepare_native_evidence_drop(tier)
        trace_dir = ROOT / contract.incoming_trace_dir
        logging_dir = ROOT / contract.incoming_logging_dir
        _clear_drop_directory(trace_dir)
        _clear_drop_directory(logging_dir)
        _write_native_execute_context(
            tier,
            {
                "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
                "started_at": dt.datetime.now().isoformat(timespec="seconds"),
                "state": "prepared",
                "run_id": run_id or "",
                "tier": tier,
                "config_name": config_name or contract.config_name,
                "summary_report": str(contract.summary_report_path),
                "incoming_raw": contract.incoming_raw,
                "incoming_trace_dir": contract.incoming_trace_dir,
                "incoming_logging_dir": contract.incoming_logging_dir,
            },
        )
        bridge.set_sysvar('Test', 'nativeExecTierCode', contract.tier_code)
        bridge.set_sysvar('Test', 'evidenceAutoWrite', 1)
    except NativeContractError as ex:
        raise CanoeComError(str(ex)) from ex
    except Exception as ex:
        raise CanoeComError(
            "Native execution evidence sysvars are unavailable. Reload the CANoe configuration after project.sysvars update."
        ) from ex


def _clear_native_execution_context(bridge: CanoeComBridge) -> None:
    try:
        bridge.set_sysvar('Test', 'evidenceAutoWrite', 0)
        bridge.set_sysvar('Test', 'nativeExecTierCode', 0)
    except Exception:
        pass


def execute_native_test_configuration(
    *,
    tier: str | None,
    config_name: str | None,
    run_id: str | None,
    timeout_seconds: int,
    poll_ms: int,
    ensure_running: bool,
    restart_if_running: bool,
    fail_on_verdict: bool,
) -> tuple[int, dict[str, object]]:
    bridge = get_canoe_bridge()
    resolved_name, resolved_tier = _resolve_config_name(
        argparse.Namespace(config_name=config_name or '', tier=tier or '')
    )
    _seed_native_execution_context(
        bridge,
        resolved_tier,
        run_id=run_id,
        config_name=resolved_name,
    )
    try:
        bridge.start_test_configuration(
            resolved_name,
            ensure_measurement=ensure_running,
            restart_if_running=restart_if_running,
        )
        summary = bridge.wait_test_configuration_complete(
            resolved_name,
            timeout_seconds=timeout_seconds,
            poll_ms=poll_ms,
        )
        if resolved_tier:
            _write_native_execute_context(
                resolved_tier,
                {
                    "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
                    "started_at": load_native_execute_context_started_at(resolved_tier),
                    "completed_at": dt.datetime.now().isoformat(timespec="seconds"),
                    "state": "completed",
                    "run_id": run_id or "",
                    "tier": resolved_tier,
                    "config_name": resolved_name,
                    "summary_report": str(resolve_tier_contract(resolved_tier).summary_report_path),
                    "verdict_raw": summary.verdict,
                    "verdict": _verdict_label(summary.verdict),
                    "test_unit_count": summary.test_unit_count,
                    "incoming_raw": resolve_tier_contract(resolved_tier).incoming_raw,
                    "incoming_trace_dir": resolve_tier_contract(resolved_tier).incoming_trace_dir,
                    "incoming_logging_dir": resolve_tier_contract(resolved_tier).incoming_logging_dir,
                },
            )
    finally:
        _clear_native_execution_context(bridge)
    payload = _native_summary_payload(summary, tier=resolved_tier)
    rc = 0
    if fail_on_verdict and summary.verdict == 2:
        rc = 2
    return rc, payload


def load_native_execute_context_started_at(tier: str) -> str:
    path = _native_execute_context_path(tier)
    if not path.exists() or not path.is_file():
        return ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(payload.get("started_at", ""))


def coerce_cli_value(raw_value: str, value_type: str) -> object:
    if value_type == 'int':
        return int(raw_value)
    if value_type == 'float':
        return float(raw_value)
    if value_type == 'bool':
        return 1 if raw_value.lower() in {'1', 'true', 'yes', 'on'} else 0
    return raw_value


def write_doctor_reports(checks: list[tuple[str, bool, str]], *, output_json: Path | None, output_md: Path | None) -> None:
    payload = {
        'status': 'PASS' if all(ok for _, ok, _ in checks) else 'FAIL',
        'generated_at': dt.datetime.now().isoformat(),
        'checks': [{'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail} for name, ok, detail in checks],
    }
    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    if output_md:
        output_md.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            '# SDV Doctor Report',
            '',
            f"- status: `{payload['status']}`",
            f"- generated_at: `{payload['generated_at']}`",
            '',
            '| check | status | detail |',
            '|---|---|---|',
        ]
        for row in payload['checks']:
            lines.append(f"| `{row['name']}` | `{row['status']}` | `{row['detail']}` |")
        output_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def cmd_scenario_run(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('scenario run')
    if platform_rc != 0:
        return platform_rc
    from cliops.common import SCRIPTS, run_cmd
    import sys

    cmd = [
        sys.executable,
        str(SCRIPTS / 'canoe' / 'send_scenario_command.py'),
        '--id', str(args.id),
        '--namespace', args.namespace,
        '--var', args.var,
        '--ack-var', args.ack_var,
        '--wait-ack-ms', str(args.wait_ack_ms),
        '--poll-ms', str(args.poll_ms),
    ]
    if args.no_ensure_running:
        cmd.append('--no-ensure-running')
    rc = run_cmd(cmd)
    write_scenario_summary(args, rc)
    return rc


def cmd_doctor(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('doctor')
    if platform_rc != 0:
        return platform_rc
    checks: list[tuple[str, bool, str]] = []
    ensure_running = bool(getattr(args, 'ensure_running', False))
    output_json = getattr(args, 'output_json', None)
    output_md = getattr(args, 'output_md', None)

    required_vars = [
        ('Test', 'scenarioCommand'),
        ('Test', 'scenarioCommandAck'),
        ('Test', 'testScenario'),
        ('Core', 'decelAssistReq'),
        ('Core', 'proximityRiskLevel'),
        ('Core', 'failSafeMode'),
    ]
    try:
        bridge = get_canoe_bridge()
        checks.append(('pywin32 import', True, 'ok'))
        checks.extend([(row.name, row.ok, row.detail) for row in bridge.run_doctor(required_vars, ensure_running=ensure_running)])
    except CanoeComError as ex:
        err = str(ex)
        checks.append(('CANoe COM attach' if 'attach failed' in err else 'pywin32 import', False, err))

    failed = [row for row in checks if not row[1]]
    print('[DOCTOR] SDV CLI environment checks')
    for name, ok, detail in checks:
        status = 'PASS' if ok else 'FAIL'
        print(f'- {status:4} | {name} | {detail}')

    write_doctor_reports(checks, output_json=output_json, output_md=output_md)

    if failed:
        print(f'[DOCTOR] FAIL ({len(failed)}/{len(checks)} failed)')
        return 2
    print(f'[DOCTOR] PASS ({len(checks)}/{len(checks)})')
    return 0


def cmd_capl_sysvar_get(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('capl sysvar-get')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        value = bridge.get_sysvar(args.namespace, args.var)
    except Exception as ex:
        print(f'[CAPL] FAIL: {ex}')
        return 2
    print(f'[CAPL] {args.namespace}::{args.var}={value}')
    return 0


def cmd_capl_sysvar_set(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('capl sysvar-set')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        readback = bridge.set_sysvar(args.namespace, args.var, coerce_cli_value(args.value, args.value_type))
    except Exception as ex:
        print(f'[CAPL] FAIL: {ex}')
        return 2
    print(f'[CAPL] set {args.namespace}::{args.var}={readback} (ok)')
    return 0


def cmd_canoe_measure_status(_: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe measure-status')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        running = bridge.measurement_running()
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    print(f"[CANOE] measurement={'running' if running else 'stopped'}")
    return 0


def cmd_canoe_measure_start(_: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe measure-start')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        bridge.measurement_start()
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    print('[CANOE] measurement started')
    return 0


def cmd_canoe_measure_stop(_: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe measure-stop')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        bridge.measurement_stop()
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    print('[CANOE] measurement stopped')
    return 0


def cmd_canoe_measure_reset(_: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe measure-reset')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        bridge.measurement_reset()
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    print('[CANOE] measurement reset')
    return 0


def cmd_canoe_capl_call(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe capl-call')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        call_args = [coerce_cli_value(item, args.arg_type) for item in args.args]
        result = bridge.call_capl_function(args.function_name, call_args)
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    print(f'[CANOE] capl-call {args.function_name} result={result}')
    return 0


def cmd_canoe_test_config_list(_: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe test-config-list')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        configs = bridge.list_test_configurations()
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    print('[CANOE] native test configurations')
    for item in configs:
        print(
            f"- name={item.name} enabled={str(item.enabled).lower()} "
            f"running={str(item.running).lower()} verdict={_verdict_label(item.verdict)}({item.verdict}) "
            f"test_units={item.test_unit_count}"
        )
    return 0


def cmd_canoe_test_config_status(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe test-config-status')
    if platform_rc != 0:
        return platform_rc
    try:
        bridge = get_canoe_bridge()
        config_name, tier = _resolve_config_name(args)
        payload = _native_summary_payload(bridge.get_test_configuration_summary(config_name), tier=tier)
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    if getattr(args, 'json', False):
        print(json.dumps(payload, indent=2))
        return 0
    print(f"[CANOE] test-config {payload['config_name']}")
    for key in ['tier', 'suite_id', 'assign_folder', 'summary_report', 'enabled', 'running', 'verdict', 'verdict_raw', 'test_unit_count']:
        if key in payload:
            print(f"- {key}: {payload[key]}")
    return 0


def cmd_canoe_test_config_run(args: argparse.Namespace) -> int:
    platform_rc = fail_unavailable('canoe test-config-run')
    if platform_rc != 0:
        return platform_rc
    try:
        rc, payload = execute_native_test_configuration(
            tier=(getattr(args, 'tier', '') or '').strip().upper() or None,
            config_name=(getattr(args, 'config_name', '') or '').strip() or None,
            run_id=(getattr(args, 'run_id', '') or '').strip() or None,
            timeout_seconds=args.timeout_seconds,
            poll_ms=args.poll_ms,
            ensure_running=not args.no_ensure_running,
            restart_if_running=args.restart_if_running,
            fail_on_verdict=args.fail_on_verdict,
        )
    except Exception as ex:
        print(f'[CANOE] FAIL: {ex}')
        return 2
    if getattr(args, 'json', False):
        print(json.dumps(payload, indent=2))
    else:
        print(f"[CANOE] native execute finished: {payload['config_name']}")
        for key in ['tier', 'suite_id', 'summary_report', 'verdict', 'verdict_raw', 'test_unit_count']:
            if key in payload:
                print(f"- {key}: {payload[key]}")
    return rc


def cmd_start_demo(args: argparse.Namespace) -> int:
    return cmd_scenario_run(argparse.Namespace(id=args.id, namespace='Test', var=args.var, ack_var='scenarioCommandAck', wait_ack_ms=args.wait_ack_ms, poll_ms=args.poll_ms, no_ensure_running=args.no_ensure_running))


def cmd_start_precheck(args: argparse.Namespace) -> int:
    return cmd_verify_batch(argparse.Namespace(
        run_id=args.run_id,
        campaign_id=args.campaign_id,
        profile_id='',
        pack_id='',
        owner=args.owner,
        run_date=args.run_date,
        phase='pre',
        surface_scope=args.surface_scope,
        repeat_count=args.repeat_count,
        duration_minutes=args.duration_minutes,
        interval_seconds=args.interval_seconds,
        skip_gates=args.skip_gates,
        stop_on_fail=args.stop_on_fail,
        report_formats=args.report_formats,
        output_json=Path('canoe/tmp/reports/verification/dev2_batch_report.json'),
        output_md=Path('canoe/tmp/reports/verification/dev2_batch_report.md'),
        output_csv=Path('canoe/tmp/reports/verification/dev2_batch_report.csv'),
        output_junit=Path('canoe/tmp/reports/verification/dev2_batch_report.junit.xml'),
    ))


def write_scenario_summary(args: argparse.Namespace, rc: int) -> None:
    payload = {
        'generated_at': dt.datetime.now().isoformat(),
        'scenario_id': args.id,
        'namespace': args.namespace,
        'var': args.var,
        'ack_var': args.ack_var,
        'wait_ack_ms': args.wait_ack_ms,
        'poll_ms': args.poll_ms,
        'status': 'PASS' if rc == 0 else 'FAIL',
        'detail': f"Scenario {args.id} acknowledged." if rc == 0 else f"Scenario {args.id} failed.",
    }
    SCENARIO_SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SCENARIO_SUMMARY_JSON.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = [
        '# Scenario Run Summary',
        '',
        f"- status: `{payload['status']}`",
        f"- scenario_id: `{payload['scenario_id']}`",
        f"- namespace: `{payload['namespace']}`",
        f"- variable: `{payload['var']}`",
        f"- ack_variable: `{payload['ack_var']}`",
        f"- wait_ack_ms: `{payload['wait_ack_ms']}`",
        f"- poll_ms: `{payload['poll_ms']}`",
        '',
        payload['detail'],
    ]
    SCENARIO_SUMMARY_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')

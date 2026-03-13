from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from cliops.canoe_com import CanoeComBridge, CanoeComError
from cliops.common import fail_unavailable, iso_today
from cliops.operator_result import SCENARIO_SUMMARY_JSON, SCENARIO_SUMMARY_MD
from cliops.platform_caps import canoe_runtime_check, platform_label
from cliops.verify_ops import cmd_verify_batch


def get_canoe_bridge() -> CanoeComBridge:
    return CanoeComBridge.connect()


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


def cmd_start_demo(args: argparse.Namespace) -> int:
    return cmd_scenario_run(argparse.Namespace(id=args.id, namespace='Test', var=args.var, ack_var='scenarioCommandAck', wait_ack_ms=args.wait_ack_ms, poll_ms=args.poll_ms, no_ensure_running=args.no_ensure_running))


def cmd_start_precheck(args: argparse.Namespace) -> int:
    return cmd_verify_batch(argparse.Namespace(
        run_id=args.run_id,
        campaign_id=args.campaign_id,
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

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from cliops.common import SCRIPTS, run_cmd
from cliops.operator_result import GATE_ALL_SUMMARY_JSON, GATE_ALL_SUMMARY_MD


def cmd_gate_doc_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / 'gates' / 'doc_code_sync_gate.py')])


def cmd_gate_cfg_hygiene(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / 'gates' / 'cfg_hygiene_gate.py')])


def cmd_gate_text_integrity(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / 'gates' / 'text_integrity_gate.py')])


def cmd_gate_capl_sync(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / 'gates' / 'check_capl_sync.py')])


def cmd_gate_multibus_dbc(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / 'gates' / 'multibus_cfg_dbc_gate.py')])


def cmd_gate_cli_readiness(_: argparse.Namespace) -> int:
    return run_cmd([sys.executable, str(SCRIPTS / 'gates' / 'cli_readiness_gate.py')])


def run_gate_all() -> int:
    gates = [
        ('doc-sync', cmd_gate_doc_sync),
        ('text-integrity', cmd_gate_text_integrity),
        ('cfg-hygiene', cmd_gate_cfg_hygiene),
        ('capl-sync', cmd_gate_capl_sync),
        ('multibus-dbc', cmd_gate_multibus_dbc),
        ('cli-readiness', cmd_gate_cli_readiness),
    ]
    failed = 0
    rows: list[dict[str, object]] = []
    for gate_name, gate_fn in gates:
        print(f'[WIZARD] gate -> {gate_name}')
        rc = gate_fn(argparse.Namespace())
        rows.append({'name': gate_name, 'rc': rc, 'status': 'PASS' if rc == 0 else 'FAIL'})
        if rc != 0:
            failed += 1
    _write_gate_all_summary(rows, failed)
    if failed:
        print(f'[WIZARD] gate summary: FAIL ({failed}/{len(gates)} failed)')
        return 2
    print(f'[WIZARD] gate summary: PASS ({len(gates)}/{len(gates)})')
    return 0


def cmd_gate_all(_: argparse.Namespace) -> int:
    return run_gate_all()


def run_named_gate(gate_name: str) -> int:
    mapping = {
        'doc-sync': cmd_gate_doc_sync,
        'text-integrity': cmd_gate_text_integrity,
        'cfg-hygiene': cmd_gate_cfg_hygiene,
        'capl-sync': cmd_gate_capl_sync,
        'multibus-dbc': cmd_gate_multibus_dbc,
        'cli-readiness': cmd_gate_cli_readiness,
    }
    fn = mapping.get(gate_name)
    if fn is None:
        print(f'[SHELL] unknown gate: {gate_name}')
        return 2
    return fn(argparse.Namespace())


def _write_gate_all_summary(rows: list[dict[str, object]], failed: int) -> None:
    payload = {
        'generated_at': dt.datetime.now().isoformat(),
        'status': 'PASS' if failed == 0 else 'FAIL',
        'failed': failed,
        'total': len(rows),
        'steps': rows,
    }
    GATE_ALL_SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    GATE_ALL_SUMMARY_JSON.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = [
        '# Gate All Summary',
        '',
        f"- status: `{payload['status']}`",
        f"- failed: `{payload['failed']}`",
        f"- total: `{payload['total']}`",
        '',
        '| gate | status | rc |',
        '|---|---|---:|',
    ]
    for row in rows:
        lines.append(f"| `{row['name']}` | `{row['status']}` | `{row['rc']}` |")
    GATE_ALL_SUMMARY_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')

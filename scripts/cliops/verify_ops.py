from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

from cliops.common import ROOT, SCRIPTS, run_cmd
from cliops.gate_ops import (
    cmd_gate_capl_sync,
    cmd_gate_cfg_hygiene,
    cmd_gate_cli_readiness,
    cmd_gate_doc_sync,
    cmd_gate_multibus_dbc,
)
from cliops.verification_policy import classify_step_status, load_phase_policy


def cmd_verify_prepare(args: argparse.Namespace) -> int:
    return run_cmd([
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'prepare',
        '--run-id',
        args.run_id,
    ])


def cmd_verify_smoke(args: argparse.Namespace) -> int:
    return run_cmd([
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'smoke',
        '--owner',
        args.owner,
        '--run-date',
        args.run_date,
    ])


def cmd_verify_fill_score(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'fill-score',
        '--tier',
        args.tier,
        '--run-id',
        args.run_id,
        '--owner',
        args.owner,
        '--run-date',
        args.run_date,
    ]
    if args.no_strict_metadata:
        cmd.append('--no-strict-metadata')
    if args.no_strict_axis:
        cmd.append('--no-strict-axis')
    if args.baseline_csv:
        cmd.extend(['--baseline-csv', str(args.baseline_csv)])
    return run_cmd(cmd)


def cmd_verify_insight(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'insight',
        '--run-id',
        args.run_id,
        '--output-md',
        str(args.output_md),
        '--output-json',
        str(args.output_json),
    ]
    if args.baseline_run_id:
        cmd.extend(['--baseline-run-id', args.baseline_run_id])
    if args.evidence_root:
        cmd.extend(['--evidence-root', str(args.evidence_root)])
    return run_cmd(cmd)


def cmd_verify_bind_doc(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'bind-doc',
        '--run-id',
        args.run_id,
        '--output-csv',
        str(args.output_csv),
        '--output-json',
        str(args.output_json),
        '--output-md',
        str(args.output_md),
    ]
    if args.evidence_root:
        cmd.extend(['--evidence-root', str(args.evidence_root)])
    if args.docs_root:
        cmd.extend(['--docs-root', str(args.docs_root)])
    return run_cmd(cmd)


def cmd_verify_fill_template(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'fill-template',
        '--run-id',
        args.run_id,
        '--owner-fallback',
        args.owner_fallback,
        '--date-fallback',
        args.date_fallback,
        '--binding-csv',
        str(args.binding_csv),
        '--binding-json',
        str(args.binding_json),
        '--binding-md',
        str(args.binding_md),
        '--output-csv',
        str(args.output_csv),
        '--output-md',
        str(args.output_md),
    ]
    if args.evidence_root:
        cmd.extend(['--evidence-root', str(args.evidence_root)])
    if args.docs_root:
        cmd.extend(['--docs-root', str(args.docs_root)])
    return run_cmd(cmd)


def cmd_verify_finalize(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'finalize',
        '--run-id',
        args.run_id,
        '--tiers',
        *args.tiers,
        '--owner',
        args.owner,
        '--run-date',
        args.run_date,
        '--owner-fallback',
        args.owner_fallback,
        '--date-fallback',
        args.date_fallback,
        '--insight-md',
        str(args.insight_md),
        '--insight-json',
        str(args.insight_json),
        '--binding-csv',
        str(args.binding_csv),
        '--binding-json',
        str(args.binding_json),
        '--binding-md',
        str(args.binding_md),
        '--fill-csv',
        str(args.fill_csv),
        '--fill-md',
        str(args.fill_md),
    ]
    if args.evidence_root:
        cmd.extend(['--evidence-root', str(args.evidence_root)])
    if args.docs_root:
        cmd.extend(['--docs-root', str(args.docs_root)])
    if args.baseline_run_id:
        cmd.extend(['--baseline-run-id', args.baseline_run_id])
    if args.no_strict_metadata:
        cmd.append('--no-strict-metadata')
    if args.no_strict_axis:
        cmd.append('--no-strict-axis')
    return run_cmd(cmd)


def cmd_verify_quick(args: argparse.Namespace) -> int:
    from cliops.runtime_ops import cmd_doctor

    steps = [
        (
            'doctor',
            lambda: cmd_doctor(
                argparse.Namespace(
                    ensure_running=True,
                    output_json=Path('canoe/tmp/reports/verification/doctor_report.json'),
                    output_md=Path('canoe/tmp/reports/verification/doctor_report.md'),
                )
            ),
        ),
        ('verify prepare', lambda: cmd_verify_prepare(argparse.Namespace(run_id=args.run_id))),
        ('verify smoke', lambda: cmd_verify_smoke(argparse.Namespace(owner=args.owner, run_date=args.run_date))),
        (
            'verify status',
            lambda: cmd_verify_status(
                argparse.Namespace(
                    run_id=args.run_id,
                    evidence_root='',
                    output_json='canoe/tmp/reports/verification/run_readiness.json',
                    output_md='canoe/tmp/reports/verification/run_readiness.md',
                )
            ),
        ),
    ]
    for step_name, step_fn in steps:
        print(f'[VERIFY_QUICK] {step_name}')
        rc = step_fn()
        if rc != 0:
            return rc
    return 0


def cmd_verify_status(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'run_verification_pipeline.py'),
        'status',
        '--run-id',
        args.run_id,
        '--output-json',
        str(args.output_json),
        '--output-md',
        str(args.output_md),
    ]
    if args.evidence_root:
        cmd.extend(['--evidence-root', str(args.evidence_root)])
    return run_cmd(cmd)


def cmd_verify_surface_bundle(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'build_surface_evidence_bundle.py'),
        '--inventory-json',
        str(args.inventory_json),
        '--traceability-json',
        str(args.traceability_json),
        '--doctor-json',
        str(args.doctor_json),
        '--readiness-json',
        str(args.readiness_json),
        '--batch-json',
        str(args.batch_json),
        '--smoke-csv',
        str(args.smoke_csv),
        '--output-json',
        str(args.output_json),
        '--output-md',
        str(args.output_md),
        '--surface-dir',
        str(args.surface_dir),
    ]
    return run_cmd(cmd)


def _materialize_verification_artifacts(*, run_id: str, phase: str) -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'materialize_verification_artifacts.py'),
        '--layout-json',
        'product/sdv_operator/config/verification_artifact_layout.json',
        '--run-id',
        run_id,
        '--phase',
        phase,
        '--staging-root',
        'canoe/tmp/reports/verification',
        '--evidence-root',
        'canoe/logging/evidence',
        '--surface-root',
        'canoe/tmp/reports/verification/surface',
    ]
    return run_cmd(cmd)


def _batch_artifact_rows(run_id: str, phase: str) -> list[dict[str, object]]:
    paths = [
        f'canoe/logging/evidence/UT/{run_id}/verification_log.csv',
        f'canoe/logging/evidence/UT/{run_id}/verification_log_scored.csv',
        f'canoe/logging/evidence/IT/{run_id}/verification_log.csv',
        f'canoe/logging/evidence/IT/{run_id}/verification_log_scored.csv',
        f'canoe/logging/evidence/ST/{run_id}/verification_log.csv',
        f'canoe/logging/evidence/ST/{run_id}/verification_log_scored.csv',
        'canoe/tmp/reports/verification/dev_completeness_smoke.csv',
        'canoe/tmp/reports/verification/dev_completeness_smoke.md',
        'canoe/tmp/reports/verification/run_readiness.json',
        'canoe/tmp/reports/verification/run_readiness.md',
        'canoe/tmp/reports/verification/dev2_batch_report.junit.xml',
        'canoe/tmp/reports/verification/surface_evidence_bundle.json',
        'canoe/tmp/reports/verification/surface_evidence_bundle.md',
        'canoe/tmp/reports/verification/run_insight_report.json',
        'canoe/tmp/reports/verification/run_insight_report.md',
        'canoe/tmp/reports/verification/doc_binding_bundle.json',
        'canoe/tmp/reports/verification/doc_binding_bundle.md',
        'canoe/tmp/reports/verification/doc_fill_template.csv',
        'canoe/tmp/reports/verification/doc_fill_template.md',
        f'artifacts/verification_runs/{run_id}/{phase}',
        f'artifacts/verification_runs/{run_id}/{phase}/manifests/artifact_manifest.json',
        f'artifacts/verification_runs/{run_id}/{phase}/manifests/artifact_manifest.md',
        f'artifacts/verification_runs/{run_id}/{phase}/manifests/execution_manifest.json',
        f'artifacts/verification_runs/{run_id}/{phase}/manifests/execution_manifest.md',
    ]
    rows: list[dict[str, object]] = []
    for rel in paths:
        p = ROOT / rel
        exists = p.exists()
        size = p.stat().st_size if exists and p.is_file() else 0
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime).isoformat() if exists else ''
        rows.append({'path': rel, 'exists': exists, 'size_bytes': size, 'last_modified': mtime})
    return rows


def _normalize_report_formats(raw: str) -> list[str]:
    allowed = {'json', 'md', 'csv', 'junit'}
    parts = [item.strip().lower() for item in raw.split(',') if item.strip()]
    if not parts:
        return ['json', 'md']
    out: list[str] = []
    for item in parts:
        if item not in allowed:
            raise ValueError(f'invalid report format: {item} (allowed: json,md,csv,junit)')
        if item not in out:
            out.append(item)
    return out


def _write_batch_report(*, run_id: str, owner: str, run_date: str, phase: str, policy: dict, steps: list[dict[str, object]], report_formats: list[str], output_json: Path, output_md: Path, output_csv: Path) -> None:
    write_json = 'json' in report_formats or 'junit' in report_formats
    if write_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
    if 'md' in report_formats:
        output_md.parent.mkdir(parents=True, exist_ok=True)
    if 'csv' in report_formats:
        output_csv.parent.mkdir(parents=True, exist_ok=True)

    pass_count = sum(1 for s in steps if s.get('status') == 'PASS')
    warn_count = sum(1 for s in steps if s.get('status') == 'WARN')
    fail_count = sum(1 for s in steps if s.get('status') == 'FAIL')
    status = 'FAIL' if fail_count else 'WARN' if warn_count else 'PASS'
    artifacts = _batch_artifact_rows(run_id, phase)
    payload = {
        'run_id': run_id,
        'owner': owner,
        'run_date': run_date,
        'phase': phase,
        'policy': policy,
        'status': status,
        'pass_count': pass_count,
        'warn_count': warn_count,
        'fail_count': fail_count,
        'steps': steps,
        'artifacts': artifacts,
        'generated_at': dt.datetime.now().isoformat(),
    }
    if write_json:
        output_json.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    if 'md' in report_formats:
        lines = [
            '# Dev2 Batch Verification Report',
            '',
            f'- run_id: `{run_id}`',
            f'- owner: `{owner}`',
            f'- run_date: `{run_date}`',
            f'- phase: `{phase}`',
            f'- status: `{status}`',
            f'- phase policy: `{policy.get("source", "-")}`',
            f'- pass/warn/fail: `{pass_count}/{warn_count}/{fail_count}`',
            '',
            '## Step Results',
            '',
            '| step | status | severity | rc |',
            '|---|---|---|---|',
        ]
        for step in steps:
            lines.append(f"| `{step['name']}` | `{step.get('status', 'UNKNOWN')}` | `{step.get('severity', 'mandatory')}` | `{step['rc']}` |")
        lines.extend(['', '## Artifact Snapshot', '', '| path | exists | size_bytes |', '|---|---:|---:|'])
        for row in artifacts:
            lines.append(f"| `{row['path']}` | `{str(row['exists']).lower()}` | `{row['size_bytes']}` |")
        output_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if 'csv' in report_formats:
        with output_csv.open('w', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=['row_type', 'run_id', 'phase', 'owner', 'run_date', 'status', 'step_name', 'step_status', 'step_severity', 'step_rc', 'artifact_path', 'artifact_exists', 'artifact_size_bytes', 'artifact_last_modified'])
            writer.writeheader()
            for step in steps:
                writer.writerow({'row_type': 'step', 'run_id': run_id, 'phase': phase, 'owner': owner, 'run_date': run_date, 'status': status, 'step_name': step['name'], 'step_status': step.get('status', 'UNKNOWN'), 'step_severity': step.get('severity', 'mandatory'), 'step_rc': step['rc'], 'artifact_path': '', 'artifact_exists': '', 'artifact_size_bytes': '', 'artifact_last_modified': ''})
            for row in artifacts:
                writer.writerow({'row_type': 'artifact', 'run_id': run_id, 'phase': phase, 'owner': owner, 'run_date': run_date, 'status': status, 'step_name': '', 'step_status': '', 'step_severity': '', 'step_rc': '', 'artifact_path': row['path'], 'artifact_exists': str(row['exists']).lower(), 'artifact_size_bytes': row['size_bytes'], 'artifact_last_modified': row['last_modified']})


def _maybe_export_batch_junit(*, report_formats: list[str], output_json: Path, output_junit: Path) -> int:
    if 'junit' not in report_formats:
        return 0
    cmd = [
        sys.executable,
        str(SCRIPTS / 'quality' / 'export_junit_from_batch.py'),
        '--batch-json',
        str(output_json),
        '--run-readiness',
        'canoe/tmp/reports/verification/run_readiness.json',
        '--doctor-report',
        'canoe/tmp/reports/verification/doctor_report.json',
        '--output-xml',
        str(output_junit),
    ]
    return run_cmd(cmd)


def _finalize_batch_reports(*, args: argparse.Namespace, policy: dict, report_formats: list[str], steps: list[dict[str, object]], exit_code: int) -> int:
    _write_batch_report(
        run_id=args.run_id,
        owner=args.owner,
        run_date=args.run_date,
        phase=args.phase,
        policy=policy,
        steps=steps,
        report_formats=report_formats,
        output_json=args.output_json,
        output_md=args.output_md,
        output_csv=args.output_csv,
    )
    junit_rc = _maybe_export_batch_junit(
        report_formats=report_formats,
        output_json=args.output_json,
        output_junit=args.output_junit,
    )
    if junit_rc != 0:
        return junit_rc
    surface_rc = cmd_verify_surface_bundle(
        argparse.Namespace(
            inventory_json=Path('product/sdv_operator/config/surface_ecu_inventory.json'),
            traceability_json=Path('product/sdv_operator/config/surface_traceability_profile.json'),
            doctor_json=Path('canoe/tmp/reports/verification/doctor_report.json'),
            readiness_json=Path('canoe/tmp/reports/verification/run_readiness.json'),
            batch_json=args.output_json,
            smoke_csv=Path('canoe/tmp/reports/verification/dev_completeness_smoke.csv'),
            output_json=Path('canoe/tmp/reports/verification/surface_evidence_bundle.json'),
            output_md=Path('canoe/tmp/reports/verification/surface_evidence_bundle.md'),
            surface_dir=Path('canoe/tmp/reports/verification/surface'),
        )
    )
    if surface_rc != 0:
        return surface_rc
    materialize_rc = _materialize_verification_artifacts(run_id=args.run_id, phase=args.phase)
    if materialize_rc != 0:
        return materialize_rc
    _write_batch_report(
        run_id=args.run_id,
        owner=args.owner,
        run_date=args.run_date,
        phase=args.phase,
        policy=policy,
        steps=steps,
        report_formats=report_formats,
        output_json=args.output_json,
        output_md=args.output_md,
        output_csv=args.output_csv,
    )
    return exit_code


def cmd_verify_batch(args: argparse.Namespace) -> int:
    from cliops.runtime_ops import cmd_doctor

    try:
        report_formats = _normalize_report_formats(args.report_formats)
    except ValueError as ex:
        print(f'[VERIFY_BATCH] FAIL: {ex}')
        return 2

    steps: list[dict[str, object]] = []
    policy = load_phase_policy(args.phase)

    def run_step(name: str, fn) -> int:
        rc = fn()
        step_status, severity = classify_step_status(name, rc, policy)
        steps.append({'name': name, 'rc': rc, 'status': step_status, 'severity': severity})
        return rc

    if args.phase in {'pre', 'full'}:
        if not args.skip_gates:
            gate_steps = [
                ('gate doc-sync', lambda: cmd_gate_doc_sync(argparse.Namespace())),
                ('gate cfg-hygiene', lambda: cmd_gate_cfg_hygiene(argparse.Namespace())),
                ('gate capl-sync', lambda: cmd_gate_capl_sync(argparse.Namespace())),
                ('gate multibus-dbc', lambda: cmd_gate_multibus_dbc(argparse.Namespace())),
                ('gate cli-readiness', lambda: cmd_gate_cli_readiness(argparse.Namespace())),
            ]
            for name, fn in gate_steps:
                rc = run_step(name, fn)
                current = steps[-1]
                if rc != 0 and args.stop_on_fail and current.get('status') == 'FAIL':
                    return _finalize_batch_reports(args=args, policy=policy, report_formats=report_formats, steps=steps, exit_code=2)

        pre_steps = [
            (
                'doctor',
                lambda: cmd_doctor(
                    argparse.Namespace(
                        ensure_running=True,
                        output_json=Path('canoe/tmp/reports/verification/doctor_report.json'),
                        output_md=Path('canoe/tmp/reports/verification/doctor_report.md'),
                    )
                ),
            ),
            ('verify prepare', lambda: cmd_verify_prepare(argparse.Namespace(run_id=args.run_id))),
            ('verify smoke', lambda: cmd_verify_smoke(argparse.Namespace(owner=args.owner, run_date=args.run_date))),
            ('verify status', lambda: cmd_verify_status(argparse.Namespace(run_id=args.run_id, evidence_root='', output_json='canoe/tmp/reports/verification/run_readiness.json', output_md='canoe/tmp/reports/verification/run_readiness.md'))),
        ]
        for name, fn in pre_steps:
            rc = run_step(name, fn)
            if name == 'doctor' and rc != 0:
                return _finalize_batch_reports(args=args, policy=policy, report_formats=report_formats, steps=steps, exit_code=2)
            if rc != 0 and args.stop_on_fail and steps[-1].get('status') == 'FAIL':
                return _finalize_batch_reports(args=args, policy=policy, report_formats=report_formats, steps=steps, exit_code=2)

    if args.phase in {'post', 'full'}:
        finalize_ns = argparse.Namespace(
            run_id=args.run_id,
            tiers=['UT', 'IT', 'ST'],
            owner=args.owner,
            run_date=args.run_date,
            owner_fallback=args.owner,
            date_fallback=args.run_date,
            baseline_run_id='',
            no_strict_metadata=False,
            no_strict_axis=False,
            evidence_root='',
            docs_root='',
            insight_md='canoe/tmp/reports/verification/run_insight_report.md',
            insight_json='canoe/tmp/reports/verification/run_insight_report.json',
            binding_csv='canoe/tmp/reports/verification/doc_binding_bundle.csv',
            binding_json='canoe/tmp/reports/verification/doc_binding_bundle.json',
            binding_md='canoe/tmp/reports/verification/doc_binding_bundle.md',
            fill_csv='canoe/tmp/reports/verification/doc_fill_template.csv',
            fill_md='canoe/tmp/reports/verification/doc_fill_template.md',
        )
        if run_step('verify finalize', lambda: cmd_verify_finalize(finalize_ns)) != 0 and args.stop_on_fail and steps[-1].get('status') == 'FAIL':
            return _finalize_batch_reports(args=args, policy=policy, report_formats=report_formats, steps=steps, exit_code=2)
        run_step('verify status', lambda: cmd_verify_status(argparse.Namespace(run_id=args.run_id, evidence_root='', output_json='canoe/tmp/reports/verification/run_readiness.json', output_md='canoe/tmp/reports/verification/run_readiness.md')))

    failed = sum(1 for s in steps if s.get('status') == 'FAIL')
    exit_code = 0 if failed == 0 else 2
    return _finalize_batch_reports(args=args, policy=policy, report_formats=report_formats, steps=steps, exit_code=exit_code)

#!/usr/bin/env python3
"""Materialize stable reviewer/CI artifact layout from staging verification outputs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LAYOUT = REPO_ROOT / "product" / "sdv_operator" / "config" / "verification_artifact_layout.json"


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict:
    path = _repo_path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_if_exists(src: Path, dst: Path) -> str | None:
    src = _repo_path(src)
    dst = _repo_path(dst)
    if not src.exists():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return _rel(dst)


def _copy_tree(src_root: Path, dst_root: Path) -> list[str]:
    src_root = _repo_path(src_root)
    dst_root = _repo_path(dst_root)
    copied: list[str] = []
    if not src_root.exists():
        return copied
    for src in src_root.rglob("*"):
        if not src.is_file():
            continue
        dst = dst_root / src.relative_to(src_root)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(_rel(dst))
    return copied


def _copy_native_reports(glob_pattern: str, dst_root: Path) -> list[str]:
    copied: list[str] = []
    for src in REPO_ROOT.glob(glob_pattern):
        if not src.is_file():
            continue
        try:
            rel = src.relative_to(REPO_ROOT)
        except ValueError:
            continue
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(_rel(dst))
    return copied


def _execution_manifest_payload(
    *,
    run_id: str,
    phase: str,
    layout_source: Path,
    reports_dir: Path,
    surface_dir: Path,
    native_reports_dir: Path,
    evidence_dir: Path,
    staging_root: Path,
    copied_reports: list[str],
    copied_surface: list[str],
    copied_native_reports: list[str],
    copied_evidence_files: list[str],
) -> dict:
    batch = _load_json(staging_root / "dev2_batch_report.json")
    readiness = _load_json(staging_root / "run_readiness.json")
    doctor = _load_json(staging_root / "doctor_report.json")
    surface_bundle = _load_json(staging_root / "surface_evidence_bundle.json")

    batch_campaign = batch.get("campaign", {}) if isinstance(batch.get("campaign"), dict) else {}
    execution = {}
    if isinstance(surface_bundle.get("execution"), dict):
        execution = dict(surface_bundle.get("execution", {}))
    else:
        execution = {
            "run_id": str(batch.get("run_id", run_id)),
            "phase": str(batch.get("phase", phase)),
            "owner": str(batch.get("owner", "")),
            "run_date": str(batch.get("run_date", "")),
            "campaign_id": str(batch.get("campaign_id", "")),
            "profile_id": str(batch.get("profile_id", "")),
            "pack_id": str(batch.get("pack_id", "")),
            "suite_id": str(batch.get("suite_id", (batch.get("campaign", {}) if isinstance(batch.get("campaign"), dict) else {}).get("suite_id", ""))),
            "assign_folder": str(batch.get("assign_folder", (batch.get("campaign", {}) if isinstance(batch.get("campaign"), dict) else {}).get("assign_folder", ""))),
            "surface_scope": str(batch_campaign.get("surface_scope", "ALL")),
            "repeat_count": int(batch_campaign.get("repeat_count", 1)),
            "duration_minutes": int(batch_campaign.get("duration_minutes", 0)),
            "interval_seconds": int(batch_campaign.get("interval_seconds", 0)),
            "stop_on_fail": bool(batch_campaign.get("stop_on_fail", False)),
            "generated_at": "",
            "executed_scenario_ids": [],
            "smoke_case_ids": [],
        }
    execution.setdefault("run_id", str(batch.get("run_id", run_id)))
    execution.setdefault("phase", str(batch.get("phase", phase)))
    execution.setdefault("owner", str(batch.get("owner", "")))
    execution.setdefault("run_date", str(batch.get("run_date", "")))
    execution.setdefault("campaign_id", str(batch.get("campaign_id", "")))
    execution.setdefault("profile_id", str(batch.get("profile_id", batch_campaign.get("profile_id", ""))))
    execution.setdefault("pack_id", str(batch.get("pack_id", batch_campaign.get("pack_id", ""))))
    execution.setdefault("suite_id", str(batch.get("suite_id", batch_campaign.get("suite_id", ""))))
    execution.setdefault("assign_folder", str(batch.get("assign_folder", batch_campaign.get("assign_folder", ""))))
    execution.setdefault("surface_scope", str(batch_campaign.get("surface_scope", "ALL")))
    execution.setdefault("repeat_count", int(batch_campaign.get("repeat_count", 1)))
    execution.setdefault("duration_minutes", int(batch_campaign.get("duration_minutes", 0)))
    execution.setdefault("interval_seconds", int(batch_campaign.get("interval_seconds", 0)))
    execution.setdefault("stop_on_fail", bool(batch_campaign.get("stop_on_fail", False)))

    surface_summary = []
    for item in surface_bundle.get("surfaces", []):
        if not isinstance(item, dict):
            continue
        surface_summary.append(
            {
                "surface_id": item.get("surface_id", ""),
                "status": item.get("status", ""),
                "bundle_key": item.get("bundle_key", ""),
                "traceability_status": item.get("traceability", {}).get("mapping_status", ""),
                "req_ids": item.get("traceability", {}).get("req_ids", []),
                "test_case_ids": item.get("traceability", {}).get("test_case_ids", {}),
                "scenario_ids": item.get("traceability", {}).get("scenario_ids", []),
            }
        )

    return {
        "schema": "sdv.verification.execution.manifest.v1",
        "run_id": run_id,
        "phase": phase,
        "layout_source": _rel(layout_source),
        "reports_dir": _rel(reports_dir),
        "surface_dir": _rel(surface_dir),
        "native_reports_dir": _rel(native_reports_dir),
        "evidence_dir": _rel(evidence_dir),
        "staging_root": _rel(staging_root),
        "execution": execution,
        "doctor_status": str(doctor.get("status", "UNKNOWN")).upper() if doctor else "MISSING",
        "readiness_status": str(readiness.get("overall_status", "UNKNOWN")).upper() if readiness else "MISSING",
        "batch_status": str(batch.get("status", "UNKNOWN")).upper() if batch else "MISSING",
        "surface_bundle_status": str(surface_bundle.get("overall_status", "UNKNOWN")).upper() if surface_bundle else "MISSING",
        "copied_reports": copied_reports,
        "copied_surface_files": copied_surface,
        "copied_native_reports": copied_native_reports,
        "copied_evidence_files": copied_evidence_files,
        "surface_summary": surface_summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize stable verification artifact layout")
    parser.add_argument("--layout-json", type=Path, default=DEFAULT_LAYOUT)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--phase", default="pre")
    parser.add_argument("--staging-root", type=Path, default=Path("canoe/tmp/reports/verification"))
    parser.add_argument("--evidence-root", type=Path, default=Path("canoe/logging/evidence"))
    parser.add_argument("--surface-root", type=Path, default=Path("canoe/tmp/reports/verification/surface"))
    args = parser.parse_args()

    layout = _load_json(args.layout_json)
    output_root = _repo_path(Path(layout.get("root", "artifacts/verification_runs")))
    staging_root = _repo_path(args.staging_root)
    evidence_root = _repo_path(args.evidence_root)
    surface_root = _repo_path(args.surface_root)

    run_root = output_root / args.run_id / args.phase
    reports_dir = run_root / "reports"
    surface_dir = run_root / "surface"
    native_reports_dir = run_root / "native_reports"
    evidence_dir = run_root / "evidence"
    manifests_dir = run_root / "manifests"
    reports_dir.mkdir(parents=True, exist_ok=True)
    surface_dir.mkdir(parents=True, exist_ok=True)
    native_reports_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    manifests_dir.mkdir(parents=True, exist_ok=True)

    copied_reports: list[str] = []
    for name in layout.get("copied_reports", []):
        copied = _copy_if_exists(staging_root / name, reports_dir / name)
        if copied:
            copied_reports.append(copied)

    copied_surface = _copy_tree(surface_root, surface_dir)
    copied_native_reports = _copy_native_reports(layout.get("native_report_glob", "canoe/**/*.vtestreport"), native_reports_dir)

    copied_evidence_files: list[str] = []
    for tier in ("UT", "IT", "ST"):
        copied_evidence_files.extend(_copy_tree(evidence_root / tier / args.run_id, evidence_dir / tier))

    batch = _load_json(staging_root / "dev2_batch_report.json")
    artifact_manifest = {
        "schema": "sdv.verification.artifact.materialized.v2",
        "run_id": args.run_id,
        "phase": args.phase,
        "campaign_id": str(batch.get("campaign_id", "")),
        "profile_id": str(batch.get("profile_id", "")),
        "pack_id": str(batch.get("pack_id", "")),
        "layout_source": _rel(args.layout_json),
        "reports_dir": _rel(reports_dir),
        "surface_dir": _rel(surface_dir),
        "native_reports_dir": _rel(native_reports_dir),
        "evidence_dir": _rel(evidence_dir),
        "staging_root": _rel(staging_root),
        "copied_reports": copied_reports,
        "copied_surface_files": copied_surface,
        "copied_native_reports": copied_native_reports,
        "copied_evidence_files": copied_evidence_files,
    }

    artifact_manifest_json = manifests_dir / "artifact_manifest.json"
    artifact_manifest_md = manifests_dir / "artifact_manifest.md"
    artifact_manifest_json.write_text(json.dumps(artifact_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    artifact_md_lines = [
        "# Verification Artifact Manifest",
        "",
        f"- Run ID: `{args.run_id}`",
        f"- Phase: `{args.phase}`",
        f"- Campaign ID: `{artifact_manifest['campaign_id'] or '-'}`",
        f"- Profile ID: `{artifact_manifest['profile_id'] or '-'}`",
        f"- Pack ID: `{artifact_manifest['pack_id'] or '-'}`",
        f"- Reports Dir: `{_rel(reports_dir)}`",
        f"- Surface Dir: `{_rel(surface_dir)}`",
        f"- Native Reports Dir: `{_rel(native_reports_dir)}`",
        f"- Evidence Dir: `{_rel(evidence_dir)}`",
        f"- Staging Root: `{_rel(staging_root)}`",
        "",
        "## Copied Reports",
    ]
    for item in copied_reports:
        artifact_md_lines.append(f"- `{item}`")
    artifact_md_lines += ["", "## Copied Surface Files"]
    for item in copied_surface:
        artifact_md_lines.append(f"- `{item}`")
    artifact_md_lines += ["", "## Copied Native Reports"]
    for item in copied_native_reports:
        artifact_md_lines.append(f"- `{item}`")
    artifact_md_lines += ["", "## Copied Evidence Files"]
    for item in copied_evidence_files:
        artifact_md_lines.append(f"- `{item}`")
    artifact_manifest_md.write_text("\n".join(artifact_md_lines) + "\n", encoding="utf-8")

    execution_manifest = _execution_manifest_payload(
        run_id=args.run_id,
        phase=args.phase,
        layout_source=args.layout_json,
        reports_dir=reports_dir,
        surface_dir=surface_dir,
        native_reports_dir=native_reports_dir,
        evidence_dir=evidence_dir,
        staging_root=staging_root,
        copied_reports=copied_reports,
        copied_surface=copied_surface,
        copied_native_reports=copied_native_reports,
        copied_evidence_files=copied_evidence_files,
    )
    execution_manifest_json = manifests_dir / "execution_manifest.json"
    execution_manifest_md = manifests_dir / "execution_manifest.md"
    execution_manifest_json.write_text(json.dumps(execution_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    exec_lines = [
        "# Verification Execution Manifest",
        "",
        f"- Run ID: `{execution_manifest['run_id']}`",
        f"- Phase: `{execution_manifest['phase']}`",
        f"- Owner: `{execution_manifest['execution'].get('owner', '-') or '-'}`",
        f"- Run Date: `{execution_manifest['execution'].get('run_date', '-') or '-'}`",
        f"- Campaign ID: `{execution_manifest['execution'].get('campaign_id', '-') or '-'}`",
        f"- Profile ID: `{execution_manifest['execution'].get('profile_id', '-') or '-'}`",
        f"- Pack ID: `{execution_manifest['execution'].get('pack_id', '-') or '-'}`",
        f"- Surface Scope: `{execution_manifest['execution'].get('surface_scope', '-') or '-'}`",
        f"- Repeat / Duration / Interval: `{execution_manifest['execution'].get('repeat_count', 1)}` / `{execution_manifest['execution'].get('duration_minutes', 0)} min` / `{execution_manifest['execution'].get('interval_seconds', 0)} sec`",
        f"- Stop On Fail: `{str(bool(execution_manifest['execution'].get('stop_on_fail', False))).lower()}`",
        f"- Executed Scenarios: `{', '.join(str(item) for item in execution_manifest['execution'].get('executed_scenario_ids', [])) or '-'}`",
        f"- Smoke Cases: `{', '.join(execution_manifest['execution'].get('smoke_case_ids', [])) or '-'}`",
        f"- Doctor / Readiness / Batch / Surface: `{execution_manifest['doctor_status']}` / `{execution_manifest['readiness_status']}` / `{execution_manifest['batch_status']}` / `{execution_manifest['surface_bundle_status']}`",
        "",
        "## Surface Summary",
        "",
        "| Surface ECU | Status | Traceability | Req IDs |",
        "| --- | --- | --- | --- |",
    ]
    for item in execution_manifest["surface_summary"]:
        exec_lines.append(
            f"| `{item['surface_id']}` | `{item['status']}` | `{item['traceability_status']}` | `{', '.join(item['req_ids']) or '-'}` |"
        )
    execution_manifest_md.write_text("\n".join(exec_lines) + "\n", encoding="utf-8")

    print(
        f"[ARTIFACT_LAYOUT] run={args.run_id} phase={args.phase} "
        f"reports={len(copied_reports)} surface_files={len(copied_surface)} "
        f"native_reports={len(copied_native_reports)} evidence_files={len(copied_evidence_files)}"
    )
    print(f"[OUT] {_rel(artifact_manifest_json)}")
    print(f"[OUT] {_rel(artifact_manifest_md)}")
    print(f"[OUT] {_rel(execution_manifest_json)}")
    print(f"[OUT] {_rel(execution_manifest_md)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

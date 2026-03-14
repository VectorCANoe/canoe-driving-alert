#!/usr/bin/env python3
"""Build surface-ECU-oriented evidence bundles from Dev2 verification outputs."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INVENTORY = REPO_ROOT / "product" / "sdv_operator" / "config" / "surface_ecu_inventory.json"
DEFAULT_TRACEABILITY = REPO_ROOT / "product" / "sdv_operator" / "config" / "surface_traceability_profile.json"
DEFAULT_REPORT_ROOT = REPO_ROOT / "canoe" / "tmp" / "reports" / "verification"
DEFAULT_SMOKE_CSV = DEFAULT_REPORT_ROOT / "dev_completeness_smoke.csv"
POLICY_PATH = REPO_ROOT / "product" / "sdv_operator" / "config" / "verification_phase_policy.json"


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (REPO_ROOT / path)


def _load_json(path: Path) -> dict:
    path = _repo_path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_phase_policy(phase: str) -> dict:
    if not POLICY_PATH.exists():
        return {
            "phase": phase,
            "readiness_warn_states": ["READY_FOR_FINALIZE", "PREPARED", "PREPARED_PARTIAL", "NOT_PREPARED"],
            "readiness_fail_states": ["MISSING", "BROKEN", "INVALID"],
            "source": "fallback",
        }
    raw = json.loads(POLICY_PATH.read_text(encoding="utf-8-sig"))
    profiles = raw.get("profiles", {}) if isinstance(raw, dict) else {}
    profile = profiles.get(phase, profiles.get("pre")) if isinstance(profiles, dict) else {}
    if not isinstance(profile, dict):
        profile = {}
    profile["phase"] = phase
    profile["source"] = _rel(POLICY_PATH)
    return profile


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    path = _repo_path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        return [dict(row) for row in reader]


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _status_rank(status: str) -> int:
    order = {"FAIL": 3, "WARN": 2, "PASS": 1, "INFO": 0}
    return order.get(status.upper(), 0)


def _merge_status(*statuses: str) -> str:
    current = "INFO"
    for item in statuses:
        if _status_rank(item) > _status_rank(current):
            current = item
    return current


def _doctor_status(doctor: dict) -> tuple[str, list[str]]:
    if not doctor:
        return "WARN", ["doctor report missing"]
    checks = doctor.get("checks", [])
    failed = [item for item in checks if isinstance(item, dict) and str(item.get("status", "")).upper() != "PASS"]
    if not failed:
        return "PASS", ["doctor PASS"]
    reasons = [f"{item.get('name', 'check')}: {item.get('detail', '-')}" for item in failed[:3]]
    if len(failed) == 1 and str(failed[0].get("name", "")) == "Measurement running":
        return "WARN", reasons
    return "FAIL", reasons


def _readiness_status(readiness: dict, phase_policy: dict) -> tuple[str, list[str]]:
    if not readiness:
        return "WARN", ["run readiness missing"]
    overall = str(readiness.get("overall_status", "")).upper()
    missing_items = readiness.get("missing_items", [])
    reasons = [str(item) for item in missing_items[:3]] if isinstance(missing_items, list) else []
    if overall in {"READY", "SCORED_READY", "PASS"}:
        return "PASS", [f"readiness {overall}"]
    fail_states = {str(item).upper() for item in phase_policy.get("readiness_fail_states", [])}
    warn_states = {str(item).upper() for item in phase_policy.get("readiness_warn_states", [])}
    if overall in fail_states:
        return "FAIL", [f"readiness {overall}", *reasons]
    if overall in warn_states or overall in {"READY_FOR_FINALIZE", "PREPARED", "PREPARED_PARTIAL", "NOT_PREPARED"}:
        return "WARN", [f"readiness {overall}", *reasons]
    return "WARN", [f"readiness {overall or 'UNKNOWN'}", *reasons]


def _batch_status(batch: dict) -> tuple[str, list[str]]:
    if not batch:
        return "WARN", ["batch report missing"]
    status = str(batch.get("status", "")).upper()
    pass_count = int(batch.get("pass_count", 0))
    warn_count = int(batch.get("warn_count", 0))
    fail_count = int(batch.get("fail_count", 0))
    if status == "PASS" and fail_count == 0 and warn_count == 0:
        return "PASS", [f"batch {batch.get('phase', 'pre')} PASS ({pass_count}/{pass_count + fail_count})"]
    if status == "WARN" and fail_count == 0:
        return "WARN", [f"batch {batch.get('phase', 'pre')} WARN ({pass_count} pass, {warn_count} warn)"]
    return "FAIL", [f"batch {batch.get('phase', 'pre')} FAIL ({pass_count}/{pass_count + fail_count})"]


def _artifact_list(report_root: Path) -> list[str]:
    report_root = _repo_path(report_root)
    artifacts = [
        report_root / "doctor_report.json",
        report_root / "doctor_report.md",
        report_root / "run_readiness.json",
        report_root / "run_readiness.md",
        report_root / "dev2_batch_report.json",
        report_root / "dev2_batch_report.md",
        report_root / "dev2_batch_report.junit.xml",
        report_root / "run_insight_report.json",
        report_root / "run_insight_report.md",
        report_root / "doc_binding_bundle.json",
        report_root / "doc_binding_bundle.md",
        report_root / "doc_fill_template.csv",
        report_root / "doc_fill_template.md",
    ]
    return [_rel(path) for path in artifacts if path.exists()]


def _traceability_index(traceability: dict) -> dict[str, dict]:
    surfaces = traceability.get("surfaces", [])
    out: dict[str, dict] = {}
    if not isinstance(surfaces, list):
        return out
    for item in surfaces:
        if not isinstance(item, dict):
            continue
        surface_id = str(item.get("surface_id", "")).strip().upper()
        if surface_id:
            out[surface_id] = item
    return out


def _execution_context(batch: dict, readiness: dict, doctor: dict, smoke_rows: list[dict[str, str]], traceability: dict) -> dict:
    scenario_ids: list[int] = []
    smoke_case_ids: list[str] = []
    for row in smoke_rows:
        raw_id = str(row.get("scenario_id", "")).strip()
        raw_case = str(row.get("test_id", "")).strip()
        if raw_case and raw_case not in smoke_case_ids:
            smoke_case_ids.append(raw_case)
        if raw_id.isdigit():
            value = int(raw_id)
            if value not in scenario_ids:
                scenario_ids.append(value)

    return {
        "run_id": str(batch.get("run_id") or readiness.get("run_id") or ""),
        "phase": str(batch.get("phase") or "pre"),
        "owner": str(batch.get("owner") or ""),
        "run_date": str(batch.get("run_date") or ""),
        "campaign_id": str(batch.get("campaign_id") or ""),
        "profile_id": str(batch.get("profile_id") or (batch.get("campaign", {}) if isinstance(batch.get("campaign"), dict) else {}).get("profile_id", "")),
        "pack_id": str(batch.get("pack_id") or (batch.get("campaign", {}) if isinstance(batch.get("campaign"), dict) else {}).get("pack_id", "")),
        "surface_scope": str(batch.get("campaign", {}).get("surface_scope", "ALL")) if isinstance(batch.get("campaign"), dict) else "ALL",
        "repeat_count": int(batch.get("campaign", {}).get("repeat_count", 1)) if isinstance(batch.get("campaign"), dict) else 1,
        "duration_minutes": int(batch.get("campaign", {}).get("duration_minutes", 0)) if isinstance(batch.get("campaign"), dict) else 0,
        "interval_seconds": int(batch.get("campaign", {}).get("interval_seconds", 0)) if isinstance(batch.get("campaign"), dict) else 0,
        "stop_on_fail": bool(batch.get("campaign", {}).get("stop_on_fail", False)) if isinstance(batch.get("campaign"), dict) else False,
        "generated_at": dt.datetime.now().isoformat(),
        "executed_scenario_ids": scenario_ids,
        "smoke_case_ids": smoke_case_ids,
        "doctor_status": str(doctor.get("status", "UNKNOWN")).upper() if doctor else "MISSING",
        "readiness_status": str(readiness.get("overall_status", "UNKNOWN")).upper() if readiness else "MISSING",
        "batch_status": str(batch.get("status", "UNKNOWN")).upper() if batch else "MISSING",
        "traceability_profile_source": traceability.get("source_docs", []),
    }


def _surface_traceability(profile: dict) -> dict:
    cases = profile.get("test_case_ids", {})
    if not isinstance(cases, dict):
        cases = {}
    return {
        "mapping_status": str(profile.get("mapping_status", "planned")),
        "req_ids": list(profile.get("req_ids", [])),
        "test_case_ids": {
            "ut": list(cases.get("ut", [])),
            "it": list(cases.get("it", [])),
            "st": list(cases.get("st", [])),
        },
        "scenario_ids": list(profile.get("scenario_ids", [])),
        "native_test_assets": list(profile.get("native_test_assets", [])),
        "doc_refs": list(profile.get("doc_refs", [])),
        "notes": str(profile.get("notes", "")),
    }


def _surface_rollup(
    surface: dict,
    traceability_profile: dict,
    doctor: dict,
    readiness: dict,
    batch: dict,
    artifacts: list[str],
    phase_policy: dict,
) -> dict:
    doctor_state, doctor_reasons = _doctor_status(doctor)
    readiness_state, readiness_reasons = _readiness_status(readiness, phase_policy)
    batch_state, batch_reasons = _batch_status(batch)

    surface_type = str(surface.get("surface_type", ""))
    surface_id = str(surface.get("surface_id", "UNKNOWN"))
    runtime_modules = [str(item) for item in surface.get("runtime_modules", [])]
    traceability = _surface_traceability(traceability_profile)

    if surface_id == "VALIDATION_HARNESS":
        status = _merge_status(readiness_state, batch_state)
        reasons = [*readiness_reasons, *batch_reasons]
    elif surface_type == "Infrastructure ECU":
        status = _merge_status(doctor_state, batch_state)
        reasons = [*doctor_reasons, *batch_reasons]
    else:
        status = _merge_status(batch_state, readiness_state)
        reasons = [*batch_reasons, *readiness_reasons]

    mapping_status = traceability["mapping_status"].upper()
    if mapping_status in {"PARTIAL", "PLANNED"} and status == "PASS":
        status = "WARN"
        reasons.append(f"traceability mapping is {traceability['mapping_status']}")

    if status == "PASS":
        next_action = "native CANoe test 증빙과 함께 Jenkins archive로 묶으십시오."
    elif status == "WARN":
        next_action = "surface별 native test 또는 marker/evidence/traceability 누락을 먼저 보강하십시오."
    else:
        next_action = "실패한 gate/batch/doctor 경로를 먼저 복구한 뒤 다시 rollup 하십시오."

    return {
        "surface_id": surface_id,
        "display_name": surface.get("display_name", surface_id),
        "bundle_key": surface.get("bundle_key", surface_id.lower()),
        "surface_type": surface_type,
        "report_order": int(surface.get("report_order", 999)),
        "runtime_modules": runtime_modules,
        "jenkins_bundle_key": surface.get("jenkins_bundle_key", ""),
        "status": status,
        "summary": reasons[0] if reasons else "no detail",
        "reasons": reasons[:5],
        "next_action": next_action,
        "traceability": traceability,
        "artifact_scope": {
            "shared_artifacts": artifacts,
            "native_archive_glob": "canoe/**/*.vtestreport",
            "evidence_root_glob": "canoe/logging/evidence/**/*",
            "note": "Dev2 provides normalized shared artifacts; Dev1 native reports remain archived as original evidence."
        }
    }


def _write_surface_markdown(path: Path, payload: dict) -> None:
    trace = payload["traceability"]
    lines = [
        f"# Surface Evidence Bundle - {payload['display_name']}",
        "",
        f"- Surface ECU: `{payload['surface_id']}`",
        f"- Type: `{payload['surface_type']}`",
        f"- Status: `{payload['status']}`",
        f"- Summary: {payload['summary']}",
        f"- Jenkins key: `{payload['jenkins_bundle_key']}`",
        f"- Traceability Status: `{trace['mapping_status']}`",
        "",
        "## Runtime Modules",
    ]
    for item in payload["runtime_modules"]:
        lines.append(f"- `{item}`")
    lines += ["", "## Traceability"]
    lines.append(f"- Req IDs: `{', '.join(trace['req_ids']) or '-'}`")
    lines.append(f"- UT: `{', '.join(trace['test_case_ids']['ut']) or '-'}`")
    lines.append(f"- IT: `{', '.join(trace['test_case_ids']['it']) or '-'}`")
    lines.append(f"- ST: `{', '.join(trace['test_case_ids']['st']) or '-'}`")
    lines.append(f"- Scenario IDs: `{', '.join(str(item) for item in trace['scenario_ids']) or '-'}`")
    lines.append(f"- Native Test Assets: `{', '.join(trace['native_test_assets']) or '-'}`")
    if trace["notes"]:
        lines.append(f"- Notes: {trace['notes']}")
    if trace["doc_refs"]:
        lines.append("- Doc Refs:")
        for item in trace["doc_refs"]:
            lines.append(f"  - `{item}`")
    lines += ["", "## Reasons"]
    for item in payload["reasons"]:
        lines.append(f"- {item}")
    lines += ["", "## Shared Artifacts"]
    for item in payload["artifact_scope"]["shared_artifacts"]:
        lines.append(f"- `{item}`")
    lines += [
        "",
        f"- Native reports: `{payload['artifact_scope']['native_archive_glob']}`",
        f"- Evidence root: `{payload['artifact_scope']['evidence_root_glob']}`",
        "",
        "## Next Action",
        f"- {payload['next_action']}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_bundle(
    inventory: dict,
    traceability: dict,
    doctor: dict,
    readiness: dict,
    batch: dict,
    smoke_rows: list[dict[str, str]],
    report_root: Path,
) -> dict:
    generated_at = dt.datetime.now().isoformat()
    artifacts = _artifact_list(report_root)
    traceability_idx = _traceability_index(traceability)
    phase = str(batch.get("phase") or "pre").lower()
    phase_policy = _load_phase_policy(phase)
    surfaces = sorted(
        [
            _surface_rollup(
                surface,
                traceability_idx.get(str(surface.get("surface_id", "")).upper(), {}),
                doctor,
                readiness,
                batch,
                artifacts,
                phase_policy,
            )
            for surface in inventory.get("surfaces", [])
        ],
        key=lambda item: item["report_order"],
    )
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for item in surfaces:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    overall = "FAIL" if counts["FAIL"] else "WARN" if counts["WARN"] else "PASS"
    return {
        "schema": "sdv.surface.evidence.bundle.v2",
        "generated_at": generated_at,
        "inventory_source": inventory.get("source_doc", ""),
        "traceability_profile": {
            "schema": traceability.get("schema", ""),
            "owner": traceability.get("owner", ""),
            "source_docs": traceability.get("source_docs", []),
        },
        "execution": _execution_context(batch, readiness, doctor, smoke_rows, traceability),
        "phase_policy": {
            "phase": phase_policy.get("phase", phase),
            "source": phase_policy.get("source", "fallback"),
            "description": phase_policy.get("description", ""),
            "advisory_steps": phase_policy.get("advisory_steps", []),
            "hard_fail_steps": phase_policy.get("hard_fail_steps", []),
            "readiness_warn_states": phase_policy.get("readiness_warn_states", []),
            "readiness_fail_states": phase_policy.get("readiness_fail_states", []),
        },
        "overall_status": overall,
        "summary": {
            "surface_count": len(surfaces),
            "pass_count": counts["PASS"],
            "warn_count": counts["WARN"],
            "fail_count": counts["FAIL"]
        },
        "global_context": {
            "doctor_status": str(doctor.get("status", "UNKNOWN")).upper() if doctor else "MISSING",
            "readiness_status": str(readiness.get("overall_status", "UNKNOWN")).upper() if readiness else "MISSING",
            "batch_status": str(batch.get("status", "UNKNOWN")).upper() if batch else "MISSING",
            "artifacts": artifacts
        },
        "surfaces": surfaces
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build surface ECU evidence bundle from Dev2 verification outputs")
    parser.add_argument("--inventory-json", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--traceability-json", type=Path, default=DEFAULT_TRACEABILITY)
    parser.add_argument("--doctor-json", type=Path, default=DEFAULT_REPORT_ROOT / "doctor_report.json")
    parser.add_argument("--readiness-json", type=Path, default=DEFAULT_REPORT_ROOT / "run_readiness.json")
    parser.add_argument("--batch-json", type=Path, default=DEFAULT_REPORT_ROOT / "dev2_batch_report.json")
    parser.add_argument("--smoke-csv", type=Path, default=DEFAULT_SMOKE_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_REPORT_ROOT / "surface_evidence_bundle.json")
    parser.add_argument("--output-md", type=Path, default=DEFAULT_REPORT_ROOT / "surface_evidence_bundle.md")
    parser.add_argument("--surface-dir", type=Path, default=DEFAULT_REPORT_ROOT / "surface")
    args = parser.parse_args()

    args.inventory_json = _repo_path(args.inventory_json)
    args.traceability_json = _repo_path(args.traceability_json)
    args.doctor_json = _repo_path(args.doctor_json)
    args.readiness_json = _repo_path(args.readiness_json)
    args.batch_json = _repo_path(args.batch_json)
    args.smoke_csv = _repo_path(args.smoke_csv)
    args.output_json = _repo_path(args.output_json)
    args.output_md = _repo_path(args.output_md)
    args.surface_dir = _repo_path(args.surface_dir)

    inventory = _load_json(args.inventory_json)
    if not inventory:
        print(f"[SURFACE_BUNDLE] FAIL: inventory not found: {args.inventory_json}")
        return 2

    traceability = _load_json(args.traceability_json)
    if not traceability:
        print(f"[SURFACE_BUNDLE] FAIL: traceability profile not found: {args.traceability_json}")
        return 2

    bundle = build_bundle(
        inventory=inventory,
        traceability=traceability,
        doctor=_load_json(args.doctor_json),
        readiness=_load_json(args.readiness_json),
        batch=_load_json(args.batch_json),
        smoke_rows=_load_csv_rows(args.smoke_csv),
        report_root=args.output_json.parent,
    )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.surface_dir.mkdir(parents=True, exist_ok=True)

    md_lines = [
        "# Surface Evidence Bundle",
        "",
        f"- Overall: `{bundle['overall_status']}`",
        f"- Run ID: `{bundle['execution']['run_id'] or '-'}`",
        f"- Campaign ID: `{bundle['execution']['campaign_id'] or '-'}`",
        f"- Profile ID: `{bundle['execution'].get('profile_id', '-') or '-'}`",
        f"- Pack ID: `{bundle['execution'].get('pack_id', '-') or '-'}`",
        f"- Phase: `{bundle['execution']['phase'] or '-'}`",
        f"- Phase Policy: `{bundle['phase_policy']['source']}`",
        f"- Owner: `{bundle['execution']['owner'] or '-'}`",
        f"- Run Date: `{bundle['execution']['run_date'] or '-'}`",
        f"- Surface Scope: `{bundle['execution']['surface_scope'] or '-'}`",
        f"- Repeat / Duration / Interval: `{bundle['execution']['repeat_count']}` / `{bundle['execution']['duration_minutes']} min` / `{bundle['execution']['interval_seconds']} sec`",
        f"- Stop On Fail: `{str(bool(bundle['execution']['stop_on_fail'])).lower()}`",
        f"- Executed Scenarios: `{', '.join(str(item) for item in bundle['execution']['executed_scenario_ids']) or '-'}`",
        f"- Smoke Cases: `{', '.join(bundle['execution']['smoke_case_ids']) or '-'}`",
        f"- Surfaces: `{bundle['summary']['surface_count']}`",
        f"- PASS/WARN/FAIL: `{bundle['summary']['pass_count']}/{bundle['summary']['warn_count']}/{bundle['summary']['fail_count']}`",
        f"- Inventory Source: `{bundle['inventory_source']}`",
        "",
        "## Surface Rollup",
        "",
        "| Surface ECU | Traceability | Type | Runtime Modules | Status | Summary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for surface in bundle["surfaces"]:
        runtime = ", ".join(f"`{item}`" for item in surface["runtime_modules"])
        md_lines.append(
            f"| `{surface['surface_id']}` | `{surface['traceability']['mapping_status']}` | {surface['surface_type']} | {runtime} | `{surface['status']}` | {surface['summary']} |"
        )
        surface_root = args.surface_dir / surface["bundle_key"]
        surface_root.mkdir(parents=True, exist_ok=True)
        surface_json = surface_root / "bundle.json"
        surface_md = surface_root / "bundle.md"
        surface["bundle_json"] = _rel(surface_json)
        surface["bundle_md"] = _rel(surface_md)
        surface_json.write_text(json.dumps(surface, indent=2, ensure_ascii=False), encoding="utf-8")
        _write_surface_markdown(surface_md, surface)

    args.output_json.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    args.output_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"[SURFACE_BUNDLE] status={bundle['overall_status']} surfaces={bundle['summary']['surface_count']}")
    print(f"[OUT] {_rel(args.output_json)}")
    print(f"[OUT] {_rel(args.output_md)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

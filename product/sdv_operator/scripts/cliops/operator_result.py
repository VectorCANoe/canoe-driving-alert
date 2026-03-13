from __future__ import annotations

import argparse
import datetime as dt
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
import sys
from typing import Any


def _find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "AGENTS.md").exists() and (candidate / "canoe").exists():
            return candidate
    return current.parents[-1]


ROOT = _find_repo_root()
ROOT_SCRIPTS = ROOT / "scripts"
if str(ROOT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ROOT_SCRIPTS))

from cliops.command_catalog import build_command_index
from release.layout import EXE_ONEFILE_PATH, EXE_ONEFOLDER_DIR, PORTABLE_FOLDER_PATH, PORTABLE_ZIP_PATH

COMMAND_INDEX = build_command_index()
VERIFICATION_ROOT = ROOT / "canoe" / "tmp" / "reports" / "verification"
LAST_OPERATOR_RESULT_PATH = VERIFICATION_ROOT / "last_operator_result.json"
SCENARIO_SUMMARY_JSON = VERIFICATION_ROOT / "scenario_run_summary.json"
SCENARIO_SUMMARY_MD = VERIFICATION_ROOT / "scenario_run_summary.md"
GATE_ALL_SUMMARY_JSON = VERIFICATION_ROOT / "gate_all_summary.json"
GATE_ALL_SUMMARY_MD = VERIFICATION_ROOT / "gate_all_summary.md"
RELEASE_CONTRACT_JSON = VERIFICATION_ROOT / "release_contract_report.json"
RELEASE_CONTRACT_MD = VERIFICATION_ROOT / "release_contract_report.md"
SURFACE_BUNDLE_JSON = VERIFICATION_ROOT / "surface_evidence_bundle.json"
SURFACE_BUNDLE_MD = VERIFICATION_ROOT / "surface_evidence_bundle.md"


@dataclass
class OperatorResult:
    schema: str = "sdv.operator.result.v1"
    command_id: str = ""
    title: str = ""
    status: str = "IDLE"
    detail: str = ""
    next_action: str = ""
    rc: int = 0
    generated_at: str = field(default_factory=lambda: dt.datetime.now().isoformat())
    artifacts: list[str] = field(default_factory=list)
    related_logs: list[str] = field(default_factory=list)
    insight: dict[str, str] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _existing_artifacts(paths: list[Path]) -> list[str]:
    out: list[str] = []
    for path in paths:
        try:
            if path.exists():
                out.append(str(path.relative_to(ROOT)).replace("\\", "/"))
        except Exception:
            continue
    return out


def _run_id_from_args(args: argparse.Namespace) -> str:
    raw = getattr(args, "run_id", "")
    return str(raw).strip()


def _title_for_command(command_id: str) -> str:
    cmd = COMMAND_INDEX.get(command_id)
    return cmd.title if cmd else command_id


def _artifact_candidates(command_id: str, args: argparse.Namespace) -> list[Path]:
    run_id = _run_id_from_args(args)
    phase = str(getattr(args, "phase", "pre")).lower()
    paths: list[Path] = []
    if command_id == "inspect.environment_doctor":
        paths.extend([VERIFICATION_ROOT / "doctor_report.json", VERIFICATION_ROOT / "doctor_report.md"])
    elif command_id == "verify.all_gates":
        paths.extend([GATE_ALL_SUMMARY_JSON, GATE_ALL_SUMMARY_MD])
    elif command_id in {"verify.precheck_batch", "verify.batch"}:
        paths.extend(
            [
                VERIFICATION_ROOT / "dev2_batch_report.json",
                VERIFICATION_ROOT / "dev2_batch_report.md",
                VERIFICATION_ROOT / "dev2_batch_report.csv",
                VERIFICATION_ROOT / "dev2_batch_report.junit.xml",
                SURFACE_BUNDLE_JSON,
                SURFACE_BUNDLE_MD,
            ]
        )
        if run_id:
            paths.append(ROOT / "artifacts" / "verification_runs" / run_id / phase)
            paths.append(ROOT / "artifacts" / "verification_runs" / run_id / phase / "manifests" / "execution_manifest.json")
            paths.append(ROOT / "artifacts" / "verification_runs" / run_id / phase / "manifests" / "execution_manifest.md")
    elif command_id == "verify.surface_bundle":
        paths.extend([SURFACE_BUNDLE_JSON, SURFACE_BUNDLE_MD])
        if run_id:
            paths.append(ROOT / "artifacts" / "verification_runs" / run_id / phase)
            paths.append(ROOT / "artifacts" / "verification_runs" / run_id / phase / "manifests" / "execution_manifest.json")
            paths.append(ROOT / "artifacts" / "verification_runs" / run_id / phase / "manifests" / "execution_manifest.md")
    elif command_id in {"verify.quick_verify", "verify.run_readiness_status"}:
        paths.extend([VERIFICATION_ROOT / "run_readiness.json", VERIFICATION_ROOT / "run_readiness.md"])
        if run_id:
            for tier in ("UT", "IT", "ST"):
                paths.append(ROOT / "canoe" / "logging" / "evidence" / tier / run_id / "verification_log.csv")
    elif command_id == "operate.scenario_trigger":
        paths.extend([SCENARIO_SUMMARY_JSON, SCENARIO_SUMMARY_MD])
    elif command_id == "package.portable_bundle":
        paths.extend([PORTABLE_FOLDER_PATH, PORTABLE_ZIP_PATH])
    elif command_id == "package.windows_exe":
        paths.extend([EXE_ONEFOLDER_DIR, EXE_ONEFILE_PATH])
    elif command_id == "package.validate_contract":
        paths.extend([RELEASE_CONTRACT_JSON, RELEASE_CONTRACT_MD])
    elif command_id.startswith("artifact.list"):
        scope = str(getattr(args, "scope", "staging")).lower()
        if scope == "source":
            paths.extend(
                [
                    ROOT / "product" / "sdv_operator" / "config" / "surface_ecu_inventory.json",
                    ROOT / "product" / "sdv_operator" / "config" / "native_canoe_test_portfolio_v1.json",
                    ROOT / "product" / "sdv_operator" / "config" / "network_gateway_verification_pack_v1.json",
                    ROOT / "product" / "sdv_operator" / "config" / "verification_pack_matrix.json",
                    ROOT / "product" / "sdv_operator" / "config" / "campaign_profiles.json",
                    ROOT / "product" / "sdv_operator" / "config" / "capability_boundary_matrix.json",
                    ROOT / "product" / "sdv_operator" / "config" / "surface_traceability_profile.json",
                    ROOT / "product" / "sdv_operator" / "config" / "verification_artifact_layout.json",
                    ROOT / "product" / "sdv_operator" / "docs-src" / "role-boundary.md",
                    ROOT / "product" / "sdv_operator" / "docs-src" / "capability-boundary.md",
                ]
            )
        elif scope == "build":
            paths.extend(
                [
                    ROOT / "dist",
                    ROOT / "build",
                    ROOT / "product" / "sdv_operator" / "site",
                ]
            )
        elif scope == "archive":
            paths.append(ROOT / "artifacts" / "verification_runs")
        else:
            paths.append(VERIFICATION_ROOT)
    elif command_id.startswith("artifact.open"):
        target = str(getattr(args, "target", "")).strip().lower()
        target_map = {
            "batch-report": VERIFICATION_ROOT / "dev2_batch_report.md",
            "surface-bundle": SURFACE_BUNDLE_MD,
            "readiness": VERIFICATION_ROOT / "run_readiness.md",
            "doctor": VERIFICATION_ROOT / "doctor_report.md",
            "surface-inventory": ROOT / "product" / "sdv_operator" / "config" / "surface_ecu_inventory.json",
            "native-test-portfolio": ROOT / "product" / "sdv_operator" / "config" / "native_canoe_test_portfolio_v1.json",
            "native-testcase-blueprints": ROOT / "product" / "sdv_operator" / "config" / "native_testcase_blueprints_v1.json",
            "network-gateway-pack": ROOT / "product" / "sdv_operator" / "config" / "network_gateway_verification_pack_v1.json",
            "verification-pack-matrix": ROOT / "product" / "sdv_operator" / "config" / "verification_pack_matrix.json",
            "campaign-profiles": ROOT / "product" / "sdv_operator" / "config" / "campaign_profiles.json",
            "capability-matrix-json": ROOT / "product" / "sdv_operator" / "config" / "capability_boundary_matrix.json",
            "traceability-profile": ROOT / "product" / "sdv_operator" / "config" / "surface_traceability_profile.json",
            "artifact-layout": ROOT / "product" / "sdv_operator" / "config" / "verification_artifact_layout.json",
            "phase-policy": ROOT / "product" / "sdv_operator" / "config" / "verification_phase_policy.json",
            "manifest": ROOT / "product" / "sdv_operator" / "manifest.json",
            "commands-doc": ROOT / "product" / "sdv_operator" / "docs-src" / "commands.md",
            "results-doc": ROOT / "product" / "sdv_operator" / "docs-src" / "results.md",
            "packaging-doc": ROOT / "product" / "sdv_operator" / "docs-src" / "packaging.md",
            "role-boundary-doc": ROOT / "product" / "sdv_operator" / "docs-src" / "role-boundary.md",
            "capability-matrix-doc": ROOT / "product" / "sdv_operator" / "docs-src" / "capability-boundary.md",
        }
        resolved = target_map.get(target)
        if resolved:
            paths.append(resolved)
        elif target == "build-root":
            paths.append(ROOT / "dist")
        elif target in {"execution-manifest", "archive-run", "reports-dir", "surface-dir", "native-reports"}:
            paths.append(ROOT / "artifacts" / "verification_runs")
    return paths


def _doctor_result(command_id: str, title: str, rc: int) -> OperatorResult:
    data = _load_json(VERIFICATION_ROOT / "doctor_report.json")
    artifacts = _existing_artifacts([VERIFICATION_ROOT / "doctor_report.json", VERIFICATION_ROOT / "doctor_report.md"])
    if not data:
        status = "PASS" if rc == 0 else "FAIL"
        detail = "Doctor command completed." if rc == 0 else "Doctor command failed."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status=status,
            detail=detail,
            next_action="Measurement와 sysvar 상태를 확인하십시오.",
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Doctor", "bottleneck": detail, "next_action": "Measurement와 sysvar 상태를 확인하십시오."},
        )

    failed_checks = [
        item
        for item in data.get("checks", [])
        if isinstance(item, dict) and str(item.get("status", "")).upper() != "PASS"
    ]
    if not failed_checks:
        detail = "Doctor checks passed."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status="PASS",
            detail=detail,
            next_action="Scenario run 또는 Verify quick으로 넘어가십시오.",
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Doctor", "bottleneck": detail, "next_action": "Scenario run 또는 Verify quick으로 넘어가십시오."},
        )

    first = failed_checks[0]
    detail = f"{first.get('name', 'check')}: {first.get('detail', '-')}"
    status = "WARN" if len(failed_checks) == 1 and str(first.get("name", "")) == "Measurement running" else "FAIL"
    next_action = "Measurement를 먼저 시작하십시오." if "Measurement running" in detail else "COM attach와 sysvar 접근 경로를 확인하십시오."
    return OperatorResult(
        command_id=command_id,
        title=title,
        status=status,
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        insight={"stage": "Doctor", "bottleneck": detail, "next_action": next_action},
    )


def _readiness_result(command_id: str, title: str, rc: int, args: argparse.Namespace) -> OperatorResult:
    data = _load_json(VERIFICATION_ROOT / "run_readiness.json")
    artifacts = _existing_artifacts(_artifact_candidates(command_id, args))
    if not data:
        status = "PASS" if rc == 0 else "FAIL"
        detail = "Run readiness artifacts are not available yet." if rc == 0 else "Verify readiness command failed."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status=status,
            detail=detail,
            next_action="run_readiness.json 생성 여부를 확인하십시오.",
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Verify", "bottleneck": detail, "next_action": "run_readiness.json 생성 여부를 확인하십시오."},
            context={"run_id": _run_id_from_args(args)},
        )

    overall = str(data.get("overall_status", "UNKNOWN")).strip().upper()
    missing_items = data.get("missing_items", [])
    missing_count = len(missing_items) if isinstance(missing_items, list) else 0
    if overall in {"READY", "PREPARED", "PASS"} and missing_count == 0:
        status = "PASS"
        detail = f"{overall}: evidence run is ready."
        next_action = "증빙을 05/06/07에 연결하십시오."
    else:
        status = "WARN" if rc == 0 else "FAIL"
        detail = f"{overall}: missing={missing_count}"
        next_action = "UT/IT/ST 누락 항목과 [EVIDENCE_OUT] marker를 보강하십시오."
    related_logs = missing_items[:3] if isinstance(missing_items, list) else []
    return OperatorResult(
        command_id=command_id,
        title=title,
        status=status,
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        related_logs=[str(item) for item in related_logs],
        insight={"stage": "Verify", "bottleneck": detail, "next_action": next_action},
        context={"run_id": data.get("run_id", _run_id_from_args(args)), "overall_status": overall},
    )


def _batch_result(command_id: str, title: str, rc: int, args: argparse.Namespace) -> OperatorResult:
    data = _load_json(VERIFICATION_ROOT / "dev2_batch_report.json")
    surface_data = _load_json(SURFACE_BUNDLE_JSON)
    artifacts = _existing_artifacts(_artifact_candidates(command_id, args))
    if not data:
        status = "PASS" if rc == 0 else "FAIL"
        detail = "Batch verification completed." if rc == 0 else "Batch verification failed."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status=status,
            detail=detail,
            next_action="배치 산출물 생성 여부를 확인하십시오.",
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Verify Batch", "bottleneck": detail, "next_action": "배치 산출물 생성 여부를 확인하십시오."},
            context={"run_id": _run_id_from_args(args)},
        )

    phase = str(data.get("phase", "pre")).upper()
    status = str(data.get("status", "FAIL")).upper()
    campaign_id = str(data.get("campaign_id", "-") or "-")
    surface_scope = (
        str(data.get("campaign", {}).get("surface_scope", "-"))
        if isinstance(data.get("campaign", {}), dict)
        else "-"
    )
    detail = f"{phase}: {data.get('pass_count', 0)} pass / {data.get('fail_count', 0)} fail | campaign={campaign_id} | scope={surface_scope}"
    if int(data.get("warn_count", 0)):
        detail = f"{detail} / {data.get('warn_count', 0)} warn"
    if surface_data:
        bundle_status = str(surface_data.get("overall_status", "UNKNOWN")).upper()
        detail = f"{detail} | surface={bundle_status}"
    next_action = (
        "PASS면 본 검증 시나리오로 넘어가십시오."
        if status == "PASS"
        else "WARN 항목이 advisory인지 mandatory인지 확인하고, release 전에는 모두 정리하십시오."
        if status == "WARN"
        else "실패한 step과 gate를 먼저 수정하십시오."
    )
    return OperatorResult(
        command_id=command_id,
        title=title,
        status="PASS" if status == "PASS" else "WARN" if status == "WARN" else "FAIL",
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        insight={"stage": "Verify Batch", "bottleneck": detail, "next_action": next_action},
        context={
            "run_id": data.get("run_id", _run_id_from_args(args)),
            "campaign_id": campaign_id,
            "phase": phase,
            "surface_scope": surface_scope,
        },
    )


def _surface_bundle_result(command_id: str, title: str, rc: int, args: argparse.Namespace) -> OperatorResult:
    data = _load_json(SURFACE_BUNDLE_JSON)
    artifacts = _existing_artifacts(_artifact_candidates(command_id, args))
    if not data:
        status = "PASS" if rc == 0 else "FAIL"
        detail = "Surface ECU evidence bundle completed." if rc == 0 else "Surface ECU evidence bundle failed."
        next_action = "bundle 산출물 생성 여부를 확인하십시오."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status=status,
            detail=detail,
            next_action=next_action,
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Surface Bundle", "bottleneck": detail, "next_action": next_action},
            context={"run_id": _run_id_from_args(args)},
        )

    overall = str(data.get("overall_status", "UNKNOWN")).upper()
    summary = data.get("summary", {}) if isinstance(data.get("summary", {}), dict) else {}
    detail = (
        f"surface={overall} | "
        f"PASS/WARN/FAIL={summary.get('pass_count', 0)}/{summary.get('warn_count', 0)}/{summary.get('fail_count', 0)}"
    )
    next_action = "surface ECU 기준 묶음을 Jenkins archive와 reviewer package에 연결하십시오." if overall == "PASS" else "WARN/FAIL surface ECU의 reason과 native evidence 연결 상태를 먼저 보강하십시오."
    related_logs: list[str] = []
    surfaces = data.get("surfaces", [])
    if isinstance(surfaces, list):
        for item in surfaces:
            if not isinstance(item, dict):
                continue
            status = str(item.get("status", "")).upper()
            if status in {"WARN", "FAIL"}:
                trace_state = item.get("traceability", {}).get("mapping_status", "")
                related_logs.append(f"{item.get('surface_id', 'SURFACE')}: {item.get('summary', '-')} (trace={trace_state or '-'})")
            if len(related_logs) >= 3:
                break
    mapped_status = "PASS" if overall == "PASS" else "WARN" if overall == "WARN" else "FAIL"
    return OperatorResult(
        command_id=command_id,
        title=title,
        status=mapped_status,
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        related_logs=related_logs,
        insight={"stage": "Surface Bundle", "bottleneck": detail, "next_action": next_action},
        context={"run_id": _run_id_from_args(args), "overall_status": overall},
    )


def _gate_all_result(command_id: str, title: str, rc: int) -> OperatorResult:
    data = _load_json(GATE_ALL_SUMMARY_JSON)
    artifacts = _existing_artifacts([GATE_ALL_SUMMARY_JSON, GATE_ALL_SUMMARY_MD])
    if not data:
        status = "PASS" if rc == 0 else "FAIL"
        detail = "Gate bundle passed." if rc == 0 else "One or more gates failed."
        next_action = "PASS면 Scenario run으로 넘어가십시오." if rc == 0 else "실패한 gate를 먼저 수정하십시오."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status=status,
            detail=detail,
            next_action=next_action,
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Gates", "bottleneck": detail, "next_action": next_action},
        )

    failed = int(data.get("failed", 0))
    total = int(data.get("total", 0))
    status = "PASS" if failed == 0 else "FAIL"
    detail = f"gate summary: {status.lower()} ({total - failed}/{total})"
    next_action = "PASS면 Scenario run으로 넘어가십시오." if failed == 0 else "실패한 gate를 먼저 수정하십시오."
    return OperatorResult(
        command_id=command_id,
        title=title,
        status=status,
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        insight={"stage": "Gates", "bottleneck": detail, "next_action": next_action},
        context={"failed": failed, "total": total},
    )


def _scenario_result(command_id: str, title: str, rc: int, args: argparse.Namespace) -> OperatorResult:
    data = _load_json(SCENARIO_SUMMARY_JSON)
    artifacts = _existing_artifacts([SCENARIO_SUMMARY_JSON, SCENARIO_SUMMARY_MD])
    scenario_id = getattr(args, "id", "")
    if data:
        status = "PASS" if str(data.get("status", "")).upper() == "PASS" else "FAIL"
        detail = str(data.get("detail", f"Scenario {scenario_id} {'acknowledged' if rc == 0 else 'failed'}"))
    else:
        status = "PASS" if rc == 0 else "FAIL"
        detail = f"Scenario {scenario_id} acknowledged." if rc == 0 else f"Scenario {scenario_id} failed."
    next_action = "ack가 확인되면 Verify quick으로 넘어가십시오." if status == "PASS" else "measurement와 Test sysvar 경로를 다시 점검하십시오."
    return OperatorResult(
        command_id=command_id,
        title=title,
        status=status,
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        insight={"stage": "Scenario", "bottleneck": detail, "next_action": next_action},
        context={"scenario_id": scenario_id, "var": getattr(args, "var", "scenarioCommand")},
    )


def _release_contract_result(command_id: str, title: str, rc: int) -> OperatorResult:
    data = _load_json(RELEASE_CONTRACT_JSON)
    artifacts = _existing_artifacts([RELEASE_CONTRACT_JSON, RELEASE_CONTRACT_MD])
    if not data:
        status = "PASS" if rc == 0 else "FAIL"
        detail = "Release contract validation completed." if rc == 0 else "Release contract validation failed."
        next_action = "PASS면 build-exe 또는 bundle-portable로 넘어가십시오." if rc == 0 else "manifest와 layout drift를 먼저 수정하십시오."
        return OperatorResult(
            command_id=command_id,
            title=title,
            status=status,
            detail=detail,
            next_action=next_action,
            rc=rc,
            artifacts=artifacts,
            insight={"stage": "Packaging", "bottleneck": detail, "next_action": next_action},
        )

    status = str(data.get("status", "FAIL")).upper()
    detail = str(data.get("detail", "release contract result unavailable"))
    failed_checks = [
        item for item in data.get("checks", [])
        if isinstance(item, dict) and str(item.get("status", "")).upper() != "PASS"
    ]
    related_logs = [f"{item.get('name', 'check')}: {item.get('detail', '-')}" for item in failed_checks[:3]]
    next_action = "PASS면 build-exe 또는 bundle-portable로 넘어가십시오." if status == "PASS" else "manifest public surface와 release_artifacts drift를 먼저 수정하십시오."
    return OperatorResult(
        command_id=command_id,
        title=title,
        status="PASS" if status == "PASS" else "FAIL",
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        related_logs=related_logs,
        insight={"stage": "Packaging", "bottleneck": detail, "next_action": next_action},
    )


def _generic_result(command_id: str, title: str, rc: int, args: argparse.Namespace) -> OperatorResult:
    artifacts = _existing_artifacts(_artifact_candidates(command_id, args))
    status = "PASS" if rc == 0 else "FAIL"
    detail = "Command completed successfully." if rc == 0 else "Command returned a non-zero exit code."
    next_action = "Results와 Logs를 함께 확인하십시오." if rc == 0 else "stderr/stdout과 COM 상태를 확인하십시오."
    return OperatorResult(
        command_id=command_id,
        title=title,
        status=status,
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        insight={"stage": title, "bottleneck": detail, "next_action": next_action},
        context={"run_id": _run_id_from_args(args)},
    )


def _artifact_result(command_id: str, title: str, rc: int, args: argparse.Namespace) -> OperatorResult:
    artifacts = _existing_artifacts(_artifact_candidates(command_id, args))
    if command_id.startswith("artifact.list"):
        scope = str(getattr(args, "scope", "staging")).lower()
        detail = f"{scope} artifact listing completed."
        next_action = "필요한 항목은 artifact open으로 바로 여십시오."
    else:
        target = str(getattr(args, "target", "artifact")).strip().lower()
        detail = f"Opened target: {target}" if rc == 0 else f"Failed to open target: {target}"
        next_action = "열린 원본/산출물을 확인한 뒤 Results 또는 문서 연결 작업으로 이어가십시오."
    return OperatorResult(
        command_id=command_id,
        title=title,
        status="PASS" if rc == 0 else "FAIL",
        detail=detail,
        next_action=next_action,
        rc=rc,
        artifacts=artifacts,
        insight={"stage": "Artifacts", "bottleneck": detail, "next_action": next_action},
        context={"run_id": _run_id_from_args(args)},
    )


def build_operator_result(args: argparse.Namespace, rc: int) -> OperatorResult | None:
    command_id = getattr(args, "operator_command_id", "")
    if not command_id:
        return None
    title = _title_for_command(command_id)
    if command_id == "inspect.environment_doctor":
        return _doctor_result(command_id, title, rc)
    if command_id in {"verify.quick_verify", "verify.run_readiness_status"}:
        return _readiness_result(command_id, title, rc, args)
    if command_id in {"verify.precheck_batch", "verify.batch"}:
        return _batch_result(command_id, title, rc, args)
    if command_id == "verify.all_gates":
        return _gate_all_result(command_id, title, rc)
    if command_id == "operate.scenario_trigger":
        return _scenario_result(command_id, title, rc, args)
    if command_id == "package.validate_contract":
        return _release_contract_result(command_id, title, rc)
    if command_id == "verify.surface_bundle":
        return _surface_bundle_result(command_id, title, rc, args)
    if command_id.startswith("artifact."):
        return _artifact_result(command_id, title, rc, args)
    return _generic_result(command_id, title, rc, args)


def write_last_operator_result(result: OperatorResult) -> None:
    LAST_OPERATOR_RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAST_OPERATOR_RESULT_PATH.write_text(
        json.dumps(asdict(result), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def clear_last_operator_result() -> None:
    try:
        LAST_OPERATOR_RESULT_PATH.unlink(missing_ok=True)
    except Exception:
        pass

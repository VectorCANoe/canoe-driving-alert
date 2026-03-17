from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from cliops.common import ROOT
from cliops.package_ops import cmd_package_clean


LAYOUT_PATH = ROOT / "product" / "sdv_operator" / "config" / "verification_artifact_layout.json"


def _load_layout() -> dict:
    return json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _phase_dirs(run_dir: Path) -> list[Path]:
    return [candidate for candidate in (run_dir / "pre", run_dir / "post", run_dir / "full") if candidate.exists()]


def _latest_archive_dir(archive_root: Path) -> Path | None:
    candidates: list[Path] = []
    if not archive_root.exists():
        return None
    for run_dir in archive_root.iterdir():
        if not run_dir.is_dir():
            continue
        candidates.extend(_phase_dirs(run_dir))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item.stat().st_mtime)


def _resolve_archive_dir(layout: dict, run_id: str, phase: str, latest: bool) -> Path:
    archive_root = ROOT / layout["root"]
    if run_id:
        run_dir = archive_root / run_id
        if phase:
            return run_dir / phase
        phase_candidates = _phase_dirs(run_dir)
        if phase_candidates:
            return max(phase_candidates, key=lambda item: item.stat().st_mtime)
        return run_dir
    if latest:
        latest_dir = _latest_archive_dir(archive_root)
        if latest_dir is None:
            raise SystemExit("[ARTIFACT] no archive runs found")
        return latest_dir
    raise SystemExit("[ARTIFACT] archive operations require --run-id or --latest")


def _staging_entries(layout: dict, run_id: str) -> list[Path]:
    staging_root = ROOT / layout["staging_root"]
    evidence_root = ROOT / layout["evidence_root"]
    incoming_root = ROOT / layout.get("incoming_root", "canoe/logging/evidence/incoming")
    entries = [
        staging_root,
        staging_root / "doctor_report.json",
        staging_root / "run_readiness.json",
        staging_root / "dev2_batch_report.json",
        staging_root / "dev2_batch_report.junit.xml",
        staging_root / "run_insight_report.json",
        staging_root / "run_insight_report.md",
        staging_root / "doc_binding_bundle.json",
        staging_root / "doc_binding_bundle.md",
        staging_root / "doc_fill_template.csv",
        staging_root / "doc_fill_template.md",
        staging_root / "surface_evidence_bundle.json",
        staging_root / "surface",
        incoming_root,
    ]
    for tier in ("UT", "IT", "ST", "FULL"):
        entries.extend(
            [
                incoming_root / tier / "raw_write_window.txt",
                incoming_root / tier / "trace",
                incoming_root / tier / "logging",
            ]
        )
    if run_id:
        for tier in ("UT", "IT", "ST", "FULL"):
            entries.append(evidence_root / tier / run_id)
    return entries


def _source_entries(layout: dict) -> list[Path]:
    return [
        LAYOUT_PATH,
        ROOT / "product" / "sdv_operator" / "manifest.json",
        ROOT / "product" / "sdv_operator" / "config" / "surface_ecu_inventory.json",
        ROOT / "product" / "sdv_operator" / "config" / "verification_pack_matrix.json",
        ROOT / "product" / "sdv_operator" / "config" / "campaign_profiles.json",
        ROOT / "product" / "sdv_operator" / "config" / "capability_boundary_matrix.json",
        ROOT / "product" / "sdv_operator" / "config" / "surface_traceability_profile.json",
        ROOT / "product" / "sdv_operator" / "config" / "verification_phase_policy.json",
        ROOT / "product" / "sdv_operator" / "docs-src" / "commands.md",
        ROOT / "product" / "sdv_operator" / "docs-src" / "ci-bridge.md",
        ROOT / "product" / "sdv_operator" / "docs-src" / "results.md",
        ROOT / "product" / "sdv_operator" / "docs-src" / "maintenance.md",
        ROOT / "product" / "sdv_operator" / "docs-src" / "packaging.md",
        ROOT / "product" / "sdv_operator" / "docs-src" / "role-boundary.md",
        ROOT / "product" / "sdv_operator" / "docs-src" / "capability-boundary.md",
        ROOT / "driving-alert-workproducts" / "05_Unit_Test.md",
        ROOT / "driving-alert-workproducts" / "06_Integration_Test.md",
        ROOT / "driving-alert-workproducts" / "07_System_Test.md",
        ROOT / "canoe" / "tests" / "modules" / "test_units" / "README.md",
        ROOT / "canoe" / "tests" / "modules" / "test_suites" / "README.md",
        ROOT / "canoe" / "docs" / "verification" / "test-asset-mapping.md",
        ROOT / "canoe" / "docs" / "verification" / "execution-guide.md",
    ]


def _build_entries() -> list[Path]:
    return [
        ROOT / "dist",
        ROOT / "build",
        ROOT / "product" / "sdv_operator" / "site",
    ]


def _archive_entries(layout: dict, run_id: str, phase: str, latest: bool) -> list[Path]:
    archive_dir = _resolve_archive_dir(layout, run_id, phase, latest)
    entries = [
        archive_dir,
        archive_dir / "reports",
        archive_dir / "surface",
        archive_dir / "native_reports",
        archive_dir / "evidence",
        archive_dir / "manifests" / "artifact_manifest.json",
        archive_dir / "manifests" / "execution_manifest.json",
    ]
    for tier in layout.get("archived_tiers", ["UT", "IT", "ST", "FULL"]):
        entries.extend(
            [
                archive_dir / "evidence" / tier,
                archive_dir / "evidence" / tier / "supplementary" / "trace",
                archive_dir / "evidence" / tier / "supplementary" / "logging",
            ]
        )
    return entries


def _first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def _print_entries(title: str, entries: list[Path], json_mode: bool) -> int:
    payload = []
    for entry in entries:
        payload.append(
            {
                "path": _rel(entry),
                "exists": entry.exists(),
                "type": "dir" if entry.is_dir() else "file",
            }
        )
    if json_mode:
        print(json.dumps({"title": title, "items": payload}, indent=2, ensure_ascii=False))
    else:
        print(f"[ARTIFACT] {title}")
        for item in payload:
            status = "OK" if item["exists"] else "MISSING"
            print(f"- [{status}] {item['path']}")
    return 0


def _open_path(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    if os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
        return
    subprocess.run(["xdg-open", str(path)], check=False)


def _resolve_open_target(layout: dict, target: str, run_id: str, phase: str, latest: bool) -> Path:
    staging_root = ROOT / layout["staging_root"]
    incoming_root = ROOT / layout.get("incoming_root", "canoe/logging/evidence/incoming")
    if target == "staging-root":
        return staging_root
    if target == "incoming-root":
        return incoming_root
    if target == "incoming-trace-root":
        return incoming_root / "UT" / "trace"
    if target == "incoming-logging-root":
        return incoming_root / "UT" / "logging"
    if target == "batch-report":
        return staging_root / "dev2_batch_report.md"
    if target == "run-insight":
        return staging_root / "run_insight_report.md"
    if target == "doc-binding-bundle":
        return staging_root / "doc_binding_bundle.md"
    if target == "doc-fill-template":
        return staging_root / "doc_fill_template.md"
    if target == "surface-bundle":
        return staging_root / "surface_evidence_bundle.md"
    if target == "readiness":
        return staging_root / "run_readiness.md"
    if target == "doctor":
        return staging_root / "doctor_report.md"
    if target == "surface-inventory":
        return ROOT / "product" / "sdv_operator" / "config" / "surface_ecu_inventory.json"
    if target == "unit-test-doc":
        return ROOT / "driving-alert-workproducts" / "05_Unit_Test.md"
    if target == "integration-test-doc":
        return ROOT / "driving-alert-workproducts" / "06_Integration_Test.md"
    if target == "system-test-doc":
        return ROOT / "driving-alert-workproducts" / "07_System_Test.md"
    if target in {"test-asset-mapping", "native-test-portfolio"}:
        return ROOT / "canoe" / "docs" / "verification" / "test-asset-mapping.md"
    if target in {"active-test-units-guide", "native-testcase-blueprints"}:
        return ROOT / "canoe" / "tests" / "modules" / "test_units" / "README.md"
    if target in {"active-test-suites-guide", "network-gateway-pack"}:
        return ROOT / "canoe" / "tests" / "modules" / "test_suites" / "README.md"
    if target == "execution-guide":
        return ROOT / "canoe" / "docs" / "verification" / "execution-guide.md"
    if target == "verification-pack-matrix":
        return ROOT / "product" / "sdv_operator" / "config" / "verification_pack_matrix.json"
    if target == "campaign-profiles":
        return ROOT / "product" / "sdv_operator" / "config" / "campaign_profiles.json"
    if target == "capability-matrix-json":
        return ROOT / "product" / "sdv_operator" / "config" / "capability_boundary_matrix.json"
    if target == "traceability-profile":
        return ROOT / "product" / "sdv_operator" / "config" / "surface_traceability_profile.json"
    if target == "artifact-layout":
        return LAYOUT_PATH
    if target == "phase-policy":
        return ROOT / "product" / "sdv_operator" / "config" / "verification_phase_policy.json"
    if target == "manifest":
        return ROOT / "product" / "sdv_operator" / "manifest.json"
    if target == "commands-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "commands.md"
    if target == "results-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "results.md"
    if target == "maintenance-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "maintenance.md"
    if target == "packaging-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "packaging.md"
    if target == "ci-bridge-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "ci-bridge.md"
    if target == "role-boundary-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "role-boundary.md"
    if target == "capability-matrix-doc":
        return ROOT / "product" / "sdv_operator" / "docs-src" / "capability-boundary.md"
    if target == "jenkinsfile-sample":
        return ROOT / "product" / "sdv_operator" / "examples" / "Jenkinsfile.verify"
    if target == "build-root":
        return ROOT / "dist"

    archive_dir = _resolve_archive_dir(layout, run_id, phase, latest)
    if target == "archive-run":
        return archive_dir
    if target == "execution-manifest":
        return archive_dir / "manifests" / "execution_manifest.json"
    if target == "evidence-dir":
        return archive_dir / "evidence"
    if target == "native-reports":
        return archive_dir / "native_reports"
    if target == "surface-dir":
        return archive_dir / "surface"
    if target == "reports-dir":
        return archive_dir / "reports"
    if target == "supplementary-trace":
        return _first_existing(
            [(archive_dir / "evidence" / tier / "supplementary" / "trace") for tier in layout.get("archived_tiers", ["UT", "IT", "ST", "FULL"])]
        )
    if target == "supplementary-logging":
        return _first_existing(
            [(archive_dir / "evidence" / tier / "supplementary" / "logging") for tier in layout.get("archived_tiers", ["UT", "IT", "ST", "FULL"])]
        )
    raise SystemExit(f"[ARTIFACT] unsupported target: {target}")


def cmd_artifact_list(args: argparse.Namespace) -> int:
    layout = _load_layout()
    if args.scope == "staging":
        return _print_entries("staging outputs", _staging_entries(layout, args.run_id), args.json)
    if args.scope == "source":
        return _print_entries("source contracts", _source_entries(layout), args.json)
    if args.scope == "build":
        return _print_entries("build outputs", _build_entries(), args.json)
    return _print_entries("archive outputs", _archive_entries(layout, args.run_id, args.phase, args.latest), args.json)


def cmd_artifact_open(args: argparse.Namespace) -> int:
    layout = _load_layout()
    path = _resolve_open_target(layout, args.target, args.run_id, args.phase, args.latest)
    print(f"[ARTIFACT] target={_rel(path)}")
    if args.print_only:
        return 0
    _open_path(path)
    return 0


def cmd_artifact_clean(args: argparse.Namespace) -> int:
    return cmd_package_clean(args)

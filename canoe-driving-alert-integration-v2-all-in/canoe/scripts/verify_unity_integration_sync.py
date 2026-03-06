#!/usr/bin/env python3
"""
Verify SDV Unity integration sync results.

Checks for each Unity project:
- Required bridge scripts under Assets/Scripts/SdvBridge
- Required skin files under Assets/Resources/Skins/unity_skin_pack_v1
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


REQUIRED_SCRIPTS = [
    "UdpUiRenderReceiver.cs",
    "UiRenderVisualMap.cs",
    "ExternalRoadViewController.cs",
    "CabinPanoramaViewController.cs",
    "SdvSceneAutoBinder.cs",
    "UiRenderStatusOverlay.cs",
    "QuickPrototypeSceneBuilder.cs",
    "SdvSkinRuntimeLoader.cs",
]

REQUIRED_SKIN_FILES = [
    "external/background/map_base.png",
    "external/icons/map_icon.svg",
    "external/icons/vehicle_icon.svg",
    "external/markers/car_marker.png",
    "external/background/map_sf.png",
    "external/background/map_yos.png",
    "external/road/road_2lane_dark02.png",
    "external/road/road_2lane_dark02_n.png",
    "external/icons/warning_alert.png",
    "external/icons/road_flow.svg",
    "cabin/cluster/cluster_bg_xj.png",
    "cabin/cluster/cluster_needle_mph.png",
    "cabin/speedometer/background.png",
    "cabin/speedometer/background.svg",
    "cabin/speedometer/needle.svg",
    "cabin/icons/car.png",
    "cabin/icons/dashboard.svg",
    "cabin/icons/speedometer.svg",
    "cabin/ambient/zone_background.png",
    "cabin/ambient/zone_top.png",
    "cabin/ambient/zone_middle.png",
    "cabin/ambient/zone_bottom.png",
    "manifest.json",
    "manifest.md",
]


@dataclass
class ProjectResult:
    project: Path
    script_missing: List[str]
    skin_missing: List[str]

    @property
    def is_pass(self) -> bool:
        return not self.script_missing and not self.skin_missing


def is_unity_project(path: Path) -> bool:
    return (path / "Assets").is_dir() and (path / "ProjectSettings" / "ProjectVersion.txt").is_file()


def discover_unity_projects(repo_root: Path) -> List[Path]:
    projects: List[Path] = []
    for settings_dir in repo_root.rglob("ProjectSettings"):
        root = settings_dir.parent
        if is_unity_project(root):
            projects.append(root.resolve())
    return sorted({p for p in projects}, key=lambda p: str(p))


def verify_project(project: Path) -> ProjectResult:
    scripts_root = project / "Assets" / "Scripts" / "SdvBridge"
    skin_root = project / "Assets" / "Resources" / "Skins" / "unity_skin_pack_v1"

    script_missing = [name for name in REQUIRED_SCRIPTS if not (scripts_root / name).exists()]
    skin_missing = [name for name in REQUIRED_SKIN_FILES if not (skin_root / name).exists()]
    return ProjectResult(project=project, script_missing=script_missing, skin_missing=skin_missing)


def write_report(path: Path, results: List[ProjectResult], repo_root: Path) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.is_pass)
    failed = total - passed

    lines: List[str] = [
        "# Unity Sync Verification Report",
        "",
        f"- total_projects: {total}",
        f"- passed: {passed}",
        f"- failed: {failed}",
        "",
    ]

    for r in results:
        rel_project = r.project.relative_to(repo_root).as_posix() if r.project.is_relative_to(repo_root) else str(r.project)
        status = "PASS" if r.is_pass else "FAIL"
        lines.append(f"## {rel_project} [{status}]")
        if r.script_missing:
            lines.append("- missing_scripts:")
            for item in r.script_missing:
                lines.append(f"  - {item}")
        if r.skin_missing:
            lines.append("- missing_skin_files:")
            for item in r.skin_missing:
                lines.append(f"  - {item}")
        if r.is_pass:
            lines.append("- all required files found")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify SDV Unity integration sync status")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Repository root path",
    )
    parser.add_argument(
        "--target-project",
        action="append",
        default=[],
        help="Unity project root path (can be repeated)",
    )
    parser.add_argument(
        "--auto-detect",
        action="store_true",
        help="Auto detect Unity projects under repo root",
    )
    parser.add_argument(
        "--write-report",
        default="canoe/docs/operations/UNITY_SYNC_VERIFICATION.md",
        help="Markdown report output path relative to repo root",
    )
    return parser.parse_args()


def resolve_targets(repo_root: Path, args: argparse.Namespace) -> List[Path]:
    targets: List[Path] = []
    if args.auto_detect:
        targets.extend(discover_unity_projects(repo_root))
    for raw in args.target_project:
        p = Path(raw).resolve()
        if p not in targets:
            targets.append(p)
    return targets


def run() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    targets = resolve_targets(repo_root, args)
    if not targets:
        raise RuntimeError("No target project. Use --auto-detect or --target-project.")

    results: List[ProjectResult] = []
    for p in targets:
        if not is_unity_project(p):
            print(f"[VERIFY] skip (not unity root): {p}")
            continue
        result = verify_project(p)
        results.append(result)
        status = "PASS" if result.is_pass else "FAIL"
        print(
            f"[VERIFY] {status} project={p} "
            f"missing_scripts={len(result.script_missing)} missing_skin={len(result.skin_missing)}"
        )

    if not results:
        raise RuntimeError("No Unity project verified.")

    report_path = (repo_root / args.write_report).resolve()
    write_report(report_path, results, repo_root)
    print(f"[VERIFY] report={report_path}")

    failed = [r for r in results if not r.is_pass]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run())

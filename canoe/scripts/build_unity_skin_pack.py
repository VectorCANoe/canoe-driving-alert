#!/usr/bin/env python3
"""
Build Unity skin pack from curated OSS panel references.

Output is written under ignored folder:
  canoe/reference/oss_panels/_exports/unity_skin_pack_v1
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class AssetSpec:
    category: str
    key: str
    source_repo: str
    source_relpath: str
    dest_relpath: str
    note: str


ASSET_SPECS: List[AssetSpec] = [
    # External road view
    AssetSpec(
        category="external",
        key="ext_map_background_png",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/navit/qml/map.png",
        dest_relpath="external/background/map_base.png",
        note="Map texture base",
    ),
    AssetSpec(
        category="external",
        key="ext_map_icon_svg",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/navit/qml/icons/appbar.map.svg",
        dest_relpath="external/icons/map_icon.svg",
        note="Map icon vector",
    ),
    AssetSpec(
        category="external",
        key="ext_vehicle_icon_svg",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/navit/qml/icons/appbar.transit.car.svg",
        dest_relpath="external/icons/vehicle_icon.svg",
        note="Vehicle icon vector",
    ),
    AssetSpec(
        category="external",
        key="ext_car_marker_png",
        source_repo="genivi_vehicle_sim_ref",
        source_relpath="Assets/Textures/DriveScenes/Admin/maps/carPos-01.png",
        dest_relpath="external/markers/car_marker.png",
        note="Road position marker",
    ),
    AssetSpec(
        category="external",
        key="ext_map_sf_png",
        source_repo="genivi_vehicle_sim_ref",
        source_relpath="Assets/StreamingAssets/Admin/images/MapSF.png",
        dest_relpath="external/background/map_sf.png",
        note="External map variant",
    ),
    AssetSpec(
        category="external",
        key="ext_map_yos_png",
        source_repo="genivi_vehicle_sim_ref",
        source_relpath="Assets/StreamingAssets/Admin/images/MapYos.png",
        dest_relpath="external/background/map_yos.png",
        note="External map variant",
    ),
    AssetSpec(
        category="external",
        key="ext_road_texture_png",
        source_repo="coupled_sim_unity_ref",
        source_relpath="Assets/KajamansRoads/Textures/Road_2lane_dark02.png",
        dest_relpath="external/road/road_2lane_dark02.png",
        note="Road surface texture",
    ),
    AssetSpec(
        category="external",
        key="ext_road_texture_n_png",
        source_repo="coupled_sim_unity_ref",
        source_relpath="Assets/KajamansRoads/Textures/Road_2lane_dark02_n.png",
        dest_relpath="external/road/road_2lane_dark02_n.png",
        note="Road normal map",
    ),
    AssetSpec(
        category="external",
        key="ext_warning_icon_png",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/hvac/icons/alert.png",
        dest_relpath="external/icons/warning_alert.png",
        note="Warning indicator",
    ),
    AssetSpec(
        category="external",
        key="ext_flow_road_icon_svg",
        source_repo="coupled_sim_unity_ref",
        source_relpath="Assets/Barmetler/RoadSystem/Resources/Icons/Road.svg",
        dest_relpath="external/icons/road_flow.svg",
        note="Flow/road icon",
    ),
    # Cabin view
    AssetSpec(
        category="cabin",
        key="cabin_cluster_bg_png",
        source_repo="genivi_vehicle_sim_ref",
        source_relpath="Assets/Textures/Consoles/1280x720/XJClusterBackground.png",
        dest_relpath="cabin/cluster/cluster_bg_xj.png",
        note="Cluster background",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_cluster_needle_png",
        source_repo="genivi_vehicle_sim_ref",
        source_relpath="Assets/Textures/Consoles/1280x720/XJClusterMPHNeedle.png",
        dest_relpath="cabin/cluster/cluster_needle_mph.png",
        note="Cluster needle",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_background_png",
        source_repo="car_speedometer_ref",
        source_relpath="img/background.png",
        dest_relpath="cabin/speedometer/background.png",
        note="Speedometer background raster",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_background_svg",
        source_repo="car_speedometer_ref",
        source_relpath="img/background.svg",
        dest_relpath="cabin/speedometer/background.svg",
        note="Speedometer background vector",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_needle_svg",
        source_repo="car_speedometer_ref",
        source_relpath="img/needle.svg",
        dest_relpath="cabin/speedometer/needle.svg",
        note="Needle vector master",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_car_png",
        source_repo="car_hmi_dashboard_ui_ref",
        source_relpath="assets/car.png",
        dest_relpath="cabin/icons/car.png",
        note="Cabin car icon",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_dashboard_svg",
        source_repo="car_hmi_dashboard_ui_ref",
        source_relpath="assets/Dashboard.svg",
        dest_relpath="cabin/icons/dashboard.svg",
        note="Cabin dashboard vector",
    ),
    AssetSpec(
        category="cabin",
        key="cabin_speedometer_svg",
        source_repo="car_hmi_dashboard_ui_ref",
        source_relpath="assets/speedometer.svg",
        dest_relpath="cabin/icons/speedometer.svg",
        note="Cabin speedometer vector",
    ),
    AssetSpec(
        category="cabin",
        key="ambient_zone_bg_png",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/hvac/icons/zone-background.png",
        dest_relpath="cabin/ambient/zone_background.png",
        note="Ambient zone base",
    ),
    AssetSpec(
        category="cabin",
        key="ambient_zone_top_png",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/hvac/icons/zone-top.png",
        dest_relpath="cabin/ambient/zone_top.png",
        note="Ambient zone top strip",
    ),
    AssetSpec(
        category="cabin",
        key="ambient_zone_middle_png",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/hvac/icons/zone-middle.png",
        dest_relpath="cabin/ambient/zone_middle.png",
        note="Ambient zone middle strip",
    ),
    AssetSpec(
        category="cabin",
        key="ambient_zone_bottom_png",
        source_repo="headunit_desktop_ref",
        source_relpath="modules/hvac/icons/zone-bottom.png",
        dest_relpath="cabin/ambient/zone_bottom.png",
        note="Ambient zone bottom strip",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Unity skin pack from oss panel references")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Repository root path",
    )
    parser.add_argument(
        "--output-dir",
        default="canoe/reference/oss_panels/_exports/unity_skin_pack_v1",
        help="Output directory relative to repo root",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete output directory before generation",
    )
    return parser.parse_args()


def copy_asset(repo_root: Path, output_root: Path, spec: AssetSpec) -> Dict[str, str]:
    src = repo_root / "canoe" / "reference" / "oss_panels" / spec.source_repo / spec.source_relpath
    dst = output_root / spec.dest_relpath
    dst.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        return {
            "key": spec.key,
            "status": "missing",
            "source": os.path.relpath(src, repo_root).replace("\\", "/"),
            "dest": os.path.relpath(dst, repo_root).replace("\\", "/"),
            "note": spec.note,
        }

    shutil.copy2(src, dst)
    return {
        "key": spec.key,
        "status": "copied",
        "source": os.path.relpath(src, repo_root).replace("\\", "/"),
        "dest": os.path.relpath(dst, repo_root).replace("\\", "/"),
        "note": spec.note,
    }


def write_manifest(output_root: Path, results: List[Dict[str, str]]) -> None:
    manifest = {
        "name": "unity_skin_pack_v1",
        "summary": {
            "total": len(results),
            "copied": sum(1 for r in results if r["status"] == "copied"),
            "missing": sum(1 for r in results if r["status"] == "missing"),
        },
        "items": results,
    }

    (output_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    lines: List[str] = [
        "# unity_skin_pack_v1",
        "",
        f"- total: {manifest['summary']['total']}",
        f"- copied: {manifest['summary']['copied']}",
        f"- missing: {manifest['summary']['missing']}",
        "",
        "## Items",
    ]
    for item in results:
        lines.append(
            f"- {item['key']}: {item['status']} "
            f"(src=`{item['source']}`, dst=`{item['dest']}`)"
        )
    (output_root / "manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    output_root = (repo_root / args.output_dir).resolve()

    if args.clean and output_root.exists():
        shutil.rmtree(output_root)

    output_root.mkdir(parents=True, exist_ok=True)

    results: List[Dict[str, str]] = []
    for spec in ASSET_SPECS:
        results.append(copy_asset(repo_root, output_root, spec))

    write_manifest(output_root, results)

    copied = sum(1 for r in results if r["status"] == "copied")
    missing = sum(1 for r in results if r["status"] == "missing")
    print(f"[SKIN_PACK] done output={output_root}")
    print(f"[SKIN_PACK] copied={copied} missing={missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

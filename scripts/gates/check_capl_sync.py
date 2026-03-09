#!/usr/bin/env python3
"""Check 1:1 sync between src/capl and cfg/channel_assign CAPL files."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "canoe" / "src" / "capl"
CFG_ROOT = REPO_ROOT / "canoe" / "cfg" / "channel_assign"

EXPECTED_CFG_DOMAIN = {
    # ADAS
    "ADAS_WARN_CTRL.can": "ADAS",
    "WARN_ARB_MGR.can": "ADAS",
    # ETH Backbone
    "DOMAIN_BOUNDARY_MGR.can": "ETH_Backbone",
    "EMS_ALERT_RX.can": "ETH_Backbone",
    "EMS_AMB_TX.can": "ETH_Backbone",
    "EMS_POLICE_TX.can": "ETH_Backbone",
    "ETH_SW.can": "ETH_Backbone",
    "NAV_CTX_MGR.can": "ETH_Backbone",
    "VAL_SCENARIO_CTRL.can": "ETH_Backbone",
    # Infotainment
    "CLU_BASE_CTRL.can": "Infotainment",
    "CLU_HMI_CTRL.can": "Infotainment",
    "INFOTAINMENT_GW.can": "Infotainment",
    "IVI_GW.can": "Infotainment",
    # Body
    "AMBIENT_CTRL.can": "Body",
    "BODY_GW.can": "Body",
    "DRV_STATE_MGR.can": "Body",
    "HAZARD_CTRL.can": "Body",
    "WINDOW_CTRL.can": "Body",
    # Powertrain
    "DOMAIN_ROUTER.can": "Powertrain",
    "ENG_CTRL.can": "Powertrain",
    "TCM.can": "Powertrain",
    # Chassis
    "ACCEL_CTRL.can": "Chassis",
    "BRK_CTRL.can": "Chassis",
    "CHS_GW.can": "Chassis",
    "STEER_CTRL.can": "Chassis",
    "VAL_BASELINE_CTRL.can": "Chassis",
}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_can_files(root: Path, exclude_legacy: bool = False) -> dict[str, Path]:
    files = {}
    duplicates = []
    for p in root.rglob("*.can"):
        if exclude_legacy and "v1_legacy" in p.parts:
            continue
        key = p.name
        if key in files:
            duplicates.append(key)
        else:
            files[key] = p

    if duplicates:
        print("[FAIL] Duplicate *.can file names detected:")
        for name in sorted(set(duplicates)):
            print(f"  - {name}")
        sys.exit(2)

    return files


def main() -> int:
    src_map = collect_can_files(SRC_ROOT, exclude_legacy=True)
    cfg_map = collect_can_files(CFG_ROOT, exclude_legacy=False)

    src_names = set(src_map.keys())
    cfg_names = set(cfg_map.keys())

    only_src = sorted(src_names - cfg_names)
    only_cfg = sorted(cfg_names - src_names)

    common = sorted(src_names & cfg_names)
    content_diff = []
    for name in common:
        if file_hash(src_map[name]) != file_hash(cfg_map[name]):
            content_diff.append(name)

    unmapped_nodes = sorted(name for name in common if name not in EXPECTED_CFG_DOMAIN)
    domain_mismatch = []
    for name in common:
        expected_domain = EXPECTED_CFG_DOMAIN.get(name)
        if not expected_domain:
            continue
        actual_domain = cfg_map[name].parent.name
        if actual_domain != expected_domain:
            domain_mismatch.append(f"{name}({actual_domain}->{expected_domain})")

    print(
        "[CAPL_SYNC] "
        f"src={len(src_map)} cfg={len(cfg_map)} "
        f"common={len(common)} only_src={len(only_src)} "
        f"only_cfg={len(only_cfg)} content_diff={len(content_diff)} "
        f"domain_diff={len(domain_mismatch)} unmapped={len(unmapped_nodes)}"
    )

    if only_src or only_cfg or content_diff or domain_mismatch or unmapped_nodes:
        if only_src:
            print("[ONLY_SRC]", ", ".join(only_src))
        if only_cfg:
            print("[ONLY_CFG]", ", ".join(only_cfg))
        if content_diff:
            print("[CONTENT_DIFF]", ", ".join(content_diff))
        if domain_mismatch:
            print("[DOMAIN_MISMATCH]", ", ".join(domain_mismatch))
        if unmapped_nodes:
            print("[UNMAPPED_NODES]", ", ".join(unmapped_nodes))
        return 2

    print("[PASS] src/capl and cfg/channel_assign are fully synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

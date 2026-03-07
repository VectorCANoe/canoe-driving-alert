#!/usr/bin/env python3
"""Multi-bus CFG + DBC domain policy gate.

Purpose
- Enforce single-node multi-bus assignment for key gateway/harness nodes.
- Enforce domain-centric DBC ownership and prevent cross-domain duplication.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CFG_PATH = ROOT / "canoe" / "cfg" / "CAN_v2_topology_wip.cfg"
DBC_ROOT = ROOT / "canoe" / "databases"

ACTIVE_DBC_FILES = [
    "chassis_can.dbc",
    "body_can.dbc",
    "infotainment_can.dbc",
    "powertrain_can.dbc",
    "adas_can.dbc",
    "eth_backbone_can_stub.dbc",
]

PRIMARY_NODE_FOR_BUS = {
    "ETH_BACKBONE": "DOMAIN_BOUNDARY_MGR",
    "INFOTAINMENT": "INFOTAINMENT_GW",
    "BODY": "BODY_GW",
    "POWERTRAIN": "DOMAIN_ROUTER",
    "CHASSIS": "CHS_GW",
    "ADAS": "ADAS_WARN_CTRL",
}

MULTIBUS_EXPECTED = {
    "DOMAIN_BOUNDARY_MGR": {"ETH_BACKBONE", "INFOTAINMENT", "BODY", "CHASSIS"},
    "VAL_SCENARIO_CTRL": {"ETH_BACKBONE", "INFOTAINMENT", "POWERTRAIN", "CHASSIS", "ADAS"},
}

REQUIRED_OWNER = {
    "ethEmergencyRiskMsg": "adas_can.dbc",
    "ethDecelAssistReqMsg": "adas_can.dbc",
    "ethSelectedAlertMsg": "adas_can.dbc",
    "ethObjectRiskInputMsg": "adas_can.dbc",
    "ethObjectRiskStateMsg": "adas_can.dbc",
    "ethObjectScenarioAlertMsg": "adas_can.dbc",
    "ethFailSafeStateMsg": "eth_backbone_can_stub.dbc",
    "ethObjectSafetyStateMsg": "eth_backbone_can_stub.dbc",
    "ethVehicleStateMsg": "eth_backbone_can_stub.dbc",
    "ethSteeringMsg": "eth_backbone_can_stub.dbc",
    "ethNavContextMsg": "eth_backbone_can_stub.dbc",
}


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp949", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def parse_cfg_node_buses(cfg_text: str) -> tuple[dict[str, set[int]], dict[str, int], list[str]]:
    lines = cfg_text.splitlines()
    path_pat = re.compile(r'channel_assign\\[^\\]+\\([A-Za-z0-9_]+)\.can')

    node_buses: dict[str, set[int]] = {}
    node_occurrence: dict[str, int] = defaultdict(int)
    parse_issues: list[str] = []

    for i, line in enumerate(lines):
        m = path_pat.search(line)
        if not m:
            continue
        node = m.group(1)
        node_occurrence[node] += 1

        eof_idx = -1
        search_end = min(i + 180, len(lines))
        for j in range(i, search_end):
            if lines[j].strip() == "EOF_MBSSDATA":
                eof_idx = j
                break
        if eof_idx < 0:
            parse_issues.append(f"{node}: EOF_MBSSDATA not found near cfg path line {i+1}")
            continue

        try:
            count = int(lines[eof_idx + 1].strip())
        except (ValueError, IndexError):
            parse_issues.append(f"{node}: invalid MBSSDATA count near line {eof_idx+2}")
            continue

        buses: set[int] = set()
        for k in range(count):
            row_idx = eof_idx + 2 + k
            if row_idx >= len(lines):
                parse_issues.append(f"{node}: MBSSDATA row out of range near line {row_idx+1}")
                break
            ints = re.findall(r"-?\d+", lines[row_idx])
            if not ints:
                parse_issues.append(f"{node}: MBSSDATA row has no bus id near line {row_idx+1}")
                continue
            buses.add(int(ints[0]))

        # Keep first occurrence as canonical and report duplicates separately.
        node_buses.setdefault(node, buses)

    return node_buses, node_occurrence, parse_issues


def parse_dbc_messages(path: Path) -> dict[str, int]:
    out: dict[str, int] = {}
    text = read_text(path)
    for m in re.finditer(r"^BO_\s+(\d+)\s+([A-Za-z0-9_]+)\s*:", text, flags=re.M):
        msg_id = int(m.group(1))
        msg_name = m.group(2)
        out[msg_name] = msg_id
    return out


def main() -> int:
    fail_issues: list[str] = []
    warn_issues: list[str] = []

    if not CFG_PATH.exists():
        print(f"[FAIL] Missing cfg: {CFG_PATH}")
        return 2

    cfg_text = read_text(CFG_PATH)
    node_buses, node_occurrence, parse_issues = parse_cfg_node_buses(cfg_text)
    if parse_issues:
        fail_issues.extend(parse_issues[:20])

    # Duplicate node entries in cfg are not allowed for target nodes.
    for node in MULTIBUS_EXPECTED:
        occ = node_occurrence.get(node, 0)
        if occ > 1:
            fail_issues.append(f"{node}: duplicate node entries in cfg ({occ})")
        elif occ == 0:
            fail_issues.append(f"{node}: missing node entry in cfg")

    # Infer bus-id map from canonical single-bus nodes.
    bus_id_by_role: dict[str, int] = {}
    for role, node in PRIMARY_NODE_FOR_BUS.items():
        buses = node_buses.get(node)
        if not buses:
            fail_issues.append(f"{node}: cannot infer bus id ({role})")
            continue
        if len(buses) != 1:
            fail_issues.append(f"{node}: expected single-bus anchor, found {sorted(buses)}")
            continue
        bus_id_by_role[role] = next(iter(buses))

    # Validate multi-bus expectations for target nodes.
    for node, roles in MULTIBUS_EXPECTED.items():
        actual = node_buses.get(node, set())
        expected: set[int] = set()
        unresolved_roles = []
        for role in roles:
            if role not in bus_id_by_role:
                unresolved_roles.append(role)
            else:
                expected.add(bus_id_by_role[role])
        if unresolved_roles:
            fail_issues.append(f"{node}: unresolved bus roles {', '.join(sorted(unresolved_roles))}")
            continue
        missing = sorted(expected - actual)
        if missing:
            fail_issues.append(
                f"{node}: missing bus assignments {missing} (actual={sorted(actual)}, expected={sorted(expected)})"
            )
        extra = sorted(actual - expected)
        if extra:
            warn_issues.append(f"{node}: extra bus assignments {extra} (expected={sorted(expected)})")

    # Parse active DBCs.
    missing_dbc = [name for name in ACTIVE_DBC_FILES if not (DBC_ROOT / name).exists()]
    if missing_dbc:
        fail_issues.append(f"Missing active DBC files: {', '.join(missing_dbc)}")

    messages_by_file: dict[str, dict[str, int]] = {}
    name_index: dict[str, set[str]] = defaultdict(set)
    id_index: dict[int, set[str]] = defaultdict(set)

    for name in ACTIVE_DBC_FILES:
        path = DBC_ROOT / name
        if not path.exists():
            continue
        msg_map = parse_dbc_messages(path)
        messages_by_file[name] = msg_map
        for msg_name, msg_id in msg_map.items():
            name_index[msg_name].add(name)
            id_index[msg_id].add(name)

    # Domain policy: message name must exist in one active DBC only.
    dup_names = sorted([n for n, files in name_index.items() if len(files) > 1])
    if dup_names:
        sample = ", ".join([f"{n}({','.join(sorted(name_index[n]))})" for n in dup_names[:8]])
        fail_issues.append(f"Duplicate message names across DBCs: {sample}")

    # Domain policy: CAN IDs must not be duplicated across active DBCs.
    dup_ids = sorted([mid for mid, files in id_index.items() if len(files) > 1])
    if dup_ids:
        sample = ", ".join([f"0x{mid:X}({','.join(sorted(id_index[mid]))})" for mid in dup_ids[:8]])
        fail_issues.append(f"Duplicate CAN IDs across DBCs: {sample}")

    # Ownership checks for critical Ethernet/ADAS bridge messages.
    for msg_name, owner in REQUIRED_OWNER.items():
        files = name_index.get(msg_name, set())
        if not files:
            fail_issues.append(f"{msg_name}: missing from active DBCs (expected owner {owner})")
            continue
        if files != {owner}:
            fail_issues.append(
                f"{msg_name}: ownership mismatch (actual={','.join(sorted(files))}, expected={owner})"
            )

    # Emergency ingress alias must exist in eth backbone stub by one of accepted names.
    eth_stub_msgs = set(messages_by_file.get("eth_backbone_can_stub.dbc", {}).keys())
    if "frmEmergencyBroadcastMsg" not in eth_stub_msgs and "ETH_EmergencyAlert" not in eth_stub_msgs:
        fail_issues.append(
            "eth_backbone_can_stub.dbc: missing emergency ingress message (frmEmergencyBroadcastMsg or ETH_EmergencyAlert)"
        )

    print("[MULTIBUS_CFG_DBC] summary")
    print(f"  - cfg: {CFG_PATH.name}")
    print(f"  - active_dbc_files: {len(messages_by_file)}/{len(ACTIVE_DBC_FILES)}")
    print(f"  - cfg_nodes_parsed: {len(node_buses)}")
    print(f"  - fails: {len(fail_issues)}")
    print(f"  - warns: {len(warn_issues)}")

    if warn_issues:
        print("[WARN]")
        for row in warn_issues[:20]:
            print(f"  - {row}")

    if fail_issues:
        print("[FAIL]")
        for row in fail_issues[:30]:
            print(f"  - {row}")
        return 2

    print("[PASS] Multi-bus cfg and DBC domain policy checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


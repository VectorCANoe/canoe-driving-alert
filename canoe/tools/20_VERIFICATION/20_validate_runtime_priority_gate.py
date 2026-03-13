#!/usr/bin/env python3
"""Validate runtime priority communication contracts for CANoe project.

This script enforces a practical gate for the mentoring direction:
1) CAN SSoT must be split domain DBCs.
2) Ethernet SSoT must be a separate contract document.
3) Message ownership must be unambiguous across active CAN DBC set.
4) Volume target must stay above minimum visibility threshold.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Dict, List, Tuple


DBC_ACTIVE_FILES = [
    "chassis_can.dbc",
    "powertrain_can.dbc",
    "body_can.dbc",
    "infotainment_can.dbc",
    "adas_can.dbc",
]
ETH_CONTRACT_REL = "canoe/docs/contracts/10_ETHERNET_BACKBONE_SSoT.md"
DEFAULT_MATRIX_OUT = "canoe/tmp/runtime_message_ownership_matrix.md"
DEFAULT_REPORT_OUT = "canoe/tmp/runtime_priority_gate_report.md"

MANDATORY_MESSAGE_IDS: Dict[str, int] = {
    "frmVehicleStateCanMsg": 0x2A0,
    "frmSteeringCanMsg": 0x2A1,
    "frmPedalInputCanMsg": 0x2A2,
    "frmSteeringStateCanMsg": 0x100,
    "frmWheelSpeedMsg": 0x101,
    "frmYawAccelMsg": 0x102,
    "frmBrakeStatusMsg": 0x120,
    "frmAccelStatusMsg": 0x121,
    "frmSteeringTorqueMsg": 0x122,
    "frmChassisHealthMsg": 0x103,
    "frmNavContextCanMsg": 0x2A3,
    "frmAmbientControlMsg": 0x260,
    "frmHazardControlMsg": 0x261,
    "frmWindowControlMsg": 0x262,
    "frmDoorStateMsg": 0x264,
    "frmLampControlMsg": 0x265,
    "frmWiperStateMsg": 0x266,
    "frmSeatBeltStateMsg": 0x267,
    "frmCabinAirStateMsg": 0x268,
    "frmBodyHealthMsg": 0x269,
    "frmClusterWarningMsg": 0x280,
    "frmClusterBaseStateMsg": 0x281,
    "frmNaviGuideStateMsg": 0x282,
    "frmMediaStateMsg": 0x283,
    "frmCallStateMsg": 0x284,
    "frmNavigationRouteMsg": 0x285,
    "frmClusterThemeMsg": 0x286,
    "frmHmiPopupStateMsg": 0x287,
    "frmInfotainmentHealthMsg": 0x288,
    "frmIgnitionEngineMsg": 0x2A8,
    "frmGearStateMsg": 0x2A9,
    "frmPowertrainGatewayMsg": 0x109,
    "frmEngineSpeedTempMsg": 0x12A,
    "frmFuelBatteryStateMsg": 0x12B,
    "frmThrottleStateMsg": 0x12C,
    "frmTransmissionTempMsg": 0x12D,
    "frmVehicleModeMsg": 0x10A,
    "frmPowerLimitMsg": 0x10B,
    "frmCruiseStateMsg": 0x10C,
    "frmPowertrainHealthMsg": 0x10D,
}

MANDATORY_MESSAGES = set(MANDATORY_MESSAGE_IDS.keys())

MIN_MESSAGE_COUNT = 40

BO_RE = re.compile(r"^BO_\s+(\d+)\s+(\w+)\s*:\s*(\d+)\s+(\w+)\s*$")
SG_RE = re.compile(r"^\s*SG_\s+(\w+)")


def parse_dbc(path: Path) -> List[Dict[str, object]]:
    messages: List[Dict[str, object]] = []
    signal_counts: Dict[int, int] = {}

    current_mid = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = BO_RE.match(line)
        if m:
            mid = int(m.group(1))
            name = m.group(2)
            dlc = int(m.group(3))
            sender = m.group(4)
            messages.append(
                {
                    "id": mid,
                    "name": name,
                    "dlc": dlc,
                    "sender": sender,
                    "file": path.name,
                    "signal_count": 0,
                }
            )
            signal_counts[mid] = 0
            current_mid = mid
            continue

        if current_mid is not None and SG_RE.match(line):
            signal_counts[current_mid] += 1

    for msg in messages:
        msg["signal_count"] = signal_counts.get(int(msg["id"]), 0)

    return messages


def build_ownership_matrix(messages: List[Dict[str, object]]) -> str:
    lines = []
    lines.append("# Runtime Message Ownership Matrix")
    lines.append("")
    lines.append(
        f"- Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    lines.append("- Scope: Active split CAN DBC set only")
    lines.append(
        "- Rule: Each message must have one clear sender in active runtime profile."
    )
    lines.append("")
    lines.append("## Special-case interpretation")
    lines.append("")
    lines.append(
        "- `frmEmergencyBroadcastMsg (0x1C0)` is the SIL backbone emergency ingress contract."
    )
    lines.append("  - Active runtime sender is `V2X`.")
    lines.append(
        "  - Historical police/ambulance split producers were absorbed into the `V2X` runtime anchor."
    )
    lines.append(
        "- `ethSelectedAlertMsg` is the active output seam for warning consumers in the current SIL profile."
    )
    lines.append(
        "  - `BCM`, `IVI`, and `CLU` prefer the fresh backbone frame and fall back to mirrored `Core::*` only when the seam is stale."
    )
    lines.append(
        "  - Treat `Core::*` use here as a SIL fallback path, not as the primary output contract."
    )
    lines.append("")
    lines.append("| Message | ID (hex) | DLC | Sender | DBC | Signals |")
    lines.append("|---|---|---|---|---|---|")

    for msg in sorted(messages, key=lambda x: (int(x["id"]), str(x["name"]))):
        mid = int(msg["id"])
        lines.append(
            f"| {msg['name']} | 0x{mid:03X} | {msg['dlc']} | {msg['sender']} | "
            f"{msg['file']} | {msg['signal_count']} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_gate_report(
    messages: List[Dict[str, object]],
    missing_dbc: List[str],
    has_eth_contract: bool,
) -> Tuple[str, bool]:
    by_id: Dict[int, List[Dict[str, object]]] = {}
    by_file_and_id: Dict[Tuple[str, int], List[Dict[str, object]]] = {}
    by_name: Dict[str, List[Dict[str, object]]] = {}

    for msg in messages:
        by_id.setdefault(int(msg["id"]), []).append(msg)
        by_file_and_id.setdefault((str(msg["file"]), int(msg["id"])), []).append(msg)
        by_name.setdefault(str(msg["name"]), []).append(msg)

    dup_ids_within_dbc = {
        key: value for key, value in by_file_and_id.items() if len(value) > 1
    }
    shared_ids_across_dbcs = {
        mid: entries
        for mid, entries in by_id.items()
        if len({str(entry["file"]) for entry in entries}) > 1
    }
    dup_names = {k: v for k, v in by_name.items() if len(v) > 1}
    msg_names = {str(m["name"]) for m in messages}
    missing_mandatory = sorted(MANDATORY_MESSAGES - msg_names)
    id_mismatches: List[Tuple[str, int, List[int]]] = []
    for name, expected_id in sorted(MANDATORY_MESSAGE_IDS.items()):
        if name not in by_name:
            continue
        actual_ids = sorted({int(e["id"]) for e in by_name[name]})
        if actual_ids != [expected_id]:
            id_mismatches.append((name, expected_id, actual_ids))

    gate_checks = [
        ("Split CAN DBC files present", len(missing_dbc) == 0),
        ("Ethernet SSoT document present", has_eth_contract),
        ("No duplicate message IDs within an active DBC", len(dup_ids_within_dbc) == 0),
        ("No duplicate message names across active DBCs", len(dup_names) == 0),
        ("Mandatory message IDs match contract", len(id_mismatches) == 0),
        (
            f"Active CAN message volume >= {MIN_MESSAGE_COUNT}",
            len(messages) >= MIN_MESSAGE_COUNT,
        ),
        ("Mandatory core/baseline message set present", len(missing_mandatory) == 0),
    ]
    gate_pass = all(ok for _, ok in gate_checks)

    lines: List[str] = []
    lines.append("# Mentor Priority Gate Report")
    lines.append("")
    lines.append(f"- Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Scope: `canoe/databases` active split set validation")
    lines.append("## Gate Summary")
    lines.append("")
    lines.append(f"- Result: {'PASS' if gate_pass else 'FAIL'}")
    lines.append(f"- Active message count: {len(messages)}")
    lines.append("")
    lines.append("| Check | Result |")
    lines.append("|---|---|")
    for name, ok in gate_checks:
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} |")
    lines.append("")

    if missing_dbc:
        lines.append("## Missing DBC Files")
        lines.append("")
        for name in missing_dbc:
            lines.append(f"- {name}")
        lines.append("")

    if dup_ids_within_dbc:
        lines.append("## Duplicate IDs Within A DBC (Invalid)")
        lines.append("")
        for (dbc_name, mid), entries in sorted(dup_ids_within_dbc.items()):
            desc = ", ".join(str(e["name"]) for e in entries)
            lines.append(f"- {dbc_name} 0x{mid:03X}: {desc}")
        lines.append("")

    if shared_ids_across_dbcs:
        lines.append("## Shared IDs Across DBCs (Allowed In Split Profile)")
        lines.append("")
        lines.append(
            "- These overlaps are informational. In the active split profile, ID reuse across different domain DBCs is allowed."
        )
        lines.append("")
        for mid, entries in sorted(shared_ids_across_dbcs.items()):
            desc = ", ".join(f"{e['file']}:{e['name']}" for e in entries)
            lines.append(f"- 0x{mid:03X}: {desc}")
        lines.append("")

    if dup_names:
        lines.append("## Duplicate Names (Active Set)")
        lines.append("")
        for name, entries in sorted(dup_names.items()):
            desc = ", ".join(f"{e['file']}:0x{int(e['id']):03X}" for e in entries)
            lines.append(f"- {name}: {desc}")
        lines.append("")

    if missing_mandatory:
        lines.append("## Missing Mandatory Messages")
        lines.append("")
        for name in missing_mandatory:
            lines.append(f"- {name}")
        lines.append("")

    if id_mismatches:
        lines.append("## Mandatory Message ID Mismatches")
        lines.append("")
        for name, expected_id, actual_ids in id_mismatches:
            actual_hex = ", ".join(f"0x{mid:03X}" for mid in actual_ids)
            lines.append(
                f"- {name}: expected 0x{expected_id:03X}, actual [{actual_hex}]"
            )
        lines.append("")

    return "\n".join(lines), gate_pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path (default: current directory).",
    )
    parser.add_argument(
        "--matrix-out",
        default=DEFAULT_MATRIX_OUT,
        help="Path for generated ownership matrix draft output.",
    )
    parser.add_argument(
        "--report-out",
        default=DEFAULT_REPORT_OUT,
        help="Path for gate report markdown output.",
    )
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    dbc_dir = root / "canoe/databases"
    missing_dbc = [f for f in DBC_ACTIVE_FILES if not (dbc_dir / f).exists()]

    all_messages: List[Dict[str, object]] = []
    for dbc_name in DBC_ACTIVE_FILES:
        dbc_path = dbc_dir / dbc_name
        if dbc_path.exists():
            all_messages.extend(parse_dbc(dbc_path))

    matrix_md = build_ownership_matrix(all_messages)
    matrix_path = root / args.matrix_out
    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_path.write_text(matrix_md, encoding="utf-8")

    has_eth_contract = (root / ETH_CONTRACT_REL).exists()
    report_md, gate_pass = build_gate_report(
        all_messages, missing_dbc, has_eth_contract
    )
    report_path = root / args.report_out
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")

    print(f"[INFO] ownership matrix: {matrix_path}")
    print(f"[INFO] gate report: {report_path}")
    print(f"[INFO] gate result: {'PASS' if gate_pass else 'FAIL'}")
    return 0 if gate_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

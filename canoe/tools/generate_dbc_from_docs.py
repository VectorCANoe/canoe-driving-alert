#!/usr/bin/env python3
"""
Generate CAN DBC files from driving-situation-alert documentation.

Scope:
- Reads read-only source docs:
  - driving-situation-alert/0303_Communication_Specification.md
  - driving-situation-alert/0304_System_Variables.md
- Writes generated DBC files under canoe/databases only.

IMPORTANT FOR AI AGENTS AND AUTOMATION:
- This script is a helper, NOT an official source of truth.
- The authoritative source is the documentation chain and human-reviewed DBC output.
- Always perform manual review before using generated DBC in CANoe config/test assets.
- This parser depends on specific Markdown table headings and column layouts.
- If doc templates/wording change, update parser constants and parsing rules first.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


DOC_0303 = "driving-situation-alert/0303_Communication_Specification.md"
DOC_0304 = "driving-situation-alert/0304_System_Variables.md"
DEFAULT_OUT_DIR = "canoe/databases"

COMM_TABLE_HEADING = "## 통신 명세 표 (공식 표준 양식)"
ALIAS_TABLE_HEADING = "## DBC Signal Alias 매핑 (OEM 관례 대응)"
MANUAL_REVIEW_NOTICE = (
    "WARNING: Generated DBC is non-authoritative helper output. "
    "Manual review against latest docs is mandatory."
)
FORMAT_NOTICE = (
    "FORMAT ASSUMPTION: Parser expects the official 0303/0304 table headings/columns. "
    "If document templates changed, update this script before use."
)


@dataclass
class RawSignal:
    standard_name: str
    start_bit: int
    bit_length: int
    range_text: str
    description: str
    usage: str


@dataclass
class Signal:
    name: str
    start_bit: int
    bit_length: int
    min_value: int
    max_value: int
    unit: str
    receivers: List[str]
    is_reserved: bool = False


@dataclass
class Message:
    frame_id: int
    name: str
    dlc: int
    sender: str
    receivers: List[str]
    cycle_ms: int
    comment: str
    signals: List[Signal]


MSG_META: Dict[str, Dict[str, object]] = {
    "frmVehicleStateCanMsg": {
        "id": 0x100,
        "dlc": 2,
        "sender": "VAL_SCENARIO_CTRL",
        "receivers": ["CHS_GW"],
        "cycle_ms": 100,
        "comment": "Chassis CAN input: vehicle speed and drive state.",
    },
    "frmSteeringCanMsg": {
        "id": 0x101,
        "dlc": 1,
        "sender": "VAL_SCENARIO_CTRL",
        "receivers": ["CHS_GW"],
        "cycle_ms": 100,
        "comment": "Chassis CAN input: steering input state.",
    },
    "frmNavContextCanMsg": {
        "id": 0x110,
        "dlc": 3,
        "sender": "VAL_SCENARIO_CTRL",
        "receivers": ["INFOTAINMENT_GW"],
        "cycle_ms": 100,
        "comment": "Infotainment CAN input: road zone, direction, distance, and speed limit.",
    },
    "frmAmbientControlMsg": {
        "id": 0x210,
        "dlc": 1,
        "sender": "BODY_GW",
        "receivers": ["AMBIENT_CTRL"],
        "cycle_ms": 50,
        "comment": "Body CAN output: ambient mode/color/pattern.",
    },
    "frmClusterWarningMsg": {
        "id": 0x220,
        "dlc": 1,
        "sender": "IVI_GW",
        "receivers": ["CLU_HMI_CTRL"],
        "cycle_ms": 50,
        "comment": "Infotainment CAN output: cluster warning text code.",
    },
    "frmTestResultMsg": {
        "id": 0x230,
        "dlc": 1,
        "sender": "VAL_SCENARIO_CTRL",
        "receivers": ["Vector__XXX"],
        "cycle_ms": 0,
        "comment": "Scenario pass/fail result for SIL traceability.",
    },
}

MSG_ORDER = [
    "frmVehicleStateCanMsg",
    "frmSteeringCanMsg",
    "frmNavContextCanMsg",
    "frmAmbientControlMsg",
    "frmClusterWarningMsg",
    "frmTestResultMsg",
]

COMPAT_SIGNAL_NAME = {
    "vehicleSpeed": "gVehicleSpeed",
    "driveState": "gDriveState",
    "steeringInput": "SteeringInput",
    "roadZone": "gRoadZone",
    "navDirection": "gNavDirection",
    "zoneDistance": "gZoneDistance",
    "speedLimit": "gSpeedLimit",
    "ambientMode": "AmbientMode",
    "ambientColor": "AmbientColor",
    "ambientPattern": "AmbientPattern",
    "warningTextCode": "WarningTextCode",
    "scenarioResult": "ScenarioResult",
}

VALUE_TABLES: Dict[str, Dict[int, str]] = {
    "gDriveState": {0: "P", 1: "R", 2: "N", 3: "D"},
    "SteeringInput": {0: "NoInput", 1: "Input"},
    "gRoadZone": {0: "Normal", 1: "SchoolZone", 2: "Highway", 3: "Guide"},
    "gNavDirection": {0: "None", 1: "Left", 2: "Right", 3: "Other"},
    "AmbientMode": {
        0: "Off",
        1: "Basic",
        2: "Caution",
        3: "SchoolZone",
        4: "Reserved",
        5: "GuideLeft",
        6: "GuideRight",
        7: "Emergency",
    },
    "AmbientPattern": {0: "None", 1: "DefaultBlink", 2: "GuideLeftPattern", 3: "GuideRightPattern"},
    "ScenarioResult": {0: "Fail", 1: "Pass"},
}

NODE_COMMENTS = {
    "VAL_SCENARIO_CTRL": "SIL test controller for CAN input injection and scenario result logging.",
    "CHS_GW": "Gateway: Chassis CAN input normalization to core variables.",
    "INFOTAINMENT_GW": "Gateway: Infotainment CAN input normalization to core variables.",
    "EMS_POLICE_TX": "Emergency producer node (Police) on Ethernet domain contract.",
    "EMS_AMB_TX": "Emergency producer node (Ambulance) on Ethernet domain contract.",
    "EMS_ALERT_RX": "Emergency receiver/timeout monitor for arbitration.",
    "WARN_ARB_MGR": "Central arbitration manager (Emergency vs Navigation context).",
    "BODY_GW": "Gateway: selected alert to Body CAN (0x210).",
    "IVI_GW": "Gateway: selected alert to Infotainment CAN (0x220).",
    "AMBIENT_CTRL": "Ambient controller ECU (consumer of 0x210).",
    "CLU_HMI_CTRL": "Cluster HMI ECU (consumer of 0x220).",
    "ACCEL_CTRL": "Baseline vehicle function node for acceleration input handling.",
    "BRK_CTRL": "Baseline vehicle function node for brake input handling.",
    "STEER_CTRL": "Baseline vehicle function node for steering input handling.",
    "ENG_CTRL": "Baseline vehicle function node for ignition/engine state handling.",
    "TCM": "Baseline vehicle function node for gear state handling.",
    "VAL_BASELINE_CTRL": "Baseline SIL test controller for vehicle basic functions.",
    "HAZARD_CTRL": "Baseline vehicle function node for hazard switch handling.",
    "WINDOW_CTRL": "Baseline vehicle function node for window command handling.",
    "DRV_STATE_MGR": "Baseline vehicle function node for driver-state forwarding.",
    "NAV_CTX_MGR": "Navigation context manager node.",
    "CLU_BASE_CTRL": "Cluster baseline display manager node.",
    "DOMAIN_ROUTER": "Domain gateway router for inter-domain frame routing policy.",
    "Vector__XXX": "Reserved node for unused or filler signals.",
}

DBC_HEADER = """NS_ :
  NS_DESC_
  CM_
  BA_DEF_
  BA_
  VAL_
  CAT_DEF_
  CAT_
  FILTER
  BA_DEF_DEF_
  EV_DATA_
  ENVVAR_DATA_
  SGTYPE_
  SGTYPE_VAL_
  BA_DEF_SGTYPE_
  BA_SGTYPE_
  SIG_TYPE_REF_
  VAL_TABLE_
  SIG_GROUP_
  SIG_VALTYPE_
  SIGTYPE_VALTYPE_
  BO_TX_BU_
  BA_DEF_REL_
  BA_REL_
  BA_SGTYPE_REL_
  SG_MUL_VAL_

BS_:
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate DBC files from docs")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root path",
    )
    parser.add_argument(
        "--out-dir",
        default=DEFAULT_OUT_DIR,
        help="Output directory (relative to repo root or absolute path)",
    )
    return parser.parse_args()


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_markdown_table(text: str, heading: str) -> List[Dict[str, str]]:
    # NOTE:
    # This parser is intentionally strict about heading/table shape.
    # Keep this synchronized with the latest project document template.
    idx = text.find(heading)
    if idx < 0:
        raise RuntimeError(f"Heading not found: {heading}")

    lines = text[idx:].splitlines()[1:]
    table_lines: List[str] = []
    for line in lines:
        if line.strip().startswith("|"):
            table_lines.append(line.rstrip())
        elif table_lines:
            break

    if len(table_lines) < 2:
        raise RuntimeError(f"Table under heading not found: {heading}")

    headers = [cell.strip() for cell in table_lines[0].strip().strip("|").split("|")]
    rows: List[Dict[str, str]] = []
    for raw_line in table_lines[2:]:
        cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        elif len(cells) > len(headers):
            cells = cells[: len(headers)]
        rows.append(dict(zip(headers, cells)))
    return rows


def parse_alias_table(text_0304: str) -> Dict[str, str]:
    rows = parse_markdown_table(text_0304, ALIAS_TABLE_HEADING)
    alias_map: Dict[str, str] = {}
    for row in rows:
        std_name = row.get("표준 Name(문서)", "").strip()
        dbc_name = row.get("DBC Signal Name", "").strip()
        if std_name and dbc_name:
            alias_map[std_name] = dbc_name
    return alias_map


def _bit_value(raw: str) -> int | None:
    raw = raw.strip()
    if not raw:
        return None
    if re.fullmatch(r"\d+", raw):
        return int(raw)
    return None


def parse_can_raw_signals(text_0303: str) -> Dict[str, List[RawSignal]]:
    rows = parse_markdown_table(text_0303, COMM_TABLE_HEADING)

    can_by_message: Dict[str, List[RawSignal]] = {name: [] for name in MSG_ORDER}
    current_msg = ""
    current_identifier = ""
    active: Dict[str, object] | None = None

    def flush_active() -> None:
        nonlocal active
        if not active:
            return
        msg_name = str(active["message"])
        bit_length = int(active["last_bit"]) - int(active["start_bit"]) + 1
        if bit_length < 1:
            bit_length = 1
        can_by_message[msg_name].append(
            RawSignal(
                standard_name=str(active["signal"]),
                start_bit=int(active["start_bit"]),
                bit_length=bit_length,
                range_text=str(active["range"]),
                description=str(active["desc"]),
                usage=str(active["usage"]),
            )
        )
        active = None

    for row in rows:
        msg_cell = row.get("Message", "").strip()
        id_cell = row.get("Identifier", "").strip()
        sig_cell = row.get("Signal", "").strip()
        bit_cell = row.get("signal bit position", "").strip()
        bit = _bit_value(bit_cell)

        if msg_cell:
            if msg_cell != current_msg:
                flush_active()
            current_msg = msg_cell
        if id_cell:
            current_identifier = id_cell

        if current_msg not in MSG_META:
            continue
        if current_identifier.lower() != f"0x{MSG_META[current_msg]['id']:x}":
            continue

        if sig_cell:
            flush_active()
            if bit is None:
                raise RuntimeError(f"Missing bit position for signal '{sig_cell}' in message '{current_msg}'")
            active = {
                "message": current_msg,
                "signal": sig_cell,
                "start_bit": bit,
                "last_bit": bit,
                "range": row.get("Data 범위", "").strip(),
                "desc": row.get("Data 설명", "").strip(),
                "usage": row.get("Data 사용", "").strip(),
            }
            continue

        if active and bit is not None:
            active["last_bit"] = bit

    flush_active()
    return can_by_message


def parse_min_max_unit(range_text: str) -> tuple[int, int, str]:
    text = range_text.strip()
    if not text:
        return 0, 0, ""

    range_match = re.search(r"(-?\d+)\s*~\s*(-?\d+)", text)
    if range_match:
        min_v = int(range_match.group(1))
        max_v = int(range_match.group(2))
        tail = text[range_match.end() :].strip()
        unit = tail
        return min_v, max_v, unit

    enum_pairs = re.findall(r"(-?\d+)\s*:\s*([^/]+?)(?=\s*/\s*-?\d+\s*:|$)", text)
    if enum_pairs:
        keys = [int(k) for k, _ in enum_pairs]
        return min(keys), max(keys), ""

    slash_nums = re.fullmatch(r"(-?\d+)\s*/\s*(-?\d+)", text)
    if slash_nums:
        return int(slash_nums.group(1)), int(slash_nums.group(2)), ""

    one_num = re.fullmatch(r"(-?\d+)", text)
    if one_num:
        v = int(one_num.group(1))
        return v, v, ""

    return 0, 0, ""


def min_bits_for_unsigned(max_value: int) -> int:
    if max_value <= 0:
        return 1
    return int(math.ceil(math.log2(max_value + 1)))


def build_message_defs(raw_signals: Dict[str, List[RawSignal]], alias_map: Dict[str, str]) -> List[Message]:
    messages: List[Message] = []

    alias = dict(COMPAT_SIGNAL_NAME)
    alias.update(alias_map)

    for msg_name in MSG_ORDER:
        meta = MSG_META[msg_name]
        dlc = int(meta["dlc"])
        total_bits = dlc * 8
        entries = sorted(raw_signals.get(msg_name, []), key=lambda s: s.start_bit)
        if not entries:
            raise RuntimeError(f"No parsed signals for required message: {msg_name}")

        out_signals: List[Signal] = []
        cursor = 0
        reserved_idx = 0
        for idx, sig in enumerate(entries):
            if sig.start_bit > cursor:
                out_signals.append(
                    Signal(
                        name=f"Reserved{reserved_idx}",
                        start_bit=cursor,
                        bit_length=sig.start_bit - cursor,
                        min_value=0,
                        max_value=0,
                        unit="",
                        receivers=["Vector__XXX"],
                        is_reserved=True,
                    )
                )
                reserved_idx += 1

            min_v, max_v, unit = parse_min_max_unit(sig.range_text)
            dbc_name = alias.get(sig.standard_name, sig.standard_name)
            bit_length = sig.bit_length

            # Range-based sanity correction:
            # If document bit rows are incomplete but range says wider data (e.g., 0~255),
            # use the minimum valid bit width when there is no overlap risk.
            if min_v >= 0 and max_v >= min_v:
                required_bits = min_bits_for_unsigned(max_v)
                if required_bits > bit_length:
                    next_start = entries[idx + 1].start_bit if idx + 1 < len(entries) else total_bits
                    max_safe_bits = max(1, next_start - sig.start_bit)
                    if required_bits <= max_safe_bits:
                        print(
                            f"[WARN] Auto-adjust bit length: {msg_name}.{dbc_name} "
                            f"{bit_length} -> {required_bits} (range {min_v}~{max_v})"
                        )
                        bit_length = required_bits
                    else:
                        print(
                            f"[WARN] Bit-length mismatch unresolved: {msg_name}.{dbc_name} "
                            f"range suggests {required_bits} bits but only {max_safe_bits} bits available."
                        )
                        bit_length = max_safe_bits

            out_signals.append(
                Signal(
                    name=dbc_name,
                    start_bit=sig.start_bit,
                    bit_length=bit_length,
                    min_value=min_v,
                    max_value=max_v,
                    unit=unit,
                    receivers=list(meta["receivers"]),  # type: ignore[arg-type]
                )
            )
            cursor = sig.start_bit + bit_length

        if cursor < total_bits:
            out_signals.append(
                Signal(
                    name=f"Reserved{reserved_idx}",
                    start_bit=cursor,
                    bit_length=total_bits - cursor,
                    min_value=0,
                    max_value=0,
                    unit="",
                    receivers=["Vector__XXX"],
                    is_reserved=True,
                )
            )

        messages.append(
            Message(
                frame_id=int(meta["id"]),
                name=msg_name,
                dlc=dlc,
                sender=str(meta["sender"]),
                receivers=list(meta["receivers"]),  # type: ignore[arg-type]
                cycle_ms=int(meta["cycle_ms"]),
                comment=str(meta["comment"]),
                signals=out_signals,
            )
        )

    return messages


def build_node_list(messages: Iterable[Message], extra_nodes: Iterable[str]) -> List[str]:
    nodes: List[str] = []
    for msg in messages:
        nodes.append(msg.sender)
        nodes.extend(msg.receivers)
        for sig in msg.signals:
            nodes.extend(sig.receivers)
    nodes.extend(extra_nodes)
    deduped: List[str] = []
    seen = set()
    for node in nodes:
        if node not in seen:
            seen.add(node)
            deduped.append(node)
    if "Vector__XXX" not in seen:
        deduped.append("Vector__XXX")
    return deduped


def render_dbc(version: str, nodes: List[str], messages: List[Message], global_comment: str, extra_comments: List[str] | None = None) -> str:
    lines: List[str] = [f'VERSION "{version}"', "", DBC_HEADER.rstrip(), "", f"BU_: {' '.join(nodes)}", ""]

    for msg in messages:
        lines.append(f"BO_ {msg.frame_id} {msg.name}: {msg.dlc} {msg.sender}")
        for sig in msg.signals:
            rx = ",".join(sig.receivers)
            lines.append(
                f' SG_ {sig.name:<16} : {sig.start_bit}|{sig.bit_length}@1+ (1,0) [{sig.min_value}|{sig.max_value}] "{sig.unit}" {rx}'
            )
        lines.append("")

    for node in nodes:
        if node in NODE_COMMENTS:
            lines.append(f'CM_ BU_ {node} "{NODE_COMMENTS[node]}";')
    if nodes:
        lines.append("")

    for msg in messages:
        lines.append(f'CM_ BO_ {msg.frame_id} "{msg.comment}";')
    if messages:
        lines.append("")

    lines.append(f'CM_ "{global_comment}";')
    if extra_comments:
        for comment in extra_comments:
            lines.append(f'CM_ "{comment}";')
    lines.append("")

    if messages:
        lines.append('BA_DEF_ BO_ "GenMsgCycleTime" INT 0 10000;')
        lines.append('BA_DEF_DEF_ "GenMsgCycleTime" 0;')
        lines.append("")
        for msg in messages:
            lines.append(f'BA_ "GenMsgCycleTime" BO_ {msg.frame_id} {msg.cycle_ms};')
        lines.append("")

    for msg in messages:
        for sig in msg.signals:
            if sig.is_reserved:
                continue
            enum_map = VALUE_TABLES.get(sig.name)
            if not enum_map:
                continue
            lines.append(f"VAL_ {msg.frame_id} {sig.name}")
            for k in sorted(enum_map):
                lines.append(f'  {k} "{enum_map[k]}"')
            lines.append(" ;")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def make_split_messages(messages: List[Message], ids: List[int]) -> List[Message]:
    id_set = set(ids)
    return [msg for msg in messages if msg.frame_id in id_set]


def main() -> int:
    args = parse_args()
    repo_root: Path = args.repo_root.resolve()

    path_0303 = repo_root / DOC_0303
    path_0304 = repo_root / DOC_0304
    out_dir_arg = Path(args.out_dir)
    out_dir = out_dir_arg if out_dir_arg.is_absolute() else repo_root / out_dir_arg

    if not path_0303.exists():
        print(f"ERROR: missing file: {path_0303}", file=sys.stderr)
        return 2
    if not path_0304.exists():
        print(f"ERROR: missing file: {path_0304}", file=sys.stderr)
        return 2

    print(f"[NOTICE] {MANUAL_REVIEW_NOTICE}")
    print(f"[NOTICE] {FORMAT_NOTICE}")

    text_0303 = read_utf8(path_0303)
    text_0304 = read_utf8(path_0304)

    alias_map = parse_alias_table(text_0304)
    raw_signals = parse_can_raw_signals(text_0303)
    all_messages = build_message_defs(raw_signals, alias_map)

    baseline_nodes = build_node_list(
        all_messages,
        extra_nodes=[
            "EMS_POLICE_TX",
            "EMS_AMB_TX",
            "EMS_ALERT_RX",
            "WARN_ARB_MGR",
            "NAV_CTX_MGR",
            "ENG_CTRL",
            "TCM",
            "ACCEL_CTRL",
            "BRK_CTRL",
            "STEER_CTRL",
            "HAZARD_CTRL",
            "WINDOW_CTRL",
            "DRV_STATE_MGR",
            "CLU_BASE_CTRL",
            "VAL_BASELINE_CTRL",
            "DOMAIN_ROUTER",
            "DOMAIN_BOUNDARY_MGR",
        ],
    )

    baseline_text = render_dbc(
        version="Emergency_System_CAN_v1.2",
        nodes=baseline_nodes,
        messages=all_messages,
        global_comment=(
            "Scope: This DBC defines CAN-domain frames only. Ethernet contracts "
            "(E100/E200, 0x510/0x511/0x512) are maintained in CAPL/sysvar interface specifications."
        ),
    )
    legacy_out_dir = out_dir / "legacy"
    legacy_out_dir.mkdir(parents=True, exist_ok=True)
    write_text(legacy_out_dir / "LEGACY_emergency_system.dbc", baseline_text)

    split_plan = {
        "emergency_system_chassis.dbc": {
            "version": "Emergency_System_CAN_Chassis_v1.1",
            "ids": [0x100, 0x101, 0x230],
            "extra_nodes": ["ACCEL_CTRL", "BRK_CTRL", "STEER_CTRL", "VAL_BASELINE_CTRL"],
            "comment": "Domain split: chassis CAN network from emergency_system.dbc baseline.",
        },
        "emergency_system_body.dbc": {
            "version": "Emergency_System_CAN_Body_v1.1",
            "ids": [0x210],
            "extra_nodes": ["HAZARD_CTRL", "WINDOW_CTRL", "DRV_STATE_MGR", "WARN_ARB_MGR"],
            "comment": "Domain split: body CAN network from emergency_system.dbc baseline.",
        },
        "emergency_system_infotainment.dbc": {
            "version": "Emergency_System_CAN_Infotainment_v1.1",
            "ids": [0x110, 0x220],
            "extra_nodes": ["NAV_CTX_MGR", "CLU_BASE_CTRL"],
            "comment": "Domain split: infotainment CAN network from emergency_system.dbc baseline.",
        },
        "emergency_system_powertrain.dbc": {
            "version": "Emergency_System_CAN_Powertrain_v1.1",
            "ids": [],
            "extra_nodes": ["VAL_SCENARIO_CTRL", "ENG_CTRL", "TCM", "DOMAIN_ROUTER"],
            "comment": "Domain split: powertrain CAN network from emergency_system.dbc baseline.",
            "extra_comments": [
                "Current baseline has no dedicated powertrain CAN frame.",
                "Reserved for engine/gear/brake related CAN frames from Req_101~Req_112 expansion.",
            ],
        },
    }

    for filename, cfg in split_plan.items():
        split_messages = make_split_messages(all_messages, cfg["ids"])  # type: ignore[arg-type]
        split_nodes = build_node_list(split_messages, cfg["extra_nodes"])  # type: ignore[arg-type]
        split_text = render_dbc(
            version=str(cfg["version"]),
            nodes=split_nodes,
            messages=split_messages,
            global_comment=str(cfg["comment"]),
            extra_comments=cfg.get("extra_comments"),  # type: ignore[arg-type]
        )
        write_text(out_dir / filename, split_text)

    print(f"[DBC] Source: {DOC_0303}")
    print(f"[DBC] Alias : {DOC_0304}")
    print(f"[DBC] Output: {out_dir}")
    print("[DBC] Generated files:")
    print("  - legacy/LEGACY_emergency_system.dbc")
    print("  - emergency_system_chassis.dbc")
    print("  - emergency_system_powertrain.dbc")
    print("  - emergency_system_body.dbc")
    print("  - emergency_system_infotainment.dbc")
    return 0


if __name__ == "__main__":
    sys.exit(main())

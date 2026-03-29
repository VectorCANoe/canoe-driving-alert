from __future__ import annotations

import json
import re
import shutil
import subprocess
import textwrap
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


DATE_STAMP = "2026-03-28"
REPO_ROOT = Path(__file__).resolve().parents[3]

SRC_CAPL_ROOT = REPO_ROOT / "canoe" / "src" / "capl"
CHANNEL_ASSIGN_ROOT = REPO_ROOT / "canoe" / "cfg" / "channel_assign"
DBC_ROOT = REPO_ROOT / "canoe" / "databases"
OWNERSHIP_MATRIX = REPO_ROOT / "canoe" / "tmp" / "runtime_message_ownership_matrix.md"
TEST_UNIT_ROOT = REPO_ROOT / "canoe" / "tests" / "modules" / "test_units"

ARCH_ROOT = REPO_ROOT / "canoe" / "docs" / "architecture" / "master_book"
DATA_ROOT = ARCH_ROOT / "data"
FLOW_ROOT = ARCH_ROOT / "flows"
PNG_ROOT = ARCH_ROOT / "png"
SVG_ROOT = ARCH_ROOT / "svg"
CARD_ROOT = SVG_ROOT / "ecu_cards"
FLOW_PNG_ROOT = PNG_ROOT / "flows"
FLOW_SVG_ROOT = SVG_ROOT / "flows"

GLOBAL_PLANTUML_JAR = Path(r"C:/PlantUML/plantuml-1.2024.8.jar")
VENDORED_PLANTUML_JAR = REPO_ROOT / "canoe" / "tools" / "20_VERIFICATION" / "vendor" / "plantuml-1.2024.8.jar"

METADATA_JSON = DATA_ROOT / f"ECU_METADATA_DATASET_{DATE_STAMP}.json"
MASTER_BOOK = ARCH_ROOT / f"ECU_METADATA_BOOK_{DATE_STAMP}.md"
CARD_INDEX = ARCH_ROOT / f"ECU_CARD_INDEX_{DATE_STAMP}.md"
GROUP06_SVG = SVG_ROOT / f"GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_{DATE_STAMP}.svg"

MESSAGE_RE = re.compile(r"^BO_\s+(\d+)\s+(\w+):\s+(\d+)\s+(\w+)")
SIGNAL_RE = re.compile(r'^SG_\s+(\w+).*?"[^"]*"\s+(.+)$')
TABLE_ROW_RE = re.compile(r"^\|")
SYSVAR_RE = re.compile(r"@?[A-Za-z0-9_]+::[A-Za-z0-9_]+")


@dataclass
class MessageContract:
    name: str
    source: str
    sender: str
    receivers: set[str] = field(default_factory=set)


@dataclass
class EcuMeta:
    ecu: str
    domain: str
    group: str
    source_capl: str
    mirror_capl: str
    role_hint: str
    owner_seam: list[str]
    published_contracts: list[str]
    consumed_contracts: list[str]
    linked_ecus: list[str]
    upstream_ecus: list[str]
    downstream_ecus: list[str]
    inbound_edges: list[str]
    outbound_edges: list[str]
    inbound_dbc_sources: list[str]
    outbound_dbc_sources: list[str]
    sysvar_hints: list[str]
    test_assets: list[str]
    dbc_sources: list[str]
    doc_sources: list[str]
    current_gap_risk: str
    runtime_note: str


CURATED_HINTS: dict[str, dict[str, object]] = {
    "VCU": {
        "role_hint": "Powertrain controller",
        "owner_seam": ["Chassis::vehicleSpeed", "Chassis::driveState", "Chassis::throttlePosition"],
        "sysvar_hints": ["@Chassis::vehicleSpeed", "@Chassis::driveState", "@Chassis::throttlePosition"],
        "current_gap_risk": "Manual speed target and pedal dynamics can still fight if stale assist hints are reasserted.",
        "runtime_note": "Primary dynamics producer for speed, drive state, and throttle interpretation.",
    },
    "ESC": {
        "role_hint": "Chassis brake controller",
        "owner_seam": ["Chassis::brakePressure", "Chassis::brakeLamp", "Chassis::absActive"],
        "sysvar_hints": ["@Chassis::brakePressure", "@Chassis::brakeLamp", "@Chassis::absActive"],
        "current_gap_risk": "assistPressureFloor remains the strongest current dynamics risk during AEB overlay.",
        "runtime_note": "Consumes vehicle and AEB state, then publishes brake and stability state to downstream readers.",
    },
    "MDPS": {
        "role_hint": "Chassis steering controller",
        "owner_seam": ["Chassis::steeringAngle", "Display::steeringFrame"],
        "sysvar_hints": ["@Chassis::steeringAngle", "@Display::steeringFrame"],
        "current_gap_risk": "Steering path is largely coherent after bar, wheel, and readback unification.",
        "runtime_note": "Steering state must stay aligned across manual command, owner readback, and display frame.",
    },
    "CGW": {
        "role_hint": "Central gateway and gatekeeper",
        "owner_seam": ["CoreState::selectedAlertGateReason"],
        "sysvar_hints": ["@CoreState::selectedAlertGateReason"],
        "current_gap_risk": "Downstream display behavior depends heavily on gate reason consistency.",
        "runtime_note": "Bridges domain outputs toward IVI, CLU, BCM, and AMP while enforcing gate logic.",
    },
    "ADAS": {
        "role_hint": "Alert arbitration and decel assist domain controller",
        "owner_seam": ["Core::selectedAlertType", "Core::selectedAlertLevel"],
        "sysvar_hints": ["@Core::selectedAlertType", "@Core::selectedAlertLevel"],
        "current_gap_risk": "Must be read together with AEB, not as a standalone risk producer.",
        "runtime_note": "Consumes route, chassis, and emergency context, then emits selected alert and assist intent.",
    },
    "SCC": {
        "role_hint": "Longitudinal assist support controller",
        "owner_seam": ["Powertrain::cruiseSetSpeed"],
        "sysvar_hints": ["@Powertrain::cruiseSetSpeed"],
        "current_gap_risk": "Support-state coupling matters more than standalone bus ownership.",
        "runtime_note": "SCC support behavior feeds ADAS and VCU rather than directly owning output HMI.",
    },
    "V2X": {
        "role_hint": "Emergency ingress and V2X alert controller",
        "owner_seam": ["V2X::v2xFrame", "V2X::AmbFrame", "V2X::MyCarFrame"],
        "sysvar_hints": ["@V2X::v2xFrame", "@V2X::AmbFrame", "@V2X::MyCarFrame"],
        "current_gap_risk": "External ingress is stable; arbitration and output priority happen later.",
        "runtime_note": "Owns emergency ingress context before ADAS and CGW perform prioritization.",
    },
    "AEB": {
        "role_hint": "AEB domain controller",
        "owner_seam": ["AEB StopReq / DecelProfile / DomainHealth"],
        "sysvar_hints": ["frmAebDomainStateMsg"],
        "current_gap_risk": "This is the most likely producer of stepped brake feel across ESC, EHB, and VSM.",
        "runtime_note": "One AEB profile change can appear as multiple simultaneous chassis ECU reactions.",
    },
    "EHB": {
        "role_hint": "Brake assist leaf ECU",
        "owner_seam": ["local brake assist state"],
        "sysvar_hints": ["local brake assist state"],
        "current_gap_risk": "Shares the same decel profile thresholds as ESC/VSM and can amplify perceived brake stutter.",
        "runtime_note": "Coupled consumer of AEB state rather than an independent decision origin.",
    },
    "VSM": {
        "role_hint": "Vehicle stability intervention leaf ECU",
        "owner_seam": ["local intervention state"],
        "sysvar_hints": ["local intervention state"],
        "current_gap_risk": "Contributes to perceived intervention step changes under the same AEB profile shifts.",
        "runtime_note": "Consumes ESC and AEB domain state to produce local stability intervention behavior.",
    },
    "IVI": {
        "role_hint": "HMI and display gateway",
        "owner_seam": ["Cluster::warningTextCode", "UiRender::*"],
        "sysvar_hints": ["@Cluster::warningTextCode", "@UiRender::renderVolumLevel"],
        "current_gap_risk": "Display path is structurally sound; most issues originate upstream.",
        "runtime_note": "Routes gated alert state into visible display, map, and audio focus paths.",
    },
    "BCM": {
        "role_hint": "Body and ambient owner",
        "owner_seam": ["Body::ambientMode", "Body::frontWiperAnimFrame", "Body::blinkLeft", "Body::blinkRight"],
        "sysvar_hints": ["@Body::ambientMode", "@Body::frontWiperAnimFrame", "@Body::blinkLeft", "@Body::blinkRight"],
        "current_gap_risk": "Ambient and comfort breadth are wider than the current input-console surface.",
        "runtime_note": "Owns comfort and ambient outputs while bridging body leaf ECU state back to HMI.",
    },
    "CLU": {
        "role_hint": "Cluster owner",
        "owner_seam": ["Cluster::warningTextCode", "Display::steeringFrame"],
        "sysvar_hints": ["@Cluster::warningTextCode", "@Display::steeringFrame"],
        "current_gap_risk": "Output ownership is clean; visible issues are usually upstream.",
        "runtime_note": "Consumes selected alert state and vehicle state to build cluster-facing output.",
    },
    "AMP": {
        "role_hint": "Audio output owner",
        "owner_seam": ["UiRender::renderVolumLevel", "CoreState::baseVolume"],
        "sysvar_hints": ["@UiRender::renderVolumLevel", "@CoreState::baseVolume"],
        "current_gap_risk": "Audio rendering is stable; alert priority path matters more than bus mapping.",
        "runtime_note": "Receives gated audio intent from IVI/BCM and renders the final alert volume.",
    },
    "TEST_SCN": {
        "role_hint": "Validation and scenario harness",
        "owner_seam": ["Test::scenarioCommand", "Test::scenarioActiveId", "Test::scenarioResult"],
        "sysvar_hints": ["@Test::scenarioCommand", "@Test::scenarioActiveId", "@Test::scenarioResult"],
        "current_gap_risk": "Must stay scenario-focused and not silently become a normal feature owner.",
        "runtime_note": "Scenario entry point for validation presets, stop/manual logic, and scenario verdict readback.",
    },
    "TEST_BAS": {
        "role_hint": "Validation baseline harness",
        "owner_seam": ["validation summary seams", "Input_Console router entry"],
        "sysvar_hints": ["validation summary seams"],
        "current_gap_risk": "Should remain validation-focused and not drift back into scenario ownership.",
        "runtime_note": "Receives internal input router helpers and publishes baseline validation summaries.",
    },
}

GROUP_LABELS: dict[str, str] = {
    "GROUP_01_BASE_VEHICLE_DYNAMICS": "Group 01 Base Vehicle Dynamics",
    "GROUP_02_ADAS_AEB_BRAKE_ASSIST": "Group 02 ADAS AEB Brake Assist",
    "GROUP_03_DISPLAY_WARNING_AUDIO": "Group 03 Display Warning Audio",
    "GROUP_04_BODY_COMFORT_AMBIENT": "Group 04 Body Comfort Ambient",
    "GROUP_05_VALIDATION_SCENARIO": "Group 05 Validation Scenario",
    "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS": "Group 06 Backbone Gateway Diagnostics",
}

FOCUS_CARD_ECUS = {"VCU", "ESC", "ADAS", "AEB", "BCM", "CGW", "IVI", "TEST_SCN"}


def short_list(items: Iterable[str], limit: int) -> list[str]:
    cleaned = [item for item in items if item]
    return cleaned[:limit]


def wrap_lines(text: str, width: int) -> list[str]:
    if not text:
        return ["-"]
    lines: list[str] = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.wrap(
            paragraph,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
        if wrapped:
            lines.extend(wrapped)
        else:
            lines.append("")
    return lines or ["-"]


def domain_group(domain: str, ecu: str) -> str:
    if ecu in {"TEST_BAS", "TEST_SCN"}:
        return "GROUP_05_VALIDATION_SCENARIO"
    if domain in {"Powertrain", "Chassis"}:
        return "GROUP_01_BASE_VEHICLE_DYNAMICS"
    if domain == "ADAS":
        return "GROUP_02_ADAS_AEB_BRAKE_ASSIST"
    if domain == "Infotainment":
        return "GROUP_03_DISPLAY_WARNING_AUDIO"
    if domain == "Body":
        return "GROUP_04_BODY_COMFORT_AMBIENT"
    return "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS"


def domain_role_hint(domain: str, ecu: str) -> str:
    mapping = {
        "Powertrain": "Powertrain runtime ECU",
        "Chassis": "Chassis runtime ECU",
        "ADAS": "ADAS / sensing runtime ECU",
        "Infotainment": "Display / infotainment runtime ECU",
        "Body": "Body / comfort runtime ECU",
        "ETH_Backbone": "Gateway / backbone / diagnostic runtime ECU",
    }
    if ecu.startswith("DOOR_"):
        return "Door body leaf ECU"
    if ecu.startswith("SEAT_"):
        return "Seat comfort leaf ECU"
    if ecu.startswith("SRR_"):
        return "Radar sensing leaf ECU"
    return mapping.get(domain, "Runtime ECU")


def derive_sysvar_like(items: Iterable[str], limit: int = 4) -> list[str]:
    found: list[str] = []
    for item in items:
        if not item:
            continue
        for match in SYSVAR_RE.findall(item):
            candidate = match if match.startswith("@") else f"@{match}"
            if candidate not in found:
                found.append(candidate)
            if len(found) >= limit:
                return found
    return found


def derive_owner_seam_from_contracts(published: Iterable[str], consumed: Iterable[str]) -> list[str]:
    result: list[str] = []
    for candidate in derive_sysvar_like(list(published) + list(consumed), limit=3):
        cleaned = candidate[1:] if candidate.startswith("@") else candidate
        if cleaned not in result:
            result.append(cleaned)
    return result


def load_inventory() -> dict[str, list[str]]:
    domains: dict[str, list[str]] = defaultdict(list)
    for path in sorted(CHANNEL_ASSIGN_ROOT.rglob("*.can")):
        if "common" in path.parts:
            continue
        domains[path.parent.name].append(path.stem)
    return {domain: sorted(set(ecus)) for domain, ecus in sorted(domains.items())}


def parse_dbc_contracts() -> dict[str, MessageContract]:
    contracts: dict[str, MessageContract] = {}
    for dbc_path in sorted(DBC_ROOT.glob("*.dbc")):
        current: MessageContract | None = None
        for raw_line in dbc_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line:
                continue

            message_match = MESSAGE_RE.match(line)
            if message_match:
                _, name, _, sender = message_match.groups()
                current = MessageContract(name=name, source=dbc_path.name, sender=sender)
                contracts[name] = current
                continue

            if current is None:
                continue

            signal_match = SIGNAL_RE.match(line)
            if not signal_match:
                continue

            receiver_blob = signal_match.group(2)
            for receiver in receiver_blob.split(","):
                receiver = receiver.strip()
                if receiver and receiver != "Vector__XXX":
                    current.receivers.add(receiver)
    return contracts


def parse_runtime_matrix(contracts: dict[str, MessageContract]) -> None:
    if not OWNERSHIP_MATRIX.exists():
        return
    for line in OWNERSHIP_MATRIX.read_text(encoding="utf-8").splitlines():
        if not TABLE_ROW_RE.match(line) or "---" in line:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        if parts[0] in {"Message", "ID (hex)"}:
            continue
        message, _, _, sender, source = parts[:5]
        if message not in contracts:
            contracts[message] = MessageContract(name=message, source=source, sender=sender)


def collect_test_assets() -> list[str]:
    assets: list[str] = []
    for path in sorted(TEST_UNIT_ROOT.iterdir()):
        if not path.is_dir():
            continue
        if path.name in {"assign", "common", "retire"}:
            continue
        if path.name.startswith("TC_CANOE_"):
            assets.append(path.name)
    return assets


def asset_matches_ecu(asset: str, ecu: str) -> bool:
    pattern = re.compile(rf"(^|_){re.escape(ecu)}($|_)")
    return bool(pattern.search(asset))


def build_metadata() -> list[EcuMeta]:
    domains = load_inventory()
    contracts = parse_dbc_contracts()
    parse_runtime_matrix(contracts)
    assets = collect_test_assets()

    published_by_ecu: dict[str, list[str]] = defaultdict(list)
    consumed_by_ecu: dict[str, list[str]] = defaultdict(list)
    linked_by_ecu: dict[str, set[str]] = defaultdict(set)
    upstream_by_ecu: dict[str, set[str]] = defaultdict(set)
    downstream_by_ecu: dict[str, set[str]] = defaultdict(set)
    dbc_by_ecu: dict[str, set[str]] = defaultdict(set)
    inbound_edges_by_ecu: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    outbound_edges_by_ecu: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    inbound_dbc_by_ecu: dict[str, set[str]] = defaultdict(set)
    outbound_dbc_by_ecu: dict[str, set[str]] = defaultdict(set)

    for contract in contracts.values():
        published_by_ecu[contract.sender].append(contract.name)
        dbc_by_ecu[contract.sender].add(contract.source)
        for receiver in sorted(contract.receivers):
            consumed_by_ecu[receiver].append(contract.name)
            dbc_by_ecu[receiver].add(contract.source)
            inbound_edges_by_ecu[receiver][contract.sender].append(contract.name)
            outbound_edges_by_ecu[contract.sender][receiver].append(contract.name)
            inbound_dbc_by_ecu[receiver].add(contract.source)
            outbound_dbc_by_ecu[contract.sender].add(contract.source)
            if receiver != contract.sender:
                linked_by_ecu[contract.sender].add(receiver)
                linked_by_ecu[receiver].add(contract.sender)
                upstream_by_ecu[receiver].add(contract.sender)
                downstream_by_ecu[contract.sender].add(receiver)

    metadata: list[EcuMeta] = []
    for domain in sorted(domains):
        for ecu in domains[domain]:
            hints = CURATED_HINTS.get(ecu, {})
            group = domain_group(domain, ecu)
            source_capl = f"canoe/src/capl/ecu/{ecu}.can" if (SRC_CAPL_ROOT / "ecu" / f"{ecu}.can").exists() else "-"
            mirror_capl = f"canoe/cfg/channel_assign/{domain}/{ecu}.can" if (CHANNEL_ASSIGN_ROOT / domain / f"{ecu}.can").exists() else "-"
            test_assets = sorted(asset for asset in assets if asset_matches_ecu(asset, ecu))

            metadata.append(
                EcuMeta(
                    ecu=ecu,
                    domain=domain,
                    group=group,
                    source_capl=source_capl,
                    mirror_capl=mirror_capl,
                    role_hint=str(hints.get("role_hint", domain_role_hint(domain, ecu))),
                    owner_seam=list(hints.get("owner_seam", derive_owner_seam_from_contracts(published_by_ecu.get(ecu, []), consumed_by_ecu.get(ecu, [])))),
                    published_contracts=sorted(set(published_by_ecu.get(ecu, []))),
                    consumed_contracts=sorted(set(consumed_by_ecu.get(ecu, []))),
                    linked_ecus=sorted(linked_by_ecu.get(ecu, set())),
                    upstream_ecus=sorted(upstream_by_ecu.get(ecu, set())),
                    downstream_ecus=sorted(downstream_by_ecu.get(ecu, set())),
                    inbound_edges=[
                        f"{sender} :: {', '.join(sorted(set(messages))[:6])}"
                        for sender, messages in sorted(inbound_edges_by_ecu.get(ecu, {}).items())
                    ],
                    outbound_edges=[
                        f"{receiver} :: {', '.join(sorted(set(messages))[:6])}"
                        for receiver, messages in sorted(outbound_edges_by_ecu.get(ecu, {}).items())
                    ],
                    inbound_dbc_sources=sorted(inbound_dbc_by_ecu.get(ecu, set())),
                    outbound_dbc_sources=sorted(outbound_dbc_by_ecu.get(ecu, set())),
                    sysvar_hints=list(hints.get("sysvar_hints", derive_sysvar_like(
                        list(hints.get("owner_seam", []))
                        + list(published_by_ecu.get(ecu, []))
                        + list(consumed_by_ecu.get(ecu, []))
                    ))),
                    test_assets=test_assets,
                    dbc_sources=sorted(dbc_by_ecu.get(ecu, set())),
                    doc_sources=list(
                        hints.get(
                            "doc_sources",
                            ["0301", "0302", "0303", "0304", "04_SW_Implementation", "ecu-flow-appendix"],
                        )
                    ),
                    current_gap_risk=str(hints.get("current_gap_risk", "")),
                    runtime_note=str(hints.get("runtime_note", "")),
                )
            )

    return sorted(metadata, key=lambda item: (item.group, item.domain, item.ecu))


def render_multiline_text(x: int, y: int, lines: list[str], css_class: str, line_height: int = 24) -> str:
    parts = []
    for idx, line in enumerate(lines):
        parts.append(f'<text x="{x}" y="{y + idx * line_height}" class="{css_class}">{escape(line)}</text>')
    return "\n".join(parts)


def clean_items(items: Iterable[str]) -> list[str]:
    return [item.strip() for item in items if item and item.strip() and item.strip() != "-"]


def block_height(lines: list[str], line_height: int, padding: int = 0) -> int:
    return len(lines) * line_height + padding


def render_bullets(items: Iterable[str], width: int = 52) -> list[str]:
    cleaned = clean_items(items)
    if not cleaned:
        return ["-"]
    result: list[str] = []
    for item in cleaned:
        wrapped = wrap_lines(item, width)
        for idx, line in enumerate(wrapped):
            result.append(f"{'- ' if idx == 0 else '  '}{line}")
    return result


def inline_summary(items: Iterable[str], limit: int = 5, placeholder: str = "-") -> str:
    cleaned = clean_items(items)
    if not cleaned:
        return placeholder
    if len(cleaned) <= limit:
        return ", ".join(cleaned)
    return ", ".join(cleaned[:limit]) + f" (+{len(cleaned) - limit} more)"


def extract_messages_from_edges(edges: Iterable[str], limit: int = 6) -> list[str]:
    found: list[str] = []
    for edge in clean_items(edges):
        _, payload = split_edge(edge)
        for token in [part.strip() for part in payload.split(",") if part.strip()]:
            if token not in found:
                found.append(token)
            if len(found) >= limit:
                return found
    return found


def primary_sysvar(meta: EcuMeta) -> str:
    curated = derive_sysvar_like(meta.sysvar_hints, limit=1)
    if curated:
        return curated[0]
    owner = derive_sysvar_like(meta.owner_seam, limit=1)
    if owner:
        return owner[0]
    fallback = derive_sysvar_like(meta.published_contracts + meta.consumed_contracts, limit=1)
    if fallback:
        return fallback[0]
    return "-"


def primary_test_asset(meta: EcuMeta) -> str:
    return meta.test_assets[0] if meta.test_assets else "No direct native test asset matched"


def primary_doc_source(meta: EcuMeta) -> str:
    return inline_summary(meta.doc_sources, limit=4)


def primary_rx_message(meta: EcuMeta) -> str:
    messages = extract_messages_from_edges(meta.inbound_edges, limit=4)
    if messages:
        return ", ".join(messages)
    fallback = [item for item in clean_items(meta.consumed_contracts) if "::" not in item][:4]
    return ", ".join(fallback) if fallback else "-"


def primary_tx_message(meta: EcuMeta) -> str:
    messages = extract_messages_from_edges(meta.outbound_edges, limit=4)
    if messages:
        return ", ".join(messages)
    fallback = [item for item in clean_items(meta.published_contracts) if "::" not in item][:4]
    return ", ".join(fallback) if fallback else "-"


def derived_gap_issue(meta: EcuMeta) -> str:
    if meta.current_gap_risk.strip():
        return meta.current_gap_risk.strip()
    issues: list[str] = []
    if not meta.test_assets:
        issues.append("No direct native test asset matched")
    if not meta.sysvar_hints:
        issues.append("Primary sysvar not yet curated")
    if not meta.inbound_edges or not meta.outbound_edges:
        issues.append("One-sided network extraction only")
    if not issues:
        issues.append("No ECU-specific issue curated yet")
    return "; ".join(issues)


def derived_runtime_note(meta: EcuMeta) -> str:
    if meta.runtime_note.strip():
        return meta.runtime_note.strip()
    consume_count = len(clean_items(meta.consumed_contracts))
    publish_count = len(clean_items(meta.published_contracts))
    linked = inline_summary(meta.linked_ecus, limit=3, placeholder="no dominant linked ECU")
    return f"Consumes {consume_count} contract(s), publishes {publish_count} contract(s), linked mainly to {linked}."


def card_filename(ecu: str) -> str:
    return f"ECU_CARD_{ecu}_{DATE_STAMP}.svg"


def group_fill(group: str) -> str:
    palette = {
        "GROUP_01_BASE_VEHICLE_DYNAMICS": "#dbeafe",
        "GROUP_02_ADAS_AEB_BRAKE_ASSIST": "#fee2e2",
        "GROUP_03_DISPLAY_WARNING_AUDIO": "#ede9fe",
        "GROUP_04_BODY_COMFORT_AMBIENT": "#dcfce7",
        "GROUP_05_VALIDATION_SCENARIO": "#fef3c7",
        "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS": "#fce7f3",
    }
    return palette.get(group, "#e5e7eb")


def summarize_edges(edges: Iterable[str], limit: int = 10) -> list[str]:
    cleaned = clean_items(edges)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit] + [f"... +{len(cleaned) - limit} more ECU edges"]


def split_edge(edge: str) -> tuple[str, str]:
    if "::" in edge:
        ecu, payload = edge.split("::", 1)
        return ecu.strip(), payload.strip()
    return edge.strip(), "-"


def render_edge_column(x: int, y: int, width: int, title: str, edges: Iterable[str], fill: str) -> tuple[str, int]:
    rendered_edges = summarize_edges(edges, limit=10)
    cursor_y = y + 58
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="10" rx="18" ry="18" class="box" fill="{fill}"/>',
        f'<text x="{x + 24}" y="{y + 36}" class="label">{escape(title)}</text>',
    ]
    if not rendered_edges:
        rendered_edges = ["- :: no direct DBC edge extracted"]
    for edge in rendered_edges:
        ecu, payload = split_edge(edge)
        payload_lines = wrap_lines(payload, width=32)
        card_height = 52 + len(payload_lines) * 18
        parts.append(
            f'<rect x="{x + 14}" y="{cursor_y}" width="{width - 28}" height="{card_height}" rx="16" ry="16" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>'
        )
        parts.append(f'<text x="{x + 30}" y="{cursor_y + 28}" class="node">{escape(ecu)}</text>')
        parts.append(render_multiline_text(x + 30, cursor_y + 52, payload_lines, "small", 18))
        cursor_y += card_height + 14

    total_height = max(220, cursor_y - y + 6)
    parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{total_height}" class="box" fill="{fill}"/>'
    return "\n".join(parts), total_height


def representative_signal_path(meta: EcuMeta) -> tuple[str | None, str | None, str | None, str | None]:
    inbound = summarize_edges(meta.inbound_edges, limit=1)
    outbound = summarize_edges(meta.outbound_edges, limit=1)
    src_ecu = None
    src_msg = None
    dst_ecu = None
    dst_msg = None
    if inbound:
        src_ecu, src_msg = split_edge(inbound[0])
    if outbound:
        dst_ecu, dst_msg = split_edge(outbound[0])
    return src_ecu, src_msg, dst_ecu, dst_msg


def render_representative_signal_flow(x: int, y: int, width: int, meta: EcuMeta) -> tuple[str, int]:
    src_ecu, src_msg, dst_ecu, dst_msg = representative_signal_path(meta)
    if not src_ecu and not dst_ecu:
        no_path_height = 118
        return (
            "\n".join(
                [
                    f'<rect x="{x}" y="{y}" width="{width}" height="{no_path_height}" class="box" fill="#eff6ff"/>',
                    f'<text x="{x + 22}" y="{y + 36}" class="label">Representative signal flow</text>',
                    f'<text x="{x + 22}" y="{y + 72}" class="text">No representative DBC signal path extracted for this ECU.</text>',
                ]
            ),
            no_path_height,
        )

    panel_height = 206
    left_x = x + 28
    center_x = x + width // 2 - 110
    right_x = x + width - 248
    box_y = y + 70
    msg_y = y + 132
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{panel_height}" class="box" fill="#eff6ff"/>',
        f'<text x="{x + 22}" y="{y + 36}" class="label">Representative signal flow</text>',
    ]

    if src_ecu:
        parts.append(f'<rect x="{left_x}" y="{box_y}" width="220" height="58" rx="16" ry="16" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>')
        parts.append(f'<text x="{left_x + 18}" y="{box_y + 34}" class="node">{escape(src_ecu)}</text>')

    parts.append(f'<rect x="{center_x}" y="{box_y}" width="220" height="58" rx="16" ry="16" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>')
    parts.append(f'<text x="{center_x + 110}" y="{box_y + 34}" text-anchor="middle" class="node">{escape(meta.ecu)}</text>')

    if dst_ecu:
        parts.append(f'<rect x="{right_x}" y="{box_y}" width="220" height="58" rx="16" ry="16" fill="#ffffff" stroke="#86efac" stroke-width="1.5"/>')
        parts.append(f'<text x="{right_x + 18}" y="{box_y + 34}" class="node">{escape(dst_ecu)}</text>')

    if src_ecu:
        parts.append(f'<line x1="{left_x + 220}" y1="{box_y + 29}" x2="{center_x}" y2="{box_y + 29}" class="lane"/>')
        rx_lines = wrap_lines(f"Rx {src_msg or '-'}", 28)
        parts.append(render_multiline_text(left_x + 236, msg_y, rx_lines, "small", 18))

    if dst_ecu:
        parts.append(f'<line x1="{center_x + 220}" y1="{box_y + 29}" x2="{right_x}" y2="{box_y + 29}" class="lane"/>')
        tx_lines = wrap_lines(f"Tx {dst_msg or '-'}", 28)
        parts.append(render_multiline_text(center_x + 236, msg_y, tx_lines, "small", 18))

    lane_note = []
    if src_ecu and dst_ecu:
        lane_note = [f"{src_ecu} -> {meta.ecu} -> {dst_ecu}"]
    elif src_ecu:
        lane_note = [f"{src_ecu} -> {meta.ecu}"]
    elif dst_ecu:
        lane_note = [f"{meta.ecu} -> {dst_ecu}"]
    if lane_note:
        parts.append(render_multiline_text(x + 22, y + 182, lane_note, "text", 20))

    return "\n".join(parts), panel_height


def render_runtime_flow_panel(x: int, y: int, width: int, meta: EcuMeta) -> tuple[str, int]:
    left_svg, left_height = render_edge_column(x + 10, y + 26, 450, "Inbound Flow", meta.inbound_edges, "#e0f2fe")
    right_svg, right_height = render_edge_column(x + width - 460, y + 26, 450, "Outbound Flow", meta.outbound_edges, "#dbeafe")
    center_height = max(420, 160 + block_height(wrap_lines(meta.role_hint, 28), 22) + block_height(render_bullets(meta.owner_seam, 34), 20))
    center_x = x + width // 2 - 230
    center_y = y + 66

    src_ecu, src_msg, dst_ecu, dst_msg = representative_signal_path(meta)
    rep_label = []
    if src_ecu and dst_ecu:
        rep_label = [f"Representative path: {src_ecu} -> {meta.ecu} -> {dst_ecu}"]
    elif src_ecu:
        rep_label = [f"Representative path: {src_ecu} -> {meta.ecu}"]
    elif dst_ecu:
        rep_label = [f"Representative path: {meta.ecu} -> {dst_ecu}"]
    else:
        rep_label = ["Representative path: not yet extracted"]

    panel_height = max(left_height, right_height, center_height + 120) + 46
    mid_y = center_y + center_height // 2

    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{panel_height}" class="box" fill="#ffffff"/>',
        f'<text x="{x + 22}" y="{y + 34}" class="label">Runtime network flow</text>',
        left_svg,
        right_svg,
        f'<rect x="{center_x}" y="{center_y}" width="460" height="{center_height}" class="box" fill="#dcfce7"/>',
        f'<text x="{center_x + 230}" y="{center_y + 40}" text-anchor="middle" class="node">{escape(meta.ecu)}</text>',
        render_multiline_text(center_x + 34, center_y + 74, wrap_lines(meta.role_hint, 28), "text", 22),
        f'<text x="{center_x + 34}" y="{center_y + 132 + block_height(wrap_lines(meta.role_hint, 28), 22)}" class="small">Owner seam</text>',
        render_multiline_text(center_x + 34, center_y + 158 + block_height(wrap_lines(meta.role_hint, 28), 22), render_bullets(meta.owner_seam, 34), "small", 20),
        f'<text x="{center_x + 34}" y="{center_y + center_height - 110}" class="small">Primary sysvar</text>',
        render_multiline_text(center_x + 34, center_y + center_height - 82, wrap_lines(primary_sysvar(meta), 36), "text", 20),
        f'<text x="{center_x + 34}" y="{center_y + center_height - 34}" class="small">{escape(inline_summary(rep_label, limit=1))}</text>',
        f'<line x1="{x + 460}" y1="{mid_y}" x2="{center_x}" y2="{mid_y}" class="lane"/>',
        f'<line x1="{center_x + 460}" y1="{mid_y}" x2="{x + width - 460}" y2="{mid_y}" class="lane"/>',
    ]

    if src_msg:
        parts.append(render_multiline_text(x + 480, mid_y - 26, wrap_lines(f"Representative Rx: {src_msg}", 22), "small", 18))
    else:
        parts.append(f'<text x="{x + 480}" y="{mid_y - 10}" class="small">Representative Rx: -</text>')

    if dst_msg:
        parts.append(render_multiline_text(center_x + 480, mid_y - 26, wrap_lines(f"Representative Tx: {dst_msg}", 22), "small", 18))
    else:
        parts.append(f'<text x="{center_x + 480}" y="{mid_y - 10}" class="small">Representative Tx: -</text>')

    return "\n".join(parts), panel_height


def render_metadata_table(x: int, y: int, width: int, meta: EcuMeta, group_label: str) -> tuple[str, int]:
    rows = [
        ("ECU", meta.ecu),
        ("Layer/Group", f"{meta.domain} / {group_label}"),
        ("Owner seam", inline_summary(meta.owner_seam, limit=4)),
        ("Rx message", primary_rx_message(meta)),
        ("Tx message", primary_tx_message(meta)),
        ("Linked ECU", inline_summary(meta.linked_ecus, limit=6)),
        ("Primary sysvar", primary_sysvar(meta)),
        ("Primary test asset", primary_test_asset(meta)),
        ("Doc source", primary_doc_source(meta)),
        ("Gap/Issue", derived_gap_issue(meta)),
        ("Runtime note", derived_runtime_note(meta)),
    ]

    label_width = 220
    value_width = width - label_width - 44
    row_parts: list[str] = [f'<rect x="{x}" y="{y}" width="{width}" height="10" class="box" fill="#f8fafc"/>', f'<text x="{x + 22}" y="{y + 34}" class="label">ECU metadata</text>']
    cursor_y = y + 54
    total_height = 0
    for label, value in rows:
        wrapped = wrap_lines(value, 92)
        row_height = max(44, 18 + len(wrapped) * 18 + 14)
        row_parts.append(f'<rect x="{x + 14}" y="{cursor_y}" width="{label_width}" height="{row_height}" rx="12" ry="12" fill="#e5eefb" stroke="#c7d2fe" stroke-width="1.2"/>')
        row_parts.append(f'<rect x="{x + 20 + label_width}" y="{cursor_y}" width="{value_width}" height="{row_height}" rx="12" ry="12" fill="#ffffff" stroke="#d1d5db" stroke-width="1.2"/>')
        row_parts.append(f'<text x="{x + 32}" y="{cursor_y + 28}" class="text">{escape(label)}</text>')
        row_parts.append(render_multiline_text(x + 34 + label_width, cursor_y + 26, wrapped, "text", 18))
        cursor_y += row_height + 12
        total_height = cursor_y - y
    total_height += 10
    row_parts[0] = f'<rect x="{x}" y="{y}" width="{width}" height="{total_height}" class="box" fill="#f8fafc"/>'
    return "\n".join(row_parts), total_height


def render_card(meta: EcuMeta) -> str:
    title = f"ECU Network Flow - {meta.ecu}"
    group_label = GROUP_LABELS[meta.group]
    group_color = group_fill(meta.group)

    role = wrap_lines(meta.role_hint, 28)
    inbound_dbc = render_bullets(meta.inbound_dbc_sources or meta.dbc_sources, width=22)
    outbound_dbc = render_bullets(meta.outbound_dbc_sources or meta.dbc_sources, width=22)

    placement_y = 100
    placement_height = max(126, 100 + block_height(role, 22))

    flow_band_y = placement_y + placement_height + 24
    flow_band_height = max(140, 98 + max(block_height(inbound_dbc, 20), block_height(outbound_dbc, 20)))

    runtime_y = flow_band_y + flow_band_height + 24
    runtime_svg, runtime_height = render_runtime_flow_panel(30, runtime_y, 1540, meta)

    footer_y = runtime_y + runtime_height + 24
    metadata_svg, metadata_height = render_metadata_table(30, footer_y, 1540, meta, group_label)
    total_height = footer_y + metadata_height + 50

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{total_height}" viewBox="0 0 1600 {total_height}">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>
  <style>
    .bg {{ fill: #f8fafc; }}
    .title {{ font: 700 30px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .sub {{ font: 500 15px 'Segoe UI', sans-serif; fill: #475569; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .text {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 14px 'Segoe UI', sans-serif; fill: #475569; }}
    .node {{ font: 700 18px 'Segoe UI', sans-serif; fill: #111827; }}
    .box {{ rx: 20; ry: 20; stroke: #475569; stroke-width: 2; }}
    .lane {{ stroke: #64748b; stroke-width: 3; fill: none; marker-end: url(#arrow); }}
  </style>
  <rect x="0" y="0" width="1600" height="{total_height}" class="bg"/>
  <text x="34" y="44" class="title">{escape(title)}</text>
  <text x="34" y="72" class="sub">{escape(group_label)} | Domain {escape(meta.domain)} | generated internal OEM-style network flow card</text>

  <rect x="30" y="{placement_y}" width="1540" height="{placement_height}" class="box" fill="{group_color}"/>
  <text x="52" y="{placement_y + 36}" class="label">ECU placement</text>
  <text x="52" y="{placement_y + 68}" class="text">Group: {escape(group_label)}</text>
  <text x="450" y="{placement_y + 68}" class="text">Domain: {escape(meta.domain)}</text>
  {render_multiline_text(52, placement_y + 98, role, "text", 22)}

  <rect x="30" y="{flow_band_y}" width="1540" height="{flow_band_height}" class="box" fill="#ffffff"/>
  <text x="52" y="{flow_band_y + 36}" class="label">Network surface</text>
  <rect x="52" y="{flow_band_y + 52}" width="430" height="{flow_band_height - 70}" rx="16" ry="16" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="74" y="{flow_band_y + 82}" class="small">Inbound DBC / bus surface</text>
  {render_multiline_text(74, flow_band_y + 108, inbound_dbc, "text", 20)}
  <rect x="585" y="{flow_band_y + 52}" width="430" height="{flow_band_height - 70}" rx="16" ry="16" fill="#ecfeff" stroke="#67e8f9" stroke-width="1.5"/>
  <text x="607" y="{flow_band_y + 82}" class="small">Current ECU lane</text>
  <text x="607" y="{flow_band_y + 110}" class="node">{escape(meta.ecu)}</text>
  <text x="607" y="{flow_band_y + 138}" class="small">{escape(meta.domain)} / {escape(group_label)}</text>
  <rect x="1118" y="{flow_band_y + 52}" width="430" height="{flow_band_height - 70}" rx="16" ry="16" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="1140" y="{flow_band_y + 82}" class="small">Outbound DBC / bus surface</text>
  {render_multiline_text(1140, flow_band_y + 108, outbound_dbc, "text", 20)}

  {runtime_svg}

  {metadata_svg}
</svg>
"""


def write_card_set(metadata: list[EcuMeta]) -> None:
    CARD_ROOT.mkdir(parents=True, exist_ok=True)
    for meta in metadata:
        card_svg = render_card(meta)
        (CARD_ROOT / card_filename(meta.ecu)).write_text(card_svg, encoding="utf-8")
        if meta.ecu in FOCUS_CARD_ECUS:
            (SVG_ROOT / card_filename(meta.ecu)).write_text(card_svg, encoding="utf-8")


def render_summary_table(counter: Counter[str], label: str) -> list[str]:
    lines = [f"| {label} | Count |", "| --- | ---: |"]
    for key, count in sorted(counter.items()):
        lines.append(f"| `{key}` | `{count}` |")
    return lines


def render_master_book(metadata: list[EcuMeta]) -> str:
    total = len(metadata)
    group_counts = Counter(item.group for item in metadata)
    domain_counts = Counter(item.domain for item in metadata)
    direct_tests = sum(1 for item in metadata if item.test_assets)
    no_test = [item.ecu for item in metadata if not item.test_assets]
    no_published = [item.ecu for item in metadata if not item.published_contracts]
    no_consumed = [item.ecu for item in metadata if not item.consumed_contracts]

    lines: list[str] = [
        f"# ECU Metadata Book ({DATE_STAMP})",
        "",
        "## Purpose",
        "",
        "This is the internal master ECU metadata book for the active CANoe runtime.",
        "Treat this markdown dataset as the master asset from which per-ECU SVG, later PDF, and later reviewer-facing extracts can be derived.",
        "",
        "## Source Priority",
        "",
        "1. `canoe/src/capl/**/*.can`",
        "2. `canoe/cfg/channel_assign/**/*.can`",
        "3. `canoe/databases/*.dbc`",
        "4. `canoe/tmp/runtime_message_ownership_matrix.md`",
        "5. `canoe/tests/modules/test_units/**`",
        "6. `driving-alert-workproducts/0301~0304`, `04_SW_Implementation`",
        "",
        "## Coverage Summary",
        "",
        f"- ECU inventory count: `{total}`",
        f"- ECUs with direct matching native tests: `{direct_tests}`",
        f"- ECUs without direct matching native tests: `{len(no_test)}`",
        f"- ECUs without published contract rows in current DBC/runtime supplement: `{len(no_published)}`",
        f"- ECUs without consumed contract rows in current DBC/runtime supplement: `{len(no_consumed)}`",
        "",
        "### By Group",
        "",
        *render_summary_table(group_counts, "Group"),
        "",
        "### By Domain",
        "",
        *render_summary_table(domain_counts, "Domain"),
        "",
        "## Immediate Read Order",
        "",
        f"1. [Group view](ECU_GROUP_NETWORK_VIEW_{DATE_STAMP}.md)",
        f"2. [Per-ECU card index](ECU_CARD_INDEX_{DATE_STAMP}.md)",
        "3. `svg/ecu_cards/`",
        f"4. [Overview SVG](svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_{DATE_STAMP}.svg)",
        "",
        "## Explicit Gaps",
        "",
        f"- No direct native test anchor yet: `{', '.join(no_test) if no_test else '-'}`",
        f"- No published contract rows: `{', '.join(no_published) if no_published else '-'}`",
        f"- No consumed contract rows: `{', '.join(no_consumed) if no_consumed else '-'}`",
        "",
    ]

    current_group = None
    for item in metadata:
        if item.group != current_group:
            current_group = item.group
            lines.extend([f"## {GROUP_LABELS[item.group]}", ""])
        lines.extend(
            [
                f"### `{item.ecu}`",
                "",
                f"- SVG card: `svg/ecu_cards/{card_filename(item.ecu)}`",
                "",
                "| Field | Value |",
                "| --- | --- |",
                f"| Domain | `{item.domain}` |",
                f"| Group | `{GROUP_LABELS[item.group]}` |",
                f"| Role hint | {item.role_hint} |",
                f"| Owner seam | {'<br>'.join(item.owner_seam) if item.owner_seam else '-'} |",
                f"| CAPL source | `{item.source_capl}` |",
                f"| Active mirror | `{item.mirror_capl}` |",
                f"| Published contracts | {'<br>'.join(item.published_contracts) if item.published_contracts else '-'} |",
                f"| Consumed contracts | {'<br>'.join(item.consumed_contracts) if item.consumed_contracts else '-'} |",
                f"| Upstream ECU | {'<br>'.join(item.upstream_ecus) if item.upstream_ecus else '-'} |",
                f"| Downstream ECU | {'<br>'.join(item.downstream_ecus) if item.downstream_ecus else '-'} |",
                f"| Linked ECU | {'<br>'.join(item.linked_ecus) if item.linked_ecus else '-'} |",
                f"| Sysvar hints | {'<br>'.join(item.sysvar_hints) if item.sysvar_hints else '-'} |",
                f"| DBC source | {'<br>'.join(item.dbc_sources) if item.dbc_sources else '-'} |",
                f"| Direct native tests | {'<br>'.join(item.test_assets) if item.test_assets else '-'} |",
                f"| Doc source | {'<br>'.join(item.doc_sources) if item.doc_sources else '-'} |",
                f"| Current gap / risk | {item.current_gap_risk} |",
                f"| Runtime note | {item.runtime_note} |",
                "",
            ]
        )

    return "\n".join(lines) + "\n"


def render_card_index(metadata: list[EcuMeta]) -> str:
    lines = [
        f"# ECU Card Index ({DATE_STAMP})",
        "",
        "This is the generated index for all per-ECU OEM-style network flow SVG cards.",
        "",
    ]
    by_group: dict[str, list[EcuMeta]] = defaultdict(list)
    for item in metadata:
        by_group[item.group].append(item)
    for group in sorted(by_group):
        lines.extend([f"## {GROUP_LABELS[group]}", ""])
        for item in by_group[group]:
            lines.append(f"- [{item.ecu}](svg/ecu_cards/{card_filename(item.ecu)})")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_group06_svg(metadata: list[EcuMeta]) -> str:
    members = [item.ecu for item in metadata if item.group == "GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS"]
    primary_nodes = ", ".join(members)
    columns = 4
    ecu_boxes: list[str] = []
    for idx, ecu in enumerate(members):
        row = idx // columns
        col = idx % columns
        x = 60 + col * 300
        y = 390 + row * 52
        ecu_boxes.append(f'<rect x="{x}" y="{y}" width="250" height="36" rx="12" ry="12" fill="#f8fafc" stroke="#475569" stroke-width="1.5"/>')
        ecu_boxes.append(f'<text x="{x + 14}" y="{y + 24}" class="node">{escape(ecu)}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="980" viewBox="0 0 1320 980">
  <style>
    .title {{ font: 700 28px 'Segoe UI', sans-serif; fill: #111827; }}
    .label {{ font: 700 18px 'Segoe UI', sans-serif; fill: #0f172a; }}
    .node {{ font: 600 15px 'Segoe UI', sans-serif; fill: #1f2937; }}
    .small {{ font: 500 14px 'Segoe UI', sans-serif; fill: #475569; }}
    .box {{ rx: 18; ry: 18; stroke: #475569; stroke-width: 2; }}
  </style>
  <text x="34" y="42" class="title">Group 06 - Backbone / Gateway / Diagnostics</text>
  <text x="34" y="70" class="small">Runtime backbone, gateway, diagnostics, and service-facing nodes that do not fit the display/body/dynamics groups.</text>

  <rect x="30" y="110" width="1260" height="130" class="box" fill="#fce7f3"/>
  <text x="52" y="146" class="label">Primary nodes</text>
  <text x="52" y="176" class="node">{escape(primary_nodes)}</text>
  <text x="52" y="204" class="small">Validation nodes stay in Group 05. This group focuses on backbone routing, diagnostics, and service surfaces.</text>

  <rect x="30" y="270" width="1260" height="90" class="box" fill="#ede9fe"/>
  <text x="52" y="306" class="label">Main path</text>
  <text x="52" y="336" class="node">domain state / service requests -> CGW / ETHB / DCM / SGW / IBOX -> routed gateway, diagnostic, and external service surfaces</text>

  <rect x="30" y="380" width="1260" height="520" class="box" fill="#ffffff"/>
  <text x="52" y="416" class="label">ECU roster</text>
  {"".join(ecu_boxes)}

  <rect x="30" y="920" width="1260" height="40" class="box" fill="#f8fafc"/>
  <text x="52" y="946" class="small">Use the per-ECU card index for individual runtime details.</text>
</svg>
"""


def ensure_dirs() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    FLOW_ROOT.mkdir(parents=True, exist_ok=True)
    FLOW_PNG_ROOT.mkdir(parents=True, exist_ok=True)
    FLOW_SVG_ROOT.mkdir(parents=True, exist_ok=True)
    CARD_ROOT.mkdir(parents=True, exist_ok=True)


def resolve_plantuml_jar() -> Path:
    if GLOBAL_PLANTUML_JAR.exists():
        return GLOBAL_PLANTUML_JAR
    if VENDORED_PLANTUML_JAR.exists():
        return VENDORED_PLANTUML_JAR
    raise FileNotFoundError(
        "PlantUML jar not found. Install global PlantUML at C:/PlantUML or keep the vendored jar under canoe/tools/20_VERIFICATION/vendor."
    )


def resolve_java() -> str:
    java = shutil.which("java")
    if java:
        return java
    fallback = Path(r"C:/Program Files/Java/jdk1.8.0_261/bin/java.exe")
    if fallback.exists():
        return str(fallback)
    raise FileNotFoundError("Java runtime not found for PlantUML rendering.")


def render_flow_assets() -> list[Path]:
    if not FLOW_ROOT.exists():
        return []

    java = resolve_java()
    plantuml_jar = resolve_plantuml_jar()
    outputs: list[Path] = []

    for puml in sorted(FLOW_ROOT.glob("*.puml")):
        png_path = FLOW_PNG_ROOT / f"{puml.stem}.png"
        svg_path = FLOW_SVG_ROOT / f"{puml.stem}.svg"

        png_result = subprocess.run(
            [java, "-jar", str(plantuml_jar), "-pipe", "-charset", "UTF-8", "-tpng"],
            input=puml.read_bytes(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if png_result.returncode != 0 or not png_result.stdout:
            stderr_text = png_result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"PlantUML PNG render failed for {puml.name}: {stderr_text or 'no stdout produced'}")
        png_path.write_bytes(png_result.stdout)
        outputs.append(png_path)

        svg_result = subprocess.run(
            [java, "-jar", str(plantuml_jar), "-pipe", "-charset", "UTF-8", "-tsvg"],
            input=puml.read_bytes(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if svg_result.returncode != 0 or not svg_result.stdout:
            stderr_text = svg_result.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"PlantUML SVG render failed for {puml.name}: {stderr_text or 'no stdout produced'}")
        svg_path.write_bytes(svg_result.stdout)
        outputs.append(svg_path)

    return outputs


def write_outputs(metadata: list[EcuMeta]) -> None:
    ensure_dirs()
    METADATA_JSON.write_text(json.dumps([asdict(item) for item in metadata], ensure_ascii=False, indent=2), encoding="utf-8")
    MASTER_BOOK.write_text(render_master_book(metadata), encoding="utf-8")
    CARD_INDEX.write_text(render_card_index(metadata), encoding="utf-8")
    GROUP06_SVG.write_text(render_group06_svg(metadata), encoding="utf-8")
    write_card_set(metadata)
    render_flow_assets()


def main() -> None:
    official_builder = REPO_ROOT / "canoe" / "docs" / "architecture" / "master_book" / "tools" / "build_master_book_asset_pack.py"
    if official_builder.exists():
        import importlib.util
        import sys

        spec = importlib.util.spec_from_file_location("master_book_asset_pack", official_builder)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)
        module.main()
        return

    metadata = build_metadata()
    write_outputs(metadata)
    print(f"[ecu-master-book] dataset: {METADATA_JSON}")
    print(f"[ecu-master-book] book: {MASTER_BOOK}")
    print(f"[ecu-master-book] index: {CARD_INDEX}")
    print(f"[ecu-master-book] group06: {GROUP06_SVG}")
    print(f"[ecu-master-book] card_count: {len(metadata)}")


if __name__ == "__main__":
    main()

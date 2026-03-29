from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ASSIGN_ROOT = REPO_ROOT / "canoe" / "cfg" / "channel_assign"
DBC_ROOT = REPO_ROOT / "canoe" / "databases"
OWNERSHIP_MATRIX = REPO_ROOT / "canoe" / "tmp" / "runtime_message_ownership_matrix.md"
TEST_UNIT_ROOT = REPO_ROOT / "canoe" / "tests" / "modules" / "test_units"
OUTPUT_DOC = REPO_ROOT / "canoe" / "docs" / "architecture" / "ecu-flow-appendix.md"


MESSAGE_RE = re.compile(r"^BO_\s+(\d+)\s+(\w+):\s+(\d+)\s+(\w+)")
SIGNAL_RE = re.compile(r'^SG_\s+(\w+).*?"[^"]*"\s+(.+)$')
TABLE_ROW_RE = re.compile(r"^\|")


@dataclass
class MessageContract:
    name: str
    source: str
    sender: str
    receivers: set[str] = field(default_factory=set)


@dataclass
class EcuFlow:
    ecu: str
    domain: str
    published: list[str] = field(default_factory=list)
    consumed: list[str] = field(default_factory=list)
    linked_ecus: list[str] = field(default_factory=list)
    test_assets: list[str] = field(default_factory=list)


def load_inventory() -> dict[str, list[str]]:
    domains: dict[str, list[str]] = defaultdict(list)
    for path in sorted(CHANNEL_ASSIGN_ROOT.rglob("*.can")):
        if "common" in path.parts:
            continue
        domains[path.parent.name].append(path.stem)
    return dict(domains)


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
                current = MessageContract(
                    name=name,
                    source=dbc_path.name,
                    sender=sender,
                )
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

    lines = OWNERSHIP_MATRIX.read_text(encoding="utf-8").splitlines()
    for line in lines:
        if not TABLE_ROW_RE.match(line):
            continue
        if "---" in line:
            continue

        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        if parts[0] in {"Message", "ID (hex)"}:
            continue

        message, _, _, sender, source = parts[:5]
        if message not in contracts:
            contracts[message] = MessageContract(
                name=message,
                source=source,
                sender=sender,
            )


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


def shorten(items: list[str], limit: int = 5) -> str:
    if not items:
        return "-"
    if len(items) <= limit:
        return "<br>".join(items)
    shown = "<br>".join(items[:limit])
    return f"{shown}<br>+{len(items) - limit} more"


def build_flows(
    domains: dict[str, list[str]],
    contracts: dict[str, MessageContract],
    assets: list[str],
) -> list[EcuFlow]:
    published_by_ecu: dict[str, list[str]] = defaultdict(list)
    consumed_by_ecu: dict[str, list[str]] = defaultdict(list)
    linked_by_ecu: dict[str, set[str]] = defaultdict(set)

    for contract in contracts.values():
        published_by_ecu[contract.sender].append(contract.name)
        for receiver in sorted(contract.receivers):
            consumed_by_ecu[receiver].append(contract.name)
            if receiver != contract.sender:
                linked_by_ecu[contract.sender].add(receiver)
                linked_by_ecu[receiver].add(contract.sender)

    flows: list[EcuFlow] = []
    for domain in sorted(domains):
        for ecu in sorted(domains[domain]):
            ecu_assets = [asset for asset in assets if asset_matches_ecu(asset, ecu)]
            flow = EcuFlow(
                ecu=ecu,
                domain=domain,
                published=sorted(set(published_by_ecu.get(ecu, []))),
                consumed=sorted(set(consumed_by_ecu.get(ecu, []))),
                linked_ecus=sorted(linked_by_ecu.get(ecu, set())),
                test_assets=sorted(ecu_assets),
            )
            flows.append(flow)
    return flows


def render(flows: list[EcuFlow]) -> str:
    domain_counts: dict[str, int] = defaultdict(int)
    direct_contract = 0
    direct_test = 0
    semantic_only: list[str] = []
    test_gap: list[str] = []

    for flow in flows:
        domain_counts[flow.domain] += 1
        if flow.published or flow.consumed:
            direct_contract += 1
        else:
            semantic_only.append(flow.ecu)
        if flow.test_assets:
            direct_test += 1
        else:
            test_gap.append(flow.ecu)

    lines: list[str] = [
        "# ECU Flow Appendix",
        "",
        "> [!IMPORTANT]",
        "> This appendix is the current reviewer-facing ECU interaction catalog for the active CANoe SIL baseline.",
        "> It is generated from active `channel_assign` inventory, split DBC contracts, runtime ownership matrix, and native test assets.",
        "",
        "## Purpose",
        "",
        "Use this appendix when the question is:",
        "",
        "- which ECU publishes active network-facing contracts",
        "- which contracts each ECU consumes in the executable baseline",
        "- which other ECUs each ECU is directly linked to through those contracts",
        "- whether that ECU already has a direct native verification anchor",
        "",
        "This document is appendix-grade and reviewer-facing.",
        "Working notes, temporary hypotheses, or migration memos must stay outside `canoe/docs/**`.",
        "",
        "## Source Assets",
        "",
        "- inventory: `canoe/cfg/channel_assign/**`",
        "- network contracts: `canoe/databases/*.dbc`",
        "- runtime ownership supplement: `canoe/tmp/runtime_message_ownership_matrix.md`",
        "- native test anchors: `canoe/tests/modules/test_units/**`",
        "- regeneration command: `python canoe/tools/20_VERIFICATION/20_build_ecu_flow_appendix.py`",
        "",
        "## Coverage Summary",
        "",
        f"- active ECU count: `{len(flows)}`",
        f"- direct network-contract ECUs: `{direct_contract}`",
        f"- semantic-only / non-network appendix rows: `{len(semantic_only)}`",
        f"- ECUs with direct native test anchors: `{direct_test}`",
        f"- ECUs without explicit direct native test anchors: `{len(test_gap)}`",
        "",
        "| Domain | ECU count |",
        "| --- | ---: |",
    ]

    for domain in sorted(domain_counts):
        lines.append(f"| `{domain}` | `{domain_counts[domain]}` |")

    lines.extend(
        [
            "",
            "## Reading Rule",
            "",
            "- `Published contracts` are the ECU's active outbound message contracts in the current executable baseline.",
            "- `Consumed contracts` are message contracts where the ECU appears as a DBC receiver in the active split databases.",
            "- `Linked ECUs` are direct sender/receiver neighbors derived from the same contracts.",
            "- `Direct native test anchors` are current explicit native assets whose IDs mention the ECU directly.",
            "- `Direct native test anchors` are a direct-anchor index, not the full indirect coverage claim for that ECU.",
            "- A row may still be valid when `Consumed contracts = -` or `Direct native test anchors = -`; that means the ECU is currently documented mainly as a publisher, semantic seam, or indirectly covered participant.",
            "",
            "## Explicit Gaps To Close",
            "",
            f"- semantic-only / non-network appendix rows: `{', '.join(semantic_only) if semantic_only else '-'}`",
            f"- no direct native anchor yet: `{', '.join(test_gap) if test_gap else '-'}`",
            "",
            "## ECU Catalog",
            "",
            "| ECU | Domain | Published contracts | Consumed contracts | Linked ECUs | Direct native test anchors |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )

    for flow in flows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{flow.ecu}`",
                    f"`{flow.domain}`",
                    shorten(flow.published),
                    shorten(flow.consumed),
                    shorten(flow.linked_ecus, limit=8),
                    shorten(flow.test_assets, limit=3),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Usage Boundary",
            "",
            "- Use `contracts/communication-matrix.md` and `contracts/owner-route.md` for authoritative ownership and routing decisions.",
            "- Use `verification/test-asset-mapping.md`, `verification/execution-guide.md`, and `verification/oracle.md` for executable test interpretation.",
            "- Use this appendix as the ECU-by-ECU reviewer summary that bridges those assets.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    domains = load_inventory()
    contracts = parse_dbc_contracts()
    parse_runtime_matrix(contracts)
    assets = collect_test_assets()
    flows = build_flows(domains, contracts, assets)
    OUTPUT_DOC.write_text(render(flows), encoding="utf-8")
    print(f"[ecu-flow-appendix] wrote: {OUTPUT_DOC}")
    print(f"[ecu-flow-appendix] rows: {len(flows)}")


if __name__ == "__main__":
    main()

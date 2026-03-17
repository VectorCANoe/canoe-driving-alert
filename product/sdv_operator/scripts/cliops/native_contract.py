from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .common import ROOT


class NativeContractError(RuntimeError):
    """Raised when the native execution contract cannot be read or resolved."""


@dataclass(frozen=True)
class NativeTierContract:
    tier: str
    tier_code: int
    profile_id: str
    pack_id: str
    suite_id: str
    assign_folder: str
    summary_report: str
    incoming_raw: str
    incoming_trace_dir: str
    incoming_logging_dir: str
    config_name: str
    execute_supported: bool

    @property
    def summary_report_path(self) -> Path:
        return ROOT / self.summary_report


_CONTRACT_PATH = ROOT / "product" / "sdv_operator" / "config" / "native_e2e_execution_contract.json"


def native_contract_path() -> Path:
    return _CONTRACT_PATH


def load_native_contract() -> dict:
    if not _CONTRACT_PATH.exists():
        raise NativeContractError(f"native execution contract not found: {_CONTRACT_PATH}")
    try:
        return json.loads(_CONTRACT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        raise NativeContractError(f"native execution contract is invalid JSON: {ex}") from ex


def iter_tier_contracts() -> list[NativeTierContract]:
    payload = load_native_contract()
    rows = payload.get("tiers", [])
    contracts: list[NativeTierContract] = []
    for row in rows:
        tier = str(row.get("tier", "")).upper()
        config_name = str(row.get("config_name", "")).strip()
        if not config_name and tier in {"UT", "IT", "ST"}:
            config_name = f"{tier}_ACTIVE_BASELINE"
        execute_supported = bool(row.get("execute_supported", bool(config_name)))
        contracts.append(
            NativeTierContract(
                tier=tier,
                tier_code=int(row.get("tier_code", 0)),
                profile_id=str(row.get("profile_id", "")),
                pack_id=str(row.get("pack_id", "")),
                suite_id=str(row.get("suite_id", "")),
                assign_folder=str(row.get("assign_folder", "")),
                summary_report=str(row.get("summary_report", "")),
                incoming_raw=str(row.get("incoming_raw", "")),
                incoming_trace_dir=str(row.get("incoming_trace_dir", "")),
                incoming_logging_dir=str(row.get("incoming_logging_dir", "")),
                config_name=config_name,
                execute_supported=execute_supported,
            )
        )
    return contracts


def resolve_tier_contract(tier: str) -> NativeTierContract:
    key = tier.strip().upper()
    for contract in iter_tier_contracts():
        if contract.tier == key:
            return contract
    raise NativeContractError(f"native tier contract not found: {tier}")

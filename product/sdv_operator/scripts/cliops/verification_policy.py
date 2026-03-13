from __future__ import annotations

import json
from pathlib import Path

from cliops.common import ROOT


DEFAULT_POLICY_PATH = ROOT / "product" / "sdv_operator" / "config" / "verification_phase_policy.json"


def load_phase_policy(phase: str, policy_path: Path | None = None) -> dict:
    path = policy_path or DEFAULT_POLICY_PATH
    if not path.exists():
        return _fallback_policy(phase)
    raw = json.loads(path.read_text(encoding="utf-8"))
    profiles = raw.get("profiles", {}) if isinstance(raw, dict) else {}
    profile = profiles.get(phase, profiles.get("pre")) if isinstance(profiles, dict) else None
    if not isinstance(profile, dict):
        return _fallback_policy(phase)
    return {
        "phase": phase,
        "description": str(profile.get("description", "")),
        "hard_fail_steps": list(profile.get("hard_fail_steps", [])),
        "advisory_steps": list(profile.get("advisory_steps", [])),
        "readiness_warn_states": [str(item).upper() for item in profile.get("readiness_warn_states", [])],
        "readiness_fail_states": [str(item).upper() for item in profile.get("readiness_fail_states", [])],
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
    }


def classify_step_status(step_name: str, rc: int, policy: dict) -> tuple[str, str]:
    if rc == 0:
        return "PASS", "mandatory"
    if step_name in set(policy.get("advisory_steps", [])):
        return "WARN", "advisory"
    return "FAIL", "mandatory"


def classify_readiness(overall: str, policy: dict) -> str:
    state = str(overall or "").upper()
    if state in {"READY", "SCORED_READY", "PASS"}:
        return "PASS"
    if state in set(policy.get("readiness_fail_states", [])):
        return "FAIL"
    if state in set(policy.get("readiness_warn_states", [])):
        return "WARN"
    return "WARN"


def _fallback_policy(phase: str) -> dict:
    return {
        "phase": phase,
        "description": "fallback verification phase policy",
        "hard_fail_steps": [],
        "advisory_steps": [],
        "readiness_warn_states": ["READY_FOR_FINALIZE", "PREPARED", "PREPARED_PARTIAL", "NOT_PREPARED"],
        "readiness_fail_states": ["MISSING", "BROKEN", "INVALID"],
        "source": "fallback",
    }

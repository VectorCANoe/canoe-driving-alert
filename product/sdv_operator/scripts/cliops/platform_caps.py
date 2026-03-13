"""Platform/runtime capability checks for the SDV CLI."""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeCapability:
    name: str
    available: bool
    detail: str


def platform_label() -> str:
    system = platform.system().strip() or sys.platform
    release = platform.release().strip()
    return f"{system} {release}".strip()


def is_windows_host() -> bool:
    return sys.platform.startswith("win")


def canoe_runtime_check() -> RuntimeCapability:
    if is_windows_host():
        return RuntimeCapability(
            name="canoe_runtime",
            available=True,
            detail="Windows host detected; CANoe COM automation may be available.",
        )
    return RuntimeCapability(
        name="canoe_runtime",
        available=False,
        detail=(
            f"Current host is {platform_label()}. "
            "CANoe COM automation is supported only on Windows."
        ),
    )


def require_canoe_runtime(action_name: str) -> str | None:
    cap = canoe_runtime_check()
    if cap.available:
        return None
    return f"{action_name} unavailable: {cap.detail}"


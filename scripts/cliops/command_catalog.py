"""Shared product command catalog for shell palette and Textual TUI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaletteCommand:
    title: str
    command: str
    summary: str
    windows_only: bool = False
    notes: str = ""


PRODUCT_COMMAND_GROUPS: dict[str, list[PaletteCommand]] = {
    "Operate": [
        PaletteCommand(
            title="Guided operator flow",
            command="start guided",
            summary="Open the stable numeric guided flow for operators.",
            notes="Use this when you want a conservative fallback without the full TUI shell.",
        ),
        PaletteCommand(
            title="Scenario 4 trigger",
            command="scenario run --id 4",
            summary="Send the default scenario 4 command through CANoe COM with ack wait.",
            windows_only=True,
            notes="Measurement should already be running, or use --no-ensure-running only when you know the runtime state.",
        ),
        PaletteCommand(
            title="Measurement status",
            command="canoe measure-status",
            summary="Read the current CANoe measurement state.",
            windows_only=True,
        ),
        PaletteCommand(
            title="Measurement start",
            command="canoe measure-start",
            summary="Start CANoe measurement through COM.",
            windows_only=True,
        ),
        PaletteCommand(
            title="Measurement stop",
            command="canoe measure-stop",
            summary="Stop CANoe measurement through COM.",
            windows_only=True,
        ),
    ],
    "Verify": [
        PaletteCommand(
            title="Precheck batch",
            command="start precheck",
            summary="Run gates + prepare + smoke + readiness status in one flow.",
            windows_only=True,
            notes="This is the fastest operator path before collecting evidence.",
        ),
        PaletteCommand(
            title="Quick verify",
            command="verify quick",
            summary="Prepare, smoke, and summarize one run quickly.",
            windows_only=True,
        ),
        PaletteCommand(
            title="Run readiness status",
            command="verify status",
            summary="Check whether raw evidence, markers, and scored outputs are complete.",
        ),
        PaletteCommand(
            title="All gates",
            command="gate all",
            summary="Run doc-sync, cfg-hygiene, capl-sync, multibus-dbc, and cli-readiness gates.",
        ),
    ],
    "Inspect": [
        PaletteCommand(
            title="Environment doctor",
            command="doctor",
            summary="Check CANoe COM attach, measurement state, and required sysvars.",
            windows_only=True,
        ),
        PaletteCommand(
            title="Read failSafeMode",
            command="capl sysvar-get --namespace Core --var failSafeMode",
            summary="Read one representative Core sysvar through the CAPL/COM bridge.",
            windows_only=True,
        ),
        PaletteCommand(
            title="Set scenarioCommand=4",
            command="capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int",
            summary="Write the manual scenario trigger sysvar directly.",
            windows_only=True,
        ),
        PaletteCommand(
            title="Command contract",
            command="contract",
            summary="Print canonical and legacy command surfaces for operators and automation.",
        ),
    ],
    "Package": [
        PaletteCommand(
            title="Portable bundle",
            command="package bundle-portable --mode onefolder",
            summary="Build the portable operator ZIP bundle.",
        ),
        PaletteCommand(
            title="Windows exe",
            command="package build-exe --mode onefolder --clean",
            summary="Build the Windows one-folder executable baseline.",
            windows_only=True,
        ),
    ],
}


def build_shell_palette_groups() -> dict[str, list[tuple[str, str]]]:
    """Render the shared product catalog as shell palette tuples."""
    groups: dict[str, list[tuple[str, str]]] = {}
    for group_name, items in PRODUCT_COMMAND_GROUPS.items():
        groups[group_name] = [(f"/{item.command}", item.summary) for item in items]
    groups["Session"] = [
        ("/history", "Show recent shell command history"),
        ("/repeat 1", "Repeat the latest shell command"),
        ("/exit", "Exit shell"),
    ]
    return groups

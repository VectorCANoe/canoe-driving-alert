"""Shared product command catalog for shell palette and Textual TUI."""

from __future__ import annotations

import datetime as dt
import shlex
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CommandParam:
    key: str
    flag: str
    label: str
    default: str = ""
    help: str = ""
    placeholder: str = ""
    kind: str = "text"
    choices: tuple[str, ...] = ()
    required: bool = False


@dataclass(frozen=True)
class PaletteCommand:
    command_id: str
    title: str
    command: str
    summary: str
    windows_only: bool = False
    notes: str = ""
    base_command: str = ""
    params: tuple[CommandParam, ...] = field(default_factory=tuple)

    def executable_base(self) -> str:
        return self.base_command or self.command


def build_command_tokens(command: PaletteCommand, values: dict[str, str] | None = None) -> list[str]:
    """Build CLI tokens from a palette command and optional form values."""
    tokens = shlex.split(command.executable_base())
    for param in command.params:
        raw = (values or {}).get(param.key, param.default)
        raw = raw.strip()
        if not raw:
            if param.required:
                raise ValueError(f"{param.label} is required.")
            continue
        if param.kind == "int":
            try:
                int(raw)
            except ValueError as ex:  # pragma: no cover - UI validation surfaces the message
                raise ValueError(f"{param.label} must be an integer.") from ex
        if param.choices and raw not in param.choices:
            allowed = ", ".join(param.choices)
            raise ValueError(f"{param.label} must be one of: {allowed}")
        tokens.extend([param.flag, raw])
    return tokens


def resolve_default_value(raw: str) -> str:
    if raw == "{run_id}":
        return dt.datetime.now().strftime("%Y%m%d_%H%M")
    if raw == "{today}":
        return dt.date.today().isoformat()
    return raw


def resolve_command_defaults(command: PaletteCommand) -> dict[str, str]:
    return {param.key: resolve_default_value(param.default) for param in command.params}


def build_command_index() -> dict[str, PaletteCommand]:
    return {
        command.command_id: command
        for commands in PRODUCT_COMMAND_GROUPS.values()
        for command in commands
    }


PRODUCT_COMMAND_GROUPS: dict[str, list[PaletteCommand]] = {
    "Operate": [
        PaletteCommand(
            command_id="operate.guided",
            title="Guided operator flow",
            command="start guided",
            summary="Open the stable numeric guided flow for operators.",
            notes="Use this when you want the conservative fallback without the full dashboard.",
        ),
        PaletteCommand(
            command_id="operate.scenario_trigger",
            title="Scenario trigger",
            command="scenario run --id 4",
            base_command="scenario run",
            summary="Send one SIL scenario command and wait for ack.",
            windows_only=True,
            notes="Use the scenario ID only. The CLI keeps namespace and ack wiring consistent.",
            params=(
                CommandParam(
                    key="scenario_id",
                    flag="--id",
                    label="Scenario ID",
                    default="4",
                    help="0 stops, 1..25 scenario runs, 100 auto-demo, 200..255 baseline diag.",
                    placeholder="4",
                    kind="int",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="operate.measure_status",
            title="Measurement status",
            command="canoe measure-status",
            summary="Read the current CANoe measurement state.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="operate.measure_start",
            title="Measurement start",
            command="canoe measure-start",
            summary="Start CANoe measurement through COM.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="operate.measure_stop",
            title="Measurement stop",
            command="canoe measure-stop",
            summary="Stop CANoe measurement through COM.",
            windows_only=True,
        ),
    ],
    "Verify": [
        PaletteCommand(
            command_id="verify.precheck_batch",
            title="Precheck batch",
            command="start precheck",
            summary="Run gates + prepare + smoke + readiness status in one operator flow.",
            windows_only=True,
            notes="Best first step before collecting evidence or screenshots.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="Evidence run identifier, usually YYYYMMDD_HHMM.",
                    placeholder="20260308_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="Owner",
                    default="DEV2",
                    help="Operator/owner tag written into reports.",
                    placeholder="DEV2",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.quick_verify",
            title="Quick verify",
            command="verify quick",
            summary="Prepare, smoke, and summarize one run quickly.",
            windows_only=True,
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="Evidence run identifier.",
                    placeholder="20260308_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="Owner",
                    default="DEV2",
                    help="Owner tag used by smoke/status reports.",
                    placeholder="DEV2",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.run_readiness_status",
            title="Run readiness status",
            command="verify status --run-id 20260308_0900",
            base_command="verify status",
            summary="Check whether raw evidence, markers, and scored outputs are complete.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="Run folder to inspect under canoe/logging/evidence.",
                    placeholder="20260308_0900",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.all_gates",
            title="All gates",
            command="gate all",
            summary="Run doc-sync, cfg-hygiene, capl-sync, multibus-dbc, and cli-readiness gates.",
        ),
    ],
    "Inspect": [
        PaletteCommand(
            command_id="inspect.environment_doctor",
            title="Environment doctor",
            command="doctor",
            summary="Check CANoe COM attach, measurement state, and required sysvars.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="inspect.read_system_variable",
            title="Read system variable",
            command="capl sysvar-get --namespace Core --var failSafeMode",
            base_command="capl sysvar-get",
            summary="Read one system variable through the CAPL/COM bridge.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="Namespace",
                    default="Core",
                    help="System variable namespace.",
                    placeholder="Core",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="Variable",
                    default="failSafeMode",
                    help="System variable name.",
                    placeholder="failSafeMode",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.write_system_variable",
            title="Write system variable",
            command="capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int",
            base_command="capl sysvar-set",
            summary="Write one system variable through the CAPL/COM bridge.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="Namespace",
                    default="Test",
                    help="System variable namespace.",
                    placeholder="Test",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="Variable",
                    default="scenarioCommand",
                    help="System variable name.",
                    placeholder="scenarioCommand",
                    required=True,
                ),
                CommandParam(
                    key="value",
                    flag="--value",
                    label="Value",
                    default="4",
                    help="Value to write.",
                    placeholder="4",
                    required=True,
                ),
                CommandParam(
                    key="value_type",
                    flag="--value-type",
                    label="Value Type",
                    default="int",
                    help="Use int, float, bool, or string.",
                    placeholder="int",
                    choices=("int", "float", "bool", "string"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.command_contract",
            title="Command contract",
            command="contract",
            summary="Print canonical and legacy command surfaces for operators and automation.",
        ),
    ],
    "Package": [
        PaletteCommand(
            command_id="package.portable_bundle",
            title="Portable bundle",
            command="package bundle-portable --mode onefolder",
            base_command="package bundle-portable",
            summary="Build the portable operator ZIP bundle.",
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="Package Mode",
                    default="onefolder",
                    help="Use onefolder for operator distribution or onefile for a single binary.",
                    placeholder="onefolder",
                    choices=("onefolder", "onefile"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="package.windows_exe",
            title="Windows exe",
            command="package build-exe --mode onefolder",
            base_command="package build-exe",
            summary="Build the Windows one-folder executable baseline.",
            windows_only=True,
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="Build Mode",
                    default="onefolder",
                    help="Use onefolder for stable operator handoff or onefile for a single exe.",
                    placeholder="onefolder",
                    choices=("onefolder", "onefile"),
                    required=True,
                ),
            ),
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

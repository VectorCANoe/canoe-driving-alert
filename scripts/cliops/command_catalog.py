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
    "Primary Workflow": [
        PaletteCommand(
            command_id="verify.all_gates",
            title="1) Gate all",
            command="gate all",
            summary="Run the full preflight gate bundle before touching runtime.",
            notes="This is the first daily step. If this fails, stop and fix consistency issues first.",
        ),
        PaletteCommand(
            command_id="operate.scenario_trigger",
            title="2) Scenario run",
            command="scenario run --id 4",
            base_command="scenario run",
            summary="Inject one SIL scenario into CANoe and wait for the ack path.",
            windows_only=True,
            notes="Use this after gates are clean and measurement is running.",
            params=(
                CommandParam(
                    key="scenario_id",
                    flag="--id",
                    label="Scenario ID",
                    default="4",
                    help="0 stops, 1..25 runs a scenario, 100 auto-demo, 200..255 baseline diagnostic.",
                    placeholder="4",
                    kind="int",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.quick_verify",
            title="3) Verify quick",
            command="verify quick",
            summary="Create evidence folders, run smoke checks, and score run readiness in one pass.",
            windows_only=True,
            notes="Use this immediately after scenario execution to collect the first validation evidence.",
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
    ],
    "Runtime Support": [
        PaletteCommand(
            command_id="inspect.environment_doctor",
            title="?? ??",
            command="doctor",
            summary="CANoe COM ??, measurement ??, ?? sysvar? ?????.",
            windows_only=True,
            notes="??? ???? measurement ??? ???? ? ?????.",
        ),
        PaletteCommand(
            command_id="operate.measure_status",
            title="?? ??",
            command="canoe measure-status",
            summary="?? CANoe measurement ??? ????.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="operate.measure_start",
            title="?? ??",
            command="canoe measure-start",
            summary="COM? ?? CANoe measurement? ?????.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="operate.measure_stop",
            title="?? ??",
            command="canoe measure-stop",
            summary="COM? ?? CANoe measurement? ?????.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="verify.precheck_batch",
            title="?? ?? ??",
            command="start precheck",
            summary="gate, prepare, smoke, readiness status? ? ?? ?????.",
            windows_only=True,
            notes="??? ?? ?? ?? ? ??? ?? ??? ??? ? ?????.",
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
            command_id="verify.run_readiness_status",
            title="?? ?? ??",
            command="verify status --run-id 20260308_0900",
            base_command="verify status",
            summary="raw evidence, marker, score ??? ????? ?????.",
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
            command_id="operate.guided",
            title="??? ??",
            command="start guided",
            summary="???? ?? ??? fallback ??? ???.",
            notes="?? Textual ????? ?? ?? ?? ?????.",
        ),
    ],
    "System Access": [
        PaletteCommand(
            command_id="inspect.read_system_variable",
            title="??? ?? ??",
            command="capl sysvar-get --namespace Core --var failSafeMode",
            base_command="capl sysvar-get",
            summary="CAPL/COM ???? ??? ?? ??? ????.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="??????",
                    default="Core",
                    help="??? ?? ?????????.",
                    placeholder="Core",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="??",
                    default="failSafeMode",
                    help="??? ?? ?????.",
                    placeholder="failSafeMode",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.write_system_variable",
            title="??? ?? ??",
            command="capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int",
            base_command="capl sysvar-set",
            summary="CAPL/COM ???? ??? ?? ??? ???.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="??????",
                    default="Test",
                    help="??? ?? ?????????.",
                    placeholder="Test",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="??",
                    default="scenarioCommand",
                    help="??? ?? ?????.",
                    placeholder="scenarioCommand",
                    required=True,
                ),
                CommandParam(
                    key="value",
                    flag="--value",
                    label="?",
                    default="4",
                    help="? ?? ?????.",
                    placeholder="4",
                    required=True,
                ),
                CommandParam(
                    key="value_type",
                    flag="--value-type",
                    label="? ??",
                    default="int",
                    help="int, float, bool, string ? ??? ?????.",
                    placeholder="int",
                    choices=("int", "float", "bool", "string"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.command_contract",
            title="?? ?? ??",
            command="contract",
            summary="?? ??? ?? alias? ?? ?????.",
        ),
    ],
    "Packaging": [
        PaletteCommand(
            command_id="package.portable_bundle",
            title="??? ??",
            command="package bundle-portable --mode onefolder",
            base_command="package bundle-portable",
            summary="???? portable ZIP ??? ????.",
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="??? ??",
                    default="onefolder",
                    help="?? ??? onefolder, ?? ????? onefile? ?????.",
                    placeholder="onefolder",
                    choices=("onefolder", "onefile"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="package.windows_exe",
            title="??? ?? ??",
            command="package build-exe --mode onefolder",
            base_command="package build-exe",
            summary="Windows one-folder ?? ?? ???? ????.",
            windows_only=True,
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="?? ??",
                    default="onefolder",
                    help="??? handoff? onefolder, ?? exe? onefile? ?????.",
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

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
            summary="런타임 조작 전에 전체 preflight gate 묶음을 실행합니다.",
            notes="일일 운영의 첫 단계입니다. 여기서 실패하면 먼저 정합성 문제를 수정하십시오.",
        ),
        PaletteCommand(
            command_id="operate.scenario_trigger",
            title="2) Scenario run",
            command="scenario run --id 4",
            base_command="scenario run",
            summary="SIL 시나리오를 CANoe에 주입하고 ack 경로를 확인합니다.",
            windows_only=True,
            notes="Gate all이 끝났고 measurement가 올라와 있을 때 실행하십시오.",
            params=(
                CommandParam(
                    key="scenario_id",
                    flag="--id",
                    label="시나리오 ID",
                    default="4",
                    help="0은 정지, 1~25는 시나리오 실행, 100은 auto-demo, 200~255는 baseline diagnostic입니다.",
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
            summary="증빙 폴더 생성, smoke, readiness scoring을 한 번에 수행합니다.",
            windows_only=True,
            notes="Scenario run 직후 첫 번째 검증 증빙을 수집할 때 사용합니다.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="증빙 실행 식별자입니다.",
                    placeholder="20260308_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="담당자",
                    default="DEV2",
                    help="smoke/status 보고서에 기록되는 owner 태그입니다.",
                    placeholder="DEV2",
                    required=True,
                ),
            ),
        ),
    ],
    "Runtime Support": [
        PaletteCommand(
            command_id="inspect.environment_doctor",
            title="환경 점검",
            command="doctor",
            summary="CANoe COM 연결, measurement 상태, 핵심 sysvar 접근성을 확인합니다.",
            windows_only=True,
            notes="Scenario run이나 Verify quick 전에 먼저 확인하십시오.",
        ),
        PaletteCommand(
            command_id="operate.measure_status",
            title="측정 상태",
            command="canoe measure-status",
            summary="현재 CANoe measurement 상태를 읽습니다.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="operate.measure_start",
            title="측정 시작",
            command="canoe measure-start",
            summary="COM 경유로 CANoe measurement를 시작합니다.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="operate.measure_stop",
            title="측정 중지",
            command="canoe measure-stop",
            summary="COM 경유로 CANoe measurement를 중지합니다.",
            windows_only=True,
        ),
        PaletteCommand(
            command_id="verify.precheck_batch",
            title="사전 점검 배치",
            command="start precheck",
            summary="gate, prepare, smoke, readiness status를 한 번에 수행합니다.",
            windows_only=True,
            notes="개발 상태를 빠르게 훑고 검증 진입 가능 여부를 판단할 때 사용합니다.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="증빙 실행 식별자입니다. 일반적으로 YYYYMMDD_HHMM 형식을 사용합니다.",
                    placeholder="20260308_0900",
                    required=True,
                ),
                CommandParam(
                    key="owner",
                    flag="--owner",
                    label="담당자",
                    default="DEV2",
                    help="보고서에 기록되는 운영자 태그입니다.",
                    placeholder="DEV2",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="verify.run_readiness_status",
            title="증빙 준비 상태",
            command="verify status --run-id 20260308_0900",
            base_command="verify status",
            summary="raw evidence, marker, score 준비 상태를 점검합니다.",
            params=(
                CommandParam(
                    key="run_id",
                    flag="--run-id",
                    label="Run ID",
                    default="{run_id}",
                    help="canoe/logging/evidence 아래에서 확인할 실행 폴더입니다.",
                    placeholder="20260308_0900",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="operate.guided",
            title="가이드 모드",
            command="start guided",
            summary="Textual TUI를 쓰기 어려울 때 사용하는 순차형 fallback입니다.",
            notes="터미널 호환성 문제가 있을 때만 사용하십시오.",
        ),
    ],
    "System Access": [
        PaletteCommand(
            command_id="inspect.read_system_variable",
            title="시스템 변수 조회",
            command="capl sysvar-get --namespace Core --var failSafeMode",
            base_command="capl sysvar-get",
            summary="CAPL/COM 경유로 system variable 값을 읽습니다.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="네임스페이스",
                    default="Core",
                    help="조회할 system variable namespace입니다.",
                    placeholder="Core",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="변수",
                    default="failSafeMode",
                    help="조회할 system variable 이름입니다.",
                    placeholder="failSafeMode",
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.write_system_variable",
            title="시스템 변수 쓰기",
            command="capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int",
            base_command="capl sysvar-set",
            summary="CAPL/COM 경유로 system variable 값을 설정합니다.",
            windows_only=True,
            params=(
                CommandParam(
                    key="namespace",
                    flag="--namespace",
                    label="네임스페이스",
                    default="Test",
                    help="설정할 system variable namespace입니다.",
                    placeholder="Test",
                    required=True,
                ),
                CommandParam(
                    key="var",
                    flag="--var",
                    label="변수",
                    default="scenarioCommand",
                    help="설정할 system variable 이름입니다.",
                    placeholder="scenarioCommand",
                    required=True,
                ),
                CommandParam(
                    key="value",
                    flag="--value",
                    label="값",
                    default="4",
                    help="설정할 값입니다.",
                    placeholder="4",
                    required=True,
                ),
                CommandParam(
                    key="value_type",
                    flag="--value-type",
                    label="값 형식",
                    default="int",
                    help="int, float, bool, string 중 하나를 사용합니다.",
                    placeholder="int",
                    choices=("int", "float", "bool", "string"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="inspect.command_contract",
            title="명령 계약 보기",
            command="contract",
            summary="지원하는 공개 명령과 compatibility alias를 확인합니다.",
        ),
    ],
    "Packaging": [
        PaletteCommand(
            command_id="package.portable_bundle",
            title="포터블 번들",
            command="package bundle-portable --mode onefolder",
            base_command="package bundle-portable",
            summary="배포용 portable ZIP 산출물을 생성합니다.",
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="패키징 모드",
                    default="onefolder",
                    help="기본 배포는 onefolder, 단일 실행파일 테스트는 onefile을 사용합니다.",
                    placeholder="onefolder",
                    choices=("onefolder", "onefile"),
                    required=True,
                ),
            ),
        ),
        PaletteCommand(
            command_id="package.windows_exe",
            title="윈도우 실행파일",
            command="package build-exe --mode onefolder",
            base_command="package build-exe",
            summary="Windows executable 산출물을 생성합니다.",
            windows_only=True,
            params=(
                CommandParam(
                    key="mode",
                    flag="--mode",
                    label="빌드 모드",
                    default="onefolder",
                    help="운영 handoff는 onefolder, 단일 exe 검증은 onefile을 사용합니다.",
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
        ("/history", "최근 shell 명령 이력을 표시합니다."),
        ("/repeat 1", "가장 최근 shell 명령을 다시 실행합니다."),
        ("/exit", "shell을 종료합니다."),
    ]
    return groups

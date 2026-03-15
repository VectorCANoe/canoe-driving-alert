"""Operator-facing text helpers for the public CANoe Test Verification Console surface."""

from __future__ import annotations

from cliops.command_catalog import PaletteCommand


GROUP_LABELS: dict[str, str] = {
    "Primary Workflow": "Verify / 핵심 검증",
    "Runtime Support": "Runtime / CANoe 제어",
    "System Access": "Inspect / 상태·Contracts 확인",
    "Packaging": "Package / 산출물 관리",
}


def group_surface_label(group_name: str) -> str:
    return GROUP_LABELS.get(group_name, group_name)


def runtime_badge(command: PaletteCommand) -> str:
    return "Windows 전용" if command.windows_only else "모든 플랫폼"


def pin_status(is_pinned: bool) -> str:
    return "고정됨" if is_pinned else "고정 안 됨"


def pin_button_label(is_pinned: bool) -> str:
    return "작업 고정 해제" if is_pinned else "작업 고정"


def execute_hint(has_params: bool) -> str:
    if has_params:
        return (
            "작업을 선택한 뒤 필요한 값을 입력하고, 지금 실행 또는 Ctrl+R로 시작하십시오. "
            "실행 중에는 자동으로 로그 화면으로 이동합니다."
        )
    return (
        "이 작업은 추가 입력이 필요 없습니다. 지금 실행 또는 Ctrl+R로 시작하십시오. "
        "실행 중에는 자동으로 로그 화면으로 이동합니다."
    )


def preview_empty() -> str:
    return "추가 입력이 없습니다."


def no_selected_command() -> str:
    return "선택된 작업이 없습니다."


def no_visible_command() -> str:
    return "이 범주에는 아직 노출된 작업이 없습니다."


def recommended_next(command: PaletteCommand) -> str:
    if command.next_step:
        return command.next_step
    if command.command_id == "verify.all_gates":
        return "PASS면 Scenario run으로 이어서 진행하십시오."
    if command.command_id == "operate.scenario_trigger":
        return "ACK가 확인되면 Verify quick으로 이어서 진행하십시오."
    if command.command_id == "verify.quick_verify":
        return "결과와 증빙을 확인한 뒤 05/06/07 문서에 반영하십시오."
    if command.command_id == "operate.measure_status":
        return "stopped 상태면 먼저 측정을 시작하십시오."
    if command.command_id == "operate.measure_start":
        return "measurement가 running이면 Scenario run 또는 Doctor를 실행하십시오."
    if command.command_id == "verify.precheck_batch":
        return "PASS면 본 검증 시나리오로 진입하십시오."
    if command.command_id == "verify.run_readiness_status":
        return "준비되지 않은 항목을 확인하고 증빙을 보강하십시오."
    if command.command_id == "inspect.environment_doctor":
        return "점검이 정상이면 measurement와 Scenario run 흐름으로 이어서 진행하십시오."
    if command.command_id == "package.portable_bundle":
        return "생성된 산출물 경로를 확인하고 전달용 패키지를 점검하십시오."
    return "결과와 다음 작업 지시를 확인한 뒤 이어서 진행하십시오."


def _section(title: str, values: tuple[str, ...] | list[str]) -> list[str]:
    if not values:
        return []
    lines = [f"[cyan]{title}[/cyan]"]
    lines.extend(f"  - {item}" for item in values if item)
    lines.append("")
    return lines


def command_info_body(
    command: PaletteCommand,
    runtime_text: str,
    pin_text: str,
    recommended: str,
) -> str:
    body: list[str] = [
        f"[bold]{command.title}[/bold]",
        "",
        command.summary,
        "",
        f"[cyan]실행 명령[/cyan]",
        f"  - python scripts/run.py {command.command}",
        f"[cyan]사용 환경[/cyan]",
        f"  - {runtime_text}",
        f"[cyan]작업 고정[/cyan]",
        f"  - {pin_text}",
        "",
    ]
    body.extend(_section("사용 시점", list(command.use_when)))
    body.extend(_section("성공 판단", list(command.success_signals)))
    body.extend(_section("생성 산출물", list(command.expected_outputs)))
    if command.notes:
        body.extend(_section("운영 메모", [command.notes]))
    body.extend(_section("점검 포인트", list(command.failure_focus)))
    body.extend(_section("다음 단계", [recommended]))
    return "\n".join(line for line in body if line is not None)


LOG_FILTER_LABELS: dict[str, str] = {
    "ALL": "F1 전체",
    "WARN": "F2 경고",
    "FAIL": "F3 실패",
    "VERIFY": "F4 Verify",
    "CANOE": "F5 CANoe",
}


def log_filter_label(filter_name: str) -> str:
    return LOG_FILTER_LABELS[filter_name]


def log_filter_status(filter_name: str, visible: int, total: int) -> str:
    return f"필터: {filter_name} | 표시 {visible}/{total} | Ctrl+O=증빙 열기 | Ctrl+Y=경로 복사"


def live_runtime_default_stage() -> str:
    return "대기"


def live_runtime_default_line() -> str:
    return "현재 실행 중인 작업이 없습니다."


def live_runtime_summary(stage: str, last_line: str, last_output: str | None) -> str:
    lines = [
        f"단계: {stage}",
        f"최근 로그: {last_line[:120]}",
    ]
    if last_output:
        lines.append(f"산출물: {last_output[:120]}")
    else:
        lines.append("산출물: 아직 확인되지 않았습니다.")
    return "\n".join(lines)


def no_artifact_path() -> str:
    return "최근 결과에 연결된 증빙 경로가 없습니다."


def artifact_opened(path: str) -> str:
    return f"[green]증빙 열기[/] {path}"


def artifact_open_failed(ex: Exception) -> str:
    return f"[bold red]증빙 열기 실패[/]: {ex}"


def artifact_copied(path: str) -> str:
    return f"[green]증빙 경로 복사[/] {path}"


def recent_selection_insight(title: str, status: str, duration_ms: int, detail: str) -> str:
    return (
        f"단계: 최근 실행 선택\n"
        f"선택 작업: {title} [{status}] {duration_ms}ms\n"
        f"다음 단계: 최근 실행 목록에서 Enter로 다시 실행하십시오.\n"
        f"상세: {detail}"
    )


def no_pin_target() -> str:
    return "고정할 작업이 선택되지 않았습니다."


def pin_removed(title: str) -> str:
    return f"[yellow]작업 고정 해제[/] {title}"


def pin_added(title: str) -> str:
    return f"[green]작업 고정[/] {title}"


def no_recent_rerun() -> str:
    return "다시 실행할 최근 작업이 없습니다."


def followup_hint(status: str) -> str:
    if status == "FAIL":
        return "실행이 실패했습니다. Results에서 판정과 근거를 확인하고, 이어서 Logs와 CANoe 상태를 확인하십시오."
    if status == "WARN":
        return "경고와 함께 실행이 끝났습니다. Results에서 주의 항목과 다음 단계를 확인하십시오."
    return "이제 Results에서 판정과 증빙을 확인하고, 필요하면 CANoe 상태를 함께 점검하십시오."

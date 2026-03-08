"""Operator-facing TUI text helpers.

Keep the SDV Operator surface text in one place so UI wording can evolve
without adding more string noise into the Textual app logic.
"""

from __future__ import annotations

from cliops.command_catalog import PaletteCommand


GROUP_LABELS: dict[str, str] = {
    "Primary Workflow": "핵심",
    "Runtime Support": "런타임",
    "System Access": "점검",
    "Packaging": "패키징",
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
    if command.command_id == "verify.all_gates":
        return "PASS면 바로 Scenario run으로 이동하십시오."
    if command.command_id == "operate.scenario_trigger":
        return "ack를 받았으면 바로 Verify quick으로 이동하십시오."
    if command.command_id == "verify.quick_verify":
        return "PASS면 생성된 증빙을 05/06/07에 연결하십시오."
    if command.title == "Measurement status":
        return "stopped면 먼저 Measurement start를 실행하십시오."
    if command.title == "Measurement start":
        return "start 후 Scenario run 또는 Precheck batch로 진행하십시오."
    if command.title == "Scenario trigger":
        return "시나리오 ack 후 Run readiness status 또는 Quick verify로 진행하십시오."
    if command.title == "Precheck batch":
        return "PASS면 캡처/증빙 수집 단계로 이동하십시오."
    if command.title == "Quick verify":
        return "PASS면 결과를 05/06/07 증빙에 연결하십시오."
    if command.title == "Environment doctor":
        return "모든 검사가 정상이면 measurement 또는 scenario 단계로 진행하십시오."
    if command.title == "Portable bundle":
        return "운영 흐름이 안정된 뒤 패키징 단계로 이동하십시오."
    return "실행 후 아래 로그를 확인하고 다음 검증 단계로 이동하십시오."


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
        lines.append("산출물: 아직 감지되지 않았습니다")
    return "\n".join(lines)


def no_artifact_path() -> str:
    return "최근 결과에 열 수 있는 증빙 경로가 없습니다."


def artifact_opened(path: str) -> str:
    return f"[green]증빙 열기[/] {path}"


def artifact_open_failed(ex: Exception) -> str:
    return f"[bold red]증빙 열기 실패[/]: {ex}"


def artifact_copied(path: str) -> str:
    return f"[green]증빙 경로 복사[/] {path}"


def recent_selection_insight(title: str, status: str, duration_ms: int, detail: str) -> str:
    return (
        f"단계: 최근 실행 선택\n"
        f"병목: {title} [{status}] {duration_ms}ms\n"
        f"다음 액션: 최근 실행 항목에서 Enter로 다시 실행하십시오.\n"
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
        return "실행이 실패했습니다. 결과 화면에서 판정을 먼저 확인하고, 이어서 로그와 COM 상태를 검토하십시오."
    if status == "WARN":
        return "경고와 함께 실행이 끝났습니다. 결과 화면에서 병목과 다음 액션을 확인하십시오."
    return "이제 결과 화면에서 판정, 증빙, COM 상태를 확인하십시오."

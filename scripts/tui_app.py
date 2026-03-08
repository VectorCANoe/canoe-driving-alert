"""Textual TUI frontend for the SDV CANoe operator CLI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from cliops.command_catalog import (
    PRODUCT_COMMAND_GROUPS,
    PaletteCommand,
    build_command_index,
    build_command_tokens,
    resolve_command_defaults,
)
from cliops.platform_caps import canoe_runtime_check, platform_label
from cliops.operator_result import LAST_OPERATOR_RESULT_PATH
from cliops.tui_text import (
    artifact_copied,
    artifact_open_failed,
    artifact_opened,
    command_info_body,
    execute_hint,
    followup_hint,
    group_surface_label,
    live_runtime_default_line,
    live_runtime_default_stage,
    live_runtime_summary,
    log_filter_label,
    log_filter_status,
    no_artifact_path,
    no_pin_target,
    no_recent_rerun,
    no_selected_command,
    no_visible_command,
    pin_added,
    pin_button_label,
    pin_removed,
    pin_status,
    preview_empty,
    recent_selection_insight,
    recommended_next,
    runtime_badge,
)
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, OptionList, RichLog, Static
from textual.widgets.option_list import Option
from textual.css.query import NoMatches
from rich.markup import escape


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts" / "run.py"
FORM_SLOTS = 4
STATE_FILE = ROOT / "canoe" / "tmp" / "reports" / "verification" / "tui_operator_state.json"
BASE_GROUP_NAMES = list(PRODUCT_COMMAND_GROUPS.keys())
COMMAND_INDEX = build_command_index()


class SdvTuiApp(App[None]):
    CSS = """
    Screen {
        background: #11161c;
        color: #d8dee9;
    }

    #hero {
        height: 3;
        padding: 1 2;
        margin: 1 1 0 1;
        background: #1b2635;
        color: #f0f4f8;
        border: round #4ea1ff;
        text-style: bold;
    }

    #runtime {
        height: 3;
        padding: 1 2;
        margin: 0 1 1 1;
        background: #17202b;
        border: round #33536f;
        color: #a9bed1;
    }

    #shell-main {
        height: 1fr;
        margin: 0 1 1 1;
    }

    #sidebar {
        width: 22;
        padding: 1;
        margin-right: 1;
        background: #121920;
        border: round #2d3e50;
    }

    .nav-button {
        width: 1fr;
        margin-bottom: 1;
    }

    #content {
        width: 1fr;
    }

    .page {
        height: 1fr;
    }

    #page-home {
        padding: 1;
        background: #121920;
        border: round #2d3e50;
    }

    #home-body {
        padding: 1 1 0 1;
        background: #17202b;
        border: round #33536f;
        min-height: 6;
    }

    #home-summary {
        padding: 1;
        margin-top: 1;
        background: #17202b;
        border: round #33536f;
        min-height: 7;
    }

    #home-core-flow {
        height: 12;
        margin-top: 1;
    }

    .home-task-card {
        width: 1fr;
        padding: 1;
        margin-right: 1;
        background: #162130;
        border: round #33536f;
    }

    .home-task-card:last-child {
        margin-right: 0;
    }

    .home-task-title {
        color: #f6c177;
        text-style: bold;
        margin-bottom: 1;
    }

    .home-task-copy {
        color: #d7e7f2;
        height: 1fr;
    }

    .quick-button {
        margin-top: 1;
        width: 1fr;
    }

    #home-recent {
        padding: 1;
        margin-top: 1;
        background: #17202b;
        border: round #33536f;
        min-height: 8;
    }

    #summary-strip {
        height: 11;
        margin-bottom: 1;
    }

    #status-strip {
        height: 9;
        margin-bottom: 1;
    }

    .summary-card {
        padding: 1;
        margin-right: 1;
        background: #121920;
        border: round #2d3e50;
    }

    #favorites-card {
        width: 28;
    }

    #recent-card {
        width: 1fr;
    }

    #insight-card {
        width: 1fr;
    }

    #result-card {
        width: 1fr;
        margin-right: 0;
    }

    #recent-list {
        height: 1fr;
    }

    #readiness-card {
        width: 1fr;
    }

    #batch-card {
        width: 1fr;
    }

    #com-card {
        width: 40;
    }

    #timeline-card {
        width: 1fr;
        margin-right: 0;
    }

    .summary-title {
        color: #f6c177;
        text-style: bold;
        margin-bottom: 1;
    }

    #workspace {
        height: 1fr;
    }

    #execute-group-strip {
        height: 3;
        margin-bottom: 1;
    }

    .group-button {
        margin-right: 1;
        width: 1fr;
    }

    .pane {
        margin-right: 1;
        padding: 1;
        background: #121920;
        border: round #2d3e50;
    }

    .pane-title {
        margin-bottom: 1;
        color: #f6c177;
        text-style: bold;
    }

    #groups-pane {
        width: 22;
    }

    #commands-pane {
        width: 32;
    }

    #details-pane {
        width: 1fr;
        margin-right: 0;
    }

    #details-body {
        padding: 0 1;
        margin-bottom: 1;
    }

    #form-body {
        margin-top: 1;
    }

    .form-row {
        margin-bottom: 1;
    }

    .field-label {
        color: #d7e7f2;
        text-style: bold;
    }

    .field-help {
        color: #8ba4b8;
        height: auto;
        margin-top: 0;
    }

    .hidden {
        display: none;
    }

    #preview-body {
        margin-top: 1;
        padding: 1;
        background: #17202b;
        border: round #33536f;
        color: #d7e7f2;
        height: 4;
    }

    #execute-hint {
        margin-top: 1;
        padding: 1;
        color: #8ba4b8;
        background: #17202b;
        border: round #33536f;
        height: 3;
    }

    #actions {
        margin-top: 1;
        height: 3;
    }

    #actions Button {
        margin-right: 1;
    }

    #log-pane {
        height: 1fr;
        padding: 1;
        background: #0f151b;
        border: round #2d3e50;
    }

    #log-controls {
        height: 3;
        margin-bottom: 1;
    }

    #log-summary {
        margin-bottom: 1;
        padding: 1;
        background: #17202b;
        border: round #33536f;
        color: #d7e7f2;
        height: 5;
    }

    .filter-button {
        margin-right: 1;
        min-width: 9;
    }

    #log-filter-status {
        width: 1fr;
        padding-top: 1;
        color: #8ba4b8;
    }

    #log {
        height: 1fr;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+r", "run_selected", "Run"),
        ("ctrl+p", "toggle_pin", "Pin"),
        ("ctrl+x", "rerun_latest", "Rerun latest"),
        ("ctrl+b", "focus_favorites", "Favorites"),
        ("ctrl+n", "focus_recent", "Recent"),
        ("ctrl+g", "focus_navigation", "Navigation"),
        ("ctrl+t", "focus_commands", "Commands"),
        ("ctrl+f", "focus_form", "Form"),
        ("ctrl+l", "focus_log", "Log"),
        ("f1", "set_log_filter_all", "Log all"),
        ("f2", "set_log_filter_warn", "Log warn"),
        ("f3", "set_log_filter_fail", "Log fail"),
        ("f4", "set_log_filter_verify", "Log verify"),
        ("f5", "set_log_filter_canoe", "Log canoe"),
        ("ctrl+o", "open_artifact", "Open artifact"),
        ("ctrl+y", "copy_artifact", "Copy artifact"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.state = self._load_state()
        self.group_names = self._build_group_names()
        self.active_group_index = 0
        self.active_command_index = 0
        self.log_filter = "ALL"
        self.log_buffer: list[dict[str, str]] = []
        self.current_page = "home"
        self._suspend_option_events = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            "SDV Operator Console",
            id="hero",
        )
        runtime = canoe_runtime_check()
        runtime_text = (
            f"호스트: {platform_label()} | CANoe 런타임: {'ready' if runtime.available else 'limited'} | "
            "실행: Ctrl+R | 최근 실행: Ctrl+N | 로그: Ctrl+L | 필터: F1..F5 | 증빙: Ctrl+O/Ctrl+Y | 종료: q"
        )
        if not runtime.available:
            runtime_text += f"\n제약: {runtime.detail}"
        yield Static(runtime_text, id="runtime")
        with Horizontal(id="shell-main"):
            with Vertical(id="sidebar"):
                yield Button("홈", id="nav-home", classes="nav-button", variant="primary")
                yield Button("실행", id="nav-execute", classes="nav-button")
                yield Button("결과", id="nav-results", classes="nav-button")
                yield Button("로그", id="nav-logs", classes="nav-button")
            with Vertical(id="content"):
                with Vertical(id="page-home", classes="page"):
                    yield Static(
                        "Verification Console\n\n"
                        "사용자 표면은 단순하게, 검증 엔진은 내부에서 복잡하게 유지합니다.\n"
                        "핵심 흐름은 Gate all -> Scenario run -> Verify quick 순서입니다.\n"
                        "CANoe Panel은 제품 조작 UI이고, 이 콘솔은 실행·증빙·검토를 담당합니다.",
                        id="home-body",
                    )
                    yield Static(id="home-summary")
                    with Horizontal(id="home-core-flow"):
                        with Vertical(classes="home-task-card"):
                            yield Static("1) Gate all", classes="home-task-title")
                            yield Static(
                                "시나리오 실행이나 증빙 수집 전에 DBC/CAPL/문서 준비 상태를 먼저 점검합니다.",
                                classes="home-task-copy",
                            )
                            yield Button("Gate all 열기", id="home-gate", classes="quick-button", variant="success")
                        with Vertical(classes="home-task-card"):
                            yield Static("2) Scenario run", classes="home-task-title")
                            yield Static(
                                "CANoe COM으로 시나리오를 주입하고 Test sysvar ack가 돌아오는지 확인합니다.",
                                classes="home-task-copy",
                            )
                            yield Button("Scenario run 열기", id="home-scenario", classes="quick-button")
                        with Vertical(classes="home-task-card"):
                            yield Static("3) Verify quick", classes="home-task-title")
                            yield Static(
                                "준비 상태와 증빙 상태를 생성한 뒤 PASS/WARN/FAIL과 증빙 경로를 함께 검토합니다.",
                                classes="home-task-copy",
                            )
                            yield Button("Verify quick 열기", id="home-verify", classes="quick-button", variant="primary")
                    yield Static(id="home-recent")
                with Horizontal(id="page-execute", classes="page hidden"):
                    with Vertical(id="commands-pane", classes="pane"):
                        yield Static("1) 작업 범주 선택", classes="pane-title")
                        with Horizontal(id="execute-group-strip"):
                            yield Button("핵심", id="group-primary", classes="group-button", variant="primary")
                            yield Button("런타임", id="group-runtime", classes="group-button")
                            yield Button("점검", id="group-inspect", classes="group-button")
                            yield Button("패키징", id="group-package", classes="group-button")
                        yield Static(id="commands-title", classes="pane-title")
                        yield OptionList(id="commands")
                    with Vertical(id="details-pane", classes="pane"):
                        yield Static("2) 작업 정보", classes="pane-title")
                        yield Static(id="details-body")
                        yield Static("3) 빠른 입력", classes="pane-title")
                        with Vertical(id="form-body"):
                            for index in range(FORM_SLOTS):
                                with Vertical(id=f"field-row-{index}", classes="form-row hidden"):
                                    yield Static(id=f"field-label-{index}", classes="field-label")
                                    yield Input(id=f"field-input-{index}")
                                    yield Static(id=f"field-help-{index}", classes="field-help")
                        yield Static(id="preview-body")
                    with Horizontal(id="actions"):
                        yield Button("지금 실행", id="run-button", variant="success")
                        yield Button("작업 고정", id="pin-button")
                        yield Button("기본값 복원", id="reset-button")
                    yield Static(
                        "실행을 시작하면 자동으로 로그 화면으로 이동합니다. 종료 후 결과 화면에서 판정과 증빙을 확인하십시오.",
                        id="execute-hint",
                    )
                with Vertical(id="page-results", classes="page hidden"):
                    with Horizontal(id="summary-strip"):
                        with Vertical(id="favorites-card", classes="summary-card"):
                            yield Static("고정 작업", classes="summary-title")
                            yield Static(id="favorites-body")
                        with Vertical(id="recent-card", classes="summary-card"):
                            yield Static("최근 실행", classes="summary-title")
                            yield OptionList(id="recent-list")
                        with Vertical(id="insight-card", classes="summary-card"):
                            yield Static("실행 인사이트", classes="summary-title")
                            yield Static(id="insight-body")
                        with Vertical(id="result-card", classes="summary-card"):
                            yield Static("최근 결과", classes="summary-title")
                            yield Static(id="result-body")
                    with Horizontal(id="status-strip"):
                        with Vertical(id="readiness-card", classes="summary-card"):
                            yield Static("계층 준비 상태", classes="summary-title")
                            yield Static(id="readiness-body")
                        with Vertical(id="batch-card", classes="summary-card"):
                            yield Static("배치 스냅샷", classes="summary-title")
                            yield Static(id="batch-body")
                        with Vertical(id="com-card", classes="summary-card"):
                            yield Static("COM 런타임", classes="summary-title")
                            yield Static(id="com-body")
                        with Vertical(id="timeline-card", classes="summary-card"):
                            yield Static("실행 타임라인", classes="summary-title")
                            yield Static(id="timeline-body")
                with Vertical(id="page-logs", classes="page hidden"):
                    with Vertical(id="log-pane"):
                        yield Static("실행 로그", classes="pane-title")
                        yield Static(id="log-summary")
                        with Horizontal(id="log-controls"):
                            yield Button("F1 전체", id="log-filter-all", classes="filter-button")
                            yield Button("F2 경고", id="log-filter-warn", classes="filter-button")
                            yield Button("F3 실패", id="log-filter-fail", classes="filter-button")
                            yield Button("F4 Verify", id="log-filter-verify", classes="filter-button")
                            yield Button("F5 CANoe", id="log-filter-canoe", classes="filter-button")
                            yield Static(id="log-filter-status")
                        yield RichLog(id="log", wrap=True, highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = "SDV Operator Console"
        self.sub_title = "검증 운영 콘솔"
        self.active_group_index = self.group_names.index("Primary Workflow")
        self._refresh_commands(self.active_group_index)
        self._show_page("home")
        self._refresh_summary_cards()
        self._refresh_log_summary()
        self._write_log("[bold cyan]TUI 준비 완료[/]  작업을 고르고 필요한 값을 입력한 뒤 [bold]Ctrl+R[/]로 실행하십시오.")

    def _show_page(self, page_name: str) -> None:
        self.current_page = page_name
        pages = ("home", "execute", "results", "logs")
        for item in pages:
            page = self.query_one(f"#page-{item}")
            if item == page_name:
                page.remove_class("hidden")
            else:
                page.add_class("hidden")
        active_nav = {
            "home": "nav-home",
            "execute": "nav-execute",
            "results": "nav-results",
            "logs": "nav-logs",
        }[page_name]
        for button_id in ("nav-home", "nav-execute", "nav-results", "nav-logs"):
            button = self.query_one(f"#{button_id}", Button)
            button.variant = "primary" if button_id == active_nav else "default"
        self._refresh_execute_group_buttons()

    def _set_command_group(self, group_name: str) -> None:
        if group_name not in self.group_names:
            return
        self.active_group_index = self.group_names.index(group_name)
        self._refresh_commands(self.active_group_index)
        self.query_one("#commands-title", Static).update(f"2) 작업 선택  |  {group_name}")
        self._show_page("execute")
        self._refresh_execute_group_buttons()
        self.query_one("#commands", OptionList).focus()

    def _refresh_execute_group_buttons(self) -> None:
        mapping = {
            "Primary Workflow": "group-primary",
            "Runtime Support": "group-runtime",
            "System Access": "group-inspect",
            "Packaging": "group-package",
        }
        active = mapping.get(self._active_group_name(), "group-primary")
        for button_id in mapping.values():
            try:
                button = self.query_one(f"#{button_id}", Button)
            except Exception:
                continue
            button.variant = "primary" if button_id == active else "default"

    def _select_command_by_id(self, command_id: str) -> None:
        commands = self._active_group_commands()
        for index, command in enumerate(commands):
            if command.command_id == command_id:
                self.active_command_index = index
                command_list = self.query_one("#commands", OptionList)
                self._suspend_option_events = True
                command_list.highlighted = index
                self._suspend_option_events = False
                self._update_command_view(command)
                return

    def _open_core_task(self, command_id: str, *, focus: str) -> None:
        self._set_command_group("Primary Workflow")
        self._select_command_by_id(command_id)
        self._show_page("execute")
        self._refresh_execute_group_buttons()
        if focus == "form":
            self.action_focus_form()
        else:
            self.query_one("#run-button", Button).focus()

    def _refresh_home_summary(self) -> None:
        last_result = self.state.get("last_result", {})
        insight = self.state.get("last_insight", {})
        timeline = self.state.get("timeline", {})
        status = str(last_result.get("status", "IDLE")) if isinstance(last_result, dict) else "IDLE"
        title = str(last_result.get("title", "아직 실행 기록이 없습니다")) if isinstance(last_result, dict) else "아직 실행 기록이 없습니다"
        detail = str(last_result.get("detail", "작업을 선택하고 실행하면 이 카드가 채워집니다.")) if isinstance(last_result, dict) else "작업을 선택하고 실행하면 이 카드가 채워집니다."
        bottleneck = str(insight.get("bottleneck", "아직 실행 인사이트가 없습니다.")) if isinstance(insight, dict) else "아직 실행 인사이트가 없습니다."
        next_action = str(insight.get("next_action", "먼저 Gate all을 실행하십시오.")) if isinstance(insight, dict) else "먼저 Gate all을 실행하십시오."
        stage = str(insight.get("stage", "대기")) if isinstance(insight, dict) else "대기"
        gate = str(timeline.get("gate", "IDLE")) if isinstance(timeline, dict) else "IDLE"
        scenario = str(timeline.get("scenario", "IDLE")) if isinstance(timeline, dict) else "IDLE"
        verify = str(timeline.get("verify", "IDLE")) if isinstance(timeline, dict) else "IDLE"
        recent = self._recent_rows()
        self.query_one(
            "#home-summary", Static
        ).update(
            f"단계: {stage}\n"
            f"최근 결과: {status} | {title}\n"
            f"타임라인: Gate={gate} / Scenario={scenario} / Verify={verify}\n"
            f"병목: {bottleneck}\n"
            f"다음 액션: {next_action}"
        )
        recent_lines = ["최근 실행 요약"]
        if recent:
            for item in recent[:3]:
                recent_lines.append(f"- {self._recent_entry_label(item)}")
        else:
            recent_lines.append("- 아직 실행 기록이 없습니다. Gate all부터 시작하십시오.")
        recent_lines.extend(["", f"최근 상세: {detail}", "", "자세한 판정·증빙·COM 상태는 결과 화면에서 확인하십시오."])
        self.query_one("#home-recent", Static).update("\n".join(recent_lines))

    def _load_state(self) -> dict[str, object]:
        default_state: dict[str, object] = {
            "pinned": [],
            "recent": [],
            "last_insight": {
                "stage": "대기",
                "bottleneck": "아직 실행 인사이트가 없습니다.",
                "next_action": "먼저 Gate all을 실행하십시오.",
            },
            "last_result": {
                "status": "IDLE",
                "title": "아직 실행 기록이 없습니다",
                "detail": "작업을 선택하고 실행하면 이 카드가 채워집니다.",
                "ts": "",
                "related_logs": [],
            },
            "timeline": {
                "gate": "IDLE",
                "scenario": "IDLE",
                "verify": "IDLE",
                "current": "대기",
                "gate_ms": 0,
                "scenario_ms": 0,
                "verify_ms": 0,
            },
            "live_runtime": {
                "stage": "대기",
                "last_line": "현재 실행 중인 작업이 없습니다.",
                "outputs": [],
            },
        }
        if not STATE_FILE.exists():
            return default_state
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return default_state
        if not isinstance(data, dict):
            return default_state
        default_state.update({k: v for k, v in data.items() if k in default_state})
        return default_state

    def _save_state(self) -> None:
        try:
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            STATE_FILE.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def _build_group_names(self) -> list[str]:
        return list(BASE_GROUP_NAMES)

    def _favorite_commands(self) -> list[PaletteCommand]:
        favorite_ids = [item for item in self.state.get("pinned", []) if isinstance(item, str)]
        return [COMMAND_INDEX[item] for item in favorite_ids if item in COMMAND_INDEX]

    def _current_command_is_pinned(self) -> bool:
        command = self._selected_command()
        if command is None:
            return False
        return command.command_id in self.state.get("pinned", [])

    def _rebuild_groups(self, preferred_group: str | None = None) -> None:
        self.group_names = self._build_group_names()
        target_group = preferred_group if preferred_group in self.group_names else "Primary Workflow"
        target_index = self.group_names.index(target_group)
        self._refresh_commands(target_index)

    def _refresh_summary_cards(self) -> None:
        favorites = self._favorite_commands()
        if favorites:
            favorite_lines = [f"{idx + 1}. {command.title}" for idx, command in enumerate(favorites[:5])]
            favorite_lines.append("")
            favorite_lines.append("선택한 작업에서 Ctrl+P로 고정/해제를 전환하십시오.")
        else:
            favorite_lines = ["아직 고정된 작업이 없습니다.", "작업을 선택한 뒤 Ctrl+P로 고정하십시오."]
        self.query_one("#favorites-body", Static).update("\n".join(favorite_lines))

        recent_rows = self._recent_rows()
        recent_list = self.query_one("#recent-list", OptionList)
        previous_index = self._selected_option_index(recent_list)
        recent_list.clear_options()
        if recent_rows:
            recent_list.add_options([Option(self._recent_entry_label(item)) for item in recent_rows])
            recent_list.highlighted = min(previous_index, len(recent_rows) - 1)
        else:
            recent_list.add_options([Option("아직 최근 실행 기록이 없습니다.")])
            recent_list.highlighted = 0

        last_insight = self.state.get("last_insight", {})
        timeline = self.state.get("timeline", {})
        if isinstance(last_insight, dict):
            stage = str(last_insight.get("stage", "대기"))
            bottleneck = str(last_insight.get("bottleneck", "아직 실행 인사이트가 없습니다."))
            next_action = str(last_insight.get("next_action", "먼저 Gate all을 실행하십시오."))
        else:
            stage, bottleneck, next_action = "대기", "아직 실행 인사이트가 없습니다.", "먼저 Gate all을 실행하십시오."
        if isinstance(timeline, dict):
            gate_state = str(timeline.get("gate", "IDLE"))
            scenario_state = str(timeline.get("scenario", "IDLE"))
            verify_state = str(timeline.get("verify", "IDLE"))
        else:
            gate_state = scenario_state = verify_state = "IDLE"
        self.query_one("#insight-body", Static).update(
            "\n".join(
                [
                    f"현재 단계: {stage}",
                    f"3단계 흐름: Gate={gate_state} / Scenario={scenario_state} / Verify={verify_state}",
                    f"직접 근거: {bottleneck}",
                    f"다음 단계: {next_action}",
                ]
            )
        )
        self.query_one("#readiness-body", Static).update(self._summarize_tier_readiness())
        self.query_one("#batch-body", Static).update(self._summarize_batch_snapshot())
        self.query_one("#com-body", Static).update(self._summarize_com_snapshot())
        self.query_one("#timeline-body", Static).update(self._summarize_timeline())

        last_result = self.state.get("last_result", {})
        if isinstance(last_result, dict):
            status = str(last_result.get("status", "IDLE"))
            title = str(last_result.get("title", "아직 실행 기록이 없습니다"))
            detail = str(last_result.get("detail", "작업을 선택하고 실행하면 이 카드가 채워집니다."))
            ts = str(last_result.get("ts", ""))
            artifacts = last_result.get("artifacts", [])
            related_logs = last_result.get("related_logs", [])
        else:
            status, title, detail, ts, artifacts, related_logs = (
                "IDLE",
                "아직 실행 기록이 없습니다",
                "작업을 선택하고 실행하면 이 카드가 채워집니다.",
                "",
                [],
                [],
            )
        result_lines = [
            f"판정: {status}",
            f"작업: {title}",
            f"직접 사유: {detail}",
            f"다음 단계: {next_action}",
        ]
        if isinstance(related_logs, list) and related_logs:
            result_lines.append("")
            result_lines.append("근거 로그:")
            result_lines.extend(str(item) for item in related_logs[:3])
        if isinstance(artifacts, list) and artifacts:
            result_lines.append("")
            result_lines.append("증빙 경로:")
            result_lines.extend(str(item) for item in artifacts[:3])
            result_lines.append("동작: Ctrl+O=열기, Ctrl+Y=첫 경로 복사")
        if ts:
            result_lines.append(ts)
        self.query_one("#result-body", Static).update("\n".join(result_lines))
        self._refresh_log_controls()
        self._refresh_home_summary()

    def _refresh_commands(self, group_index: int) -> None:
        self.active_group_index = group_index
        self.active_command_index = 0
        commands = self._active_group_commands()
        group_label = group_surface_label(self._active_group_name())
        try:
            self.query_one("#commands-title", Static).update(f"2) 작업 선택  |  {group_label}")
            command_list = self.query_one("#commands", OptionList)
        except NoMatches:
            return
        self._suspend_option_events = True
        command_list.clear_options()
        command_list.add_options([Option(cmd.title) for cmd in commands])
        if commands:
            command_list.highlighted = 0
        self._suspend_option_events = False
        if commands:
            self._update_command_view(commands[0])
        else:
            self._suspend_option_events = False
            self.query_one("#details-body", Static).update(no_visible_command())
            self._clear_form()

    def _active_group_name(self) -> str:
        return self.group_names[self.active_group_index]

    def _active_group_commands(self) -> list[PaletteCommand]:
        if self._active_group_name() == "Favorites":
            return self._favorite_commands()
        return PRODUCT_COMMAND_GROUPS[self._active_group_name()]

    def _recent_rows(self) -> list[dict[str, object]]:
        recent = self.state.get("recent", [])
        if not isinstance(recent, list):
            return []
        return [item for item in recent[:5] if isinstance(item, dict)]

    def _recent_entry_label(self, item: dict[str, object]) -> str:
        status = str(item.get("status", ""))
        title = str(item.get("title", ""))
        ts = str(item.get("ts", ""))
        duration_ms = int(item.get("duration_ms", 0) or 0)
        duration_text = f"{duration_ms}ms" if duration_ms > 0 else "-"
        return f"{status} | {title} | {duration_text} | {ts}"

    def _selected_command(self) -> PaletteCommand | None:
        commands = self._active_group_commands()
        if not commands:
            return None
        if self.active_command_index < 0 or self.active_command_index >= len(commands):
            return None
        return commands[self.active_command_index]

    def _field_widgets(self, index: int) -> tuple[Vertical, Static, Input, Static]:
        row = self.query_one(f"#field-row-{index}", Vertical)
        label = self.query_one(f"#field-label-{index}", Static)
        input_widget = self.query_one(f"#field-input-{index}", Input)
        help_widget = self.query_one(f"#field-help-{index}", Static)
        return row, label, input_widget, help_widget

    def _update_command_view(self, command: PaletteCommand) -> None:
        try:
            details_widget = self.query_one("#details-body", Static)
            pin_button = self.query_one("#pin-button", Button)
            execute_hint_widget = self.query_one("#execute-hint", Static)
        except NoMatches:
            return
        runtime_text = runtime_badge(command)
        recommended = self._recommended_next(command)
        pin_text = pin_status(self._current_command_is_pinned())
        details_widget.update(
            command_info_body(
                command=command,
                runtime_text=runtime_text,
                pin_text=pin_text,
                recommended=recommended,
            )
        )
        pin_button.label = pin_button_label(self._current_command_is_pinned())
        self._populate_form(command)
        self._update_preview()
        if command.params:
            execute_hint_widget.update(execute_hint(True))
        else:
            execute_hint_widget.update(execute_hint(False))
    def _clear_form(self) -> None:
        try:
            preview_widget = self.query_one("#preview-body", Static)
        except NoMatches:
            return
        for index in range(FORM_SLOTS):
            row, _, input_widget, help_widget = self._field_widgets(index)
            row.add_class("hidden")
            input_widget.value = ""
            input_widget.placeholder = ""
            help_widget.update("")
        preview_widget.update(preview_empty())
    def _populate_form(self, command: PaletteCommand) -> None:
        params = list(command.params)
        defaults = resolve_command_defaults(command)
        for index in range(FORM_SLOTS):
            row, label, input_widget, help_widget = self._field_widgets(index)
            if index < len(params):
                param = params[index]
                row.remove_class("hidden")
                label.update(param.label)
                resolved_default = defaults.get(param.key, param.default)
                input_widget.value = resolved_default
                input_widget.placeholder = param.placeholder or resolved_default
                help_widget.update(param.help)
            else:
                row.add_class("hidden")
                input_widget.value = ""
                input_widget.placeholder = ""
                help_widget.update("")

    def _form_values(self) -> dict[str, str]:
        command = self._selected_command()
        if command is None:
            return {}
        values: dict[str, str] = {}
        for index, param in enumerate(command.params):
            _, _, input_widget, _ = self._field_widgets(index)
            values[param.key] = input_widget.value
        return values

    def _recommended_next(self, command: PaletteCommand) -> str:
        return recommended_next(command)
    def _extract_flag(self, tokens: list[str], flag: str) -> str:
        for index, token in enumerate(tokens):
            if token == flag and index + 1 < len(tokens):
                return tokens[index + 1]
        return ""

    def _artifact_paths(self, command: PaletteCommand, tokens: list[str]) -> list[str]:
        run_id = self._extract_flag(tokens, "--run-id")
        if command.command_id == "inspect.environment_doctor":
            return [
                "canoe/tmp/reports/verification/doctor_report.json",
                "canoe/tmp/reports/verification/doctor_report.md",
            ]
        if command.command_id == "verify.all_gates":
            return [
                "canoe/tmp/reports/verification/cli_readiness_gate.json",
                "canoe/tmp/reports/verification/cli_readiness_gate.md",
            ]
        if command.command_id == "verify.precheck_batch":
            return [
                "canoe/tmp/reports/verification/dev2_batch_report.json",
                "canoe/tmp/reports/verification/dev2_batch_report.md",
            ]
        if command.command_id in {"verify.quick_verify", "verify.run_readiness_status"}:
            paths = [
                "canoe/tmp/reports/verification/run_readiness.json",
                "canoe/tmp/reports/verification/run_readiness.md",
            ]
            if run_id:
                paths.extend(
                    [
                        f"canoe/logging/evidence/UT/{run_id}",
                        f"canoe/logging/evidence/IT/{run_id}",
                        f"canoe/logging/evidence/ST/{run_id}",
                    ]
                )
            return paths
        if command.command_id == "package.portable_bundle":
            return ["dist/portable/sdv_portable.zip"]
        if command.command_id == "package.windows_exe":
            return ["dist/sdv_cli"]
        return []

    def _extract_output_paths_from_lines(self, lines: list[str]) -> list[str]:
        outputs: list[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("[OUT]"):
                value = stripped.removeprefix("[OUT]").strip()
                if value:
                    outputs.append(value)
        return outputs

    def _merge_artifact_paths(self, command: PaletteCommand, tokens: list[str], lines: list[str]) -> list[str]:
        merged: list[str] = []
        for item in self._artifact_paths(command, tokens) + self._extract_output_paths_from_lines(lines):
            if item and item not in merged:
                merged.append(item)
        return merged

    def _set_live_runtime(self, *, stage: str, last_line: str, outputs: list[str] | None = None) -> None:
        live = self.state.get("live_runtime", {})
        if not isinstance(live, dict):
            live = {}
        live["stage"] = stage
        live["last_line"] = last_line
        live["outputs"] = outputs or list(live.get("outputs", []))
        self.state["live_runtime"] = live
        self._refresh_log_summary()

    def _update_live_runtime_from_line(self, command: PaletteCommand, line: str) -> None:
        stripped = line.strip()
        if not stripped:
            return
        live = self.state.get("live_runtime", {})
        if not isinstance(live, dict):
            live = {"stage": command.title, "last_line": "", "outputs": []}
        outputs = live.get("outputs", [])
        if not isinstance(outputs, list):
            outputs = []
        stage = str(live.get("stage", command.title))
        if stripped.startswith("[VERIFY_QUICK]"):
            stage = stripped.removeprefix("[VERIFY_QUICK]").strip() or command.title
        elif stripped.startswith("[SCENARIO]"):
            stage = "Scenario run"
        elif stripped.startswith("[DOCTOR]"):
            stage = "Doctor"
        elif stripped.startswith("[RUN_STATUS]"):
            stage = "증빙 준비 상태"
        elif stripped.startswith("[SMOKE]"):
            stage = "Smoke verification"
        elif stripped.startswith("[CANOE]"):
            stage = "CANoe runtime"
        if stripped.startswith("[OUT]"):
            output_path = stripped.removeprefix("[OUT]").strip()
            if output_path and output_path not in outputs:
                outputs.append(output_path)
        self.state["live_runtime"] = {
            "stage": stage,
            "last_line": stripped,
            "outputs": outputs,
        }
        self._refresh_log_summary()

    def _update_preview(self) -> None:
        command = self._selected_command()
        if command is None:
            self.query_one("#preview-body", Static).update(no_selected_command())
            return
        try:
            tokens = build_command_tokens(command, self._form_values())
            preview_lines = [f"python scripts/run.py {' '.join(tokens)}"]
            artifact_lines = command.expected_outputs or tuple(self._artifact_paths(command, tokens))
            if artifact_lines:
                preview_lines.extend(["", "[cyan]예상 산출물[/cyan]"])
                preview_lines.extend(f"  - {item}" for item in artifact_lines[:5])
            preview = "\n".join(preview_lines)
        except ValueError as ex:
            preview = f"[red]Input check[/red]: {ex}"
        self.query_one("#preview-body", Static).update(preview)

    def _write_log(self, message: str) -> None:
        self._append_log_entry(message, rendered=message, category="APP")

    def _format_log_line(self, line: str) -> str:
        stripped = line.rstrip()
        lowered = stripped.lower()
        safe = escape(stripped)

        if not stripped:
            return ""
        if stripped.startswith("[RUN]"):
            return f"[bold cyan]{safe}[/]"
        if stripped.startswith("[OUT]"):
            return f"[cyan]{safe}[/]"
        if stripped.startswith("[VERIFY_QUICK]") or stripped.startswith("[SCENARIO]"):
            return f"[bold green]{safe}[/]"
        if stripped.startswith("[RUN_STATUS]") or stripped.startswith("[SMOKE]"):
            return f"[green]{safe}[/]"
        if stripped.startswith("[CANOE]") or stripped.startswith("[DOCTOR]") or stripped.startswith("[WIZARD]"):
            return f"[bold blue]{safe}[/]"
        if any(keyword in lowered for keyword in ("error", "failed", "traceback", "exception")):
            return f"[bold red]{safe}[/]"
        if any(keyword in lowered for keyword in ("warning", "warn", "limited", "missing", "deferred", "stopped")):
            return f"[bold yellow]{safe}[/]"
        if any(keyword in lowered for keyword in ("pass", "ready", "ack", "ok")):
            return f"[green]{safe}[/]"
        return safe

    def _classify_log_entry(self, raw: str, category: str | None = None) -> tuple[str, str]:
        stripped = raw.strip()
        lowered = stripped.lower()
        resolved_category = category or "GENERAL"
        level = "INFO"

        if resolved_category == "GENERAL":
            if stripped.startswith("[VERIFY") or "verify" in lowered or "evidence" in lowered:
                resolved_category = "VERIFY"
            elif stripped.startswith("[OUT]") or stripped.startswith("[RUN_STATUS]") or stripped.startswith("[SMOKE]"):
                resolved_category = "VERIFY"
            elif stripped.startswith("[CANOE]") or "measurement" in lowered or "canoe" in lowered:
                resolved_category = "CANOE"
            elif stripped.startswith("[SCENARIO]"):
                resolved_category = "VERIFY"
            elif stripped.startswith("[DOCTOR]"):
                resolved_category = "CANOE"

        if any(keyword in lowered for keyword in ("error", "failed", "traceback", "exception", "rc=1", "rc=2", "rc=3")):
            level = "FAIL"
        elif any(keyword in lowered for keyword in ("warning", "warn", "limited", "missing", "deferred", "stopped")):
            level = "WARN"
        elif any(keyword in lowered for keyword in ("pass", "ready", "ack", "ok", "rc=0")):
            level = "PASS"

        return resolved_category, level

    def _log_entry_visible(self, entry: dict[str, str]) -> bool:
        filter_name = self.log_filter
        if filter_name == "ALL":
            return True
        if filter_name == "WARN":
            return entry.get("level") == "WARN"
        if filter_name == "FAIL":
            return entry.get("level") == "FAIL"
        if filter_name == "VERIFY":
            return entry.get("category") == "VERIFY"
        if filter_name == "CANOE":
            return entry.get("category") == "CANOE"
        return True

    def _append_log_entry(self, raw: str, rendered: str | None = None, category: str | None = None) -> None:
        resolved_category, level = self._classify_log_entry(raw, category)
        entry = {
            "raw": raw,
            "rendered": rendered or self._format_log_line(raw),
            "category": resolved_category,
            "level": level,
        }
        self.log_buffer.append(entry)
        if self._log_entry_visible(entry):
            self.query_one("#log", RichLog).write(entry["rendered"])
        self._refresh_log_controls()
        self._refresh_log_summary()

    def _rerender_log(self) -> None:
        log_widget = self.query_one("#log", RichLog)
        log_widget.clear()
        for entry in self.log_buffer:
            if self._log_entry_visible(entry):
                log_widget.write(entry["rendered"])
        self._refresh_log_controls()

    def _refresh_log_controls(self) -> None:
        visible = sum(1 for entry in self.log_buffer if self._log_entry_visible(entry))
        total = len(self.log_buffer)
        button_map = {
            "ALL": ("log-filter-all", log_filter_label("ALL")),
            "WARN": ("log-filter-warn", log_filter_label("WARN")),
            "FAIL": ("log-filter-fail", log_filter_label("FAIL")),
            "VERIFY": ("log-filter-verify", log_filter_label("VERIFY")),
            "CANOE": ("log-filter-canoe", log_filter_label("CANOE")),
        }
        for filter_name, (button_id, base_label) in button_map.items():
            button = self.query_one(f"#{button_id}", Button)
            button.label = f"[{base_label}]" if self.log_filter == filter_name else base_label
        self.query_one("#log-filter-status", Static).update(log_filter_status(self.log_filter, visible, total))
    def _set_log_filter(self, filter_name: str) -> None:
        self.log_filter = filter_name
        self._rerender_log()

    def _refresh_log_summary(self) -> None:
        live = self.state.get("live_runtime", {})
        if not isinstance(live, dict):
            live = {}
        stage = str(live.get("stage", live_runtime_default_stage()))
        last_line = str(live.get("last_line", live_runtime_default_line()))
        outputs = live.get("outputs", [])
        if not isinstance(outputs, list):
            outputs = []
        last_output = str(outputs[-1]) if outputs else None
        self.query_one("#log-summary", Static).update(live_runtime_summary(stage, last_line, last_output))
    def _timeline_stage_for_command(self, command_id: str) -> str | None:
        if command_id == "verify.all_gates":
            return "gate"
        if command_id == "operate.scenario_trigger":
            return "scenario"
        if command_id in {"verify.quick_verify", "verify.run_readiness_status", "verify.precheck_batch"}:
            return "verify"
        return None

    def _update_timeline_state(self, command_id: str, status: str, title: str, duration_ms: int = 0) -> None:
        timeline = self.state.get("timeline", {})
        if not isinstance(timeline, dict):
            timeline = {}
        stage = self._timeline_stage_for_command(command_id)
        if stage is not None:
            timeline[stage] = status
            timeline[f"{stage}_ms"] = int(duration_ms)
        timeline["current"] = title
        self.state["timeline"] = {
            "gate": str(timeline.get("gate", "IDLE")),
            "scenario": str(timeline.get("scenario", "IDLE")),
            "verify": str(timeline.get("verify", "IDLE")),
            "current": str(timeline.get("current", "대기")),
            "gate_ms": int(timeline.get("gate_ms", 0) or 0),
            "scenario_ms": int(timeline.get("scenario_ms", 0) or 0),
            "verify_ms": int(timeline.get("verify_ms", 0) or 0),
        }
    def _summarize_timeline(self) -> str:
        timeline = self.state.get("timeline", {})
        if not isinstance(timeline, dict):
            timeline = {}
        gate = str(timeline.get("gate", "IDLE"))
        scenario = str(timeline.get("scenario", "IDLE"))
        verify = str(timeline.get("verify", "IDLE"))
        current = str(timeline.get("current", "대기"))
        gate_ms = int(timeline.get("gate_ms", 0) or 0)
        scenario_ms = int(timeline.get("scenario_ms", 0) or 0)
        verify_ms = int(timeline.get("verify_ms", 0) or 0)
        gate_line = f"Gate: {gate}" + (f" ({gate_ms}ms)" if gate_ms > 0 else "")
        scenario_line = f"Scenario: {scenario}" + (f" ({scenario_ms}ms)" if scenario_ms > 0 else "")
        verify_line = f"Verify: {verify}" + (f" ({verify_ms}ms)" if verify_ms > 0 else "")
        return "\n".join([
            gate_line,
            scenario_line,
            verify_line,
            f"현재 단계: {current}",
        ])
    def _resolve_artifact_target(self) -> Path | None:
        last_result = self.state.get("last_result", {})
        if not isinstance(last_result, dict):
            return None
        artifacts = last_result.get("artifacts", [])
        if not isinstance(artifacts, list) or not artifacts:
            return None
        candidate = Path(str(artifacts[0]))
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        if candidate.exists():
            return candidate
        if candidate.parent.exists():
            return candidate.parent
        return None

    def _copy_text_to_clipboard(self, text: str) -> bool:
        try:
            if sys.platform.startswith("win"):
                subprocess.run("clip", input=text, text=True, check=True, shell=True)
                return True
            if sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text, text=True, check=True)
                return True
            for program in ("wl-copy", "xclip"):
                try:
                    args = [program] if program == "wl-copy" else [program, "-selection", "clipboard"]
                    subprocess.run(args, input=text, text=True, check=True)
                    return True
                except Exception:
                    continue
        except Exception:
            return False
        return False

    def action_set_log_filter_all(self) -> None:
        self._set_log_filter("ALL")

    def action_set_log_filter_warn(self) -> None:
        self._set_log_filter("WARN")

    def action_set_log_filter_fail(self) -> None:
        self._set_log_filter("FAIL")

    def action_set_log_filter_verify(self) -> None:
        self._set_log_filter("VERIFY")

    def action_set_log_filter_canoe(self) -> None:
        self._set_log_filter("CANOE")

    def action_open_artifact(self) -> None:
        target = self._resolve_artifact_target()
        if target is None:
            self._write_log(f"[yellow]{no_artifact_path()}[/]")
            return
        try:
            if sys.platform.startswith("win"):
                os.startfile(str(target))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(target)])
            else:
                subprocess.Popen(["xdg-open", str(target)])
            self._write_log(artifact_opened(str(target)))
        except Exception as ex:
            self._write_log(artifact_open_failed(ex))

    def action_copy_artifact(self) -> None:
        target = self._resolve_artifact_target()
        if target is None:
            self._write_log(f"[yellow]{no_artifact_path()}[/]")
            return
        if self._copy_text_to_clipboard(str(target)):
            self._write_log(artifact_copied(str(target)))
            return
        self._write_log(f"[bold yellow]Clipboard copy unavailable[/] {target}")

    def _load_json_file(self, path: Path) -> dict[str, object] | None:
        try:
            if not path.exists():
                return None
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            return None
        return None

    def _build_execution_insight(
        self,
        command: PaletteCommand,
        status: str,
        detail: str,
        tokens: list[str],
        artifacts: list[str],
    ) -> dict[str, str]:
        insight = {
            "stage": command.title,
            "bottleneck": detail,
            "next_action": self._recommended_next(command),
        }

        if command.command_id == "verify.quick_verify":
            readiness = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_readiness.json")
            if readiness:
                overall_status = str(readiness.get("overall_status", "")).strip() or status
                missing_items = readiness.get("missing_items", [])
                tiers = readiness.get("tiers", {})
                insight["stage"] = f"{command.title} -> {overall_status}"
                if isinstance(missing_items, list) and missing_items:
                    insight["bottleneck"] = str(missing_items[0])
                    if isinstance(tiers, dict):
                        missing_tiers = []
                        for tier_name, tier_data in tiers.items():
                            if isinstance(tier_data, dict) and int(tier_data.get("marker_count", 0)) == 0:
                                missing_tiers.append(str(tier_name))
                        if missing_tiers:
                            insight["bottleneck"] += f" | marker missing tiers: {', '.join(missing_tiers)}"
                    insight["next_action"] = "Capture [EVIDENCE_OUT] markers and rerun Verify quick."
                else:
                    insight["bottleneck"] = "누락된 증빙 마커가 없습니다."
                    insight["next_action"] = "Attach run_readiness artifacts into 05/06/07."
                return insight

        if command.command_id == "verify.precheck_batch":
            batch = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "dev2_batch_report.json")
            if batch:
                phase = str(batch.get("phase", "pre")).upper()
                status_value = str(batch.get("status", status))
                steps = batch.get("steps", [])
                failed_steps = [item for item in steps if isinstance(item, dict) and int(item.get("rc", 1)) != 0]
                insight["stage"] = f"Precheck {phase} -> {status_value}"
                if failed_steps:
                    failed = failed_steps[0]
                    insight["bottleneck"] = f"{failed.get('name', 'unknown step')} rc={failed.get('rc', '?')}"
                    insight["next_action"] = "Fix the failed precheck step before runtime execution."
                else:
                    insight["bottleneck"] = f"{int(batch.get('pass_count', 0))} steps passed"
                    insight["next_action"] = "Proceed to scenario run or evidence capture."
                return insight

        if command.command_id == "inspect.environment_doctor":
            doctor = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "doctor_report.json")
            if doctor:
                failed_checks = []
                for item in doctor.get("checks", []):
                    if isinstance(item, dict) and str(item.get("status", "")) != "PASS":
                        failed_checks.append(item)
                insight["stage"] = f"Doctor -> {doctor.get('status', status)}"
                if failed_checks:
                    first = failed_checks[0]
                    insight["bottleneck"] = f"{first.get('name', 'check')} = {first.get('detail', '-')}"
                    if str(first.get("name", "")) == "Measurement running":
                        insight["next_action"] = "Start CANoe measurement, then rerun doctor or scenario."
                    elif str(first.get("name", "")).startswith("SysVar "):
                        insight["next_action"] = "Load the right CANoe config/sysvars and rerun doctor."
                    else:
                        insight["next_action"] = "Check CANoe COM attach/session privilege and rerun doctor."
                else:
                    insight["bottleneck"] = "COM attach, measurement, 필수 sysvar가 모두 준비되었습니다."
                    insight["next_action"] = "Proceed to Scenario run."
                return insight

        if command.command_id == "verify.all_gates":
            insight["stage"] = "Gate bundle PASS" if status == "PASS" else "Gate bundle review"
            insight["bottleneck"] = "No gate failures detected." if status == "PASS" else detail
            insight["next_action"] = "Start runtime path with Scenario run." if status == "PASS" else "Fix the failing gate before runtime."
            return insight

        if command.command_id == "operate.scenario_trigger":
            scenario_id = self._extract_flag(tokens, "--id") or "?"
            if status == "PASS":
                insight["stage"] = f"Scenario {scenario_id} acknowledged"
                insight["bottleneck"] = "Ack path responded within the wait window."
                insight["next_action"] = "바로 Verify quick을 실행하십시오."
            elif "ack timeout" in detail.lower():
                insight["stage"] = f"Scenario {scenario_id} ack timeout"
                insight["bottleneck"] = detail
                insight["next_action"] = "Check measurement state, scenarioCommandAck, and active scenario CAPL path."
            elif "attach" in detail.lower() or "privilege/session" in detail.lower():
                insight["stage"] = f"Scenario {scenario_id} COM attach issue"
                insight["bottleneck"] = detail
                insight["next_action"] = "같은 CANoe 사용자 세션에서 doctor를 다시 실행하십시오."
            else:
                insight["stage"] = f"Scenario {scenario_id} review"
                insight["bottleneck"] = detail
                insight["next_action"] = "Check measurement state and scenario ack variable."
            return insight

        if artifacts:
            insight["next_action"] = f"Review evidence: {artifacts[0]}"
        return insight

    def _summarize_tier_readiness(self) -> str:
        readiness = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "run_readiness.json")
        if not readiness:
            return "아직 run_readiness.json이 없습니다.\nVerify quick을 실행하면 계층 준비 상태가 채워집니다."

        lines = [
            f"Run: {readiness.get('run_id', '-')}",
            f"Overall: {readiness.get('overall_status', '-')}",
        ]
        tiers = readiness.get("tiers", {})
        if isinstance(tiers, dict):
            for tier_name in ("UT", "IT", "ST"):
                tier = tiers.get(tier_name, {})
                if not isinstance(tier, dict):
                    continue
                marker_count = int(tier.get("marker_count", 0))
                scored_exists = bool(tier.get("scored_exists", False))
                filled_exists = bool(tier.get("filled_exists", False))
                tier_status = "PASS" if marker_count > 0 else "WARN"
                lines.append(
                    f"{tier_name}: {tier_status} marker={marker_count} filled={'Y' if filled_exists else 'N'} scored={'Y' if scored_exists else 'N'}"
                )
        return "\n".join(lines)

    def _summarize_batch_snapshot(self) -> str:
        batch = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "dev2_batch_report.json")
        if not batch:
            return "아직 dev2_batch_report.json이 없습니다.\nPrecheck batch 또는 Verify quick을 실행하면 배치 상태가 채워집니다."

        phase = str(batch.get("phase", "-")).upper()
        status = str(batch.get("status", "-"))
        pass_count = int(batch.get("pass_count", 0))
        fail_count = int(batch.get("fail_count", 0))
        steps = batch.get("steps", [])
        total_steps = len(steps) if isinstance(steps, list) else 0
        last_step = "-"
        first_fail = "-"
        if isinstance(steps, list) and steps:
            last = steps[-1]
            if isinstance(last, dict):
                last_step = str(last.get("name", "-"))
            failed_steps = [item for item in steps if isinstance(item, dict) and int(item.get("rc", 1)) != 0]
            if failed_steps:
                first_fail = str(failed_steps[0].get("name", "-"))
        lines = [
            f"Run: {batch.get('run_id', '-')}",
            f"Phase/Status: {phase} / {status}",
            f"Steps: {pass_count}/{total_steps} pass, fail={fail_count}",
            f"Last step: {last_step}",
            f"First fail: {first_fail}",
        ]
        return "\n".join(lines)

    def _last_scenario_recent(self) -> dict[str, object] | None:
        for item in self._recent_rows():
            if str(item.get("command_id", "")) == "operate.scenario_trigger":
                return item
        return None

    def _summarize_com_snapshot(self) -> str:
        doctor = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "doctor_report.json")
        if not doctor:
            lines = [
                "Doctor: no snapshot yet",
                "Attach/measurement/sysvar state unknown",
            ]
        else:
            checks = doctor.get("checks", [])
            attach = "-"
            measurement = "-"
            sysvar_pass = 0
            sysvar_total = 0
            if isinstance(checks, list):
                for item in checks:
                    if not isinstance(item, dict):
                        continue
                    name = str(item.get("name", ""))
                    status = str(item.get("status", "-"))
                    detail = str(item.get("detail", ""))
                    if name == "CANoe COM attach":
                        attach = status
                    elif name == "Measurement running":
                        measurement = detail.upper()
                    elif name.startswith("SysVar "):
                        sysvar_total += 1
                        if status == "PASS":
                            sysvar_pass += 1
            lines = [
                f"Doctor: {doctor.get('status', '-')}",
                f"COM attach: {attach}",
                f"Measurement: {measurement}",
                f"SysVar: {sysvar_pass}/{sysvar_total} pass",
            ]

        scenario = self._last_scenario_recent()
        if scenario is not None:
            status = str(scenario.get("status", "-"))
            detail = str(scenario.get("detail", "-"))
            lines.append(f"Scenario ack: {status}")
            lines.append(detail[:72])
        else:
            lines.append("Scenario ack: no recent run")
        return "\n".join(lines)

    def _set_running_state(self, command: PaletteCommand, started_ts: str, tokens: list[str]) -> None:
        self._update_timeline_state(command.command_id, "RUNNING", command.title, 0)
        self.state["live_runtime"] = {
            "stage": command.title,
            "last_line": "Process started. Waiting for runtime output...",
            "outputs": [],
        }
        self.state["last_insight"] = {
            "stage": f"Running: {command.title}",
            "bottleneck": "Process started. Watch the live log below.",
            "next_action": "Wait for completion, then review the result and evidence cards.",
        }
        self.state["last_result"] = {
            "status": "RUNNING",
            "title": command.title,
            "detail": "Execution in progress.",
            "ts": started_ts,
            "argv": tokens,
            "artifacts": self._artifact_paths(command, tokens),
            "related_logs": [],
        }
        self._save_state()
        self._refresh_summary_cards()
        self._refresh_log_summary()

    def _selected_option_index(self, option_list: OptionList) -> int:
        highlighted = option_list.highlighted
        return 0 if highlighted is None else int(highlighted)

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        if self._suspend_option_events:
            return
        if event.option_list.id == "commands":
            self.active_command_index = self._selected_option_index(event.option_list)
            command = self._selected_command()
            if command is not None:
                self._update_command_view(command)
            return
        if event.option_list.id == "recent-list":
            recent = self._recent_rows()
            index = self._selected_option_index(event.option_list)
            if 0 <= index < len(recent):
                item = recent[index]
                title = str(item.get("title", ""))
                status = str(item.get("status", ""))
                duration_ms = int(item.get("duration_ms", 0) or 0)
                detail = str(item.get("detail", ""))
                self.query_one(
                    "#insight-body", Static
                ).update(recent_selection_insight(title, status, duration_ms, detail))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "commands":
            self.active_command_index = self._selected_option_index(event.option_list)
            command = self._selected_command()
            if command is not None:
                self._update_command_view(command)
                if command.params:
                    self.action_focus_form()
                else:
                    self.query_one("#run-button", Button).focus()
            return
        if event.option_list.id == "recent-list":
            recent = self._recent_rows()
            index = self._selected_option_index(event.option_list)
            if 0 <= index < len(recent):
                self._rerun_recent_item(recent[index])

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id and event.input.id.startswith("field-input-"):
            self._update_preview()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id and event.input.id.startswith("field-input-"):
            self.action_run_selected()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "nav-home":
            self._show_page("home")
        elif event.button.id == "nav-execute":
            self._show_page("execute")
            self._refresh_execute_group_buttons()
            self.query_one("#commands", OptionList).focus()
        elif event.button.id == "nav-results":
            self._show_page("results")
        elif event.button.id == "nav-logs":
            self._show_page("logs")
        elif event.button.id == "home-gate":
            self._open_core_task("verify.all_gates", focus="run")
        elif event.button.id == "home-scenario":
            self._open_core_task("operate.scenario_trigger", focus="form")
        elif event.button.id == "home-verify":
            self._open_core_task("verify.quick_verify", focus="form")
        elif event.button.id == "group-primary":
            self._set_command_group("Primary Workflow")
        elif event.button.id == "group-runtime":
            self._set_command_group("Runtime Support")
        elif event.button.id == "group-inspect":
            self._set_command_group("System Access")
        elif event.button.id == "group-package":
            self._set_command_group("Packaging")
        elif event.button.id == "run-button":
            self.action_run_selected()
        elif event.button.id == "pin-button":
            self.action_toggle_pin()
        elif event.button.id == "reset-button":
            command = self._selected_command()
            if command is not None:
                self._populate_form(command)
                self._update_preview()
        elif event.button.id == "log-filter-all":
            self.action_set_log_filter_all()
        elif event.button.id == "log-filter-warn":
            self.action_set_log_filter_warn()
        elif event.button.id == "log-filter-fail":
            self.action_set_log_filter_fail()
        elif event.button.id == "log-filter-verify":
            self.action_set_log_filter_verify()
        elif event.button.id == "log-filter-canoe":
            self.action_set_log_filter_canoe()

    def action_focus_navigation(self) -> None:
        self.query_one("#nav-home", Button).focus()

    def action_focus_commands(self) -> None:
        self._show_page("execute")
        self.query_one("#commands", OptionList).focus()

    def action_focus_form(self) -> None:
        self._show_page("execute")
        command = self._selected_command()
        if command is None or not command.params:
            self.query_one("#commands", OptionList).focus()
            return
        _, _, input_widget, _ = self._field_widgets(0)
        input_widget.focus()

    def action_focus_log(self) -> None:
        self._show_page("logs")
        self.query_one("#log", RichLog).focus()

    def action_focus_favorites(self) -> None:
        self._show_page("results")

    def action_focus_recent(self) -> None:
        self._show_page("results")
        self.query_one("#recent-list", OptionList).focus()

    def action_toggle_pin(self) -> None:
        command = self._selected_command()
        if command is None:
            self._write_log(f"[yellow]{no_pin_target()}[/]")
            return
        pinned = [item for item in self.state.get("pinned", []) if isinstance(item, str)]
        if command.command_id in pinned:
            pinned = [item for item in pinned if item != command.command_id]
            self._write_log(pin_removed(command.title))
        else:
            pinned.insert(0, command.command_id)
            pinned = pinned[:8]
            self._write_log(pin_added(command.title))
        self.state["pinned"] = pinned
        self._save_state()
        preferred_group = self._active_group_name()
        self._rebuild_groups(preferred_group=preferred_group)
        self._refresh_summary_cards()

    def action_rerun_latest(self) -> None:
        recent = self._recent_rows()
        if not recent:
            self._write_log(f"[yellow]{no_recent_rerun()}[/]")
            return
        self._rerun_recent_item(recent[0])

    def _rerun_recent_item(self, item: dict[str, object]) -> None:
        command_id = str(item.get("command_id", ""))
        argv = item.get("argv", [])
        command = COMMAND_INDEX.get(command_id)
        if command is None or not isinstance(argv, list) or not argv:
            self._write_log("[yellow]Selected recent task cannot be rerun because its command metadata is missing.[/]")
            return
        tokens = [str(item) for item in argv]
        self._write_log(f"[bold green]$[/] python scripts/run.py {' '.join(tokens)}")
        self._run_command(command, tokens)

    def action_run_selected(self) -> None:
        command = self._selected_command()
        if command is None:
            self._write_log(f"[yellow]{no_selected_command()}[/]")
            return
        values = self._form_values()
        try:
            tokens = build_command_tokens(command, values)
        except ValueError as ex:
            self._write_log(f"[bold red]Input error[/]: {ex}")
            self._update_preview()
            return
        self._write_log(f"[bold green]$[/] python scripts/run.py {' '.join(tokens)}")
        self._show_page("logs")
        self._run_command(command, tokens)

    @work(thread=True, exclusive=True)
    def _run_command(self, command: PaletteCommand, tokens: list[str]) -> None:
        argv = [sys.executable, str(RUNNER), *tokens]
        lines: list[str] = []
        started_ts = time.strftime("%H:%M:%S")
        started_perf = time.perf_counter()
        self.call_from_thread(self._set_running_state, command, started_ts, tokens)
        try:
            LAST_OPERATOR_RESULT_PATH.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            proc = subprocess.Popen(
                argv,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except Exception as ex:
            self.call_from_thread(self._write_log, f"[bold red]Launch failed[/]: {ex}")
            artifacts = self._artifact_paths(command, tokens)
            insight = self._build_execution_insight(command, "FAIL", f"Launch failed: {ex}", tokens, artifacts)
            duration_ms = int((time.perf_counter() - started_perf) * 1000)
            self.call_from_thread(
                self._record_execution_result,
                command.title,
                command.command_id,
                "FAIL",
                f"Launch failed: {ex}",
                started_ts,
                duration_ms,
                tokens,
                artifacts,
                [f"Launch failed: {ex}"],
                insight,
            )
            return

        assert proc.stdout is not None
        self.call_from_thread(self._write_log, "[dim]------------------------------------------------------------[/]")
        for line in proc.stdout:
            lines.append(line.rstrip())
            self.call_from_thread(self._update_live_runtime_from_line, command, line.rstrip())
            self.call_from_thread(self._append_log_entry, line.rstrip())
        rc = proc.wait()
        duration_ms = int((time.perf_counter() - started_perf) * 1000)
        style = "green" if rc == 0 else "red"
        self.call_from_thread(self._write_log, f"[bold {style}]rc={rc}[/]")
        structured = self._load_operator_result(command.command_id)
        if structured:
            status = str(structured.get("status", "PASS"))
            detail = str(structured.get("detail", "Command completed successfully."))
            artifacts = [
                str(item)
                for item in structured.get("artifacts", [])
                if isinstance(item, str)
            ] or self._merge_artifact_paths(command, tokens, lines)
            related_logs = [
                str(item)
                for item in structured.get("related_logs", [])
                if isinstance(item, str)
            ] or self._collect_related_logs(lines, status, detail)
            raw_insight = structured.get("insight", {})
            insight = raw_insight if isinstance(raw_insight, dict) else self._build_execution_insight(command, status, detail, tokens, artifacts)
        else:
            status, detail = self._classify_result(command, rc, lines)
            artifacts = self._merge_artifact_paths(command, tokens, lines)
            insight = self._build_execution_insight(command, status, detail, tokens, artifacts)
            related_logs = self._collect_related_logs(lines, status, detail)
        self.call_from_thread(
            self._record_execution_result,
            command.title,
            command.command_id,
            status,
            detail,
            started_ts,
            duration_ms,
            tokens,
            artifacts,
            related_logs,
            insight,
        )
        next_hint = followup_hint(status)
        self.call_from_thread(self._write_log, f"[bold cyan]Next[/] {next_hint}")

    def _load_operator_result(self, command_id: str) -> dict[str, object] | None:
        data = self._load_json_file(LAST_OPERATOR_RESULT_PATH)
        if not data:
            return None
        if str(data.get("command_id", "")) != command_id:
            return None
        return data

    def _first_matching_line(self, lines: list[str], keywords: tuple[str, ...]) -> str:
        for line in lines:
            lowered = line.lower()
            if any(keyword in lowered for keyword in keywords):
                return line.strip()
        return ""

    def _collect_related_logs(self, lines: list[str], status: str, detail: str) -> list[str]:
        if status not in {"FAIL", "WARN"}:
            return []

        buckets: list[str] = []
        detail_token = detail.lower().strip()
        if detail_token:
            for line in lines:
                stripped = line.strip()
                lowered = stripped.lower()
                if not stripped:
                    continue
                if detail_token in lowered:
                    buckets.append(stripped)
            if buckets:
                return buckets[:3]

        keywords = ("error", "failed", "traceback", "exception") if status == "FAIL" else (
            "warning",
            "warn",
            "limited",
            "missing",
            "deferred",
            "stopped",
        )
        seen: set[str] = set()
        for line in lines:
            stripped = line.strip()
            lowered = stripped.lower()
            if not stripped:
                continue
            if any(keyword in lowered for keyword in keywords) and stripped not in seen:
                seen.add(stripped)
                buckets.append(stripped)
            if len(buckets) >= 3:
                break
        return buckets[:3]

    def _classify_result(self, command: PaletteCommand, rc: int, lines: list[str]) -> tuple[str, str]:
        joined = "\n".join(lines).lower()
        error_line = self._first_matching_line(lines, ("error", "failed", "traceback", "exception"))
        warn_line = self._first_matching_line(lines, ("warning", "warn", "limited", "stopped", "missing", "deferred"))
        pass_line = self._first_matching_line(lines, ("pass", "ok", "ready", "ack"))
        scenario_timeout = self._first_matching_line(lines, ("ack timeout",))
        scenario_attach = self._first_matching_line(lines, ("cannot attach canoe com", "same privilege/session"))

        if command.command_id == "inspect.environment_doctor":
            doctor = self._load_json_file(ROOT / "canoe" / "tmp" / "reports" / "verification" / "doctor_report.json")
            if doctor:
                failed_checks = [
                    item
                    for item in doctor.get("checks", [])
                    if isinstance(item, dict) and str(item.get("status", "")) != "PASS"
                ]
                if failed_checks:
                    first = failed_checks[0]
                    detail = f"{first.get('name', 'check')}: {first.get('detail', '-')}"
                    if len(failed_checks) == 1 and str(first.get("name", "")) == "Measurement running":
                        return "WARN", detail
                    return "FAIL", detail
                return "PASS", "Doctor checks passed."

        if command.command_id == "operate.scenario_trigger":
            if scenario_timeout:
                return "WARN", scenario_timeout
            if scenario_attach:
                return "FAIL", scenario_attach

        if command.command_id == "operate.measure_status":
            if "measurement=running" in joined:
                return "PASS", "CANoe measurement is running."
            if "measurement=stopped" in joined:
                return "WARN", "CANoe measurement is stopped. Start measurement before scenario or verify tasks."

        if rc != 0:
            if error_line:
                return "FAIL", error_line
            if warn_line:
                return "WARN", warn_line
            return "FAIL", "The command returned a non-zero exit code."

        if command.command_id == "operate.measure_start":
            if "measurement started" in joined or "measurement=start" in joined or "running" in joined:
                return "PASS", "Measurement가 시작되었습니다."

        if command.command_id == "operate.measure_stop":
            if "measurement stopped" in joined or "measurement=stopped" in joined or "stopped" in joined:
                return "WARN", "Measurement is stopped now. This is expected only if you intended to halt runtime."

        if command.command_id == "operate.scenario_trigger":
            ack_line = self._first_matching_line(lines, ("ack",))
            if ack_line:
                return "PASS", ack_line

        if command.command_id == "verify.run_readiness_status":
            if "ready" in joined and "missing" not in joined:
                return "PASS", "Evidence run is ready for finalize."
            if warn_line:
                return "WARN", warn_line

        if command.command_id == "verify.precheck_batch":
            if "gate summary: pass" in joined or "[guided] pass" in joined:
                return "PASS", "Precheck flow passed and the operator can move to evidence capture."

        if command.command_id == "verify.quick_verify":
            if "[verify_quick] verify status" in joined and "missing" not in joined:
                return "PASS", "Verify quick가 readiness까지 정상 완료되었습니다."

        if command.command_id == "verify.all_gates":
            if "gate summary: pass" in joined:
                return "PASS", "All configured gates passed."
            if warn_line:
                return "WARN", warn_line

        if command.command_id in {"package.portable_bundle", "package.windows_exe"}:
            ok_line = self._first_matching_line(lines, ("[ok]", "portable zip", "portable folder", "dist\\", "dist/"))
            if ok_line:
                return "PASS", ok_line

        if warn_line:
            return "WARN", warn_line
        if pass_line:
            return "PASS", pass_line
        return "PASS", "Command completed successfully."

    def _record_execution_result(
        self,
        title: str,
        command_id: str,
        status: str,
        detail: str,
        started_ts: str,
        duration_ms: int,
        argv: list[str],
        artifacts: list[str],
        related_logs: list[str],
        insight: dict[str, str],
    ) -> None:
        self._update_timeline_state(command_id, status, title, duration_ms)
        live = self.state.get("live_runtime", {})
        if not isinstance(live, dict):
            live = {}
        self.state["live_runtime"] = {
            "stage": f"{title} -> {status}",
            "last_line": detail,
            "outputs": artifacts,
        }
        recent = self.state.get("recent", [])
        if not isinstance(recent, list):
            recent = []
        recent.insert(
            0,
            {
                "title": title,
                "command_id": command_id,
                "status": status,
                "detail": detail,
                "ts": started_ts,
                "duration_ms": duration_ms,
                "argv": argv,
                "artifacts": artifacts,
                "related_logs": related_logs,
                "insight": insight,
            },
        )
        self.state["recent"] = recent[:5]
        self.state["last_insight"] = insight
        self.state["last_result"] = {
            "status": status,
            "title": title,
            "detail": detail,
            "ts": started_ts,
            "duration_ms": duration_ms,
            "argv": argv,
            "artifacts": artifacts,
            "related_logs": related_logs,
        }
        self._save_state()
        self._refresh_summary_cards()


def launch_tui() -> int:
    app = SdvTuiApp()
    app.run()
    return 0

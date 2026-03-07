"""Textual TUI frontend for the SDV CANoe operator CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from cliops.command_catalog import (
    PRODUCT_COMMAND_GROUPS,
    PaletteCommand,
    build_command_tokens,
    resolve_command_defaults,
)
from cliops.platform_caps import canoe_runtime_check, platform_label
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, OptionList, RichLog, Static
from textual.widgets.option_list import Option


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts" / "run.py"
FORM_SLOTS = 4


class SdvTuiApp(App[None]):
    CSS = """
    Screen {
        background: #11161c;
        color: #d8dee9;
    }

    #hero {
        height: 4;
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

    #workspace {
        height: 1fr;
        margin: 0 1;
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
        width: 34;
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

    #actions {
        margin-top: 1;
        height: 3;
    }

    #actions Button {
        margin-right: 1;
    }

    #log-pane {
        height: 14;
        margin: 1;
        padding: 1;
        background: #0f151b;
        border: round #2d3e50;
    }

    #log {
        height: 1fr;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "run_selected", "Run"),
        ("g", "focus_groups", "Groups"),
        ("c", "focus_commands", "Commands"),
        ("f", "focus_form", "Form"),
        ("l", "focus_log", "Log"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.group_names = list(PRODUCT_COMMAND_GROUPS.keys())
        self.active_group_index = 0
        self.active_command_index = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            "SDV Operator Console\n"
            "Pick a task, adjust only the required values, then run it.",
            id="hero",
        )
        runtime = canoe_runtime_check()
        runtime_text = (
            f"Host: {platform_label()} | CANoe runtime: {'ready' if runtime.available else 'limited'} | "
            "Focus: g/c/f/l | Run: Enter or r | Quit: q"
        )
        if not runtime.available:
            runtime_text += f"\nConstraint: {runtime.detail}"
        yield Static(runtime_text, id="runtime")
        with Horizontal(id="workspace"):
            with Vertical(id="groups-pane", classes="pane"):
                yield Static("1) What do you want to do?", classes="pane-title")
                yield OptionList(id="groups")
            with Vertical(id="commands-pane", classes="pane"):
                yield Static("2) Pick one task", classes="pane-title")
                yield OptionList(id="commands")
            with Vertical(id="details-pane", classes="pane"):
                yield Static("3) Review and run", classes="pane-title")
                yield Static(id="details-body")
                yield Static("Quick Form", classes="pane-title")
                with Vertical(id="form-body"):
                    for index in range(FORM_SLOTS):
                        with Vertical(id=f"field-row-{index}", classes="form-row hidden"):
                            yield Static(id=f"field-label-{index}", classes="field-label")
                            yield Input(id=f"field-input-{index}")
                            yield Static(id=f"field-help-{index}", classes="field-help")
                yield Static(id="preview-body")
                with Horizontal(id="actions"):
                    yield Button("Run now", id="run-button", variant="success")
                    yield Button("Reset defaults", id="reset-button")
        with Vertical(id="log-pane"):
            yield Static("Execution Log", classes="pane-title")
            yield RichLog(id="log", wrap=True, highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = "SDV Operator Console"
        self.sub_title = "Textual TUI"
        groups = self.query_one("#groups", OptionList)
        groups.add_options([Option(group_name) for group_name in self.group_names])
        groups.highlighted = 0
        self._refresh_commands(0)
        self.query_one("#commands", OptionList).focus()
        self._write_log("[bold cyan]TUI ready[/]  Select a task, fill required values, then press [bold]r[/].")

    def _refresh_commands(self, group_index: int) -> None:
        self.active_group_index = group_index
        self.active_command_index = 0
        commands = self._active_group_commands()
        command_list = self.query_one("#commands", OptionList)
        command_list.clear_options()
        command_list.add_options([Option(cmd.title) for cmd in commands])
        if commands:
            command_list.highlighted = 0
            self._update_command_view(commands[0])
        else:
            self.query_one("#details-body", Static).update("No commands in this category.")
            self._clear_form()

    def _active_group_name(self) -> str:
        return self.group_names[self.active_group_index]

    def _active_group_commands(self) -> list[PaletteCommand]:
        return PRODUCT_COMMAND_GROUPS[self._active_group_name()]

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
        badges = ["Windows-only" if command.windows_only else "Cross-platform"]
        recommended = self._recommended_next(command)
        body = [
            f"[bold]{command.title}[/bold]",
            "",
            command.summary,
            "",
            f"[cyan]Default command[/cyan]: python scripts/run.py {command.command}",
            f"[cyan]Runtime[/cyan]: {', '.join(badges)}",
            f"[cyan]Recommended next[/cyan]: {recommended}",
        ]
        if command.notes:
            body.extend(["", f"[cyan]Operator note[/cyan]: {command.notes}"])
        self.query_one("#details-body", Static).update("\n".join(body))
        self._populate_form(command)
        self._update_preview()

    def _clear_form(self) -> None:
        for index in range(FORM_SLOTS):
            row, _, input_widget, help_widget = self._field_widgets(index)
            row.add_class("hidden")
            input_widget.value = ""
            input_widget.placeholder = ""
            help_widget.update("")
        self.query_one("#preview-body", Static).update("No parameters required.")

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
        if command.title == "Measurement status":
            return "If stopped, run Measurement start next."
        if command.title == "Measurement start":
            return "After start, trigger a scenario or run Precheck batch."
        if command.title == "Scenario trigger":
            return "After scenario ack, run Run readiness status or Quick verify."
        if command.title == "Precheck batch":
            return "If PASS, move to screenshots/evidence capture."
        if command.title == "Quick verify":
            return "If PASS, bind results into 05/06/07 evidence."
        if command.title == "Environment doctor":
            return "If all checks are green, move to measurement or scenario."
        if command.title == "Portable bundle":
            return "Use this only after operator flow and reports are stable."
        return "Run this, review the log below, then move to the next verification step."

    def _update_preview(self) -> None:
        command = self._selected_command()
        if command is None:
            self.query_one("#preview-body", Static).update("No command selected.")
            return
        try:
            tokens = build_command_tokens(command, self._form_values())
            preview = "python scripts/run.py " + " ".join(tokens)
        except ValueError as ex:
            preview = f"[red]Input check[/red]: {ex}"
        self.query_one("#preview-body", Static).update(preview)

    def _write_log(self, message: str) -> None:
        self.query_one("#log", RichLog).write(message)

    def _selected_option_index(self, option_list: OptionList) -> int:
        highlighted = option_list.highlighted
        return 0 if highlighted is None else int(highlighted)

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        if event.option_list.id == "groups":
            group_index = self._selected_option_index(event.option_list)
            self._refresh_commands(group_index)
            return
        if event.option_list.id == "commands":
            self.active_command_index = self._selected_option_index(event.option_list)
            command = self._selected_command()
            if command is not None:
                self._update_command_view(command)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "groups":
            group_index = self._selected_option_index(event.option_list)
            self._refresh_commands(group_index)
            self.query_one("#commands", OptionList).focus()
            return
        if event.option_list.id == "commands":
            self.active_command_index = self._selected_option_index(event.option_list)
            self.action_run_selected()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id and event.input.id.startswith("field-input-"):
            self._update_preview()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id and event.input.id.startswith("field-input-"):
            self.action_run_selected()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-button":
            self.action_run_selected()
        elif event.button.id == "reset-button":
            command = self._selected_command()
            if command is not None:
                self._populate_form(command)
                self._update_preview()

    def action_focus_groups(self) -> None:
        self.query_one("#groups", OptionList).focus()

    def action_focus_commands(self) -> None:
        self.query_one("#commands", OptionList).focus()

    def action_focus_form(self) -> None:
        command = self._selected_command()
        if command is None or not command.params:
            self.query_one("#commands", OptionList).focus()
            return
        _, _, input_widget, _ = self._field_widgets(0)
        input_widget.focus()

    def action_focus_log(self) -> None:
        self.query_one("#log", RichLog).focus()

    def action_run_selected(self) -> None:
        command = self._selected_command()
        if command is None:
            self._write_log("[yellow]No command selected.[/]")
            return
        try:
            tokens = build_command_tokens(command, self._form_values())
        except ValueError as ex:
            self._write_log(f"[bold red]Input error[/]: {ex}")
            self._update_preview()
            return
        self._write_log(f"[bold green]$[/] python scripts/run.py {' '.join(tokens)}")
        self._run_command(tokens)

    @work(thread=True, exclusive=True)
    def _run_command(self, tokens: list[str]) -> None:
        argv = [sys.executable, str(RUNNER), *tokens]
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
            return

        assert proc.stdout is not None
        for line in proc.stdout:
            self.call_from_thread(self._write_log, line.rstrip())
        rc = proc.wait()
        style = "green" if rc == 0 else "red"
        self.call_from_thread(self._write_log, f"[bold {style}]rc={rc}[/]")


def launch_tui() -> int:
    app = SdvTuiApp()
    app.run()
    return 0

"""Textual TUI frontend for the SDV CANoe operator CLI."""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

from cliops.command_catalog import PRODUCT_COMMAND_GROUPS, PaletteCommand
from cliops.platform_caps import canoe_runtime_check, platform_label
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, OptionList, RichLog, Static
from textual.widgets.option_list import Option


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts" / "run.py"


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
        width: 24;
    }

    #commands-pane {
        width: 44;
    }

    #details-pane {
        width: 1fr;
        margin-right: 0;
    }

    #details-body {
        padding: 0 1;
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
            "CANoe SIL verification control plane | Operate / Verify / Inspect / Package",
            id="hero",
        )
        runtime = canoe_runtime_check()
        runtime_text = (
            f"Host: {platform_label()} | CANoe runtime: {'ready' if runtime.available else 'limited'} | "
            "Run: Enter/r | Quit: q | Shell fallback: python scripts/run.py shell"
        )
        if not runtime.available:
            runtime_text += f"\nConstraint: {runtime.detail}"
        yield Static(runtime_text, id="runtime")
        with Horizontal(id="workspace"):
            with Vertical(id="groups-pane", classes="pane"):
                yield Static("Categories", classes="pane-title")
                yield OptionList(id="groups")
            with Vertical(id="commands-pane", classes="pane"):
                yield Static("Commands", classes="pane-title")
                yield OptionList(id="commands")
            with Vertical(id="details-pane", classes="pane"):
                yield Static("Details", classes="pane-title")
                yield Static(id="details-body")
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
        self._write_log("[bold cyan]TUI ready[/]  Press [bold]r[/] to execute the selected command.")

    def _refresh_commands(self, group_index: int) -> None:
        self.active_group_index = group_index
        self.active_command_index = 0
        commands = self._active_group_commands()
        command_list = self.query_one("#commands", OptionList)
        command_list.clear_options()
        command_list.add_options([Option(cmd.title) for cmd in commands])
        if commands:
            command_list.highlighted = 0
            self._update_details(commands[0])
        else:
            self.query_one("#details-body", Static).update("No commands in this category.")

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

    def _update_details(self, command: PaletteCommand) -> None:
        badges = ["Windows-only" if command.windows_only else "Cross-platform"]
        body = [
            f"[bold]{command.title}[/bold]",
            "",
            command.summary,
            "",
            f"[cyan]Command[/cyan]: python scripts/run.py {command.command}",
            f"[cyan]Runtime[/cyan]: {', '.join(badges)}",
        ]
        if command.notes:
            body.extend(["", f"[cyan]Operator note[/cyan]: {command.notes}"])
        self.query_one("#details-body", Static).update("\n".join(body))

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
                self._update_details(command)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "groups":
            group_index = self._selected_option_index(event.option_list)
            self._refresh_commands(group_index)
            self.query_one("#commands", OptionList).focus()
            return
        if event.option_list.id == "commands":
            self.active_command_index = self._selected_option_index(event.option_list)
            self.action_run_selected()

    def action_focus_groups(self) -> None:
        self.query_one("#groups", OptionList).focus()

    def action_focus_commands(self) -> None:
        self.query_one("#commands", OptionList).focus()

    def action_focus_log(self) -> None:
        self.query_one("#log", RichLog).focus()

    def action_run_selected(self) -> None:
        command = self._selected_command()
        if command is None:
            self._write_log("[yellow]No command selected.[/]")
            return
        self._write_log(f"[bold green]$[/] python scripts/run.py {command.command}")
        self._run_command(command)

    @work(thread=True, exclusive=True)
    def _run_command(self, command: PaletteCommand) -> None:
        argv = [sys.executable, str(RUNNER), *shlex.split(command.command)]
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

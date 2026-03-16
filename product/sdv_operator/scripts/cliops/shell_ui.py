from __future__ import annotations

import datetime as dt
import difflib
import json
import sys

try:
    import questionary
except Exception:
    questionary = None

try:
    from rich.console import Console
    from rich.panel import Panel
except Exception:
    Console = None
    Panel = None

from cliops.command_catalog import build_shell_palette_groups
from cliops.common import SHELL_HISTORY_FILE

_RICH_CONSOLE = Console() if Console is not None else None
SHELL_PALETTE_GROUPS: dict[str, list[tuple[str, str]]] = build_shell_palette_groups()


def is_interactive_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def has_questionary_support() -> bool:
    return questionary is not None and is_interactive_tty()


def has_rich_support() -> bool:
    return _RICH_CONSOLE is not None and is_interactive_tty()


def prompt_with_default(label: str, default: str) -> str:
    if has_questionary_support():
        answer = questionary.text(label, default=default).ask()
        if answer is None:
            return default
        answer = answer.strip()
        return answer or default
    raw = input(f'{label} [{default}]: ').strip()
    return raw or default


def ui_info(msg: str) -> None:
    if has_rich_support():
        _RICH_CONSOLE.print(msg)
    else:
        print(msg)


def ui_welcome_banner() -> None:
    title = 'CANoe Test Verification Console'
    body = 'CANoe verification console\nScenario trigger | Results | Artifacts | Measurement control'
    if has_rich_support() and Panel is not None:
        _RICH_CONSOLE.print(Panel(body, title=title, border_style='cyan'))
    else:
        print('=' * 56)
        print(f'{title} - CANoe 검증 운영 콘솔')
        print('=' * 56)


def run_with_loading(label: str, func) -> int:
    if has_rich_support():
        with _RICH_CONSOLE.status(f'[bold cyan]{label}[/]'):
            return func()
    ui_info(f'[GUIDED] running: {label}')
    return func()


def prompt_menu_choice(default: int = 1, minimum: int = 1, maximum: int = 11) -> int:
    if has_questionary_support():
        choices = [
            questionary.Choice('1) 환경 점검 (CANoe COM + measurement + sysvar)', value=1),
            questionary.Choice('2) 사전 점검 (gate + prepare + smoke + status)', value=2),
            questionary.Choice('3) 시나리오 실행 (scenarioCommand/testScenario)', value=3),
            questionary.Choice('4) 증빙 상태 (readiness report)', value=4),
            questionary.Choice('5) 측정 시작', value=5),
            questionary.Choice('6) 측정 중지', value=6),
            questionary.Choice('7) 측정 상태', value=7),
            questionary.Choice('8) slash shell 열기', value=8),
            questionary.Choice('9) 빠른 흐름 (점검 -> 시나리오 -> 검증)', value=9),
            questionary.Choice('10) 도움말', value=10),
            questionary.Choice('11) 조용히 종료', value=11),
        ]
        answer = questionary.select('작업 선택', choices=choices, default=choices[default - 1]).ask()
        if answer is None:
            return 11
        return int(answer)
    while True:
        raw = input(f'선택 [{minimum}-{maximum}] (기본 {default}, q=조용히 종료): ').strip()
        if raw.lower() in {'q', 'quit', 'x'}:
            return 11
        if not raw:
            return default
        try:
            value = int(raw)
        except ValueError:
            print('[GUIDED] 유효한 숫자를 입력하십시오.')
            continue
        if value < minimum or value > maximum:
            print(f'[GUIDED] 값은 {minimum}..{maximum} 범위여야 합니다.')
            continue
        return value


def prompt_int(label: str, default: int, minimum: int, maximum: int) -> int:
    while True:
        if has_questionary_support():
            answer = questionary.text(label, default=str(default)).ask()
            raw = '' if answer is None else answer.strip()
        else:
            raw = input(f'{label} [{default}]: ').strip()
        if not raw:
            return default
        try:
            value = int(raw)
        except ValueError:
            print('[WIZARD] enter a valid integer.')
            continue
        if value < minimum or value > maximum:
            print(f'[WIZARD] value must be in range {minimum}..{maximum}.')
            continue
        return value


def suggest_choice(value: str, choices: list[str]) -> str | None:
    matches = difflib.get_close_matches(value, choices, n=1, cutoff=0.5)
    return matches[0] if matches else None


def print_shell_help() -> None:
    print('Slash commands:')
    print('  /help')
    print('  /exit')
    print('  /gate all            # daily step 1: run all gates')
    print('  /scenario run <id>   # daily step 2: inject one scenario')
    print('  /verify quick [run_id] [owner]  # daily step 3: collect quick evidence')
    print('  /palette  # grouped command palette')
    print('  /tui      # launch the Textual operator console')
    print('  /history [N]  # recent command history (default 10)')
    print('  /repeat [N]   # repeat Nth latest command (default 1)')
    print('  /scenario [run] <id> [scenarioCommand|testScenario]')
    print('  /start guided|demo [id]|precheck [run_id] [campaign_id] [owner] [surface_scope] [repeat] [duration_min] [interval_sec]')
    print('  /go  # alias of /start guided')
    print('  /verify prepare [run_id]')
    print('  /verify batch [run_id] [campaign_id] [owner] [pre|post|full] [surface_scope] [repeat] [duration_min] [interval_sec] [json,md|json,md,csv|json,md,junit|...]')
    print('                 [--profile-id <id>] [--pack-id <id>]')
    print('  /verify smoke [owner] [run_date]')
    print('  /verify status [run_id]')
    print('  /verify surface-bundle   # build reviewer-facing surface ECU bundle')
    print('  /verify finalize [run_id] [owner] [run_date]')
    print('  /verify quick [run_id] [owner]  # prepare + smoke + readiness status')
    print('  /gate all|doc-sync|text-integrity|cfg-hygiene|capl-sync|multibus-dbc|cli-readiness')
    print('  /artifact list [staging|archive|source] [--latest|--run-id <id>] [--phase <pre|post|full>]')
    print('  /artifact open --target <batch-report|run-insight|doc-binding-bundle|doc-fill-template|surface-bundle|readiness|doctor|surface-inventory|unit-test-doc|integration-test-doc|system-test-doc|test-asset-mapping|active-test-units-guide|active-test-suites-guide|execution-guide|verification-pack-matrix|campaign-profiles|traceability-profile|artifact-layout|phase-policy|manifest|commands-doc|results-doc|packaging-doc|archive-run|reports-dir|surface-dir|native-reports|execution-manifest>')
    print('  /artifact clean [staging|archive|build|all] [run_id] [phase] [--yes]')
    print('  /package portable [onefolder|onefile]')
    print('  /package exe [onefolder|onefile]')
    print('  /package validate-contract')
    print('  /doctor [ensure-running]')
    print('  /capl get <Namespace> <Variable>')
    print('  /capl set <Namespace> <Variable> <Value>')
    print('  /canoe measure <status|start|stop|reset>')
    print('  /canoe capl-call <FunctionName> [arg1 arg2 ...] [--int|--float|--bool]')
    print('  /skill list')
    print('  /skill run quickstart|verify-pack|portable-release')
    print('  /contract')


def append_shell_history(command: str, rc: int, duration_ms: int) -> None:
    try:
        SHELL_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = {'ts': dt.datetime.now().isoformat(timespec='seconds'), 'command': command, 'rc': rc, 'duration_ms': duration_ms}
        with SHELL_HISTORY_FILE.open('a', encoding='utf-8') as fp:
            fp.write(json.dumps(payload, ensure_ascii=False) + '\n')
    except Exception:
        pass


def print_shell_history(session_commands: list[str], limit: int = 10) -> None:
    if limit < 1:
        limit = 1
    recent = session_commands[-limit:]
    if not recent:
        print('[SHELL] history is empty')
        return
    print('[SHELL] recent commands')
    start_idx = len(session_commands) - len(recent) + 1
    for i, item in enumerate(recent, start=start_idx):
        print(f'  {i}) {item}')


def prompt_shell_palette_command() -> str | None:
    group_names = list(SHELL_PALETTE_GROUPS.keys())
    print('[SHELL] palette')
    for idx, group_name in enumerate(group_names, start=1):
        print(f'  {idx}) {group_name}')
    while True:
        raw_group = input('group number (Enter=cancel): ').strip()
        if not raw_group:
            return None
        try:
            group_value = int(raw_group)
        except ValueError:
            print('[SHELL] enter a valid number.')
            continue
        if group_value < 1 or group_value > len(group_names):
            print(f'[SHELL] number must be 1..{len(group_names)}.')
            continue
        break
    selected_group = group_names[group_value - 1]
    items = SHELL_PALETTE_GROUPS[selected_group]
    print(f'[SHELL] {selected_group}')
    for idx, (cmd, desc) in enumerate(items, start=1):
        print(f'  {idx}) {cmd:<34} - {desc}')
    while True:
        raw = input('command number (Enter=cancel): ').strip()
        if not raw:
            return None
        try:
            value = int(raw)
        except ValueError:
            print('[SHELL] enter a valid number.')
            continue
        if value < 1 or value > len(items):
            print(f'[SHELL] number must be 1..{len(items)}.')
            continue
        return items[value - 1][0]


def can_launch_tui() -> tuple[bool, str]:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return False, 'non-interactive terminal'
    try:
        import textual  # noqa: F401
    except Exception as ex:
        return False, f'Textual import failed: {ex}'
    return True, ''

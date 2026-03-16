from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

from cliops.platform_caps import require_canoe_runtime

def _find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "AGENTS.md").exists() and (candidate / "canoe").exists():
            return candidate
    return current.parents[-1]


ROOT = _find_repo_root()
SCRIPTS = ROOT / 'scripts'
SHELL_HISTORY_FILE = ROOT / 'canoe' / 'tmp' / 'reports' / 'verification' / 'cli_shell_history.jsonl'


def _display_arg(value: str) -> str:
    if value == sys.executable:
        return Path(value).name
    candidate = Path(value)
    if candidate.is_absolute():
        try:
            return candidate.relative_to(ROOT).as_posix()
        except ValueError:
            return value
    return value


def run_cmd(args: list[str]) -> int:
    print('[RUN]', ' '.join(_display_arg(arg) for arg in args))
    proc = subprocess.run(args, cwd=ROOT)
    return proc.returncode


def fail_unavailable(action_name: str) -> int:
    message = require_canoe_runtime(action_name)
    if message:
        print(f'[PLATFORM] {message}')
        print('[PLATFORM] available everywhere: gate/verify/evidence/package/report commands')
        return 2
    return 0


def default_run_id() -> str:
    return dt.datetime.now().strftime('%Y%m%d_%H%M')


def default_campaign_id() -> str:
    return dt.datetime.now().strftime('CMP_%Y%m%d')


def iso_today() -> str:
    return dt.date.today().isoformat()

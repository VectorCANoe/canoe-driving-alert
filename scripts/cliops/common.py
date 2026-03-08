from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

from cliops.platform_caps import require_canoe_runtime

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'scripts'
SHELL_HISTORY_FILE = ROOT / 'canoe' / 'tmp' / 'reports' / 'verification' / 'cli_shell_history.jsonl'


def run_cmd(args: list[str]) -> int:
    print('[RUN]', ' '.join(args))
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


def iso_today() -> str:
    return dt.date.today().isoformat()

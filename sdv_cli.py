#!/usr/bin/env python3
"""Installable CLI shim for this repository.

`sdv` delegates to `scripts/run.py` after resolving repository root.
This keeps command behavior identical between:
- direct script usage (`python scripts/run.py ...`)
- installed entrypoint usage (`sdv ...`)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def _is_repo_root(path: Path) -> bool:
    return (path / "scripts" / "run.py").exists() and (path / "AGENTS.md").exists()


def _find_repo_root(start: Path) -> Path | None:
    env_root = os.environ.get("SDV_REPO_ROOT", "").strip()
    if env_root:
        candidate = Path(env_root).resolve()
        if _is_repo_root(candidate):
            return candidate

    current = start.resolve()
    for candidate in [current, *current.parents]:
        if _is_repo_root(candidate):
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    repo_root = _find_repo_root(Path.cwd())
    if repo_root is None:
        print(
            "[SDV][FAIL] Repository root not found. "
            "Run from inside the repo or set SDV_REPO_ROOT.",
            file=sys.stderr,
        )
        return 2

    run_py = repo_root / "scripts" / "run.py"
    # In frozen exe mode, calling sys.executable would recurse into this exe.
    if getattr(sys, "frozen", False):
        if os.environ.get("SDV_PYTHON", "").strip():
            py_cmd: list[str] = [os.environ["SDV_PYTHON"].strip()]
        elif shutil.which("python"):
            py_cmd = ["python"]
        elif shutil.which("py"):
            py_cmd = ["py", "-3"]
        else:
            print(
                "[SDV][FAIL] Python runtime not found. Install Python or set SDV_PYTHON.",
                file=sys.stderr,
            )
            return 3
    else:
        py_cmd = [sys.executable]

    cmd = [*py_cmd, str(run_py), *args]
    proc = subprocess.run(cmd, cwd=repo_root)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

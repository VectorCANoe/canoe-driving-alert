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
import runpy
import argparse as _bundle_argparse
import csv as _bundle_csv
import datetime as _bundle_datetime
import dataclasses as _bundle_dataclasses
import hashlib as _bundle_hashlib
import json as _bundle_json
import math as _bundle_math
import re as _bundle_re
import tomllib as _bundle_tomllib
from collections import Counter as _bundle_counter, defaultdict as _bundle_defaultdict
from pathlib import Path

try:  # optional runtime dependency for CANoe COM scripts
    import win32com.client as _bundle_win32com_client  # type: ignore
except Exception:  # pragma: no cover
    _bundle_win32com_client = None


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


def _resolve_external_python_cmd() -> list[str] | None:
    if os.environ.get("SDV_PYTHON", "").strip():
        return [os.environ["SDV_PYTHON"].strip()]
    if shutil.which("python"):
        return ["python"]
    if shutil.which("py"):
        return ["py", "-3"]
    return None


def _run_python_script(script_path: Path, script_args: list[str]) -> int:
    old_argv = sys.argv[:]
    old_cwd = Path.cwd()
    sys.argv = [str(script_path), *script_args]
    try:
        if script_path.parent.exists():
            os.chdir(script_path.parent)
        runpy.run_path(str(script_path), run_name="__main__")
        return 0
    except SystemExit as ex:
        code = ex.code
        if isinstance(code, int):
            return code
        if code is None:
            return 0
        return 1
    finally:
        sys.argv = old_argv
        os.chdir(old_cwd)


def _run_external_python(script_path: Path, script_args: list[str], cwd: Path) -> int | None:
    py_cmd = _resolve_external_python_cmd()
    if not py_cmd:
        return None
    cmd = [*py_cmd, str(script_path), *script_args]
    proc = subprocess.run(cmd, cwd=cwd)
    return proc.returncode


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
        # Embedded script execution path for subprocess([sys.executable, <script.py>, ...])
        # so that sdv.exe can run without external Python.
        if args and args[0].lower().endswith(".py"):
            script_path = Path(args[0])
            if not script_path.is_absolute():
                script_path = (repo_root / script_path).resolve()
            try:
                return _run_python_script(script_path, args[1:])
            except Exception as ex:  # fallback to external python if embedded path fails
                rc = _run_external_python(script_path, args[1:], repo_root)
                if rc is not None:
                    return rc
                print(
                    f"[SDV][FAIL] Embedded script execution failed and no external Python found: {ex}",
                    file=sys.stderr,
                )
                return 3

        # Main entry: run scripts/run.py embedded first, then fallback.
        try:
            return _run_python_script(run_py, args)
        except Exception as ex:
            rc = _run_external_python(run_py, args, repo_root)
            if rc is not None:
                return rc
            print(
                f"[SDV][FAIL] Embedded mode failed and no external Python found: {ex}",
                file=sys.stderr,
            )
            return 3

    cmd = [sys.executable, str(run_py), *args]
    proc = subprocess.run(cmd, cwd=repo_root)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

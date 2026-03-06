#!/usr/bin/env python3
"""Build sdv CLI executable using PyInstaller.

Baseline policy:
- onefolder first (default)
- onefile optional
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build sdv exe bundle")
    parser.add_argument("--mode", choices=["onefolder", "onefile"], default="onefolder")
    parser.add_argument("--clean", action="store_true", help="Remove previous build output before building")
    return parser.parse_args()


def resolve_pyinstaller_cmd() -> list[str] | None:
    """Prefer the current interpreter environment, then fallback to PATH."""
    probe = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--version"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if probe.returncode == 0:
        return [sys.executable, "-m", "PyInstaller"]

    pyinstaller_bin = shutil.which("pyinstaller")
    if pyinstaller_bin:
        return [pyinstaller_bin]
    return None


def run(cmd: list[str]) -> int:
    print("[RUN]", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def main() -> int:
    args = parse_args()
    pyinstaller_cmd = resolve_pyinstaller_cmd()
    if not pyinstaller_cmd:
        print("[FAIL] pyinstaller not found. Install with: python -m pip install pyinstaller")
        return 2

    dist_root = ROOT / "dist" / "sdv_cli"
    work_root = ROOT / "build" / "pyinstaller"
    spec_root = ROOT / "build" / "spec"

    if args.clean:
        shutil.rmtree(dist_root, ignore_errors=True)
        shutil.rmtree(work_root, ignore_errors=True)
        shutil.rmtree(spec_root, ignore_errors=True)

    dist_root.mkdir(parents=True, exist_ok=True)
    work_root.mkdir(parents=True, exist_ok=True)
    spec_root.mkdir(parents=True, exist_ok=True)

    cmd = pyinstaller_cmd + [
        "--noconfirm",
        "--name",
        "sdv",
        "--distpath",
        str(dist_root),
        "--workpath",
        str(work_root),
        "--specpath",
        str(spec_root),
    ]

    if args.mode == "onefile":
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    cmd.append(str(ROOT / "sdv_cli.py"))

    rc = run(cmd)
    if rc != 0:
        return rc

    mode_path = dist_root / ("sdv.exe" if args.mode == "onefile" else "sdv")
    print(f"[OK] build completed: {mode_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

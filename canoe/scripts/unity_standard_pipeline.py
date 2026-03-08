#!/usr/bin/env python3
"""
CANoe + Unity standard pipeline runner.

Standard policy:
- Use a single runtime Unity project target.
- Keep CAPL as logic source and Unity as renderer adapter.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


DEFAULT_TARGET_REL = Path("canoe/reference/oss_panels/coupled_sim_unity_ref")
DEFAULT_REPORT_REL = Path("canoe/docs/operations/unity/UNITY_SYNC_VERIFICATION_STANDARD.md")


def run_cmd(cmd: List[str], cwd: Path) -> None:
    print(f"[STD] run: {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=str(cwd))
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}")


def ensure_unity_root(path: Path) -> None:
    if not (path / "Assets").is_dir():
        raise FileNotFoundError(f"Unity Assets folder not found: {path / 'Assets'}")
    if not (path / "ProjectSettings" / "ProjectVersion.txt").is_file():
        raise FileNotFoundError(
            f"Unity ProjectVersion.txt not found: {path / 'ProjectSettings' / 'ProjectVersion.txt'}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run standard CANoe+Unity setup pipeline")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Repository root path",
    )
    parser.add_argument(
        "--target-project",
        default="",
        help="Unity project root path (default: coupled_sim_unity_ref)",
    )
    parser.add_argument(
        "--mode",
        choices=["prepare", "verify", "all", "print"],
        default="all",
        help="Pipeline mode",
    )
    return parser.parse_args()


def print_runtime_steps(repo_root: Path, target: Path) -> None:
    bridge = repo_root / "canoe/scripts/unity_renderer_bridge.py"
    mock = repo_root / "canoe/scripts/unity_renderer_mock_sender.py"
    print("[STD] Runtime steps")
    print("1) In CANoe: Start Measurement")
    print(f"2) Start bridge: python \"{bridge}\" --host 127.0.0.1 --port 7400 --period-ms 50")
    print(f"3) Open Unity project: {target}")
    print("4) Play scene (ExternalRoadScene first, CabinScene next)")
    print(f"[STD] Offline test (without CANoe): python \"{mock}\" --host 127.0.0.1 --port 7400 --period-ms 50")


def run_prepare(repo_root: Path, target: Path) -> None:
    build = repo_root / "canoe/scripts/build_unity_skin_pack.py"
    sync = repo_root / "canoe/scripts/sync_unity_integration.py"

    run_cmd([sys.executable, str(build), "--clean"], repo_root)
    run_cmd(
        [
            sys.executable,
            str(sync),
            "--target-project",
            str(target),
            "--clean-skin-dir",
        ],
        repo_root,
    )


def run_verify(repo_root: Path, target: Path) -> None:
    verify = repo_root / "canoe/scripts/verify_unity_integration_sync.py"
    report = repo_root / DEFAULT_REPORT_REL
    run_cmd(
        [
            sys.executable,
            str(verify),
            "--target-project",
            str(target),
            "--write-report",
            str(report.relative_to(repo_root).as_posix()),
        ],
        repo_root,
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    if args.target_project:
        target = Path(args.target_project).resolve()
    else:
        target = (repo_root / DEFAULT_TARGET_REL).resolve()

    ensure_unity_root(target)
    print(f"[STD] repo_root={repo_root}")
    print(f"[STD] target_project={target}")
    print(f"[STD] mode={args.mode}")

    if args.mode in ("all", "prepare"):
        run_prepare(repo_root, target)

    if args.mode in ("all", "verify"):
        run_verify(repo_root, target)

    print_runtime_steps(repo_root, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

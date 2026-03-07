#!/usr/bin/env python3
"""Build a portable ZIP bundle for sdv CLI runtime.

Bundle goals:
- immediate team usage without local source repo checkout
- single ZIP containing sdv.exe + required runtime files
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create portable ZIP bundle for sdv CLI")
    parser.add_argument("--mode", choices=["onefolder", "onefile"], default="onefolder")
    parser.add_argument("--clean", action="store_true", help="Remove previous bundle folder/zip before build")
    parser.add_argument("--rebuild-exe", action="store_true", help="Rebuild exe before bundling")
    parser.add_argument("--output-dir", default=str(ROOT / "dist" / "portable"))
    parser.add_argument("--bundle-name", default="sdv_portable")
    parser.add_argument("--zip-name", default="", help="Default: <bundle-name>.zip")
    return parser.parse_args()


def run(cmd: list[str]) -> int:
    print("[RUN]", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def write_quickstart(bundle_root: Path, mode: str) -> None:
    exe_rel = "sdv\\sdv.exe" if mode == "onefolder" else "sdv.exe"
    lines = [
        "# SDV Portable Quickstart",
        "",
        "## 1) Open terminal in this folder",
        "",
        "```powershell",
        ".\\run-sdv.bat contract",
        ".\\run-sdv.bat scenario run --id 4",
        "```",
        "",
        "## 2) Requirements",
        "- CANoe is installed and running when scenario/verify commands are used.",
        "- Use same Windows user/privilege level for CANoe and terminal.",
        "",
        "## 3) Main paths",
        f"- Executable: `{exe_rel}`",
        "- Wrapper: `run-sdv.bat`",
        "- Evidence output: `canoe/logging/evidence/`",
        "- Verification report output: `canoe/tmp/reports/verification/`",
    ]
    (bundle_root / "PORTABLE_QUICKSTART.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wrapper(bundle_root: Path, mode: str) -> None:
    lines = [
        "@echo off",
        "setlocal",
        "set \"SDV_REPO_ROOT=%~dp0\"",
    ]
    if mode == "onefolder":
        lines += [
            "if not exist \"%~dp0sdv\\sdv.exe\" (",
            "  echo [FAIL] sdv\\sdv.exe not found",
            "  exit /b 2",
            ")",
            "\"%~dp0sdv\\sdv.exe\" %*",
        ]
    else:
        lines += [
            "if not exist \"%~dp0sdv.exe\" (",
            "  echo [FAIL] sdv.exe not found",
            "  exit /b 2",
            ")",
            "\"%~dp0sdv.exe\" %*",
        ]
    lines += ["endlocal"]
    (bundle_root / "run-sdv.bat").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()

    output_dir = Path(args.output_dir).resolve()
    bundle_root = output_dir / args.bundle_name
    zip_name = args.zip_name.strip() or f"{args.bundle_name}.zip"
    zip_path = output_dir / zip_name

    if args.rebuild_exe:
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "release" / "build_sdv_exe.py"),
            "--mode",
            args.mode,
        ]
        if args.clean:
            cmd.append("--clean")
        rc = run(cmd)
        if rc != 0:
            return rc

    exe_dir = ROOT / "dist" / "sdv_cli" / "sdv"
    exe_file = ROOT / "dist" / "sdv_cli" / "sdv.exe"
    if args.mode == "onefolder" and not exe_dir.exists():
        print(f"[FAIL] exe folder not found: {exe_dir}")
        print("hint: run --rebuild-exe or build exe first")
        return 2
    if args.mode == "onefile" and not exe_file.exists():
        print(f"[FAIL] exe file not found: {exe_file}")
        print("hint: run --rebuild-exe --mode onefile or build exe first")
        return 2

    if args.clean:
        shutil.rmtree(bundle_root, ignore_errors=True)
        if zip_path.exists():
            zip_path.unlink()

    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_root.mkdir(parents=True, exist_ok=True)

    # Runtime root marker expected by sdv_cli.py
    copy_file(ROOT / "AGENTS.md", bundle_root / "AGENTS.md")

    # CLI runtime scripts
    copy_tree(ROOT / "scripts", bundle_root / "scripts")

    # Minimal docs required by verify bind-doc/fill-template commands
    docs_root = bundle_root / "driving-situation-alert"
    docs_root.mkdir(parents=True, exist_ok=True)
    for rel in [
        "05_Unit_Test.md",
        "06_Integration_Test.md",
        "07_System_Test.md",
        "TMP_HANDOFF.md",
    ]:
        src = ROOT / "driving-situation-alert" / rel
        if src.exists():
            copy_file(src, docs_root / rel)

    # Onboarding quick runbook
    runbook = ROOT / "canoe" / "tmp" / "onboarding" / "VERIFY_EXECUTION_RUNBOOK.md"
    if runbook.exists():
        copy_file(runbook, bundle_root / "canoe" / "tmp" / "onboarding" / "VERIFY_EXECUTION_RUNBOOK.md")

    # Output folders expected by verify workflow
    (bundle_root / "canoe" / "logging" / "evidence").mkdir(parents=True, exist_ok=True)
    (bundle_root / "canoe" / "tmp" / "reports" / "verification").mkdir(parents=True, exist_ok=True)

    # Executable payload
    if args.mode == "onefolder":
        copy_tree(exe_dir, bundle_root / "sdv")
    else:
        copy_file(exe_file, bundle_root / "sdv.exe")

    write_wrapper(bundle_root, args.mode)
    write_quickstart(bundle_root, args.mode)

    archive_base = output_dir / args.bundle_name
    if zip_path.exists():
        zip_path.unlink()
    created = shutil.make_archive(str(archive_base), "zip", root_dir=output_dir, base_dir=args.bundle_name)
    if Path(created).name != zip_name:
        Path(created).replace(zip_path)

    print(f"[OK] portable folder: {bundle_root}")
    print(f"[OK] portable zip:    {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


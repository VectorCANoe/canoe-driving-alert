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

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.release.layout import (
    EXE_ONEFILE_PATH,
    EXE_ONEFOLDER_DIR,
    PORTABLE_BUNDLE_NAME,
    PORTABLE_DIST_ROOT,
    ROOT,
)


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else (ROOT / path)


def _rel(path: Path) -> str:
    path = _repo_path(path)
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create portable ZIP bundle for sdv CLI")
    parser.add_argument("--mode", choices=["onefolder", "onefile"], default="onefolder")
    parser.add_argument("--clean", action="store_true", help="Remove previous bundle folder/zip before build")
    parser.add_argument("--rebuild-exe", action="store_true", help="Rebuild exe before bundling")
    parser.add_argument("--output-dir", default=str(PORTABLE_DIST_ROOT))
    parser.add_argument("--bundle-name", default=PORTABLE_BUNDLE_NAME)
    parser.add_argument("--zip-name", default="", help="Default: <bundle-name>.zip")
    return parser.parse_args()


def run(cmd: list[str]) -> int:
    print("[RUN]", " ".join(_display_arg(arg) for arg in cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def _display_arg(value: str) -> str:
    if value == sys.executable:
        return Path(value).name
    candidate = Path(value)
    return _rel(candidate) if candidate.is_absolute() else value


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def copy_runtime_scripts(bundle_root: Path) -> None:
    scripts_root = bundle_root / "scripts"
    scripts_root.mkdir(parents=True, exist_ok=True)
    copy_file(ROOT / "scripts" / "run.py", scripts_root / "run.py")
    for name in ("gates", "quality", "release"):
        copy_tree(ROOT / "scripts" / name, scripts_root / name)


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
        "set \"SDV_REPO_ROOT=%~dp0.\"",
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

    output_dir = _repo_path(Path(args.output_dir))
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

    exe_dir = EXE_ONEFOLDER_DIR
    exe_file = EXE_ONEFILE_PATH
    if args.mode == "onefolder" and not exe_dir.exists():
        print(f"[FAIL] exe folder not found: {_rel(exe_dir)}")
        print("hint: run --rebuild-exe or build exe first")
        return 2
    if args.mode == "onefile" and not exe_file.exists():
        print(f"[FAIL] exe file not found: {_rel(exe_file)}")
        print("hint: run --rebuild-exe --mode onefile or build exe first")
        return 2

    if args.clean:
        shutil.rmtree(bundle_root, ignore_errors=True)
        if zip_path.exists():
            zip_path.unlink()

    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_root.mkdir(parents=True, exist_ok=True)

    # Minimal root files expected by sdv_cli.py
    copy_file(ROOT / "pyproject.toml", bundle_root / "pyproject.toml")
    copy_file(ROOT / "sdv_cli.py", bundle_root / "sdv_cli.py")

    # CLI runtime scripts limited to the packaged product surface
    copy_runtime_scripts(bundle_root)
    copy_tree(ROOT / "product" / "sdv_operator", bundle_root / "product" / "sdv_operator")

    # Minimal docs required by verify bind-doc/fill-template commands
    docs_root = bundle_root / "driving-alert-workproducts"
    docs_root.mkdir(parents=True, exist_ok=True)
    for rel in [
        "05_Unit_Test.md",
        "06_Integration_Test.md",
        "07_System_Test.md",
    ]:
        src = ROOT / "driving-alert-workproducts" / rel
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

    print(f"[OK] portable folder: {_rel(bundle_root)}")
    print(f"[OK] portable zip:    {_rel(zip_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

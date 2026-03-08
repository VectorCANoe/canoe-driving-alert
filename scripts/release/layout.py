from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST_ROOT = ROOT / "dist"
EXE_DIST_ROOT = DIST_ROOT / "sdv_cli"
EXE_ONEFOLDER_DIR = EXE_DIST_ROOT / "sdv"
EXE_ONEFILE_PATH = EXE_DIST_ROOT / "sdv.exe"
PORTABLE_DIST_ROOT = DIST_ROOT / "portable"
PORTABLE_BUNDLE_NAME = "sdv_portable"
PORTABLE_ZIP_PATH = PORTABLE_DIST_ROOT / f"{PORTABLE_BUNDLE_NAME}.zip"
PORTABLE_FOLDER_PATH = PORTABLE_DIST_ROOT / PORTABLE_BUNDLE_NAME
PYINSTALLER_WORK_ROOT = ROOT / "build" / "pyinstaller"
PYINSTALLER_SPEC_ROOT = ROOT / "build" / "spec"

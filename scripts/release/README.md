# Release Scripts

This folder contains packaging/distribution scripts for CLI delivery.

## Build sdv exe (PyInstaller)

From repository root:

- Install dependency:
  - `python -m pip install pyinstaller`

- One-folder (recommended baseline):
  - `python scripts/run.py package build-exe --mode onefolder --clean`
- One-file (optional):
  - `python scripts/run.py package build-exe --mode onefile --clean`

Direct script usage:

- `python scripts/release/build_sdv_exe.py --mode onefolder --clean`
- `python scripts/release/build_portable_bundle.py --mode onefolder --clean --rebuild-exe`

## Output

- One-folder:
  - `dist/sdv_cli/sdv/`
- One-file:
  - `dist/sdv_cli/sdv.exe`

- Portable ZIP:
  - `dist/portable/sdv_portable.zip`
  - extracted folder includes:
    - `run-sdv.bat`
    - `sdv/` (or `sdv.exe` in onefile mode)
    - `scripts/` runtime
    - minimal docs for verify doc-binding (`driving-situation-alert/05/06/07`)

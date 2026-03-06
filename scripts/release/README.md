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

## Output

- One-folder:
  - `dist/sdv_cli/sdv/`
- One-file:
  - `dist/sdv_cli/sdv.exe`

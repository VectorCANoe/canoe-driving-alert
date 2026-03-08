# Packaging Scope

This file defines what belongs in the packaged `SDV Operator` distribution.

## Include

### Entry and metadata
- `pyproject.toml`
- `sdv_cli.py`

### Product launcher/UI
- `scripts/run.py`
- `scripts/tui_app.py`
- `scripts/cliops/`

### Product backend
- `scripts/gates/`
- `scripts/quality/`
- `scripts/release/`

### Runtime dependencies
- packaged Python runtime or frozen executable output
- generated entrypoint `sdv.exe` / `sdv`

## Exclude

### CANoe runtime project assets
- `canoe/cfg/`
- `canoe/project/panel/`
- `canoe/project/sysvars/`
- `canoe/databases/`
- `canoe/src/capl/`

Reason:
- those belong to the CANoe project and Dev1 runtime ownership
- they are not part of the CLI/TUI product binary itself

### Non-product helper/legacy areas
- `scripts/docs/`
- `scripts/report/`
- `scripts/canoe/`
- `canoe/scripts/`
- `reference/`
- `legacy_projects/`

### Generated working outputs
- `canoe/tmp/reports/verification/`
- `canoe/logging/evidence/`
- `canoe/cfg/.run/`
- `dist/` previous outputs

## Fixed Artifact Paths

- one-folder exe: `dist/sdv_cli/sdv/`
- one-file exe: `dist/sdv_cli/sdv.exe`
- portable folder: `dist/portable/sdv_portable/`
- portable zip: `dist/portable/sdv_portable.zip`
- PyInstaller work: `build/pyinstaller/`
- PyInstaller spec: `build/spec/`

## Distribution Principle

The packaged product should be:

- small enough to hand over
- stable enough to run the same commands
- clear enough that operators do not browse the repository to use it

The repository can remain large.
The packaged product must remain narrow.

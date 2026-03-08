# Scripts Guide

This folder is the automation surface for the project.

Important:

- not everything under `scripts/` is the product
- the packaged product boundary is defined in:
  - `product/sdv_operator/README.md`

## Start Here
Use one entrypoint only:

- `python scripts/run.py`
- `sdv <command>` after local install

If you need orientation, read these in order:

1. `scripts/MAINTENANCE_MAP.md`
2. `scripts/COMMAND_REFERENCE.md`
3. `scripts/SCRIPT_INVENTORY.md`
4. `product/sdv_operator/README.md`

## Canonical Daily Surface
Ordinary operators should stay on these workflows:

1. `python scripts/run.py gate all`
2. `python scripts/run.py scenario run --id <n>`
3. `python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>`
4. `python scripts/run.py doctor`

Interpretation:

- `run.py` is the single public launcher
- `tui_app.py` is the review console behind that launcher
- `cliops/*`, `quality/*`, and `gates/*` are internal implementation layers
- compatibility aliases still work, but are hidden from normal help

## Runtime Policy

Cross-platform:

- shell/TUI UX
- gates
- verification report generation
- packaging helpers

Windows-only:

- `doctor`
- `scenario run`
- `capl sysvar-*`
- `canoe measure-*`
- `canoe capl-call`

Reason:

- CANoe COM automation is Windows-only

## Main Working Modes

### 1. Operator TUI
- `python scripts/run.py`
- default path for daily operation and review

### 2. Plain shell fallback
- `python scripts/run.py shell`
- conservative fallback when TUI is not desired

### 3. Guided mode
- `python scripts/run.py start guided`
- menu-driven fallback for operators

## Packaging

Local editable install:

- `python -m pip install -e .`

Portable packaging:

- `python scripts/run.py package build-exe --mode onefolder --clean`
- `python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe`

## Folder Roles

- `scripts/cliops/`: command parsing and runtime implementation
- `scripts/gates/`: quality gates
- `scripts/quality/`: verification/evidence engines
- `scripts/canoe/`: advanced CANoe maintenance helpers
- `scripts/release/`: packaging helpers
- `scripts/docs/`, `scripts/report/`: legacy/maintenance scripts, not daily operator surface

## Complexity Rule

If a teammate asks "What do I run?", the answer should remain:

1. `python scripts/run.py`
2. `gate all`
3. `scenario run`
4. `verify quick`

If the answer requires explaining many subfolders, the public surface is too large.

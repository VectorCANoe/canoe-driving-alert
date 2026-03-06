# Scripts Guide

Use this folder through one entrypoint:

- `python scripts/run.py <command>`

## Daily Commands

### Verification
- Prepare run folders:
  - `python scripts/run.py verify-prepare --run-id 20260306_1930`
- Smoke check (CANoe COM):
  - `python scripts/run.py verify-smoke --owner DEV1`
- Fill + score one tier:
  - `python scripts/run.py verify-fill-score --tier UT --run-id 20260306_1930 --owner DEV1`

### Gates
- Doc/code sync:
  - `python scripts/run.py gate-doc-sync`
- CANoe cfg hygiene:
  - `python scripts/run.py gate-cfg-hygiene`
- CAPL mirror sync (`src/capl` vs `cfg/channel_assign`):
  - `python scripts/run.py gate-capl-sync`

## Folder Roles

- `scripts/quality/`: validation and evidence pipeline
- `scripts/canoe/`: CANoe setup/reload helpers
- `scripts/docs/`: doc-authoring helpers (not day-to-day dev runtime)
- `scripts/report/`: report conversion/export helpers

## Recommended Rule

- Daily work: only use `scripts/run.py`
- Low-level scripts: call directly only when debugging a specific tool

## Compatibility

- `scripts/doc_code_sync_gate.py` is a backward-compat wrapper.
- Preferred gate entrypoint remains `scripts/quality/doc_code_sync_gate.py`.

# Scripts Guide

Use this folder through one entrypoint:

- `python scripts/run.py <command>`
- `sdv <command>` (after local install)

## Local CLI Install (F3 Baseline)

From repository root:

- `python -m pip install -e .`

Then you can use:

- `sdv contract`
- `sdv verify prepare --run-id 20260306_1930`
- `sdv gate doc-sync`

## Daily Commands

### Verification
- Prepare run folders:
  - `python scripts/run.py verify prepare --run-id 20260306_1930`
  - `sdv verify prepare --run-id 20260306_1930`
- Smoke check (CANoe COM):
  - `python scripts/run.py verify smoke --owner DEV1`
  - `sdv verify smoke --owner DEV1`
- Fill + score one tier:
  - `python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner DEV1`
  - `sdv verify fill-score --tier UT --run-id 20260306_1930 --owner DEV1`
  - (optional baseline) `python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner DEV1 --baseline-csv canoe/logging/evidence/UT/20260305_1800/verification_log_scored.csv`
- Build run-level insight report (UT/IT/ST merge):
  - `python scripts/run.py verify insight --run-id 20260306_1930`
  - `sdv verify insight --run-id 20260306_1930`
  - (optional baseline run) `python scripts/run.py verify insight --run-id 20260306_1930 --baseline-run-id 20260305_1800`
- Build 05/06/07 doc binding bundle:
  - `python scripts/run.py verify bind-doc --run-id 20260306_1930`
  - `sdv verify bind-doc --run-id 20260306_1930`
- Build 05/06/07 doc fill template:
  - `python scripts/run.py verify fill-template --run-id 20260306_1930 --owner-fallback DEV1`
  - `sdv verify fill-template --run-id 20260306_1930 --owner-fallback DEV1`
- Check run readiness (missing raw log / marker / scored file):
  - `python scripts/run.py verify status --run-id 20260306_1930`
  - `sdv verify status --run-id 20260306_1930`
- One-shot finalize (fill-score UT/IT/ST + insight + fill-template):
  - `python scripts/run.py verify finalize --run-id 20260306_1930 --owner DEV1`
  - `sdv verify finalize --run-id 20260306_1930 --owner DEV1`

### Gates
- Doc/code sync:
  - `python scripts/run.py gate doc-sync`
  - `sdv gate doc-sync`
- CANoe cfg hygiene:
  - `python scripts/run.py gate cfg-hygiene`
  - `sdv gate cfg-hygiene`
- CAPL mirror sync (`src/capl` vs `cfg/channel_assign`):
  - `python scripts/run.py gate capl-sync`
  - `sdv gate capl-sync`
- CLI readiness (before GUI phase):
  - `python scripts/run.py gate cli-readiness`
  - `sdv gate cli-readiness`

### Packaging
- Build exe one-folder baseline:
  - `python scripts/run.py package build-exe --mode onefolder --clean`
- Build exe one-file:
  - `python scripts/run.py package build-exe --mode onefile --clean`

## Folder Roles

- `scripts/gates/`: official quality gate implementations
- `scripts/quality/`: validation and evidence pipeline
- `scripts/canoe/`: CANoe setup/reload helpers
- `scripts/docs/`: doc-authoring helpers (not day-to-day dev runtime)
- `scripts/report/`: report conversion/export helpers
- `scripts/release/`: CLI packaging/distribution scripts

## Recommended Rule

- Daily work: only use `scripts/run.py`
- Low-level scripts: call directly only when debugging a specific tool
- Script governance/inventory: `scripts/SCRIPT_INVENTORY.md`
- Gate overview/mapping: `scripts/GATE_MATRIX.md`
- End-to-end operational playbook: `canoe/docs/operations/VERIFICATION_INSIGHT_PLAYBOOK.md`
- Team quick runbook (Korean ops note): `canoe/tmp/onboarding/VERIFY_EXECUTION_RUNBOOK.md`

## Compatibility

- Preferred gate script paths are under `scripts/gates/`.
- Legacy flat commands are still accepted (`verify-prepare`, `gate-doc-sync`, ...).
- Print canonical contract: `python scripts/run.py contract`

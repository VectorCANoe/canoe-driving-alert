# Scripts Guide

Use this folder through one entrypoint:

- `python scripts/run.py <command>`
- `sdv <command>` (after local install)
- `python scripts/run.py` (no args -> guided menu)

## Local CLI Install (F3 Baseline)

From repository root:

- `python -m pip install -e .`

Then you can use:

- `sdv contract`
- `sdv verify prepare --run-id 20260306_1930`
- `sdv gate doc-sync`

## Daily Commands

### Quick Entry (New)
- Menu-style guided flow (recommended for operators):
  - `python scripts/run.py start guided`
  - `python scripts/run.py go`
  - `sdv start guided`
  - Menu supports numeric selection (`1..11`) and typed inputs (`run-id`, `owner`, `scenario id`).
  - Includes startup banner + action loading spinner + silent exit option.
- Operator-first demo trigger:
  - `python scripts/run.py start demo --id 4`
  - `python scripts/run.py demo --id 4`
  - `sdv start demo --id 4`
- Precheck batch (gates + prepare + smoke + status):
  - `python scripts/run.py start precheck`  (auto run-id + default owner)
  - `python scripts/run.py precheck`
  - `sdv start precheck --owner DEV2`
- Environment doctor:
  - `python scripts/run.py doctor`
  - `python scripts/run.py doctor --ensure-running`
  - `sdv doctor`
- CAPL-linked sysvar access:
  - `python scripts/run.py capl sysvar-get --namespace Core --var failSafeMode`
  - `python scripts/run.py capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int`
  - `sdv capl sysvar-get --namespace Test --var scenarioCommandAck`
- CANoe control plane:
  - `python scripts/run.py canoe measure-status`
  - `python scripts/run.py canoe measure-start`
  - `python scripts/run.py canoe measure-stop`
  - `python scripts/run.py canoe measure-reset`
  - `python scripts/run.py canoe capl-call --function-name MyFunction --args 1 2 --arg-type int`
- Evidence shortcuts:
  - `sdv evidence status --run-id 20260308_1900`
  - `sdv evidence insight --run-id 20260308_1900`
- Release shortcuts:
  - `sdv release exe --mode onefolder --clean`
  - `sdv release portable --mode onefolder --clean --rebuild-exe`
  - `python scripts/run.py mstatus|mstart|mstop`

### Interactive UX Backbone
- UX benchmark base: `questionary` (single open-source prompt library).
- CLI visual UX: `rich` (banner/panel/status spinner).
- Install (recommended):
  - `python -m pip install questionary>=2.1.1`
  - `python -m pip install rich>=13.7.1`
- If not installed, CLI falls back to plain `input()` prompts automatically.

### Interactive Shell (Recommended)
- Slash-command shell (no command memorization):
  - `python scripts/run.py shell`
  - `sdv shell`
- Example session:
  - `/start guided`
  - `/start precheck`
  - `/scenario 4`
  - `/verify batch 20260308_0900 DEV2 pre`
  - `/canoe measure status`
  - `/gate all`
  - `/skill list`
  - `/exit`

### Scenario Trigger (No Panel)
- Send one scenario command to running CANoe via COM:
  - `python scripts/run.py scenario run --id 4`
  - `sdv scenario run --id 4`
- Optional options:
  - `--var scenarioCommand|testScenario` (default: `scenarioCommand`)
  - `--wait-ack-ms 1200` (ack timeout)
  - `--no-ensure-running` (do not auto-start measurement)

### Verification
- Prepare run folders:
  - `python scripts/run.py verify prepare --run-id 20260306_1930`
  - `sdv verify prepare --run-id 20260306_1930`
- Dev2 batch workflow (recommended):
  - pre-check batch (gates + prepare + smoke + status):
    - `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase pre`
  - post-run batch (finalize + status):
    - `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase post`
  - full batch (pre + post, only when raw evidence is ready):
    - `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase full`
  - report format selection (default `json,md`, optional `csv`):
    - `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase pre --report-formats json,md`
    - `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase pre --report-formats json,md,csv`
  - standard outputs:
    - canonical machine: `canoe/tmp/reports/verification/dev2_batch_report.json`
    - human review: `canoe/tmp/reports/verification/dev2_batch_report.md`
    - optional interchange: `canoe/tmp/reports/verification/dev2_batch_report.csv`
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
- Multi-bus cfg + DBC domain policy:
  - `python scripts/run.py gate multibus-dbc`
  - `sdv gate multibus-dbc`
- CLI readiness (before GUI phase):
  - `python scripts/run.py gate cli-readiness`
  - `sdv gate cli-readiness`

### Packaging
- Build exe one-folder baseline:
  - `python scripts/run.py package build-exe --mode onefolder --clean`
- Build exe one-file:
  - `python scripts/run.py package build-exe --mode onefile --clean`
- Build portable ZIP (team handoff):
  - `python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe`
  - output: `dist/portable/sdv_portable.zip`

## Folder Roles

- `scripts/gates/`: official quality gate implementations
- `scripts/quality/`: validation and evidence pipeline
- `scripts/canoe/`: CANoe setup/reload helpers
- `scripts/docs/`: doc-authoring helpers (not day-to-day dev runtime)
- `scripts/report/`: report conversion/export helpers
- `scripts/release/`: CLI packaging/distribution scripts

## CLI Architecture (Practical BP)

- Command layer: `scripts/run.py` (`start/doctor/evidence/release/...`)
- Adapter layer: CANoe COM + sysvar contract (`scripts/cliops/canoe_com.py`, `capl sysvar-*`, `canoe measure-*`)
- Evidence layer: JSON canonical + MD review + optional CSV
- Runtime truth: CAPL nodes consume/produce sysvars in CANoe measurement; CLI triggers and observes via COM

## Recommended Rule

- Daily work: only use `scripts/run.py`
- Low-level scripts: call directly only when debugging a specific tool
- Script governance/inventory: `scripts/SCRIPT_INVENTORY.md`
- Gate overview/mapping: `scripts/GATE_MATRIX.md`
- End-to-end operational playbook: `canoe/docs/operations/VERIFICATION_INSIGHT_PLAYBOOK.md`
- Team quick runbook (Korean ops note): `canoe/tmp/onboarding/VERIFY_EXECUTION_RUNBOOK.md`

## Compatibility

- Preferred gate script paths are under `scripts/gates/`.
- New preferred entrypoints: `start`, `doctor`, `evidence`, `release`.
- Legacy flat commands are still accepted (`verify-prepare`, `gate-doc-sync`, ...).
- Print canonical contract: `python scripts/run.py contract`

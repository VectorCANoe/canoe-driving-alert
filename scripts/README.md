# Scripts Guide

Use this folder through one entrypoint:

- `python scripts/run.py <command>`
- `sdv <command>` (after local install)
- `python scripts/run.py` (no args -> Textual TUI on interactive terminal, shell fallback otherwise)

## Runtime Policy

- Common on Windows/macOS/Linux:
  - shell/TUI UX
  - gates
  - verification reports and evidence formatting
  - packaging helpers
- Windows-only:
  - `doctor`
  - `scenario run`
  - `capl sysvar-*`
  - `canoe measure-*`
  - `canoe capl-call`
- Reason:
  - CANoe COM automation is Windows-only. The CLI UX is cross-platform, but CANoe execution is not.

## Local CLI Install (F3 Baseline)

From repository root:

- `python -m pip install -e .`

Then you can use:

- `sdv contract`
- `sdv verify prepare --run-id 20260306_1930`
- `sdv gate doc-sync`

## Primary Daily Commands

The operator surface is intentionally centered on three workflows:

1. `python scripts/run.py gate all`
2. `python scripts/run.py scenario run --id 4`
3. `python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2`

Everything else in this folder exists to support those three actions.

## Daily Commands

### Quick Entry (New)
- Single default entry:
  - `python scripts/run.py`
  - Starts the Textual operator console when running in an interactive terminal.
  - Falls back to the plain shell when TUI is unavailable.
- Product operator console:
  - `python scripts/run.py tui`
  - `sdv tui`
  - Designed as a thin launcher for the three daily workflows: `Gate all -> Scenario run -> Verify quick`.
  - Users choose a task first, then fill only the required values on the right panel.
  - `run-id` is auto-filled with the current timestamp, and repeated values remain visible in the form.
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
- Product UI: `Textual` (category layout, detail pane, live execution log).
- CLI visual UX: `rich` (banner/panel/status spinner in fallback shell/guided mode).
- Guided prompt UX: `questionary` (select/text forms only, not the main shell REPL).
- Input model:
  - default: Textual operator console
  - guided/forms: questionary-enhanced prompts when available
  - fallback: plain `sdv>` prompt + numeric selection for stability in PowerShell/CANoe environments
- Install (recommended):
  - `python -m pip install \"questionary>=2.1.1,<3\" \"rich>=14,<15\" \"textual>=8,<9\"`

### Interactive Shell (Recommended)
- Slash-command shell (no command memorization):
  - `python scripts/run.py shell`
  - `sdv shell`
- Default mode:
  - `python scripts/run.py`
  - Opens TUI first; use `shell` explicitly when you want the conservative REPL fallback.
- Textual flow:
  - left sidebar screens:
    - `Home`
    - `Execute`
    - `Results`
    - `Logs`
  - `Home`: daily 3-step path and quick jump buttons
  - `Execute`: one operator workspace; switch task groups inside the page (`Primary / Runtime / Inspect / Package`)
  - command selection does not run immediately; pick a task, adjust inputs, then press `Run now` or `r`
  - `Results`: pinned tasks / recent runs / run insight / last result / readiness / batch / COM runtime / timeline
  - `Logs`: full-width live execution log with filter buttons and live stage/output summary
  - run behavior: pressing `Run` moves to `Logs` automatically; after completion, inspect `Results`
  - `COM runtime` card: use it first when scenario/verify fails to see whether the break is at attach, measurement, sysvar, or ack
  - `recent runs` list: selectable; press `Enter` on a recent task to rerun it
  - log filters: `F1 All`, `F2 Warn`, `F3 Fail`, `F4 Verify`, `F5 CANoe`
  - artifact shortcuts: `Ctrl+O` open first evidence path, `Ctrl+Y` copy first evidence path
  - keys: `Ctrl+R` run, `Ctrl+P` pin current task, `Ctrl+X` rerun latest, `Ctrl+B` jump to results, `Ctrl+N` focus recent list, `Ctrl+G` focus navigation, `Ctrl+T` focus commands, `Ctrl+F` focus form, `Ctrl+L` focus log, `q` quit
- Grouped command palette:
  - `/palette`
  - First choose group: `Primary Workflow / Runtime Support / System Access / Packaging / Session`
  - Then choose command by number
- Command history and replay:
  - `/history` or `/history 20`
  - `/repeat` (last command), `/repeat 2` (second latest)
- Example session:
  - `/gate all`
  - `/scenario 4`
  - `/verify quick 20260308_0900 DEV2`
  - `/canoe measure status`
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
- Quick operator pass (recommended daily verification path):
  - `python scripts/run.py verify quick`
  - `python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2`
  - `sdv verify quick --run-id 20260308_0900 --owner DEV2`
  - defaults:
    - `run-id`: current timestamp (`YYYYMMDD_HHMM`)
    - `owner`: `DEV2`
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

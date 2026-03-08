# TUI Direction

## 1. Purpose
- This TUI is not a replacement for CANoe.
- CANoe remains the execution environment and panel/operator UI.
- The TUI is the verification operator console for:
  - running the standard workflow
  - reviewing PASS/WARN/FAIL
  - locating evidence and bottlenecks quickly

## 2. Product Boundary
### In scope
- `gate all`
- `scenario run`
- `verify quick`
- COM runtime visibility
- evidence path review
- recent run replay
- log filtering and failure drill-down

### Out of scope
- re-implementing CANoe panels in Python
- replacing CANoe measurement setup/configuration GUI
- creating a second product-operation HMI outside CANoe

## 3. Core Philosophy
- Complexity stays in code and pipeline.
- The operator surface must remain simple.
- The first screen should answer only three questions:
  1. Is the project ready to run?
  2. Which scenario should I trigger?
  3. Did verification pass, warn, or fail?

This follows a product principle:
- powerful internals
- low operator friction
- clear next action

## 4. Interaction Model
### Execution layer
- CLI is the source of truth for execution.
- Standard commands:
  - `python scripts/run.py gate all`
  - `python scripts/run.py scenario run --id <n>`
  - `python scripts/run.py verify quick`

### Review layer
- TUI is the primary review surface.
- It should expose:
  - run status
  - COM health
  - evidence paths
  - recent history
  - bottleneck summary
  - live logs

## 5. Screen Model
### Home
- show only the three core actions:
  - Gate all
  - Scenario run
  - Verify quick
- also show:
  - latest result
  - current bottleneck
  - recent runs summary

### Execute
- choose a task
- edit only required parameters
- run once
- move automatically to Logs while running

### Results
- inspect:
  - PASS/WARN/FAIL
  - evidence paths
  - tier readiness
  - batch snapshot
  - COM runtime
  - execution timeline

### Logs
- show live execution log
- support filtered views:
  - All
  - Warn
  - Fail
  - Verify
  - CANoe

## 6. Why This Exists
This tool is justified only if it provides something the team does not get easily from raw CANoe usage alone:
- repeatable team workflow without memorizing commands
- evidence-first verification review
- one consistent operator path across team members
- direct COM-based automation with visible runtime state

If the TUI becomes decoration without improving verification clarity, it is the wrong investment.

## 7. Current Decision
- Keep CLI as execution SoT.
- Keep TUI as verification/review console.
- Do not build a separate Python control GUI for CANoe behavior.
- If a future GUI is added, it must be a report viewer, not a CANoe replacement.

## 8. Immediate Quality Bar
The TUI is acceptable only when:
- the operator can understand the first screen in under 10 seconds
- the three core actions are obvious without reading a manual
- FAIL/WARN always shows a direct reason and next action
- evidence paths are visible without searching the filesystem
- live logs are readable during execution

## 9. Reference Patterns
The current TUI follows three external reference patterns:

### Trogon
- source: `Textualize/trogon`
- adopted idea:
  - command list
  - command info
  - parameter form
- applied here as:
  - Execute page task list
  - structured task info panel
  - quick form + preview

### pgcli
- source: `dbcli/pgcli`
- adopted idea:
  - keep the interactive surface predictable
  - keep the operator entry path narrow
- applied here as:
  - small public command surface
  - shell/CLI remains the execution truth

### aider
- source: `Aider-AI/aider`
- adopted idea:
  - product-facing repo surface should stay thin
  - internal implementation complexity may remain behind that surface
- applied here as:
  - `product/sdv_operator` as public surface
  - implementation remains under `scripts/*`

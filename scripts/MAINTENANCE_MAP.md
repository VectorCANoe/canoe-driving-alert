# Scripts Maintenance Map

## Purpose
This file reduces operational complexity without risky file moves.
Use it to decide what is daily surface, what is internal, and what is legacy.

## 1. Canonical Daily Surface
These are the only commands ordinary operators need day to day.

- `python scripts/run.py`
- `python scripts/run.py gate all`
- `python scripts/run.py scenario run --id <n>`
- `python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>`
- `python scripts/run.py doctor`

Interpretation:
- `run.py` = single public entrypoint
- `tui_app.py` = review console only
- everything else under `scripts/` is support code unless explicitly documented otherwise
- compatibility aliases remain executable, but are intentionally hidden from normal `--help`

## 2. Layer Model
### A. Public operator surface
- `scripts/run.py`
- `scripts/tui_app.py`
- `scripts/README.md`

### B. Internal command/runtime layer
- `scripts/cliops/common.py`
- `scripts/cliops/parser_factory.py`
- `scripts/cliops/command_catalog.py`
- `scripts/cliops/runtime_ops.py`
- `scripts/cliops/verify_ops.py`
- `scripts/cliops/gate_ops.py`
- `scripts/cliops/package_ops.py`
- `scripts/cliops/platform_caps.py`
- `scripts/cliops/shell_ui.py`

Rule:
- These files are implementation detail.
- Do not reference them directly in team runbooks unless the user is maintaining the CLI itself.

### C. Verification engines
- `scripts/quality/*.py`
- `scripts/gates/*.py`

Rule:
- Treat them as backend workers behind `run.py`.
- They may be executed directly during maintenance, but not as the standard team entrypoint.

### D. Advanced CANoe operations
- `scripts/canoe/*.py`
- `canoe/scripts/*.py`

Rule:
- Use only for advanced recovery, simulator sync, panel/unity support, or low-level CANoe maintenance.
- Not part of the normal operator quick path.

### E. Legacy / one-off helpers
- `scripts/docs/*.py`
- `scripts/report/*.py`

Rule:
- Keep them for history and batch maintenance.
- Do not grow these further unless there is a concrete modernization task.

## 3. Current Complexity Policy
### Keep stable
- `run.py` as single launcher
- TUI page model: `Home / Execute / Results / Logs`
- 3-step operator flow:
  - `Gate all`
  - `Scenario run`
  - `Verify quick`

### Do not expand casually
- new top-level command namespaces
- duplicate entrypoints outside `run.py`
- direct Python GUI that tries to replace CANoe panels
- hidden script-only workflows that bypass `run.py`

### Prefer in future refactors
- make new features a `cliops/*_ops.py` module first
- expose them through `run.py` only after the command contract is clear
- keep generated artifacts outside source directories

## 4. Generated Artifacts
Generated outputs belong in working/report folders, not source folders.

Main generated areas:
- `canoe/tmp/reports/verification/`
- `canoe/logging/evidence/`
- `dist/`

Rule:
- review them
- attach them as evidence when needed
- do not treat them as source-of-truth code

## 5. Practical Operator Rule
If a teammate asks "What do I run?", the answer should stay short:

1. `python scripts/run.py`
2. or use:
   - `gate all`
   - `scenario run`
   - `verify quick`

If the answer requires explaining five subfolders, the structure is too complex.

## 6. Refactor Boundary
Allowed now:
- README/index cleanup
- internal module split
- clearer daily-vs-internal boundaries
- reducing duplicate code and dead paths

Not recommended now:
- large folder moves
- renaming broad script trees without updating every reference
- reworking evidence/report locations during active development

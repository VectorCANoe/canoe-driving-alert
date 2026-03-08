# Command Reference

Detailed command examples for the `scripts/run.py` launcher.

## Core Workflows

### Gate all
- `python scripts/run.py gate all`

### Scenario run
- `python scripts/run.py scenario run --id 4`
- `python scripts/run.py scenario run --id 4 --var testScenario`

### Verify quick
- `python scripts/run.py verify quick`
- `python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2`

### Doctor
- `python scripts/run.py doctor`
- `python scripts/run.py doctor --ensure-running`

## Operator Modes

### TUI
- `python scripts/run.py`
- `python scripts/run.py tui`

### Plain shell
- `python scripts/run.py shell`

### Guided flow
- `python scripts/run.py start guided`
- `python scripts/run.py start demo --id 4`
- `python scripts/run.py start precheck --owner DEV2`

## Verification Commands

### Prepare
- `python scripts/run.py verify prepare --run-id 20260306_1930`

### Batch
- `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase pre`
- `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase post`
- `python scripts/run.py verify batch --run-id 20260308_0900 --owner DEV2 --phase full`

### Smoke
- `python scripts/run.py verify smoke --owner DEV1`

### Fill and score
- `python scripts/run.py verify fill-score --tier UT --run-id 20260306_1930 --owner DEV1`

### Insight
- `python scripts/run.py verify insight --run-id 20260306_1930`
- `python scripts/run.py verify insight --run-id 20260306_1930 --baseline-run-id 20260305_1800`

### Bind documentation
- `python scripts/run.py verify bind-doc --run-id 20260306_1930`
- `python scripts/run.py verify fill-template --run-id 20260306_1930 --owner-fallback DEV1`

### Status and finalize
- `python scripts/run.py verify status --run-id 20260306_1930`
- `python scripts/run.py verify finalize --run-id 20260306_1930 --owner DEV1`

## Gate Commands

- `python scripts/run.py gate doc-sync`
- `python scripts/run.py gate cfg-hygiene`
- `python scripts/run.py gate capl-sync`
- `python scripts/run.py gate multibus-dbc`
- `python scripts/run.py gate cli-readiness`

## CAPL and CANoe COM

### SysVar access
- `python scripts/run.py capl sysvar-get --namespace Core --var failSafeMode`
- `python scripts/run.py capl sysvar-set --namespace Test --var scenarioCommand --value 4 --value-type int`

### Measurement control
- `python scripts/run.py canoe measure-status`
- `python scripts/run.py canoe measure-start`
- `python scripts/run.py canoe measure-stop`
- `python scripts/run.py canoe measure-reset`

### CAPL function call
- `python scripts/run.py canoe capl-call --function-name MyFunction --args 1 2 --arg-type int`

## Evidence Aliases

- `python scripts/run.py evidence status --run-id 20260308_0900`
- `python scripts/run.py evidence insight --run-id 20260308_0900`
- `python scripts/run.py evidence finalize --run-id 20260308_0900 --owner DEV2`

## Packaging

- `python scripts/run.py package build-exe --mode onefolder --clean`
- `python scripts/run.py package build-exe --mode onefile --clean`
- `python scripts/run.py package bundle-portable --mode onefolder --clean --rebuild-exe`

## Compatibility Note

Legacy aliases remain executable during transition, but they are intentionally hidden from normal help output.
Use the canonical commands above in runbooks and team guidance.

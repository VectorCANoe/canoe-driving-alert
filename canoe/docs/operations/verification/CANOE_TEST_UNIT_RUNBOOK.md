# CANoe Test Unit Runbook

## Purpose
- Define how Dev1 uses native CANoe Test Unit assets in the current SIL project.
- Keep the harness-first strategy intact:
  - `VAL_SCENARIO_CTRL` drives the scenario
  - `VAL_BASELINE_CTRL` aggregates the baseline result frame
  - Dev2 TUI/CLI remains the external bridge for packaging and CI

## Current PoC Assets
1. `canoe/tests/modules/test_units/TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
2. `canoe/tests/modules/test_units/TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY`

## Harness Contract
- `Test::scenarioCommand`
  - one-shot automation entry
- `Test::scenarioCommandAck`
  - accepted command id
- `Test::scenarioResult`
  - 0/1 validation result from `VAL_SCENARIO_CTRL`
- `frmBaseTestResultMsg (0x2A6)`
  - baseline aggregation frame from `VAL_BASELINE_CTRL`

## Execution Rule
1. Open the active CANoe configuration in the GUI.
2. Register the matching `*.vtestunit.yaml` as a Test Unit asset.
3. Start measurement.
4. Execute the selected Test Unit through the CANoe test UI.
5. Save the report and screenshot as evidence.

## Mapping
| Asset | Scenario | Main Runtime Checks |
|---|---|---|
| `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED` | `2` | `vehicleSpeedNorm`, `speedLimitNorm`, `baseZoneContext`, `selectedAlert*`, `ambient*`, `warningTextCode` |
| `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY` | `18` | `failSafeMode`, `decelAssistReq`, `selectedAlert*`, `warningTextCode`, `frmBaseTestResultMsg` |

## Out of Scope
- Direct patching of `canoe/cfg/*.cfg`
- Replacing Dev2 TUI/CLI
- Broad test architecture redesign

## Follow-up
- Docs team reflects the asset in `04/05/06/07`
- Dev2 may package the generated native report after execution

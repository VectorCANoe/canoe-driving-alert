# Execution Guide

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the current native CANoe SIL execution flow for verification assets.

It is the official execution reference for:

- Test Unit registration and execution
- harness interaction through `TEST_SCN` and `TEST_BAS`
- evidence capture after native execution

## Verification model

The current baseline uses a harness-first execution model.

| Element | Role |
| --- | --- |
| `TEST_SCN` | drives scenario stimulus and sets per-scenario verdict state |
| `TEST_BAS` | aggregates the baseline result through `Test::base*` summary variables |
| native CANoe Test Unit asset | executes the selected verification package inside CANoe |

## Current native assets

Current assets kept as the active native execution baseline:

1. `canoe/tests/modules/test_units/TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION`
2. `canoe/tests/modules/test_units/TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING`

These assets are the current baseline only.
They are not a claim that the full future test architecture is complete.

## Harness contract

The current execution flow depends on the following harness variables:

| Variable | Meaning |
| --- | --- |
| `Test::scenarioCommand` | one-shot execution trigger |
| `Test::scenarioCommandAck` | accepted command identifier |
| `Test::scenarioResult` | per-scenario verdict from `TEST_SCN` |
| `Test::baseScenarioId` | baseline aggregation scenario identifier |
| `Test::baseScenarioResult` | baseline PASS/FAIL result from `TEST_BAS` |
| `Test::baseFlowCoverageMask` | baseline coverage summary |
| `Test::baseTraceSnapshotId` | baseline trace anchor |
| `Test::baseTestHealth` | baseline harness health summary |

## Standard execution procedure

1. Open the active CANoe configuration in the CANoe GUI.
2. Confirm the required runtime nodes, databases, panel assets, and SysVar surfaces are available.
3. Register the matching `*.vtestunit.yaml` asset in the CANoe Test Unit environment.
4. Start measurement.
5. Execute the selected native Test Unit.
6. Confirm the per-scenario verdict and the baseline summary verdict.
7. Save the required report, screenshot, and supporting evidence defined by the evidence policy.

## Current mapping

| Asset | Main scope | Main runtime checks |
| --- | --- | --- |
| `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` | school-zone warning-selection path | `selectedAlert*`, `warningPathStatus`, `failSafeMode`, `warningTextCode` |
| `TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING` | boundary fail-safe path | `failSafeMode`, `decelAssistReq`, `selectedAlert*`, `warningTextCode`, `Test::baseScenarioId`, `Test::baseScenarioResult` |

## Expected outputs

Each official native execution should produce, as applicable:

- compile-clean result
- native test verdict
- native report path
- screenshot or GUI capture
- write-window or trace support when required by the evidence policy

## Boundaries

This document does not define:

- the final customer-facing test architecture
- packaging ownership outside the CANoe native execution surface
- broad redesign of the full `05/06/07` test set

Those areas may be redesigned later from the customer workproduct baseline.

## Development note

The current guide is a valid execution baseline for the active CANoe surface, but the complete project test architecture may later be restructured from the customer document chain.

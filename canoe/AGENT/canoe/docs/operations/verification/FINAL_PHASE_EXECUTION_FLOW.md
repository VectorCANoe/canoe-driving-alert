# Final Phase Execution Flow

## Purpose

- Define the closeout flow for the current SIL cycle without reopening scope.
- Keep the final phase centered on evidence, packaging, and submission structure.

## Fixed Boundary

### Dev1
- owns CANoe runtime behavior under `canoe/`
- owns CAPL, DBC, sysvars, panels, and native CANoe Test Unit assets
- fixes only reproducible runtime defects in the current baseline

### Dev2
- owns the `SDV Operator` product boundary
- primary references:
  - `product/sdv_operator/README.md`
  - `product/sdv_operator/docs/PACKAGING_SCOPE.md`
- continues CLI/TUI, evidence packaging, and CI/Jenkins bridge work

### Docs
- owns the SoT chain under `driving-situation-alert/`
- owns the final submission workspace under:
  - `driving-situation-alert/tmp/submission/final-docs/`

## Final-Phase Rule

Do not reopen:

- requirement expansion
- topology redesign
- broad runtime refactoring

Only do:

- native execution proof
- evidence packaging
- document synchronization
- submission structure cleanup

## Execution Order

1. Dev1 keeps the CANoe runtime baseline stable.
2. Dev1 executes or supports execution of native CANoe Test Unit PoC assets.
3. Dev1 captures native evidence:
   - test verdict
   - native report path
   - screenshot
   - relevant write-window trace if needed
4. Dev2 consumes the native outcome and turns it into operator-facing assets:
   - `JSON`
   - `MD`
   - optional `CSV`
   - portable package / CI handoff
5. Docs updates:
   - `04_SW_Implementation.md`
   - `05_Unit_Test.md`
   - `06_Integration_Test.md`
   - `07_System_Test.md`
   - `TMP_HANDOFF.md` if the active next-step picture changes
6. Docs refreshes the final submission set under `tmp/submission/final-docs/`.

## Native CANoe Test Scope

Current Dev1 native CANoe Test Unit PoC assets:

- `canoe/tests/modules/test_units/TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED/`
- `canoe/tests/modules/test_units/TC_CANOE_IT_V2_FAILSAFE_001_CGW/`

Primary execution guidance:

- `canoe/docs/operations/verification/CANOE_TEST_UNIT_RUNBOOK.md`
- `canoe/docs/operations/verification/CANOE_TEST_POC_SCOPE_2026-03-08.md`

## Evidence Mapping

### Native evidence owned by Dev1
- CANoe Test Unit result
- native `.vtestreport`
- GUI capture

### Externalized evidence owned by Dev2
- packaged report set
- operator run output
- CI-friendly artifact bundle

### SoT evidence owned by Docs
- `05/06/07` verdict rows
- final-docs submission copy

## Out of Scope For Packaging

The packaged `SDV Operator` does not own the CANoe runtime project itself.

Do not package as Dev2 product surface:

- `canoe/cfg/`
- `canoe/databases/`
- `canoe/src/capl/`
- `canoe/project/sysvars/`
- `canoe/project/panel/`

Those remain Dev1 runtime assets.

## Decision Summary

- Dev1 closes runtime correctness and native execution proof.
- Dev2 closes external operator packaging and automation surface.
- Docs closes traceability wording and final submission readability.

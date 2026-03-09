# Verification Docs Index

This folder contains active verification-side runbooks and closeout references for the CANoe SIL baseline.

## Start Here

Open these first:

1. `FINAL_PHASE_EXECUTION_FLOW.md`
2. `CANOE_TEST_UNIT_RUNBOOK.md`
3. `DIAGNOSTIC_TESTER_COVERAGE_2026-03-10.md`
4. `DIAGNOSTIC_COVERAGE_TIERS_2026-03-10.md`
5. `DIAGNOSTIC_SYSVAR_CONTRACT_2026-03-10.md`
6. `CANOE_TEST_CI_BRIDGE_STRATEGY_2026-03-09.md`
7. `TEST_AUTOMATION_REFERENCE_BASELINE_2026-03-09.md`
8. `SIL_PASS_CRITERIA.md`

## Active Docs

- `FINAL_PHASE_EXECUTION_FLOW.md`
  - final-phase split between Dev1, Dev2, and Docs
- `CANOE_TEST_UNIT_RUNBOOK.md`
  - GUI-side registration and execution steps for native CANoe Test Units
- `DIAGNOSTIC_TESTER_COVERAGE_2026-03-10.md`
  - current `TEST_SCN` diagnostic request/response coverage
- `DIAGNOSTIC_COVERAGE_TIERS_2026-03-10.md`
  - `FULL` / `BASIC` / `DEFERRED` diagnostic responder tiers for Dev2 automation
- `DIAGNOSTIC_SYSVAR_CONTRACT_2026-03-10.md`
  - stable `Diag::*` tester-facing sysvar surface for Dev2 pipelines
- `OEM_VECTOR_DIAGNOSTIC_STACK_GAP_ANALYSIS_2026-03-10.md`
  - current stack vs OEM/Vector formal diagnostic stack and description roadmap
- `CANOE_TEST_POC_SCOPE_2026-03-08.md`
  - selected native CANoe test PoC scope and mapping
- `CANOE_TEST_CI_BRIDGE_STRATEGY_2026-03-09.md`
  - Dev1 native CANoe test and Dev2 Jenkins/CLI bridge split
- `TEST_AUTOMATION_REFERENCE_BASELINE_2026-03-09.md`
  - official reference baseline and Dev2 scope boundary for native test + CI bridge
- `SIL_PASS_CRITERIA.md`
  - pass/fail baseline for SIL execution
- `VERIFICATION_INSIGHT_PLAYBOOK.md`
  - evidence interpretation and review guidance

## Working Rule

- Keep this folder focused on active verification execution and closeout.
- Put dated review snapshots in `../audit/`, not here.
- Put final evidence artifacts in report/output paths, not in this folder.

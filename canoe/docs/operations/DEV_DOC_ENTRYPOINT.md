# Developer Document Entrypoint

This file is the active whitelist for CANoe-side working documents.
Use it to avoid browsing too many files.

## Purpose

- keep the daily document surface small
- separate active docs from topic-specific references
- reduce browsing noise during development and verification

## 1) Canonical SoT Chain

Open these first, in order:

1. `driving-situation-alert/TMP_HANDOFF.md`
2. `driving-situation-alert/01_Requirements.md`
3. `driving-situation-alert/03_Function_definition.md`
4. `driving-situation-alert/0301_SysFuncAnalysis.md`
5. `driving-situation-alert/0302_NWflowDef.md`
6. `driving-situation-alert/0303_Communication_Specification.md`
7. `driving-situation-alert/0304_System_Variables.md`
8. `driving-situation-alert/04_SW_Implementation.md`
9. `driving-situation-alert/05_Unit_Test.md`
10. `driving-situation-alert/06_Integration_Test.md`
11. `driving-situation-alert/07_System_Test.md`

## 2) Active CANoe Operations Docs

Read these only after the SoT chain above:

- `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`
- `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`
- `canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md`
- `canoe/docs/operations/CLI_PRODUCTIZATION_BP.md`
- `canoe/docs/operations/README.md`

## 3) Task-Specific Buckets

Open subfolders only when the task needs them:

### Verification
- `canoe/docs/operations/verification/`
- `canoe/docs/operations/verification/README.md`
- `canoe/docs/operations/verification/FINAL_PHASE_EXECUTION_FLOW.md`

### Audit
- `canoe/docs/operations/audit/`

### Panel
- `canoe/docs/operations/panel/`

### Unity / external renderer
- `canoe/docs/operations/unity/`

### Reference / strategy
- `canoe/docs/operations/reference/`

## 4) Default Ignore Set

Do not browse these first:

- `driving-situation-alert/tmp/reference-*`
- `driving-situation-alert/tmp/archive/`
- `driving-situation-alert/tmp/onboarding/`
- `reference/`
- `legacy_projects/`
- `canoe/tmp/reports/verification/` as source code

## 5) Working Rule

If a new note is not part of daily active flow, do not leave it at a top-level folder root.
Place it in the correct bucket immediately.

## 6) Traceability Reminder

Always preserve:

- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`

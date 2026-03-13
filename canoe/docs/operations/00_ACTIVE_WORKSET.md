# CANoe Active Workset

This file is the active whitelist for CANoe-side working documents.

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

## 2) Active CANoe Docs

Read these after the SoT chain:

- `canoe/docs/operations/10_ETHERNET_BACKBONE_INTERFACE_SPEC.md`
- `canoe/docs/operations/11_RUNTIME_MESSAGE_OWNERSHIP_MATRIX.md`
- `canoe/docs/operations/12_MULTIBUS_VISIBILITY_POLICY.md`
- `canoe/docs/operations/verification/20_CANOE_TEST_EXECUTION_GUIDE.md`
- `canoe/docs/operations/verification/21_SIL_ACCEPTANCE_CRITERIA.md`

## 3) Keep Out Of Daily Flow

Do not browse these first:

- `archive/*` branches
- `reference/`
- `driving-situation-alert/tmp/archive/`
- local-only `canoe/{legacy,logging,reference,scripts,tmp}/`

## 4) Working Rule

If a note is not part of daily active flow, do not recreate a new bucket for it.
Use archive branches instead.

## 5) Traceability Reminder

Always preserve:

- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`

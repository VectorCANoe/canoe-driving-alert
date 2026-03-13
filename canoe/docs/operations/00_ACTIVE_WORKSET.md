# CANoe Active Workset

This file is the active whitelist for CANoe-side working documents.

## 1) Canonical SSoT Chain

Open these first, in order:

1. `driving-alert-workproducts/ops/handoff/TMP_HANDOFF.md`
2. `driving-alert-workproducts/01_Requirements.md`
3. `driving-alert-workproducts/03_Function_definition.md`
4. `driving-alert-workproducts/0301_SysFuncAnalysis.md`
5. `driving-alert-workproducts/0302_NWflowDef.md`
6. `driving-alert-workproducts/0303_Communication_Specification.md`
7. `driving-alert-workproducts/0304_System_Variables.md`
8. `driving-alert-workproducts/04_SW_Implementation.md`
9. `driving-alert-workproducts/05_Unit_Test.md`
10. `driving-alert-workproducts/06_Integration_Test.md`
11. `driving-alert-workproducts/07_System_Test.md`

## 2) Active CANoe Docs

Read these after the SSoT chain:

- `canoe/docs/contracts/10_ETHERNET_BACKBONE_SSoT.md`
- `canoe/docs/contracts/11_RUNTIME_MESSAGE_OWNERSHIP_MATRIX.md`
- `canoe/docs/contracts/12_RUNTIME_MULTIBUS_VISIBILITY_POLICY.md`
- `canoe/docs/verification/20_CANOE_TEST_EXECUTION_GUIDE.md`
- `canoe/docs/verification/21_SIL_ACCEPTANCE_CRITERIA.md`

## 3) Keep Out Of Daily Flow

Do not browse these first:

- `archive/*` branches
- `reference/`
- `driving-alert-workproducts/archive/`
- local-only `canoe/{AGENT,logging,reference,scripts,tmp}/`

## 4) Working Rule

If a note is not part of daily active flow, do not recreate a new bucket for it.
Use archive branches instead.

## 5) Traceability Reminder

Always preserve:

- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`

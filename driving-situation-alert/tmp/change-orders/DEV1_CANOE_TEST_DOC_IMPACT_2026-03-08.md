# Dev1 -> Docs Handoff: CANoe Test PoC Impact (2026-03-08)

## Purpose

- Reflect the upcoming native CANoe Test PoC assets without reopening requirement expansion.
- Keep verification asset updates limited to impacted documents only.

## Selected Assets

1. `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
2. `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY`

## Docs Update Scope

### 1. `04_SW_Implementation.md`

- Add one implementation note that native CANoe test assets now coexist with Dev2 externalized verification tooling.
- Clarify role split:
  - native CANoe test = tool-understanding / native execution proof
  - Dev2 CLI/TUI = orchestration, evidence packaging, CI bridge

### 2. `05_Unit_Test.md`

- Add the official CANoe test PoC reference for:
  - `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
- Bind it to existing UT trace rows rather than creating a new requirement branch.

### 3. `06_Integration_Test.md`

- Add the official CANoe test PoC reference for:
  - `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY`
- Bind it to existing fail-safe integration trace rows.

### 4. `07_System_Test.md`

- No new system scenario is required by default.
- Only add evidence/reference linkage if one of the PoC runs is reused for demo or qualification evidence.

### 5. `TMP_HANDOFF.md`

- Add next-step note that native CANoe test PoC authoring is now part of the open verification track for `M41-10`.

### 6. `TEAM_SYNC_BOARD.md`

- Update `TSB-004` with:
  - Dev1 native test authoring
  - Dev2 packaging/orchestration dependency
  - Docs impact path

## Non-Scope

Do **not** expand or rewrite the full chain by default.

No default update required for:

- `01_Requirements.md`
- `03_Function_definition.md`
- `0301_SysFuncAnalysis.md`
- `0302_NWflowDef.md`
- `0303_Communication_Specification.md`
- `0304_System_Variables.md`

unless new validation-only interfaces are introduced by the test PoC itself.

## Validation Harness Rule

- `VAL_SCENARIO_CTRL` / `VAL_BASELINE_CTRL` remain allowed in docs only as validation-only nodes.
- Do not rewrite them as product/customer ECUs.
- Keep product function ownership on product nodes; keep test asset ownership on validation/test sections.

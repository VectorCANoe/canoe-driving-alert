# CANoe Official Test PoC Scope (2026-03-08)

**Document ID**: CANOE-OPS-TEST-POC-SCOPE  
**Version**: 1.0  
**Date**: 2026-03-08  
**Status**: Working  
**Owner**: Dev1

---

## 1. Purpose

- Define the minimum official CANoe Test PoC scope for this cycle.
- Keep the current verification architecture intact:
  - CANoe native test asset for tool understanding
  - Dev2 CLI/TUI for orchestration, evidence packaging, and CI bridge
- Avoid broad verification redesign during expansion-freeze mode.

---

## 2. Decision

Dev1 will author **two** official CANoe test assets only.

1. `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
2. `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY`

Reason:

- one nominal warning-path PoC
- one fail-safe / domain-boundary PoC
- enough to prove native CANoe test authoring capability without competing with Dev2 automation scope

---

## 3. Selected PoC Cases

| Asset ID | Level | Primary Intent | Main Trace Target | Expected Evidence |
|---|---|---|---|---|
| `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED` | Unit-oriented PoC | Prove native CANoe testcase authoring on the core school-zone overspeed warning path | `Req_001, Req_002, Req_003, Req_004, Req_006, Req_010` / `Func_001, Func_002, Func_003, Func_004, Func_006, Func_010` / `Flow_001, Flow_003` / `Comm_001, Comm_003` / `Var_012, Var_013, Var_016, Var_031` / `UT_ADAS_001`, `IT_CORE_001`, `ST_SPEED_001` | CANoe native test report, execution screenshot, measurement log, run-id binding |
| `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY` | Integration-oriented PoC | Prove native CANoe testcase authoring on the V2 fail-safe and domain-boundary path | `Req_127, Req_128, Req_129` / `Func_127, Func_128, Func_129` / `Flow_124` / `Comm_124` / `Var_326, Var_327, Var_328, Var_329` / `IT_V2_FAILSAFE_001`, `ST_V2_FAILSAFE_001` | CANoe native test report, execution screenshot, measurement log, run-id binding |

---

## 4. Team Split

| Team | Scope | Output |
|---|---|---|
| Dev1 | Author the two native CANoe test assets and validate traceability | test source, execution notes, evidence anchor |
| Dev2 | Keep TUI/CLI as external orchestration/evidence/CI bridge layer | run commands, packaging flow, CI bridge notes |
| Docs | Reflect the new verification assets in impacted chain docs only | `04`, `05`, `06`, `07`, `TMP_HANDOFF`, `TEAM_SYNC_BOARD` updates |

---

## 5. Validation Harness Documentation Boundary

### 5.1 Rule

- Product ECUs and validation harness nodes must not be mixed without labeling.
- `VAL_SCENARIO_CTRL` and `VAL_BASELINE_CTRL` are allowed in documentation only when explicitly marked as:
  - `Validation Harness`
  - `Validation-only`
  - `Non-Production`

### 5.2 Allowed Placement

- `00b_Project_Scope.md`
- `0301_SysFuncAnalysis.md`
- `0302_NWflowDef.md`
- `0303_Communication_Specification.md`
- `04_SW_Implementation.md`
- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`
- handoff / mentoring / sync-board notes

### 5.3 Not Allowed

- Treating `VAL_*` nodes as customer-facing product ECUs
- Using `VAL_*` nodes as justification for product feature ownership in `01`
- Presenting validation harness behavior as if it were in-vehicle runtime behavior

### 5.4 Current Project Judgment

- The current project is **not wrong** to include `VAL_SCENARIO_CTRL` / `VAL_BASELINE_CTRL`.
- The reason is that CANoe SIL itself is the verification environment, and the harness nodes own validation-only frames such as `0x2A5` and `0x2A6`.
- The important boundary is labeling, not removal.

---

## 6. Docs Impact Rule

This PoC does **not** require broad `00~07` rewrite.

Primary impact only:

1. `04_SW_Implementation.md`
2. `05_Unit_Test.md`
3. `06_Integration_Test.md`
4. `07_System_Test.md`
5. `TMP_HANDOFF.md`
6. `TEAM_SYNC_BOARD.md`

No default update required for:

- `01_Requirements.md`
- `03_Function_definition.md`
- `0301_SysFuncAnalysis.md`
- `0302_NWflowDef.md`
- `0303_Communication_Specification.md`
- `0304_System_Variables.md`

unless the PoC introduces a new validation-only interface, message, or variable.

---

## 7. Exit Criteria

1. Both native CANoe PoC assets are authored.
2. At least one native CANoe execution result is captured.
3. Dev2 can reference or package the result through the external verification flow.
4. Docs reflect the new asset boundary without promoting harness nodes to product ECUs.

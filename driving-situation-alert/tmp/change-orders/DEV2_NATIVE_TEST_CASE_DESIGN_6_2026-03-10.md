# Dev2 Native CANoe Test Case Design (6 Assets)

- Date: 2026-03-10
- Owner: Dev2
- Status: `Design Baseline for Dev1 Implementation`
- Scope:
  - native CANoe test asset design only
  - canonical `00~07` rewrite is deferred to Docs team after ECU/Req/Scenario refresh
- Rule:
  - common harness stays shared
  - native assets expand from `2 -> 6`
  - broad regression remains Dev2 `verify batch` scope

## 1. Decision Summary

- Native CANoe assets for this cycle: `6`
- Shared harness baseline:
  - `TST_SCN`
  - `TST_BAS`
  - `ValidationHarnessTestCommon.cin`
- Expression rule:
  - do not call these "6 harnesses"
  - call them "1 common harness set + 6 native test assets"

## 1.1 Existing Two-Asset Review

### Judgment

- The existing two native CANoe assets are valid as baseline anchors.
- They already follow the correct OEM-facing direction for this project:
  - shared harness reuse
  - explicit oracle assertions
  - scenario/ack/reset discipline
  - native `.vtestreport` evidence production
- Therefore, they should **not** be discarded or rewritten first.

### What Is Good

1. `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
   - strong nominal anchor
   - explicit end-state oracle on Core/Cluster/Body
2. `TC_CANOE_IT_V2_FAILSAFE_001_CGW`
   - strong fail-safe anchor
   - message + sysvar mixed oracle is appropriate for integration level
3. Common harness contract is already visible and reusable:
   - `resetValidationHarnessIfNeeded()`
   - `waitForScenarioAck()`
   - `launchScenarioAndWait()`
   - shared assert helpers

### What Should Be Normalized Before Expansion Freeze Closes

- Remove `PoC` wording from reviewer-facing descriptions in:
  - `*.vtestunit.yaml`
  - `*.vtesttree.yaml`
  - test runbook text
- Align scenario launch style so both assets use the common helper path consistently where practical.
- Keep current oracle values unless Dev1 changes runtime behavior after ECU reset.

### Recommendation

- Keep the two existing assets as `anchor assets`.
- Expand from `2 -> 6` on the functional side without redesigning the first two.
- Treat metadata/wording normalization as a small follow-up task, not a blocker for the remaining asset skeletons.

## 2. Why These 6

The portfolio is selected by representative verification intent, not by ECU count.

1. one nominal school-zone warning path
2. one emergency ETA priority path
3. one timeout/stale robustness path
4. one fail-safe downgrade path
5. one cross-channel sync path
6. one ADAS object-risk extension path

This gives reviewer-facing native evidence without turning native CANoe tests into full regression replacement.

## 3. Shared Harness Contract

### 3.1 Common Inputs

- `@Test::scenarioCommand`
- `@Test::scenarioCommandAck`
- `@Test::scenarioResult`
- `frmBaseTestResultMsg.BaseScenarioResult`

### 3.2 Common Helper Functions

- `resetValidationHarnessIfNeeded()`
- `waitForScenarioAck()`
- `launchScenarioAndWait()`
- `assertIntEq()`
- `assertIntMin()`

### 3.3 Common Evidence Rule

Each native asset should produce:

1. native CANoe test verdict
2. `.vtestreport`
3. scenario id binding
4. key sysvar/message oracle evidence
5. optional screenshot when panel-visible behavior is part of expected output

## 4. Asset Portfolio

| Asset ID | Level | Scenario | Surface Focus | Primary Intent |
|---|---|---:|---|---|
| `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED` | UT | `2` | `ADAS`, `CLU`, `BCM` | nominal school-zone overspeed warning |
| `TC_CANOE_UT_V2X_001_EMERGENCY_PRIORITY_ETA` | UT | `9` | `V2X`, `ADAS`, `CLU` | ETA-based emergency priority decision |
| `TC_CANOE_UT_V2X_002_TIMEOUT_CLEAR` | UT | `6` | `V2X`, `ADAS`, `BCM`, `CLU` | timeout clear / stale robustness |
| `TC_CANOE_IT_V2_FAILSAFE_001_CGW` | IT | `18` | `CGW`, `ADAS`, `BCM`, `CLU` | fail-safe downgrade with minimum warning retention |
| `TC_CANOE_IT_V2_SYNC_001_DECEL_AND_WARNING` | IT | `19` | `ADAS`, `BCM`, `CLU`, `V2X` | decel assist and warning sync |
| `TC_CANOE_IT_ADAS_001_OBJECT_FORWARD_CONFLICT` | IT | `20` | `ADAS`, `CLU`, `BCM` | forward object TTC conflict path |

## 5. Detailed Design

### 5.1 `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`

- Level: `UT`
- Scenario ID: `2`
- Linked Req/VC:
  - `Req_009`, `Req_010`, `Req_037`
  - `VC_010`
- Related System Cases:
  - `ST_SPEED_001`
- Primary intent:
  - prove nominal school-zone overspeed warning path from context to output
- Preconditions:
  - validation harness reset complete
  - no emergency alert active
- Stimulus:
  1. launch scenario `2`
  2. wait for `scenarioCommandAck == 2`
  3. wait for scenario result settle
- Oracle:
  - `@Test::scenarioResult == 1`
  - `@Core::driveStateNorm == 3`
  - `@Core::vehicleSpeedNorm == 45`
  - `@Core::speedLimitNorm == 30`
  - `@Core::baseZoneContext == 1`
  - `@Core::warningState == 1`
  - `@Core::selectedAlertLevel == 3`
  - `@Core::selectedAlertType == 3`
  - `@Cluster::warningTextCode == 33`
  - `@Body::ambientColor == 3`
  - `@Body::ambientPattern == 5`
- Timing target:
  - warning reflection within `150ms`
- Evidence:
  - `.vtestreport`
  - final sysvar snapshot
  - scenario binding note: `S02`

### 5.2 `TC_CANOE_UT_V2X_001_EMERGENCY_PRIORITY_ETA`

- Level: `UT`
- Scenario ID: `9`
- Linked Req/VC:
  - `Req_030`
  - `VC_030`
- Related System Cases:
  - `ST_ARB_ETA_001`
- Primary intent:
  - prove ETA-based takeover when same-class emergency alerts compete
  - this is a functional priority decision, not a CAN bus arbitration case
- Preconditions:
  - emergency path idle before start
- Stimulus:
  1. launch scenario `9`
  2. phase 1 expects police ETA `20`, source `5`
  3. phase 2 expects takeover by police ETA `10`, source `99`
- Oracle:
  - `@Test::scenarioResult == 1`
  - `@V2X::eta == 10`
  - `@V2X::sourceId == 99`
  - `@Core::selectedAlertLevel == 6`
  - selected emergency class remains police-path consistent
- Timing target:
  - priority update within `150ms` after competitive input change
- Evidence:
  - `.vtestreport`
  - priority decision snapshot / selected source trace
  - scenario binding note: `S09`

### 5.3 `TC_CANOE_UT_V2X_002_TIMEOUT_CLEAR`

- Level: `UT`
- Scenario ID: `6`
- Linked Req/VC:
  - `Req_024`
  - `VC_024`
- Related System Cases:
  - `ST_TIMEOUT_001`
- Primary intent:
  - prove timeout clear after emergency signal becomes stale
- Preconditions:
  - emergency warning path active before timeout window starts
- Stimulus:
  1. launch scenario `6`
  2. stop update / allow timeout path to age out
  3. observe clear and safe release
- Oracle:
  - `@Test::scenarioResult == 1`
  - timeout clear state reached
  - warning level returns to `0`
  - warning code returns to `0`
  - no oscillation after timeout clear
- Timing target:
  - stale window `1000ms`
  - safe clear and return path within `150ms` after timeout decision
- Evidence:
  - `.vtestreport`
  - timeout-related log or variable snapshot
  - scenario binding note: `S06`

### 5.4 `TC_CANOE_IT_V2_FAILSAFE_001_CGW`

- Level: `IT`
- Scenario ID: `18`
- Linked Req/VC:
  - `Req_127`, `Req_128`, `Req_129`
  - `VC_127`, `VC_128`, `VC_129`
- Related System Cases:
  - `IT_V2_FAILSAFE_001`
  - `ST_V2_FAILSAFE_001`
- Primary intent:
  - prove fail-safe downgrade when domain warning path is broken
- Preconditions:
  - domain path healthy before fail-safe trigger
- Stimulus:
  1. launch scenario `18`
  2. force domain boundary / path failure condition
  3. observe downgrade behavior
- Oracle:
  - `@Test::scenarioResult == 1`
  - `frmBaseTestResultMsg.BaseScenarioResult == 1`
  - `@Core::failSafeMode >= 1`
  - `@Core::decelAssistReq == 0`
  - `@Core::selectedAlertLevel >= 6`
  - `@Core::selectedAlertType == 1`
  - `@Cluster::warningTextCode >= 100`
  - minimum warning channel remains available
- Timing target:
  - fail-safe transition within `150ms`
  - automatic decel request generation count remains `0`
- Evidence:
  - `.vtestreport`
  - fail-safe variables / minimum warning channel proof
  - scenario binding note: `S18`

### 5.5 `TC_CANOE_IT_V2_SYNC_001_DECEL_AND_WARNING`

- Level: `IT`
- Scenario ID: `19`
- Linked Req/VC:
  - `Req_125`, `Req_126`
  - `VC_125`, `VC_126`
- Related System Cases:
  - `IT_V2_RISK_001`
  - `ST_V2_RISK_001`
- Primary intent:
  - prove synchronized emergency warning context during decel assist request
- Preconditions:
  - no driver override active
- Stimulus:
  1. launch scenario `19`
  2. allow risk path to activate decel assist and emergency output
  3. inspect synchronized output channels
- Oracle:
  - `@Test::scenarioResult == 1`
  - `@Core::decelAssistReq == 1`
  - `@Core::selectedAlertLevel == 7`
  - `@Core::selectedAlertType == 2`
  - `@Cluster::uiRenderAlertType == 2`
  - `@Cluster::uiRenderTextCode >= 200`
  - `@Body::ambientColor == 7`
  - cluster/ambient sync offset `<= 50ms`
- Timing target:
  - decel and warning activation within `150ms`
  - channel sync offset `<= 50ms`
- Evidence:
  - `.vtestreport`
  - cluster/body synchronization proof
  - scenario binding note: `S19`

### 5.6 `TC_CANOE_IT_ADAS_001_OBJECT_FORWARD_CONFLICT`

- Level: `IT`
- Scenario ID: `20`
- Linked Req/VC:
  - `Req_130`, `Req_131`, `Req_132`
  - `VC_130`, `VC_131`, `VC_132`
- Related System Cases:
  - `IT_ADAS_OBJ_001`
  - `ST_ADAS_OBJ_001`
- Primary intent:
  - prove forward object TTC conflict path without emergency dependency
- Preconditions:
  - no emergency source active
  - object input path available
- Stimulus:
  1. launch scenario `20`
  2. inject/activate forward object risk path
  3. observe TTC-based warning activation
- Oracle:
  - `@Test::scenarioResult == 1`
  - `@ADAS::objectTrackValid == 1` or equivalent active object validity
  - `@ADAS::objectRiskClass >= 3`
  - `@ADAS::objectTtcMin <= 3500`
  - `@Core::proximityRiskLevel >= 60`
  - warning path activates without emergency ownership takeover
- Timing target:
  - object input reflected within `100ms`
  - warning output within `150ms`
- Evidence:
  - `.vtestreport`
  - object-risk variable snapshot
  - scenario binding note: `S20`

## 6. Dev1 Implementation Guidance

For each of the 4 new assets, Dev1 should create:

1. `.../<AssetID>.can`
2. `.../<AssetID>.vtestunit.yaml`
3. `.../<AssetID>.vtesttree.yaml`

Implementation pattern should follow the two existing assets:

- reset harness
- launch scenario
- wait ack
- wait settle
- assert scenario pass
- assert key oracle values
- stop with explicit verdict

## 7. Dev2 Integration Guidance

Dev2 should not author native testcase logic.

Dev2 consumes these assets as:

- `campaign_id`
- `run_id`
- `phase`
- `surface_scope`
- `surface_evidence_bundle`
- `execution_manifest`
- `JUnit XML`
- Jenkins archive set

## 8. Temporary Governance

- This file is a coordination baseline, not canonical `05/06/07`.
- Docs team should later reflect accepted asset IDs and trace links into:
  - `05_Unit_Test.md`
  - `06_Integration_Test.md`
  - `07_System_Test.md`
- Until then, Dev1 may implement against this design baseline.

## 9. Terminology Boundary

- In this design set, use `ETA priority` or `priority decision` for Scenario `9`.
- Do not use `CAN arbitration` to describe this case.
- `CAN bus arbitration` is reserved for separate network/protocol verification such as:
  - bus contention
  - ID priority
  - network load competition
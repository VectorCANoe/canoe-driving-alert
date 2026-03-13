## Native CANoe Harness Portfolio Recommendation (6 Assets)

- Date: 2026-03-09
- Owner: Dev2
- Purpose: define the recommended native CANoe test asset portfolio for Dev1 while keeping Dev2 scope limited to orchestration, evidence packaging, and CI bridge.

### 1. Decision

- Recommended native CANoe harness count for this cycle: `6`
- Rationale:
  - enough to prove CANoe native test authoring capability
  - enough to cover nominal, ETA priority, timeout robustness, fail-safe, and object-risk extension
  - still small enough that native assets do not compete with Dev2 automation scope

### 2. Rule

- Native CANoe Test Unit assets should cover:
  1. one core nominal warning path
  2. one emergency ETA priority path
  3. one timeout/robustness path
  4. one fail-safe/downgrade path
  5. one synchronized output integration path
  6. one object-risk extension path

- Native assets must remain:
  - representative
  - reviewer-facing
  - traceable to `Req -> Func -> Flow -> Comm -> Var`

- Broad regression remains Dev2 scope:
  - `gate all`
  - `doctor`
  - `scenario run`
  - `verify quick / verify batch`
  - `JSON / MD / JUnit / archive`

### 3. Recommended Asset Portfolio

| Asset ID | Level | Scenario | Primary Intent | Main Expected Checks |
|---|---|---:|---|---|
| `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED` | UT | `2` | baseline nominal warning path | school zone context, overspeed warning, ambient/cluster output |
| `TC_CANOE_UT_V2X_001_EMERGENCY_PRIORITY_ETA` | UT | `9` | emergency ETA priority decision | lower ETA source wins, selected alert stays on expected emergency |
| `TC_CANOE_UT_V2X_002_TIMEOUT_CLEAR` | UT | `6` | timeout-clear / stale robustness | timeout clear within policy, warning released without illegal residue |
| `TC_CANOE_IT_V2_FAILSAFE_001_CGW` | IT | `18` | forced fail-safe downgrade / domain-boundary response | failSafeMode set, decelAssistReq blocked, minimum warning path preserved |
| `TC_CANOE_IT_V2_SYNC_001_DECEL_AND_WARNING` | IT | `19` | decel assist + emergency warning sync | decel assist request and warning output stay synchronized across ADAS/BCM/CLU/V2X path |
| `TC_CANOE_IT_ADAS_001_OBJECT_FORWARD_CONFLICT` | IT | `20` | object-risk extension representative path | TTC/object risk detection, object-context warning output, no emergency dependency |

### 4. Why These 6

#### 4.1 Keep Existing Two

- `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
  - already implemented
  - strongest nominal baseline PoC
- `TC_CANOE_IT_V2_FAILSAFE_001_CGW`
  - already implemented
  - strongest fail-safe / downgrade PoC

#### 4.2 Add Four New Assets

- `EMERGENCY_PRIORITY_ETA`
  - proves ETA priority rule, not just nominal emergency alert
  - directly matches project priority rule
- `TIMEOUT_CLEAR`
  - proves robustness and stale handling
  - needed because timeout clear is a fixed policy rule
- `DECEL_AND_WARNING`
  - proves cross-ECU integration path, not isolated logic only
- `OBJECT_FORWARD_CONFLICT`
  - gives one representative ADAS extension harness without exploding test count

### 5. What Dev1 Should Implement in Each Native Asset

- Native source shape:
  - `*.can`
  - `*.vtestunit.yaml`
  - `*.vtesttree.yaml`
- Common harness contract:
  - `Test::scenarioCommand`
  - `Test::scenarioCommandAck`
  - `Test::scenarioResult`
  - `frmBaseTestResultMsg (0x2A6)` when needed

- Assertion style:
  - explicit oracle checks, not only "report generated"
  - check:
    - trigger accepted
    - scenario result pass
    - key sysvars/messages for the target path
    - key output state for cluster/body/ADAS/V2X when applicable

### 6. Dev1 / Dev2 Split

#### Dev1

- decides:
  - what is validated
  - expected value / expected state
  - native CANoe testcase source
- owns:
  - CAPL testcase
  - `.vtestunit.yaml`
  - `.vtesttree.yaml`
  - native `.vtestreport`
  - screenshot / measurement note

#### Dev2

- decides:
  - how it is run in batch/CI
  - how evidence is packaged
  - how it is mapped to `run_id / campaign_id / phase / surface ECU`
  - how Jenkins sees the result
- owns:
  - `verify batch`
  - `execution_manifest`
  - `surface_evidence_bundle`
  - `JUnit XML`
  - archive materialization

### 7. Non-Recommended Directions

- Do not create 6 native assets that all test the same nominal path with different names.
- Do not expand native assets into a full regression replacement for Dev2 automation.
- Do not use native CANoe tests as customer-facing product ECU evidence without marking harness-only boundaries.

### 7.1 Terminology Boundary

- In this portfolio, Scenario `9` is an `ETA priority` test.
- Do not call Scenario `9` a `CAN arbitration` test.
- Reserve `CAN bus arbitration` for protocol/network tests such as:
  - network priority
  - ID policy
  - bus load contention
- If needed later, create those as a separate network verification category.

### 8. Recommendation Summary

- Replace the old "2 only" PoC target with a controlled `6 asset` native portfolio.
- Keep it balanced:
  - `3` logic/robustness-oriented representative paths
  - `3` integration/safety-oriented representative paths
- Let Dev1 own testcase logic and expected values.
- Let Dev2 own campaign/evidence/CI lifecycle around those assets.

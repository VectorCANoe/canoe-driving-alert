# Dev1 Interface Audit Playbook

**Document ID**: CANOE-OPS-DEV1-INT-PLAYBOOK  
**Version**: 1.0  
**Date**: 2026-03-08  
**Status**: Active  
**Owner**: Dev1

---

## 1. Purpose

This playbook defines how Dev1 audits the active runtime before further implementation.

- Focus: active runtime profile, not archive or legacy fallback.
- Priority: interface quality before new feature expansion.
- Outcome: one closed list of code issues, doc-sync requests, and non-issues.

Companion checklist:
- `canoe/docs/operations/audit/DEV1_INTERFACE_AUDIT_CHECKLIST.md`

---

## 2. Audit Inputs

### Source of Truth
- `driving-situation-alert/TMP_HANDOFF.md`
- `driving-situation-alert/0302_NWflowDef.md`
- `driving-situation-alert/0303_Communication_Specification.md`
- `driving-situation-alert/0304_System_Variables.md`
- `canoe/databases/*.dbc`
- `canoe/src/capl/*`
- `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`

### Runtime Scope
- CANoe SIL only
- CAN + Ethernet contract/stub only
- active folders only:
  - `canoe/src/capl/`
  - `canoe/cfg/channel_assign/`

Ignore for this audit:
- `v1_legacy`
- GUI art/layout changes
- Dev2 CLI productization details

### Ethernet Transition Rule

This audit must separate three things:

1. Stable domain CAN runtime
- `chassis_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `powertrain_can.dbc`
- `adas_can.dbc`

These are not the primary migration target.

2. Replaceable Ethernet transport stub
- `eth_backbone_can_stub.dbc`

This is a SIL transport substitute and should be treated as replaceable at real Ethernet cutover.

3. Transport-independent runtime logic
- arbitration
- emergency state handling
- object-risk logic
- boundary/fail-safe logic

The audit should prefer decisions that keep logic reusable when the stub is replaced by real Ethernet.

---

## 3. Deliverables

Dev1 should produce only these outputs:

1. code fix
2. doc update request
3. explicit no-action decision with evidence

Do not create speculative architecture branches during the audit.

---

## 4. Priority 1. Message Contract Audit

### What to Check
- owner uniqueness
- Tx/Rx path correctness
- ID and DLC match
- period/event and timeout match
- validation-only labeling
- ETH logical name to CAN-stub mapping consistency
- whether the active path is stable CAN or replaceable ETH stub

### How to Check
1. Start from ownership matrix.
2. Cross-check DBC sender and CAPL `output(...)`.
3. Cross-check CAPL `on message` receivers.
4. Cross-check `0302` flow path and `0303` communication rows.
5. Mark each finding as one of:
   - match
   - code fix needed
   - docs fix needed
   - both fix needed
   - defer until Ethernet cutover

### Hotspots to Start With
- validation result chain:
  - `frmTestResultMsg (0x2A5)`
  - `frmBaseTestResultMsg (0x2A6)`
- emergency chain:
  - `frmEmergencyBroadcastMsg`
  - `frmEmergencyMonitorMsg`
- object-risk chain:
  - `ethObjectRiskInputMsg`
  - `ethObjectRiskStateMsg`
  - `ethObjectScenarioAlertMsg`
  - `ethObjectSafetyStateMsg`
- diagnostic request/response pairs:
  - `frmBcmDiagReqMsg / frmBcmDiagResMsg`
  - `frmIviDiagReqMsg / frmIviDiagResMsg`
  - `frmPtDiagReqMsg / frmPtDiagResMsg`
  - `frmChassisDiagReqMsg / frmChassisDiagResMsg`

### Exit Rule
- no ambiguous sender
- no duplicate active sender
- no unresolved doc/code mismatch for active messages

---

## 5. Priority 2. SysVar Boundary Audit

### Classification Rule

Every active SysVar must be one of these:

| Class | Meaning | Allowed Example |
|---|---|---|
| Runtime Owner State | canonical state owned by active runtime logic | `Core::selectedAlertLevel` |
| Runtime Mirror | mirrored bus or derived status for visibility | `CoreState::turnLampState` |
| Validation-only Control | injected control used by harness/testing only | `Test::scenarioCommand` |
| UI/Debug Support | operator convenience or query support | `Test::historyQueryOffset` |

### Red Flags
- product logic depends only on SysVar without a message contract
- `Test::*` leaks into product behavior without explicit validation-only intent
- range/unit in `0304` does not match code or `.sysvars`
- multiple writers update the same state without policy

### Interpretation Rule

Do not score SysVar usage by raw count alone.

Classify each active SysVar path by boundary:

1. acceptable SIL mirror/state
- local normalization after `on message`
- derived state for arbitration/output
- health/status mirror for visibility

2. acceptable SIL shortcut for now
- active runtime uses SysVar to bridge a path that is documented as a logical Ethernet contract
- cleanup is deferred until real Ethernet cutover

3. cleanup target before Ethernet cutover
- shortcut bypasses the intended contract boundary and would force mixed transport/logic refactor later

4. invalid hidden dependency
- no documented contract
- no owner clarity
- product behavior depends on validation-only input

### Current Review Targets
- `WARN_ARB_MGR.can` reads many `Core::*` and `CoreState::*`
- `ADAS_WARN_CTRL.can` writes object-risk states into `Core::*`
- `BODY_GW.can`, `IVI_GW.can`, `CLU_HMI_CTRL.can` use `Test::*` overrides/settings
- `VAL_SCENARIO_CTRL.can` is the allowed harness-heavy writer

### Active Shortcut Hotspots
- `CHS_GW -> Core::vehicleSpeedNorm -> ADAS_WARN_CTRL`
- `INFOTAINMENT_GW -> Infotainment::roadZone -> NAV_CTX_MGR`
- `WARN_ARB_MGR -> Core::selectedAlertLevel / selectedAlertType -> BODY_GW`
- `WARN_ARB_MGR -> Core::selectedAlertLevel / selectedAlertType -> IVI_GW`

These are not all equal:
- stable domain CAN ingress can remain message-driven
- logical Ethernet/stub boundaries may stay as SIL shortcut until cutover
- downstream product/output paths should be reviewed carefully if they bypass an already-defined message contract

### Exit Rule
- every active SysVar classified
- every `Test::*` usage explained as validation-only or removed

---

## 6. Priority 3. Single Owner / Single Writer Audit

### Goal
Runtime state and result outputs must be deterministic.

### Check List
- one message owner per active message
- one write owner per state/event counter
- one health owner per domain result
- one baseline result owner

### Current Known Baseline
- `frmTestResultMsg (0x2A5)` owner: `VAL_SCENARIO_CTRL`
- `frmBaseTestResultMsg (0x2A6)` owner: `VAL_BASELINE_CTRL`

### Hotspots
- `Core::objectEventCode`
- `Core::failSafeMode`
- `Core::decelAssistReq`
- `CoreState::alertHistoryCount`
- `CoreState::arbitrationSnapshotId`

### Exit Rule
- no duplicated active writer remains

---

## 7. Priority 4. Timeout / Reset / Fail-safe Audit

### What to Check
- startup initialization
- scenario reset cleanup
- timeout clear
- stale data drop
- fail-safe enter and recovery
- timer wrap safety

### Current Known Watchpoints
- emergency receive age / timeout handling
- object-risk stale path
- duplicate popup guard cleanup
- domain boundary health transition

### Exit Rule
- no known stuck state after reset or timeout

---

## 8. Priority 5. Observability Support Audit

### Goal
Dev2 should be able to explain PASS/FAIL from logs, variables, and traces.

### Minimum Needed
- selected alert level and type
- selected object-risk reason
- arbitration snapshot progression
- fail-safe reason
- boundary status
- validation result ID / scenario ID

### Exit Rule
- runtime failure can be triaged without opening multiple CAPL files first

---

## 9. Kickoff Findings (2026-03-08)

Current first-pass findings:

1. `Comm_106 / frmBaseTestResultMsg` still has one doc-side residual mismatch.
   - `0302` flow chain is already correct.
   - `0303` top message row still says `VAL_BASELINE_CTRL -> VAL_SCENARIO_CTRL`.
   - Active runtime has `VAL_BASELINE_CTRL` sender, but no active `on message frmBaseTestResultMsg` consumer in `canoe/src/capl`.
   - Action: docs-side clarification required.

2. `frmEmergencyBroadcastMsg (0x1C0)` still has a sender ownership ambiguity in DBC.
   - Active runtime uses `EMS_POLICE_TX` and `EMS_AMB_TX`.
   - Active DBC sender field is still `Vector__XXX`.
   - DBC comment explains the dual-source intent, but sender ownership is not explicit enough for the active ownership rule.
   - Action: Dev1 design decision required before docs-side closure.

3. Diagnostic request/response paths are currently aligned in the active profile.
   - `frmChassisDiagReqMsg / frmChassisDiagResMsg`
   - `frmBcmDiagReqMsg / frmBcmDiagResMsg`
   - `frmIviDiagReqMsg / frmIviDiagResMsg`
   - `frmPtDiagReqMsg / frmPtDiagResMsg`
   - Action: keep as reference-good paths for the rest of the audit.

4. Current SysVar-heavy paths must be interpreted by boundary, not by raw count.
   - Stable mirror/state use is acceptable in CANoe SIL.
   - Shortcut paths that bypass the intended message contract should be marked as:
     - acceptable SIL shortcut for now, or
     - cleanup target before Ethernet cutover
   - Action: do not start a broad refactor before classifying each path.

5. The statement "domain CAN stays on `on message`" is only partially true in the active profile.
   - Chassis and infotainment ingress already normalize through `on message`.
   - Downstream alert/output distribution still uses `Core::*` shortcut paths in active CAPL.
   - Action: keep this distinction explicit in reviews and mentoring answers.

6. SysVar audit should focus on `Test::*` usage in product-facing nodes:
   - `BODY_GW`
   - `IVI_GW`
   - `CLU_HMI_CTRL`
   - Matching variables exist in `project.sysvars`, but current `0304` coverage must be checked explicitly.
   - Missing `0304` rows are a docs issue, not an automatic code defect.

7. Timeout/reset audit should start from:
   - emergency timeout path
   - object-risk stale path
   - domain boundary fail-safe path

8. Domain CAN is not the migration target.
   - The future Ethernet cutover should primarily replace the transport/stub side.
   - Do not mix this with unnecessary redesign of stable domain CAN messages.

---

## 10. Execution Sequence

1. Audit message contract path.
2. Freeze owner/writer decisions.
3. Audit SysVar boundary against the frozen contract.
4. Audit timeout/reset/fail-safe after ownership is fixed.
5. Add only the minimum observability needed for Dev2 evidence.

This order is mandatory. Do not start with cosmetic refactoring.

# Dev1 Interface Audit Report (2026-03-08)

**Document ID**: CANOE-OPS-DEV1-INT-REPORT-20260308  
**Version**: 1.0  
**Date**: 2026-03-08  
**Status**: Working  
**Owner**: Dev1

---

## 1. Scope

This report records the first-pass Dev1 audit decisions for the active CANoe SIL runtime.

- Runtime profile: active `canoe/src/capl/*`
- Exclusions:
  - `v1_legacy`
  - GUI topology edits
  - broad architecture redesign
- Rule:
  - separate stable domain CAN from replaceable Ethernet stub
  - classify SysVar shortcuts by boundary, not by raw count

---

## 2. Decision Summary

| ID | Topic | Decision | Status |
|---|---|---|---|
| A-001 | `frmEmergencyBroadcastMsg (0x1C0)` ownership | Treat as logical dual-source emergency contract in SIL stub. Do not force a fake single runtime owner into the stub DBC. | Closed |
| A-002 | `ethSelectedAlertMsg` downstream distribution | Active path still bypasses the logical Ethernet contract and reads `Core::*` directly in output gateways. Keep as SIL shortcut now, but mark as cleanup target before real Ethernet cutover. | Open |
| A-003 | `Comm_106 / frmBaseTestResultMsg` | Runtime is already single-owner correct. Residual mismatch is docs-only. | Docs Request |
| A-004 | `ETH_SW` role | `ETH_SW` is currently a health/freshness monitor, not a forwarding router. Keep this explicit in reviews and cutover planning. | Closed |
| A-005 | `EMS_ALERT_RX` fallback path | `on message frmEmergencyBroadcastMsg` is the active primary path. `V2X::*` polling remains as compatibility fallback and should be retired before or at Ethernet cutover. | Open |
| A-006 | `Test::*` controls in product-facing nodes | Active usage is validation-only and acceptable, but `0304` does not currently document the matching variables. | Docs Request |
| A-007 | `domainBoundaryStatus` writer duplication | Redundant mirror write in `DOMAIN_ROUTER` removed. `DOMAIN_BOUNDARY_MGR` is now the sole active owner. | Closed |
| A-008 | `alertHistoryCount` semantic collision | `EMS_ALERT_RX` counter increment removed. `CLU_HMI_CTRL` remains the active owner for query/display history count. | Closed |
| A-009 | output mirror duplication (`IVI_GW` vs `CLU_HMI_CTRL`) | Multiple `CoreState::*` mirrors are written in both producer and consumer nodes. Not a current functional defect, but should be narrowed later if strict single-writer policy is enforced. | Open |
| A-010 | guarded override / validation exception writers | Some duplicate writers are intentional: fail-safe override and harness object injection. Treat as controlled exceptions, not immediate defects. | Closed |
| A-011 | `VAL_SCENARIO_CTRL` delayed timer residue | Scenario stop/switch paths did not cancel `tScenarioEval`, `tScenarioPhase2`, `tScenarioPhase3`, so delayed callbacks could still fire after reset or mode switch. Fixed in code. | Closed |
| A-012 | timeout/reset/fail-safe control paths | `EMS_ALERT_RX`, `ADAS_WARN_CTRL`, `CLU_HMI_CTRL`, `DOMAIN_BOUNDARY_MGR` are structurally deterministic in the active profile after reviewing watchdog clear, hold-time, duplicate-popup guard, and fail-safe recompute paths. | Closed |
| A-013 | `timeNowInt64()` time-base consistency | Active CAPL files mix raw `timeNowInt64()` comparisons with `/100000` conversions under variables named `*Ms`. This needs Vector-reference confirmation before any wide fix. | Open |

---

## 3. Findings

### A-001. `frmEmergencyBroadcastMsg (0x1C0)` ownership

**Evidence**
- DBC sender field is still `Vector__XXX`:
  - `canoe/databases/eth_backbone_can_stub.dbc`
- Active runtime producers are:
  - `canoe/src/capl/ems/EMS_POLICE_TX.can`
  - `canoe/src/capl/ems/EMS_AMB_TX.can`
- Logical Ethernet contract already defines dual-source Tx:
  - `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`

**Decision**
- This is not a normal single-owner message in the SIL stub.
- The logical contract owner is `EMS_ALERT` with two implementation producers:
  - `EMS_POLICE_TX`
  - `EMS_AMB_TX`
- Forcing one fake sender into the stub DBC would hide the real architecture.

**Action**
- Keep runtime code unchanged.
- Keep the DBC comment and logical contract as the architecture source.
- Reflect the exception in operations docs and ownership notes.

---

### A-002. `ethSelectedAlertMsg` downstream distribution

**Evidence**
- Active producer:
  - `canoe/src/capl/logic/WARN_ARB_MGR.can`
  - `output(mSelected);`
- Contract receiver path in docs:
  - `BODY_GW, IVI_GW`
  - `driving-situation-alert/0302_NWflowDef.md`
  - `driving-situation-alert/0303_Communication_Specification.md`
- Active downstream consumers still read:
  - `@Core::selectedAlertLevel`
  - `@Core::selectedAlertType`
  - `canoe/src/capl/output/BODY_GW.can`
  - `canoe/src/capl/output/IVI_GW.can`

**Decision**
- This is not a current SIL defect.
- This is a documented logical Ethernet contract that is still implemented as a SysVar shortcut in the downstream gateways.
- Classification:
  - `cleanup target before Ethernet cutover`

**Reason**
- If this remains untouched until real Ethernet cutover, transport swap and handler rewrite happen at the same time.
- That increases cutover risk without improving the current SIL baseline.

**Action**
- Do not refactor now as part of the current closure cycle.
- Keep this item open in the Dev1 audit backlog as an Ethernet transition cleanup.

---

### A-003. `Comm_106 / frmBaseTestResultMsg`

**Evidence**
- Runtime sender owner:
  - `VAL_BASELINE_CTRL`
- Runtime duplicate sender in `VAL_SCENARIO_CTRL` was already removed.
- `0302` chain is aligned.
- `0303` still contains a residual top-row mismatch.

**Decision**
- Runtime is correct.
- Remaining issue is docs-only.

**Action**
- Request docs update only.

---

### A-004. `ETH_SW` role

**Evidence**
- `ETH_SW` tracks age/freshness:
  - `frmVehicleStateCanMsg`
  - `frmNavContextCanMsg`
  - `frmSteeringCanMsg`
  - `frmEmergencyMonitorMsg`
- No forwarding output exists in the active file:
  - `canoe/src/capl/network/ETH_SW.can`

**Decision**
- `ETH_SW` is a SIL health monitor for the logical Ethernet path, not a true forwarding switch in the current runtime.

**Action**
- Keep this explicit in:
  - mentoring answers
  - audit notes
  - Ethernet cutover planning

---

### A-005. `EMS_ALERT_RX` fallback path

**Evidence**
- Primary path:
  - `on message frmEmergencyBroadcastMsg`
- Compatibility fallback:
  - `on timer tRxCycle`
  - polls `@V2X::*`
  - `canoe/src/capl/logic/EMS_ALERT_RX.can`

**Decision**
- Primary active path is already message-driven.
- The fallback path is acceptable for SIL compatibility now.
- Classification:
  - `cleanup target before or at Ethernet cutover`

**Action**
- Do not remove during current baseline closure.
- Retire when real Ethernet receive path becomes the only production transport.

---

### A-006. `Test::*` controls in product-facing nodes

**Evidence**
- Product-facing nodes use:
  - `@Test::displayModeSetting`
  - `@Test::alertVolumeSetting`
  - `@Test::seatBeltOverride`
  - `@Test::historyQueryOffset`
  - `@Test::historyQueryCode`
- Active files:
  - `canoe/src/capl/output/BODY_GW.can`
  - `canoe/src/capl/output/IVI_GW.can`
  - `canoe/src/capl/output/CLU_HMI_CTRL.can`
- Matching variables exist in:
  - `canoe/project/sysvars/project.sysvars`
- Current search found no matching rows in:
  - `driving-situation-alert/0304_System_Variables.md`

**Decision**
- These are validation-only controls and query helpers, not hidden product inputs.
- The code usage is acceptable in the current SIL profile.
- The docs gap should be closed so the boundary is explicit.

**Action**
- Request `0304` update for the active `Test::*` variables used by:
  - `BODY_GW`
  - `IVI_GW`
  - `CLU_HMI_CTRL`

---

### A-007. `domainBoundaryStatus` writer duplication

**Evidence**
- Original active writers:
  - `DOMAIN_BOUNDARY_MGR`
  - `DOMAIN_ROUTER`
- `DOMAIN_ROUTER` only read `domainBoundaryStatus`, copied it into a local variable, then wrote the same value back.

**Decision**
- This was redundant and unnecessary.
- `DOMAIN_BOUNDARY_MGR` must remain the sole active owner.

**Action**
- Removed the redundant `@CoreState::domainBoundaryStatus` write from:
  - `canoe/src/capl/ecu/DOMAIN_ROUTER.can`
  - `canoe/cfg/channel_assign/Powertrain/DOMAIN_ROUTER.can`

---

### A-008. `alertHistoryCount` semantic collision

**Evidence**
- `EMS_ALERT_RX` incremented `CoreState::alertHistoryCount` on alert event trace.
- `CLU_HMI_CTRL` incremented the same variable on display/query history push.
- The variable meaning in `project.sysvars` is query/history oriented.

**Decision**
- `alertHistoryCount` should belong to the display/query history owner.
- `EMS_ALERT_RX` already has dedicated trace fields:
  - `lastAlertEventType`
  - `lastAlertEventLevel`
  - `lastAlertEventCode`
  - `lastAlertEventPhase`
- The extra count increment in `EMS_ALERT_RX` created a semantic collision.

**Action**
- Removed the `alertHistoryCount` increment from:
  - `canoe/src/capl/logic/EMS_ALERT_RX.can`
  - `canoe/cfg/channel_assign/ETH_Backbone/EMS_ALERT_RX.can`
- `CLU_HMI_CTRL` remains the active owner of `alertHistoryCount`.

---

### A-009. output mirror duplication (`IVI_GW` vs `CLU_HMI_CTRL`)

**Evidence**
- `IVI_GW` writes output-side `CoreState::*` mirrors at transmit time.
- `CLU_HMI_CTRL` writes the same mirrors again on received cluster/HMI messages.
- Affected mirrors include:
  - `themeMode`
  - `popupType`
  - `popupPriority`
  - `popupActive`
  - `volumeLevel`
  - `audioFocusOwner`
  - `audioDuckingLvl`
  - `ttsState`
  - `clusterNotifType`
  - `clusterNotifPrio`
  - `clusterSyncState`
  - `clusterSyncSeq`

**Decision**
- This is a real single-writer policy violation for mirror variables.
- It is not yet a confirmed runtime defect because both paths write equivalent values in the active profile.
- Keep as an open cleanup item rather than refactoring during the current closure cycle.

**Action**
- No code change in this cycle.
- Revisit when the team wants stricter mirror ownership hygiene.

---

### A-010. guarded override / validation exception writers

**Evidence**
- `Core::decelAssistReq`
  - `WARN_ARB_MGR` writes the normal decision
  - `DOMAIN_BOUNDARY_MGR` forces clear under degraded/fail-safe conditions
- `Core::object*`
  - `ADAS_WARN_CTRL` writes runtime object state
  - `VAL_SCENARIO_CTRL` injects/reset test inputs for SIL harness scenarios

**Decision**
- These are controlled exceptions, not accidental duplicate writers.
- They should remain visible in the audit, but they do not require immediate cleanup.

**Action**
- Keep as explicit exceptions under:
  - fail-safe override
  - validation harness injection/reset

---

### A-011. `VAL_SCENARIO_CTRL` delayed timer residue

**Evidence**
- Scenario apply path schedules delayed callbacks:
  - `tScenarioEval`
  - `tScenarioPhase2`
  - `tScenarioPhase3`
- Stop/reset and diag-switch paths previously canceled only:
  - `tDemoStep`
- Active file:
  - `canoe/src/capl/input/VAL_SCENARIO_CTRL.can`

**Decision**
- This was a real runtime defect.
- A scenario could be stopped or switched while delayed callbacks from the previous scenario were still pending.
- That makes scenario stop/reset non-deterministic and can leak stale writes into the next run.

**Action**
- Added:
  - `cancelScenarioTransientTimers()`
  - `stopScenarioExecution()`
- Updated scenario stop/switch/diag paths to cancel:
  - `tScenarioEval`
  - `tScenarioPhase2`
  - `tScenarioPhase3`
- Also clear:
  - `gCurrentScenarioId`
  - `gArbitrationSnapshotBaseline`
  - `@Test::scenarioResult`
  - `@Test::forceFailSafe`

---

### A-012. timeout/reset/fail-safe control paths

**Evidence**
- `EMS_ALERT_RX`
  - watchdog clear sets `timeoutClear=1`, pulses `tTimeoutClearPulse`, and auto-clears back to `0`
- `ADAS_WARN_CTRL`
  - object hold-time uses `gLastObjectTrackRxMs` and `objectAlertHoldMs`
  - startup resets object-risk state
- `CLU_HMI_CTRL`
  - duplicate-popup guard cancels on clear and recomputes on timer
- `DOMAIN_BOUNDARY_MGR`
  - fail-safe recomputes every `100 ms`
  - degraded/force-fail-safe clears `decelAssistReq`

**Decision**
- After the scenario timer residue fix above, these active control paths are structurally deterministic.
- No additional reset/timeout residue defect was confirmed in this audit pass.

**Action**
- Keep current logic.
- Continue using this section as the baseline when Dev2 runs long-duration evidence capture.

---

### A-013. `timeNowInt64()` time-base consistency

**Evidence**
- Raw comparisons exist in active files:
  - `WARN_ARB_MGR`
  - `ADAS_WARN_CTRL`
  - `EMS_ALERT_RX`
  - `CLU_HMI_CTRL`
- `/100000` conversion exists in active files:
  - `DOMAIN_BOUNDARY_MGR`
  - `VAL_SCENARIO_CTRL`
- Variable naming currently implies millisecond semantics in both styles.

**Decision**
- There is a project-level time-base consistency risk.
- This audit does not yet have a Vector primary-source citation confirming the exact unit expected from `timeNowInt64()`.
- Do not perform a wide time-base rewrite until that reference is confirmed.

**Action**
- Keep this item open.
- Confirm the official unit from Vector documentation or runtime proof before changing:
  - watchdog thresholds
  - duplicate-popup guard windows
  - hold-time logic
  - boundary health age logic

---

## 4. Stable CAN vs Replaceable Stub

### Stable domain CAN
- `chassis_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `powertrain_can.dbc`
- `adas_can.dbc`

These are not the primary migration target.

### Replaceable Ethernet transport boundary
- `eth_backbone_can_stub.dbc`

This is the planned swap boundary at real Ethernet cutover.

---

## 5. P2 Boundary Classification Snapshot

| Namespace / Path | Current Role | Classification | Decision |
|---|---|---|---|
| `Core::*` normalized ingress (`vehicleSpeedNorm`, `driveStateNorm`, `steeringInputNorm`, `brakePedalNorm`) | gateway-normalized runtime state | acceptable SIL mirror/state | Keep |
| `Core::*` arbitration/result state (`selectedAlertLevel`, `selectedAlertType`, `timeoutClear`, `decelAssistReq`, `failSafeMode`) | canonical runtime owner state | acceptable SIL owner state | Keep |
| `Core::*` object-risk state (`objectTrackValid`, `objectRange`, `objectRelSpeed`, `objectConfidence`, `objectRiskClass`, `objectTtcMin`, `intersectionConflictFlag`, `mergeCutInFlag`, `objectAlertHoldMs`, `objectEventCode`) | active ADAS/runtime state | acceptable SIL owner state | Keep |
| `CoreState::*` mirrors and counters | runtime mirror / observability state | acceptable SIL mirror/state | Keep |
| `Test::*` scenario control (`testScenario`, `scenarioCommand`, `scenarioCommandAck`, `scenarioResult`, `forceFailSafe`) | validation harness control | validation-only control | Keep |
| `Test::*` operator controls (`displayModeSetting`, `alertVolumeSetting`, `seatBeltOverride`, `historyQueryOffset`, `historyQueryCode`) | validation-only override / query support | validation-only control / UI-debug support | Keep, doc gap remains |
| `Chassis::*`, `Infotainment::*` input vars | harness/panel ingress for SIL | validation-only ingress namespace | Keep |
| `V2X::*` primary emergency context | active runtime compatibility + EMS producer/receiver state | acceptable SIL shortcut for now | Keep, cutover cleanup still needed in fallback path |
| `Body::*`, `Cluster::*`, `UiRender::*` | output mirror / renderer support | UI-debug support / output mirror | Keep |
| `WARN_ARB_MGR -> Core::* -> BODY_GW/IVI_GW` | downstream alert distribution shortcut | cleanup target before Ethernet cutover | Track |
| `INFOTAINMENT_GW -> Infotainment::* -> NAV_CTX_MGR` | nav context bridge | acceptable SIL shortcut for now | Track, no immediate refactor |
| `CHS_GW -> Core::* -> ADAS_WARN_CTRL` | vehicle-state bridge into logic | acceptable SIL shortcut for now | Track, no immediate refactor |
| `WARN_ARB_MGR -> Core::decelAssistReq` and `DOMAIN_BOUNDARY_MGR -> Core::decelAssistReq` | arbitration + fail-safe override | controlled exception | Keep |
| `ADAS_WARN_CTRL -> Core::object*` and `VAL_SCENARIO_CTRL -> Core::object*` | runtime object state + harness injection/reset | controlled validation exception | Keep |
| `IVI_GW -> CoreState::*` and `CLU_HMI_CTRL -> CoreState::*` | output mirror duplication | open cleanup target | Track |
| `timeNowInt64()` raw vs `/100000` conversion | mixed time-base assumption across active files | open audit risk | Track |

Current conclusion:
- No invalid hidden dependency has been confirmed yet in the active profile.
- The main issue is not SysVar count.
- The main issue is whether a shortcut crosses a boundary that will become real Ethernet later.

---

## 6. Pending Doc Sync Requests (Batch Hold)

These items should be recorded now and handed to the docs team together later.

| Request ID | Target Doc | Request |
|---|---|---|
| DSR-001 | `0303_Communication_Specification.md` | Fix residual `Comm_106 / frmBaseTestResultMsg` wording to match the active chain: `VAL_SCENARIO_CTRL -> frmTestResultMsg(0x2A5) -> VAL_BASELINE_CTRL -> frmBaseTestResultMsg(0x2A6)` |
| DSR-002 | `0304_System_Variables.md` | Add active `Test::*` rows used in runtime: `displayModeSetting`, `alertVolumeSetting`, `seatBeltOverride`, `historyQueryOffset`, `historyQueryCode` |
| DSR-003 | `0302_NWflowDef.md`, `0303_Communication_Specification.md` | When the team is ready, clarify that `ETH_SW` is a SIL health/freshness monitor in the active profile, not a forwarding Ethernet switch |

---

## 7. Dev1 Next Actions

1. Keep `A-002` and `A-005` visible as cutover cleanup items.
2. Send docs-only requests for `A-003` and `A-006`.
3. Resolve `A-013` only after Vector time-base reference is confirmed.
4. Do not start broad message-routing refactor during the current SIL closure cycle.
5. Continue SysVar boundary audit with this classification rule:
   - acceptable SIL mirror/state
   - acceptable SIL shortcut for now
   - cleanup target before Ethernet cutover
   - invalid hidden dependency

---

## 8. Conclusion

The current architecture does not require immediate redesign.

- Stable domain CAN should remain stable.
- The Ethernet stub boundary must stay explicit.
- Current Dev1 work should focus on:
  - ownership clarity
  - boundary classification
  - cutover-ready cleanup tracking

Do not confuse "SysVar exists" with "architecture defect."

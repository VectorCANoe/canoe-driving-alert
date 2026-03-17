# Diagnostic Seam Design

> [!IMPORTANT]
> This document is the current development baseline for diagnostic-linked verification seam design.
> It may change as CANoe diagnostic hooks, sysvar contracts, and tester interpretation are finalized.

## 1. Purpose

This document defines the minimum seam design for the current official diagnostic scope.

The current official scope is intentionally narrow and is limited to:

- `UT_063`
- `UT_064`
- `IT_040`
- `ST_043`

These items require stronger diagnostic or security state visibility than the normal oracle/evidence path alone.

## 2. Design principles

1. Expose verdict-critical state, not every internal state.
2. Keep business semantics separate from transport details.
3. Make seam values readable in CANoe native reports, sysvar snapshots, and write-window evidence.
4. Reuse the same seam meaning from `UT` to `IT` to `ST` where possible.
5. Do not expand diagnostic seams into normal `No` items unless the official verdict scope changes.

## 3. Minimum seam fields

The minimum seam set should support these questions:

- what security or diagnostic state is active
- which route owner or gateway owner is active
- which request or response class was last processed
- whether the verdict is blocked by timeout, denial, or unavailable service state

Recommended minimum fields:

- `diag_state`
- `security_state`
- `service_state`
- `route_owner`
- `last_sid`
- `last_did_or_dtc`
- `response_kind`
- `timeout_flag`
- `source_bus`
- `target_bus`
- `reason_code`

These are semantic field names, not final implementation identifiers.

## 4. Current 0304-aligned seam candidates

The current system-variable baseline already exposes part of the needed seam surface through `0304_System_Variables.md` and `Diag::*`.

Use these existing variables first:

| Semantic need | Current candidate sysvar surface |
|---|---|
| fail-safe state | `Core::failSafeMode` |
| path health | `CoreState::warningPathStatus`, `CoreState::e2eHealthState` |
| route and boundary condition | `Powertrain::RoutingPolicy`, `Powertrain::BoundaryStatus`, `Body::BodyGwHealth` |
| diagnostic request identity | `Diag::LastRequestTarget`, `Diag::LastRequestSid`, `Diag::LastRequestDidHigh`, `Diag::LastRequestDidLow`, `Diag::LastRequestSourceBus`, `Diag::RequestCounter`, `Diag::LastRequestTimeMs` |
| diagnostic response identity | `Diag::LastResponseTarget`, `Diag::LastResponseCode`, `Diag::LastResponseData0`, `Diag::LastResponseData1`, `Diag::LastResponseOk`, `Diag::LastResponseSourceBus`, `Diag::ResponseCounter`, `Diag::LastResponseTimeMs` |
| ECU-local diagnostic state hints | `Chassis::ChassisDiagState`, `Body::BodyDiagState`, `Infotainment::InfoDiagState`, `Powertrain::PtDiagState` |
| ECU-local diagnostic request/response hints | `Chassis::ChsDiagServiceId`, `Chassis::ChsDiagRespCode`, `Body::BcmDiagServiceId`, `Body::BcmDiagRespCode`, `Infotainment::IviDiagServiceId`, `Infotainment::IviDiagRespCode`, `Powertrain::PtDiagServiceId`, `Powertrain::PtDiagRespCode` |

These existing variables are enough to start skeleton wiring and evidence capture.

They are not yet enough to express every official diagnostic verdict cleanly.

## 5. Current reserved seam additions

The following semantic fields are now reserved in `project.sysvars` under `Diag::*` for verification use.

Producer wiring may still be pending.

| Reserved seam | Why it matters |
|---|---|
| `Diag::SecurityState` | `UT_063`, `IT_040`, and `ST_043` need a stable security verdict seam rather than indirect interpretation only |
| `Diag::ServiceState` | integrated service-context verdicts should not rely only on mixed runtime side effects |
| `Diag::RouteOwner` | current route and boundary health surfaces exist, but direct ownership explanation is still weak without a stable semantic seam |
| `Diag::ResponseKind` | `Positive / Negative / Timeout / Unavailable` needs a stable verdict-facing interpretation |
| `Diag::ReasonCode` | final official verdicts should be able to explain why a diagnostic-linked decision was made |

## 6. Remaining meaning-level gaps

The remaining gap is no longer variable reservation.

It is producer-side semantic wiring.

| Remaining gap | Why it matters |
|---|---|
| semantic producer wiring | runtime or harness logic must still set the reserved seams consistently |
| stable enum meaning | each seam must keep one stable interpretation across `UT`, `IT`, and `ST` |
| trace correlation rule | seam updates must stay correlatable with `Diag::*` request/response mirrors and write-window evidence |

## 7. Baseline enum contract

Use one stable numeric interpretation from `UT` to `ST`.

| Seam | Value | Meaning |
|---|---:|---|
| `Diag::SecurityState` | `0` | unavailable or inactive |
| `Diag::SecurityState` | `1` | session open or degraded security context |
| `Diag::SecurityState` | `2` | authorized and route-usable |
| `Diag::SecurityState` | `3` | denied, faulted, or fail-safe-blocked |
| `Diag::ServiceState` | `0` | unavailable |
| `Diag::ServiceState` | `1` | degraded |
| `Diag::ServiceState` | `2` | available |
| `Diag::RouteOwner` | `0` | none or unknown |
| `Diag::RouteOwner` | `1` | `SGW` |
| `Diag::RouteOwner` | `2` | `DCM` |
| `Diag::RouteOwner` | `3` | integrated warning path |
| `Diag::ResponseKind` | `0` | none |
| `Diag::ResponseKind` | `1` | positive |
| `Diag::ResponseKind` | `2` | negative |
| `Diag::ResponseKind` | `3` | timeout |
| `Diag::ResponseKind` | `4` | unavailable or denied |
| `Diag::ReasonCode` | `0` | none |
| `Diag::ReasonCode` | `1` | boundary down |
| `Diag::ReasonCode` | `2` | fail-safe active |
| `Diag::ReasonCode` | `3` | service degraded |
| `Diag::ReasonCode` | `4` | policy denied |
| `Diag::ReasonCode` | `5` | response timeout |
| `Diag::ReasonCode` | `6` | route mismatch |

## 8. Seam design by current official scope

| Source ID | Seam question | Minimum required fields | Primary evidence path |
|---|---|---|---|
| `UT_063` | was the security preset interpreted as the intended security state and ownership context | current: `Powertrain::RoutingPolicy`, `Body::BodyGwHealth`; reserved: `Diag::SecurityState`, `Diag::RouteOwner`, `Diag::ReasonCode` | write window + trace + sysvar snapshot |
| `UT_064` | was the diagnostic preset interpreted as the intended diagnostic state and request class | current: `Diag::LastRequestSid`, `Diag::LastResponseCode`, `Diag::LastResponseOk`; reserved: ECU-local diag state + `Diag::ResponseKind`, `Diag::ReasonCode` | write window + trace + sysvar snapshot |
| `IT_040` | did integrated service, security, and diagnostic context resolve to the expected runtime verdict | current: `Diag::*`, ECU-local `*DiagState`, `Powertrain::RoutingPolicy`; reserved: `Diag::ServiceState`, `Diag::SecurityState`, `Diag::RouteOwner` | native report + trace + write window + sysvar snapshot |
| `ST_043` | did the system-level service/security/diagnostic context justify the final scenario verdict | current: `Diag::*`, ECU-local `*DiagState`, `CoreState::warningPathStatus`; reserved: `Diag::ServiceState`, `Diag::SecurityState`, `Diag::RouteOwner`, `Diag::ReasonCode` | native report + trace + write window + sysvar snapshot |

## 9. Planned assertion profiles

| Source ID | Planned nominal assert set | Planned degraded or blocked assert set | Current blocker |
|---|---|---|---|
| `UT_063` | `SecurityState=2`, `RouteOwner=3 or 1` | degraded: `SecurityState=3`, `RouteOwner=1`; blocked: `SecurityState=3`, `RouteOwner=1` | executable via `TEST_SCN` scenario `203` |
| `UT_064` | `LastRequestSid=0x22`, `ResponseKind=1`, `ReasonCode=0` | degraded: `ResponseKind=2`, `ReasonCode=3`; blocked: `ResponseKind=4`, `ReasonCode=2` | executable via `TEST_SCN` scenario `204` |
| `IT_040` | `ServiceState=2`, `SecurityState=2`, `RouteOwner=3`, `ResponseKind=1`, `ReasonCode=0` | degraded: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=3`; blocked: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=2` | executable via `TEST_SCN` scenario `205` |
| `ST_043` | scenario verdict remains explainable with `ServiceState=2`, `SecurityState=2`, `RouteOwner=3`, `ReasonCode=0` | degraded context: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=3`; blocked context: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=2` | executable via `TEST_SCN` scenario `202` |

## 10. Publisher ownership baseline

To avoid conflicting writes, keep one producer per reserved seam.

| Producer | Owned reserved seam |
|---|---|
| `SGW.can` | `Diag::SecurityState`, `Diag::RouteOwner` |
| `DCM.can` | `Diag::ServiceState`, `Diag::ResponseKind`, `Diag::ReasonCode`, all current executable request/response identity mirrors (`LastRequestTarget`, `LastRequestSid`, `LastRequestDidHigh`, `LastRequestDidLow`, `LastRequestSourceBus`, `RequestCounter`, `LastRequestTimeMs`, `LastResponseTarget`, `LastResponseCode`, `LastResponseData0`, `LastResponseData1`, `LastResponseOk`, `LastResponseSourceBus`, `ResponseCounter`, `LastResponseTimeMs`) |

## 11. ST_043 scenario stimulus contract

The first executable `ST_043` scenario should use three phases only.

1. nominal context
   - boundary healthy
   - fail-safe inactive
   - service available
   - expected seam: `ServiceState=2`, `SecurityState=2`, `RouteOwner=3`, `ReasonCode=0`
2. degraded context
   - emergency refresh intentionally degraded
   - `warningPathStatus=1`, `failSafeMode=1`
   - expected seam: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=3`
3. blocked context
   - explicit fail-safe active
   - expected seam: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=2`

The system-level testcase should pass only if visible behavior and seam explanation remain consistent across all three phases.

## 12. Response interpretation baseline

The first implementation baseline should distinguish only:

- positive completion
- negative completion
- timeout
- unavailable service or denied state

Recommended semantic values for `response_kind`:

- `Positive`
- `Negative`
- `Timeout`
- `Unavailable`

Do not expand into full NRC catalogs until the current official coverage is stable.

## 13. Implementation order

1. `UT_063`
   - wire `Diag::SecurityState`
   - wire `Diag::RouteOwner`
2. `UT_064`
   - wire ECU-local diagnostic state interpretation
   - wire `Diag::ResponseKind`
3. `IT_040`
   - wire `Diag::ServiceState`
   - reuse shared ownership interpretation
4. `ST_043`
   - system-level diagnostic-context verdict seam

## 14. Expansion gate

Expand this seam set only when one of the following becomes true:

1. the official verdict depends on session or security access stage
2. reviewer asks for SID, DID, DTC, or NRC-level explanation
3. gateway route ownership becomes part of formal acceptance
4. ODX/CDD-based tester interpretation becomes required for the current baseline

## 15. Relationship to other verification documents

Use this document together with:

- `diagnostic-coverage.md`
- `test-asset-mapping.md`
- `oracle.md`
- `diagnostic-sysvar-contract.md`

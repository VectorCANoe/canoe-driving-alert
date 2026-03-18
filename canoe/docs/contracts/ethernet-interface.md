# ETH Interface Contract

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## 1. Purpose

This document defines the operational Ethernet contract for the active CANoe SIL profile.

It complements the bit-level Ethernet specification by answering:

- which seams are active
- who logically owns them
- who consumes them
- which fallback paths are allowed
- which shortcuts are validation-only

For bit fields, IDs, and signal packing, use:

- `docs/contracts/ethernet-backbone.md`

For owner, observer, validation, and render separation, use:

- `docs/contracts/layer-separation-policy.md`

## 2. Active transport baseline

The active backbone transport is:

- `UDP multicast 239.0.2.1:5000`

This backbone is the active inter-domain seam for the current CANoe SIL profile.

Retired CAN stub seams must not be treated as the primary architecture contract.

In the current SIL validation baseline, multicast sender identity may vary by CANoe runtime stack behavior.
Therefore ingress owners reject self-originated transport first, prefer the documented validation sender when it is visible, and trace unexpected external sources before accepting them as external ingress.

## 3. Contract classes

### 3.1 Input-context seams

These seams bring raw context into the shared runtime.

| Seam | Logical owner | Primary consumers | Intent |
|---|---|---|---|
| `ethVehicleStateMsg` | `VCU` | `CGW`, `IBOX` | vehicle speed and drive state context |
| `ethSteeringMsg` | `MDPS` | `CGW` | steering activity context |
| `ethNavContextMsg` | `IVI` | `CGW`, `IBOX` | road zone, direction, speed-limit context |
| `ETH_EmergencyAlert` | `V2X` | emergency-context runtime path | emergency ingress context |
| `ethObjectRiskInputMsg` | `TEST_SCN` | `ADAS` | validation-only object-risk stimulus |

### 3.2 Decision-output seams

These seams publish selected runtime meaning after arbitration.

| Seam | Logical owner | Primary consumers | Intent |
|---|---|---|---|
| `ethSelectedAlertMsg` | `ADAS` transport relay of the active selected-alert state | `BCM`, `IVI`, downstream warning consumers | selected alert result after applying the currently active boundary-shaped alert state |
| `ethEmergencyRiskMsg` | `ADAS` | ADAS-side consumers, `TEST_SCN` | emergency proximity risk |
| `ethDecelAssistReqMsg` | `ADAS` | `ESC`, `TEST_SCN` | deceleration assist request |
| `ethObjectRiskStateMsg` | `ADAS` | ADAS-side consumers, `TEST_SCN` | object risk classification |
| `ethObjectScenarioAlertMsg` | `ADAS` | `BCM`, `IVI`, `TEST_SCN` | object-context warning result |

### 3.3 Boundary-health seams

These seams expose health, degradation, and observability state.

| Seam | Logical owner | Primary consumers | Intent |
|---|---|---|---|
| `ethFailSafeStateMsg` | `CGW` | `ADAS`, `TEST_SCN`, selected safety observers | path health and fail-safe mode |
| `ETH_EmergencyMonitor` | `V2X` | `TEST_SCN`, trace observers | emergency transport monitor |
| `ethObjectSafetyStateMsg` | `CGW` | `ADAS`, `TEST_SCN`, selected observers | object-path health and event code |

### 3.4 Diagnostic observation surface

This surface exists for the current lightweight diagnostic baseline.

| Surface | Logical owner | Primary consumers | Intent |
|---|---|---|---|
| `Diag::*` semantic observation seam | `SGW` + `DCM` | `EXT_DIAG`, verification, evidence tools | compact diagnostic request/response and verdict observation without adding a new Ethernet payload contract |

Current interpretation:

- `EXT_DIAG` is the logical external diagnostic requester or observer placeholder
- it does not own a new UDP multicast message in the current baseline
- it reads the existing `Diag::*` semantic seam rather than subscribing to every product node raw message
- later DoIP, UDS, or CANoe Diagnostics Feature Set expansion may replace the requester implementation without changing this architecture role

## 4. Contract rules

### 4.1 Business meaning is separate from transport

The business meaning of a warning must not be tied to a temporary stub or mirror path.

Examples:

- `ETH_EmergencyAlert` is the active emergency ingress seam
- a retired stub frame is not the architecture source of truth
- `Core::*` and normalized `CoreState::*` mirrors may support SIL compatibility and product-consumer separation, but they are not the published Ethernet contract

### 4.2 One logical owner per seam

Each active Ethernet seam must have one clear logical owner in the current runtime.

Compatibility mirrors and verification observers do not change that ownership.

### 4.3 Consumers may use documented fallback, not silent substitution

The current SIL profile allows limited fallback behavior for some downstream consumers.

Example:

- `BCM`, `IVI`, and similar warning consumers may fall back to mirrored `Core::*` state when the fresh backbone result seam is unavailable
- `ADAS` and render nodes consume normalized ingress metadata from `CoreState::*` when they need direction, ETA, or source information derived by the `V2X` owner

Rule:

- treat fallback as a documented compatibility path
- do not present fallback as the primary interface contract

### 4.4 Validation-only seams stay explicit

`TEST_SCN` may produce Ethernet seams such as `ethObjectRiskInputMsg` for SIL validation.

`TEST_SCN` may also emit `ETH_EmergencyAlert` as a validation ingress stimulus when the emergency ingress path itself is under test.

In the current executable baseline, `V2X` accepts emergency ingress from the validation injector path only, and `ADAS` accepts `ethObjectRiskInputMsg` from the validation injector path only.

This does not make `TEST_SCN` a product ECU owner.

### 4.5 Health and timeout state belong to boundary authority

Health and degradation state must come from the boundary authority path, not from ad-hoc local guesses.

Primary examples:

- `Core::timeoutClear`
- `CoreState::warningPathStatus`
- `CoreState::e2eHealthState`
- `CoreState::selectedAlertEffectiveLevel`
- `CoreState::selectedAlertEffectiveType`
- `CoreState::selectedAlertGateReason`
- `CoreState::driverReleaseReason`
- `V2X::ingressHeartbeat`
- `ethFailSafeStateMsg`

### 4.6 `EXT_DIAG` does not add a new backbone payload contract

`EXT_DIAG` belongs to the backbone-side diagnostic surface, but the current executable baseline adds:

- no new Ethernet message ID
- no new CAN DBC row
- no new direct backbone RX owner

Its current role is observation and evidence alignment through `Diag::*`.

## 5. Update rules

When an Ethernet seam changes, update in this order:

1. `docs/contracts/ethernet-backbone.md`
2. `docs/contracts/ethernet-interface.md`
3. `docs/contracts/communication-matrix.md`
4. `docs/contracts/multibus-policy.md`
5. runtime CAPL and verification docs

## 6. Non-goals

This document does not replace:

- bit-level DBC-style signal packing rules
- GUI topology instructions
- dated migration backlog notes

Those belong elsewhere.

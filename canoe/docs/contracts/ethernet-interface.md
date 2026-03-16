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

## 2. Active transport baseline

The active backbone transport is:

- `UDP multicast 239.0.2.1:5000`

This backbone is the active inter-domain seam for the current CANoe SIL profile.

Retired CAN stub seams must not be treated as the primary architecture contract.

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
| `ethSelectedAlertMsg` | `ADAS` | `BCM`, `IVI`, downstream warning consumers | selected alert result |
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

## 4. Contract rules

### 4.1 Business meaning is separate from transport

The business meaning of a warning must not be tied to a temporary stub or mirror path.

Examples:

- `ETH_EmergencyAlert` is the active emergency ingress seam
- a retired stub frame is not the architecture source of truth
- `Core::*` mirrors may support SIL compatibility, but they are not the published Ethernet contract

### 4.2 One logical owner per seam

Each active Ethernet seam must have one clear logical owner in the current runtime.

Compatibility mirrors and verification observers do not change that ownership.

### 4.3 Consumers may use documented fallback, not silent substitution

The current SIL profile allows limited fallback behavior for some downstream consumers.

Example:

- `BCM`, `IVI`, and similar warning consumers may fall back to mirrored `Core::*` state when the fresh backbone result seam is unavailable

Rule:

- treat fallback as a documented compatibility path
- do not present fallback as the primary interface contract

### 4.4 Validation-only seams stay explicit

`TEST_SCN` may produce Ethernet seams such as `ethObjectRiskInputMsg` for SIL validation.

This does not make `TEST_SCN` a product ECU owner.

### 4.5 Health and timeout state belong to boundary authority

Health and degradation state must come from the boundary authority path, not from ad-hoc local guesses.

Primary examples:

- `Core::timeoutClear`
- `CoreState::warningPathStatus`
- `CoreState::e2eHealthState`
- `ethFailSafeStateMsg`

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

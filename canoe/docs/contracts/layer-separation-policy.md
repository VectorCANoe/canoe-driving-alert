# Runtime Layer Separation Policy

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the official layer-separation rule for the active CANoe SIL baseline.

It answers these questions:

- which node owns the business meaning of a seam
- which node may transport or route that seam
- which node may only observe or validate that seam
- which seams are operational, render-facing, diagnostic, or validation-only

Use this document before changing:

- backbone producer or consumer ownership
- test stimulus injection paths
- observer or verdict seams
- diagnostic semantic seams

## External Reference Basis

The separation rule below is aligned to public OEM-side and tool-vendor references:

- Vector, *CAPL Callback Interface in CANoe* (tester side vs ECU simulation side, explicit diagnostic target/channel separation)
  - https://support.vector.com/sys_attachment.do?sys_id=27ee721387020a18a0460fe40cbb35d3
- Vector, *Ethernet_E: DoIP* (diagnostic tester, diagnostic gateway, DoIP node split)
  - https://certification.vector.com/mod/page/view.php?id=167
- AUTOSAR CP, *Diagnostic Communication Manager* (external diagnostic tool vs onboard DCM; network-independent diagnostic state management)
  - https://www.autosar.org/fileadmin/standards/R24-11/CP/AUTOSAR_CP_SWS_DiagnosticCommunicationManager.pdf
- AUTOSAR, *PDU Router* (routing forwards I-PDUs and must not redefine payload meaning)
  - https://www.autosar.org/fileadmin/fileadmin/standards/classic/2-0/AUTOSAR_SWS_PDU_Router.pdf
- ISO 13400-2:2025, *DoIP* (client tester, vehicle gateway, sub-component routing)
  - https://www.iso.org/standard/13400-2

## Layer Model

The active baseline uses six runtime layers.

| Layer | Meaning | Typical owner type |
| --- | --- | --- |
| Transport ingress | accepts raw network context and normalizes freshness | ingress owner |
| Functional decision | decides warning, risk, and assist meaning | decision owner |
| Boundary / override | applies fail-safe, route, and freshness policy | gateway or boundary owner |
| Render / output | presents the result to body, display, cluster, or audio consumers | render owner |
| Observer / validation | observes already-owned seams for evidence and verdict only | validation harness |
| Diagnostic semantic | exposes diagnostic state, session, security, or response meaning | diagnostic owner |

## Separation Rules

### 1. One business owner per seam

- each logical seam must have exactly one business owner
- compatibility mirrors, trace seams, and validation observers do not change that ownership
- a transport injector may exist for validation, but it must not become the product owner

### 2. Transport is not decision ownership

- transport acceptance does not authorize arbitration or render decisions
- a gateway or router may forward a seam without redefining the seam meaning
- payload routing and semantic ownership must remain separate

### 3. Boundary policy is explicit

- stale, timeout-clear, degraded, and fail-safe behavior must come from one boundary authority
- downstream nodes may consume boundary state, but they must not silently invent a second freshness policy

### 4. Observer stays out of operational ownership

- observer nodes may subscribe to published seams
- observer nodes must not become alternate product decision owners
- validation aggregation is allowed only after the operational owner has already published a seam
- outside an active validation lifecycle, observer seams must stay in a reset-safe idle state
- idle transport traffic must not overwrite validation observer reset values
- observer freshness or receive timestamps must come from actual observed transport or owner-published seams, not from synthetic harness-side inference

### 5. Diagnostic semantic and network request/response stay separate

- diagnostic semantic state may be published as a compact observation seam
- that semantic seam must not be treated as a replacement for the actual request/response route
- requester, gateway, ECU simulation, and semantic publisher roles must stay distinguishable

### 6. Validation-only stimulus must stay explicit

- `TEST_SCN` may inject validation-only transport stimuli in SIL
- that exception exists to drive product owners under test
- validation stimulus does not reassign product ownership of the target seam
- `TEST_SCN` may compute test verdict state, but that verdict must be derived from owner-published seams and test outputs
- `TEST_SCN` must not become a fallback semantic owner when product owners fail to publish
- `TEST_BAS` may aggregate observer results, but it must not synthesize alternate product meaning for the observed seam
- test harness state may orchestrate scenario timing, but it must not keep product semantic state alive after the product owner has already cleared it

## Current Project Application

### Emergency / V2X path

| Seam | Product owner | Transport role | Observer role | Validation-only exception |
| --- | --- | --- | --- | --- |
| `ETH_EmergencyAlert` | `V2X` | raw emergency ingress contract | trace only | `TEST_SCN` may emit this as a validation ingress stimulus; this does not make `TEST_SCN` the product owner |
| `Core::emergencyContext` | `V2X` | normalized internal semantic | `TEST_BAS`, evidence tools | none |
| `CoreState::emergencyIngressDirection / emergencyIngressEtaSec / emergencyIngressSourceId` | `V2X` | normalized ingress metadata seam for product consumers | `TEST_BAS`, evidence tools | none |
| `V2X::ingressHeartbeat` | `V2X` | ingress freshness heartbeat for acceptance/clear/watchdog transitions | `TEST_BAS`, evidence tools | none |
| `ETH_EmergencyMonitor` | `V2X` | transport-monitor publication | `TEST_BAS`, trace observers | none |
| `CoreState::selectedAlertDecisionLevel / selectedAlertDecisionType` | `ADAS` | functional selected-alert decision seam before gateway shaping | `TEST_BAS`, evidence tools | none |
| `CoreState::selectedAlertEffectiveLevel / selectedAlertEffectiveType / selectedAlertGateReason` | `CGW` | boundary-shaped selected-alert effective seam | `TEST_BAS`, evidence tools | none |
| `ethSelectedAlertMsg` / selected alert result | `ADAS` transport publication of selected-alert state for downstream consumers | transport relay of the active selected-alert state | `TEST_BAS`, evidence tools | none |
| `@Core::decelAssistDecisionReq` | `ADAS` | internal decision seam | `TEST_BAS`, debug traces | none |
| `CoreState::driverReleaseReason` | `ADAS` | driver-intervention release seam before gateway effective gating | `TEST_BAS`, debug traces | none |
| `@Core::decelAssistReq` / `CoreState::decelGateReason` | `CGW` | effective assist seam after boundary/fail-safe gating | `TEST_BAS`, debug traces | none |
| `ethFailSafeStateMsg` / `warningPathStatus` | `CGW` | boundary-health publication | `TEST_BAS`, trace observers | `TEST_SCN` may emit `ValidationOverride`; this must stay test-only |

### Render / output path

| Output meaning | Product owner | Required input |
| --- | --- | --- |
| visual warning level/type | `IVI`, `HUD`, `CLU` render side | `CoreState::selectedAlertEffective*` plus documented compatibility fallback |
| ambient / body warning actuation | `BCM` | CGW-effective selected-alert state plus boundary health |
| audio focus / ducking / volume guidance | `AMP`, `IVI`, `VCS` render side | CGW-effective selected-alert state plus user policy inputs |

Rule:

- render nodes consume owner-published result seams
- render consumers should prefer `effective -> decision -> compatibility fallback` in that order
- render nodes must not become alternate emergency ingress owners
- render and decision nodes should consume normalized ingress metadata from `CoreState` instead of raw `V2X::*` transport mirrors
- direct use of raw ingress context is allowed only as a documented compatibility path
- when `TEST_SCN` injects a direct emergency transport frame, legacy dispatch compatibility inputs must stay cleared; dispatch compatibility stimulus is reserved for dispatch-only validation paths

### Diagnostic path

| Seam | Owner | Role |
| --- | --- | --- |
| network request / response route | requester + gateway + ECU server path | actual transport and addressing flow |
| `Diag::*` semantic seam | `SGW` + `DCM` | compact observation of diagnostic status and result meaning |
| `EXT_DIAG` | logical external requester / observer surface | reads `Diag::*` in the current baseline; does not add a new backbone payload contract |

Rule:

- `EXT_DIAG` is not a replacement for a future DoIP or UDS stack
- `Diag::*` is an observation surface, not the transport contract itself

## Producer Boundary Rule For The Active Backbone

The current active baseline must preserve producer identity at the backbone seam.

| Backbone seam | Accepted producer |
| --- | --- |
| `ETH_EmergencyAlert` (current SIL validation ingress) | `TEST_SCN` |
| `ethObjectRiskInputMsg` | `TEST_SCN` |
| `ETH_EmergencyMonitor` | `V2X` |
| `ethSelectedAlertMsg` | `ADAS` |
| `ethDecelAssistReqMsg` | `ADAS` |
| `ethObjectRiskStateMsg` | `ADAS` |
| `ethObjectScenarioAlertMsg` | `ADAS` |
| `ethFailSafeStateMsg` | `CGW` |
| `ethObjectSafetyStateMsg` | `CGW` |
| `ethValidationOverride` | `TEST_SCN` |

Implication:

- backbone consumers must validate source ownership before treating a frame as authoritative
- self-originated transport must be rejected with a strict self-source check
- unexpected external sources may be traced and accepted for SIL continuity, but they must not silently become a second logical owner
- message ID match alone is not a sufficient authority check for the active development baseline

## Reading Order

Use the documents in this order:

1. `contracts/layer-separation-policy.md`
2. `contracts/owner-route.md`
3. `contracts/ethernet-interface.md`
4. `contracts/communication-matrix.md`
5. `contracts/multibus-policy.md`

Use this document when the question is:

- "who is the real owner?"
- "is this transport, decision, observer, or render?"
- "may a test node inject or observe this seam without becoming the owner?"

## Update Rule

When a seam changes role, update in this order:

1. `contracts/layer-separation-policy.md`
2. `contracts/owner-route.md`
3. `contracts/ethernet-interface.md`
4. `contracts/communication-matrix.md`
5. `contracts/multibus-policy.md`
6. runtime CAPL and verification assets

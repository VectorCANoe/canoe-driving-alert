# ECU Classification and Boundaries

## 1. Purpose

This document defines the stable runtime classification for the active CANoe SIL architecture.

The goal is to separate:

- domain-local ECU behavior
- cross-domain boundary control
- warning/arbitration logic
- output/render behavior
- validation-only harness behavior

This is an architecture document, not a GUI rebuild checklist.

## 2. Active architecture baseline

The active runtime uses:

- domain CAN for domain-local ECU contracts
- UDP multicast Ethernet for inter-domain backbone seams
- system variables for normalized state, panel binding, and verification seams

The active CAN databases are:

- `chassis_can.dbc`
- `powertrain_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `adas_can.dbc`

The active backbone transport baseline is:

- `UDP multicast 239.0.2.1:5000`

## 3. Classification model

The active ECU/runtime surface is classified into five layers.

| Layer | Role | Typical assets |
|---|---|---|
| Input edge | receives or injects raw domain context | `VCU`, `MDPS`, `IVI`, `V2X`, `TEST_SCN` |
| Boundary and normalization | converts domain inputs into normalized shared runtime state and health | `CGW`, normalized `Core::*`, selected `CoreState::*` |
| Decision and arbitration | computes alert meaning, priority, and fail-safe decisions | `ADAS`, related logic nodes |
| Output and presentation | converts selected runtime result into body/HMI/cluster behavior | `BCM`, `IVI`, `CLU`, `UiRender::*` |
| Verification harness | drives scenarios, aggregates verdicts, mirrors evidence | `TEST_SCN`, `TEST_BAS`, `Test::*`, `Diag::*` |

## 4. Layer boundaries

### 4.1 Input edge

Input-edge nodes own raw context acquisition or scenario injection.

Examples:

- `VCU` provides vehicle state context
- `MDPS` provides steering context
- `IVI` provides navigation and route context
- `V2X` provides emergency context ingress
- `TEST_SCN` injects validation-only context for SIL

Rule:

- input-edge nodes should not own final warning arbitration

### 4.2 Boundary and normalization

Boundary logic exists to absorb transport and domain differences before decision logic uses them.

Examples:

- `CGW` acts as the cross-domain boundary and health authority
- `Core::*` stores normalized values such as:
  - `Core::vehicleSpeedNorm`
  - `Core::driveStateNorm`
  - `Core::steeringInputNorm`
  - `Core::speedLimitNorm`
  - `Core::emergencyContext`
- `CoreState::*` stores runtime health and traceability mirrors such as:
  - `CoreState::domainBoundaryStatus`
  - `CoreState::warningPathStatus`
  - `CoreState::e2eHealthState`

Rule:

- boundary logic may normalize, mirror, or guard
- boundary logic should not silently absorb reviewer-visible business meaning

### 4.3 Decision and arbitration

Decision logic determines which warning should win and what the active output state should be.

Examples:

- `ADAS` publishes:
  - `ethSelectedAlertMsg`
  - `ethEmergencyRiskMsg`
  - `ethDecelAssistReqMsg`
  - `ethObjectRiskStateMsg`
  - `ethObjectScenarioAlertMsg`

Rule:

- final warning meaning belongs here, not in raw transport handlers

### 4.4 Output and presentation

Output nodes convert the selected runtime state into product-facing behavior.

Examples:

- `BCM` publishes ambient and body warning outputs
- `IVI` publishes cluster/HMI-facing infotainment outputs
- `CLU` and render mirrors expose display state
- `UiRender::*` mirrors derived visual state for panel/demo presentation

Primary visible outputs include:

- `Body::ambientMode`
- `Body::ambientColor`
- `Body::ambientPattern`
- `Cluster::warningTextCode`

Rule:

- output nodes consume selected runtime meaning
- output nodes must not become alternative arbitration owners

### 4.5 Verification harness

Verification assets are allowed to observe broadly and inject intentionally.

Examples:

- `TEST_SCN` orchestrates scenarios and cross-domain stimulus
- `TEST_BAS` aggregates final verdict state through `Test::*`
- `Diag::*` mirrors diagnostic request/response evidence

Rule:

- validation ownership is separate from product ownership
- harness convenience paths must not redefine the product architecture

## 5. Node classes

The active architecture distinguishes three practical node classes.

| Class | Meaning | Typical examples |
|---|---|---|
| Domain-local ECU | stays mostly within one CAN domain and performs product behavior there | `ESC`, `ABS`, `TPMS`, `BCM`, `DATC`, `NAV`, `TMU` |
| Cross-domain boundary ECU | requires foreign-domain visibility or backbone placement because it protects or bridges system behavior | `CGW`, selected multibus nodes such as `SCC`, `HWP`, `VCU` |
| Verification-only node | exists to stimulate, observe, or score SIL scenarios | `TEST_SCN`, `TEST_BAS` |

## 6. Non-negotiable architecture rules

### 6.1 Business semantics and transport must stay separate

Do not bind final warning meaning directly to a temporary transport seam.

Examples:

- do not treat a retired CAN stub frame as the architecture source of truth
- do not treat a fallback `Core::*` mirror as the primary published output contract

### 6.2 One visible owner per active contract

Each active message or state contract must have one clear logical owner in the active runtime.

Exceptions may exist for validation seams or transitional compatibility, but they must be documented explicitly.

### 6.3 Validation breadth does not justify product coupling

`TEST_SCN` is intentionally broad.

That does not justify widening product ECUs beyond the foreign visibility they actually need.

## 7. Design intent

The active architecture is intentionally shaped for Ethernet cutover:

- transport seams are already separated from much of the domain-local logic
- normalized state is centralized instead of duplicated in many product nodes
- validation is explicit and does not need to be disguised as product runtime ownership

This structure should be preserved as official documentation grows.

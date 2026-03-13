# Surface, Runtime, and Verification Map

## 1. Purpose

This document explains how the active CANoe SIL system is split across:

- user-facing surface
- runtime processing
- transport seams
- verification seams

It exists so agents and developers can locate the right source of truth quickly.

## 2. High-level map

| Layer | Primary source | Typical content |
|---|---|---|
| Surface | `project/panel/*`, `project/sysvars/project.sysvars` | panel inputs, output monitors, render mirrors |
| Runtime | `src/capl/**` | normalization, arbitration, output control, fail-safe |
| Transport | `databases/*.dbc`, UDP backbone contracts, `docs/contracts/*` | CAN frames, Ethernet seams, ownership policy |
| Verification | `tests/**`, `Test::*`, `Diag::*`, `docs/verification/*` | scenario orchestration, verdicts, evidence, diagnostic mirrors |

## 3. Surface layer

The surface layer is what a person or harness interacts with first.

### 3.1 Input surface

The current panel/system-variable input surface is based on these namespaces:

- `Chassis`
- `Infotainment`
- `V2X`
- `Test`

Representative inputs:

- `Chassis::vehicleSpeed`
- `Chassis::driveState`
- `Chassis::steeringInput`
- `Infotainment::roadZone`
- `Infotainment::navDirection`
- `Infotainment::zoneDistance`
- `V2X::emergencyType`
- `V2X::emergencyDirection`
- `V2X::eta`
- `V2X::alertState`
- `Test::scenarioCommand`

### 3.2 Output and monitor surface

The current monitored output surface is based on:

- `Body`
- `Cluster`
- `Core`
- `CoreState`
- `UiRender`
- `Diag`
- `Test`

Representative monitored outputs:

- `Body::ambientMode`
- `Body::ambientColor`
- `Body::ambientPattern`
- `Cluster::warningTextCode`
- `Core::selectedAlertLevel`
- `Core::selectedAlertType`
- `Core::timeoutClear`
- `CoreState::warningPathStatus`
- `CoreState::e2eHealthState`
- `UiRender::renderTextCode`
- `Test::scenarioResult`

## 4. Runtime layer

The runtime layer owns actual system behavior.

### 4.1 Input capture and normalization

Domain inputs are captured from CAN or UDP seams and normalized into `Core::*`.

Examples:

- vehicle state and steering context
- navigation context and speed limit
- emergency context and timing
- object-risk context for ADAS pre-activation

### 4.2 Arbitration and fail-safe

Runtime arbitration produces:

- selected alert meaning
- risk outputs
- fail-safe state
- degraded or blocked path decisions

This is runtime behavior, not a panel concern.

### 4.3 Output generation

Runtime outputs drive:

- ambient/body alerts
- cluster/HMI warning codes
- render-friendly mirrors
- verification and trace anchors

## 5. Transport layer

The transport layer exposes the runtime through domain CAN and Ethernet seams.

### 5.1 Domain CAN

Use domain CAN for domain-local ECU contracts.

Primary DBCs:

- `chassis_can.dbc`
- `powertrain_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `adas_can.dbc`

### 5.2 Ethernet backbone

Use UDP multicast Ethernet for active inter-domain seams.

Baseline:

- `239.0.2.1:5000`

Representative Ethernet seams:

- `ethVehicleStateMsg`
- `ethSteeringMsg`
- `ethNavContextMsg`
- `ETH_EmergencyAlert`
- `ethSelectedAlertMsg`
- `ethFailSafeStateMsg`
- `ethObjectRiskInputMsg`
- `ethObjectRiskStateMsg`

### 5.3 Where transport rules live

Use these documents for transport-level truth:

- `docs/contracts/10_ETHERNET_BACKBONE_SSoT.md`
- `docs/contracts/11_RUNTIME_MESSAGE_OWNERSHIP_MATRIX.md`
- `docs/contracts/12_RUNTIME_MULTIBUS_VISIBILITY_POLICY.md`
- `docs/contracts/13_ETH_INTERFACE_CONTRACT.md`

## 6. Verification layer

Verification is intentionally explicit.

### 6.1 Scenario and scoring seam

`TEST_SCN` drives system-wide scenarios and writes:

- `Test::scenarioResult`

`TEST_BAS` aggregates baseline results and writes:

- `Test::baseScenarioId`
- `Test::baseScenarioResult`
- `Test::baseFlowCoverageMask`
- `Test::baseTraceSnapshotId`
- `Test::baseTestHealth`

### 6.2 Diagnostic seam

Diagnostic observation is mirrored through `Diag::*`.

This keeps request/response evidence visible without turning product ECUs into ad-hoc debug owners.

### 6.3 Evidence surface

Verification evidence is expected from:

- trace / write-window observation
- `Test::*` verdict state
- `Diag::*` request/response mirrors
- official verification documents under `docs/verification/*`

## 7. Source-of-truth map

When deciding where to edit, use this order.

| Question | Edit here first |
|---|---|
| CAPL logic and runtime behavior | `src/capl/**` |
| GUI import mirror after CAPL sync | `cfg/channel_assign/**` |
| bit-level Ethernet contract | `docs/contracts/10_ETHERNET_BACKBONE_SSoT.md` |
| message owner or multibus policy | `docs/contracts/11_*`, `docs/contracts/12_*`, `docs/contracts/13_*` |
| panel/system-variable binding | `docs/contracts/17_PANEL_SYSVAR_BINDING_CONTRACT.md` |
| scenario pass criteria or evidence rules | `docs/verification/**` |

## 8. Design rule

The surface must stay thin.

The panel and sysvar surface should expose:

- controlled inputs
- readable outputs
- verification mirrors

The surface should not become a second runtime implementation.

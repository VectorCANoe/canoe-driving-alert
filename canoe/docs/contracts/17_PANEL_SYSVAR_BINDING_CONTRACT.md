# Panel and SysVar Binding Contract

## 1. Purpose

This document defines the stable binding contract between:

- CANoe panel inputs
- system-variable namespaces
- runtime-visible output monitors

It describes what the panel is allowed to write and what it should read for observation.

It does not describe panel editor click steps.

## 2. Active binding principle

The panel must bind to stable system-variable names, not to temporary aliases or transport-specific internals.

Primary rules:

- write to approved input namespaces only
- read product and verification outputs from approved monitor namespaces
- do not bind new widgets directly to temporary `g*` aliases
- do not treat `cfg/channel_assign/**` as the panel source of truth

## 3. Write surface

The panel write surface is limited to controlled input namespaces.

### 3.1 Chassis input bindings

| SysVar | Meaning | Direction |
|---|---|---|
| `Chassis::vehicleSpeed` | panel input speed | panel writes |
| `Chassis::driveState` | drive selector state | panel writes |
| `Chassis::steeringInput` | steering activity flag | panel writes |

### 3.2 Infotainment input bindings

| SysVar | Meaning | Direction |
|---|---|---|
| `Infotainment::roadZone` | road-zone context | panel writes |
| `Infotainment::navDirection` | navigation direction | panel writes |
| `Infotainment::zoneDistance` | distance to zone boundary | panel writes |
| `Infotainment::speedLimit` | speed-limit context when needed | panel writes or scripted input |

### 3.3 V2X input bindings

| SysVar | Meaning | Direction |
|---|---|---|
| `V2X::emergencyType` | emergency vehicle type | panel writes |
| `V2X::emergencyDirection` | emergency direction context | panel writes |
| `V2X::eta` | emergency ETA | panel writes |
| `V2X::sourceId` | emergency source identifier | panel writes when source tie-break is relevant |
| `V2X::alertState` | emergency active/clear state | panel writes |
| `V2X::policeDispatch` | police dispatch toggle | panel writes when dispatch flow is tested |
| `V2X::ambulanceDispatch` | ambulance dispatch toggle | panel writes when dispatch flow is tested |

### 3.4 Test control bindings

| SysVar | Meaning | Direction |
|---|---|---|
| `Test::testScenario` | selected SIL scenario id | panel or automation writes |
| `Test::scenarioCommand` | execute command | panel or automation writes |
| `Test::forceFailSafe` | validation override | panel or automation writes |
| `Test::displayModeSetting` | test-only HMI mode override | panel or automation writes |
| `Test::alertVolumeSetting` | test-only audio override | panel or automation writes |

## 4. Read surface

The panel monitor surface should prefer stable, reviewer-readable variables.

### 4.1 Primary product-visible outputs

| SysVar | Meaning | Direction |
|---|---|---|
| `Body::ambientMode` | ambient output mode | panel reads |
| `Body::ambientColor` | ambient output color | panel reads |
| `Body::ambientPattern` | ambient output pattern | panel reads |
| `Cluster::warningTextCode` | cluster warning result | panel reads |

### 4.2 Runtime status mirrors

| SysVar | Meaning | Direction |
|---|---|---|
| `Core::selectedAlertLevel` | selected alert level | panel reads |
| `Core::selectedAlertType` | selected alert type | panel reads |
| `Core::timeoutClear` | timeout clear state | panel reads |
| `Core::proximityRiskLevel` | emergency proximity risk | panel reads |
| `Core::decelAssistReq` | deceleration assist request | panel reads |
| `Core::failSafeMode` | fail-safe mode | panel reads |

### 4.3 Health and traceability mirrors

| SysVar | Meaning | Direction |
|---|---|---|
| `CoreState::warningPathStatus` | warning-path health state | panel reads |
| `CoreState::e2eHealthState` | end-to-end health state | panel reads |
| `CoreState::domainBoundaryStatus` | boundary alive summary | panel reads |
| `CoreState::lastEmergencyRxMs` | emergency receive timestamp mirror | panel reads |
| `CoreState::alertHistoryCount` | alert history accumulation | panel reads |

### 4.4 Verification and render mirrors

| SysVar | Meaning | Direction |
|---|---|---|
| `Test::scenarioResult` | per-scenario PASS/FAIL summary | panel reads |
| `Test::baseScenarioResult` | baseline aggregate PASS/FAIL | panel reads |
| `Diag::*` | diagnostic observation seam | panel or tools read |
| `UiRender::*` | presentation-only derived render state | panel reads when demo rendering is used |

## 5. Binding rules

### 5.1 Input widgets write only to input namespaces

The panel must not write directly to:

- `Core::*`
- `CoreState::*`
- `Body::*`
- `Cluster::*`
- `UiRender::*`

unless a widget is explicitly documented as a verification-only override.

### 5.2 Runtime mirrors are not command inputs

`Core::*` and `CoreState::*` are for observation, normalization, and evidence.

Do not treat them as the first input seam for new panel controls.

### 5.3 Keep panel bindings name-stable

If implementation aliases or transport handlers change, preserve the public panel/sysvar binding names whenever possible.

The panel should not churn because an internal CAPL refactor happened.

### 5.4 Verification-only controls must stay labeled

Any panel control that writes `Test::*` or similar harness-only variables must be visibly marked as:

- validation-only
- non-product behavior

## 6. Recommended page grouping

The current binding model is stable when panel pages are grouped like this:

| Page | Primary namespaces |
|---|---|
| Drive input | `Chassis::*` |
| Navigation input | `Infotainment::*` |
| Emergency input | `V2X::*` |
| Output monitor | `Body::*`, `Cluster::*`, `Core::*`, `CoreState::*` |
| Verification / diagnostics | `Test::*`, `Diag::*`, optional `UiRender::*` |

## 7. Update rule

When the panel surface changes:

1. update `project/sysvars/project.sysvars` if the public sysvar surface changes
2. update the panel assets under `project/panel/*`
3. update this contract document
4. update verification documents if scenario execution or evidence interpretation changed

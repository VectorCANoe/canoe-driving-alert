# Panel and SysVar Binding Contract

> [!IMPORTANT]
> This document reflects the current runtime baseline.
> The active operator/input model is now `Input_Console -> Cmd::* / Inject::* / Test::* -> owner ECU -> state/readback`.
> Older donor input panels remain only as transitional compatibility assets and must not be treated as the long-term command source.

## 1. Purpose

This document defines the current stable contract between:

- CANoe operator/input panels
- system-variable namespaces
- owner ECU runtime seams
- observer/readback panels

It answers three questions:

1. which namespaces an input panel is allowed to write
2. which namespaces observer panels are expected to read
3. which legacy seams still exist only for compatibility and must not be used for new widgets

It does not describe Panel Designer click steps.

## 2. Current Panel Model

### 2.1 Active command source

The target active command source is:

- [Input_Console.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Input_Console.xvp)

Its pages are:

- `Vehicle`
- `Context`
- `Scenario`

This local panel is allowed to write only:

- `Cmd::*`
- `Inject::*`
- `Test::*`

### 2.2 Observer/readback panels

The following panels are observer/readback surfaces by runtime contract:

- [Cluster_Alert.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Cluster_Alert.xvp)
- [Navigation_Alert.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Navigation_Alert.xvp)
- [Cabin_Cockpit.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Cabin_Cockpit.xvp)
- [Vehicle_Dashboard.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Vehicle_Dashboard.xvp)
- [Body_Status.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Body_Status.xvp)
- [Ambient_TopView.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Ambient_TopView.xvp)
- [V2X_Ingress.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/V2X_Ingress.xvp)
- [V2X_Cross.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/V2X_Cross.xvp)
- [Diagnostic_Console.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Diagnostic_Console.xvp)

### 2.3 Transitional donor input panels

The following donor panels still exist but are transitional compatibility assets only:

- [Ambient_Control.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Ambient_Control.xvp)
- [Cruise_Pedal.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Cruise_Pedal.xvp)
- [Driver_Control.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Driver_Control.xvp)
- [Operator_Input.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Operator_Input.xvp)
- [Scenario_Control.xvp](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Scenario_Control.xvp)

They must not remain co-open as active command sources beside `Input_Console` after cutover.

## 3. Active Write Surface

## 3.1 Vehicle command namespace

| SysVar | Meaning | Writer |
|---|---|---|
| `Cmd::ignitionCmd` | ignition request | input panel |
| `Cmd::driveStateCmd` | gear selector request | input panel |
| `Cmd::vehicleSpeedCmd` | vehicle speed request | input panel |
| `Cmd::steeringAngleCmd` | steering request | input panel |
| `Cmd::throttlePedalPct` | accelerator pedal request | input panel |
| `Cmd::brakePedalPct` | brake pedal request | input panel |
| `Cmd::cruiseStateCmd` | cruise mode request | input panel |
| `Cmd::cruiseSetSpeedCmd` | cruise set-speed request | input panel |
| `Cmd::doorLockCmd` | door lock request | input panel |
| `Cmd::doorOpenCmd` | door open/close request | input panel |
| `Cmd::windowCmd` | window request | input panel |
| `Cmd::wiperCmd` | wiper level request | input panel |
| `Cmd::turnSignalCmd` | turn/hazard request | input panel |
| `Cmd::ambientModeCmd` | ambient mode request | input panel |

## 3.2 Context / injection namespace

| SysVar | Meaning | Writer |
|---|---|---|
| `Inject::roadZone` | road-zone context injection | input panel or harness |
| `Inject::navDirection` | navigation direction injection | input panel or harness |
| `Inject::zoneDistance` | distance-to-zone injection | input panel or harness |
| `Inject::speedLimit` | speed-limit injection | input panel or harness |
| `Inject::emergencyActiveCmd` | emergency ingress enable | input panel or harness |
| `Inject::emergencyType` | emergency type injection | input panel or harness |
| `Inject::emergencyDirection` | emergency direction injection | input panel or harness |
| `Inject::emergencyEtaSec` | emergency ETA injection | input panel or harness |
| `Inject::emergencySourceId` | emergency source-id injection | input panel or harness |
| `Inject::manualAlertOverrideCmd` | manual alert override request | input panel or harness |
| `Inject::alertVolumeCmd` | alert-volume request | input panel |

## 3.3 Scenario / validation namespace

| SysVar | Meaning | Writer |
|---|---|---|
| `Test::scenarioCommand` | scenario launch command | input panel or automation |
| `Test::testScenario` | selected scenario / compat stop control | input panel or automation |
| `Test::scenarioStopReq` | explicit scenario stop request | input panel or automation |
| `Test::forceFailSafe` | validation-only fail-safe override | input panel or automation |
| `Test::displayModeSetting` | validation-only display mode override | input panel or automation |

## 3.4 Transitional exceptions

These seams still exist and may appear in transitional panels or helper scenes.
Do not use them for new widgets unless the user explicitly approves the exception.

| SysVar | Reason |
|---|---|
| `V2X::AnimationTrigger` | local `V2X_Cross` scene trigger |
| `V2X::policePos` | temporary proximity preset compatibility |
| `V2X::ambulancePos` | temporary proximity preset compatibility |
| `Test::driverBeltOff` | temporary belt toggle compatibility |
| `Test::passengerBeltOff` | temporary belt toggle compatibility |

## 4. Observer / Readback Surface

Observer panels must prefer owner-state seams.

## 4.1 Vehicle / body readback

| SysVar / signal | Meaning | Primary owner |
|---|---|---|
| `Chassis::vehicleSpeed` | vehicle speed readback | `VCU` |
| `Chassis::driveState` | drive state readback | `VCU` |
| `Display::steeringFrame` | steering animation/readback | `CLU` |
| `Chassis::brakeLamp` | brake lamp state | `ESC` |
| `Body::frontWiperAnimFrame` | wiper animation frame | `WIP` |
| `Body::blinkLeft` | left turn state | `BCM` |
| `Body::blinkRight` | right turn state | `BCM` |
| `Powertrain::coolantTemp` | coolant temperature | `EMS` or powertrain owner |
| `Powertrain::fuelLevel` | fuel level | powertrain owner |
| `Powertrain::cruiseState` | cruise state readback | `SCC` |
| `Powertrain::cruiseSetSpeed` | cruise set-speed readback | `SCC` |
| `Display::animFrame` | main animation frame | `EMS` |
| `Infotainment::cabinAmbientAnimFrame` | cabin ambient frame | infotainment owner |
| `powertrain_can::frmGearStateMsg.GearState` | donor gear readback signal | `VCU` path |
| `powertrain_can::frmEngineSpeedTempMsg.EngineRpm` | engine speed signal | `EMS` |
| `body_can::frmDoorFlStateMsg.DoorFlWindowPos` | window state signal | `DOOR_FL` |

## 4.2 Alert / context readback

| SysVar | Meaning | Primary owner |
|---|---|---|
| `Core::selectedAlertLevel` | final alert level | `ADAS` |
| `Core::selectedAlertType` | final alert type | `ADAS` |
| `Core::timeoutClear` | timeout clear state | `ADAS` / runtime |
| `Core::proximityRiskLevel` | proximity risk | `ADAS` |
| `Core::decelAssistReq` | decel assist request | `ADAS` |
| `Core::failSafeMode` | fail-safe state | runtime owner |
| `Core::vehicleSpeedNorm` | normalized speed | `ADAS` / integration path |
| `Core::speedLimitNorm` | normalized speed limit | `IVI` / integration path |
| `CoreState::baseVolume` | audio base volume | `AMP` |
| `Cluster::warningTextCode` | cluster warning text | `CLU` |
| `UiRender::roadZoneColorCode` | road-zone render color | `IVI` |
| `UiRender::navLaneFrame` | nav lane frame | `NAV` |
| `UiRender::renderVolumLevel` | rendered volume level | `AMP` |
| `UiRender::warningBeepState` | warning beep state | `IVI` / `AMP` path |
| `UiRender::beepEmergency` | emergency audio state | `IVI` / `AMP` path |
| `UiRender::beepSpeed` | speed audio state | `IVI` / `AMP` path |
| `UiRender::beepIC` | intersection/crossing audio state | `IVI` / `AMP` path |
| `UiRender::roadFlowDirection` | road-flow direction render | `IVI` |
| `Infotainment::emergencySound` | emergency sound mirror | `V2X` |
| `V2X::v2xFrame` | ingress scene frame | `V2X` |
| `V2X::MyCarFrame` | cross-scene ego frame | `V2X` |
| `V2X::AmbFrame` | cross-scene ambulance frame | `V2X` |
| `V2X::CrossAnimAlertActive` | cross-scene popup active mirror | `V2X` |

## 4.3 Scenario / harness readback

| SysVar | Meaning | Primary owner |
|---|---|---|
| `Test::scenarioActiveId` | active scenario id | `TEST_SCN` |
| `Test::scenarioResult` | scenario result | `TEST_SCN` |
| `Test::scenarioCommandAck` | last scenario ack | `TEST_SCN` |
| `Test::scenarioLampStop` | stop lamp state | `TEST_SCN` |
| `Test::scenarioLampWarn` | warn lamp state | `TEST_SCN` |
| `Test::scenarioLampRun` | run lamp state | `TEST_SCN` |

## 4.4 Diagnostic readback

| SysVar | Meaning |
|---|---|
| `Diag::*` | diagnostic observer surface |

## 5. Binding Rules

## 5.1 New input widgets must not write product readback seams

Do not bind new input widgets directly to:

- `Chassis::*`
- `Body::*`
- `Powertrain::*`
- `Core::*`
- `CoreState::*`
- `Cluster::*`
- `UiRender::*`
- `Diag::*`
- legacy `Infotainment::roadZone`
- legacy `Infotainment::navDirection`
- legacy `Infotainment::zoneDistance`
- legacy `Infotainment::speedLimit`
- legacy `Test::manualAlertOverride`
- legacy `Test::alertVolumeSetting`

## 5.2 Observer semantics are runtime-defined, not `ReadOnlyControl`-defined

Some frozen donor display widgets do not explicitly serialize `ReadOnlyControl=True`.
That does **not** make them valid command widgets.

Ownership is decided by:

- runtime seam SoT
- panel role
- owner ECU writer map

not by the presence or absence of one XVP property.

## 5.3 One command domain, one active source

At runtime:

- `Vehicle` commands must come from one active operator surface
- `Context` injections must come from one active operator surface
- `Scenario` lifecycle must come from one active operator surface

Do not intentionally keep multiple input panels active on the same command domain.

## 5.4 `TEST_SCN` is harness-only

`TEST_SCN` may write:

- `Test::*` lifecycle/evidence seams
- approved `Inject::*` scenario lock seams

`TEST_SCN` must not become the normal feature owner for:

- manual vehicle control
- body comfort control
- legacy context state seams

## 5.5 `Navigation_Alert.xvp` is observer-audit-hold

The frozen donor XVP still contains writable `Test::alertVolumeSetting`.
Until that path is fully retired from operation:

- treat `Navigation_Alert.xvp` as `display-first / observer-audit-hold`
- do not describe it as a fully clean observer panel in closeout evidence

## 6. Recommended Operator / Observer Grouping

| Group | Purpose | Primary namespaces |
|---|---|---|
| `Vehicle` | manual driving and body control | `Cmd::*` |
| `Context` | warning, road, nav, emergency, V2X injection | `Inject::*` |
| `Scenario` | validation harness lifecycle | `Test::*` |
| Vehicle/body observers | cockpit, dashboard, body status | `Chassis::*`, `Body::*`, `Powertrain::*`, `Display::*` |
| Alert/context observers | cluster, navigation, ambient, V2X | `Core::*`, `CoreState::*`, `Cluster::*`, `UiRender::*`, `V2X::*`, `Infotainment::*` |
| Diagnostic observer | external diagnostic monitor | `Diag::*` |

## 7. Evidence Note

For verification and closeout:

- output/readback evidence must use observer panels, not retired donor input panels
- panel capture should be tied to:
  - test ID
  - scenario ID
  - exact panel name
  - evidence path
- if a panel is transitional or mixed, call that out explicitly in the evidence note

## 8. Update Rule

When the panel/runtime surface changes:

1. update [project.sysvars](/C:/Users/이준영/CANoe-IVI-OTA/canoe/project/sysvars/project.sysvars) if the public surface changes
2. update CAPL owner/runtime behavior under:
   - [canoe/src/capl](/C:/Users/이준영/CANoe-IVI-OTA/canoe/src/capl)
   - [canoe/cfg/channel_assign](/C:/Users/이준영/CANoe-IVI-OTA/canoe/cfg/channel_assign)
3. update this contract document
4. update verification/evidence documents if panel role, scenario interpretation, or observer evidence meaning changed

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

## 3.5 Input_Console Detailed Contract

This section is the implementation target for the local `Input_Console`.
It fixes the command/readback meaning so donor widgets can be retired without seam collision.

### 3.5.1 Vehicle page

| UI function | Active write seam | Value map / range | Readback seam | Owner | Widget contract | Legacy donor status |
|---|---|---|---|---|---|---|
| Ignition | `Cmd::ignitionCmd` | `0=off, 1=on` | `Chassis::ignitionCmd` or owner-equivalent state | `EMS` / `VCU` path | two-state explicit mapping widget | replaces legacy chassis/manual ignition input |
| Gear select | `Cmd::driveStateCmd` | `0=P, 1=R, 2=N, 3=D` | `Chassis::driveState` | `VCU` | explicit discrete value widget | replaces donor gear command path |
| Speed preset | `Cmd::vehicleSpeedCmd` | `0..255 km/h`; current presets may be `0/30/50/80/100` | `Chassis::vehicleSpeed` | `VCU` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces manual speed input donor path |
| Steering | `Cmd::steeringAngleCmd` | `-540..+540 deg`; local UI uses fixed preset commands | `Chassis::steeringAngle`, `Display::steeringFrame` | `MDPS` / `CLU` | explicit discrete-value widget for command, observer indicator for frame | replaces legacy `manualSteeringAngleCmd` style path |
| Brake pedal | `Cmd::brakePedalPct` | `0..100 %` | `Chassis::brakePressure` | `ESC` | bounded actuation widget; donor pedal art may be reused as visual only | do not write legacy `Chassis::brakePedalBtn` from new widgets |
| Throttle pedal | `Cmd::throttlePedalPct` | `0..100 %` | `Chassis::throttlePosition` | `VCU` / `EMS` | bounded actuation widget; donor pedal art may be reused as visual only | do not write legacy `Chassis::throttlePedalBtn` from new widgets |
| Cruise mode | `Cmd::cruiseStateCmd` | `0=off, 1=on, 2=decel-assist` | `Powertrain::cruiseState` | `SCC` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces donor CAN signal write path |
| Cruise set speed | `Cmd::cruiseSetSpeedCmd` | `0..255 km/h`; current presets may be `30/50/80/100` | `Powertrain::cruiseSetSpeed` | `SCC` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces donor CAN signal write path |
| Meter / live speed | none; observer only | n/a | `Chassis::vehicleSpeed` | `VCU` | readback-only meter/LCD | local console-only observer aid |
| Door lock | `Cmd::doorLockCmd` | `0=hold, 1=unlock, 2=lock` | owner lock state mirror if exposed | `DOOR_FL` / `BCM` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | do not write legacy `Body::doorLockCmd` from new widgets |
| Door open | `Cmd::doorOpenCmd` | `0=hold, 1=open, 2=close` | owner open state mirror if exposed | `DOOR_FL` / `BCM` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | do not write legacy `Body::doorOpenCmd` from new widgets |
| Window | `Cmd::windowCmd` | `0=hold, 1=up, 2=down` | `Body::windowPos` | `DOOR_FL` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | do not write legacy `Body::windowCmd` from new widgets |
| Wiper | `Cmd::wiperCmd` | `0=off, 1=intermittent, 2=high` | `Body::frontWiperAnimFrame` | `WIP` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | do not write legacy `Body::wiperCmd` from new widgets |
| Turn signal | `Cmd::turnSignalCmd` | `0=off, 1=left, 2=right, 3=hazard` | `CoreState::turnLampState`, `Body::blinkLeft`, `Body::blinkRight` | `BCM` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | do not write legacy `Body::manualTurnCmd` from new widgets |
| Ambient mode | `Cmd::ambientModeCmd` | `0..7` | `Body::ambientMode` | `BCM` / ambient owner | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | planned local-console migration item |
| Driver belt sim | `Test::driverBeltOff` | `0=normal, 1=driver belt off` | consumer-specific warning/readback seam | `TEST_SCN` compat path | explicit two-state widget only if belt sim is kept local | transitional exception only |
| Passenger belt sim | `Test::passengerBeltOff` | `0=normal, 1=passenger belt off` | consumer-specific warning/readback seam | `TEST_SCN` compat path | explicit two-state widget only if belt sim is kept local | transitional exception only |

### 3.5.2 Context page

| UI function | Active write seam | Value map / range | Readback seam | Owner | Widget contract | Legacy donor status |
|---|---|---|---|---|---|---|
| Road zone | `Inject::roadZone` | `0=normal, 1=school, 2=highway, 3=guide` | `Infotainment::roadZone`, `Core::baseZoneContext` | `IVI` / `NAV` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `Infotainment::roadZone` write path |
| Navigation direction | `Inject::navDirection` | `0=none, 1=left, 2=right, 3=other/straight` | `Infotainment::navDirection` | `IVI` / `NAV` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `Infotainment::navDirection` write path |
| Zone distance | `Inject::zoneDistance` | `0..255 m`; local UI exposes fixed representative presets | `Infotainment::zoneDistance` | `NAV` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `Infotainment::zoneDistance` write path |
| Speed limit | `Inject::speedLimit` | `0..255 km/h`; local UI exposes fixed representative presets | `Core::speedLimitNorm` | `NAV` / `ADAS` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `Infotainment::speedLimit` write path |
| Emergency active | `Inject::emergencyActiveCmd` | `0=clear, 1=active` | `Core::emergencyContext` and ingress mirrors | `V2X` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy alert on/off path |
| Emergency type | `Inject::emergencyType` | `0=none, 1=police, 2=ambulance` | `Core::emergencyContext`, `V2X::emergencyType` compat mirror | `V2X` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `V2X::emergencyType` write path |
| Emergency direction | `Inject::emergencyDirection` | `0=front, 1=left, 2=right, 3=rear` | `CoreState::emergencyIngressDirection`, `V2X::emergencyDirection` compat mirror | `V2X` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `V2X::emergencyDirection` write path |
| Emergency ETA | `Inject::emergencyEtaSec` | `0..255 s`; local UI uses dense stepped slider for fine adjustment | `CoreState::emergencyIngressEtaSec`, `V2X::eta` compat mirror | `V2X` | stepped `TrackBarControl` allowed for continuous time-domain injection | replaces legacy `V2X::eta` write path |
| Emergency source ID | `Inject::emergencySourceId` | `0..255` | `CoreState::emergencyIngressSourceId` if exposed | `V2X` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `V2X::sourceId` write path |
| Manual alert override | `Inject::manualAlertOverrideCmd` | `0..255`; local presets may expose representative levels only | `Core::selectedAlertLevel`, `Core::selectedAlertType` | `ADAS` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `Test::manualAlertOverride` write path |
| Audio base / alert volume | `Inject::alertVolumeCmd` | `0=default, 1..100=explicit`; local UI exposes fixed representative presets | `CoreState::baseVolume`, `UiRender::renderVolumLevel` | `AMP` | explicit discrete-value widget; button bank or button-style `SwitchControl` both allowed if Tx values are fixed in XVP | replaces legacy `Test::alertVolumeSetting` write path |
| Cross trigger | `V2X::AnimationTrigger` | `0=off, 1=on` | `V2X::CrossAnimAlertActive` | local V2X scene compat | explicit two-state widget only if cross scene remains in local console | transitional exception only |
| Police proximity | `V2X::policePos` | `0..7`; local UI exposes fixed representative presets | `V2X` compat scene frame path | local V2X scene compat | discrete preset button bank | transitional exception only |
| Ambulance proximity | `V2X::ambulancePos` | `0..7`; local UI exposes fixed representative presets | `V2X` compat scene frame path | local V2X scene compat | discrete preset button bank | transitional exception only |

### 3.5.3 Scenario page

| UI function | Active write seam | Value map / range | Readback seam | Owner | Widget contract | Legacy donor status |
|---|---|---|---|---|---|---|
| Scenario preset launch | `Test::scenarioCommand` | `1, 2, 3, 4, 5, 7, 8, 20, 21, 100` | `Test::scenarioActiveId`, `Test::scenarioCommandAck`, `Test::scenarioResult` | `TEST_SCN` | explicit discrete value widget with fixed Tx values | replaces donor `Scenario_Control` preset writes |
| Scenario stop / manual return | `Test::scenarioStopReq` | `0=idle, 1=stop request` | `Test::scenarioLampStop`, `Test::scenarioActiveId` | `TEST_SCN` | one-shot explicit widget | replaces active stop ownership; donor `Test::testScenario` becomes compat only |
| Compat stop seam | `Test::testScenario` | `0=manual baseline`; additional values only if compat is intentionally exposed | compat-only readback/owner behavior | `TEST_SCN` | compat widget only when explicit parity is needed | not a new primary scenario-launch seam |
| Scenario start request | `Test::scenarioStartReq` | `0=idle, 1=start request` | lifecycle mirrors if exposed | `TEST_SCN` | one-shot explicit widget only when lifecycle UI is enabled | local-console lifecycle extension |
| Scenario ack request | `Test::scenarioAckReq` | `0=idle, 1=ack request` | lifecycle mirrors if exposed | `TEST_SCN` | one-shot explicit widget only when lifecycle UI is enabled | local-console lifecycle extension |
| Scenario stop/warn/run lamps | none; observer only | n/a | `Test::scenarioLampStop`, `Test::scenarioLampWarn`, `Test::scenarioLampRun` | `TEST_SCN` | readback-only LED controls | observer aid only |
| Active/result/ack displays | none; observer only | n/a | `Test::scenarioActiveId`, `Test::scenarioResult`, `Test::scenarioCommandAck` | `TEST_SCN` | readback-only text/LCD controls | observer aid only |

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

## 5.6 Interactive widget rule

For `Input_Console`, the authoritative command meaning is fixed by the detailed contract table in section `3.5`.
Widget choice must follow that contract, not redefine it.

Preferred final command widgets:

- explicit discrete-value widgets for enumerated commands
- `Check Box` only for simple two-state toggles such as transitional belt simulation
- `Picture Box` only as visual accompaniment
- `LED`, `LCD`, `Input/Output Box`, `Progress Bar`, `Meter` only as readback surfaces

Preferred explicit-value patterns:

- `ButtonControl` only when the per-button Tx value is actually serialized or otherwise guaranteed by the XVP contract
- button-style `SwitchControl` with `SwitchValuesVT` / `SwitchValuesVTXml` when per-button Tx values must be encoded explicitly

Transitional allowance:

- donor-like `SwitchControl` remains acceptable for `Scenario` launch and for any discrete command where it is the only proven explicit Tx-value carrier in current XVP practice

Not acceptable for the final local console:

- `TrackBarControl`
- `RadioButtonControl`
- `ComboBoxControl` as the primary command selector
- a `ButtonControl` bank whose per-button value contract is not explicitly defined in section `3.5` and not explicitly serialized in XVP
- donor visual assets reused while still writing legacy owner/readback seams directly

If donor visuals are reused, only the image contract may be borrowed.
The authoritative write seam must still remain:

- `Cmd::*`
- `Inject::*`
- `Test::*`

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

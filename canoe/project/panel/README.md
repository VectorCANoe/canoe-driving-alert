# project/panel

Current root panel set for `develop`.

## Source Policy

- Root `canoe/project/panel/*.xvp` is the panel source of truth.
- Imported donor panels are frozen at donor design/binding level.
- Current root filenames are project-normalized names, but internal XVP content and contract semantics are donor-canonical.
- Do not change donor panel layout, widget type, label, root `ControlName`, or existing donor binding contract.
- Runtime adaptation must be done in:
  - `canoe/project/sysvars/project.sysvars`
  - `canoe/src/capl`
  - `canoe/cfg/channel_assign`
- `Diagnostic_Console.xvp`, `Input_Console.xvp`, and `V2X_Cross.xvp` are local project-specific panels outside the donor set.
- Detailed frozen contract matrix: `../../AGENT/canoe/docs/operations/panel/DONOR_PANEL_CONTRACT_MATRIX_2026-03-21.md`

## Current Root Inventory

- `Ambient_Control.xvp`
- `Ambient_TopView.xvp`
- `Body_Status.xvp`
- `Cabin_Cockpit.xvp`
- `Cluster_Alert.xvp`
- `Cruise_Pedal.xvp`
- `Diagnostic_Console.xvp`
- `Input_Console.xvp`
- `Driver_Control.xvp`
- `Navigation_Alert.xvp`
- `Operator_Input.xvp`
- `Scenario_Control.xvp`
- `V2X_Ingress.xvp`
- `V2X_Cross.xvp`
- `Vehicle_Dashboard.xvp`

## Donor Mapping

| Current root file | Donor baseline source |
| --- | --- |
| `Ambient_Control.xvp` | `Ambient_Control.xvp` |
| `Ambient_TopView.xvp` | `Ambient_Top_View.xvp` |
| `Body_Status.xvp` | `windowstate.xvp` |
| `Cabin_Cockpit.xvp` | `car_inner.xvp` |
| `Cluster_Alert.xvp` | `cluster.xvp` |
| `Cruise_Pedal.xvp` | `sample_Control.xvp` |
| `Driver_Control.xvp` | `MyDriverPanel.xvp` |
| `Input_Console.xvp` | local project panel |
| `Navigation_Alert.xvp` | `Navigation.xvp` |
| `Operator_Input.xvp` | `input.xvp` |
| `Scenario_Control.xvp` | `scenariocontrol.xvp` |
| `V2X_Ingress.xvp` | `v2xpanel.xvp` |
| `V2X_Cross.xvp` | local project panel |
| `Vehicle_Dashboard.xvp` | `sample_Dashboard.xvp` |
| `Diagnostic_Console.xvp` | local project panel |

## Input / Output Pairing

| Pair set | Input / control panel | Output / display panel | Current Desktop_ASSIGN copies | Main runtime seam |
| --- | --- | --- | --- | --- |
| Ambient | `Ambient_Control.xvp` | `Ambient_TopView.xvp` | `Module/Ambient_Control.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | `Body::*`, `Infotainment::*`, `UiRender::*` |
| Driver / body | `Driver_Control.xvp` | `Body_Status.xvp` | `Module/Driver_Control.xvp`, `3D/Driver_Control.xvp`, `3D/Body_Status.xvp` | `Body::*`, `Chassis::*` |
| Driver / cabin | `Driver_Control.xvp` | `Cabin_Cockpit.xvp` | `Module/Driver_Control.xvp`, `3D/Driver_Control.xvp`, `Cabin/Cabin_Cockpit.xvp` | `Body::*`, `Display::*`, `Powertrain::*` |
| Cruise / vehicle | `Cruise_Pedal.xvp` | `Vehicle_Dashboard.xvp` | `Module/Cruise_Pedal.xvp`, `Cabin/Cruise_Pedal.xvp`, `Cabin/Vehicle_Dashboard.xvp` | `Chassis::*`, `Powertrain::*` |
| Manual warning | `Operator_Input.xvp` | `Cluster_Alert.xvp`, `Navigation_Alert.xvp`, `Ambient_TopView.xvp` | `Module/Operator_Input.xvp`, `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | `Core::*`, `CoreState::*`, `UiRender::*` |
| Scenario warning | `Scenario_Control.xvp` | `Cluster_Alert.xvp`, `Navigation_Alert.xvp`, `Ambient_TopView.xvp`, `V2X_Ingress.xvp` | `3D/Scenario_Control.xvp`, `3D/V2X_Ingress.xvp`, `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | `Test::*`, `V2X::*`, `Core::*` |
| Cross scene | `Scenario_Control.xvp` or future local scenario input | `V2X_Cross.xvp` | `3D/V2X_Cross.xvp` | `V2X::AnimationTrigger`, `MyCarFrame`, `AmbFrame`, `Display::animFrame` |
| Diagnostic monitor | none | `Diagnostic_Console.xvp` | `Diag/Diagnostic_Console.xvp` | `Diag::*`, domain health mirrors |

The input-side entries above document frozen donor pairings and current GUI placement only. They do not grant long-term active-command ownership once the local `Input Console` is introduced.

## Runtime Meaning

| Root file | Primary role |
| --- | --- |
| `Ambient_Control.xvp` | ⛔ RETIRED — close from Desktop |
| `Ambient_TopView.xvp` | 3D ambient/effect visualization |
| `Body_Status.xvp` | body/window/light status view |
| `Cabin_Cockpit.xvp` | cabin/cockpit visualization |
| `Cluster_Alert.xvp` | cluster-side warning presentation |
| `Cruise_Pedal.xvp` | ⛔ RETIRED — close from Desktop |
| `Diagnostic_Console.xvp` | diagnostic observer console |
| `Driver_Control.xvp` | ⛔ RETIRED — close from Desktop |
| `Input_Console.xvp` | local tabbed `Vehicle` / `Context` / `Scenario` command console |
| `Navigation_Alert.xvp` | navigation/warning presentation; legacy audio-control binding requires audit before full observer-only demotion |
| `Operator_Input.xvp` | ⛔ RETIRED — close from Desktop |
| `Scenario_Control.xvp` | ⛔ RETIRED — close from Desktop |
| `V2X_Ingress.xvp` | V2X ingress scene/status view |
| `V2X_Cross.xvp` | V2X crossing animation observer view |
| `Vehicle_Dashboard.xvp` | vehicle dashboard state view |

## Active Runtime Focus

- legacy donor command panels still exist for compatibility, but they are not the redesign end-state
- cutover target active command pages inside one local `Input Console` are:
  - local `Vehicle`
  - local `Context`
  - local `Scenario`
- donor input panels that must retire from active-source status when the local input console lands:
  - `Ambient_Control.xvp`
  - `Cruise_Pedal.xvp`
  - `Driver_Control.xvp`
  - `Operator_Input.xvp`
  - `Scenario_Control.xvp`
- do not keep retired donor input panels open beside the new local input console; GUI co-open is a duplicate command source
- current runtime priority is not `driver-view natural HMI`
- current runtime priority is:
  - engineer manual control
  - scenario / validation injection
- all remaining donor panels are treated as observer / readback panels
- `Navigation_Alert.xvp` is `display-first / observer-audit-hold` because the frozen donor XVP still exposes writable `Test::alertVolumeSetting`
- runtime adaptation rule:
  - the local `Input Console` owns writable command / injection seams
  - owner ECU or `VALIDATION_HARNESS(TEST_SCN)` consumes those seams
  - donor observer panels read final state only

## Next Operator Architecture

- donor output/readback panels remain frozen and continue as observer-only surfaces
- future cleanup must not keep donor command panels active beside the new local input console
- default redesign direction is one local `Input Console` patterned after `Diagnostic_Console.xvp`
- the panel switches screens inside one XVP:
  - `Vehicle`
  - `Context`
  - `Scenario`
- preferred domain boundary is:
  - `Vehicle`
    - `Cmd::*`
    - ignition / gear / steering / pedal / cruise / door / window / wiper / turn / ambient
  - `Context`
    - `Inject::*`
    - road zone / nav direction / zone distance / speed limit / emergency type / direction / eta / source id / alert override / alert-volume request
  - `Scenario`
    - `Test::*`
    - validation harness start / stop / ack / status only
- use three separate local panels only as fallback if GUI stability blocks the single-console flow
- the important rule is semantic separation, not the number of XVP files
- local input widgets must be visual and actuation-oriented:
  - switches, momentary buttons, rocker controls, pedal sliders/click widgets, steering step widgets, and scenario lamp/button groups
  - avoid raw numeric text entry except hidden service/debug-only fields

## Single-Source Command Policy

- one operator mode owns one command domain
- `Vehicle`
  - vehicle/body/manual driving commands only
- `Context`
  - warning/context/V2X/environment injection plus alert-volume request only
- `Scenario`
  - validation harness lifecycle only
- `Scenario` must not own `roadZone`, `vehicleSpeed`, `emergencyType`, or other `Vehicle` / `Context` seams
- no two active operator pages or donor-compat panels should intentionally write the same command seam
- product readback seams must not be reused as new input seams in the redesign target

## Observer Demotion Gate

- `Navigation_Alert.xvp` is an observer-target panel in the redesign direction, but the current frozen donor XVP still contains a writable `Test::alertVolumeSetting` trackbar
- migrate that write path into the local `Input Console` or an explicit owner command seam before declaring `Navigation_Alert.xvp` fully observer-only

## Desktop_ASSIGN

Grouped desktop copies live under [Desktop_ASSIGN](./Desktop_ASSIGN/README.md).

- `Desktop_ASSIGN/*/*.xvp` must stay byte-equal to the root file with the same runtime name.
- Desktop grouping is for GUI composition only.
- Pairing rules and current GUI-saved grouping are documented again in `Desktop_ASSIGN/README.md`.
- Current `Desktop_ASSIGN` file placement reflects the latest GUI save. If GUI composition changes again, update the folder copies and both README tables together.
- Diagnostic observer layout now targets `Desktop_ASSIGN/Diag/Diagnostic_Console.xvp`; `3D/Diagnostic_Console.xvp` may remain temporarily for legacy GUI path compatibility until the next GUI save.

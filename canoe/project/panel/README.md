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
- `Diagnostic_Console.xvp` is the only local project-specific panel outside the donor set.
- Detailed frozen contract matrix: `../../AGENT/canoe/docs/operations/panel/DONOR_PANEL_CONTRACT_MATRIX_2026-03-21.md`

## Current Root Inventory

- `Ambient_Control.xvp`
- `Ambient_TopView.xvp`
- `Body_Status.xvp`
- `Cabin_Cockpit.xvp`
- `Cluster_Alert.xvp`
- `Cruise_Pedal.xvp`
- `Diagnostic_Console.xvp`
- `Driver_Control.xvp`
- `Navigation_Alert.xvp`
- `Operator_Input.xvp`
- `Scenario_Control.xvp`
- `V2X_Ingress.xvp`
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
| `Navigation_Alert.xvp` | `Navigation.xvp` |
| `Operator_Input.xvp` | `input.xvp` |
| `Scenario_Control.xvp` | `scenariocontrol.xvp` |
| `V2X_Ingress.xvp` | `v2xpanel.xvp` |
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
| Diagnostic monitor | none | `Diagnostic_Console.xvp` | `3D/Diagnostic_Console.xvp` | `Diag::*`, domain health mirrors |

## Runtime Meaning

| Root file | Primary role |
| --- | --- |
| `Ambient_Control.xvp` | operator ambient input |
| `Ambient_TopView.xvp` | 3D ambient/effect visualization |
| `Body_Status.xvp` | body/window/light status view |
| `Cabin_Cockpit.xvp` | cabin/cockpit visualization |
| `Cluster_Alert.xvp` | cluster-side warning presentation |
| `Cruise_Pedal.xvp` | cruise and pedal input |
| `Diagnostic_Console.xvp` | diagnostic observer console |
| `Driver_Control.xvp` | driver/body/chassis manual control |
| `Navigation_Alert.xvp` | navigation/warning presentation and audio control |
| `Operator_Input.xvp` | operator scenario/vehicle manual input |
| `Scenario_Control.xvp` | scenario launch/result control |
| `V2X_Ingress.xvp` | V2X ingress scene/status view |
| `Vehicle_Dashboard.xvp` | vehicle dashboard state view |

## Desktop_ASSIGN

Grouped desktop copies live under [Desktop_ASSIGN](./Desktop_ASSIGN/README.md).

- `Desktop_ASSIGN/*/*.xvp` must stay byte-equal to the root file with the same runtime name.
- Desktop grouping is for GUI composition only.
- Pairing rules and current GUI-saved grouping are documented again in `Desktop_ASSIGN/README.md`.
- Current `Desktop_ASSIGN` file placement reflects the latest GUI save. If GUI composition changes again, update the folder copies and both README tables together.

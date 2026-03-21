# project/panel

Current root panel set for `develop`.

## Source Policy

- Root `canoe/project/panel/*.xvp` is the panel source of truth.
- Imported donor panels are frozen at donor design/binding level.
- Do not change donor panel layout, widget type, label, or existing writable binding.
- Runtime adaptation must be done in:
  - `canoe/project/sysvars/project.sysvars`
  - `canoe/src/capl`
  - `canoe/cfg/channel_assign`
- `Diagnostic_Console.xvp` is the only local project-specific panel outside the donor set.

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

| Pair set | Input / control panel | Output / display panel | Main runtime seam |
| --- | --- | --- | --- |
| Ambient | `Ambient_Control.xvp` | `Ambient_TopView.xvp` | `Body::*`, `Infotainment::*`, `UiRender::*` |
| Driver / cabin | `Driver_Control.xvp` | `Cabin_Cockpit.xvp`, `Body_Status.xvp` | `Body::*`, `Chassis::*`, `Display::*` |
| Cruise / vehicle | `Cruise_Pedal.xvp` | `Vehicle_Dashboard.xvp` | `Chassis::*`, `Powertrain::*` |
| Alert / operator | `Operator_Input.xvp` | `Cluster_Alert.xvp`, `Navigation_Alert.xvp` | `Core::*`, `CoreState::*`, `UiRender::*` |
| Scenario / V2X | `Scenario_Control.xvp` | `V2X_Ingress.xvp`, `Cluster_Alert.xvp`, `Navigation_Alert.xvp` | `Test::*`, `V2X::*`, `Core::*` |
| Diagnostic monitor | none | `Diagnostic_Console.xvp` | `Diag::*`, domain health mirrors |

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

Grouped desktop copies live under [Desktop_ASSIGN](C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Desktop_ASSIGN).

- `Desktop_ASSIGN/*/*.xvp` must stay byte-equal to the root file with the same runtime name.
- Desktop grouping is for GUI composition only.
- Pairing rules are documented again in `Desktop_ASSIGN/README.md`.

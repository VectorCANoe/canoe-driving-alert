# project/panel

Normalized CANoe panel source set for root `develop`.

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

## Naming Rule

- Root filename format: `SemanticCategory_ActualName.xvp`
- Use ASCII only.
- Keep names short and reviewer-readable.
- Do not use donor/internal placeholders such as `sample`, `My`, `inner`, or generic `panel`.
- Desktop grouping belongs to the folder path, not the root filename.

## Migration Map

| Donor file | Current root file | Why |
| --- | --- | --- |
| `Ambient_Control.xvp` | `Ambient_Control.xvp` | already clear |
| `Ambient_Top_View.xvp` | `Ambient_TopView.xvp` | normalized token split |
| `car_inner.xvp` | `Cabin_Cockpit.xvp` | donor/internal name removed |
| `cluster.xvp` | `Cluster_Alert.xvp` | alert role made explicit |
| `input.xvp` | `Operator_Input.xvp` | operator role made explicit |
| `native diagnostic observer` | `Diagnostic_Console.xvp` | dedicated external diagnostic monitor panel |
| `MyDriverPanel.xvp` | `Driver_Control.xvp` | donor/personal naming removed |
| `Navigation.xvp` | `Navigation_Alert.xvp` | alert role made explicit |
| `sample_Control.xvp` | `Cruise_Pedal.xvp` | sample naming removed, actual function retained |
| `sample_Dashboard.xvp` | `Vehicle_Dashboard.xvp` | sample naming removed, dashboard meaning retained |
| `scenariocontrol.xvp` | `Scenario_Control.xvp` | normalized casing and separator |
| `v2xpanel.xvp` | `V2X_Ingress.xvp` | actual role retained, generic panel name removed |
| `windowstate.xvp` | `Body_Status.xvp` | vague internal wording removed |

## Panel Meaning

| Root file | Internal `ControlName` | Dominant contract |
| --- | --- | --- |
| `Ambient_Control.xvp` | `AmbientControl` | `Body::ambientMode` |
| `Ambient_TopView.xvp` | `AmbientTopView` | `Infotainment::emergencySound` |
| `Body_Status.xvp` | `BodyStatus` | `Body::windowPos`, `Body::wiperPos`, `Body::blinkLeft/Right`, `Chassis::brakeLamp` |
| `Cabin_Cockpit.xvp` | `CabinCockpit` | `Display::steeringFrame`, `Display::animFrame`, `Chassis::*`, `Powertrain::*` |
| `Cluster_Alert.xvp` | `ClusterAlert` | `Core::*`, `Cluster::*`, `UiRender::*`, `V2X::*` |
| `Cruise_Pedal.xvp` | `CruisePedal` | `Powertrain::cruiseState`, `Powertrain::cruiseSetSpeed`, `Chassis::throttlePosition`, `Chassis::brakePressure` |
| `Diagnostic_Console.xvp` | `DiagnosticConsole` | `Diag::*` observer seam for request, response, security, and domain health |
| `Driver_Control.xvp` | `DriverControl` | door, window, wiper, turn, ignition, belt, steering, emergency vehicle position |
| `Navigation_Alert.xvp` | `NavigationAlert` | volume, road-flow, zone, beep, and alert presentation |
| `Operator_Input.xvp` | `OperatorInput` | manual operator/test inputs and compat controls |
| `Scenario_Control.xvp` | `ScenarioControl` | `Test::scenarioCommand`, result, and demo flow |
| `V2X_Ingress.xvp` | `V2XIngress` | `V2X::v2xFrame` |
| `Vehicle_Dashboard.xvp` | `VehicleDashboard` | speed, rpm, coolant, fuel, ABS, blinkers, and animation |

## Desktop_ASSIGN

Grouped GUI copies live under [Desktop_ASSIGN](C:/Users/이준영/CANoe-IVI-OTA/canoe/project/panel/Desktop_ASSIGN).

## Donor Bundle Basis

- `sh_rael_merge` kept one integrated warning stack:
  - `SDV_Ambient_Control.xvp`
  - `SDV_Ambient_Top_View.xvp`
  - `input.xvp`
  - `Navigation.xvp`
  - `cluster.xvp`
- `merge/lee` split into three practical families:
  - control family: `MyDriverPanel.xvp`, `sample_Control.xvp`
  - cockpit family: `car_inner.xvp`, `sample_Dashboard.xvp`
  - scene family: `scenariocontrol.xvp`, `v2xpanel.xvp`, `windowstate.xvp`
- Current `Desktop_ASSIGN` keeps those original affinities, but normalizes them into `Module / Cabin / 3D`.

### Module

- `Ambient_Control.xvp`
- `Cluster_Alert.xvp`
- `Cruise_Pedal.xvp`
- `Diagnostic_Console.xvp`
- `Driver_Control.xvp`
- `Navigation_Alert.xvp`
- `Operator_Input.xvp`

### Cabin

- `Cabin_Cockpit.xvp`
- `Vehicle_Dashboard.xvp`

### 3D

- `Ambient_TopView.xvp`
- `Body_Status.xvp`
- `Scenario_Control.xvp`
- `V2X_Ingress.xvp`

## Mirror Rule

- `Desktop_ASSIGN/*/*.xvp` must be exact copies of the root files.
- The filename in `Desktop_ASSIGN` must match the root filename exactly.
- Each desktop folder carries its own `Bitmaps/` copy so the panels open correctly from that folder alone.

## Rename Gate Status

- `CAN_v2_topology.cfg` currently has no panel file references, so root panel rename was safe.
- If panels are re-registered in GUI later, use the normalized filenames above.

## Contract Status

- Root panel source scan target remains `missing sysvar 0`
- Root panel source scan target remains `missing asset 0`
- Root panel source scan target remains `direct DBC binding 0`
- Root panel source scan target remains `external path 0`

# Desktop_ASSIGN

Exact panel copies for CANoe GUI desktop assignment.

## Purpose

- Keep root `panel/*.xvp` as the source-of-truth set.
- Provide grouped copies for CANoe desktop composition only.
- Keep filenames and contents identical to the root source panels.

## Desktop Groups

Current file placement below reflects the latest GUI save only. It is not the target active-command composition after the local `Input Console` cutover.

### Module

- `Ambient_Control.xvp`
- `Ambient_TopView.xvp`
- `Cluster_Alert.xvp`
- `Cruise_Pedal.xvp`
- `Driver_Control.xvp`
- `Input_Console.xvp`
- `Navigation_Alert.xvp`
- `Operator_Input.xvp`

### Cabin

- `Cabin_Cockpit.xvp`
- `Cruise_Pedal.xvp`
- `Vehicle_Dashboard.xvp`

### 3D

- `Ambient_TopView.xvp`
- `Body_Status.xvp`
- `Driver_Control.xvp`
- `Scenario_Control.xvp`
- `V2X_Cross.xvp`
- `V2X_Ingress.xvp`

### Diag

- `Diagnostic_Console.xvp`

## Pairing Matrix

| Pair set | Input / control side | Output / display side | GUI status / cutover rule |
| --- | --- | --- | --- |
| Ambient | `Module/Ambient_Control.xvp` | `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | legacy donor input desktop; retire from active GUI when the local `Input Console` `Vehicle` page owns ambient/body commands |
| Driver / body | `Module/Driver_Control.xvp`, `3D/Driver_Control.xvp` | `3D/Body_Status.xvp` | legacy donor input desktop; keep `Body_Status` visible, but retire donor driver controls at local `Vehicle` cutover |
| Driver / cabin | `Module/Driver_Control.xvp`, `3D/Driver_Control.xvp` | `Cabin/Cabin_Cockpit.xvp` | legacy donor input desktop; keep cabin observer view, but retire donor driver controls at local `Vehicle` cutover |
| Cruise / vehicle | `Module/Cruise_Pedal.xvp`, `Cabin/Cruise_Pedal.xvp` | `Cabin/Vehicle_Dashboard.xvp` | legacy donor input desktop; keep dashboard observer view, but retire donor cruise/pedal input at local `Vehicle` cutover |
| Manual warning | `Module/Operator_Input.xvp` | `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | legacy donor input desktop; keep warning outputs visible, but retire `Operator_Input` at local `Context` cutover |
| Local input console | `Module/Input_Console.xvp` | domain observer panels stay on their current desktops | preferred local active command source once runtime cutover reaches `Cmd::*`, `Inject::*`, and lifecycle-only `Test::*` |
| Scenario warning | `3D/Scenario_Control.xvp` | `3D/V2X_Ingress.xvp`, `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | keep only if `Scenario_Control` is reduced to `Test::*` lifecycle / lock / evidence control; if it still writes vehicle/context seams, retire it |
| Cross scene | `3D/Scenario_Control.xvp` or future local scenario input | `3D/V2X_Cross.xvp` | keep crossing observer visible with a lifecycle-only scenario trigger source; do not use mixed vehicle/context input here |
| Diagnostic | none | `Diag/Diagnostic_Console.xvp` | observer-only |

## Layout Intent

- `Module` hosts operator input and main warning modules.
- `Cabin` hosts driver-facing in-cabin status views.
- `3D` hosts top-view, external scene, and scenario/V2X scene panels.
- `Diag` hosts the diagnostic observer desktop.
- Some panel sets are intentionally paired across folders for observer visibility; they are not alternate command owners.
- Legacy donor input copies are transitional compatibility surfaces, not permanent co-open command sources.
- Once the local `Input Console` is introduced, do not leave donor input copies open beside it in GUI.
- `Navigation_Alert.xvp` stays display-first, but its frozen donor XVP still contains a writable `Test::alertVolumeSetting` trackbar; treat it as observer-audit-hold until that control migrates into the local console.

## Cutover Retirement Set

- retire from active GUI when the local `Input Console` `Vehicle` page becomes the command owner:
  - `Module/Ambient_Control.xvp`
  - `Module/Cruise_Pedal.xvp`
  - `Cabin/Cruise_Pedal.xvp`
  - `Module/Driver_Control.xvp`
  - `3D/Driver_Control.xvp`
- retire from active GUI when the local `Input Console` `Context` page becomes the command owner:
  - `Module/Operator_Input.xvp`
- keep conditionally:
  - `3D/Scenario_Control.xvp` may remain only as the `Test::*` scenario desktop until the local `Scenario` page takes over; if it still writes `Vehicle` or `Context` seams, retire it with the donor inputs

## Future Input Desktop Direction

- current `Desktop_ASSIGN` still reflects donor operator-panel placement
- the long-term cleanup target is simpler:
  - output/readback desktops stay paired to display panels
  - one local `Input Console` owns command entry by domain and switches pages inside one XVP like `Diag/Diagnostic_Console.xvp`
- preferred page split:
  - `Vehicle`
  - `Context`
  - `Scenario`
- ownership boundary for those pages:
  - `Vehicle` owns manual/body/ambient `Cmd::*`
  - `Context` owns warning/environment `Inject::*` plus alert-volume request
  - `Scenario` owns `Test::*` start / stop / ack / status only
- `Scenario` must not publish `roadZone`, `vehicleSpeed`, `emergencyType`, or other `Vehicle` / `Context` seams
- use three separate local panels only as fallback if GUI stability blocks the single-console flow
- the runtime rule stays the same:
  - one active input domain owns one command family
  - display desktops do not become alternate command sources
- widget rule for the future local console:
  - prefer switches, momentary buttons, rocker controls, pedal sliders/click widgets, steering step widgets, and scenario lamp/button groups
  - avoid raw numeric text entry except hidden service/debug-only fields

## Rules

- `Desktop_ASSIGN/*/*.xvp` is a copy, not an alias.
- The filename inside each desktop folder must match the root filename exactly.
- If a root panel changes, the corresponding desktop copy must be refreshed immediately.
- `Module/Bitmaps/`, `Cabin/Bitmaps/`, and `3D/Bitmaps/` are full copies of the root `Bitmaps/` folder.
- `Diag/Diagnostic_Console.xvp` is the preferred diagnostic desktop copy.
- `3D/Diagnostic_Console.xvp` may remain temporarily as a legacy path shim until the next GUI save repoints the desktop to `Diag/Diagnostic_Console.xvp`.
- Do not reinterpret donor panel semantics inside `Desktop_ASSIGN`; only place exact copies into the intended composition group.
- Actual CANoe desktop layout is GUI-managed. This README records the current GUI-saved placement and must be updated when the GUI layout changes again.

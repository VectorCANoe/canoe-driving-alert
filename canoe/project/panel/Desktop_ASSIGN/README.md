# Desktop_ASSIGN

Exact panel copies for CANoe GUI desktop assignment.

## Purpose

- Keep root `panel/*.xvp` as the source-of-truth set.
- Provide grouped copies for CANoe desktop composition only.
- Keep filenames and contents identical to the root source panels.

## Structure

- `Module/`
- `Cabin/`
- `3D/`

## Desktop Composition

### Module

- `Ambient_Control.xvp`
- `Cluster_Alert.xvp`
- `Cruise_Pedal.xvp`
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

## Why These Bundles

- `Module` holds the warning/control stack that `sh_rael_merge` originally worked as one set:
  - ambient selection
  - operator input
  - cluster warning
  - navigation warning
  - driver and cruise controls
- `Cabin` stays focused on the cockpit-sized driver view:
  - the large cabin/cockpit panel
  - the dashboard panel
- `3D` holds top-view and external-scene behavior:
  - ambient top view
  - body/window/light status
  - scenario execution
  - V2X scene ingress

## Rules

- `Desktop_ASSIGN/*/*.xvp` is a copy, not an alias.
- The filename inside each desktop folder must match the root filename exactly.
- If a root panel changes, the corresponding desktop copy must be refreshed.
- `Module/Bitmaps/`, `Cabin/Bitmaps/`, and `3D/Bitmaps/` are full copies of the root `Bitmaps/` folder.
- `ALL_VIEW` remains deferred until a dedicated composite panel is designed.

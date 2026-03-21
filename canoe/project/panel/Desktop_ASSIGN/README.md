# Desktop_ASSIGN

Exact panel copies for CANoe GUI desktop assignment.

## Purpose

- Keep root `panel/*.xvp` as the source-of-truth set.
- Provide grouped copies for CANoe desktop composition only.
- Keep filenames and contents identical to the root source panels.

## Desktop Groups

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

## Pairing Matrix

| Pair set | Input / control side | Output / display side | Recommended Desktop_ASSIGN opening set |
| --- | --- | --- | --- |
| Ambient | `Module/Ambient_Control.xvp` | `3D/Ambient_TopView.xvp` | open together |
| Driver / cabin | `Module/Driver_Control.xvp` | `Cabin/Cabin_Cockpit.xvp`, `3D/Body_Status.xvp` | open together |
| Cruise / vehicle | `Module/Cruise_Pedal.xvp` | `Cabin/Vehicle_Dashboard.xvp` | open together |
| Alert / operator | `Module/Operator_Input.xvp` | `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp` | open together |
| Scenario / V2X | `3D/Scenario_Control.xvp` | `3D/V2X_Ingress.xvp`, `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp` | open together |
| Diagnostic | none | `Module/Diagnostic_Console.xvp` | observer-only |

## Layout Intent

- `Module` hosts operator input and main warning modules.
- `Cabin` hosts driver-facing in-cabin status views.
- `3D` hosts top-view, external scene, and scenario/V2X scene panels.
- Some panel sets are intentionally paired across folders; they are not alternatives.

## Rules

- `Desktop_ASSIGN/*/*.xvp` is a copy, not an alias.
- The filename inside each desktop folder must match the root filename exactly.
- If a root panel changes, the corresponding desktop copy must be refreshed immediately.
- `Module/Bitmaps/`, `Cabin/Bitmaps/`, and `3D/Bitmaps/` are full copies of the root `Bitmaps/` folder.
- Do not reinterpret donor panel semantics inside `Desktop_ASSIGN`; only place exact copies into the intended composition group.

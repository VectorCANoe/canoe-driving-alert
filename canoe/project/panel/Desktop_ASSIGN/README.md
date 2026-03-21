# Desktop_ASSIGN

Exact panel copies for CANoe GUI desktop assignment.

## Purpose

- Keep root `panel/*.xvp` as the source-of-truth set.
- Provide grouped copies for CANoe desktop composition only.
- Keep filenames and contents identical to the root source panels.

## Desktop Groups

Current file placement below reflects the latest GUI save.

### Module

- `Ambient_Control.xvp`
- `Ambient_TopView.xvp`
- `Cluster_Alert.xvp`
- `Cruise_Pedal.xvp`
- `Driver_Control.xvp`
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

| Pair set | Input / control side | Output / display side | Current Desktop_ASSIGN opening set |
| --- | --- | --- | --- |
| Ambient | `Module/Ambient_Control.xvp` | `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | keep control and at least one ambient view open together |
| Driver / body | `Module/Driver_Control.xvp`, `3D/Driver_Control.xvp` | `3D/Body_Status.xvp` | keep body status paired with driver control |
| Driver / cabin | `Module/Driver_Control.xvp`, `3D/Driver_Control.xvp` | `Cabin/Cabin_Cockpit.xvp` | keep cabin view paired with driver control |
| Cruise / vehicle | `Module/Cruise_Pedal.xvp`, `Cabin/Cruise_Pedal.xvp` | `Cabin/Vehicle_Dashboard.xvp` | keep dashboard view paired with cruise/pedal input |
| Manual warning | `Module/Operator_Input.xvp` | `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | keep warning outputs visible with operator input |
| Scenario warning | `3D/Scenario_Control.xvp` | `3D/V2X_Ingress.xvp`, `Module/Cluster_Alert.xvp`, `Module/Navigation_Alert.xvp`, `Module/Ambient_TopView.xvp`, `3D/Ambient_TopView.xvp` | keep ingress and warning outputs visible with scenario control |
| Cross scene | `3D/Scenario_Control.xvp` or future local scenario input | `3D/V2X_Cross.xvp` | keep crossing observer visible with scenario trigger source |
| Diagnostic | none | `Diag/Diagnostic_Console.xvp` | observer-only |

## Layout Intent

- `Module` hosts operator input and main warning modules.
- `Cabin` hosts driver-facing in-cabin status views.
- `3D` hosts top-view, external scene, and scenario/V2X scene panels.
- `Diag` hosts the diagnostic observer desktop.
- Some panel sets are intentionally paired across folders; they are not alternatives.
- If one side of a pair is assigned in GUI, the matching display/control side must also be assigned in the same working desktop.

## Future Input Desktop Direction

- current `Desktop_ASSIGN` still reflects donor operator-panel placement
- the long-term cleanup target is simpler:
  - output/readback desktops stay paired to display panels
  - new local input desktop(s) own command entry by domain
- preferred domain split:
  - `Vehicle Control`
  - `Context Injection`
  - `Scenario`
- whether those domains are opened as three desktops or one tabbed local input console is a GUI decision
- the runtime rule stays the same:
  - one active input domain owns one command family
  - display desktops do not become alternate command sources

## Rules

- `Desktop_ASSIGN/*/*.xvp` is a copy, not an alias.
- The filename inside each desktop folder must match the root filename exactly.
- If a root panel changes, the corresponding desktop copy must be refreshed immediately.
- `Module/Bitmaps/`, `Cabin/Bitmaps/`, and `3D/Bitmaps/` are full copies of the root `Bitmaps/` folder.
- `Diag/Diagnostic_Console.xvp` is the preferred diagnostic desktop copy.
- `3D/Diagnostic_Console.xvp` may remain temporarily as a legacy path shim until the next GUI save repoints the desktop to `Diag/Diagnostic_Console.xvp`.
- Do not reinterpret donor panel semantics inside `Desktop_ASSIGN`; only place exact copies into the intended composition group.
- Actual CANoe desktop layout is GUI-managed. This README records the current GUI-saved placement and must be updated when the GUI layout changes again.

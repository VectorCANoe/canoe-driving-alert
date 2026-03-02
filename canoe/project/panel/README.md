# project/panel

CANoe panel artifacts for this project.

## Files
- `SDV_Control.xvp`: scenario/input control panel
- `SDV_Monitor.xvp`: pipeline/output monitor panel
- `SDV_Render_Debug.xvp`: UiRender adapter debug panel
- `SDV_Demo_Stage.xvp`: demo-stage visualization panel (road + moving vehicle object)
- `SDV_Cluster_View.xvp`: cluster-focused visualization panel (warning/direction/pattern)

## Panel Split
- Validation panels: `SDV_Control.xvp`, `SDV_Monitor.xvp`, `SDV_Render_Debug.xvp`
- Visualization panels: `SDV_Demo_Stage.xvp`, `SDV_Cluster_View.xvp`

## BP (Renderer Only)
- XVP panels are display/input surfaces only.
- Warning/arbitration logic stays in CAPL nodes (`WARN_ARB_MGR`, `BODY_GW`, `IVI_GW`).
- For high-fidelity rendering, bind XVP controls to `UiRender::*` system variables.

## Render Variables
Use these derived sysvars for animation-ready visualization:
- `UiRender::renderMode`
- `UiRender::renderColor`
- `UiRender::renderPattern`
- `UiRender::renderTextCode`
- `UiRender::renderDirection`
- `UiRender::roadZoneColorCode`
- `UiRender::roadFlowDirection`
- `UiRender::vehicleObjectPos`
- `UiRender::emsBlinkPhase`
- `UiRender::ambientPulsePhase`
- `UiRender::icFlowPhase`
- `UiRender::activeAlertType`

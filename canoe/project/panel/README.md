# project/panel

CANoe panel artifacts for this project.

## Files
- `SDV_Control.xvp`: scenario/input control panel
- `SDV_Monitor.xvp`: pipeline/output monitor panel

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
- `UiRender::emsBlinkPhase`
- `UiRender::ambientPulsePhase`
- `UiRender::icFlowPhase`
- `UiRender::activeAlertType`

# project/panel

CANoe panel artifacts for this project.

## Files
- `SDV_Control.xvp`: scenario/input control panel
- `SDV_Monitor.xvp`: pipeline/output monitor panel
- `SDV_Render_Debug.xvp`: UiRender adapter debug panel
- `SDV_Cluster_View.xvp`: cluster-focused visualization panel (warning/direction/zone)
- `SDV_Ambient_View.xvp`: ambient-focused visualization panel (mode/color/pattern/pulse)
- `SDV_Navigation_View.xvp`: navigation-focused visualization panel (zone/flow/vehicle movement)
- `SDV_Demo_Stage.xvp`: legacy combined demo panel (kept for backward comparison)

## Skin Assets
- `Bitmaps/DashboardCombi.png`
- `Bitmaps/DashboardCircleBlack.png`
- `Bitmaps/warnLevelFront.png`
- `Bitmaps/warnLevelRear.png`
- `Bitmaps/alert3.bmp`
- `Bitmaps/StageDashboard.png`
- `Bitmaps/VehicleStrip11.png`
- `Bitmaps/ZoneBadge4.png`
- `Bitmaps/FlowBadge3.png`
- `Bitmaps/VehicleClassStrip8.png`
- `Bitmaps/AmbientColorRail8.png`
- `Bitmaps/AmbientPatternRail8.png`
- `Bitmaps/AmbientPulseGlow4.png`
- Source reference:
- `reference/samples/vector_samples_19_4_10/ADAS/ADASSystem/Panels/Bitmaps`
- `reference/samples/vector_samples_19_4_10/SOA/SOASystem/Panels/BMP`
- `reference/samples/vector_samples_19_4_10/CAN/CANBasic/Panels/Bitmaps`

## Panel Split
- Validation panels: `SDV_Control.xvp`, `SDV_Monitor.xvp`, `SDV_Render_Debug.xvp`
- Visualization panels (recommended):
- `SDV_Cluster_View.xvp`
- `SDV_Ambient_View.xvp`
- `SDV_Navigation_View.xvp`

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

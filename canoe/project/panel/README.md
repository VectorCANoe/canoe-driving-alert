# project/panel

CANoe panel artifacts for this project.

## Files
- `SDV_Control.xvp`: scenario/input control panel
- `SDV_Monitor.xvp`: pipeline/output monitor panel
- `SDV_Render_Debug.xvp`: UiRender adapter debug panel
- `SDV_External_Road_View.xvp`: external environment macro view
- `SDV_Cabin_Panorama_View.xvp`: in-cabin panoramic macro view
- `SDV_Cluster_View.xvp`: cluster detail view
- `SDV_Ambient_View.xvp`: ambient detail view
- `SDV_Navigation_View.xvp`: navigation detail view
- `SDV_Demo_Stage.xvp`: legacy combined panel (retirement target)

## Skin Assets (Project)
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
- `Bitmaps/ExternalRoadScene.png`
- `Bitmaps/CabinPanoramaScene.png`
- `Bitmaps/reference_pack_v1/*`: curated Vector sample pack for external/cabin upgrade

## Reference Source Matrix (Adopted)
- External vehicle/light base: `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels`
- External top-view/road line icons: `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel`
- V2X traffic icon set: `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels`
- Cabin panorama/window animation strips: `reference/vector_samples_19_4_10/LIN/LINSystem/Panels`
- Additional control idioms: `reference/vector_code_sample`

## Panel Split (Target)
- Validation panels: `SDV_Control.xvp`, `SDV_Monitor.xvp`, `SDV_Render_Debug.xvp`
- Macro panels: `SDV_External_Road_View.xvp`, `SDV_Cabin_Panorama_View.xvp`
- Detail panels (v2 skin aligned): `SDV_Cluster_View.xvp`, `SDV_Ambient_View.xvp`, `SDV_Navigation_View.xvp`
- Legacy panel: `SDV_Demo_Stage.xvp` (freeze new features)

## BP (Renderer-Only Contract)
- Decision/arbitration logic stays in `ADAS` and `ADAS`
- `IVI` and XVP panels are display-only
- No priority/timeout logic in renderer layer
- Renderer binds derived outputs only (`UiRender::*`)
- Do not bind raw inputs (`vehicleSpeed`, `eta`) directly to skin controls
- Add/modify `UiRender_*` only with SSoT update in `0304`

## GUI-Only Scope
- `.xvp` layout/property/binding changes must be done in CANoe GUI Panel Editor
- `.cfg`, `.cfg.ini`, `.stcfg` save/generation must be done in CANoe GUI
- Agent may edit text docs, CAPL logic, and bitmap assets only

## Compat Guardrail
- Donor panel compat outputs such as `V2X::v2xFrame`, `Infotainment::emergencySound`, and `UiRender::beep*` are display-only
- Keep those compat sysvars read-only and producer-owned
- Manual exploration inputs stay under `Test::*` or approved operator input namespaces

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

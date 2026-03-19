# project/panel

CANoe panel artifacts for this project.

## Donor Intake Status

### Active donor set
- `SDV_Ambient_Control.xvp`: adopted from `sh_rael_merge`
- `input.xvp`: adopted from `sh_rael_merge`
- `cluster.xvp`: adopted from `sh_rael_merge`
- `Navigation.xvp`: adopted from `sh_rael_merge`
- `SDV_Ambient_Top_View.xvp`: adopted from `sh_rael_merge`
- `v2xpanel.xvp`: adopted from `merge/lee`
- `scenariocontrol.xvp`: adopted from `merge/lee`

### Deferred donor set
- `sample_Dashboard.xvp`: source-staged only, raw CAN and `Display::animFrame` cleanup still needed
- `windowstate.xvp`: source-staged only, direct body CAN bindings still need operator-safe review

### No-go donor files
- `MyDriverPanel.xvp`: do not adopt into the `develop` panel set
- `sample_Control.xvp`: do not adopt into the `develop` panel set

### Retirement targets
- `SDV_Control.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Monitor.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Render_Debug.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_External_Road_View.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Cabin_Panorama_View.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Cluster_View.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Ambient_View.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Navigation_View.xvp`: current `develop` draft panel, delete only after GUI replacement proof
- `SDV_Demo_Stage.xvp`: current `develop` draft panel, delete only after GUI replacement proof

## Skin Assets (Project)
- `Bitmaps/DashboardCombi.png`
- `Bitmaps/DashboardCircleBlack.png`
- `Bitmaps/DashboardABS.png`
- `Bitmaps/DashboardFlasherLeft.png`
- `Bitmaps/DashboardFlasherRight.png`
- `Bitmaps/warnLevelFront.png`
- `Bitmaps/warnLevelRear.png`
- `Bitmaps/alert3.bmp`
- `Bitmaps/brakelamp.png`
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
- `Bitmaps/ivi.png`
- `Bitmaps/left flash.png`
- `Bitmaps/right flash.png`
- `Bitmaps/left window.png`
- `Bitmaps/wifer.png`
- `Bitmaps/KakaoTalk_20260310_003301280_10 (1).bmp`
- `Bitmaps/KakaoTalk_20260310_003458323.bmp`
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
- Donor panel compat outputs such as `V2X::v2xFrame`, `Infotainment::emergencySound`, and `UiRender::beep*` are display-only at the panel layer
- Producer-owned compat sysvars may remain writable for CAPL publishers, but panel widgets must keep read-only bindings
- Manual exploration inputs stay under `Test::*` or approved operator input namespaces
- Panels still carrying direct `SymbolConfiguration` CAN bindings are source-only until they are reviewed against the `develop` owner model

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

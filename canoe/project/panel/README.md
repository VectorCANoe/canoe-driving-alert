# project/panel

CANoe panel artifacts for this project.

## Donor Intake Status

### GUI-activated donor set
- `SDV_Ambient_Control.xvp`: adopted from `sh_rael_merge`
- `input.xvp`: adopted from `sh_rael_merge`
- `cluster.xvp`: adopted from `sh_rael_merge`
- `Navigation.xvp`: adopted from `sh_rael_merge`
- `SDV_Ambient_Top_View.xvp`: adopted from `sh_rael_merge`
- `v2xpanel.xvp`: adopted from `merge/lee`
- `scenariocontrol.xvp`: adopted from `merge/lee`

### Source-staged donor set
- `SDV_Control.xvp`: restored from `sh_rael_merge`
- `sample_Dashboard.xvp`: source-staged only, raw CAN and `Display::animFrame` cleanup still needed
- `sample_Control.xvp`: source-staged only, local bitmap path normalized, raw CAN review still needed
- `MyDriverPanel.xvp`: source-staged only, donor-only utility panel
- `windowstate.xvp`: source-staged only, direct body CAN bindings still need operator-safe review

### Draft-panel note
- Unchanged `develop` draft XVP carry-overs were removed again after donor union intake
- Only donor-modified `SDV_*` panels remain in this branch

## Skin Assets (Project)
- `Bitmaps/DashboardCombi.png`
- `Bitmaps/DashboardCircleBlack.png`
- `Bitmaps/DashboardABS.png`
- `Bitmaps/DashboardFlasherLeft.png`
- `Bitmaps/DashboardFlasherRight.png`
- `Bitmaps/CruiseControlIndicator.bmp`
- `Bitmaps/warnLevelFront.png`
- `Bitmaps/warnLevelRear.png`
- `Bitmaps/alert3.bmp`
- `Bitmaps/brakelamp.png`
- `Bitmaps/brake.bmp`
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
- `Bitmaps/pedal.bmp`
- `Bitmaps/wifer.png`
- `Bitmaps/ControlIgnition.png`
- `Bitmaps/KakaoTalk_20260310_003301280_10 (1).bmp`
- `Bitmaps/KakaoTalk_20260310_003458323.bmp`
- `Bitmaps/reference_pack_v1/*`: curated Vector sample pack for external/cabin upgrade

## Reference Source Matrix (Adopted)
- External vehicle/light base: `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels`
- External top-view/road line icons: `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel`
- V2X traffic icon set: `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels`
- Cabin panorama/window animation strips: `reference/vector_samples_19_4_10/LIN/LINSystem/Panels`
- Additional control idioms: `reference/vector_code_sample`

## Panel Split (Integration Branch)
- Donor union intake was pruned to exclude unchanged `develop` draft XVP carry-overs
- GUI-activated donor panels: `SDV_Ambient_Control.xvp`, `input.xvp`, `cluster.xvp`, `Navigation.xvp`, `SDV_Ambient_Top_View.xvp`, `v2xpanel.xvp`, `scenariocontrol.xvp`
- Source-staged donor panels still need GUI/operator review before activation: `SDV_Control.xvp`, `sample_Dashboard.xvp`, `sample_Control.xvp`, `MyDriverPanel.xvp`, `windowstate.xvp`

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

## GUI Cleanup Pending
- `CAN_v2_topology.cfg` must reflect the final donor registration set on the next CANoe GUI panel-registration save

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

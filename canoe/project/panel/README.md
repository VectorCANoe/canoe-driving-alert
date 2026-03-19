# project/panel

CANoe panel artifacts for this project.

## Files
- Legacy `develop` draft XVP panels were retired and removed.
- Active donor-panel integration work is maintained in the dedicated merge branch/worktree.
- `develop` no longer keeps placeholder panel drafts as an in-repo baseline.

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
- `develop` does not preserve draft-panel structure.
- Final active panel registration is resolved through the donor merge branch and GUI registration cleanup.

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

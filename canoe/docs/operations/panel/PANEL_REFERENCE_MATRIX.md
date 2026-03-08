# PANEL REFERENCE MATRIX (External View + Cabin View)

## Purpose
- Scope: build two macro views (`External`, `Cabin`) and retire `Demo Stage` from active development
- Constraint: XVP is renderer-only, decision/arbitration logic remains in CAPL nodes
- Constraint: `.xvp` editing is GUI-only in CANoe

## Scan Result Summary
- Scanned root: `canoe/reference`
- XVP sample count: 979
- Primary sample set: `vector_samples_19_4_10`
- Supplemental local set: `vector_code_sample`
- OSS set (`canoe/reference/oss`) is useful for code references, not primary XVP skin source

## Adopted High-Value References
- Cluster baseline:
- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Dashboard.xvp`
- `reference/vector_samples_19_4_10/ADAS/ADASSystemCarMaker/Panels/Dashboard.xvp`
- External vehicle/light idiom:
- `reference/vector_samples_19_4_10/Ethernet/EthernetSystem/Panel/ConceptCar.xvp`
- `reference/vector_samples_19_4_10/SIL/SilKitCAN/CANoe/Panels/Display.xvp`
- Cabin panorama/window animation idiom:
- `reference/vector_samples_19_4_10/LIN/LINSystem/Panels/VCarWinConsole.xvp`
- `reference/vector_samples_19_4_10/CAN/CANSystem/CANoe/Panels/Door.xvp`
- V2X signage/event icon idiom:
- `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Car2xSystem/Panels/HeadUnit.xvp`
- `reference/vector_samples_19_4_10/Car2x/Car2x_EU/Infrastructure/Testenvironments/Car2xSignalizedIntersectionTest/Panels/TrafficLights/TrafficLight.xvp`

## Curated Asset Pack (Prepared)
- Destination: `canoe/project/panel/Bitmaps/reference_pack_v1`
- Includes copied sample assets + generated macro skin strips (`EXT_*`, `CABIN_*`)
- External assets:
- `EXT_VCar_side.bmp`
- `EXT_VCar_topview.png`
- `EXT_HeadLight_Left.bmp`
- `EXT_HeadLight_Right.bmp`
- `EXT_PoliceLight_Left.bmp`
- `EXT_PoliceLight_Right.bmp`
- `EXT_Lane_horizontal.png`
- `EXT_Lane_left.png`
- `EXT_Lane_right.png`
- `EXT_TrafficLight_strip.png`
- Cabin assets:
- `CABIN_FrontWindow_scene.bmp`
- `CABIN_FrontWindow_overlay.bmp`
- `CABIN_Window_front_left_strip.bmp`
- `CABIN_Window_front_right_strip.bmp`
- `CABIN_Window_rear_left_strip.bmp`
- `CABIN_Window_rear_right_strip.bmp`
- Navigation arrows:
- `NAV_Arrow_left.bmp`
- `NAV_Arrow_right.bmp`

## GUI Build Plan (No cfg patch by agent)
- Step 1: keep `SDV_External_Road_View.xvp` as the primary external macro panel and remove overlap objects
- Step 2: split external panel layers into background road, ego vehicle, emergency vehicles, and traffic context
- Step 3: bind animation using `UiRender::vehicleObjectPos`, `UiRender::roadFlowDirection`, `UiRender::emsBlinkPhase`
- Step 4: keep `SDV_Cabin_Panorama_View.xvp` as the primary cabin macro panel and split front/rear/left/right ambient zones
- Step 5: bind ambient pulse and direction using `UiRender::ambientPulsePhase` and `UiRender::renderDirection`
- Step 6: freeze `SDV_Demo_Stage.xvp` for legacy comparison only

## BP Compliance Checkpoints
- Keep decision/arbitration in `ADAS` and `ADAS`
- Use derived output variables (`UiRender::*`) only in renderer
- On any `UiRender_*` addition, update traceability chain in `0304 -> 04 -> 05/06/07`
- Keep Python simulator as input injector only (no arbitration logic)

## Demo Stage Retirement Rule
- Keep file for visual regression comparison
- Freeze feature additions on `SDV_Demo_Stage.xvp`
- Redirect all new visual work to `SDV_External_Road_View.xvp` and `SDV_Cabin_Panorama_View.xvp`

## Next GUI Execution Order
- 1. Finish layer cleanup on `SDV_External_Road_View.xvp`
- 2. Finish layer cleanup on `SDV_Cabin_Panorama_View.xvp`
- 3. Keep `SDV_Cluster_View.xvp`, `SDV_Ambient_View.xvp`, `SDV_Navigation_View.xvp` as detail views
- 4. Apply v2 detail skin assets on Cluster/Ambient/Navigation
- 5. Run measurement and capture evidence on FZ_005/FZ_006/FZ_007 criteria

## Execution Documents
- GUI execution checklist: `canoe/docs/operations/panel/PANEL_SPLIT_EXECUTION_GUIDE.md`
- Binding audit report: `canoe/docs/operations/panel/PANEL_BINDING_AUDIT.md`
- Binding audit script: `canoe/scripts/audit_panel_bindings.py`


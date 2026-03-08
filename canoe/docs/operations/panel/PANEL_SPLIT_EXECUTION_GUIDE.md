# PANEL SPLIT EXECUTION GUIDE

## Goal
- Promote two macro panels:
- `SDV_External_Road_View.xvp` as the external environment view
- `SDV_Cabin_Panorama_View.xvp` as the full cabin panorama view
- Retire `SDV_Demo_Stage.xvp` from active feature development

## Non-Negotiable Boundaries
- Decision and arbitration remain in CAPL (`WARN_ARB_MGR`, `ADAS_WARN_CTRL`)
- XVP renderer uses derived outputs only (`UiRender::*`)
- Do not add priority/timeout logic in panels
- Perform panel edits in CANoe GUI only
- Do not patch `.cfg`, `.cfg.ini`, `.stcfg` by script for normal development

## Inputs (Prepared)
- Binding audit: `canoe/docs/operations/panel/PANEL_BINDING_AUDIT.md`
- Reference matrix: `canoe/docs/operations/panel/PANEL_REFERENCE_MATRIX.md`
- Curated assets: `canoe/project/panel/Bitmaps/reference_pack_v1`

## Baseline Backup (GUI)
- Save As current config to a new timestamped name before editing panels
- Keep previous known-good cfg in `canoe/cfg/v1_cfg/`

## Panel Actions (GUI)

### A) External Macro Panel
- File: `SDV_External_Road_View.xvp`
- Keep objects:
- `SwZoneBadge` (`UiRender::roadZoneColorCode`)
- `SwFlowBadge` (`UiRender::roadFlowDirection`)
- `SwVehicleStrip` (`UiRender::vehicleObjectPos`)
- `SwVehicleClassSkin` (`UiRender::activeAlertType`)
- `SwEmsBlink` (`UiRender::emsBlinkPhase`)
- `TxtVehiclePos` (`UiRender::vehicleObjectPos`) optional debug
- `TxtDirection` (`UiRender::renderDirection`) optional debug
- Remove objects (cross-domain overlap):
- `SwRoadPattern` (`UiRender::renderPattern`)
- `SwRoadColor` (`UiRender::renderColor`)
- `TxtTextCode` (`UiRender::renderTextCode`)
- Background and icon replacement plan:
- Keep panel background as external road scene
- Replace/augment car and lane visuals using `reference_pack_v1` (`EXT_*`)

### B) Cabin Macro Panel
- File: `SDV_Cabin_Panorama_View.xvp`
- Keep objects:
- `SwAmbientPulseDash` (`UiRender::ambientPulsePhase`)
- `SwAmbientPatternTop`, `SwAmbientPatternRear` (`UiRender::renderPattern`)
- `SwAmbientColorTop`, `SwAmbientColorRear` (`UiRender::renderColor`)
- `SwVehicleClassSkin` (`UiRender::activeAlertType`)
- `SwEmsBlink` (`UiRender::emsBlinkPhase`)
- `TxtMode` (`UiRender::renderMode`) optional debug
- `TxtDirection` (`UiRender::renderDirection`) optional debug
- Remove objects (cluster overlap):
- `TxtTextCode` (`UiRender::renderTextCode`)
- Background and icon replacement plan:
- Keep cabin panorama base
- Layer window/interior strips from `reference_pack_v1` (`CABIN_*`)

### C) Detail Panels (Keep as Specialized)
- `SDV_Navigation_View.xvp`: keep navigation-only vars
- `SDV_Ambient_View.xvp`: keep ambient-only vars
- `SDV_Cluster_View.xvp`: keep cluster warning vars
- Recommended cluster cleanup (optional):
- remove `renderMode` and `renderPattern` debug controls from cluster if visual clutter exists

### D) Demo Stage Retirement
- File: `SDV_Demo_Stage.xvp`
- Keep file for regression comparison only
- Do not add new controls/bindings
- Remove from default workspace layout after split panels are validated

## Quick Validation Procedure (GUI)
- Open all macro/detail panels after save
- Confirm no visual overlap across macro panels
- Confirm expected vars in each panel using bindings property view
- Run measurement and execute at least:
- Emergency blink case (red/blue or red/white alternation)
- School zone/highway context switch case
- Timeout clear case (1000 ms)

## PASS Criteria
- External panel does not render ambient bars or text code
- Cabin panel does not render navigation strip or text code
- Demo Stage not used for new feature verification
- Existing detail panels remain functional and readable
- CAPL compile is clean

## Post-Edit Audit (CLI)
- Run:
- `python canoe/scripts/audit_panel_bindings.py`
- Check generated file:
- `canoe/docs/operations/panel/PANEL_BINDING_AUDIT.md`
- Expected warnings to resolve:
- `SDV_External_Road_View.xvp` should have no `renderColor`, `renderPattern`, `renderTextCode`
- `SDV_Cabin_Panorama_View.xvp` should have no `renderTextCode`

## Note on Encoding
- Keep code/script content in English ASCII where possible
- Use UTF-8 for all text files

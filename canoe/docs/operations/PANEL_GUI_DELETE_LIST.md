# PANEL GUI DELETE LIST

Use this file during CANoe Panel Editor work.

## Target
- Remove cross-domain duplicate controls from macro panels only.
- Keep detail panels unchanged.

## External Macro Panel
- File: `canoe/project/panel/SDV_External_Road_View.xvp`
- Delete these controls:
- `SwRoadPattern` (binds `UiRender::renderPattern`)
- `SwRoadColor` (binds `UiRender::renderColor`)
- `TxtTextCode` (binds `UiRender::renderTextCode`)

## Cabin Macro Panel
- File: `canoe/project/panel/SDV_Cabin_Panorama_View.xvp`
- Delete these controls:
- `TxtTextCode` (binds `UiRender::renderTextCode`)

## Demo Stage Panel
- File: `canoe/project/panel/SDV_Demo_Stage.xvp`
- Rule: no new controls, no new bindings
- Keep only for visual regression comparison

## Keep As-Is
- `SDV_Cluster_View.xvp`
- `SDV_Ambient_View.xvp`
- `SDV_Navigation_View.xvp`

## Save Sequence (GUI)
- Save panel edits
- Save configuration as a new timestamped cfg
- Compile CAPL
- Run measurement

## After GUI Edit (CLI)
- Run `python canoe/scripts/audit_panel_bindings.py`
- Run `python canoe/scripts/check_panel_split_status.py`

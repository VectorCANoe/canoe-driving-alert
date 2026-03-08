# canoe/scripts

## Purpose
This folder is not the main operator entry surface.
It contains CANoe-side helper scripts for panel, Unity bridge, simulator, and maintenance support.

## Use This Folder Only For
- Unity renderer bridge support
- navigation simulator support
- panel binding/split audits
- advanced sync/verification helpers around CANoe-side assets

## Do Not Use As Daily Team Entry
Daily operator entry remains:
- `python scripts/run.py`

Primary daily actions remain:
1. `gate all`
2. `scenario run`
3. `verify quick`

## Current Classification
### Unity / renderer support
- `unity_renderer_bridge.py`
- `unity_renderer_mock_sender.py`
- `unity_standard_pipeline.py`
- `sync_unity_integration.py`
- `verify_unity_integration_sync.py`
- `build_unity_skin_pack.py`
- `generate_macro_skin_assets.py`

### Panel / CANoe-side audits
- `audit_panel_bindings.py`
- `check_panel_split_status.py`

### Simulator support
- `navigation_simulator.py`

### Experimental / recovery-style scripts
- `fix_cfg_paths.py`
- `fix_new_cfg.py`

Rule:
- `fix_cfg_paths.py` and `fix_new_cfg.py` directly touch cfg-like concerns.
- They are not part of the normal stable operator path.
- Prefer GUI-first config operations according to repo policy.

## Maintenance Rule
If a script here becomes part of normal day-to-day flow, promote it through:
1. `scripts/cliops/*`
2. `scripts/run.py`
3. `scripts/README.md`

If it cannot satisfy that bar, keep it here as a helper only.

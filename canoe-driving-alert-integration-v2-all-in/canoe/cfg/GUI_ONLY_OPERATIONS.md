# CANoe GUI-Only Operations

This project has recurring configuration corruption when `.cfg` state is edited outside CANoe GUI.
Follow this file as a strict operational boundary.

## 1) GUI-First (Do in CANoe GUI by default)
- Open / Save / Save As of configuration (`*.cfg`)
- Auto-generated side files (`*.cfg.ini`, `*.stcfg`) lifecycle
- System Variables editor changes and config-side registration
- CANoeIL / network channel / bus resource mapping changes
- Measurement setup state and environment persistence

## 2) Agent-Allowed (Text/File Safe Zone)
- CAPL source (`canoe/src/capl/**/*.can`)
- `project.sysvars` source template (`canoe/project/sysvars/project.sysvars`)
- Panel source (`canoe/project/panel/*.xvp`) when explicitly requested
- Panel image assets (`canoe/project/panel/Bitmaps/*`)
- Documentation (`driving-situation-alert/*.md`, `canoe/project/panel/README.md`)
- Scripts and test artifacts under `canoe/scripts`, `canoe/docs` (text-based only)

## 3) Forbidden Direct Edit (Unless Emergency Recovery Explicitly Requested)
- `canoe/cfg/*.cfg`
- `canoe/cfg/*.cfg.ini`
- `canoe/cfg/*.stcfg`

## 4) Recommended Recovery Flow for Config Errors
1. Stop measurement.
2. Close CANoe fully.
3. Reopen the target `.cfg` from GUI.
4. Apply pending System Variables / Panel bindings in GUI.
5. Save As to a new filename if existing file is unstable.
6. Compile CAPL and run measurement.
7. Only after GUI success, reflect doc/source updates in Git.

## 5) Version Control Guidance
- Commit `*.cfg` only when it is known-good from GUI save.
- Do not commit transient `*.stcfg` unless explicitly required by process.
- Archive obsolete configs under `canoe/cfg/legacy/` with timestamped names.

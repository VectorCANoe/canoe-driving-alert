# Development Entrypoints

Use this file when the repository feels too large.

## 1. Working Set Only
Ignore the full tree first. Start from these areas only:

- `driving-situation-alert/`
- `canoe/`
- `scripts/`

Everything else is reference, legacy, or support material unless explicitly needed.

## 2. First Files to Open

Read in this order:

1. `AGENTS.md`
2. `driving-situation-alert/TMP_HANDOFF.md`
3. `canoe/FILE_INDEX.md`
4. `scripts/README.md`
5. `canoe/docs/operations/DEV_DOC_ENTRYPOINT.md`

## 3. Daily Developer Surface

### Documents
- `driving-situation-alert/TMP_HANDOFF.md`
- `driving-situation-alert/01_Requirements.md`
- `driving-situation-alert/03_Function_definition.md`
- `driving-situation-alert/0301_SysFuncAnalysis.md`
- `driving-situation-alert/0302_NWflowDef.md`
- `driving-situation-alert/0303_Communication_Specification.md`
- `driving-situation-alert/0304_System_Variables.md`
- `driving-situation-alert/04_SW_Implementation.md`
- `driving-situation-alert/05_Unit_Test.md`
- `driving-situation-alert/06_Integration_Test.md`
- `driving-situation-alert/07_System_Test.md`

### CANoe assets
- `canoe/cfg/CAN_v2_topology_wip.cfg`
- `canoe/project/sysvars/project.sysvars`
- `canoe/databases/*.dbc`
- `canoe/cfg/channel_assign/`
- `canoe/src/capl/`

### Automation surface
- `python scripts/run.py`
- `python scripts/run.py gate all`
- `python scripts/run.py scenario run --id <n>`
- `python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>`
- `python scripts/run.py doctor`

## 4. Default Ignore Set

Do not browse these by default:

- `driving-situation-alert/tmp/reference-*`
- `driving-situation-alert/tmp/archive/`
- `reference/`
- `legacy_projects/`
- `canoe/tmp/reports/verification/` as source code
- `dist/`, `build/`, `__pycache__/`

Open them only when the current task explicitly needs them.

## 5. Complexity Rule

If a team member needs more than these five answers, the public surface is too wide:

1. What are we building now?
2. Which docs are canonical?
3. Which cfg/dbc/sysvar/capl files are active?
4. What command do I run?
5. Where do verification outputs go?

This file exists to keep those five answers short.

# AGENTS.md

## Session Start Priority
At the start of every Codex session, read this file first, then read:
- `driving-situation-alert/TMP_HANDOFF.md`

Use `driving-situation-alert/TMP_HANDOFF.md` as the current project intent/source of truth for:
- what the team is building now
- fixed scope and exclusions
- immediate next steps
- non-negotiable traceability rules

## Handoff Freshness Gate
- Before treating `driving-situation-alert/TMP_HANDOFF.md` as SoT, check section `0) Freshness Control`.
- If handoff status is `FRESH`, follow handoff-first execution.
- If handoff status is `STALE` (or stale criteria are met), use canonical docs as temporary SoT in this order:
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
  - `driving-situation-alert/tmp/mentoring/Mentoring_MET40.md`
- After stale causes are cleared, update `TMP_HANDOFF.md` and switch back to handoff-first execution.

## Reference Standards (When Ambiguous)
If any requirement, format, or wording is unclear, consult:
- `reference/standards/ASPICE*`
- `reference/standards/ISO26262*`
- `reference/standards/Project Result_Sample*`

Use those references to align:
- document structure and table format
- requirement quality (clarity, completeness, verifiability, traceability)
- V-model mapping and evidence chain consistency

## Working Rules for This Repository
- Keep 01 (Requirements) as `What`, keep 03+ as `How`.
- Maintain 1:1 traceability chain:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- Do not remove existing template columns in requirement/function tables.
- Keep all text files in UTF-8 (do not re-save with legacy code pages).
- Verification scope is fixed to CANoe SIL, CAN + Ethernet only.

## CANoe GUI-First Operations
- For CANoe configuration and runtime state stability, keep these as **GUI-first**:
  - Open/Save/Save As for `canoe/cfg/*.cfg`
  - Any generation/update of `*.cfg.ini`, `*.stcfg`
  - IL/Network setup changes (channel mapping, IL Tx/Rx registration, bus/hardware assignment)
- Agent must **not** directly patch `*.cfg`, `*.cfg.ini`, `*.stcfg` via shell/script unless explicitly requested for recovery.
- Panel and sysvar source edits can be done directly by agent when explicitly requested:
  - `canoe/project/panel/*.xvp`
  - `canoe/project/sysvars/project.sysvars`
- If config integrity issue occurs, recover by GUI reload/save path first, then document deltas in text docs (`0304`, panel README, etc.).
- Detailed operational checklist: `canoe/cfg/GUI_ONLY_OPERATIONS.md`

## Notes
- `driving-situation-alert/TMP_HANDOFF.md` is temporary and can be replaced as project state changes.
- If this file and `driving-situation-alert/TMP_HANDOFF.md` conflict:
  - when handoff is `FRESH`, follow handoff first
  - when handoff is `STALE`, follow canonical docs first, then refresh handoff

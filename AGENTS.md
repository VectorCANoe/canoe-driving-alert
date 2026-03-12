# AGENTS.md

## Session Start Priority
At the start of every Codex session, read this file first, then read:
- `driving-situation-alert/TMP_HANDOFF.md`
- `driving-situation-alert/tmp/submission/README.md`

Use `driving-situation-alert/TMP_HANDOFF.md` as the current project intent/execution guardrail source of truth for:
- what the team is building now
- fixed scope and exclusions
- immediate next steps
- non-negotiable traceability rules
Use `driving-situation-alert/tmp/submission/final-docs/` as the operational document SoT for ongoing edits.
Treat root docs under `driving-situation-alert/` as canonical sync targets to be updated later.

## Handoff Freshness Gate
- Before treating `driving-situation-alert/TMP_HANDOFF.md` as intent SoT, check section `0) Freshness Control`.
- If handoff status is `FRESH`, follow handoff-first execution and `final-docs`-first document edits.
- If handoff status is `STALE` (or stale criteria are met), use canonical docs as temporary intent reference in this order:
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
- Keep ongoing edits in `final-docs` unless a task explicitly requests root SoT sync-back.
- After stale causes are cleared, update `TMP_HANDOFF.md` and switch back to `FRESH`.

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
- Do not change the column/header structure of any top-level `공식 표준 양식` table unless the user explicitly requests a template change.
- When more detail is needed, keep the official table format and enrich the cell content instead of adding/replacing columns ad hoc.
- Keep top-level `공식 표준 양식` text concise and reviewer-facing; do not list runtime/module implementation details there unless the template explicitly requires them.
- For reviewer-facing official tables, follow the sample/BP tone: short plain sentences, actual ECU/service wording first, and prefer expressions like "A 정보를 수신하여 B에 반영/전달" over internal state or variable names.
- In top-level `공식 표준 양식`, do not rely on `Flow/Comm` IDs, the word `체인`, or cross-document references to explain behavior; the table itself must be understandable on its own.
- Broad ID ranges are not a reason to over-merge reviewer-facing rows; split rows when OEM-facing meaning, actors, or verification intent are materially different.
- In `05/06/07` official test tables, interim status values such as `Ready` and `Planned` may be used only as temporary implementation progress markers before executable test assets are fixed.
- All `Ready`/`Planned` items are expected to be implemented, and once corresponding TEST assets are available they must be diagnosed with evidence and replaced by `PASS`/`FAIL`.
- Keep all text files in UTF-8 (do not re-save with legacy code pages).
- Verification scope is fixed to CANoe SIL, CAN + Ethernet only.
- Before `pull/rebase`, inspect remote changed paths first (`fetch -> log/diff`).
- If remote changes mix `canoe/` and `driving-situation-alert/`, do not blindly full-pull on behalf of the docs instance.
- In mixed-change recovery, sync `canoe/` selectively first and preserve `driving-situation-alert/` until docs ownership changes are reviewed or explicitly approved.

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

## CAPL / Ethernet Guardrails
- When replacing CAN-stub backbone paths with Ethernet, separate `business semantics` from `transport` first.
  - Do not bind owner logic directly to stub DBC message types if the final target is real Ethernet transport.
- In CAPL include files (`*.cin`) that are pulled in via `includes {}`, avoid top-level `const` and preprocessor directives for transport constants.
  - Prefer helper functions or normal variables inside valid CAPL sections.
- Avoid C-only idioms that often break CAPL parsing during refactors.
  - Example: do not use `(void)x;` suppression statements.
- For CANoe UDP work, do not start from host adapter probing or loopback assumptions.
  - Prefer CANoe sample patterns first: open with wildcard/configured stack address, then validate broadcast or multicast behavior against the configured Ethernet stack.
- Do not assume a local host UDP pattern is equivalent to CANoe internal Ethernet behavior.
  - If runtime delivery is unclear, verify with CANoe trace/write-window evidence before expanding the refactor.
- Before broad transport migration, create one narrow producer/consumer sanity path or explicit CAPL test hook and verify that path first.
- Whenever `src/capl` is the SoT and `cfg/channel_assign` is the active mirror, update both together and compile immediately after sync.
- Treat `compile success` and `runtime success` as separate gates.
  - If MCP cannot observe Ethernet trace or write-window evidence, report runtime verification as pending instead of assuming transport is correct.

## Notes
- `driving-situation-alert/TMP_HANDOFF.md` is temporary and can be replaced as project state changes.
- If this file and `driving-situation-alert/TMP_HANDOFF.md` conflict:
  - when handoff is `FRESH`, follow handoff for intent and `final-docs` for working docs
  - when handoff is `STALE`, follow canonical docs for intent, keep `final-docs` as working baseline, then refresh handoff

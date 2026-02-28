# AGENTS.md

## Session Start Priority
At the start of every Codex session, read this file first, then read:
- `driving-situation-alert/TMP_HANDOFF.md`

Use `driving-situation-alert/TMP_HANDOFF.md` as the current project intent/source of truth for:
- what the team is building now
- fixed scope and exclusions
- immediate next steps
- non-negotiable traceability rules

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

## Notes
- `driving-situation-alert/TMP_HANDOFF.md` is temporary and can be replaced as project state changes.
- If this file and `driving-situation-alert/TMP_HANDOFF.md` conflict, follow the handoff first for current execution, then update this file if needed.

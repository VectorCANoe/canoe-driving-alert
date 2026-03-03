# V2 Branch Guardrail

## Purpose
Keep one stable integration baseline for v2 (`integration/v2-all-in`) and stop recurring merge conflicts caused by mixed sync methods.

## Why conflicts keep happening
1. Two branches edit the same docs in parallel (`integration/v2-all-in` and `v2-post-mid-report`).
2. Mixed sync methods are used together (folder overwrite + cherry-pick + manual conflict edits).
3. Force-push after manual conflict resolution rewrites branch history and invalidates teammate merge base.

## Fixed policy (mandatory)
1. `integration/v2-all-in` is the only integration baseline for v2.
2. `v2-post-mid-report` is docs source only (never merge it as full branch).
3. Sync docs by explicit file list only.
4. Do not cherry-pick doc commits into `integration/v2-all-in`.
5. Do not force-push `integration/v2-all-in` except emergency recovery approved by team lead.

## Daily start rule (mandatory)
1. Start work only after updating local branch from `origin/integration/v2-all-in`.
2. Team members must read and edit the same baseline commit before any document/code change.
3. If local branch is behind, stop editing and run fast-forward pull first.

```powershell
git switch integration/v2-all-in
git fetch origin --prune
git pull --ff-only origin integration/v2-all-in
```

## Allowed sync method (single method)
Use file-level checkout from source branch:

```powershell
git fetch origin --prune
git switch integration/v2-all-in
git pull --ff-only origin integration/v2-all-in
git checkout origin/v2-post-mid-report -- `
  canoe/docs/operations/ETH_INTERFACE_CONTRACT.md `
  driving-situation-alert/0301_SysFuncAnalysis.md `
  driving-situation-alert/04_SW_Implementation.md
git commit -m "docs(v2): sync selected files from v2-post-mid-report"
git push origin integration/v2-all-in
```

## Pre-merge gates (always)
```powershell
python scripts/quality/cfg_hygiene_gate.py
python scripts/quality/doc_code_sync_gate.py
```

## Runtime/SIL pass criteria
1. Input cycle: `100ms`
2. Output cycle: `50ms`
3. End-to-end reaction: `<= 150ms`
4. Timeout clear: `1000ms`

## Evidence links
1. Unit test: `driving-situation-alert/05_Unit_Test.md`
2. Integration test: `driving-situation-alert/06_Integration_Test.md`
3. System test: `driving-situation-alert/07_System_Test.md`

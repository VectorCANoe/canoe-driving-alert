# Contributing

This repository is operated as a CANoe SIL development project with strict document-to-code traceability.

## 1) Mandatory Read Order

Before any change, read in this order:

1. `AGENTS.md`
2. `driving-situation-alert/TMP_HANDOFF.md`

Apply the handoff freshness rule:

- `FRESH`: follow handoff-first.
- `STALE`: use canonical docs (`01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07`) until handoff is refreshed.

## 2) Scope and Traceability

- `01` documents requirements (**What**).
- `03+` documents design/implementation mapping (**How**).
- Always preserve:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`

Do not remove template columns from requirement/function tables.

## 3) CAPL / DBC / CFG Rules

### CAPL mirror sync (required)

The following trees must remain synchronized:

- `canoe/src/capl/**`
- `canoe/cfg/channel_assign/**`

Run:

```bash
python scripts/run.py gate capl-sync
```

### GUI-first for CANoe config

Treat these as GUI-managed:

- `canoe/cfg/*.cfg`
- `canoe/cfg/*.cfg.ini`
- `canoe/cfg/*.stcfg`

Do not patch these files directly by script unless explicitly asked for recovery work.

### DBC ownership and ID policy

- follow `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md`
- keep active split DBC set consistent with runtime profile

## 4) Required Local Gates

Run before commit (at minimum):

```bash
python scripts/run.py gate cfg-hygiene
python scripts/run.py gate capl-sync
```

Also run when relevant:

```bash
python scripts/run.py gate doc-sync         # docs/trace/code chain changes
python scripts/run.py gate cli-readiness    # CLI/scripts packaging changes
```

Gate reference: `scripts/GATE_MATRIX.md`

## 5) CI and Ownership

Gate workflows are in `.github/workflows/`:

- `cfg-hygiene-gate.yml`
- `doc-code-sync-gate.yml`
- `cli-readiness-gate.yml`

Gate policy/code ownership is defined in `.github/CODEOWNERS`.
Current gate owner:

- `@junexi0828` for `scripts/gates/*` and `*gate*.yml`.

## 6) Commit and PR Policy

- Prefer small, scoped commits.
- Keep generated temporary reports out of commits unless intentionally required as evidence.
- Use clear commit messages (Conventional Commits style is recommended):
  - `feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `chore: ...`

For PRs:

- explain scope and impacted trace chain (`Req/Func/Flow/Comm/Var/Code/Test` as applicable),
- include gate results or links to CI run,
- call out any GUI-only operations performed in CANoe.

## 7) Language Policy

- `driving-situation-alert/` (formal project docs): Korean-centered.
- code/CI/automation (`scripts/`, `.github/`, technical ops docs): English-centered.
- Keep one language per file; avoid mixed-language paragraphs.

## 8) Encoding and Safety

- Keep text files UTF-8.
- Do not use destructive git actions (`reset --hard`, forced file rollback of unrelated changes) unless explicitly approved.


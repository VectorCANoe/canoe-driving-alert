# Contributing to canoe-driving-alert

This repository contains three different working surfaces:

1. `canoe/` for the CANoe runtime project
2. `product/sdv_operator/` for the Dev2 operator surface
3. `driving-alert-workproducts/` for the canonical lifecycle documents and submission set

Contributions should keep those boundaries explicit instead of mixing them.

## Read First

Before changing code or docs, open:

1. `AGENTS.md`
2. `driving-alert-workproducts/ops/handoff/TMP_HANDOFF.md`
3. `docs/DEVELOPMENT_ENTRYPOINTS.md`

## Basic Workflow

1. Confirm the current scope and exclusions from `TMP_HANDOFF.md`
2. Update the correct ownership area:
   - runtime behavior: `canoe/`
   - operator surface: `scripts/` and `product/sdv_operator/`
   - canonical docs: `driving-alert-workproducts/`
3. Run the relevant local checks
4. Update traceability or evidence docs when the change affects the chain

## GUI-First Rule

Do not script direct edits to these files unless the task explicitly calls for recovery work:

- `canoe/cfg/*.cfg`
- `canoe/cfg/*.cfg.ini`
- `canoe/cfg/*.stcfg`

Use the CANoe GUI for configuration save/load, channel mapping, IL/network setup, and related stability-sensitive operations.

## Local Checks

Common checks:

- `python scripts/run.py gate all`
- `python scripts/run.py doctor`
- `python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>`

When the task is narrower, run only the relevant gate or scenario flow.

## Traceability Rule

Preserve the active chain:

`Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`

Keep `01` as `What` and `03+` as `How`.

## Pull Request / Merge Expectation

- Keep changes scoped to one ownership area whenever possible
- Do not mix runtime fixes, packaging changes, and large doc rewrites in one review unless they are tightly coupled
- Update only the docs that the change actually impacts
- Leave generated outputs and temporary evidence out of commits unless they are explicitly treated as source

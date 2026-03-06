# Gate Matrix

This document is the single quick reference for gate ownership, scope, and trigger policy.

## 1) Structure Decision

Current policy:

- Keep gate implementations in `scripts/gates/`.
- Keep CI wiring in `.github/workflows/`.
- Keep one command entrypoint in `scripts/run.py`.

Reason:

- avoids breaking existing CI/script references
- gives a single, explicit gate folder
- minimizes migration risk during active GUI/CAPL work

Legacy references were updated to the new path in runbook docs and CI workflows.

## 2) Gate Inventory

| Gate | Local Command | Main Script | Primary Scope |
|---|---|---|---|
| CFG Hygiene | `python scripts/run.py gate cfg-hygiene` | `scripts/gates/cfg_hygiene_gate.py` | CANoe text hygiene (absolute path, mojibake) |
| CAPL Sync | `python scripts/run.py gate capl-sync` | `scripts/gates/check_capl_sync.py` | `src/capl` and `cfg/channel_assign` 1:1 sync |
| Doc-Code Sync | `python scripts/run.py gate doc-sync` | `scripts/gates/doc_code_sync_gate.py` | `01/03/0301/0302/0303/0304/05/06/07` traceability + runtime linkage checks |
| CLI Readiness | `python scripts/run.py gate cli-readiness` | `scripts/gates/cli_readiness_gate.py` | CLI contract, entrypoint, command help/contract stability |

## 3) CI Mapping

| Workflow | Runs Which Gate | Trigger |
|---|---|---|
| `.github/workflows/cfg-hygiene-gate.yml` | `cfg-hygiene`, `capl-sync` | `push`, `pull_request` (selected paths), `workflow_dispatch` |
| `.github/workflows/doc-code-sync-gate.yml` | `doc-sync` | `push`, `pull_request` (doc/code selected paths), `schedule` (daily), `workflow_dispatch` |
| `.github/workflows/cli-readiness-gate.yml` | `cli-readiness` | `push`, `pull_request` (CLI-related paths), `workflow_dispatch` |

Notes:

- `cfg-hygiene` includes mojibake checks for `.can/.dbc/.sysvars` (strict fail class).
- `capl-sync` is a file-name + content-hash equality gate, not an encoding gate.

## 4) Operational Rule

Before commit/push in development:

1. `python scripts/run.py gate cfg-hygiene`
2. `python scripts/run.py gate capl-sync`
3. `python scripts/run.py gate doc-sync` (when doc/trace/code chain changed)

## 5) Folder Policy

Recommended now:

- Keep all gate files under `scripts/gates` only.
- Keep non-gate verification/evidence scripts under `scripts/quality`.
- Route local/CI calls through `python scripts/run.py gate ...`.

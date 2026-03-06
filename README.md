# canoe-driving-alert

CANoe SIL project for driving-situation warning logic with V-model traceability.

## Overview

This repository implements and verifies:

- navigation-context warning behavior (school zone, highway, guide lane),
- emergency-vehicle warning flow (police/ambulance),
- warning arbitration and fail-safe handling,
- synchronized outputs to ambient and cluster channels.

Verification scope is fixed to **CANoe SIL** with **CAN + Ethernet** transport.

## Repository Layout

```text
canoe-driving-alert/
├─ canoe/                      # CANoe runtime assets (cfg, CAPL, DBC, sysvars, ops docs)
│  ├─ cfg/
│  ├─ src/capl/
│  ├─ databases/
│  ├─ project/sysvars/
│  └─ docs/operations/
├─ driving-situation-alert/    # 00~07 V-model document chain (project SoT docs)
├─ scripts/                    # CLI entrypoint and automation
│  ├─ gates/                   # quality gates
│  ├─ quality/                 # verification/evidence tooling (non-gate)
│  ├─ canoe/
│  ├─ report/
│  └─ run.py
├─ .github/workflows/          # CI gates/workflows
└─ reference/                  # standards and reference materials
```

## Source of Truth

At session start and during implementation decisions:

1. `AGENTS.md`
2. `driving-situation-alert/TMP_HANDOFF.md` (respect `FRESH/STALE` rule in section `0) Freshness Control`)

When handoff is stale, fallback order is the canonical 01/03/030x/04/05/06/07 chain.

## Quick Start

### Prerequisites

- Windows + Vector CANoe SIL environment
- Python 3.11+
- Git

### Clone

```bash
git clone https://github.com/VectorCANoe/canoe-driving-alert.git
cd canoe-driving-alert
```

### Optional CLI install

```bash
python -m pip install -e .
```

After install, both forms are supported:

- `python scripts/run.py <command>`
- `sdv <command>`

### Common commands

```bash
python scripts/run.py gate cfg-hygiene
python scripts/run.py gate capl-sync
python scripts/run.py gate doc-sync
python scripts/run.py gate cli-readiness
```

Full gate matrix: `scripts/GATE_MATRIX.md`

## CI Gates

Current GitHub Actions gate workflows:

- `CFG Hygiene + CAPL Sync Gate`
- `Doc-Code Sync Gate`
- `CLI Readiness Gate`

Gate implementations are under `scripts/gates/`.

## Core Working Rules

- Keep `01` as **What**, keep `03+` as **How**.
- Preserve traceability chain:
  - `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
- Maintain CAPL mirror sync:
  - `canoe/src/capl/**` and `canoe/cfg/channel_assign/**` must remain 1:1.
- Keep text files UTF-8.
- Treat CANoe config as GUI-first:
  - do not script-patch `canoe/cfg/*.cfg`, `*.cfg.ini`, `*.stcfg` unless recovery is explicitly requested.

## Language Policy

- `driving-situation-alert/` (formal project document assets): Korean-centered.
- code/CI/automation docs (`scripts/`, `.github/`, most `canoe/docs/operations`): English-centered.
- Avoid mixed-language writing inside a single file.

## Contributing

Contribution rules and review flow:

- `CONTRIBUTING.md`
- gate/path policy owner: `.github/CODEOWNERS`


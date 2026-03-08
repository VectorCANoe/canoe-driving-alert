# canoe-driving-alert

CANoe SIL-based driving-situation warning project with a separate operator surface for verification execution, evidence collection, and packaging.

This repository is intentionally a collaboration workspace, not a single public product tree.
It contains three surfaces that are kept separate at the documentation level:

- CANoe runtime project
- canonical V-model document set
- SDV Operator verification surface

## Start Here

Use these entrypoints instead of scanning the whole tree:

1. [SDV Operator](product/sdv_operator/README.md)
2. [CANoe Runtime Guide](canoe/README.md)
3. [Canonical Docs Surface](driving-situation-alert/README.md)
4. [Contributing](CONTRIBUTING.md)

## Quick Start

### Operator / verification workflow

```powershell
python scripts/run.py
python scripts/run.py gate all
python scripts/run.py scenario run --id <n>
python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>
```

### CANoe runtime workflow

1. Open `canoe/cfg/CAN_v2_topology_wip.cfg` in CANoe
2. Confirm the active DBC set under `canoe/databases/`
3. Start measurement and execute the target scenario or test flow

## Repository Layers

- `product/sdv_operator/`
  - public-facing verification surface
  - TUI/CLI scope, packaging boundary, and docs source for generated HTML
- `canoe/`
  - CANoe runtime project
  - cfg, CAPL, DBC, sysvars, tests, and CANoe-side operation docs
- `driving-situation-alert/`
  - canonical lifecycle documents (`00~07`)
  - submission-editing workspace under `tmp/submission/`
- `docs/`
  - internal meeting, mentoring, and planning records
- `reference/`
  - standards and supporting external references

## Documentation Policy

- Markdown is the source of truth.
- HTML is a generated surface built from `product/sdv_operator/docs-src/`.
- Internal handoff, mentoring, tmp workspaces, and team boards are kept in the repository for traceability, but they are not the public first-read surface.

To build the operator docs locally:

```powershell
python -m pip install -e .[docs]
python -m mkdocs build -f product/sdv_operator/mkdocs.yml --strict
```

## Internal Working Docs

<details>
<summary>Open internal working entrypoints</summary>

Start here when you are working inside the repository:

1. `AGENTS.md`
2. `driving-situation-alert/TMP_HANDOFF.md`
3. `DEVELOPMENT_ENTRYPOINTS.md`
4. `canoe/FILE_INDEX.md`
5. `scripts/README.md`

Supporting internal paths:

- `driving-situation-alert/tmp/`
- `canoe/tmp/`
- `docs/README.md`
- `reference/`

</details>

## Contribution

For setup, workflow, and review rules, open [CONTRIBUTING.md](CONTRIBUTING.md).

# SDV Operator Product Boundary

This folder defines the product boundary for the Dev2 verification console.

It does **not** mean all source code has already moved here.
It means the team now treats one subset of the repository as a product with its own ownership and packaging target.

Machine-readable boundary:

- `product/sdv_operator/manifest.json`

Documentation source:

- `product/sdv_operator/docs-src/`
- `product/sdv_operator/mkdocs.yml`

Generated site output (do not treat as source):

- `product/sdv_operator/site/`

Build locally:

```powershell
python -m pip install -e .[docs]
python -m mkdocs build -f product/sdv_operator/mkdocs.yml --strict
```

## Product Definition

Product name:

- `SDV Operator`

Product role:

- CANoe verification automation launcher
- operator TUI / CLI surface
- evidence and gate execution frontend
- packaging target for portable ZIP / exe distribution

This product is **not**:

- the CANoe runtime project itself
- CAPL/DBC/sysvar ownership
- CANoe panel replacement
- generic repository script dumping ground

## Ownership Split

### Dev1 owns
- `canoe/`
  - cfg
  - panel
  - sysvars
  - DBC
  - CAPL
  - CANoe runtime behavior

### Dev2 owns
- verification automation product surface
- CLI/TUI launcher
- gate execution surface
- evidence/report execution surface
- portable packaging flow

## Current Product-Owned Files

### Public product surface
- `pyproject.toml`
- `sdv_cli.py`
- `scripts/run.py`
- `scripts/tui_app.py`
- `scripts/README.md`
- `scripts/COMMAND_REFERENCE.md`
- `scripts/MAINTENANCE_MAP.md`

### Product runtime layer
- `scripts/cliops/`
- `scripts/release/`

### Product backend engines
- `scripts/gates/`
- `scripts/quality/`

## Explicitly Not Product Surface

These may still support the repo, but they are not part of the daily SDV Operator product contract:

- `scripts/docs/`
- `scripts/report/`
- `scripts/canoe/`
- `canoe/scripts/`
- `canoe/tmp/`

These remain helper, advanced, generated, or legacy territory unless explicitly promoted later.

## Packaging Rule

When building a ZIP/exe, the packaging target is the `SDV Operator` product surface, not the entire repository.

Practical interpretation:

- entrypoint: `sdv`
- launcher source: `sdv_cli.py` + `scripts/run.py`
- UI: `scripts/tui_app.py`
- command/runtime logic: `scripts/cliops/*`
- packaging helpers: `scripts/release/*`
- required backend execution modules: `scripts/gates/*`, `scripts/quality/*`

## Migration Policy

Do **not** physically move the whole `scripts/` tree during active development just to make it look cleaner.

Do this instead:

1. Freeze the product boundary first
2. Keep compatibility paths stable
3. Promote only product-owned modules over time
4. Move helper/legacy tooling only when references are fully updated

This avoids breaking:

- CI workflows
- docs
- local operator habits
- packaging scripts

## End State

Long-term, the repository may physically separate:

- product surface
- internal helper scripts
- repo maintenance scripts

But that is a later migration.

For now, the correct model is:

- `canoe/` = runtime project
- `product/sdv_operator/` = product boundary and ownership reference
- `scripts/` = implementation location, with only part of it belonging to the SDV Operator product

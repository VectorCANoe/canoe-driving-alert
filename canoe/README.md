# CANoe Runtime Surface

This folder keeps the active CANoe runtime only.

## Start Here

1. `cfg/CAN_v2_topology_wip.cfg`
2. `FILE_INDEX.md`
3. `docs/README.md`

## Active Surface

- configuration
  - `cfg/CAN_v2_topology_wip.cfg`
- system variables
  - `project/sysvars/project.sysvars`
- runtime DBCs
  - `databases/chassis_can.dbc`
  - `databases/powertrain_can.dbc`
  - `databases/body_can.dbc`
  - `databases/infotainment_can.dbc`
  - `databases/adas_can.dbc`
- CAPL source of truth
  - `src/capl/`
- GUI import mirror
  - `cfg/channel_assign/`
- verification assets
  - `tests/`
- active operation docs
  - `docs/`
- active maintenance tools
  - `tools/`

## GUI-First Rule

Do not patch these directly unless recovery work is explicitly requested:

- `cfg/*.cfg`
- `cfg/*.cfg.ini`
- `cfg/*.stcfg`

## Local-Only Paths

These may exist on a developer machine but are not part of the active Git surface:

- `AGENT/`
- `logging/`
- `reference/`
- `scripts/`
- `tmp/`

Legacy runtime assets are preserved in archive branches and local `AGENT/legacy/`, not in the active root.

## Not Owned Here

- operator product
- canonical requirements/design document set
- archive/reference notes

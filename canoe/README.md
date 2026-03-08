# CANoe Runtime Surface

This folder contains the CANoe runtime project for the driving-situation warning baseline.

## What This Folder Owns

- active CANoe configuration
- CAPL runtime logic
- CAN DBC set
- system variables and panel assets
- native CANoe test assets
- CANoe-side operation docs

## Start Here

Open these first:

1. `cfg/CAN_v2_topology_wip.cfg`
2. `FILE_INDEX.md`
3. `docs/operations/README.md`

## Active Runtime Files

- configuration
  - `cfg/CAN_v2_topology_wip.cfg`
- system variables
  - `project/sysvars/project.sysvars`
- active DBC set
  - `databases/chassis_can.dbc`
  - `databases/powertrain_can.dbc`
  - `databases/body_can.dbc`
  - `databases/infotainment_can.dbc`
  - `databases/adas_can.dbc`
  - `databases/eth_backbone_can_stub.dbc`
- CAPL source
  - `cfg/channel_assign/`
  - `src/capl/`

## GUI-First Rule

Treat these as GUI-first:

- `cfg/*.cfg`
- `cfg/*.cfg.ini`
- `cfg/*.stcfg`

Do not patch them directly unless the task explicitly calls for recovery work.

## Folder Map

- `cfg/`
  - CANoe configuration and channel assignment
- `databases/`
  - runtime DBC files
- `project/`
  - sysvars and panel assets
- `src/`
  - CAPL source tree
- `tests/`
  - native CANoe test assets
- `docs/operations/`
  - CANoe-side working docs
- `tmp/`
  - generated verification outputs and temporary runtime-side artifacts

## What This Folder Is Not

- not the public operator product surface
- not the canonical requirements/design document set
- not the place for internal meeting records

For those surfaces, go to:

- `product/sdv_operator/README.md`
- `driving-situation-alert/README.md`
- `docs/README.md`

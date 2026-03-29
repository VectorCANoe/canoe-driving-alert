# CANoe Runtime Surface

This guide points to the active CANoe runtime project for the driving-alert CANoe SIL baseline.

## What This Folder Owns

- active CANoe configuration
- CAPL runtime logic
- CAN DBC set
- system variables and panel assets
- native CANoe test assets
- CANoe-side operation docs

## Start Here

Open these first:

1. `canoe/cfg/CAN_v2_topology.cfg`
2. `canoe/AGENT/canoe/docs/operations/README.md`
3. `canoe/docs/architecture/master_book/README.md`
4. `driving-alert-workproducts/README.md`

## Active Runtime Files

- configuration
  - `canoe/cfg/CAN_v2_topology.cfg`
- system variables
  - `canoe/project/sysvars/project.sysvars`
- active DBC set
  - `canoe/databases/chassis_can.dbc`
  - `canoe/databases/powertrain_can.dbc`
  - `canoe/databases/body_can.dbc`
  - `canoe/databases/infotainment_can.dbc`
  - `canoe/databases/adas_can.dbc`
- CAPL source
  - `canoe/cfg/channel_assign/`
  - `canoe/src/capl/`

## GUI-First Rule

Treat these as GUI-first:

- `cfg/*.cfg`
- `cfg/*.cfg.ini`
- `cfg/*.stcfg`

Do not patch them directly unless the task explicitly calls for recovery work.

## Folder Map

- `canoe/cfg/`
  - CANoe configuration and channel assignment
- `canoe/databases/`
  - runtime DBC files
- `canoe/project/`
  - sysvars and panel assets
- `canoe/src/`
  - CAPL source tree
- `canoe/tests/`
  - native CANoe test assets
- `canoe/docs/`
  - reviewer-facing runtime docs
- `canoe/AGENT/canoe/docs/`
  - internal CANoe-side working docs
- `canoe/tmp/`
  - generated verification outputs and temporary runtime-side artifacts

## What This Folder Is Not

- not the public operator product surface
- not the canonical requirements/design document set
- not the place for internal meeting records

For those surfaces, go to:

- `product/sdv_operator/README.md`
- `driving-alert-workproducts/README.md`
- `docs/README.md`

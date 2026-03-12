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
- active CAN DBC set
  - `databases/chassis_can.dbc`
  - `databases/powertrain_can.dbc`
  - `databases/body_can.dbc`
  - `databases/infotainment_can.dbc`
  - `databases/adas_can.dbc`
- active Ethernet contract
  - `docs/operations/ETH_INTERFACE_CONTRACT.md`
- transitional cfg attachment
  - `databases/eth_backbone_can_stub.dbc`
  - keep only while the active GUI configuration still references it
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
  - local generated outputs may appear here during gate or verification runs
  - this branch does not keep legacy snapshots or temp reports as tracked source

## What This Folder Is Not

- not the public operator product surface
- not the canonical requirements/design document set
- not the place for internal meeting records

For those surfaces, go to:

- `product/sdv_operator/README.md`
- `driving-situation-alert/README.md`
- `docs/README.md`

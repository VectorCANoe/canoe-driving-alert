# CAN DBC Usage Guide

## Active DBC Set (SoT)
- `chassis_can.dbc`
- `powertrain_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `adas_can.dbc`

These files are the canonical CAN runtime set for split-domain architecture.

Ethernet backbone SoT is the contract document:

- `../docs/operations/ETH_INTERFACE_CONTRACT.md`

Transitional GUI attachment only:

- `eth_backbone_can_stub.dbc`
  - keep only while the inherited `.cfg` still references it
  - do not treat it as the primary active backbone contract

`test_can.dbc` is kept as a deprecated placeholder only.

## Legacy Backup DBC

Legacy DBC backups are preserved in archive branches.
Do not recreate a local `legacy/` runtime tree on the active branch.

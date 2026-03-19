# CAN DBC Usage Guide

## Active DBC Set (SoT)
- `chassis_can.dbc`
- `powertrain_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `adas_can.dbc`
- `eth_backbone_can_stub.dbc`

These files are the canonical runtime set for split-domain architecture.

`test_can.dbc` is kept as a deprecated placeholder only.

## Legacy Backup DBC
- `legacy/LEGACY_emergency_system.dbc`

This file is backup compatibility artifact only.
Do not use it as default runtime DBC for new development.

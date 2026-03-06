# CAN DBC Usage Guide

## Active DBC Set (SoT)
- `chassis_can.dbc`
- `powertrain_can.dbc`
- `body_can.dbc`
- `infotainment_can.dbc`
- `test_can.dbc`

These files are the canonical runtime set for split-domain architecture.

## Legacy Backup DBC
- `legacy/LEGACY_emergency_system.dbc`

This file is backup compatibility artifact only.
Do not use it as default runtime DBC for new development.

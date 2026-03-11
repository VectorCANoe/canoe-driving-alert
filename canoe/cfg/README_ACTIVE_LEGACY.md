# CANoe CFG Profile Guide

## Active (Use This in GUI)
- `CAN_v2_topology_wip.cfg`
- `CAN_v2_topology_wip.cfg.ini`
- `CAN_v2_topology_wip.stcfg`

This is the only runtime profile for current development and SIL verification.

## V1 Legacy Backup (Do Not Use for Daily Development)
- `legacy/cfg/v1_cfg/CAN_500kBaud_1ch.cfg`
- `legacy/cfg/v1_cfg/CAN_500kBaud_1ch.cfg.ini`
- `legacy/cfg/v1_cfg/CAN_500kBaud_1ch.stcfg`

V1 was a single-bus flat architecture optimized for fast parallel development.
Use v1 profile only for compatibility troubleshooting and historical comparison.

## Operator Rule
When opening CANoe manually:
1. Open `cfg/CAN_v2_topology_wip.cfg`.
2. Do not select files under `legacy/cfg/v1_cfg` unless explicitly requested.

# CANoe CFG Profile Guide

## Active (Use This in GUI)
- `CAN_500kBaud_1ch_split.cfg`
- `CAN_500kBaud_1ch_split.cfg.ini`
- `CAN_500kBaud_1ch_split.stcfg`

This is the only runtime profile for current development and SIL verification.

## Legacy Backup (Do Not Use for Daily Development)
- `legacy/LEGACY_CAN_500kBaud_1ch.cfg`
- `legacy/LEGACY_CAN_500kBaud_1ch.cfg.ini`

Use legacy profile only for compatibility troubleshooting.

## Operator Rule
When opening CANoe manually:
1. Open `cfg/CAN_500kBaud_1ch_split.cfg`.
2. Do not select any file under `cfg/legacy` unless explicitly requested.

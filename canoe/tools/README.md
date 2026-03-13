# tools

Active utility scripts for CANoe maintenance.

## Kept Tools

### `generate_dbc_from_docs.py`
- generate draft DBC baselines from current `0303/0304` docs
- output path: `canoe/databases/`
- always review output manually before integration

### `validate_mentor_priority.py`
- enforce the active CAN/ETH priority gate
- uses active CAN DBCs and `ETH_INTERFACE_CONTRACT.md`
- writes a local gate report under `canoe/tmp/`
- exit code `0` = pass, `2` = fail

## Policy

- `driving-situation-alert` documents remain the source of truth
- generated artifacts are draft support outputs
- cfg patch helpers and reference-side helper scripts are not kept in the active tree

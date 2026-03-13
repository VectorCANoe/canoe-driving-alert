# tools

Active utility scripts for CANoe maintenance.

## Folder Convention

- `10_RUNTIME/`
  - runtime-side generation helpers
- `20_VERIFICATION/`
  - verification-side gates and checks

## Naming Rule

- `10_*` : runtime helpers
- `20_*` : verification helpers

## Kept Tools

### `10_RUNTIME/10_generate_can_dbc_from_docs.py`
- generate draft DBC baselines from current `0303/0304` docs
- output path: `canoe/databases/`
- always review output manually before integration

### `20_VERIFICATION/20_validate_runtime_priority_gate.py`
- enforce the active CAN/ETH priority gate
- uses active CAN DBCs and `10_ETHERNET_BACKBONE_SSoT.md`
- writes local draft outputs under `canoe/tmp/`
- exit code `0` = pass, `2` = fail

## Policy

- `driving-alert-workproducts` documents remain the source of truth
- generated artifacts are draft support outputs
- cfg patch helpers and reference-side helper scripts are not kept in the active tree

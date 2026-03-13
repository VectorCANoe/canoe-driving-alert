# CANoe File Index

Quick index for the active `canoe` surface.

## 0) First Open

1. `C:\Users\이준영\CANoe-IVI-OTA\driving-alert-workproducts\ops\handoff\TMP_HANDOFF.md`
2. `C:\Users\이준영\CANoe-IVI-OTA\canoe\README.md`
3. `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\operations\00_ACTIVE_WORKSET.md`

## 1) Runtime Core

- config
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\cfg\CAN_v2_topology_wip.cfg`
- sysvars
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\project\sysvars\project.sysvars`
- CAPL source of truth
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\src\capl\`
- GUI import mirror
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\cfg\channel_assign\`

## 2) Network Contracts

- CAN DBCs
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\chassis_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\powertrain_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\body_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\infotainment_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\adas_can.dbc`
- Ethernet contract
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\contracts\10_ETHERNET_BACKBONE_SSoT.md`
- ownership matrix
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\contracts\11_RUNTIME_MESSAGE_OWNERSHIP_MATRIX.md`
- multibus policy
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\contracts\12_RUNTIME_MULTIBUS_VISIBILITY_POLICY.md`

## 3) Verification

- `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\verification\20_CANOE_TEST_EXECUTION_GUIDE.md`
- `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\verification\21_SIL_ACCEPTANCE_CRITERIA.md`
- `C:\Users\이준영\CANoe-IVI-OTA\canoe\tests\`

## 4) Maintenance Tools

- `C:\Users\이준영\CANoe-IVI-OTA\canoe\tools\10_RUNTIME\10_generate_can_dbc_from_docs.py`
- `C:\Users\이준영\CANoe-IVI-OTA\canoe\tools\20_VERIFICATION\20_validate_runtime_priority_gate.py`

## 5) Archive Policy

- legacy runtime assets are preserved in archive branches and local `canoe/AGENT/legacy/`, not in the active root.
- local helper, reference, and staging assets may still exist under ignored paths for developer workflows.

# CANoe File Index

Quick index for the `canoe` folder.

## 0) First Open

If you are entering the CANoe side for daily work, open these first:

1. `C:\Users\이준영\CANoe-IVI-OTA\docs\DEVELOPMENT_ENTRYPOINTS.md`
2. `C:\Users\이준영\CANoe-IVI-OTA\driving-situation-alert\TMP_HANDOFF.md`
3. `C:\Users\이준영\CANoe-IVI-OTA\scripts\README.md`

## 1) Runtime Profiles

- Active runtime config:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\cfg\CAN_v2_topology_wip.cfg`
- V1 legacy backup config:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\cfg\v1_cfg\CAN_500kBaud_1ch.cfg`
- System variables:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\project\sysvars\project.sysvars`

## 2) CAN Databases

- Active split DBC set:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\chassis_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\powertrain_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\body_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\infotainment_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\adas_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\eth_backbone_can_stub.dbc`
- V1 legacy backup DBC:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\v1_legacy\v1_split_345bdb4\emergency_system.dbc`

## 3) CAPL Source

- v2 runtime source (cfg-referenced): `canoe\cfg\channel_assign\`
- mirror source tree: `canoe\src\capl\{input|logic|output|ems|ecu|network}\`
- v1 legacy backup source: `canoe\src\capl\v1_legacy\`

## 4) Documents

- Operations: `canoe\docs\operations\`
- Architecture: `canoe\docs\architecture\`
- Working outputs: `canoe\tmp\reports\verification\` (generated, not source)

## 5) Legacy Notes

- v1 was a single-bus flat architecture for fast parallel development.
- Legacy backups are under `canoe\cfg\v1_cfg\`, `canoe\databases\v1_legacy\`, `canoe\src\capl\v1_legacy\`.

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
- System variables:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\project\sysvars\project.sysvars`

## 2) CAN Databases

- Active CAN DBC set:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\chassis_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\powertrain_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\body_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\infotainment_can.dbc`
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\databases\adas_can.dbc`
- Ethernet contract SoT:
  - `C:\Users\이준영\CANoe-IVI-OTA\canoe\docs\operations\ETH_INTERFACE_CONTRACT.md`

## 3) CAPL Source

- v2 runtime source (cfg-referenced): `canoe\cfg\channel_assign\`
- mirror source tree: `canoe\src\capl\{common|ecu|input|logic|output}\`

## 4) Documents

- Operations: `canoe\docs\operations\`
- Generated local outputs may appear under `canoe\tmp\` during validation runs

## 5) Archive Notes

- v1 and pre-cutover backup assets are preserved in `archive/*` git branches.
- The active branch no longer keeps local `canoe\legacy\` or `canoe\src\capl\v1_legacy\` trees.

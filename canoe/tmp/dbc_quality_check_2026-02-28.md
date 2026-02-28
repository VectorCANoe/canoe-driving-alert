# DBC Quality Check (Mentoring 08 + MET_30)

## Scope
- Checked files:
  - `canoe/network/dbc/emergency_system.dbc`
  - `canoe/network/dbc/emergency_system_chassis.dbc`
  - `canoe/network/dbc/emergency_system_body.dbc`
  - `canoe/network/dbc/emergency_system_infotainment.dbc`
  - `canoe/network/dbc/emergency_system_powertrain.dbc`
  - `canoe/network/dbc/chassis_can.dbc`
  - `canoe/network/dbc/body_can.dbc`
  - `canoe/network/dbc/infotainment_can.dbc`
  - `canoe/network/dbc/powertrain_can.dbc`
  - `canoe/network/dbc/test_can.dbc`
- Reference-only docs:
  - `driving-situation-alert/tmp/Mentoring_08_Action_Plan.md`
  - `docs/meeting-notes/MET_30_2026.02.28.txt`

## Result Summary
- `PASS`: Domain-split DBC files exist (chassis/body/infotainment/powertrain).
- `PASS`: Ethernet is managed outside DBC (separate contract approach).
- `PASS`: All current DBC files are syntactically loadable by `cantools`.
- `PASS`: Vehicle baseline node expansion (Req_101~Req_112 context) is reflected in node inventory/comments.
- `PASS`: Expected ECU set (baseline + emergency core nodes) has no missing node in split DBC union.
- `PASS`: `Comm_101~Comm_106` core CAN message IDs are aligned in canonical files (`0x300~0x304`).
- `PARTIAL`: Network/gateway decomposition is mostly aligned, but infotainment domain currently includes both `INFOTAINMENT_GW` and `IVI_GW` in one DBC.
- `PASS`: Message volume reached mentoring target level (`44` split messages, target `>=40`).
- `GAP`: Central gateway-only network DBC (if required by final architecture) is not separated yet.

## Quantitative Snapshot
- `emergency_system.dbc`: 6 messages, 25 nodes
- `emergency_system_chassis.dbc`: 13 messages, 10 nodes
- `emergency_system_body.dbc`: 10 messages, 7 nodes
- `emergency_system_infotainment.dbc`: 10 messages, 7 nodes
- `emergency_system_powertrain.dbc`: 11 messages, 5 nodes
- Split message total (`chassis+body+infotainment+powertrain`): 44
- `chassis_can.dbc`: 3 messages (`0x100`, `0x101`, `0x301`)
- `powertrain_can.dbc`: 1 message (`0x300`)
- `body_can.dbc`: 2 messages (`0x210`, `0x302`)
- `infotainment_can.dbc`: 3 messages (`0x110`, `0x220`, `0x303`)
- `test_can.dbc`: 2 messages (`0x230`, `0x304`)

## Immediate DBC-Only Backlog
1. Re-check gateway ownership per network and decide whether infotainment should keep dual gateway nodes or split.
2. Keep ETH IDs (`0x510/0x511/0x512/0xE100/0xE200`) out of DBC and in ETH contract only.
3. Extend canonical domain files (`*_can.dbc`) from core IDs to target message scale (`80~120` CAN total).
4. Synchronize added CAN frames with next `0302/0303/0304` revision.

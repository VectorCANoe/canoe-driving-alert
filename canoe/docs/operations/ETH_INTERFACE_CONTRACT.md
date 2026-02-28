# Ethernet Interface Contract (CANoe SIL)

**Document ID**: CANOE-ETH-IFC  
**Version**: 1.0  
**Date**: 2026-02-28  
**Status**: Active  
**Scope**: CANoe SIL, UDP 湲곕컲 Ethernet 怨꾩빟 ?뺤쓽

---

## 1. 紐⑹쟻

- 蹂?臾몄꽌??`E100/E200, 0x510/0x511/0x512` Ethernet 硫붿떆吏???⑥씪 ?먮낯(Single Source of Truth)?대떎.
- CAN ?꾨젅???먮낯? `canoe/network/dbc/{chassis_can.dbc, body_can.dbc, infotainment_can.dbc, powertrain_can.dbc, test_can.dbc}`媛 ?대떦?섎ŉ, Ethernet ?꾨젅?꾩? 蹂?臾몄꽌媛 ?대떦?쒕떎.

---

## 2. Ethernet Message Contract

| Message | ID | DLC | Signal | Bit | Range | Tx Node | Rx Node | Period/Trigger | Clear/鍮꾧퀬 |
|---|---|---|---|---|---|---|---|---|---|
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0~7 | 0~255 | CHASSIS_GW | ADAS_WARN_CTRL | 100ms | Chassis CAN(0x100) ?뺢퇋??|
|  |  |  | driveState | 8~9 | 0~3 | CHASSIS_GW | ADAS_WARN_CTRL | 100ms | 0:P,1:R,2:N,3:D |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 0~1 | CHASSIS_GW | ADAS_WARN_CTRL | 100ms | Chassis CAN(0x101) ?뺢퇋??|
| ethNavContextMsg | 0x512 | 3 | roadZone | 0~1 | 0~3 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | Infotainment CAN(0x110) ?뺢퇋??|
|  |  |  | navDirection | 2~3 | 0~3 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | 0:None,1:Left,2:Right,3:Other |
|  |  |  | zoneDistance | 8~15 | 0~255 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | m |
|  |  |  | speedLimit | 16~23 | 0~255 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | km/h |
| ETH_EmergencyAlert | 0xE100 | 4 | emergencyType | 0~1 | 0~3 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 0:None,1:Police,2:Ambulance |
|  |  |  | emergencyDirection | 2~3 | 0~3 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 0:Front,1:Left,2:Right,3:Rear |
|  |  |  | eta | 8~15 | 0~255 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | s |
|  |  |  | sourceId | 16~23 | 0~255 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | ?숇쪧 ?먮떒 蹂댁“ |
|  |  |  | alertState | 24 | 0~1 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 0:Clear,1:Active |
| ethSelectedAlertMsg | 0xE200 | 2 | selectedAlertLevel | 0~2 | 0~7 | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms | 以묒옱 寃곌낵 |
|  |  |  | selectedAlertType | 3~5 | 0~7 | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms | 以묒옱 寃곌낵 |
|  |  |  | timeoutClear | 8 | 0~1 | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms | 1000ms 臾닿갚???댁젣 |

---

## 3. ?곌퀎 洹쒖튃

- `0302_NWflowDef.md`? `0303_Communication_Specification.md`??Ethernet ??ぉ? 蹂?臾몄꽌瑜?李몄“?쒕떎.
- `0304_System_Variables.md`??`ETH_IN/ETH_CORE` 蹂?섎뒗 蹂?臾몄꽌 Signal ?뺤쓽? 1:1 ??묓븳??
- 援ы쁽 蹂寃???媛깆떊 ?쒖꽌:
  - `ETH_INTERFACE_CONTRACT.md -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

## 4. 媛쒖젙 ?대젰

| 踰꾩쟾 | ?좎쭨 | 蹂寃??ы빆 |
|---|---|---|
| 1.0 | 2026-02-28 | Ethernet 怨꾩빟 ?먮낯 臾몄꽌 ?좉퇋 ?앹꽦(0x510/0x511/0x512/0xE100/0xE200) |



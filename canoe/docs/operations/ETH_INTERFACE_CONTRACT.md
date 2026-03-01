# Ethernet Interface Contract (CANoe SIL)

**Document ID**: CANOE-ETH-IFC  
**Version**: 1.0  
**Date**: 2026-02-28  
**Status**: Active  
**Scope**: CANoe SIL, UDP 기반 Ethernet 계약 정의

---

## 1. 목적

- 본 문서는 `E100/E200, 0x510/0x511/0x512` Ethernet 메시지의 단일 원본(Single Source of Truth)이다.
- CAN 프레임 원본은 `canoe/databases/chassis_can.dbc`, `canoe/databases/powertrain_can.dbc`, `canoe/databases/body_can.dbc`, `canoe/databases/infotainment_can.dbc`, `canoe/databases/test_can.dbc`가 담당하며, Ethernet 프레임은 본 문서가 담당한다.

---

## 2. Ethernet Message Contract

| Message | ID | DLC | Signal | Bit | Range | Tx Node | Rx Node | Period/Trigger | Clear/비고 |
|---|---|---|---|---|---|---|---|---|---|
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0~7 | 0~255 | CHASSIS_GW | ADAS_WARN_CTRL | 100ms | Chassis CAN(0x100) 정규화 |
|  |  |  | driveState | 8~9 | 0~3 | CHASSIS_GW | ADAS_WARN_CTRL | 100ms | 0:P,1:R,2:N,3:D |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 0~1 | CHASSIS_GW | ADAS_WARN_CTRL | 100ms | Chassis CAN(0x101) 정규화 |
| ethNavContextMsg | 0x512 | 3 | roadZone | 0~1 | 0~3 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | Infotainment CAN(0x110) 정규화 |
|  |  |  | navDirection | 2~3 | 0~3 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | 0:None,1:Left,2:Right,3:Other |
|  |  |  | zoneDistance | 8~15 | 0~255 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | m |
|  |  |  | speedLimit | 16~23 | 0~255 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | 100ms | km/h |
| ETH_EmergencyAlert | 0xE100 | 4 | emergencyType | 0~1 | 0~3 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 0:None,1:Police,2:Ambulance |
|  |  |  | emergencyDirection | 2~3 | 0~3 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 0:Front,1:Left,2:Right,3:Rear |
|  |  |  | eta | 8~15 | 0~255 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | s |
|  |  |  | sourceId | 16~23 | 0~255 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 동률 판단 보조 |
|  |  |  | alertState | 24 | 0~1 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms | 0:Clear,1:Active |
| ethSelectedAlertMsg | 0xE200 | 2 | selectedAlertLevel | 0~2 | 0~7 | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms | 중재 결과 |
|  |  |  | selectedAlertType | 3~5 | 0~7 | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms | 중재 결과 |
|  |  |  | timeoutClear | 8 | 0~1 | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms | 1000ms 무갱신 해제 |

---

## 3. 연계 규칙

- `0302_NWflowDef.md`와 `0303_Communication_Specification.md`의 Ethernet 항목은 본 문서를 참조한다.
- `0304_System_Variables.md`의 `ETH_IN/ETH_CORE` 변수는 본 문서 Signal 정의와 1:1 대응한다.
- 구현 변경 시 갱신 순서:
  - `ETH_INTERFACE_CONTRACT.md -> 0302 -> 0303 -> 0304 -> 04 -> 05/06/07`

---

## 4. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-28 | Ethernet 계약 원본 문서 신규 생성(0x510/0x511/0x512/0xE100/0xE200) |


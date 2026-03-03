# Ethernet Interface Contract (CANoe SIL)

**Document ID**: CANOE-ETH-IFC  
**Version**: 1.2  
**Date**: 2026-03-03  
**Status**: Active  
**Scope**: CANoe SIL, UDP 기반 Ethernet 계약 정의

---

## 1. 목적

- 본 문서는 `E100/E200/E210/E211/E212, 0x510/0x511/0x512` Ethernet 논리 메시지의 단일 원본(Single Source of Truth)이다.
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
| ethEmergencyRiskMsg | 0xE210 | 5 | proximityRiskLevel | 0~7 | 0~100 | ADAS_WARN_CTRL | WARN_ARB_MGR, SIL_TEST_CTRL | 100ms | V2 근접위험 산정 |
|  |  |  | emergencyDirection | 8~9 | 0~3 | ADAS_WARN_CTRL | WARN_ARB_MGR, SIL_TEST_CTRL | 100ms | 방향 정보 |
|  |  |  | eta | 16~23 | 0~255 | ADAS_WARN_CTRL | WARN_ARB_MGR, SIL_TEST_CTRL | 100ms | 도달예상시간(s) |
|  |  |  | vehicleSpeed | 24~31 | 0~255 | ADAS_WARN_CTRL | WARN_ARB_MGR, SIL_TEST_CTRL | 100ms | 자차 속도(km/h) |
| ethDecelAssistReqMsg | 0xE211 | 4 | decelAssistReq | 0 | 0~1 | WARN_ARB_MGR | DOMAIN_GW_ROUTER, BRAKE_CTRL, SIL_TEST_CTRL | Event + 50ms | V2 감속보조 요청 |
|  |  |  | driverReleaseReason | 1~3 | 0~7 | WARN_ARB_MGR | DOMAIN_GW_ROUTER, BRAKE_CTRL, SIL_TEST_CTRL | Event + 50ms | 해제 사유 |
| ethFailSafeStateMsg | 0xE212 | 2 | failSafeMode | 0~1 | 0~3 | DOMAIN_BOUNDARY_MGR | DOMAIN_GW_ROUTER, WARN_ARB_MGR, BODY_GW, IVI_GW, SIL_TEST_CTRL | 100ms + Event | V2 경로 단절 강등 |
|  |  |  | domainPathStatus | 2~3 | 0~3 | DOMAIN_BOUNDARY_MGR | DOMAIN_GW_ROUTER, WARN_ARB_MGR, BODY_GW, IVI_GW, SIL_TEST_CTRL | 100ms + Event | 도메인 경로 상태 |

---

## 2.1 SIL CAN Stub ID 매핑

| Ethernet Logical ID | SIL CAN Stub ID(`eth_backbone_can_stub.dbc`) | Message |
|---|---|---|
| 0xE100 | 0x064 | frmEmergencyBroadcastMsg |
| 0xE210 | 0x313 | ethEmergencyRiskMsg |
| 0xE211 | 0x314 | ethDecelAssistReqMsg |
| 0xE212 | 0x315 | ethFailSafeStateMsg |

- `0xE200(ethSelectedAlertMsg)`는 현재 SIL 구성에서 CAN Stub 프레임으로 분리하지 않고 Core 경로에서 직접 처리한다.
- CANoe.CAN 라이선스 SIL 구간에서는 위 Stub ID를 사용하고, Ethernet 라이선스 환경에서는 Logical ID 기준으로 동일 의미를 유지한다.

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
| 1.2 | 2026-03-03 | V2 활성 체인 정합 반영: `ethDecelAssistReqMsg(0xE211)` Tx를 `WARN_ARB_MGR`로 정정하고 `driverReleaseReason` 필드명을 통일. |
| 1.1 | 2026-03-03 | V2 확장 Pre-Activation Ethernet 계약(`ethEmergencyRiskMsg(0xE210)`, `ethDecelAssistReqMsg(0xE211)`, `ethFailSafeStateMsg(0xE212)`) 추가로 0303 Comm_120~124 SoT 정합 반영. |
| 1.0 | 2026-02-28 | Ethernet 계약 원본 문서 신규 생성(0x510/0x511/0x512/0xE100/0xE200) |

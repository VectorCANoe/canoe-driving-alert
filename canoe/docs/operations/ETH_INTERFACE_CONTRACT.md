# Ethernet Interface Contract (CANoe SIL)

**Document ID**: CANOE-ETH-IFC  
**Version**: 1.3  
**Date**: 2026-03-09  
**Status**: Active  
**Scope**: CANoe SIL, UDP 기반 Ethernet 계약 정의

---

## 1. 목적

- 본 문서는 `E100/E200/E210~E216`(논리 ID) 및 SIL Stub ID(`0x1C3/0x1C4/0x111/0x1C5~0x1C8`)를 포함한 Ethernet 메시지 계약의 단일 원본(Single Source of Truth)이다.
- CAN 프레임 원본은 `canoe/databases/chassis_can.dbc`, `canoe/databases/powertrain_can.dbc`, `canoe/databases/body_can.dbc`, `canoe/databases/infotainment_can.dbc`, `canoe/databases/adas_can.dbc`, `canoe/databases/eth_backbone_can_stub.dbc`가 담당하며, Ethernet 프레임은 본 문서가 담당한다.

---

## 2. Ethernet Message Contract

| Message | ID | DLC | Signal | Bit | Range | Tx Node | Rx Node | Period/Trigger | Clear/비고 |
|---|---|---|---|---|---|---|---|---|---|
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0~7 | 0~255 | VCU | CGW, IBOX | 100ms | CAN-stub backbone seam, downstream ECU logic keeps normalized core state |
|  |  |  | driveState | 8~9 | 0~3 | VCU | CGW, IBOX | 100ms | 0:P,1:R,2:N,3:D |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 0~1 | MDPS | CGW | 100ms | CAN-stub backbone seam, downstream ECU logic keeps normalized core state |
| ethNavContextMsg | 0x512 | 3 | roadZone | 0~1 | 0~3 | IVI | CGW, IBOX | 100ms | Infotainment CAN(0x2A3) backbone publication |
|  |  |  | navDirection | 2~3 | 0~3 | IVI | CGW, IBOX | 100ms | 0:None,1:Left,2:Right,3:Other |
|  |  |  | zoneDistance | 8~15 | 0~255 | IVI | CGW, IBOX | 100ms | m |
|  |  |  | speedLimit | 16~23 | 0~255 | IVI | CGW, IBOX | 100ms | km/h |
| ETH_EmergencyAlert | 0xE100 | 4 | emergencyType | 0~1 | 0~3 | V2X | V2X | 100ms | 0:None,1:Police,2:Ambulance |
|  |  |  | emergencyDirection | 2~3 | 0~3 | V2X | V2X | 100ms | 0:Front,1:Left,2:Right,3:Rear |
|  |  |  | eta | 8~15 | 0~255 | V2X | V2X | 100ms | s |
|  |  |  | sourceId | 16~23 | 0~255 | V2X | V2X | 100ms | 동률 판단 보조 |
|  |  |  | alertState | 24 | 0~1 | V2X | V2X | 100ms | 0:Clear,1:Active |
| ethSelectedAlertMsg | 0xE200 | 2 | selectedAlertLevel | 0~2 | 0~7 | ADAS | BCM, IVI | Event + 50ms | 중재 결과 |
|  |  |  | selectedAlertType | 3~5 | 0~7 | ADAS | BCM, IVI | Event + 50ms | 중재 결과 |
|  |  |  | timeoutClear | 8 | 0~1 | ADAS | BCM, IVI | Event + 50ms | 1000ms 무갱신 해제 |
| ethEmergencyRiskMsg | 0x1C3(SIL Stub) / 0xE210(Logical) | 5 | proximityRiskLevel | 0~7 | 0~100 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms | V2 근접위험 산정 |
|  |  |  | eta | 8~15 | 0~255 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms | 도달예상시간(s) |
|  |  |  | vehicleSpeed | 16~23 | 0~255 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms | 자차 속도(km/h) |
|  |  |  | emergencyDirection | 24~25 | 0~3 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms | 방향 정보 |
|  |  |  | emergencyType | 26~27 | 0~2 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms | 긴급차량 유형 |
| ethDecelAssistReqMsg | 0x1C4(SIL Stub) / 0xE211(Logical) | 4 | decelAssistReq | 0 | 0~1 | ADAS | ESC, VAL_SCENARIO_CTRL | Event + 50ms | decel assist decision export for SIL/runtime seam |
|  |  |  | failSafeMode | 1~2 | 0~2 | ADAS | ESC, VAL_SCENARIO_CTRL | Event + 50ms | 0:Normal,1:Degraded,2:Blocked |
|  |  |  | driverReleaseReason | 3~4 | 0~3 | ADAS | ESC, VAL_SCENARIO_CTRL | Event + 50ms | 0:None,1:Steer,2:Brake,3:FailSafe |
|  |  |  | emergencyContext | 5~6 | 0~2 | ADAS | ESC, VAL_SCENARIO_CTRL | Event + 50ms | 긴급 컨텍스트 |
|  |  |  | proximityRiskLevel | 8~15 | 0~100 | ADAS | ESC, VAL_SCENARIO_CTRL | Event + 50ms | 위험도 전달 |
| ethFailSafeStateMsg | 0x111(SIL Stub) / 0xE212(Logical) | 2 | domainPathStatus | 0~1 | 0~2 | CGW | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 0:Normal,1:Degraded,2:Failed |
|  |  |  | e2eHealthState | 2~3 | 0~2 | CGW | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 0:Failed,1:Degraded,2:Healthy |
|  |  |  | failSafeMode | 4~5 | 0~2 | CGW | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 강등 모드 상태 |
|  |  |  | boundaryAlive | 6 | 0~1 | CGW | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 경계관리 노드 생존 상태 |
| ethObjectRiskInputMsg | 0x1C5(SIL Stub) / 0xE213(Logical) | 8 | objectTrackValid | 0 | 0~1 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 객체 입력 유효성 |
|  |  |  | objectRange | 1~9 | 0~500 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 대표 객체 상대거리(m) |
|  |  |  | objectRelSpeed | 10~18 | -200~200 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 대표 객체 상대속도(km/h) |
|  |  |  | objectConfidence | 19~25 | 0~100 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 객체 신뢰도(%) |
|  |  |  | intersectionConflict | 26 | 0~1 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 교차로 충돌 맥락 |
|  |  |  | mergeCutIn | 27 | 0~1 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 합류/끼어들기 맥락 |
|  |  |  | objectAlertHoldMs | 28~40 | 0~5000 | VAL_SCENARIO_CTRL (SIL harness) | ADAS | 100ms | 추적손실 보수 유지시간(ms) |
| ethObjectRiskStateMsg | 0x1C6(SIL Stub) / 0xE214(Logical) | 6 | objectRiskClass | 0~2 | 0~7 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 객체 위험 등급 |
|  |  |  | objectTtcMinMs | 3~16 | 0~10000 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 객체 최소 TTC(ms) |
|  |  |  | objectRiskLevel | 17~23 | 0~100 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 객체 위험도(0~100) |
|  |  |  | objectTrackValid | 24 | 0~1 | ADAS | ADAS, VAL_SCENARIO_CTRL | 100ms + Event | 객체 추적 유효 상태 |
| ethObjectScenarioAlertMsg | 0x1C7(SIL Stub) / 0xE215(Logical) | 4 | objectAlertLevel | 0~2 | 0~7 | ADAS | BCM, IVI, VAL_SCENARIO_CTRL | Event + 50ms | 객체 맥락 경고 레벨 |
|  |  |  | objectAlertType | 3~5 | 0~7 | ADAS | BCM, IVI, VAL_SCENARIO_CTRL | Event + 50ms | 객체 맥락 경고 타입 |
|  |  |  | intersectionConflict | 6 | 0~1 | ADAS | BCM, IVI, VAL_SCENARIO_CTRL | Event + 50ms | 교차로 충돌 플래그 |
|  |  |  | mergeCutIn | 7 | 0~1 | ADAS | BCM, IVI, VAL_SCENARIO_CTRL | Event + 50ms | 합류 충돌 플래그 |
|  |  |  | objectRiskClass | 8~10 | 0~7 | ADAS | BCM, IVI, VAL_SCENARIO_CTRL | Event + 50ms | 객체 위험 분류 |
| ethObjectSafetyStateMsg | 0x1C8(SIL Stub) / 0xE216(Logical) | 4 | objectConfidence | 0~6 | 0~100 | CGW | ADAS, VAL_SCENARIO_CTRL, V2X | 100ms + Event | 객체 신뢰도 |
|  |  |  | objectEventCode | 7~22 | 0~65535 | CGW | ADAS, VAL_SCENARIO_CTRL, V2X | 100ms + Event | 객체 이벤트 코드 |
|  |  |  | objectFailSafeMode | 23~24 | 0~2 | CGW | ADAS, VAL_SCENARIO_CTRL, V2X | 100ms + Event | 객체 경로 강등 모드 |
|  |  |  | objectTrackValid | 25 | 0~1 | CGW | ADAS, VAL_SCENARIO_CTRL, V2X | 100ms + Event | 객체 추적 유효 상태 |

---

## 2.1 SIL Stub 매핑 규칙

| Logical ID (Architecture) | SIL Stub ID (CANoe.CAN) | 비고 |
|---|---|---|
| 0xE210 | 0x1C3 | `ethEmergencyRiskMsg` |
| 0xE211 | 0x1C4 | `ethDecelAssistReqMsg` |
| 0xE212 | 0x111 | `ethFailSafeStateMsg` |
| 0xE213 | 0x1C5 | `ethObjectRiskInputMsg` |
| 0xE214 | 0x1C6 | `ethObjectRiskStateMsg` |
| 0xE215 | 0x1C7 | `ethObjectScenarioAlertMsg` |
| 0xE216 | 0x1C8 | `ethObjectSafetyStateMsg` |

- 시스템/문서 아키텍처는 Logical ID를 기준으로 해석한다.
- CANoe.CAN 라이선스 SIL 구현은 Stub ID(0x1C3/0x1C4/0x111/0x1C5~0x1C8)를 사용한다.
- Ethernet 라이선스 적용 시 동일 의미를 Logical ID 기반으로 재검증한다.

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
| 1.3 | 2026-03-09 | Active runtime sender 기준으로 Ethernet contract 정렬: `VCU/MDPS/IVI/CGW/V2X` ownership 및 CAN-stub backbone seam 설명 최신화. |
| 1.2 | 2026-03-06 | ADAS 객체 인지 Pre-Activation 계약 추가: `E213~E216` (`ethObjectRiskInputMsg`, `ethObjectRiskStateMsg`, `ethObjectScenarioAlertMsg`, `ethObjectSafetyStateMsg`) 및 SIL Stub ID(`0x1C5~0x1C8`) 반영. |
| 1.1 | 2026-03-03 | V2 확장 메시지(`ethEmergencyRiskMsg`, `ethDecelAssistReqMsg`, `ethFailSafeStateMsg`) 및 SIL Stub ID 매핑(0x1C3/0x1C4/0x111) 추가. |
| 1.0 | 2026-02-28 | Ethernet 계약 원본 문서 신규 생성(0x510/0x511/0x512/0xE100/0xE200) |

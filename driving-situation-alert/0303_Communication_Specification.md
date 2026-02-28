# 통신 명세서 (Communication Specification)

**Document ID**: PROJ-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 (Software Architectural Design)
**Version**: 2.8
**Date**: 2026-02-28
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2) | `0303_Communication_Specification.md` | `0302_NWflowDef.md` | `0304_System_Variables.md` |

---

## 작성 원칙

- 상단 표는 공식 샘플(`0303.md`)과 동일하게 `Message/Identifier/DLC/Signal/signal bit position/Data 설명/Data 범위/Data 사용` 열만 사용한다.
- `Identifier`는 순수 ID 값만 기재한다(예: `0x100`, `0xE100`).
- `DLC`는 순수 숫자만 기재한다.
- 상단 표의 `Signal`은 0304 표준 변수명(`vehicleSpeed` 등) 기준으로 작성하고, 코드/런타임 별칭(`g*`)은 하단 보강표에서만 관리한다.
- 본 설계는 Ethernet 백본(`ETH_SWITCH`) + 도메인 게이트웨이(`CHASSIS_GW`, `INFOTAINMENT_GW`, `BODY_GW`, `IVI_GW`) + 도메인 CAN 분배 구조를 사용한다.
- 하단 추적표는 `Comm ID -> Flow ID -> Func ID -> Req ID`를 유지한다.
- 검증 범위는 CANoe SIL, CAN + Ethernet(UDP)로 고정한다.

---

## 통신 명세 표 (공식 표준 양식)

| Message | Identifier | DLC | Signal | signal bit position | Data 설명 | Data 범위 | Data 사용 |
|---|---|---|---|---|---|---|---|
| frmVehicleStateCanMsg | 0x100 | 2 | vehicleSpeed | 0 | 차량 속도 입력 | 0~255 km/h | Chassis CAN에서 CHASSIS_GW가 수신 후 Ethernet으로 변환 전달 |
|  |  |  |  | 1 |  |  |  |
|  |  |  |  | 2 |  |  |  |
|  |  |  |  | 3 |  |  |  |
|  |  |  |  | 4 |  |  |  |
|  |  |  |  | 5 |  |  |  |
|  |  |  |  | 6 |  |  |  |
|  |  |  |  | 7 |  |  |  |
|  |  |  | driveState | 8 | 주행 상태 입력(P/R/N/D) | 0~3 | ADAS_WARN_CTRL 주행/비주행 활성 판단 입력 |
|  |  |  |  | 9 |  |  |  |
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0 | 게이트웨이 변환 차량 속도 | 0~255 km/h | CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
|  |  |  |  | 1 |  |  |  |
|  |  |  |  | 2 |  |  |  |
|  |  |  |  | 3 |  |  |  |
|  |  |  |  | 4 |  |  |  |
|  |  |  |  | 5 |  |  |  |
|  |  |  |  | 6 |  |  |  |
|  |  |  |  | 7 |  |  |  |
|  |  |  | driveState | 8 | 게이트웨이 변환 주행 상태 | 0~3 | 경고 엔진 조건 판정 입력 |
|  |  |  |  | 9 |  |  |  |
| frmSteeringCanMsg | 0x101 | 1 | steeringInput | 0 | 조향 입력 여부 | 0:미입력 / 1:입력 | Chassis CAN에서 CHASSIS_GW가 수신 |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 게이트웨이 변환 조향 입력 | 0:미입력 / 1:입력 | CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| frmNavContextCanMsg | 0x110 | 2 | roadZone | 0 | 구간 타입 | 0:일반 / 1:스쿨존 / 2:고속 / 3:유도 | Infotainment CAN에서 INFOTAINMENT_GW가 수신 |
|  |  |  |  | 1 |  |  |  |
|  |  |  | navDirection | 2 | 유도 방향 | 0:없음 / 1:좌 / 2:우 / 3:기타 | 방향 안내 정책 입력 |
|  |  |  |  | 3 |  |  |  |
|  |  |  | zoneDistance | 8 | 구간까지 남은 거리 | 0~255 m | 구간 전환 타이밍 판단 입력 |
|  |  |  |  | 9 |  |  |  |
|  |  |  |  | 10 |  |  |  |
|  |  |  |  | 11 |  |  |  |
|  |  |  |  | 12 |  |  |  |
|  |  |  |  | 13 |  |  |  |
|  |  |  |  | 14 |  |  |  |
|  |  |  |  | 15 |  |  |  |
| ethNavContextMsg | 0x512 | 2 | roadZone | 0 | 게이트웨이 변환 구간 타입 | 0~3 | INFOTAINMENT_GW -> ETH_SWITCH -> NAV_CONTEXT_MGR/WARN_ARB_MGR |
|  |  |  |  | 1 |  |  |  |
|  |  |  | navDirection | 2 | 게이트웨이 변환 유도 방향 | 0:없음 / 1:좌 / 2:우 / 3:기타 | 구간 안내 분기 입력 |
|  |  |  |  | 3 |  |  |  |
|  |  |  | zoneDistance | 8 | 게이트웨이 변환 구간 거리 | 0~255 m | 구간 컨텍스트 갱신 입력 |
|  |  |  |  | 9 |  |  |  |
|  |  |  |  | 10 |  |  |  |
|  |  |  |  | 11 |  |  |  |
|  |  |  |  | 12 |  |  |  |
|  |  |  |  | 13 |  |  |  |
|  |  |  |  | 14 |  |  |  |
|  |  |  |  | 15 |  |  |  |
| ETH_EmergencyAlert | 0xE100 | 4 | emergencyType | 0 | 긴급차량 종류 | 0:None / 1:Police / 2:Ambulance | EMS_POLICE_TX/EMS_AMB_TX -> ETH_SWITCH -> EMS_ALERT_RX |
|  |  |  |  | 1 |  |  |  |
|  |  |  | emergencyDirection | 2 | 접근 방향 | 0:앞 / 1:좌 / 2:우 / 3:후 | CLU_HMI_CTRL 방향 표시 입력 |
|  |  |  |  | 3 |  |  |  |
|  |  |  | eta | 8 | 도달 예상 시간 | 0~255 s | WARN_ARB_MGR 우선순위 판단 |
|  |  |  |  | 9 |  |  |  |
|  |  |  |  | 10 |  |  |  |
|  |  |  |  | 11 |  |  |  |
|  |  |  |  | 12 |  |  |  |
|  |  |  |  | 13 |  |  |  |
|  |  |  |  | 14 |  |  |  |
|  |  |  |  | 15 |  |  |  |
|  |  |  | sourceId | 16 | 송신 주체 ID | 0~255 | ETA 동률 시 2차 우선순위 판단 |
|  |  |  |  | 17 |  |  |  |
|  |  |  |  | 18 |  |  |  |
|  |  |  |  | 19 |  |  |  |
|  |  |  |  | 20 |  |  |  |
|  |  |  |  | 21 |  |  |  |
|  |  |  |  | 22 |  |  |  |
|  |  |  |  | 23 |  |  |  |
|  |  |  | alertState | 24 | 경고 상태 | 0:Clear / 1:Active | Clear/타임아웃 처리 기준 |
| ethSelectedAlertMsg | 0xE200 | 2 | selectedAlertLevel | 0 | 최종 경고 레벨 | 0~7 | WARN_ARB_MGR -> ETH_SWITCH -> BODY_GW/IVI_GW |
|  |  |  |  | 1 |  |  |  |
|  |  |  |  | 2 |  |  |  |
|  |  |  | selectedAlertType | 3 | 최종 경고 타입 | 0~7 | 도메인별 출력 분기 |
|  |  |  |  | 4 |  |  |  |
|  |  |  |  | 5 |  |  |  |
|  |  |  | timeoutClear | 8 | 타임아웃 해제 플래그 | 0/1 | 출력 복귀 조건 신호 |
| frmAmbientControlMsg | 0x210 | 1 | ambientMode | 0 | 앰비언트 동작 모드 | 0~7 | BODY_GW -> BCM_AMBIENT_CTRL(CAN) |
|  |  |  |  | 1 |  |  |  |
|  |  |  |  | 2 |  |  |  |
|  |  |  | ambientColor | 3 | 앰비언트 색상 코드 | 0~7 | 긴급/구간 정책 색상 출력 |
|  |  |  |  | 4 |  |  |  |
|  |  |  |  | 5 |  |  |  |
|  |  |  | ambientPattern | 6 | 점등 패턴 코드 | 0~3 | 고정/점멸/파동 패턴 제어 |
|  |  |  |  | 7 |  |  |  |
| frmClusterWarningMsg | 0x220 | 1 | warningTextCode | 0 | 클러스터 경고 코드 | 0~255 | IVI_GW -> CLU_HMI_CTRL(Infotainment CAN) |
|  |  |  |  | 1 |  |  |  |
|  |  |  |  | 2 |  |  |  |
|  |  |  |  | 3 |  |  |  |
|  |  |  |  | 4 |  |  |  |
|  |  |  |  | 5 |  |  |  |
|  |  |  |  | 6 |  |  |  |
|  |  |  |  | 7 |  |  |  |
| frmTestResultMsg | 0x230 | 1 | scenarioResult | 0 | 테스트 판정 결과 | 0:Fail / 1:Pass | SIL_TEST_CTRL 결과 기록 및 로그 연동 |

---

## 하단 보강표 (감사/추적 전용)

- 상단 공식 표준 양식은 변경하지 않고 유지한다.
- 아래 표들은 추적성/감사 해석 명확화를 위한 하단 보강 정보다.

---

## 통신 상세 추적 표 (Comm/Flow/Func/Req)

| Comm ID | Flow ID | Func ID | Req ID | Message(ID) | Tx Node | Rx Node | Protocol | Period | Clear/비고 |
|---|---|---|---|---|---|---|---|---|---|
| Comm_001 | Flow_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x100), ethVehicleStateMsg(0x510) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 |
| Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x101), ethSteeringMsg(0x511) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 |
| Comm_003 | Flow_003 | Func_007 | Req_007 | frmNavContextCanMsg(0x110), ethNavContextMsg(0x512) | SIL_TEST_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CONTEXT_MGR, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리 입력 갱신 |
| Comm_004 | Flow_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_POLICE_TX | EMS_ALERT_RX | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_005 | Flow_005 | Func_018 | Req_018 | ETH_EmergencyAlert(0xE100) | EMS_AMB_TX | EMS_ALERT_RX | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_006 | Flow_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT_RX, WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | 1000ms 무갱신 시 timeoutClear=1 |
| Comm_007 | Flow_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_036, Req_037, Req_038, Req_039 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x210) | WARN_ARB_MGR, BODY_GW | BODY_GW, BCM_AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_008 | Flow_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x220) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_009 | Flow_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x230) | SIL_TEST_CTRL | SIL_TEST_CTRL(Log/Panel) | CAN | Event | 판정 결과 기록 완료 시 종료 |

---

## Comm_006 메시지 단계 분해 (감사용 명확화)

| 단계 | 상위 Comm ID | Message(ID) | Tx Node | Rx Node | 주기/조건 |
|---|---|---|---|---|---|
| Ingress | Comm_006 | ETH_EmergencyAlert(0xE100) | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms, Active/Clear |
| Egress | Comm_006 | ethSelectedAlertMsg(0xE200) | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms |

- 주의: `Comm_006`은 입력(E100)과 출력(E200) 단계를 묶은 논리 Comm이며, 감사 시에는 위 단계 표를 기준으로 `Rx/Tx`를 분리 해석한다.

### 표준 Signal-별칭(g*) 매핑 (문서/코드 정합용)

| 표준 Signal(0303/0304) | 코드/런타임 별칭 |
|---|---|
| vehicleSpeed | gVehicleSpeed |
| driveState | gDriveState |
| roadZone | gRoadZone |
| navDirection | gNavDirection |
| zoneDistance | gZoneDistance |

---

## 0302/0304 연계 체크포인트

- `Comm ID`는 `0302_NWflowDef.md`의 `Flow ID`와 1:1 연결한다.
- 모든 Comm 항목은 `0304_System_Variables.md`에서 Signal 단위 변수(`Var ID`)로 연결한다.
- 필수 검증 항목:
- `EmergencyAlert` Active/Clear 신호가 1000ms 타임아웃 규칙과 일치해야 한다.
- `selectedAlertLevel/selectedAlertType` 기반 Ambient/Cluster 출력 Comm이 모두 존재해야 한다.
- `ETH_SWITCH` 경유 Ethernet 신호가 각 도메인 게이트웨이에서 CAN 메시지로 정상 변환되어야 한다.

---

## 통신 예외 처리 규칙

| Comm Group | 예외 조건 | Fail-safe 동작 | 검증 포인트 |
|---|---|---|---|
| Group_A(Comm_001,002) | CHASSIS_GW 변환 프레임 누락(연속 2주기) | ADAS_WARN_CTRL 입력 품질 플래그 저하, 경고 강등 모드 진입 | CAN 입력 정상 + ETH 변환 누락 시 동작 확인 |
| Group_B(Comm_003) | INFOTAINMENT_GW 변환 프레임 누락(연속 2주기) | NAV_CONTEXT_MGR를 일반구간 기본 컨텍스트로 복귀 | 유도구간 상태에서 변환 누락 주입 |
| Group_C(Comm_004~006) | EmergencyAlert 1000ms 무갱신 | `timeoutClear=1`, emergencyContext clear, 출력 복귀 | Req_024 타임아웃 검증 |
| Group_D(Comm_007) | BODY_GW CAN 송신 ACK 실패 | ambientMode를 안전 기본값(0)으로 전환 후 재전송 | CAN Tx fail 주입 테스트 |
| Group_E(Comm_008) | IVI_GW CAN 송신 ACK 실패 | warningTextCode를 최소 안내 코드로 축소 후 재전송 | Cluster 경고 축소 출력 확인 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 최신 프로젝트 스코프 반영 전면 재작성. Comm_001~Comm_009 및 Flow/Func/Req 1:1 추적 구조 반영, OTA/UDS/DoIP 제거 |
| 2.1 | 2026-02-25 | 공식 샘플 표기 스타일(Identifier/DLC 순수값)로 상단 표 정렬, Ethernet 백본+도메인 게이트웨이+CAN 분배 구조 반영 |
| 2.2 | 2026-02-25 | 상단 공식표 signal bit position을 개별 비트 행으로 전개하고 Comm별 통신 예외 처리 규칙 추가 |
| 2.3 | 2026-02-25 | navDirection 범위를 0304 변수 정의(0~3)와 정합되게 통일하고 ScenarioResult bit 행(0 단일 bit) 표기를 일치화 |
| 2.4 | 2026-02-26 | Cluster 경고 경로를 Infotainment CAN 기준으로 명확화(IVI_GW -> CLU_HMI_CTRL) |
| 2.5 | 2026-02-26 | Comm_006 단계 분해 표(E100 Ingress / E200 Egress) 추가로 감사 해석 모호성 제거 |
| 2.6 | 2026-02-26 | 상단 공식표 비변경 원칙을 명시하고 하단 보강표 구역(감사/추적 전용)으로 분리 |
| 2.7 | 2026-02-26 | 상단 Signal 명칭을 0304 표준명(vehicleSpeed 등)으로 통일하고, g* 별칭은 하단 매핑표로 분리 |
| 2.8 | 2026-02-28 | signal 케이스/명칭을 0304 표준명(`steeringInput/emergencyType/eta/sourceId` 등)으로 정합하고 `SelectedAlertContext` 잔여 표현 제거 |

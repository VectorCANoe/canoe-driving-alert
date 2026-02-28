# 시스템 변수 정의 (System Variables)

**Document ID**: PROJ-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 / SWE.3
**Version**: 2.4
**Date**: 2026-02-28
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2/SWE.3) | `0304_System_Variables.md` | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

---

## 작성 원칙

- 상단 표는 공식 샘플(`0304.md`)과 동일하게 `ID/Namespace/Name/Data type/Min/Max/Initial Value/Description` 열만 사용한다.
- 상단 표의 `Namespace`는 도메인명(`Chassis/Infotainment/V2X/Core/Body/Cluster/Test`)을 사용하고, `Name`은 순수 기능 변수명으로 유지한다.
- 통신 계층/버스 경로/구현 식별자(`*_CAN_IN`, `*_ETH_CORE`, `*_CAN_OUT`)는 하단 매핑 표와 추적표에서 관리한다.
- 하단 추적표에서 `Var -> Comm -> Flow -> Func -> Req` 1:1 연결을 명시한다.

---

## 시스템 변수 표 (공식 표준 양식)

| ID | Namespace | Name | Data type | Min | Max | Initial Value | Description |
|---|---|---|---|---|---|---|---|
| 1 | Chassis | vehicleSpeed | uint32 | 0 | 255 | 0 | 차량 속도 입력값 |
| 2 | Chassis | driveState | uint32 | 0 | 3 | 0 | 주행 상태(P/R/N/D) 입력값 |
| 3 | Chassis | steeringInput | uint32 | 0 | 1 | 0 | 조향 입력 여부 |
| 4 | Infotainment | roadZone | uint32 | 0 | 3 | 0 | 구간 타입 입력값 |
| 5 | Infotainment | navDirection | uint32 | 0 | 3 | 0 | 내비게이션 방향 정보 |
| 6 | Infotainment | zoneDistance | uint32 | 0 | 255 | 0 | 구간 잔여 거리 |
| 7 | V2X | emergencyType | uint32 | 0 | 3 | 0 | 긴급차량 종류 |
| 8 | V2X | emergencyDirection | uint32 | 0 | 3 | 0 | 긴급차량 접근 방향 |
| 9 | V2X | eta | uint32 | 0 | 255 | 0 | 긴급차량 ETA(유효값 0~255, 내부 invalid sentinel 65535) |
| 10 | V2X | sourceId | uint32 | 0 | 255 | 0 | 긴급 메시지 Source ID |
| 11 | V2X | alertState | uint32 | 0 | 1 | 0 | 긴급 메시지 Active/Clear 상태 |
| 12 | Core | vehicleSpeedNorm | uint32 | 0 | 255 | 0 | 게이트웨이 정규화 후 차량 속도 |
| 13 | Core | driveStateNorm | uint32 | 0 | 3 | 0 | 게이트웨이 정규화 후 주행 상태 |
| 14 | Core | steeringInputNorm | uint32 | 0 | 1 | 0 | 게이트웨이 정규화 후 조향 입력 |
| 15 | Core | baseZoneContext | uint32 | 0 | 255 | 0 | 구간 컨텍스트 계산 결과 |
| 16 | Core | warningState | uint32 | 0 | 255 | 0 | 경고 조건 판정 상태 |
| 17 | Core | emergencyContext | uint32 | 0 | 255 | 0 | 긴급 수신 컨텍스트 상태 |
| 18 | Core | selectedAlertLevel | uint32 | 0 | 7 | 0 | 중재 결과 경고 레벨 |
| 19 | Core | selectedAlertType | uint32 | 0 | 7 | 0 | 중재 결과 경고 타입 |
| 20 | Core | timeoutClear | uint32 | 0 | 1 | 0 | 1000ms 무갱신 해제 플래그 |
| 21 | Body | ambientMode | uint32 | 0 | 7 | 0 | 앰비언트 제어 모드 |
| 22 | Body | ambientColor | uint32 | 0 | 7 | 0 | 앰비언트 색상 코드 |
| 23 | Body | ambientPattern | uint32 | 0 | 3 | 0 | 앰비언트 패턴 코드 |
| 24 | Cluster | warningTextCode | uint32 | 0 | 255 | 0 | 클러스터 경고 코드 |
| 25 | Test | testScenario | uint32 | 0 | 255 | 0 | SIL 테스트 시나리오 선택값 |
| 26 | Test | scenarioResult | uint32 | 0 | 1 | 0 | SIL 시나리오 Pass/Fail 결과 |
| 27 | CoreState | lastEmergencyRxMs | uint32 | 0 | 60000 | 0 | 마지막 긴급 신호 수신 시각(ms) |
| 28 | CoreState | duplicatePopupGuard | uint32 | 0 | 5000 | 0 | 중복 팝업 억제 타이머(ms) |
| 29 | CoreState | arbitrationSnapshotId | uint32 | 0 | 65535 | 0 | 중재 스냅샷 식별자 |

---

## 표준 Name-내부 구현 Name 매핑 표

| ID | Namespace(표준) | Name(표준) | Internal Name(구현) | 계층 | Bus Path |
|---|---|---|---|---|---|
| 1 | Chassis | vehicleSpeed | vehicleSpeed_CAN_IN | CAN_IN | Chassis CAN -> CHASSIS_GW |
| 2 | Chassis | driveState | driveState_CAN_IN | CAN_IN | Chassis CAN -> CHASSIS_GW |
| 3 | Chassis | steeringInput | steeringInput_CAN_IN | CAN_IN | Chassis CAN -> CHASSIS_GW |
| 4 | Infotainment | roadZone | roadZone_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 5 | Infotainment | navDirection | navDirection_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 6 | Infotainment | zoneDistance | zoneDistance_CAN_IN | CAN_IN | Infotainment CAN -> INFOTAINMENT_GW |
| 7 | V2X | emergencyType | emergencyType_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT_RX |
| 8 | V2X | emergencyDirection | emergencyDirection_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT_RX |
| 9 | V2X | eta | eta_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT_RX |
| 10 | V2X | sourceId | sourceId_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT_RX |
| 11 | V2X | alertState | alertState_ETH_IN | ETH_IN | Ethernet UDP -> EMS_ALERT_RX |
| 12 | Core | vehicleSpeedNorm | vehicleSpeed_ETH_CORE | ETH_CORE | CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| 13 | Core | driveStateNorm | driveState_ETH_CORE | ETH_CORE | CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| 14 | Core | steeringInputNorm | steeringInput_ETH_CORE | ETH_CORE | CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| 15 | Core | baseZoneContext | baseZoneContext_ETH_CORE | ETH_CORE | INFOTAINMENT_GW -> ETH_SWITCH -> NAV_CONTEXT_MGR |
| 16 | Core | warningState | warningState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL 내부 계산 |
| 17 | Core | emergencyContext | emergencyContext_ETH_CORE | ETH_CORE | EMS_ALERT_RX 내부 계산 |
| 18 | Core | selectedAlertLevel | selectedAlertLevel_ETH_CORE | ETH_CORE | WARN_ARB_MGR 내부 계산 |
| 19 | Core | selectedAlertType | selectedAlertType_ETH_CORE | ETH_CORE | WARN_ARB_MGR 내부 계산 |
| 20 | Core | timeoutClear | timeoutClear_ETH_CORE | ETH_CORE | EMS_ALERT_RX 생성 -> WARN_ARB_MGR 소비(타임아웃 해제) |
| 21 | Body | ambientMode | ambientMode_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SWITCH -> BODY_GW -> BCM_AMBIENT_CTRL |
| 22 | Body | ambientColor | ambientColor_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SWITCH -> BODY_GW -> BCM_AMBIENT_CTRL |
| 23 | Body | ambientPattern | ambientPattern_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SWITCH -> BODY_GW -> BCM_AMBIENT_CTRL |
| 24 | Cluster | warningTextCode | warningTextCode_CAN_OUT | CAN_OUT | WARN_ARB_MGR -> ETH_SWITCH -> IVI_GW -> CLU_HMI_CTRL |
| 25 | Test | testScenario | testScenario_INPUT | TEST | SIL_TEST_CTRL Panel Input |
| 26 | Test | scenarioResult | scenarioResult_OUTPUT | TEST | SIL_TEST_CTRL Test Result Output |
| 27 | CoreState | lastEmergencyRxMs | lastEmergencyRxMs | CORE_STATE | EMS_ALERT_RX 내부 상태 |
| 28 | CoreState | duplicatePopupGuard | duplicatePopupGuard | CORE_STATE | CLU_HMI_CTRL 내부 상태 |
| 29 | CoreState | arbitrationSnapshotId | arbitrationSnapshotId | CORE_STATE | WARN_ARB_MGR 내부 상태 |

---

## 변수 구현 속성 보강 표 (Unit/Scale/Endian/Invalid)

| Name(표준) | Internal Name(구현) | Unit | Scale | Endian | Invalid Value | 비고 |
|---|---|---|---|---|---|---|
| vehicleSpeed | vehicleSpeed_CAN_IN | km/h | 1 | Little | 255 | 센서 단절 시 최대값 예약 |
| driveState | driveState_CAN_IN | enum | 1 | Little | 255 | 0:P,1:R,2:N,3:D |
| steeringInput | steeringInput_CAN_IN | bool | 1 | Little | 255 | 0/1 외 값은 invalid |
| roadZone | roadZone_CAN_IN | enum | 1 | Little | 255 | 0:일반,1:스쿨존,2:고속,3:유도 |
| navDirection | navDirection_CAN_IN | enum | 1 | Little | 255 | 0:없음,1:좌,2:우,3:기타 |
| zoneDistance | zoneDistance_CAN_IN | m | 1 | Little | 65535 | 거리 미수신 시 invalid |
| emergencyType | emergencyType_ETH_IN | enum | 1 | Little | 255 | 0:none,1:police,2:ambulance |
| emergencyDirection | emergencyDirection_ETH_IN | enum | 1 | Little | 255 | 0:front,1:left,2:right,3:rear |
| eta | eta_ETH_IN | s | 1 | Little | 65535 | 유효범위 0~255, 내부 처리에서 65535를 invalid sentinel로 사용 |
| sourceId | sourceId_ETH_IN | id | 1 | Little | 65535 | 송신원 미식별 값 |
| alertState | alertState_ETH_IN | bool | 1 | Little | 255 | 0:clear,1:active |
| vehicleSpeedNorm | vehicleSpeed_ETH_CORE | km/h | 1 | Little | 255 | GW 정규화 후 값 |
| driveStateNorm | driveState_ETH_CORE | enum | 1 | Little | 255 | GW 정규화 후 값 |
| steeringInputNorm | steeringInput_ETH_CORE | bool | 1 | Little | 255 | GW 정규화 후 값 |
| baseZoneContext | baseZoneContext_ETH_CORE | context_id | 1 | Little | 65535 | 컨텍스트 계산 실패 값 |
| warningState | warningState_ETH_CORE | state_id | 1 | Little | 65535 | 경고 판정 실패 값 |
| emergencyContext | emergencyContext_ETH_CORE | state_id | 1 | Little | 65535 | 긴급 컨텍스트 미유효 값 |
| selectedAlertLevel | selectedAlertLevel_ETH_CORE | level | 1 | Little | 255 | 0~7 이외 invalid |
| selectedAlertType | selectedAlertType_ETH_CORE | type | 1 | Little | 255 | 0~7 이외 invalid |
| timeoutClear | timeoutClear_ETH_CORE | bool | 1 | Little | 255 | 0/1 외 값 invalid |
| ambientMode | ambientMode_CAN_OUT | mode | 1 | Little | 255 | 안전 기본값은 0 |
| ambientColor | ambientColor_CAN_OUT | color_id | 1 | Little | 255 | palette 외 값 invalid |
| ambientPattern | ambientPattern_CAN_OUT | pattern_id | 1 | Little | 255 | 패턴 코드 외 invalid |
| warningTextCode | warningTextCode_CAN_OUT | text_id | 1 | Little | 65535 | 메시지 테이블 미매칭 값 |
| testScenario | testScenario_INPUT | scenario_id | 1 | Little | 65535 | 미등록 시나리오 값 |
| scenarioResult | scenarioResult_OUTPUT | bool | 1 | Little | 255 | 0:fail,1:pass |
| lastEmergencyRxMs | lastEmergencyRxMs | ms | 1 | Little | 4294967295 | 타임스탬프 미기록 값 |
| duplicatePopupGuard | duplicatePopupGuard | ms | 1 | Little | 4294967295 | 타이머 비활성 예약값 |
| arbitrationSnapshotId | arbitrationSnapshotId | seq | 1 | Little | 4294967295 | 스냅샷 미생성 값 |

---

## 변수 추적 상세 표 (Var/Comm/Flow/Func/Req)

| Var ID | 표준 Name | Internal Name | 계층 | Owner Node | Comm ID | Flow ID | Func ID | Req ID | 갱신 규칙 |
|---|---|---|---|---|---|---|---|---|---|
| Var_001 | vehicleSpeed | vehicleSpeed_CAN_IN | CAN_IN | CHASSIS_GW | Comm_001 | Flow_001 | Func_001, Func_010 | Req_001, Req_010 | 100ms CAN 수신 시 갱신 |
| Var_002 | driveState | driveState_CAN_IN | CAN_IN | CHASSIS_GW | Comm_001 | Flow_001 | Func_001, Func_002 | Req_001, Req_002 | 100ms CAN 수신 시 갱신 |
| Var_003 | steeringInput | steeringInput_CAN_IN | CAN_IN | CHASSIS_GW | Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | 100ms CAN 수신 시 갱신 |
| Var_004 | roadZone | roadZone_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_005 | navDirection | navDirection_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_006 | zoneDistance | zoneDistance_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_007 | emergencyType | emergencyType_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_025, Func_029 | Req_017, Req_018, Req_023, Req_025, Req_029 | E100 수신 시 즉시 갱신 |
| Var_008 | emergencyDirection | emergencyDirection_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_020, Func_023 | Req_017, Req_018, Req_020, Req_023 | E100 수신 시 즉시 갱신 |
| Var_009 | eta | eta_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_030 | Req_017, Req_018, Req_023, Req_030 | E100 수신 시 즉시 갱신 |
| Var_010 | sourceId | sourceId_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_031 | Req_017, Req_018, Req_023, Req_031 | E100 수신 시 즉시 갱신 |
| Var_011 | alertState | alertState_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_024 | Req_017, Req_018, Req_023, Req_024 | Active/Clear 변화 시 갱신 |
| Var_012 | vehicleSpeedNorm | vehicleSpeed_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001 | Flow_001 | Func_001, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_003, Req_004, Req_006, Req_010 | CHASSIS_GW 변환 메시지 수신 시 갱신 |
| Var_013 | driveStateNorm | driveState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001 | Flow_001 | Func_001, Func_002 | Req_001, Req_002 | CHASSIS_GW 변환 메시지 수신 시 갱신 |
| Var_014 | steeringInputNorm | steeringInput_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | CHASSIS_GW 변환 메시지 수신 시 갱신 |
| Var_015 | baseZoneContext | baseZoneContext_ETH_CORE | ETH_CORE | NAV_CONTEXT_MGR | Comm_003 | Flow_003 | Func_007 | Req_007 | NAV 컨텍스트 계산 후 갱신 |
| Var_016 | warningState | warningState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001, Comm_002, Comm_006 | Flow_001, Flow_002, Flow_006 | Func_003, Func_004, Func_006, Func_010, Func_011, Func_012, Func_027 | Req_003, Req_004, Req_006, Req_010, Req_011, Req_012, Req_027 | 경고 조건 계산 시 갱신 |
| Var_017 | emergencyContext | emergencyContext_ETH_CORE | ETH_CORE | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_024 | Req_017, Req_018, Req_023, Req_024 | E100 수신/해제/타임아웃 시 갱신 |
| Var_018 | selectedAlertLevel | selectedAlertLevel_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_022, Func_025, Func_026, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_025, Req_026, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | 중재 결과 생성 시 갱신 |
| Var_019 | selectedAlertType | selectedAlertType_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_022, Func_025, Func_026, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_025, Req_026, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | 중재 결과 생성 시 갱신 |
| Var_020 | timeoutClear | timeoutClear_ETH_CORE | ETH_CORE | EMS_ALERT_RX | Comm_006 | Flow_006 | Func_024, Func_033, Func_034 | Req_024, Req_033, Req_034 | 1000ms 무갱신 시 1로 전환(WARN_ARB_MGR 전달) |
| Var_021 | ambientMode | ambientMode_CAN_OUT | CAN_OUT | BODY_GW/BCM_AMBIENT_CTRL | Comm_007 | Flow_007 | Func_008, Func_009, Func_013~Func_016, Func_033~Func_039 | Req_008, Req_009, Req_013~Req_016, Req_033~Req_039 | 50ms 출력 주기 갱신 |
| Var_022 | ambientColor | ambientColor_CAN_OUT | CAN_OUT | BODY_GW/BCM_AMBIENT_CTRL | Comm_007 | Flow_007 | Func_035, Func_037, Func_038, Func_039 | Req_035, Req_037, Req_038, Req_039 | 50ms 출력 주기 갱신 |
| Var_023 | ambientPattern | ambientPattern_CAN_OUT | CAN_OUT | BODY_GW/BCM_AMBIENT_CTRL | Comm_007 | Flow_007 | Func_015, Func_036, Func_037, Func_038, Func_039 | Req_015, Req_036, Req_037, Req_038, Req_039 | 50ms 출력 주기 갱신 |
| Var_024 | warningTextCode | warningTextCode_CAN_OUT | CAN_OUT | IVI_GW/CLU_HMI_CTRL | Comm_008 | Flow_008 | Func_005, Func_019~Func_021, Func_026, Func_040 | Req_005, Req_019~Req_021, Req_026, Req_040 | 50ms 출력 주기 갱신 |
| Var_025 | testScenario | testScenario_INPUT | TEST | SIL_TEST_CTRL | Comm_009 | Flow_009 | Func_041, Func_042 | Req_041, Req_042 | 시나리오 시작 시 설정 |
| Var_026 | scenarioResult | scenarioResult_OUTPUT | TEST | SIL_TEST_CTRL | Comm_009 | Flow_009 | Func_043 | Req_043 | 시나리오 종료 시 판정 기록 |
| Var_027 | lastEmergencyRxMs | lastEmergencyRxMs | CORE_STATE | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_023, Func_024 | Req_023, Req_024 | E100 수신 시각(ms) 기록, 1000ms 타임아웃 기준 |
| Var_028 | duplicatePopupGuard | duplicatePopupGuard | CORE_STATE | CLU_HMI_CTRL | Comm_008 | Flow_008 | Func_026 | Req_026 | 동일 Alert 반복 시 타이머 갱신 |
| Var_029 | arbitrationSnapshotId | arbitrationSnapshotId | CORE_STATE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_032 | Req_032 | 중재 수행 시 스냅샷 ID 증가 |

---

## 0303/코드 연계 체크포인트

- `0303`의 모든 Signal은 본 문서 변수와 1개 이상 매핑되어야 한다.
- `timeoutClear`(내부 구현: `timeoutClear_ETH_CORE`)는 `Req_024(1000ms)` 검증 로직과 직접 연결되어야 한다.
- `selectedAlertLevel`, `selectedAlertType`(내부 구현: `selectedAlertLevel_ETH_CORE`, `selectedAlertType_ETH_CORE`)는 `WARN_ARB_MGR` 출력의 단일 소스로 유지한다.
- 구현 단계에서 코드 레벨 변수 키는 `Internal Name`을 기준으로 통일하고, 문서 간 추적은 `표준 Name`과 함께 병기한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 옵션1 아키텍처 기준으로 전면 재작성. 변수 계층(CAN_IN/ETH_CORE/CAN_OUT) 분리, Var-Comm-Flow-Func-Req 추적 표 추가 |
| 2.1 | 2026-02-25 | 상단 29개 변수와 하단 추적표를 1:1 대응하도록 누락 변수(emergency*_ETH_IN, driveState_ETH_CORE, warningState_ETH_CORE, lastEmergencyRxMs) 직접 매핑 추가 |
| 2.2 | 2026-02-25 | 변수 구현 속성 보강 표(Unit/Scale/Endian/Invalid) 추가로 04 구현 시 해석 오차 방지 기준 명시 |
| 2.3 | 2026-02-25 | 상단 공식표를 도메인 Namespace + 순수 Name 구조로 정리하고, 통신/구현 식별자는 하단 매핑/추적 표로 분리 |
| 2.4 | 2026-02-28 | `timeoutClear` 생성 주체를 EMS_ALERT_RX로 명확화, `selectedAlertLevel/Type` Func/Req 범위표기를 명시 나열로 전환, `eta` 유효범위/invalid sentinel 규칙을 분리 명시 |

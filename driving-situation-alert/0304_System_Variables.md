# 시스템 변수 정의 (System Variables)

**Document ID**: PROJ-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 / SWE.3
**Version**: 2.1
**Date**: 2026-02-25
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2/SWE.3) | `0304_System_Variables.md` | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

---

## 작성 원칙

- 상단 표는 공식 샘플(`0304.md`)과 동일하게 `ID/Namespace/Name/Data type/Min/Max/Initial Value/Description` 열만 사용한다.
- 변수 계층을 고정한다: `*_CAN_IN` -> `*_ETH_CORE` -> `*_CAN_OUT`.
- 옵션1 아키텍처(ETH_SWITCH + 도메인 GW + 도메인 CAN)의 전달/중재 상태를 변수로 분리한다.
- 하단 추적표에서 `Var -> Comm -> Flow -> Func -> Req` 1:1 연결을 명시한다.

---

## 시스템 변수 표 (공식 표준 양식)

| ID | Namespace | Name | Data type | Min | Max | Initial Value | Description |
|---|---|---|---|---|---|---|---|
| 1 | InputCan | vehicleSpeed_CAN_IN | uint32 | 0 | 255 | 0 | Chassis CAN에서 수신한 차량 속도 입력 |
| 2 | InputCan | driveState_CAN_IN | uint32 | 0 | 3 | 0 | Chassis CAN에서 수신한 주행 상태(P/R/N/D) |
| 3 | InputCan | steeringInput_CAN_IN | uint32 | 0 | 1 | 0 | Chassis CAN에서 수신한 조향 입력 여부 |
| 4 | InputCan | roadZone_CAN_IN | uint32 | 0 | 3 | 0 | Infotainment CAN에서 수신한 구간 타입 |
| 5 | InputCan | navDirection_CAN_IN | uint32 | 0 | 3 | 0 | Infotainment CAN에서 수신한 방향 정보 |
| 6 | InputCan | zoneDistance_CAN_IN | uint32 | 0 | 255 | 0 | Infotainment CAN에서 수신한 구간 잔여 거리 |
| 7 | EthIn | emergencyType_ETH_IN | uint32 | 0 | 3 | 0 | Ethernet 긴급 신호 종류 |
| 8 | EthIn | emergencyDirection_ETH_IN | uint32 | 0 | 3 | 0 | Ethernet 긴급 신호 접근 방향 |
| 9 | EthIn | eta_ETH_IN | uint32 | 0 | 255 | 0 | Ethernet 긴급 신호 ETA |
| 10 | EthIn | sourceId_ETH_IN | uint32 | 0 | 255 | 0 | Ethernet 긴급 신호 SourceID |
| 11 | EthIn | alertState_ETH_IN | uint32 | 0 | 1 | 0 | Ethernet 긴급 신호 Active/Clear 상태 |
| 12 | EthCore | vehicleSpeed_ETH_CORE | uint32 | 0 | 255 | 0 | CHASSIS_GW가 정규화한 속도 입력 |
| 13 | EthCore | driveState_ETH_CORE | uint32 | 0 | 3 | 0 | CHASSIS_GW가 정규화한 주행 상태 |
| 14 | EthCore | steeringInput_ETH_CORE | uint32 | 0 | 1 | 0 | CHASSIS_GW가 정규화한 조향 입력 |
| 15 | EthCore | baseZoneContext_ETH_CORE | uint32 | 0 | 255 | 0 | NAV_CONTEXT_MGR가 생성한 구간 컨텍스트 |
| 16 | EthCore | warningState_ETH_CORE | uint32 | 0 | 255 | 0 | ADAS_WARN_CTRL 경고 조건 판정 상태 |
| 17 | EthCore | emergencyContext_ETH_CORE | uint32 | 0 | 255 | 0 | EMS_ALERT_RX 긴급 수신 상태 |
| 18 | EthCore | selectedAlertLevel_ETH_CORE | uint32 | 0 | 7 | 0 | WARN_ARB_MGR 중재 결과 레벨 |
| 19 | EthCore | selectedAlertType_ETH_CORE | uint32 | 0 | 7 | 0 | WARN_ARB_MGR 중재 결과 타입 |
| 20 | EthCore | timeoutClear_ETH_CORE | uint32 | 0 | 1 | 0 | 1000ms 무갱신 시 해제 플래그 |
| 21 | OutputCan | ambientMode_CAN_OUT | uint32 | 0 | 7 | 0 | BODY_GW를 통해 BCM_AMBIENT_CTRL로 송신되는 모드 |
| 22 | OutputCan | ambientColor_CAN_OUT | uint32 | 0 | 7 | 0 | BODY_GW를 통해 BCM_AMBIENT_CTRL로 송신되는 색상 |
| 23 | OutputCan | ambientPattern_CAN_OUT | uint32 | 0 | 3 | 0 | BODY_GW를 통해 BCM_AMBIENT_CTRL로 송신되는 패턴 |
| 24 | OutputCan | warningTextCode_CAN_OUT | uint32 | 0 | 255 | 0 | IVI_GW를 통해 CLU_HMI_CTRL로 송신되는 경고 코드 |
| 25 | Test | testScenario_INPUT | uint32 | 0 | 255 | 0 | SIL 테스트 시나리오 선택값 |
| 26 | Test | scenarioResult_OUTPUT | uint32 | 0 | 1 | 0 | SIL 시나리오 Pass/Fail 판정 결과 |
| 27 | CoreState | lastEmergencyRxMs | uint32 | 0 | 60000 | 0 | 마지막 긴급 신호 수신 시각(ms) |
| 28 | CoreState | duplicatePopupGuard | uint32 | 0 | 5000 | 0 | 중복 팝업 억제 타이머(ms) |
| 29 | CoreState | arbitrationSnapshotId | uint32 | 0 | 65535 | 0 | 중재 입력 스냅샷 식별자 |

---

## 변수 추적 상세 표 (Var/Comm/Flow/Func/Req)

| Var ID | 변수명 | 계층 | Owner Node | Comm ID | Flow ID | Func ID | Req ID | 갱신 규칙 |
|---|---|---|---|---|---|---|---|---|
| Var_001 | vehicleSpeed_CAN_IN | CAN_IN | CHASSIS_GW | Comm_001 | Flow_001 | Func_001, Func_010 | Req_001, Req_010 | 100ms CAN 수신 시 갱신 |
| Var_002 | driveState_CAN_IN | CAN_IN | CHASSIS_GW | Comm_001 | Flow_001 | Func_001, Func_002 | Req_001, Req_002 | 100ms CAN 수신 시 갱신 |
| Var_003 | steeringInput_CAN_IN | CAN_IN | CHASSIS_GW | Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | 100ms CAN 수신 시 갱신 |
| Var_004 | roadZone_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_005 | navDirection_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_006 | zoneDistance_CAN_IN | CAN_IN | INFOTAINMENT_GW | Comm_003 | Flow_003 | Func_007 | Req_007 | 100ms CAN 수신 시 갱신 |
| Var_007 | emergencyType_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_025, Func_029 | Req_017, Req_018, Req_023, Req_025, Req_029 | E100 수신 시 즉시 갱신 |
| Var_008 | emergencyDirection_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_020, Func_023 | Req_017, Req_018, Req_020, Req_023 | E100 수신 시 즉시 갱신 |
| Var_009 | eta_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_030 | Req_017, Req_018, Req_023, Req_030 | E100 수신 시 즉시 갱신 |
| Var_010 | sourceId_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_031 | Req_017, Req_018, Req_023, Req_031 | E100 수신 시 즉시 갱신 |
| Var_011 | alertState_ETH_IN | ETH_IN | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_024 | Req_017, Req_018, Req_023, Req_024 | Active/Clear 변화 시 갱신 |
| Var_012 | vehicleSpeed_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001 | Flow_001 | Func_001, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_003, Req_004, Req_006, Req_010 | CHASSIS_GW 변환 메시지 수신 시 갱신 |
| Var_013 | driveState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001 | Flow_001 | Func_001, Func_002 | Req_001, Req_002 | CHASSIS_GW 변환 메시지 수신 시 갱신 |
| Var_014 | steeringInput_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | CHASSIS_GW 변환 메시지 수신 시 갱신 |
| Var_015 | baseZoneContext_ETH_CORE | ETH_CORE | NAV_CONTEXT_MGR | Comm_003 | Flow_003 | Func_007 | Req_007 | NAV 컨텍스트 계산 후 갱신 |
| Var_016 | warningState_ETH_CORE | ETH_CORE | ADAS_WARN_CTRL | Comm_001, Comm_002, Comm_006 | Flow_001, Flow_002, Flow_006 | Func_003, Func_004, Func_006, Func_010, Func_011, Func_012, Func_027 | Req_003, Req_004, Req_006, Req_010, Req_011, Req_012, Req_027 | 경고 조건 계산 시 갱신 |
| Var_017 | emergencyContext_ETH_CORE | ETH_CORE | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_017, Func_018, Func_023, Func_024 | Req_017, Req_018, Req_023, Req_024 | E100 수신/해제/타임아웃 시 갱신 |
| Var_018 | selectedAlertLevel_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_022, Func_025~Func_032 | Req_022, Req_025~Req_032 | 중재 결과 생성 시 갱신 |
| Var_019 | selectedAlertType_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_022, Func_025~Func_032 | Req_022, Req_025~Req_032 | 중재 결과 생성 시 갱신 |
| Var_020 | timeoutClear_ETH_CORE | ETH_CORE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_024, Func_033, Func_034 | Req_024, Req_033, Req_034 | 1000ms 무갱신 시 1로 전환 |
| Var_021 | ambientMode_CAN_OUT | CAN_OUT | BODY_GW/BCM_AMBIENT_CTRL | Comm_007 | Flow_007 | Func_008, Func_009, Func_013~Func_016, Func_033~Func_039 | Req_008, Req_009, Req_013~Req_016, Req_033~Req_039 | 50ms 출력 주기 갱신 |
| Var_022 | ambientColor_CAN_OUT | CAN_OUT | BODY_GW/BCM_AMBIENT_CTRL | Comm_007 | Flow_007 | Func_035, Func_037, Func_038, Func_039 | Req_035, Req_037, Req_038, Req_039 | 50ms 출력 주기 갱신 |
| Var_023 | ambientPattern_CAN_OUT | CAN_OUT | BODY_GW/BCM_AMBIENT_CTRL | Comm_007 | Flow_007 | Func_015, Func_036, Func_037, Func_038, Func_039 | Req_015, Req_036, Req_037, Req_038, Req_039 | 50ms 출력 주기 갱신 |
| Var_024 | warningTextCode_CAN_OUT | CAN_OUT | IVI_GW/CLU_HMI_CTRL | Comm_008 | Flow_008 | Func_005, Func_019~Func_021, Func_026, Func_040 | Req_005, Req_019~Req_021, Req_026, Req_040 | 50ms 출력 주기 갱신 |
| Var_025 | testScenario_INPUT | TEST | SIL_TEST_CTRL | Comm_009 | Flow_009 | Func_041, Func_042 | Req_041, Req_042 | 시나리오 시작 시 설정 |
| Var_026 | scenarioResult_OUTPUT | TEST | SIL_TEST_CTRL | Comm_009 | Flow_009 | Func_043 | Req_043 | 시나리오 종료 시 판정 기록 |
| Var_027 | lastEmergencyRxMs | CORE_STATE | EMS_ALERT_RX | Comm_004, Comm_005, Comm_006 | Flow_004, Flow_005, Flow_006 | Func_023, Func_024 | Req_023, Req_024 | E100 수신 시각(ms) 기록, 1000ms 타임아웃 기준 |
| Var_028 | duplicatePopupGuard | CORE_STATE | CLU_HMI_CTRL | Comm_008 | Flow_008 | Func_026 | Req_026 | 동일 Alert 반복 시 타이머 갱신 |
| Var_029 | arbitrationSnapshotId | CORE_STATE | WARN_ARB_MGR | Comm_006 | Flow_006 | Func_032 | Req_032 | 중재 수행 시 스냅샷 ID 증가 |

---

## 0303/코드 연계 체크포인트

- `0303`의 모든 Signal은 본 문서 변수와 1개 이상 매핑되어야 한다.
- `timeoutClear_ETH_CORE`는 `Req_024(1000ms)` 검증 로직과 직접 연결되어야 한다.
- `selectedAlertLevel_ETH_CORE`, `selectedAlertType_ETH_CORE`는 `WARN_ARB_MGR` 출력의 단일 소스로 유지한다.
- 구현 단계에서 변수명은 동일 키(`Name`)를 CAPL/C 코드/테스트 스크립트에 공통 사용한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 옵션1 아키텍처 기준으로 전면 재작성. 변수 계층(CAN_IN/ETH_CORE/CAN_OUT) 분리, Var-Comm-Flow-Func-Req 추적 표 추가 |
| 2.1 | 2026-02-25 | 상단 29개 변수와 하단 추적표를 1:1 대응하도록 누락 변수(emergency*_ETH_IN, driveState_ETH_CORE, warningState_ETH_CORE, lastEmergencyRxMs) 직접 매핑 추가 |

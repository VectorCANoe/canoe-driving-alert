# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 4.7
**Date**: 2026-02-28
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 작성 원칙

- 본 문서는 요구사항(01)의 What을 노드 기능(How)으로 분해한다.
- 상단 표는 표준 양식 구조만 유지하고, 상세 추적 정보는 하단 표에 분리한다.
- Panel은 테스트 자극/관측 인터페이스이며 기능 주체 ECU로 보지 않는다.
- 기능 ID는 `Func_001~Func_043`으로 요구사항 ID와 1:1 대응한다.
- DBC 단계에서 OEM 네이밍으로 변경 가능하며, 기능 ID/추적 ID는 유지한다.
- 네트워크 구현은 옵션1 아키텍처를 고정 적용한다: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 도메인 CAN`.

---

## 기능 정의 표 (공식 표준 양식)

| 분류 | 기능명 | 기능설명 | 비고 | 검증 |
|---|---|---|---|---|
| 입력 | 구간 정보 | 구간 상태 입력(일반/스쿨존/고속/유도) | Panel/Indicator로 값 입력 | Req_007 / Flow_003 / Comm_003 / ST_ZONE_001 |
| 입력 | 유도 방향 | 유도 구간 방향 입력(좌/우) | Panel/Indicator로 값 입력 | Req_014 / Flow_003 / Comm_003 / ST_GUIDE_001 |
| 입력 | 구간 거리 | 구간 거리 입력 | TrackBar로 값 조절 | Req_013 / Flow_003 / Comm_003 / ST_GUIDE_002 |
| 입력 | 제한 속도 | 현재 구간 제한속도 입력 | CAN 또는 Panel 입력 | Req_007,Req_010 / Flow_003 / Comm_003 / ST_SPEED_001 |
| 입력 | 차량 속도 | 차량 속도 입력 | CAN 또는 Panel 입력 | Req_001,Req_010 / Flow_001 / Comm_001 / ST_SPEED_001 |
| 입력 | 조향 입력 | 조향 입력 여부 입력 | CAN 또는 Panel 입력 | Req_011,Req_012 / Flow_002 / Comm_002 / ST_STEER_001 |
| 입력 | 경찰 긴급 활성 | 경찰 긴급 활성 상태 입력 | Switch/Indicator ON/OFF | Req_017 / Flow_004 / Comm_004 / ST_EMS_001 |
| 입력 | 경찰 ETA | 경찰 도달예상시간 입력 | TrackBar로 값 조절 | Req_030 / Flow_006 / Comm_006 / ST_ARB_ETA_001 |
| 입력 | 경찰 방향 | 경찰 접근 방향 입력 | Switch/Indicator로 방향 선택 | Req_020 / Flow_006 / Comm_006 / ST_HMI_DIR_001 |
| 입력 | 구급 긴급 활성 | 구급 긴급 활성 상태 입력 | Switch/Indicator ON/OFF | Req_018 / Flow_005 / Comm_005 / ST_EMS_002 |
| 입력 | 구급 ETA | 구급 도달예상시간 입력 | TrackBar로 값 조절 | Req_030 / Flow_006 / Comm_006 / ST_ARB_ETA_002 |
| 입력 | 구급 방향 | 구급 접근 방향 입력 | Switch/Indicator로 방향 선택 | Req_020 / Flow_006 / Comm_006 / ST_HMI_DIR_002 |
| 입력 | 시나리오 선택 | 테스트 시나리오 선택 입력 | 테스트 패널 선택 | Req_041 / Flow_009 / Comm_009 / ST_SIL_001 |
| 출력 | 앰비언트 제어 | 구간/긴급 상태에 따른 앰비언트 출력 | ETH 백본 -> BODY_GW -> CAN 출력 | Req_008~Req_009,Req_013~Req_016,Req_033~Req_039 / Flow_007 / Comm_007 / IT_AMB_001 |
| 출력 | 클러스터 경고 | 경고 문구 및 상태 출력 | ETH 백본 -> IVI_GW -> CAN 출력 | Req_005,Req_019~Req_021,Req_026,Req_040 / Flow_008 / Comm_008 / IT_CLU_001 |
| 출력 | 경찰 알림 송신 | 경찰 긴급 알림 송신 | Ethernet UDP 송신 | Req_017 / Flow_004 / Comm_004 / IT_EMS_TX_001 |
| 출력 | 구급 알림 송신 | 구급 긴급 알림 송신 | Ethernet UDP 송신 | Req_018 / Flow_005 / Comm_005 / IT_EMS_TX_002 |
| 출력 | 판정 결과 | 시나리오 판정 결과 출력 | 로그/패널 출력 | Req_043 / Flow_009 / Comm_009 / ST_RESULT_001 |
| ECU 동작 | 구간 컨텍스트 관리 | 구간/제한속도 입력을 바탕으로 컨텍스트 갱신 | 상태 업데이트 | Req_007,Req_010 / Flow_003 / Comm_003 / UT_NAV_001 |
| ECU 동작 | 경고 조건 판정 | 속도/조향/제한속도 기반 경고 조건 판정 | 경고 트리거 생성 | Req_001~Req_004,Req_006,Req_010~Req_012 / Flow_001,Flow_002,Flow_003 / Comm_001,Comm_002,Comm_003 / UT_ADAS_001 |
| ECU 동작 | 경찰 알림 송신 제어 | 경찰 알림 송신 주기 관리 | 송신 상태 관리 | Req_017 / Flow_004 / Comm_004 / UT_EMS_POL_001 |
| ECU 동작 | 구급 알림 송신 제어 | 구급 알림 송신 주기 관리 | 송신 상태 관리 | Req_018 / Flow_005 / Comm_005 / UT_EMS_AMB_001 |
| ECU 동작 | 긴급 알림 수신 처리 | 긴급 알림 수신/해제 처리 | 타임아웃 처리 | Req_023,Req_024 / Flow_006 / Comm_006 / UT_EMS_RX_001 |
| ECU 동작 | 우선순위 중재 | 긴급/구간 충돌 시 우선순위 결정 | 중재 결과 산출 | Req_022,Req_025~Req_032 / Flow_006 / Comm_006 / UT_ARB_001 |
| ECU 동작 | 앰비언트 제어 | 경고 패턴/색상 적용 | 패턴 결정 | Req_008,Req_009,Req_013~Req_016,Req_033~Req_039 / Flow_007 / Comm_007 / UT_BCM_001 |
| ECU 동작 | 클러스터 표시 | 경고 문구/유형 표시 | 문구 결정 | Req_005,Req_019~Req_021,Req_026,Req_040 / Flow_008 / Comm_008 / UT_CLU_001 |
| ECU 동작 | 테스트 실행/판정 | 테스트 시나리오 실행 및 판정 | Pass/Fail 기록 | Req_041~Req_043 / Flow_009 / Comm_009 / ST_SIL_002 |

---

## 기능 정의 상세 표 (추적성/노드/입출력 정의)
| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_001 | Req_001 | ADAS_WARN_CTRL | 주행시 경고엔진 활성 | 주행 상태에서 경고 판단 엔진 활성화 | 입력: vehicleSpeedNorm, driveStateNorm / 출력: warningState |
| Func_002 | Req_002 | ADAS_WARN_CTRL | 비주행 경고 억제 | 정차/비주행 상태에서 경고 출력 억제 | 입력: driveStateNorm / 출력: warningState |
| Func_003 | Req_003 | ADAS_WARN_CTRL | 경고 시작 트리거 | 경고 조건 성립 시 출력층 활성 시작 | 입력: baseZoneContext, warningState / 출력: warningState |
| Func_004 | Req_004 | ADAS_WARN_CTRL | 경고 종료 트리거 | 해제 조건 성립 시 출력층 종료 | 입력: warningState / 출력: warningState |
| Func_005 | Req_005 | CLU_HMI_CTRL | 경고 원인 전달 | 경고 원인 텍스트 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_006 | Req_006 | ADAS_WARN_CTRL | 반복 경고 디바운스 | 동일 경고 재출력 간격 제어 | 입력: warningState / 출력: warningState |
| Func_007 | Req_007 | NAV_CONTEXT_MGR | 구간값 변경 반영 | roadZone/speedLimit 변경 시 구간 상태 갱신 | 입력: roadZone, navDirection, zoneDistance, speedLimit / 출력: baseZoneContext, speedLimitNorm |
| Func_008 | Req_008 | BCM_AMBIENT_CTRL | 일반구간 정책 적용 | 일반 구간 기본 패턴 적용 | 입력: selectedAlertLevel / 출력: ambientMode |
| Func_009 | Req_009 | BCM_AMBIENT_CTRL | 스쿨존 강화 경고 | 스쿨존 전용 강화 패턴 적용 | 입력: selectedAlertLevel / 출력: ambientMode |
| Func_010 | Req_010 | ADAS_WARN_CTRL | 스쿨존 과속 경고 | 스쿨존 속도 초과 이벤트 판정 | 입력: vehicleSpeedNorm, speedLimitNorm, baseZoneContext / 출력: warningState |
| Func_011 | Req_011 | ADAS_WARN_CTRL | 고속 장시간 무조향 감지 | 고속 구간 무조향 타이머 경고 | 입력: steeringInputNorm, baseZoneContext / 출력: warningState |
| Func_012 | Req_012 | ADAS_WARN_CTRL | 무조향 경고 해제 | 조향 입력 복귀 시 경고 해제 | 입력: steeringInputNorm / 출력: warningState |
| Func_013 | Req_013 | BCM_AMBIENT_CTRL | 유도구간 진입 전환 | 유도구간 진입 시 방향안내 모드 전환 | 입력: selectedAlertType, navDirection / 출력: ambientMode |
| Func_014 | Req_014 | BCM_AMBIENT_CTRL | 좌우 방향 구분 표시 | navDirection 기준 좌/우 패턴 분기 | 입력: navDirection / 출력: ambientPattern |
| Func_015 | Req_015 | BCM_AMBIENT_CTRL | 구간 전환 완화 | 전환 중 점멸 튐 현상 완화 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_016 | Req_016 | BCM_AMBIENT_CTRL | 구간경고 종료 복귀 | 조건 해제 시 기본 구간 패턴 복귀 | 입력: timeoutClear / 출력: ambientMode |
| Func_017 | Req_017 | EMS_POLICE_TX | 경찰 접근 경고 송신 | 경찰 긴급 ACTIVE 알림 송신 | 출력: emergencyType, emergencyDirection, eta, sourceId, alertState / ETH_EmergencyAlert |
| Func_018 | Req_018 | EMS_AMB_TX | 구급 접근 경고 송신 | 구급 긴급 ACTIVE 알림 송신 | 출력: emergencyType, emergencyDirection, eta, sourceId, alertState / ETH_EmergencyAlert |
| Func_019 | Req_019 | CLU_HMI_CTRL | 긴급차량 종류 표시 | 경찰/구급 타입 구분 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_020 | Req_020 | CLU_HMI_CTRL | 긴급차량 방향 표시 | 접근 방향 정보 표시 | 입력: emergencyDirection / 출력: warningTextCode |
| Func_021 | Req_021 | CLU_HMI_CTRL | 양보 유도 메시지 | 양보 요청 고정 메시지 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_022 | Req_022 | WARN_ARB_MGR | 긴급경고 우선 출력 | 일반 안내보다 긴급경고 우선 적용 | 입력: emergencyContext, warningState, baseZoneContext / 출력: selectedAlertLevel, selectedAlertType |
| Func_023 | Req_023 | EMS_ALERT_RX | 종료 신호 처리 | CLEAR 수신 시 긴급경고 종료 | 입력: alertState, emergencyType / 출력: emergencyContext |
| Func_024 | Req_024 | EMS_ALERT_RX | 타임아웃 보호해제 | 1000ms 무갱신 시 안전 해제 | 입력: lastEmergencyRxMs / 출력: timeoutClear |
| Func_025 | Req_025 | WARN_ARB_MGR | 다중긴급 단일선택 | 동시 긴급 신호 중 1개 선택 | 입력: emergencyContext / 출력: selectedAlertType |
| Func_026 | Req_026 | CLU_HMI_CTRL | 중복 팝업 억제 | 동일 긴급 이벤트 중복 팝업 억제 | 입력: selectedAlertType, duplicatePopupGuard / 출력: warningTextCode |
| Func_027 | Req_027 | WARN_ARB_MGR | 충돌중재 개시 | 구간/긴급 동시 발생 시 중재 시작 | 입력: emergencyContext, warningState / 출력: selectedAlertLevel |
| Func_028 | Req_028 | WARN_ARB_MGR | 긴급>구간 우선 적용 | 긴급 시 구간 패턴 오버라이드 | 입력: emergencyContext / 출력: selectedAlertLevel |
| Func_029 | Req_029 | WARN_ARB_MGR | 구급>경찰 우선 적용 | emergencyType 우선순위 적용 | 입력: emergencyType / 출력: selectedAlertType |
| Func_030 | Req_030 | WARN_ARB_MGR | ETA 우선 적용 | 동급 알림이면 ETA 최소값 선택 | 입력: eta / 출력: selectedAlertType |
| Func_031 | Req_031 | WARN_ARB_MGR | SourceID 동률판정 | ETA 동률 시 sourceId 오름차순 | 입력: sourceId / 출력: selectedAlertType |
| Func_032 | Req_032 | WARN_ARB_MGR | 중재결과 결정론 보장 | 동일 입력이면 동일 결과 출력 | 입력: arbitrationSnapshotId / 출력: selectedAlertLevel, selectedAlertType |
| Func_033 | Req_033 | BCM_AMBIENT_CTRL | 종료후 이전상태 복원 | 긴급 종료 후 직전 구간 상태 복원 | 입력: timeoutClear, baseZoneContext / 출력: ambientMode |
| Func_034 | Req_034 | BCM_AMBIENT_CTRL | 전환 깜빡임 완화 | 중재 전환 시 패턴 안정화 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_035 | Req_035 | BCM_AMBIENT_CTRL | 긴급 색상 정책 | 긴급 색상 팔레트 고정 적용 | 입력: selectedAlertType / 출력: ambientColor |
| Func_036 | Req_036 | BCM_AMBIENT_CTRL | 긴급 패턴 정책 | 긴급 점등 패턴 고정 적용 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_037 | Req_037 | BCM_AMBIENT_CTRL | 스쿨존 패턴 정책 | 스쿨존 패턴 고정 적용 | 입력: baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_038 | Req_038 | BCM_AMBIENT_CTRL | 고속도로 패턴 정책 | 고속 경고 패턴 고정 적용 | 입력: baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_039 | Req_039 | BCM_AMBIENT_CTRL | 유도선 패턴 정책 | 좌/우 유도 패턴 고정 적용 | 입력: navDirection, baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_040 | Req_040 | CLU_HMI_CTRL | 문구 길이 제한 | 경고 문구 길이/형식 고정 | 입력: warningTextCode / 출력: warningTextCode |
| Func_041 | Req_041 | SIL_TEST_CTRL | SIL 시나리오 실행 | CANoe SIL에서 시나리오 실행 제어 | 입력: testScenario / 출력: scenarioResult |
| Func_042 | Req_042 | SIL_TEST_CTRL | CAN+ETH 동시 검증 | CAN/Ethernet 동시 조건 검증 | 입력: testScenario / 출력: scenarioResult |
| Func_043 | Req_043 | SIL_TEST_CTRL | 판정 결과 산출 | 시나리오 Pass/Fail 판정 출력 | 입력: scenarioResult / 출력: scenarioResult |

---

## 상세 설명 및 추가 사항

- 상단 표는 공식 표준 양식의 열 구성(분류/기능명/기능설명/비고/검증)을 유지한다.
- 하단 표는 `Func/Req/노드/입출력` 기준으로 추적성을 보강한다.
- 추적 체인: `Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`.
- 옵션1 네트워크 전달 경로 고정: `입력 CAN -> 도메인 GW 정규화 -> ETH_SWITCH -> 중앙 경고코어 -> 도메인 GW -> 출력 CAN`.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.2 | 2026-02-25 | 상단 공식 표준 양식 단순화, 하단 상세 추적 표 분리 |
| 4.3 | 2026-02-25 | 옵션1 아키텍처 기준 반영. 출력 경로를 ETH 백본+도메인 GW 구조로 정합화하고 Func_013~016 입출력 정의를 실제 전달체계 기준으로 보정 |
| 4.4 | 2026-02-25 | 상단 공식표 `검증` 열의 TBD 제거. Req/Flow/Comm/Test ID를 행별로 명시해 감사 추적성을 강화 |
| 4.5 | 2026-02-28 | 기능 정의 상세 표의 입출력 변수를 0304 표준 변수명으로 정규화하고 비정의 변수(WarningCond/LastAlertId 등) 제거 |
| 4.6 | 2026-02-28 | Func_014 설명에서 비정의 객체명(`selectedAlertContext`)을 제거하고 0304 표준 변수(`navDirection`) 기준으로 정합화 |
| 4.7 | 2026-02-28 | 스쿨존 과속 정합 강화를 위해 `speedLimit/speedLimitNorm` 입력을 Func_007/Func_010과 상단 입력 표에 반영. |

# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 4.24
**Date**: 2026-03-05
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

## 작성 원칙

- 본 문서는 요구사항(01)의 What을 노드 기능(How)으로 분해한다.
- 상단 표는 표준 양식 구조만 유지하고, 상세 추적 정보는 하단 표에 분리한다.
- Panel은 테스트 자극/관측 인터페이스이며 기능 주체 ECU로 보지 않는다.
- 통합 기본요구사항 구간은 기능 ID `Func_001~Func_043`으로 요구사항 ID(`Req_001~Req_043`)와 1:1 대응한다.
- 차량 기본 기능 확장 요구(`Req_101~Req_119`)는 `Func_101~Func_119`로 별도 관리한다.
- V2 확장 요구(`Req_120~Req_124`)는 `Func_120~Func_124`로 별도 관리하며, 본 문서에서는 구현 활성 상태로 유지한다.
- 제출 전 현대/기아 및 OEM 기준 명칭으로 일괄 대체하되, 기능 ID/추적 ID는 유지한다.
- ID 규칙 SoT는 `00f_CAN_ID_Allocation_Standard.md`를 따른다.
- ECU 명칭은 Canonical(`UPPER_SNAKE_CASE`)만 사용하며, 명명 규칙 본문은 `00e/0301/04`에서만 관리한다.
- 네트워크 구현은 옵션1 아키텍처를 고정 적용한다: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 도메인 CAN`.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- `WARN_ARB_MGR`의 중재는 서비스(QoS) 우선순위 중재이며, CAN 비트 레벨 arbitration과 구분해 해석한다.
- EMS는 문서 상위 계층에서 단일 논리 단말 `EMS_ALERT`로 정의하고, 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`)은 하단 매핑표에서만 분리 관리한다.
- 본 사이클의 기능-요구 추적 범위는 `Req_001~043`, `Req_101~124`를 활성 범위로 유지한다.

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
| 출력 | 앰비언트 제어 | 구간/긴급 상태에 따른 앰비언트 출력 | ETH 백본 -> BODY_GW -> CAN 출력 | Req_008~Req_009,Req_013~Req_016,Req_033~Req_039 / Flow_007 / Comm_007 / IT_OUT_001 |
| 출력 | 클러스터 경고 | 경고 문구 및 상태 출력 | ETH 백본 -> IVI_GW -> CAN 출력 | Req_005,Req_019~Req_021,Req_026,Req_040 / Flow_008 / Comm_008 / IT_OUT_001 |
| 출력 | 경찰 알림 송신 | 경찰 긴급 알림 송신 | Ethernet UDP 송신 | Req_017 / Flow_004 / Comm_004 / IT_EMS_001 |
| 출력 | 구급 알림 송신 | 구급 긴급 알림 송신 | Ethernet UDP 송신 | Req_018 / Flow_005 / Comm_005 / IT_EMS_001 |
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
| ECU 동작 | 엔진 기본 제어 | 시동 입력 기반 엔진 상태 반영 | Vehicle Baseline | Req_101 / Func_101 / ST_BASE_PT_001 |
| ECU 동작 | 변속 기본 제어 | 기어 입력(P/R/N/D) 상태 반영 | Vehicle Baseline | Req_102 / Func_102 / ST_BASE_PT_001 |
| ECU 동작 | 가속 기본 제어 | 가속 입력 상태 반영 | Vehicle Baseline | Req_103 / Func_103 / ST_BASE_CH_001 |
| ECU 동작 | 제동 기본 제어 | 브레이크 입력 상태 반영 | Vehicle Baseline | Req_104 / Func_104 / ST_BASE_CH_001 |
| ECU 동작 | 조향 기본 제어 | 조향 입력 상태 반영 | Vehicle Baseline | Req_105 / Func_105 / ST_BASE_CH_001 |
| ECU 동작 | 비상등 기본 제어 | 비상등 On/Off 상태 반영 | Vehicle Baseline | Req_106 / Func_106 / ST_BASE_BODY_001 |
| ECU 동작 | 창문 기본 제어 | 창문 개폐 상태 반영 | Vehicle Baseline | Req_107 / Func_107 / ST_BASE_BODY_001 |
| ECU 동작 | 운전자 상태 입력 처리 | 운전자 상태 입력 전달 | Vehicle Baseline | Req_108 / Func_108 / ST_BASE_BODY_001 |
| ECU 동작 | 클러스터 기본 표시 | 속도/기어/경고 기본 표시 반영 | Vehicle Baseline | Req_109 / Func_109 / ST_BASE_IVI_001 |
| ECU 동작 | 도메인 게이트웨이 전달 | 도메인 경계 기반 메시지 전달 | Vehicle Baseline | Req_110 / Func_110 / IT_BASE_GW_001 |
| ECU 동작 | 도메인 경계 유지 | 도메인 통신 경계/정책 유지 | Vehicle Baseline | Req_111 / Func_111 / IT_BASE_GW_001 |
| ECU 동작 | 차량 기본 기능 SIL 검증 | 기본 기능 시나리오 실행/판정 | Vehicle Baseline | Req_112 / Func_112 / ST_BASE_DIAG_001 |
| ECU 동작 | 공조 상태 반영 | HVAC 상태/제어 신호 반영 | Vehicle Baseline | Req_113 / Func_113 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 시트 상태 반영 | 시트 상태/제어 신호 반영 | Vehicle Baseline | Req_114 / Func_114 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 미러 상태 반영 | 미러 상태 신호 반영 | Vehicle Baseline | Req_115 / Func_115 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 도어 제어 상태 반영 | 도어 제어/잠금/열림 상태 반영 | Vehicle Baseline | Req_116 / Func_116 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 와이퍼/우적 연동 반영 | 와이퍼/우적/오토라이트 상태 반영 | Vehicle Baseline | Req_117 / Func_117 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 보안 상태 반영 | 이모빌라이저/경보 상태 반영 | Vehicle Baseline | Req_118 / Func_118 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 오디오 상태 반영 | Audio Focus/Voice/TTS 상태 반영 | Vehicle Baseline | Req_119 / Func_119 / IT_BASE_EXT_IVI_001 |
| ECU 동작 | 긴급차량 근접 위험 판단 | 긴급차량 방향/ETA/자차속도 결합 기반 위험도 산정 | V2 확장(Implemented) | Req_120 / Flow_120 / Comm_120 / ST_V2_RISK_001 |
| ECU 동작 | 위험도 기반 감속 보조 요청 | 위험도 임계 초과 시 감속 보조 요청 생성 | V2 확장(Implemented) | Req_121 / Flow_121 / Comm_121 / ST_V2_RISK_001 |
| ECU 동작 | 감속 보조-경고 동기화 | 감속 보조 활성 시 긴급 경고 최우선 + Ambient/Cluster 동기화 | V2 확장(Implemented) | Req_122 / Flow_122 / Comm_122 / ST_V2_RISK_001 |
| ECU 동작 | 운전자 개입 우선 해제 | 제동/조향 회피 입력 시 감속 보조 요청 즉시 해제 | V2 확장(Implemented) | Req_123 / Flow_123 / Comm_123 / ST_V2_RISK_001 |
| ECU 동작 | 도메인 경로 단절 강등(Fail-safe) | 도메인 경로 단절 시 자동 감속 보조 금지 + 최소 경고 채널 유지 | V2 확장(Implemented) | Req_124 / Flow_124 / Comm_124 / ST_V2_FAILSAFE_001 |

---

## 기능 정의 상세 표 (추적성/노드/입출력 정의)
| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_001 | Req_001 | ADAS_WARN_CTRL | 주행 시 경고 시스템 활성 | 주행 상태에서 경고 시스템 활성화 | 입력: vehicleSpeedNorm, driveStateNorm / 출력: warningState |
| Func_002 | Req_002 | ADAS_WARN_CTRL | 비주행 경고 억제 | 정차/비주행 상태에서 경고 출력 억제 | 입력: driveStateNorm / 출력: warningState |
| Func_003 | Req_003 | ADAS_WARN_CTRL | 경고 시작 트리거 | 경고 조건 성립 시 시스템 출력 시작 | 입력: baseZoneContext, warningState / 출력: warningState |
| Func_004 | Req_004 | ADAS_WARN_CTRL | 경고 종료 트리거 | 해제 조건 성립 시 시스템 출력 종료 | 입력: warningState / 출력: warningState |
| Func_005 | Req_005 | CLU_HMI_CTRL | 경고 원인 전달 | 경고 원인 텍스트 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_006 | Req_006 | ADAS_WARN_CTRL | 반복 경고 디바운스 | 동일 조건 경고의 재출력 간격을 관리해 중복 표시를 억제 | 입력: warningState / 출력: warningState |
| Func_007 | Req_007 | NAV_CONTEXT_MGR | 구간값 변경 반영 | roadZone/speedLimit 변경 시 구간 상태 갱신 | 입력: roadZone, navDirection, zoneDistance, speedLimit / 출력: baseZoneContext, speedLimitNorm |
| Func_008 | Req_008 | BCM_AMBIENT_CTRL | 일반구간 정책 적용 | 일반 구간 기본 패턴 적용 | 입력: selectedAlertLevel / 출력: ambientMode |
| Func_009 | Req_009 | BCM_AMBIENT_CTRL | 스쿨존 강화 경고 | 스쿨존 전용 강화 패턴 적용 | 입력: selectedAlertLevel / 출력: ambientMode |
| Func_010 | Req_010 | ADAS_WARN_CTRL | 스쿨존 과속 경고 | 스쿨존 속도 초과 이벤트 판정 | 입력: vehicleSpeedNorm, speedLimitNorm, baseZoneContext / 출력: warningState |
| Func_011 | Req_011 | ADAS_WARN_CTRL | 고속 장시간 무조향 감지 | 고속 구간 무조향 타이머 경고 | 입력: steeringInputNorm, baseZoneContext / 출력: warningState |
| Func_012 | Req_012 | ADAS_WARN_CTRL | 무조향 경고 해제 | 고속도로 주의 경고 활성 상태에서 조향 입력 검출 시 경고 해제 | 입력: steeringInputNorm / 출력: warningState |
| Func_013 | Req_013 | BCM_AMBIENT_CTRL | 유도구간 진입 전환 | 유도구간 진입 시 방향안내 모드 전환 | 입력: selectedAlertType, navDirection / 출력: ambientMode |
| Func_014 | Req_014 | BCM_AMBIENT_CTRL | 좌우 방향 구분 표시 | navDirection 기준 좌/우 패턴 분기 | 입력: navDirection / 출력: ambientPattern |
| Func_015 | Req_015 | BCM_AMBIENT_CTRL | 구간 전환 완화 | 전환 중 점멸 튐 현상 완화 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_016 | Req_016 | BCM_AMBIENT_CTRL | 구간경고 종료 복귀 | 조건 해제 시 기본 구간 패턴 복귀 | 입력: timeoutClear / 출력: ambientMode |
| Func_017 | Req_017 | EMS_ALERT | 경찰 접근 경고 송신 | 경찰 긴급 ACTIVE 알림 송신 | 출력: emergencyType, emergencyDirection, eta, sourceId, alertState / ETH_EmergencyAlert |
| Func_018 | Req_018 | EMS_ALERT | 구급 접근 경고 송신 | 구급 긴급 ACTIVE 알림 송신 | 출력: emergencyType, emergencyDirection, eta, sourceId, alertState / ETH_EmergencyAlert |
| Func_019 | Req_019 | CLU_HMI_CTRL | 긴급차량 종류 표시 | 경찰/구급 타입 구분 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_020 | Req_020 | CLU_HMI_CTRL | 긴급차량 방향 표시 | 접근 방향 정보 표시 | 입력: emergencyDirection / 출력: warningTextCode |
| Func_021 | Req_021 | CLU_HMI_CTRL | 양보 유도 메시지 | 양보 요청 고정 메시지 표시 | 입력: selectedAlertType / 출력: warningTextCode |
| Func_022 | Req_022 | WARN_ARB_MGR | 긴급경고 우선 출력 | 비긴급 경고(구간/안내형)보다 긴급 경고 우선 적용 | 입력: emergencyContext, warningState, baseZoneContext / 출력: selectedAlertLevel, selectedAlertType |
| Func_023 | Req_023 | EMS_ALERT | 종료 신호 처리 | CLEAR 수신 시 긴급경고 종료 | 입력: alertState, emergencyType / 출력: emergencyContext |
| Func_024 | Req_024 | EMS_ALERT | 타임아웃 보호해제 | 긴급 신호가 1000ms 이상 미갱신되면 안전 해제 | 입력: lastEmergencyRxMs / 출력: timeoutClear |
| Func_025 | Req_025 | WARN_ARB_MGR | 다중긴급 단일선택 | 동시 긴급 신호 중 1개만 선택해 표시 | 입력: emergencyContext / 출력: selectedAlertType |
| Func_026 | Req_026 | CLU_HMI_CTRL | 중복 팝업 억제 | 동일 긴급 이벤트 중복 팝업 억제 | 입력: selectedAlertType, duplicatePopupGuard / 출력: warningTextCode |
| Func_027 | Req_027 | WARN_ARB_MGR | 충돌중재 적용 | 구간 경고/긴급 경고 동시 유효 시 중재 규칙 적용 | 입력: emergencyContext, warningState / 출력: selectedAlertLevel |
| Func_028 | Req_028 | WARN_ARB_MGR | 긴급>구간 우선 적용 | 긴급 시 구간 패턴 오버라이드 | 입력: emergencyContext / 출력: selectedAlertLevel |
| Func_029 | Req_029 | WARN_ARB_MGR | 구급>경찰 우선 적용 | emergencyType 우선순위 적용 | 입력: emergencyType / 출력: selectedAlertType |
| Func_030 | Req_030 | WARN_ARB_MGR | ETA 우선 적용 | 동급 알림이면 ETA 최소값 선택 | 입력: eta / 출력: selectedAlertType |
| Func_031 | Req_031 | WARN_ARB_MGR | SourceID 동률판정 | ETA 동률 시 sourceId 오름차순 | 입력: sourceId / 출력: selectedAlertType |
| Func_032 | Req_032 | WARN_ARB_MGR | 중재결과 결정론 보장 | 동일 입력이면 동일 결과 출력 | 입력: arbitrationSnapshotId / 출력: selectedAlertLevel, selectedAlertType |
| Func_033 | Req_033 | BCM_AMBIENT_CTRL | 종료후 이전상태 복원 | 긴급 종료 후 직전 구간 상태 복원 | 입력: timeoutClear, baseZoneContext / 출력: ambientMode |
| Func_034 | Req_034 | BCM_AMBIENT_CTRL | 전환 깜빡임 완화 | 구간 경고에서 긴급 경고 전환 시 표시 안정화(점멸/소실 방지) 제어 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_035 | Req_035 | BCM_AMBIENT_CTRL | 긴급 색상 정책 | 긴급 색상 팔레트 고정 적용 | 입력: selectedAlertType / 출력: ambientColor |
| Func_036 | Req_036 | BCM_AMBIENT_CTRL | 긴급 패턴 정책 | 긴급 점등 패턴 고정 적용 | 입력: selectedAlertLevel / 출력: ambientPattern |
| Func_037 | Req_037 | BCM_AMBIENT_CTRL | 스쿨존 패턴 정책 | 스쿨존 패턴 고정 적용 | 입력: baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_038 | Req_038 | BCM_AMBIENT_CTRL | 고속도로 패턴 정책 | 고속 경고 패턴 고정 적용 | 입력: baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_039 | Req_039 | BCM_AMBIENT_CTRL | 유도선 패턴 정책 | 좌/우 유도 패턴 고정 적용 | 입력: navDirection, baseZoneContext / 출력: ambientColor, ambientPattern |
| Func_040 | Req_040 | CLU_HMI_CTRL | 문구 길이 제한 | 경고 문구 길이/형식 고정 | 입력: warningTextCode / 출력: warningTextCode |
| Func_041 | Req_041 | VAL_SCENARIO_CTRL | SIL 시나리오 실행 | CANoe SIL에서 시나리오 실행 제어 | 입력: testScenario / 출력: scenarioResult |
| Func_042 | Req_042 | VAL_SCENARIO_CTRL | CAN+ETH 동시 검증 | CAN/Ethernet 동시 조건 검증 | 입력: testScenario / 출력: scenarioResult |
| Func_043 | Req_043 | VAL_SCENARIO_CTRL | 판정 결과 산출 | 시나리오 Pass/Fail 판정 출력 | 입력: scenarioResult / 출력: scenarioResult |

---

## 차량 기본 기능 확장 상세 표 (Phase-1)

| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_101 | Req_101 | ENGINE_CTRL | 시동 상태 반영 | 시동 On/Off 입력을 차량 기본 동작 상태로 반영 | 입력: IgnitionState / 출력: EngineState |
| Func_102 | Req_102 | TRANSMISSION_CTRL | 기어 상태 반영 | P/R/N/D 기어 입력을 상태값으로 유지/전달 | 입력: GearInput / 출력: GearState |
| Func_103 | Req_103 | ACCEL_CTRL | 가속 입력 반영 | 가속 페달 입력을 종방향 제어 입력으로 전달 | 입력: AccelPedal / 출력: AccelRequest |
| Func_104 | Req_104 | BRAKE_CTRL | 제동 입력 반영 | 브레이크 페달 입력을 감속 제어 입력으로 전달 | 입력: BrakePedal / 출력: BrakePressure |
| Func_105 | Req_105 | STEERING_CTRL | 조향 입력 반영 | 조향 입력을 차량 상태/주의 판단 입력으로 전달 | 입력: steeringInput / 출력: SteeringState |
| Func_106 | Req_106 | HAZARD_CTRL | 비상등 기본 제어 | 비상등 On/Off 입력을 상태 출력으로 반영 | 입력: HazardSwitch / 출력: HazardState |
| Func_107 | Req_107 | WINDOW_CTRL | 창문 기본 제어 | 창문 개폐 입력을 창문 상태로 반영 | 입력: WindowCommand / 출력: WindowState |
| Func_108 | Req_108 | DRIVER_STATE_CTRL | 운전자 상태 반영 | 운전자 상태 입력(예: 졸음 단계)을 관련 도메인으로 전달 | 입력: DriverStateLevel / 출력: DriverStateInfo |
| Func_109 | Req_109 | CLUSTER_BASE_CTRL | 클러스터 기본 표시 | 속도/기어/경고 기본 상태를 클러스터에 표시 | 입력: ClusterSpeed, ClusterGear, warningTextCode / 출력: ClusterStatus |
| Func_110 | Req_110 | DOMAIN_GW_ROUTER | 도메인 게이트웨이 전달 | 도메인 간 입력/출력 메시지 라우팅 수행 | 입력: RoutingPolicy / 출력: BodyGatewayRoute |
| Func_111 | Req_111 | DOMAIN_BOUNDARY_MGR | 도메인 경계 유지 | 도메인별 통신 경계/역할 분리를 유지 | 입력: RoutingPolicy / 출력: BoundaryStatus |
| Func_112 | Req_112 | VAL_BASELINE_CTRL | 차량 기본 기능 SIL 검증 | 기본 차량 기능 시나리오 실행 및 판정 | 입력: BaseScenarioId / 출력: BaseScenarioResult |
| Func_113 | Req_113 | BODY_GW | 공조 상태 반영 | 공조 상태/제어 프레임(HVAC) 수신 정보를 도메인 정책에 반영 | 입력: CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode / 출력: CabinTemp |
| Func_114 | Req_114 | DRIVER_STATE_CTRL | 시트 상태 반영 | 시트 상태/제어 프레임 수신 정보를 상태 관리에 반영 | 입력: DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel / 출력: DriverStateInfo |
| Func_115 | Req_115 | WINDOW_CTRL | 미러 상태 반영 | 미러 상태 프레임(폴딩/열선/조정) 정보를 차량 상태에 반영 | 입력: MirrorFoldState, MirrorHeatState, MirrorAdjAxis / 출력: WindowState |
| Func_116 | Req_116 | WINDOW_CTRL | 도어 제어 상태 반영 | 도어 제어/잠금/열림 상태를 수신/반영/전달 | 입력: DoorUnlockCmd, DoorLockState, DoorOpenWarn / 출력: DoorStateMask |
| Func_117 | Req_117 | BCM_AMBIENT_CTRL | 와이퍼/우적 연동 반영 | 와이퍼/우적/오토라이트 상태를 연동 정책에 반영 | 입력: FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq / 출력: WiperInterval |
| Func_118 | Req_118 | DRIVER_STATE_CTRL | 보안 상태 반영 | 이모빌라이저/경보 상태를 보안 상태로 반영 | 입력: ImmoState, AlarmArmed, AlarmTrigger, AlarmZone / 출력: DriverStateInfo |
| Func_119 | Req_119 | CLU_HMI_CTRL | 오디오 상태 반영 | 오디오 포커스/음성비서/TTS 상태를 HMI 정책에 반영 | 입력: AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId / 출력: warningTextCode |

---

## V2 확장 기능 상세 표 (Implemented, Phase-2)

| Func ID | Req ID | 실제 노드명 | 기능명 | 기능 설명 | 실제값 정의(입력/출력) |
|---|---|---|---|---|---|
| Func_120 | Req_120 | ADAS_WARN_CTRL | 긴급차량 근접 위험 판단 | 긴급차량 방향/ETA/자차속도 결합 기반 근접 위험도 산정 | 입력: emergencyDirection, eta, vehicleSpeedNorm / 출력: proximityRiskLevel |
| Func_121 | Req_121 | WARN_ARB_MGR | 위험도 기반 감속 보조 요청 | 위험도 임계 초과 시 감속 보조 요청 생성 | 입력: proximityRiskLevel, failSafeMode, driveStateNorm / 출력: decelAssistReq |
| Func_122 | Req_122 | WARN_ARB_MGR | 감속 보조-경고 동기화 | 감속 보조 요청 활성 시 긴급 경고 최우선 유지 및 Ambient/Cluster 출력 동기화 | 입력: decelAssistReq, selectedAlertType, selectedAlertLevel / 출력: selectedAlertType, selectedAlertLevel |
| Func_123 | Req_123 | WARN_ARB_MGR | 운전자 개입 우선 해제 | 운전자 제동/조향 회피 입력 검출 시 감속 보조 요청 해제 | 입력: steeringInputNorm, brakePedalNorm / 출력: decelAssistReq |
| Func_124 | Req_124 | DOMAIN_BOUNDARY_MGR | 도메인 경로 단절 강등(Fail-safe) | 도메인 경로 단절 감지 시 자동 감속 보조 금지 + 최소 경고 채널 유지 | 입력: domainPathStatus, e2eHealthState / 출력: decelAssistReq, failSafeMode |

---

## 상세 설명 및 추가 사항

- 상단 표는 공식 표준 양식의 열 구성(분류/기능명/기능설명/비고/검증)을 유지한다.
- 하단 표는 `Func/Req/노드/입출력` 기준으로 추적성을 보강한다.
- 추적 체인: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`.
- 옵션1 네트워크 전달 경로 고정: `입력 CAN -> 도메인 GW 정규화 -> ETH_SWITCH -> 중앙 경고코어 -> 도메인 GW -> 출력 CAN`.
- `Func_101~Func_119`는 차량 기본 기능 확장 체인으로, 0302/0303/0304의 Flow/Comm/Var와 최신 도메인 DBC 기준으로 동기화되어야 한다.
- `Func_120~Func_124`는 V2 확장 활성 체인으로 관리하며, 코드/DBC/05/06/07 변경을 동일 커밋 단위로 동기화한다.

## EMS 논리 단말-내부 모듈 매핑

| 논리 단말(문서 표준) | 내부 구현 모듈(코드/통신) | 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 알림 송신 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 알림 송신 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 알림 수신/해제/타임아웃 처리 |

## 차량 ECU 인벤토리 (03 기준 요약)

| 도메인 | ECU |
|---|---|
| Powertrain | ENGINE_CTRL, TRANSMISSION_CTRL |
| Chassis | ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL, EMS_ALERT, WARN_ARB_MGR, VAL_SCENARIO_CTRL |
| Body | BCM_AMBIENT_CTRL, HAZARD_CTRL, WINDOW_CTRL, DRIVER_STATE_CTRL |
| Infotainment | NAV_CONTEXT_MGR, CLU_HMI_CTRL, CLUSTER_BASE_CTRL |
| Gateway/Infra | CHASSIS_GW, INFOTAINMENT_GW, BODY_GW, IVI_GW, ETH_SWITCH, DOMAIN_GW_ROUTER, DOMAIN_BOUNDARY_MGR |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.24 | 2026-03-05 | ECU 명칭 관리 경계를 정리해 03 문서에서는 Canonical 표기만 유지하고, 명명 규칙 본문 관리 위치를 `00e/0301/04`로 고정. |
| 4.23 | 2026-03-05 | Validation Harness 노드 명칭을 `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`로 정리해 Req_041~043, Req_112 추적 표기 일관성을 강화. |
| 4.22 | 2026-03-03 | 중간감사 대응 보강: 추적 체인을 `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`로 통일하고, Vehicle Baseline `Req_101~Req_112` 검증 ID를 도메인 단위(`ST_BASE_PT/CH/BODY/IVI`, `IT_BASE_GW`, `ST_BASE_DIAG`)로 세분화. |
| 4.21 | 2026-03-03 | `Func_121/Func_123` 소유 노드를 `WARN_ARB_MGR`로 정정하고 V2 확장(`Func_120~124`) 상태를 Implemented로 전환. Chassis 인벤토리에서 미구현 `DECEL_ASSIST_CTRL` 제거. |
| 4.20 | 2026-03-02 | 감사 정합 보강: 통합구간 1:1 문구 명확화, 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구 추가, V2 확장 행 검증 컬럼을 ST/Flow/Comm ID 기준으로 구체화. |
| 4.19 | 2026-03-02 | V2 확장 제어 책임 분리: `Func_121/Func_123` 실제 노드를 `DECEL_ASSIST_CTRL`로 조정하고 Chassis ECU 인벤토리에 반영. |
| 4.18 | 2026-03-02 | V2 확장 요구 반영: `Func_120~Func_124`(근접위험/감속보조/동기화/운전자개입해제/도메인단절강등) 추가, 작성 원칙의 활성/Pre-Activation 범위 분리, 상단 공식표 확장 항목 반영. |
| 4.17 | 2026-03-02 | 03-하위문서 최종 동기화 준비 반영: `Func_101~Func_119` 설명을 병렬 반영 문구에서 최신 DBC 동기화 운영 문구로 정리. |
| 4.16 | 2026-03-02 | Vehicle Baseline 상단 `검증` 참조 ID 정합화: `Req_113~Req_118`는 `IT_BASE_EXT_BODY_001`, `Req_119`는 `IT_BASE_EXT_IVI_001`로 연결 보정. |
| 4.15 | 2026-03-02 | 본 사이클 추적 범위 고정(`Req_001~043`,`Req_101~119`) 원칙을 작성 원칙에 명시. |
| 4.14 | 2026-03-02 | 0304 변수 계약명 정합화: `Func_101~Func_119` 입력/출력명을 0304 표준 Name 기준으로 보정(`AcCompressorReq`, `DoorUnlockCmd`, `ImmoState`, `TtsLangId` 등)하고 Domain/Test 변수명 불일치(`domainInputFrames`, `baseTestScenario`)를 제거. |
| 4.13 | 2026-03-02 | V2 추적 밀도 보강 1차: 차량 기본 기능 확장 `Func_113~Func_119`(HVAC/Seat/Mirror/Door/Wiper-Rain/Security/Audio) 추가 및 `Req_113~Req_119` 1:1 매핑 반영. |
| 4.12 | 2026-03-01 | 표현 명확화 반영: Func_001/003/004/006/012/022/024/025/027/034 문구를 고객 관점 요구(Req_012/022/024/025/027/034)와 정합되도록 보정. |
| 4.2 | 2026-02-25 | 상단 공식 표준 양식 단순화, 하단 상세 추적 표 분리 |
| 4.3 | 2026-02-25 | 옵션1 아키텍처 기준 반영. 출력 경로를 ETH 백본+도메인 GW 구조로 정합화하고 Func_013~016 입출력 정의를 실제 전달체계 기준으로 보정 |
| 4.4 | 2026-02-25 | 상단 공식표 `검증` 열의 TBD 제거. Req/Flow/Comm/Test ID를 행별로 명시해 감사 추적성을 강화 |
| 4.5 | 2026-02-28 | 기능 정의 상세 표의 입출력 변수를 0304 표준 변수명으로 정규화하고 비정의 변수(WarningCond/LastAlertId 등) 제거 |
| 4.6 | 2026-02-28 | Func_014 설명에서 비정의 객체명(`selectedAlertContext`)을 제거하고 0304 표준 변수(`navDirection`) 기준으로 정합화 |
| 4.7 | 2026-02-28 | 스쿨존 과속 정합 강화를 위해 `speedLimit/speedLimitNorm` 입력을 Func_007/Func_010과 상단 입력 표에 반영. |
| 4.8 | 2026-02-28 | 차량 기본 기능 확장 대응으로 `Func_101~Func_112`(시동/기어/페달/창문/비상등/도메인경계 등) 상세 표를 추가. |
| 4.9 | 2026-02-28 | 상단 공식표에 Vehicle Baseline ECU 동작 행을 추가하고, 03 기준 차량 ECU 인벤토리 요약 표를 신설. |
| 4.10 | 2026-02-28 | 06/07 Lean IT 체계와 정합화: 상단 `검증`의 구 IT ID를 `IT_OUT_001`, `IT_EMS_001`로 갱신하고 서비스 중재/CAN 중재 경계 문구를 작성 원칙에 추가. |
| 4.11 | 2026-03-01 | 멘토 피드백 반영: EMS를 상위 문서에서 단일 논리 단말(`EMS_ALERT`)로 통합 표기하고, 내부 TX/RX 모듈 분리는 하단 매핑표로 분리. |

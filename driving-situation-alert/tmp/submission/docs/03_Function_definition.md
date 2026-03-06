# 기능 정의서 (Function Definition)

**Document ID**: PROJ-03-FD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 4.31
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 요구사항(01)의 What을 노드 기능(How)으로 분해한다.
- 상단 표는 표준 양식 구조만 유지하고, 상세 추적 정보는 하단 표에 분리한다.
- Panel은 테스트 자극/관측 인터페이스이며 기능 주체 ECU로 보지 않는다.
- 통합 기본요구사항 구간은 기능 ID `Func_001~Func_043`을 기준으로 요구사항 ID(`Req_001~Req_043`)와 누락 없는 추적 커버리지(N:M 허용)를 유지한다.
- 차량 기본 기능 확장 요구(`Req_101~Req_107`, `Req_109~Req_119`)는 `Func_101~Func_107`, `Func_109~Func_119`로 별도 관리한다.
- V2 확장 요구(`Req_120~Req_121`, `Req_123`, `Req_125~Req_129`)는 `Func_120~Func_121`, `Func_123`, `Func_125~Func_129`로 별도 관리하며, 본 문서에서는 구현 활성 상태로 유지한다.
- ADAS 객체 인지 확장 요구(`Req_130~Req_139`)는 `Func_130~Func_139`로 별도 관리하며, 본 문서에서는 Pre-Activation(설계 선반영) 상태로 유지한다.
- 차량 경보 편의 확장 요구(`Req_140~Req_147`)는 `Func_140~Func_147`로 별도 관리하며, 본 문서에서는 Pre-Activation(설계 선반영) 상태로 유지한다.
- 경고 강건성·인지성 확장 요구(`Req_148~Req_155`)는 `Func_148~Func_155`로 별도 관리하며, 본 문서에서는 Pre-Activation(설계 선반영) 상태로 유지한다.
- 제출 전 현대/기아 및 OEM 기준 명칭으로 일괄 대체하되, 기능 ID/추적 ID는 유지한다.
- ID 규칙 SoT는 `00f_CAN_ID_Allocation_Standard.md`를 따르며, 적용 참조는 `0303_Communication_Specification.md`를 사용한다.
- ECU 명칭은 Canonical(`UPPER_SNAKE_CASE`)만 사용하며, 명명 규칙은 `00e`를 단일 SoT로 하고 본 문서는 ECU 적용 참조 문서로 유지한다.
- RTE 생성명 규칙은 `00g_RTE_Name_Mapping_Standard.md`를 SoT로 하고, 본 문서가 아닌 `04`에서 적용한다.
- 네트워크 구현은 옵션1 아키텍처를 고정 적용한다: `ETH_SW + CHS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 도메인 CAN`.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- `WARN_ARB_MGR`의 기능은 경보 우선순위 판정이며, CAN 비트 레벨 arbitration과 구분해 해석한다.
- EMS는 문서 상위 계층에서 단일 논리 단말 `EMS_ALERT`로 정의하고, 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`)은 하단 매핑표에서만 분리 관리한다.
- 약어 충돌 방지 규칙: `EMS_AMB_TX`의 `AMB`는 `Ambulance` 의미의 구현 literal이며, `Ambient`는 항상 `AMBIENT` 풀토큰으로 표기한다.
- 본 사이클의 기능-요구 추적 범위는 `Req_001~043`, `Req_101~107`, `Req_109~121`, `Req_123`, `Req_125~129`를 활성 범위로 유지하고, `Req_130~Req_155`는 확장 요구(Pre-Activation) 범위로 관리한다.
- `Req_108`은 Legacy 참조 요구로 관리하며 `Req_113/Req_116/Req_118` 통합 결과를 상속 추적한다.

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
| 입력 | 구급 긴급 활성 | 구급 긴급 활성 상태 입력 | Switch/Indicator ON/OFF | Req_017 / Flow_005 / Comm_005 / ST_EMS_002 |
| 입력 | 구급 ETA | 구급 도달예상시간 입력 | TrackBar로 값 조절 | Req_030 / Flow_006 / Comm_006 / ST_ARB_ETA_002 |
| 입력 | 구급 방향 | 구급 접근 방향 입력 | Switch/Indicator로 방향 선택 | Req_020 / Flow_006 / Comm_006 / ST_HMI_DIR_002 |
| 입력 | 시나리오 선택 | 테스트 시나리오 선택 입력 | 테스트 패널 선택 | Req_041 / Flow_009 / Comm_009 / ST_SIL_001 |
| 출력 | 앰비언트 제어 | 구간/긴급 상태에 따른 앰비언트 출력 | ETH 백본 -> BODY_GW -> CAN 출력 | Req_008~Req_009,Req_013~Req_016,Req_033,Req_034,Req_035,Req_037 / Flow_007 / Comm_007 / IT_OUT_001 |
| 출력 | 클러스터 경고 | 경고 문구 및 상태 출력 | ETH 백본 -> IVI_GW -> CAN 출력 | Req_005,Req_019~Req_021,Req_026,Req_040 / Flow_008 / Comm_008 / IT_OUT_001 |
| 출력 | 경찰 알림 송신 | 경찰 긴급 알림 송신 | Ethernet UDP 송신 | Req_017 / Flow_004 / Comm_004 / IT_EMS_001 |
| 출력 | 구급 알림 송신 | 구급 긴급 알림 송신 | Ethernet UDP 송신 | Req_017 / Flow_005 / Comm_005 / IT_EMS_001 |
| 출력 | 판정 결과 | 시나리오 판정 결과 출력 | 로그/패널 출력 | Req_043 / Flow_009 / Comm_009 / ST_RESULT_001 |
| ECU 동작 | 구간 컨텍스트 관리 | 구간/제한속도 입력을 바탕으로 컨텍스트 갱신 | 상태 업데이트 | Req_007,Req_010 / Flow_003 / Comm_003 / UT_NAV_001 |
| ECU 동작 | 경고 조건 판정 | 속도/조향/제한속도 기반 경고 조건 판정 | 경고 트리거 생성 | Req_001~Req_004,Req_006,Req_010~Req_012 / Flow_001,Flow_002,Flow_003 / Comm_001,Comm_002,Comm_003 / UT_ADAS_001 |
| ECU 동작 | 경찰 알림 송신 제어 | 경찰 알림 송신 주기 관리 | 송신 상태 관리 | Req_017 / Flow_004 / Comm_004 / UT_EMS_POL_001 |
| ECU 동작 | 구급 알림 송신 제어 | 구급 알림 송신 주기 관리 | 송신 상태 관리 | Req_017 / Flow_005 / Comm_005 / UT_EMS_AMB_001 |
| ECU 동작 | 긴급 알림 수신 처리 | 긴급 알림 수신/해제 처리 | 타임아웃 처리 | Req_023,Req_024 / Flow_006 / Comm_006 / UT_EMS_RX_001 |
| ECU 동작 | 경보 우선순위 판정 | 긴급/구간 충돌 시 우선순위 결정 | 중재 결과 산출 | Req_022,Req_025~Req_032 / Flow_006 / Comm_006 / UT_ARB_001 |
| ECU 동작 | 앰비언트 제어 | 경고 패턴/색상 적용 | 패턴 결정 | Req_008,Req_009,Req_013~Req_016,Req_033,Req_034,Req_035,Req_037 / Flow_007 / Comm_007 / UT_BCM_001 |
| ECU 동작 | 클러스터 표시 | 경고 문구/유형 표시 | 문구 결정 | Req_005,Req_019~Req_021,Req_026,Req_040 / Flow_008 / Comm_008 / UT_CLU_001 |
| ECU 동작 | 테스트 실행/판정 | 테스트 시나리오 실행 및 판정 | Pass/Fail 기록 | Req_041~Req_043 / Flow_009 / Comm_009 / ST_SIL_002 |
| ECU 동작 | 엔진 기본 제어 | 시동 입력 기반 엔진 상태 반영 | Vehicle Baseline | Req_101 / Func_101 / ST_BASE_PT_001 |
| ECU 동작 | 변속 기본 제어 | 기어 입력(P/R/N/D) 상태 반영 | Vehicle Baseline | Req_102 / Func_102 / ST_BASE_PT_001 |
| ECU 동작 | 가속 기본 제어 | 가속 입력 상태 반영 | Vehicle Baseline | Req_103 / Func_103 / ST_BASE_CH_001 |
| ECU 동작 | 제동 기본 제어 | 브레이크 입력 상태 반영 | Vehicle Baseline | Req_104 / Func_104 / ST_BASE_CH_001 |
| ECU 동작 | 조향 기본 제어 | 조향 입력 상태 반영 | Vehicle Baseline | Req_105 / Func_105 / ST_BASE_CH_001 |
| ECU 동작 | 비상등 기본 제어 | 비상등 On/Off 상태 반영 | Vehicle Baseline | Req_106 / Func_106 / ST_BASE_BODY_001 |
| ECU 동작 | 창문 기본 제어 | 창문 개폐 상태 반영 | Vehicle Baseline | Req_107 / Func_107 / ST_BASE_BODY_001 |
| ECU 동작 | 클러스터 기본 표시 | 속도/기어/경고 기본 표시 반영 | Vehicle Baseline | Req_109 / Func_109 / ST_BASE_IVI_001 |
| ECU 동작 | 도메인 게이트웨이 전달 | 도메인 경계 기반 메시지 전달 | Vehicle Baseline | Req_110 / Func_110 / IT_BASE_GW_001 |
| ECU 동작 | 도메인 경계 유지 | 도메인 통신 경계/정책 유지 | Vehicle Baseline | Req_111 / Func_111 / IT_BASE_GW_001 |
| ECU 동작 | 차량 기본 기능 SIL 검증 | 기본 기능 시나리오 실행/판정 | Vehicle Baseline | Req_112 / Func_112 / ST_BASE_DIAG_001 |
| ECU 동작 | 공조 상태 반영 | HVAC 상태/제어 신호 반영 | Vehicle Baseline | Req_113 / Func_113 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 시트 상태 반영 | 시트 상태/제어 신호 반영 | Vehicle Baseline | Req_113 / Func_114 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 미러 상태 반영 | 미러 상태 신호 반영 | Vehicle Baseline | Req_113 / Func_115 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 도어 제어 상태 반영 | 도어 제어/잠금/열림 상태 반영 | Vehicle Baseline | Req_116 / Func_116 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 와이퍼/우적 연동 반영 | 와이퍼/우적/오토라이트 상태 반영 | Vehicle Baseline | Req_116 / Func_117 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 보안 상태 반영 | 이모빌라이저/경보 상태 반영 | Vehicle Baseline | Req_118 / Func_118 / IT_BASE_EXT_BODY_001 |
| ECU 동작 | 오디오 상태 반영 | Audio Focus/Voice/TTS 상태 반영 | Vehicle Baseline | Req_119 / Func_119 / IT_BASE_EXT_IVI_001 |
| ECU 동작 | 긴급차량 근접 위험 판단 | 긴급차량 방향/ETA/자차속도 결합 기반 위험도 산정 | V2 확장(Implemented) | Req_120 / Flow_120 / Comm_120 / ST_V2_RISK_001 |
| ECU 동작 | 위험도 기반 감속 보조 요청 | 위험도 임계 초과 시 감속 보조 요청 생성 | V2 확장(Implemented) | Req_121 / Flow_121 / Comm_121 / ST_V2_RISK_001 |
| ECU 동작 | 감속 보조 시 긴급경고 최우선 유지 | 감속 보조 활성 시 긴급 경고가 비긴급 경고보다 우선 유지 | V2 확장(Implemented) | Req_125 / Flow_122 / Comm_122 / ST_V2_RISK_001 |
| ECU 동작 | 감속 보조 시 경고 채널 동기화 | 감속 보조 활성 시 Ambient/Cluster 출력 동기화 유지 | V2 확장(Implemented) | Req_126 / Flow_122 / Comm_122 / ST_V2_RISK_001 |
| ECU 동작 | 운전자 개입 우선 해제 | 제동/조향 회피 입력 시 감속 보조 요청 즉시 해제 | V2 확장(Implemented) | Req_123 / Flow_123 / Comm_123 / ST_V2_RISK_001 |
| ECU 동작 | 도메인 단절 시 자동감속 금지 | 도메인 경로 단절 시 자동 감속 보조 요청 생성 금지 | V2 확장(Implemented) | Req_127 / Flow_124 / Comm_124 / ST_V2_FAILSAFE_001 |
| ECU 동작 | 도메인 단절 시 최소 경고 유지 | 도메인 경로 단절 시 최소 경고 채널 유지 | V2 확장(Implemented) | Req_128 / Flow_124 / Comm_124 / ST_V2_FAILSAFE_001 |
| ECU 동작 | 도메인 단절 시 안전 강등 전환 | 도메인 경로 단절 시 failSafeMode 전환 | V2 확장(Implemented) | Req_129 / Flow_124 / Comm_124 / ST_V2_FAILSAFE_001 |
| ECU 동작 | 객체 목록 수용/위험 객체 선정 | 주변 객체 목록 수신 후 대표 위험 객체를 선정 | ADAS 객체 인지 확장(Planned) | Req_130,Req_131 / Flow_130 / Comm_130 / ST_ADAS_OBJ_001 |
| ECU 동작 | TTC/상대속도 기반 위험 단계화 | TTC/상대속도/거리 기반으로 위험 단계를 산정하고 보수 유지시간을 적용 | ADAS 객체 인지 확장(Planned) | Req_132,Req_133,Req_136 / Flow_131 / Comm_131 / ST_ADAS_OBJ_001 |
| ECU 동작 | 교차로/합류 위험 경고 판정 | 교차로 측방 접근 및 합류/끼어들기 위험 경고를 생성하고 기존 경고와 정합 판정 | ADAS 객체 인지 확장(Planned) | Req_134,Req_135,Req_139 / Flow_132 / Comm_132 / ST_ADAS_OBJ_001 |
| ECU 동작 | 신뢰도 기반 강등 및 이벤트 기록 | 객체 신뢰도 저하 시 자동감속 보조 차단/강등 및 이벤트 로깅 | ADAS 객체 인지 확장(Planned) | Req_137,Req_138 / Flow_133 / Comm_133 / ST_ADAS_OBJ_001 |
| ECU 동작 | 방향지시등/안전벨트 기반 경보 맥락 반영 | 방향지시등/안전벨트 상태를 경보 맥락 및 강조 정책에 반영 | 차량 경보 편의 확장(Planned) | Req_140,Req_142 / Flow_103 / Comm_103 / ST_BASE_ALERT_EXT_001 |
| ECU 동작 | 주행모드 기반 경보 민감도 반영 | 주행 모드에 따라 경보 민감도 프로파일을 보정 | 차량 경보 편의 확장(Planned) | Req_141 / Flow_105 / Comm_105 / ST_BASE_ALERT_EXT_001 |
| ECU 동작 | 접근거리 표시/이벤트 이력 관리 | 긴급차량 접근 거리 표시와 경보 이벤트 기록·이력 조회를 제공 | 차량 경보 편의 확장(Planned) | Req_143,Req_144,Req_145 / Flow_006,Flow_008,Flow_203 / Comm_006,Comm_008,Comm_203 / ST_BASE_ALERT_EXT_001 |
| ECU 동작 | 표시 방식/음량 설정 반영 | 경보 표시 방식/음량 설정을 HMI 출력 정책에 반영 | 차량 경보 편의 확장(Planned) | Req_146,Req_147 / Flow_104,Flow_203 / Comm_104,Comm_203 / ST_BASE_ALERT_EXT_001 |
| ECU 동작 | 경고 입력 유효성/신선도 보호 | 경고 판정 입력의 유효성/신선도를 검사하고 stale·저신뢰 입력에 보수 정책을 적용 | 경고 강건성·인지성 확장(Planned) | Req_148,Req_149 / Flow_130,Flow_006,Flow_105 / Comm_130,Comm_006,Comm_105 / ST_BASE_ROBUST_EXT_001 |
| ECU 동작 | 경고 안정화/채널 가용성·대체·인지성/동기 관리 | 상태전이 안정화, 출력 채널 가용성 판정, 대체 출력 유지, 오디오 경합/팝업 과밀 제어, 채널 동기 일관성 관리 | 경고 강건성·인지성 확장(Planned) | Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 / Flow_006,Flow_007,Flow_008,Flow_104,Flow_124,Flow_203 / Comm_006,Comm_007,Comm_008,Comm_104,Comm_124,Comm_203 / ST_BASE_ROBUST_EXT_001 |

---

## 기능 상세 요약 (제출본)

- 제출본은 상단 공식 기능 정의 표를 기준으로 하단 상세표를 대표행 중심으로 축소한다.
- 전수 Func 매핑/확장 상세는 원문 SoT(`driving-situation-alert/03_Function_definition.md`)를 기준으로 관리한다.

| 분류 | 포함 범위 | 핵심 Func ID | 상태 | 비고 |
|---|---|---|---|---|
| 통합 기본 기능 | 공통 경고 판단/표시/중재 | Func_001~Func_040 | Active | Req_001~040 대응 |
| Validation Harness | SIL 실행/판정 기록 | Func_041~Func_043 | Active(Validation-only) | 양산 기능과 분리 |
| 차량 기본 기능 확장 | Baseline 입력/표시/도메인 경계 | Func_101~Func_107, Func_109, Func_113, Func_116, Func_118, Func_119 | Active | Req_101~107, 109, 113, 116, 118, 119 |
| V2 확장 | 위험도/감속 보조/Fail-safe | Func_120, Func_121, Func_123, Func_125~Func_129 | Implemented | Req_120,121,123,125~129 |
| ADAS 객체 인지 확장 | 객체 기반 위험/교차로/합류 | Func_130~Func_139 | Planned(Pre-Activation) | Req_130~139 |
| 경보 편의 확장 | 표시/음량/이벤트 기록/조회 | Func_140~Func_147 | Planned(Pre-Activation) | Req_140~147 |
| 강건성·인지성 확장 | 유효성/전이안정/대체출력 | Func_148~Func_155 | Planned(Pre-Activation) | Req_148~155 |

## Req-Func 대표 매핑 (축소본)

| Req ID | Func ID | 실제 노드명 | 기능명 |
|---|---|---|---|
| Req_001 | Func_001 | ADAS_WARN_CTRL | 주행시 경고엔진 활성 |
| Req_007 | Func_007 | NAV_CTX_MGR | 구간 컨텍스트 갱신 |
| Req_017 | Func_017, Func_018 | EMS_ALERT | 긴급차량 접근 경고 송신 |
| Req_027 | Func_027 | WARN_ARB_MGR | 충돌 중재 적용 |
| Req_035 | Func_035, Func_036 | AMBIENT_CTRL | 긴급 시각표현 정책 |
| Req_101 | Func_101 | ENG_CTRL | 시동 상태 반영 |
| Req_109 | Func_109 | CLU_BASE_CTRL | 클러스터 기본 표시 |
| Req_120 | Func_120 | ADAS_WARN_CTRL | 근접 위험도 산정 |
| Req_125 | Func_125 | WARN_ARB_MGR | 긴급경고 최우선 유지 |
| Req_130 | Func_130 | ADAS_WARN_CTRL | 객체 위험 입력 반영(Pre-Activation) |
| Req_140 | Func_140 | WARN_ARB_MGR | 방향지시등 연동 경보(Pre-Activation) |
| Req_148 | Func_148 | ADAS_WARN_CTRL | 입력 유효성/신뢰도 필터링(Pre-Activation) |

## EMS 논리 단말-내부 모듈 매핑

| 논리 단말(문서 표준) | 내부 구현 모듈(코드/통신) | 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 알림 송신 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 알림 송신 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 알림 수신/해제/타임아웃 처리 |

---

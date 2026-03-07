# 통합 테스트 (Integration Test)

**Document ID**: PROJ-06-IT
**ISO 26262 Reference**: Part 6, Cl.10 (Software Integration and Integration Test)
**ASPICE Reference**: SWE.5 (Software Integration and Integration Test)
**Version**: 4.19
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 중단 (SWE.5) | `06_Integration_Test.md` | `05_Unit_Test.md` | `07_System_Test.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 모듈 간 인터페이스/흐름(IT) 검증을 정리한다.
- 제출본은 상단 공식 IT 표를 유지하고, 하단은 핵심 체인만 유지한다.
- 전수 IT 추적은 원문 06에서 관리한다.
- 검증 환경 표기는 CANoe SIL(CAN+Ethernet, 필요 시 stub) 기준으로 유지한다.
- Pre-Activation 라벨은 원문과 동일하게 유지한다.
- 대조군/우수성 비교 실험은 제출본 범위 밖으로 두고 Pass/Fail 중심으로 제시한다.
- 검증 배치 실행/리포트 생성은 `scripts/run.py verify batch` 기준(기본 `json,md`, 옵션 `csv`)으로 운영한다.

---

## 통합 테스트 표 (공식 표준 양식)

| 테스트 ID | 요구사항 ID | VC ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|---|---|---|---|---|---|---|---|
| IT_CORE_001 | Req_001,Req_002,Req_003,Req_004,Req_005,Req_006,Req_007,Req_008,Req_009,Req_010,Req_011,Req_012 | VC_001~VC_012 | 입력 CAN(0x2A0/0x2A1/0x2A3)부터 GW 변환(0x510/0x511/0x512), 경고 코어 판정까지 핵심 경로 통합 검증 | 입력 변화 후 `150ms` 이내 warningState/zoneContext가 기대값으로 반영되고 경로 단절이 없다 |  |  |  |
| IT_EMS_001 | Req_017,Req_023 | VC_017,VC_023 | 경찰/구급 긴급 알림 송신-수신 체인(Flow_004~006) 통합 검증 | E100 Active/Clear 송수신이 일치하고 송신 주기 `100ms`가 유지되며 `150ms` 이내 중재 입력에 반영된다 |  |  |  |
| IT_ARB_001 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027~VC_032 | 긴급/구간 동시 발생 시 경고 중재 로직 통합 검증 | Emergency>Zone, Ambulance>Police, ETA, SourceID 규칙으로 단일 selectedAlert가 결정론적으로 생성된다 |  |  |  |
| IT_OUT_001 | Req_005,Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_019,Req_020,Req_021,Req_026,Req_033,Req_034,Req_035,Req_037,Req_040 | VC_005,VC_008,VC_009,VC_013~VC_016,VC_019~VC_021,VC_026,VC_033~VC_040 | 중재 결과(0xE200)에서 Ambient/Cluster 출력(0x289/0x280)까지 통합 검증 | 출력 정책(문구/색상/패턴/복귀)이 일치하고 출력 주기 `50ms`가 유지된다 |  |  |  |
| IT_TIMEOUT_001 | Req_024,Req_033,Req_034 | VC_024,VC_033,VC_034 | 긴급 미수신 타임아웃 해제 및 복귀 체인 통합 검증 | `1000ms` 무갱신 시 timeoutClear가 전환되고 `150ms` 이내 안전 복귀가 완료되며 중복 토글이 없다 |  |  |  |
| IT_V2_RISK_001 | Req_120,Req_121,Req_125,Req_126,Req_123 | VC_120,VC_121,VC_125,VC_126,VC_123 | 긴급차량 근접 위험도 기반 감속 보조 요청/경고 동기화 체인 통합 검증 | 위험도 임계 초과 시 `150ms` 이내 감속 보조 요청 생성, 활성 상태에서 Ambient/Cluster 동기 오프셋 `<=50ms`, 운전자 개입 시 `150ms` 이내 해제 (SIL Scenario 15/16/17/19) | Ready |  |  |
| IT_V2_FAILSAFE_001 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | 도메인 경로 단절 강등(Fail-safe) 체인 통합 검증 | 단절 감지 후 `150ms` 이내 failSafeMode 전환, 자동 감속 보조 0건 유지, 최소 경고 채널 유지 (SIL Scenario 18) | Ready |  |  |
| IT_ADAS_OBJ_001 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_137,Req_138,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_137,VC_138,VC_139 | 객체 목록 입력부터 TTC/상대속도 단계화, 교차로/합류 위험 경고, 신뢰도 강등 및 이벤트 기록 체인 통합 검증 | 객체 입력 반영 `100ms`, 위험 경고 반영 `150ms`, 신뢰도 저하 시 자동감속 차단/강등 `150ms`, 이벤트 기록 누락 0건 | Planned |  |  |
| IT_BASE_ALERT_EXT_001 | Req_140,Req_141,Req_142,Req_143,Req_144,Req_145,Req_146,Req_147 | VC_140,VC_141,VC_142,VC_143,VC_144,VC_145,VC_146,VC_147 | 차량 경보 편의 확장(입력 맥락 보정/접근거리 표시/이벤트 기록·조회/표시·음량 설정) 체인 통합 검증 | 입력 보정 반영 `150ms`, 접근거리 표시 갱신 `200ms`, 이벤트 기록 누락 0건, 표시·음량 설정 반영 `150ms` | Planned |  |  |
| IT_BASE_ROBUST_EXT_001 | Req_148,Req_149,Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 | VC_148,VC_149,VC_150,VC_151,VC_152,VC_153,VC_154,VC_155 | 경고 강건성·인지성 확장(입력 유효성/신선도 보호, 상태전이 안정화, 채널 가용성·대체, 오디오 경합/팝업 과밀/채널 동기 복원) 체인 통합 검증 | 유효성 필터링 `100ms`, stale/전이 안정화 `150ms`, 채널 가용성 판정·대체 출력 `150ms`, 오디오 경합/과밀 억제/동기 복원 `150ms` 기준 충족 | Planned |  |  |
| IT_SIL_001 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | CANoe SIL 실행/판정 경로(TestScenario->ScenarioResult) 통합 검증 | CAN+Ethernet(또는 CAN 대체 백본) 조건에서도 시나리오 실행/결과 기록/로그 요약이 일관되게 유지된다 |  |  |  |
| IT_BASE_001 | Req_101~Req_107,Req_109~Req_119 | VC_101~VC_107,VC_109~VC_119 | 차량 기본 기능(시동/기어/가감속/조향/비상등/창문/표시/도메인 경계 + Body/IVI 확장 상태) 통합 검증 | Flow_101~106, Flow_201~205 경로에서 기본 차량 기능 체인이 성립하고 기본 상태/표시가 일관되게 유지된다 |  |  |  |
| IT_BASE_PT_001 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | Powertrain 도메인 기본 동력/변속/상태 경로 통합 검증 | Comm_101/204/105 경로에서 엔진/변속/동력 상태가 `100ms` 주기로 일관되게 연계된다 |  |  |  |
| IT_BASE_CH_001 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | Chassis 도메인 가감속/조향/제동/차체상태 경로 통합 검증 | Comm_102/201/105 경로에서 입력/상태/헬스 연계가 `100ms` 기준으로 유지된다 |  |  |  |
| IT_BASE_BODY_001 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | Body 도메인 비상등/창문/편의상태 경로 통합 검증 | Comm_103/202/105 경로에서 차체 제어 상태와 경계 라우팅이 일관되게 유지된다 |  |  |  |
| IT_BASE_IVI_001 | Req_109,Req_111 | VC_109,VC_111 | Infotainment 도메인 기본 표시/UI/경계 연동 통합 검증 | Comm_104/203/105 경로에서 표시 상태와 연계 이벤트가 50/100ms 규칙을 만족한다 |  |  |  |
| IT_BASE_EXT_BODY_001 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | Body 확장 기능(HVAC/Seat/Mirror/Door/Wiper-Rain/Security) 통합 검증 | Comm_202/105 경로에서 확장 상태/제어 프레임이 `100ms` 주기로 연계되고 `150ms` 이내 정책 반영된다 |  |  |  |
| IT_BASE_EXT_IVI_001 | Req_119 | VC_119 | Infotainment 확장 기능(Audio Focus/Voice/TTS 상태) 통합 검증 | Comm_203/105 경로에서 오디오/음성 상태가 50/100ms 규칙을 만족하고 `150ms` 이내 HMI 정책에 반영된다 |  |  |  |
| IT_BASE_DIAG_001 | Req_112 | VC_112 | Test/Diag 결과 경로 통합 검증 | Comm_106/205(Event+100ms) 경로에서 진단 요청-응답 및 결과 기록이 누락 없이 유지된다 |  |  |  |

---

## 통합 테스트 추적 상세 표

| IT ID | 관련 Flow | 관련 Comm | 관련 Func | 관련 Req | 관련 VC | 선행 UT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| IT_CORE_001 | Flow_001,Flow_002,Flow_003 | Comm_001,Comm_002,Comm_003 | Func_001~Func_012 | Req_001,Req_002,Req_003,Req_004,Req_005,Req_006,Req_007,Req_008,Req_009,Req_010,Req_011,Req_012 | VC_001~VC_012 | UT_ADAS_001, UT_NAV_001, UT_GW_001 | 입력 `100ms` + 출력 `50ms` 기준 `150ms` 이내 반영 |
| IT_EMS_001 | Flow_004,Flow_005,Flow_006 | Comm_004,Comm_005,Comm_006 | Func_017,Func_018,Func_023 | Req_017,Req_023 | VC_017,VC_023 | UT_EMS_POL_001, UT_EMS_AMB_001, UT_EMS_RX_001 | Active/Clear 송수신 상태 일치, 송신주기 `100ms` 유지 |
| IT_ARB_001 | Flow_006 | Comm_006 | Func_022,Func_025,Func_027~Func_032 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027~VC_032 | UT_ARB_001 | 우선순위/동률 규칙 결과가 기대값과 일치 |
| IT_OUT_001 | Flow_007,Flow_008 | Comm_007,Comm_008 | Func_005,Func_008,Func_009,Func_013~Func_016,Func_019~Func_021,Func_026,Func_033~Func_040 | Req_005,Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_019,Req_020,Req_021,Req_026,Req_033,Req_034,Req_035,Req_037,Req_040 | VC_005,VC_008,VC_009,VC_013~VC_016,VC_019~VC_021,VC_026,VC_033~VC_040 | UT_BCM_001, UT_CLU_001, UT_OUT_GW_001 | Ambient/Cluster 출력이 정책표와 일치, 출력 주기 `50ms` 유지 |
| IT_TIMEOUT_001 | Flow_006,Flow_007,Flow_008 | Comm_006,Comm_007,Comm_008 | Func_024,Func_033,Func_034 | Req_024,Req_033,Req_034 | VC_024,VC_033,VC_034 | UT_EMS_RX_001, UT_BCM_001 | `1000ms` 무갱신 후 timeoutClear=1, `150ms` 이내 복귀 완료 |
| IT_V2_RISK_001 | Flow_120,Flow_121,Flow_122,Flow_123 | Comm_120,Comm_121,Comm_122,Comm_123 | Func_120,Func_121,Func_125,Func_126,Func_123 | Req_120,Req_121,Req_125,Req_126,Req_123 | VC_120,VC_121,VC_125,VC_126,VC_123 | UT_V2_RISK_001, UT_V2_RELEASE_001 | 위험도 기반 보조 요청 생성/경고 동기화/운전자 개입 해제가 수치 기준(`100ms`,`150ms`,`<=50ms`) 충족 (SIL Scenario 15/16/17/19) |
| IT_V2_FAILSAFE_001 | Flow_124 | Comm_124 | Func_127,Func_128,Func_129 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | UT_V2_FAILSAFE_001 | 경로 단절 감지 후 `150ms` 이내 강등 전환, 자동 감속 보조 0건, 최소 경고 채널 유지 (SIL Scenario 18) |
| IT_ADAS_OBJ_001 | Flow_130,Flow_131,Flow_132,Flow_133 | Comm_130,Comm_131,Comm_132,Comm_133 | Func_130,Func_131,Func_132,Func_133,Func_134,Func_135,Func_136,Func_137,Func_138,Func_139 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_137,Req_138,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_137,VC_138,VC_139 | UT_ADAS_OBJ_RISK_001, UT_ADAS_OBJ_SAFETY_001 | 객체 기반 위험 경고/강등/이벤트 체인이 수치 기준(`100ms`,`150ms`)과 정책 일관성 기준을 충족(Pre-Activation) |
| IT_BASE_ALERT_EXT_001 | Flow_103,Flow_104,Flow_105,Flow_203,Flow_006,Flow_008 | Comm_103,Comm_104,Comm_105,Comm_203,Comm_006,Comm_008 | Func_140,Func_141,Func_142,Func_143,Func_144,Func_145,Func_146,Func_147 | Req_140,Req_141,Req_142,Req_143,Req_144,Req_145,Req_146,Req_147 | VC_140,VC_141,VC_142,VC_143,VC_144,VC_145,VC_146,VC_147 | UT_BASE_ALERT_EXT_001 | 입력 맥락 보정 `150ms`, 거리 표시 `200ms`, 이벤트 기록 누락 0건, 표시/음량 설정 반영 `150ms` 기준 충족(Pre-Activation) |
| IT_BASE_ROBUST_EXT_001 | Flow_130,Flow_133,Flow_006,Flow_007,Flow_008,Flow_104,Flow_105,Flow_124,Flow_203 | Comm_130,Comm_133,Comm_006,Comm_007,Comm_008,Comm_104,Comm_105,Comm_124,Comm_203 | Func_148,Func_149,Func_150,Func_151,Func_152,Func_153,Func_154,Func_155 | Req_148,Req_149,Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 | VC_148,VC_149,VC_150,VC_151,VC_152,VC_153,VC_154,VC_155 | UT_BASE_ROBUST_EXT_001 | 입력 유효성/신선도 보호, 전이 안정화, 채널 가용성·대체, 오디오 경합·팝업 과밀·채널 동기 복원 체인이 수치 기준(`100ms`,`150ms`)을 충족(Pre-Activation) |
| IT_SIL_001 | Flow_009 | Comm_009 | Func_041,Func_042,Func_043 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | UT_SIL_001 | 시나리오 실행/결과 기록/로그 연동 완료 |
| IT_BASE_001 | Flow_101~Flow_106, Flow_201~Flow_205 | Comm_101~Comm_106, Comm_201~Comm_205 | Func_101~Func_107,Func_109~Func_119 | Req_101~Req_107,Req_109~Req_119 | VC_101~VC_107,VC_109~VC_119 | UT_BASE_001, UT_BASE_PT_001, UT_BASE_CH_001, UT_BASE_BODY_001, UT_BASE_IVI_001, UT_BASE_EXT_BODY_001, UT_BASE_EXT_IVI_001, UT_BASE_GW_001, UT_BASE_TEST_001 | 차량 기본 기능 입력/상태/표시/도메인 경계/SIL 판정 연동이 일관되게 유지 |
| IT_BASE_PT_001 | Flow_101,Flow_204,Flow_105 | Comm_101,Comm_204,Comm_105 | Func_101,Func_102,Func_110 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | UT_BASE_PT_001, UT_BASE_GW_001 | 엔진/변속/동력 상태 연계가 `100ms` 기준으로 유지 |
| IT_BASE_CH_001 | Flow_102,Flow_201,Flow_105 | Comm_102,Comm_201,Comm_105 | Func_103,Func_104,Func_105,Func_110 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | UT_BASE_CH_001, UT_BASE_GW_001 | 가감속/제동/조향/차체상태 연계가 `100ms` 기준으로 유지 |
| IT_BASE_BODY_001 | Flow_103,Flow_202,Flow_105 | Comm_103,Comm_202,Comm_105 | Func_106,Func_107,Func_111 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | UT_BASE_BODY_001, UT_BASE_GW_001 | 차체 제어/편의/상태 경로가 일관되게 유지 |
| IT_BASE_IVI_001 | Flow_104,Flow_203,Flow_105 | Comm_104,Comm_203,Comm_105 | Func_109,Func_111 | Req_109,Req_111 | VC_109,VC_111 | UT_BASE_IVI_001, UT_BASE_GW_001 | 기본 표시/UI/연계 이벤트가 50/100ms 기준으로 유지 |
| IT_BASE_EXT_BODY_001 | Flow_202,Flow_105 | Comm_202,Comm_105 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | UT_BASE_EXT_BODY_001, UT_BASE_GW_001 | HVAC/Seat/Mirror/Door/Wiper-Rain/Security 확장 상태가 `100ms` 주기로 연계되고 `150ms` 이내 반영 |
| IT_BASE_EXT_IVI_001 | Flow_203,Flow_105 | Comm_203,Comm_105 | Func_119 | Req_119 | VC_119 | UT_BASE_EXT_IVI_001, UT_BASE_GW_001 | Audio Focus/Voice/TTS 상태가 50/100ms 주기 규칙과 `150ms` 반영 기준을 만족 |
| IT_BASE_DIAG_001 | Flow_106,Flow_205 | Comm_106,Comm_205 | Func_112 | Req_112 | VC_112 | UT_BASE_TEST_001 | 진단 요청-응답 및 결과 기록이 Event+100ms 기준으로 유지 |

---

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

## 통합 테스트 대표 추적 표 (축소본)

- 제출본은 대표 IT만 유지하고, 전수 IT 추적은 원문 SoT(`driving-situation-alert/06_Integration_Test.md`)에서 관리한다.

| IT ID | Req/VC(대표) | 체인 범위 | 판정 기준(요약) | 상태 |
|---|---|---|---|---|
| IT_CORE_001 | Req_001~012 / VC_001~012 | Flow_001~003 -> Comm_001~003 | 입력->경고코어 `150ms` 반영 | Active |
| IT_EMS_001 | Req_017, Req_023 / VC_017, VC_023 | Flow_004~006 -> Comm_004~006 | 긴급 송수신/중재 입력 일치 | Active |
| IT_ARB_001 | Req_022, Req_025~032 | Flow_006 -> Comm_006 | 중재 규칙 결정론 | Active |
| IT_OUT_001 | Req_005, Req_008~009, Req_033~040 | Flow_007~008 -> Comm_007~008 | Ambient/Cluster 출력 정책 일치 | Active |
| IT_TIMEOUT_001 | Req_024, Req_033, Req_034 | Flow_006~008 -> Comm_006~008 | 1000ms timeout + 150ms 복귀 | Active |
| IT_SIL_001 | Req_041~043 | Flow_009 -> Comm_009 | SIL 실행/결과 기록 유지 | Active |
| IT_BASE_001 | Req_101~119 | Flow_101~106,201~205 | 기본 차량 체인 일관성 | Active |
| IT_V2_RISK_001 | Req_120, Req_121, Req_123, Req_125, Req_126 | Flow_120~123 -> Comm_120~123 | 위험도/보조요청/해제/동기화 | Ready |
| IT_V2_FAILSAFE_001 | Req_127~129 | Flow_124 -> Comm_124 | 경로 단절 강등/최소 채널 유지 | Ready |
| IT_ADAS_OBJ_001 | Req_130~139 | Flow_130~133 -> Comm_130~133 | 객체 위험경고/신뢰도 강등 | Planned |
| IT_BASE_ALERT_EXT_001 | Req_140~147 | Flow_103~105,203,006,008 | 경보 편의 확장 E2E | Planned |
| IT_BASE_ROBUST_EXT_001 | Req_148~155 | Flow_130,133,006~008,104~105,124,203 | 강건성/인지성 확장 E2E | Planned |

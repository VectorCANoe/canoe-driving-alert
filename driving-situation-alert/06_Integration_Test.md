# 통합 테스트 (Integration Test)

**Document ID**: PROJ-06-IT
**ISO 26262 Reference**: Part 6, Cl.10 (Software Integration and Integration Test)
**ASPICE Reference**: SWE.5 (Software Integration and Integration Test)
**Version**: 4.15
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 중단 (SWE.5) | `06_Integration_Test.md` | `05_Unit_Test.md` | `07_System_Test.md` |

---

## 작성 원칙

- 본 문서는 모듈 간 인터페이스/흐름(Flow, Comm) 연동 검증을 수행한다.
- 상단 표는 샘플 형식(`테스트 ID/요구사항 ID/테스트 목적/예상 결과/...`)을 유지한다.
- 상세 추적은 하단 IT-Flow/Comm 연계 표로 분리하며 Req-VC-IT 추적을 유지한다.
- 범위는 CANoe SIL, CAN+Ethernet으로 고정한다.
- 임시 주석(실행 제약): 현재 CANoe.CAN 라이선스 환경에서는 SIL 실행 시 Ethernet 구간을 CAN 대체 백본으로 검증하며, Ethernet 라이선스 확보 후 동일 IT 케이스로 재검증한다.
- 본 문서는 `FZ_001~FZ_012` 결과 반영 전 Baseline Draft이며, 측정값 확정 시 수행결과를 기입한다.
- IT는 인터페이스/흐름 중심의 핵심 체인만 유지한다(Lean IT).
- 세부 경계값/미세 분기는 원칙적으로 UT(05)와 ST(07)에서 검증하고, 인터페이스 리스크가 큰 항목은 IT 보강 케이스로 선별 검증한다.
- `IT_SIL_001`, `IT_BASE_DIAG_001`은 Validation Harness 경로 검증(검증 전용) 항목이다.
- IT 증적(로그/캡처/리포트)은 `canoe/logging/evidence/IT/` 경로 규칙으로 관리한다.
- V2 확장 요구(`Req_120~Req_124`)는 구현 활성 상태로 IT 항목을 관리하며, SIL 시나리오 15~19와 연계해 검증한다.

---

## 통합 테스트 표 (공식 표준 양식)

| 테스트 ID | 요구사항 ID | VC ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|---|---|---|---|---|---|---|---|
| IT_CORE_001 | Req_001,Req_002,Req_003,Req_004,Req_005,Req_006,Req_007,Req_008,Req_009,Req_010,Req_011,Req_012 | VC_001~VC_012 | 입력 CAN(0x2A0/0x2A1/0x2A3)부터 GW 변환(0x510/0x511/0x512), 경고 코어 판정까지 핵심 경로 통합 검증 | 입력 변화 후 `150ms` 이내 warningState/zoneContext가 기대값으로 반영되고 경로 단절이 없다 |  |  |  |
| IT_EMS_001 | Req_017,Req_018,Req_023 | VC_017,VC_018,VC_023 | 경찰/구급 긴급 알림 송신-수신 체인(Flow_004~006) 통합 검증 | E100 Active/Clear 송수신이 일치하고 송신 주기 `100ms`가 유지되며 `150ms` 이내 중재 입력에 반영된다 |  |  |  |
| IT_ARB_001 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027~VC_032 | 긴급/구간 동시 발생 시 경고 중재 로직 통합 검증 | Emergency>Zone, Ambulance>Police, ETA, SourceID 규칙으로 단일 selectedAlert가 결정론적으로 생성된다 |  |  |  |
| IT_OUT_001 | Req_005,Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_019,Req_020,Req_021,Req_026,Req_033,Req_034,Req_035,Req_036,Req_037,Req_038,Req_039,Req_040 | VC_005,VC_008,VC_009,VC_013~VC_016,VC_019~VC_021,VC_026,VC_033~VC_040 | 중재 결과(0xE200)에서 Ambient/Cluster 출력(0x289/0x280)까지 통합 검증 | 출력 정책(문구/색상/패턴/복귀)이 일치하고 출력 주기 `50ms`가 유지된다 |  |  |  |
| IT_TIMEOUT_001 | Req_024,Req_033,Req_034 | VC_024,VC_033,VC_034 | 긴급 미수신 타임아웃 해제 및 복귀 체인 통합 검증 | `1000ms` 무갱신 시 timeoutClear가 전환되고 `150ms` 이내 안전 복귀가 완료되며 중복 토글이 없다 |  |  |  |
| IT_V2_RISK_001 | Req_120,Req_121,Req_122,Req_123 | VC_120,VC_121,VC_122,VC_123 | 긴급차량 근접 위험도 기반 감속 보조 요청/경고 동기화 체인 통합 검증 | 위험도 임계 초과 시 `150ms` 이내 감속 보조 요청 생성, 활성 상태에서 Ambient/Cluster 동기 오프셋 `<=50ms`, 운전자 개입 시 `150ms` 이내 해제 (SIL Scenario 15/16/17/19) | Ready |  |  |
| IT_V2_FAILSAFE_001 | Req_124 | VC_124 | 도메인 경로 단절 강등(Fail-safe) 체인 통합 검증 | 단절 감지 후 `150ms` 이내 failSafeMode 전환, 자동 감속 보조 0건 유지, 최소 경고 채널 유지 (SIL Scenario 18) | Ready |  |  |
| IT_SIL_001 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | CANoe SIL 실행/판정 경로(TestScenario->ScenarioResult) 통합 검증 | CAN+Ethernet(또는 CAN 대체 백본) 조건에서도 시나리오 실행/결과 기록/로그 요약이 일관되게 유지된다 |  |  |  |
| IT_BASE_001 | Req_101~Req_107,Req_109~Req_119 | VC_101~VC_107,VC_109~VC_119 | 차량 기본 기능(시동/기어/가감속/조향/비상등/창문/표시/도메인 경계 + Body/IVI 확장 상태) 통합 검증 | Flow_101~106, Flow_201~205 경로에서 기본 차량 기능 체인이 성립하고 기본 상태/표시가 일관되게 유지된다 |  |  |  |
| IT_BASE_PT_001 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | Powertrain 도메인 기본 동력/변속/상태 경로 통합 검증 | Comm_101/204/105 경로에서 엔진/변속/동력 상태가 `100ms` 주기로 일관되게 연계된다 |  |  |  |
| IT_BASE_CH_001 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | Chassis 도메인 가감속/조향/제동/차체상태 경로 통합 검증 | Comm_102/201/105 경로에서 입력/상태/헬스 연계가 `100ms` 기준으로 유지된다 |  |  |  |
| IT_BASE_BODY_001 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | Body 도메인 비상등/창문/편의상태 경로 통합 검증 | Comm_103/202/105 경로에서 차체 제어 상태와 경계 라우팅이 일관되게 유지된다 |  |  |  |
| IT_BASE_IVI_001 | Req_109,Req_111 | VC_109,VC_111 | Infotainment 도메인 기본 표시/UI/경계 연동 통합 검증 | Comm_104/203/105 경로에서 표시 상태와 연계 이벤트가 50/100ms 규칙을 만족한다 |  |  |  |
| IT_BASE_EXT_BODY_001 | Req_113,Req_114,Req_115,Req_116,Req_117,Req_118 | VC_113,VC_114,VC_115,VC_116,VC_117,VC_118 | Body 확장 기능(HVAC/Seat/Mirror/Door/Wiper-Rain/Security) 통합 검증 | Comm_202/105 경로에서 확장 상태/제어 프레임이 `100ms` 주기로 연계되고 `150ms` 이내 정책 반영된다 |  |  |  |
| IT_BASE_EXT_IVI_001 | Req_119 | VC_119 | Infotainment 확장 기능(Audio Focus/Voice/TTS 상태) 통합 검증 | Comm_203/105 경로에서 오디오/음성 상태가 50/100ms 규칙을 만족하고 `150ms` 이내 HMI 정책에 반영된다 |  |  |  |
| IT_BASE_DIAG_001 | Req_112 | VC_112 | Test/Diag 결과 경로 통합 검증 | Comm_106/205(Event+100ms) 경로에서 진단 요청-응답 및 결과 기록이 누락 없이 유지된다 |  |  |  |

---

## 통합 테스트 추적 상세 표

| IT ID | 관련 Flow | 관련 Comm | 관련 Func | 관련 Req | 관련 VC | 선행 UT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| IT_CORE_001 | Flow_001,Flow_002,Flow_003 | Comm_001,Comm_002,Comm_003 | Func_001~Func_012 | Req_001,Req_002,Req_003,Req_004,Req_005,Req_006,Req_007,Req_008,Req_009,Req_010,Req_011,Req_012 | VC_001~VC_012 | UT_ADAS_001, UT_NAV_001, UT_GW_001 | 입력 `100ms` + 출력 `50ms` 기준 `150ms` 이내 반영 |
| IT_EMS_001 | Flow_004,Flow_005,Flow_006 | Comm_004,Comm_005,Comm_006 | Func_017,Func_018,Func_023 | Req_017,Req_018,Req_023 | VC_017,VC_018,VC_023 | UT_EMS_POL_001, UT_EMS_AMB_001, UT_EMS_RX_001 | Active/Clear 송수신 상태 일치, 송신주기 `100ms` 유지 |
| IT_ARB_001 | Flow_006 | Comm_006 | Func_022,Func_025,Func_027~Func_032 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027~VC_032 | UT_ARB_001 | 우선순위/동률 규칙 결과가 기대값과 일치 |
| IT_OUT_001 | Flow_007,Flow_008 | Comm_007,Comm_008 | Func_005,Func_008,Func_009,Func_013~Func_016,Func_019~Func_021,Func_026,Func_033~Func_040 | Req_005,Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_019,Req_020,Req_021,Req_026,Req_033,Req_034,Req_035,Req_036,Req_037,Req_038,Req_039,Req_040 | VC_005,VC_008,VC_009,VC_013~VC_016,VC_019~VC_021,VC_026,VC_033~VC_040 | UT_BCM_001, UT_CLU_001, UT_OUT_GW_001 | Ambient/Cluster 출력이 정책표와 일치, 출력 주기 `50ms` 유지 |
| IT_TIMEOUT_001 | Flow_006,Flow_007,Flow_008 | Comm_006,Comm_007,Comm_008 | Func_024,Func_033,Func_034 | Req_024,Req_033,Req_034 | VC_024,VC_033,VC_034 | UT_EMS_RX_001, UT_BCM_001 | `1000ms` 무갱신 후 timeoutClear=1, `150ms` 이내 복귀 완료 |
| IT_V2_RISK_001 | Flow_120,Flow_121,Flow_122,Flow_123 | Comm_120,Comm_121,Comm_122,Comm_123 | Func_120,Func_121,Func_122,Func_123 | Req_120,Req_121,Req_122,Req_123 | VC_120,VC_121,VC_122,VC_123 | UT_V2_RISK_001, UT_V2_RELEASE_001 | 위험도 기반 보조 요청 생성/경고 동기화/운전자 개입 해제가 수치 기준(`100ms`,`150ms`,`<=50ms`) 충족 (SIL Scenario 15/16/17/19) |
| IT_V2_FAILSAFE_001 | Flow_124 | Comm_124 | Func_124 | Req_124 | VC_124 | UT_V2_FAILSAFE_001 | 경로 단절 감지 후 `150ms` 이내 강등 전환, 자동 감속 보조 0건, 최소 경고 채널 유지 (SIL Scenario 18) |
| IT_SIL_001 | Flow_009 | Comm_009 | Func_041,Func_042,Func_043 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | UT_SIL_001 | 시나리오 실행/결과 기록/로그 연동 완료 |
| IT_BASE_001 | Flow_101~Flow_106, Flow_201~Flow_205 | Comm_101~Comm_106, Comm_201~Comm_205 | Func_101~Func_107,Func_109~Func_119 | Req_101~Req_107,Req_109~Req_119 | VC_101~VC_107,VC_109~VC_119 | UT_BASE_001, UT_BASE_PT_001, UT_BASE_CH_001, UT_BASE_BODY_001, UT_BASE_IVI_001, UT_BASE_EXT_BODY_001, UT_BASE_EXT_IVI_001, UT_BASE_GW_001, UT_BASE_TEST_001 | 차량 기본 기능 입력/상태/표시/도메인 경계/SIL 판정 연동이 일관되게 유지 |
| IT_BASE_PT_001 | Flow_101,Flow_204,Flow_105 | Comm_101,Comm_204,Comm_105 | Func_101,Func_102,Func_110 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | UT_BASE_PT_001, UT_BASE_GW_001 | 엔진/변속/동력 상태 연계가 `100ms` 기준으로 유지 |
| IT_BASE_CH_001 | Flow_102,Flow_201,Flow_105 | Comm_102,Comm_201,Comm_105 | Func_103,Func_104,Func_105,Func_110 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | UT_BASE_CH_001, UT_BASE_GW_001 | 가감속/제동/조향/차체상태 연계가 `100ms` 기준으로 유지 |
| IT_BASE_BODY_001 | Flow_103,Flow_202,Flow_105 | Comm_103,Comm_202,Comm_105 | Func_106,Func_107,Func_111 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | UT_BASE_BODY_001, UT_BASE_GW_001 | 차체 제어/편의/상태 경로가 일관되게 유지 |
| IT_BASE_IVI_001 | Flow_104,Flow_203,Flow_105 | Comm_104,Comm_203,Comm_105 | Func_109,Func_111 | Req_109,Req_111 | VC_109,VC_111 | UT_BASE_IVI_001, UT_BASE_GW_001 | 기본 표시/UI/연계 이벤트가 50/100ms 기준으로 유지 |
| IT_BASE_EXT_BODY_001 | Flow_202,Flow_105 | Comm_202,Comm_105 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Req_113,Req_114,Req_115,Req_116,Req_117,Req_118 | VC_113,VC_114,VC_115,VC_116,VC_117,VC_118 | UT_BASE_EXT_BODY_001, UT_BASE_GW_001 | HVAC/Seat/Mirror/Door/Wiper-Rain/Security 확장 상태가 `100ms` 주기로 연계되고 `150ms` 이내 반영 |
| IT_BASE_EXT_IVI_001 | Flow_203,Flow_105 | Comm_203,Comm_105 | Func_119 | Req_119 | VC_119 | UT_BASE_EXT_IVI_001, UT_BASE_GW_001 | Audio Focus/Voice/TTS 상태가 50/100ms 주기 규칙과 `150ms` 반영 기준을 만족 |
| IT_BASE_DIAG_001 | Flow_106,Flow_205 | Comm_106,Comm_205 | Func_112 | Req_112 | VC_112 | UT_BASE_TEST_001 | 진단 요청-응답 및 결과 기록이 Event+100ms 기준으로 유지 |

---
## 핵심 보강 케이스 (선별 수용)

| IT 보강 ID | 기준 IT | Req/VC | 목적 | 입력/조건 | 합격 기준 | 선행 UT |
|---|---|---|---|---|---|---|
| IT_BND_024_A | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 미만 확인 | 마지막 긴급 수신 후 `999ms` | `timeoutClear=0` 유지 | UT_BND_024_A |
| IT_BND_024_B | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 확인 | 마지막 긴급 수신 후 `1000ms` | `timeoutClear=1` 단회 전환 | UT_BND_024_B |
| IT_BND_024_C | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 초과 확인 | 마지막 긴급 수신 후 `>1000ms` | 해제 상태 유지, 중복 토글 없음 | UT_BND_024_C |
| IT_ARB_030_031_A | IT_ARB_001 | Req_030,Req_031 / VC_030,VC_031 | ETA/SourceID 동률 규칙 확인 | 동급 긴급 2건(ETA 동률 포함) | ETA 우선, 동률 시 sourceId 오름차순 선택 | UT_ARB_001 |
| IT_HMI_020_A | IT_OUT_001 | Req_020 / VC_020 | 방향 표시 분기 확인 | emergencyDirection = LEFT/RIGHT/NONE | 방향 코드가 규칙표와 일치 | UT_CLU_001 |

---

## 07 연계 체크포인트

- `IT_*`의 E2E 결과는 `07_System_Test.md`의 `ST_*` 수용 판단 근거로 사용한다.
- `IT_CORE_001`, `IT_EMS_001`, `IT_ARB_001`, `IT_OUT_001`, `IT_TIMEOUT_001`, `IT_SIL_001`, `IT_BASE_001`, `IT_BASE_PT_001`, `IT_BASE_CH_001`, `IT_BASE_BODY_001`, `IT_BASE_IVI_001`, `IT_BASE_DIAG_001`는 03/04 문서의 검증 참조 ID와 일치해야 한다.
- `IT_V2_RISK_001`, `IT_V2_FAILSAFE_001`은 `Req_120~Req_124` 활성 체인의 ST 연계 근거로 유지한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 4.15 | 2026-03-06 | 미사용 체인 정리: `Req/VC/Func_108`을 `IT_BASE_001/IT_BASE_BODY_001`에서 제거하고 Baseline 범위를 `108 제외`로 동기화. |
| 4.14 | 2026-03-03 | V2 IT를 구현 활성 상태로 전환하고 `IT_V2_RISK_001`, `IT_V2_FAILSAFE_001` 수행 상태를 Ready로 갱신. |
| 4.13 | 2026-03-02 | V2 확장(Pre-Activation) IT 반영: `IT_V2_RISK_001`, `IT_V2_FAILSAFE_001` 추가 및 `Req_120~Req_124` 추적 연계/체크포인트 보강. |
| 4.12 | 2026-03-02 | 작성 원칙에 CANoe.CAN 실행 제약 임시 주석을 추가하고, 경계값 검증 규칙을 `UT/ST 원칙 + IT 선별 보강`으로 명확화. `IT_SIL_001` 기대결과에 대체 백본 조건을 병기. |
| 4.11 | 2026-03-02 | 중간감사 추적성 보강: IT 상단/상세 표의 Req 범위 표기를 일부 구간(`~`)에서 개별 Req 나열로 확장해 `Req_002/003/004/006/007/011/014/015/028/029/035~039`의 명시 추적을 강화. |
| 4.10 | 2026-03-02 | 차량 기본 기능 확장 추적 보강: `Req/VC/Func_113~119`를 `IT_BASE_001` 범위에 반영하고 `IT_BASE_EXT_BODY_001`, `IT_BASE_EXT_IVI_001`를 상단/하단 표에 추가. |
| 4.9 | 2026-03-02 | 증적 경로 규칙 고정: IT 실행 증적 저장 경로를 `canoe/logging/evidence/IT/`로 명시. |
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-23 | 구버전 요구 ID 구조 반영 |
| 3.0 | 2026-02-24 | 구버전 TS 시나리오 확장 |
| 4.0 | 2026-02-26 | 옵션1 아키텍처 기준 전면 재작성. OTA/UDS/DoIP 제거, IT ID 체계 및 Flow/Comm 중심 통합 검증 구조 반영 |
| 4.1 | 2026-02-26 | 합격 기준에 50ms/100ms/150ms/1000ms 수치 기준을 반영하고, FZ 사전 점검 결과 반영 전 Draft 경계 문구 추가 |
| 4.2 | 2026-02-26 | VC 추적 강화를 위해 상단/상세 표에 VC ID 컬럼을 추가하고 Req-VC-IT 연결을 명시 |
| 4.3 | 2026-02-28 | 팀 제안 중 현업 BP에 부합하는 핵심만 선별 반영: 타임아웃 경계값(999/1000/>1000), ETA/SourceID 우선순위, 방향 분기 보강 케이스 추가 |
| 4.4 | 2026-02-28 | Flow_003(Comm_003)에 `speedLimit` 연계를 추가하여 Req_010(스쿨존 과속) 통합 검증 경로를 보강. |
| 4.5 | 2026-02-28 | 차량 기본 기능 통합 검증을 위해 `IT_BASE_001`(Req/VC/Func 101~112, Flow/Comm 101~106 및 201~205)을 추가. |
| 4.6 | 2026-02-28 | 멘토링 피드백 반영: IT를 핵심 통합 체인 중심(Lean IT)으로 재구성하고 세부 경계값은 UT/ST로 분리. |
| 4.7 | 2026-02-28 | Lean IT 재구성 후 잔여 참조 ID 정리(`IT_HMI_020_A`, 07 연계 체크포인트) 및 03/04 검증 링크 문구를 최신 체계로 동기화. |
| 4.8 | 2026-02-28 | 확장된 통신/기본차량 범위 반영: 도메인별 통합 검증(`IT_BASE_PT/CH/BODY/IVI/DIAG`)을 상단/하단 표에 추가. |

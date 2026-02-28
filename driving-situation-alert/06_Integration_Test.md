# 통합 테스트 (Integration Test)

**Document ID**: PROJ-06-IT
**ISO 26262 Reference**: Part 6, Cl.10 (Software Integration and Integration Test)
**ASPICE Reference**: SWE.5 (Software Integration and Integration Test)
**Version**: 4.5
**Date**: 2026-02-28
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
- 본 문서는 `FZ_001~FZ_012` 결과 반영 전 Baseline Draft이며, 측정값 확정 시 수행결과를 기입한다.
- IT는 인터페이스/흐름 중심으로 유지하고, 세부 시나리오 분해는 핵심 경계값/우선순위 항목만 보강 케이스로 관리한다.

---

## 통합 테스트 표 (공식 표준 양식)

| 테스트 ID | 요구사항 ID | VC ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|---|---|---|---|---|---|---|---|
| IT_FLOW_001 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010 | VC_001,VC_002,VC_003,VC_004,VC_006,VC_010 | Chassis 입력 -> CHASSIS_GW -> ADAS_WARN_CTRL 연동 검증 | 0x100/0x101 입력이 0x510/0x511로 변환되고 `150ms` 이내 경고 상태 계산 반영 |  |  |  |
| IT_FLOW_002 | Req_007,Req_010 | VC_007,VC_010 | Nav 입력 -> INFOTAINMENT_GW -> NAV_CONTEXT_MGR/ADAS_WARN_CTRL/WARN_ARB_MGR 연동 검증 | 0x110 입력(roadZone/navDirection/zoneDistance/speedLimit)이 0x512로 변환되고 `150ms` 이내 baseZoneContext/speedLimitNorm 갱신 |  |  |  |
| IT_EMS_TX_001 | Req_017 | VC_017 | 경찰 긴급 송신 연동 검증 | EMS_POLICE_TX `100ms` 송신이 EMS_ALERT_RX 수신으로 연결되고 `150ms` 이내 중재 입력 반영 |  |  |  |
| IT_EMS_TX_002 | Req_018 | VC_018 | 구급 긴급 송신 연동 검증 | EMS_AMB_TX `100ms` 송신이 EMS_ALERT_RX 수신으로 연결되고 `150ms` 이내 중재 입력 반영 |  |  |  |
| IT_ARB_001 | Req_022,Req_025,Req_027~Req_032 | VC_022,VC_025,VC_027~VC_032 | 긴급/구간 충돌 중재 연동 검증 | 우선순위 규칙에 따라 단일 selectedAlert 결과 생성 |  |  |  |
| IT_AMB_001 | Req_008,Req_009,Req_013~Req_016,Req_033~Req_039 | VC_008,VC_009,VC_013~VC_016,VC_033~VC_039 | WARN_ARB_MGR -> BODY_GW -> BCM_AMBIENT_CTRL 연동 검증 | 0xE200 수신 후 0x210 출력이 정책과 일치 |  |  |  |
| IT_CLU_001 | Req_005,Req_019~Req_021,Req_026,Req_040 | VC_005,VC_019~VC_021,VC_026,VC_040 | WARN_ARB_MGR -> IVI_GW -> CLU_HMI_CTRL 연동 검증 | 0xE200 수신 후 0x220 출력이 정책과 일치 |  |  |  |
| IT_TIMEOUT_001 | Req_024 | VC_024 | EmergencyAlert 1000ms 무갱신 타임아웃 연동 검증 | `1000ms` 무갱신 시 timeoutClear=1 생성, 이후 `150ms` 이내 안전 상태 복귀 |  |  |  |
| IT_RECOVERY_001 | Req_033,Req_034 | VC_033,VC_034 | 긴급 해제 후 이전 구간 상태 복귀 검증 | 중재 종료 후 Zone 컨텍스트 복귀 및 전환 완화 동작 |  |  |  |
| IT_SIL_001 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | SIL 시나리오 실행/판정 연동 검증 | CAN+ETH 동시 조건에서 시나리오 판정 결과 기록 |  |  |  |
| IT_BASE_001 | Req_101~Req_112 | VC_101~VC_112 | 차량 기본 기능(시동/기어/입력/표시/도메인경계) 통합 연동 검증 | Flow_101~Flow_106,Flow_201~Flow_205 경로에서 입력/상태/표시/헬스/판정 체인이 일관되게 동작 |  |  |  |

---

## 통합 테스트 추적 상세 표

| IT ID | 관련 Flow | 관련 Comm | 관련 Func | 관련 Req | 관련 VC | 선행 UT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| IT_FLOW_001 | Flow_001, Flow_002 | Comm_001, Comm_002 | Func_001~Func_004,Func_006,Func_010~Func_012 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010,Req_011,Req_012 | VC_001,VC_002,VC_003,VC_004,VC_006,VC_010,VC_011,VC_012 | UT_ADAS_001, UT_GW_001 | 입력 `100ms` + 출력 `50ms` 기준 `150ms` 이내 반영 |
| IT_FLOW_002 | Flow_003 | Comm_003 | Func_007,Func_010 | Req_007,Req_010 | VC_007,VC_010 | UT_NAV_001, UT_GW_001 | 구간/제한속도 입력 변경 후 `150ms` 이내 컨텍스트/과속기준 반영 |
| IT_EMS_TX_001 | Flow_004 | Comm_004 | Func_017,Func_023 | Req_017,Req_023 | VC_017,VC_023 | UT_EMS_POL_001, UT_EMS_RX_001 | Police Active/Clear 송수신 일치, 송신주기 `100ms` 유지 |
| IT_EMS_TX_002 | Flow_005 | Comm_005 | Func_018,Func_023 | Req_018,Req_023 | VC_018,VC_023 | UT_EMS_AMB_001, UT_EMS_RX_001 | Ambulance Active/Clear 송수신 일치, 송신주기 `100ms` 유지 |
| IT_ARB_001 | Flow_006 | Comm_006 | Func_022,Func_025,Func_027~Func_032 | Req_022,Req_025,Req_027~Req_032 | VC_022,VC_025,VC_027~VC_032 | UT_ARB_001 | 우선순위/동률 규칙 결과가 기대표와 일치 |
| IT_AMB_001 | Flow_007 | Comm_007 | Func_008,Func_009,Func_013~Func_016,Func_033~Func_039 | Req_008,Req_009,Req_013~Req_016,Req_033~Req_039 | VC_008,VC_009,VC_013~VC_016,VC_033~VC_039 | UT_BCM_001, UT_OUT_GW_001 | Ambient 출력 주기 `50ms` 유지, 정책표와 일치 |
| IT_CLU_001 | Flow_008 | Comm_008 | Func_005,Func_019~Func_021,Func_026,Func_040 | Req_005,Req_019~Req_021,Req_026,Req_040 | VC_005,VC_019~VC_021,VC_026,VC_040 | UT_CLU_001, UT_OUT_GW_001 | Cluster 출력 주기 `50ms` 유지, 중복 억제 동작 일치 |
| IT_TIMEOUT_001 | Flow_006, Flow_007, Flow_008 | Comm_006, Comm_007, Comm_008 | Func_024,Func_033,Func_034,Func_040 | Req_024,Req_033,Req_034,Req_040 | VC_024,VC_033,VC_034,VC_040 | UT_EMS_RX_001, UT_BCM_001, UT_CLU_001 | `1000ms` 무갱신 후 timeoutClear=1, `150ms` 이내 안전 복귀 완료 |
| IT_RECOVERY_001 | Flow_006, Flow_007, Flow_008 | Comm_006, Comm_007, Comm_008 | Func_033,Func_034 | Req_033,Req_034 | VC_033,VC_034 | UT_BCM_001 | 긴급 종료 후 직전 Zone 상태 정상 복원 |
| IT_SIL_001 | Flow_009 | Comm_009 | Func_041,Func_042,Func_043 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | UT_ADAS_001~UT_CLU_001 | 시나리오 실행/결과 기록/로그 연동 완료 |
| IT_BASE_001 | Flow_101~Flow_106, Flow_201~Flow_205 | Comm_101~Comm_106, Comm_201~Comm_205 | Func_101~Func_112 | Req_101~Req_112 | VC_101~VC_112 | UT_BASE_001 | 차량 기본 기능 입력/상태/표시/도메인 경계/SIL 판정 연동이 일관되게 유지 |

---

## 핵심 보강 케이스 (선별 수용)

| IT 보강 ID | 기준 IT | Req/VC | 목적 | 입력/조건 | 합격 기준 | 선행 UT |
|---|---|---|---|---|---|---|
| IT_BND_024_A | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 미만 확인 | 마지막 긴급 수신 후 `999ms` | `timeoutClear=0` 유지 | UT_BND_024_A |
| IT_BND_024_B | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 확인 | 마지막 긴급 수신 후 `1000ms` | `timeoutClear=1` 단회 전환 | UT_BND_024_B |
| IT_BND_024_C | IT_TIMEOUT_001 | Req_024 / VC_024 | 타임아웃 경계값 초과 확인 | 마지막 긴급 수신 후 `>1000ms` | 해제 상태 유지, 중복 토글 없음 | UT_BND_024_C |
| IT_ARB_030_031_A | IT_ARB_001 | Req_030,Req_031 / VC_030,VC_031 | ETA/SourceID 동률 규칙 확인 | 동급 긴급 2건(ETA 동률 포함) | ETA 우선, 동률 시 sourceId 오름차순 선택 | UT_ARB_001 |
| IT_HMI_020_A | IT_CLU_001 | Req_020 / VC_020 | 방향 표시 분기 확인 | emergencyDirection = LEFT/RIGHT/NONE | 방향 코드가 규칙표와 일치 | UT_CLU_001 |

---

## 07 연계 체크포인트

- `IT_*`의 E2E 결과는 `07_System_Test.md`의 `ST_*` 수용 판단 근거로 사용한다.
- `IT_AMB_001`, `IT_CLU_001`, `IT_EMS_TX_001`, `IT_EMS_TX_002`는 03 문서 검증 컬럼 참조 ID와 일치해야 한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-23 | 구버전 요구 ID 구조 반영 |
| 3.0 | 2026-02-24 | 구버전 TS 시나리오 확장 |
| 4.0 | 2026-02-26 | 옵션1 아키텍처 기준 전면 재작성. OTA/UDS/DoIP 제거, IT ID 체계 및 Flow/Comm 중심 통합 검증 구조 반영 |
| 4.1 | 2026-02-26 | 합격 기준에 50ms/100ms/150ms/1000ms 수치 기준을 반영하고, FZ 사전 점검 결과 반영 전 Draft 경계 문구 추가 |
| 4.2 | 2026-02-26 | VC 추적 강화를 위해 상단/상세 표에 VC ID 컬럼을 추가하고 Req-VC-IT 연결을 명시 |
| 4.3 | 2026-02-28 | 팀 제안 중 현업 BP에 부합하는 핵심만 선별 반영: 타임아웃 경계값(999/1000/>1000), ETA/SourceID 우선순위, 방향 분기 보강 케이스 추가 |
| 4.4 | 2026-02-28 | Flow_003(Comm_003)에 `speedLimit` 연계를 추가하여 Req_010(스쿨존 과속) 통합 검증 경로를 보강. |
| 4.5 | 2026-02-28 | 차량 기본 기능 통합 검증을 위해 `IT_BASE_001`(Req/VC/Func 101~112, Flow/Comm 101~106 및 201~205)을 추가. |

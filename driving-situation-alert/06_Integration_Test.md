# 통합 테스트 (Integration Test)

**Document ID**: PROJ-06-IT
**ISO 26262 Reference**: Part 6, Cl.10 (Software Integration and Integration Test)
**ASPICE Reference**: SWE.5 (Software Integration and Integration Test)
**Version**: 4.0
**Date**: 2026-02-26
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 중단 (SWE.5) | `06_Integration_Test.md` | `05_Unit_Test.md` | `07_System_Test.md` |

---

## 작성 원칙

- 본 문서는 모듈 간 인터페이스/흐름(Flow, Comm) 연동 검증을 수행한다.
- 상단 표는 샘플 형식(`테스트 ID/요구사항 ID/테스트 목적/예상 결과/...`)을 유지한다.
- 상세 추적은 하단 IT-Flow/Comm 연계 표로 분리한다.
- 범위는 CANoe SIL, CAN+Ethernet으로 고정한다.

---

## 통합 테스트 표 (공식 표준 양식)

| 테스트 ID | 요구사항 ID | 테스트 목적 | 예상 결과 | 테스트 수행 결과 | 담당자 | 일자 |
|---|---|---|---|---|---|---|
| IT_FLOW_001 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010 | Chassis 입력 -> CHASSIS_GW -> ADAS_WARN_CTRL 연동 검증 | 0x100/0x101 입력이 0x510/0x511로 변환되어 경고 상태 계산에 반영 |  |  |  |
| IT_FLOW_002 | Req_007 | Nav 입력 -> INFOTAINMENT_GW -> NAV_CONTEXT_MGR/WARN_ARB_MGR 연동 검증 | 0x110 입력이 0x512로 변환되어 baseZoneContext 갱신 |  |  |  |
| IT_EMS_TX_001 | Req_017 | 경찰 긴급 송신 연동 검증 | EMS_POLICE_TX 송신이 EMS_ALERT_RX 수신으로 연결되고 중재 입력 반영 |  |  |  |
| IT_EMS_TX_002 | Req_018 | 구급 긴급 송신 연동 검증 | EMS_AMB_TX 송신이 EMS_ALERT_RX 수신으로 연결되고 중재 입력 반영 |  |  |  |
| IT_ARB_001 | Req_022,Req_025,Req_027~Req_032 | 긴급/구간 충돌 중재 연동 검증 | 우선순위 규칙에 따라 단일 selectedAlert 결과 생성 |  |  |  |
| IT_AMB_001 | Req_008,Req_009,Req_013~Req_016,Req_033~Req_039 | WARN_ARB_MGR -> BODY_GW -> BCM_AMBIENT_CTRL 연동 검증 | 0xE200 수신 후 0x210 출력이 정책과 일치 |  |  |  |
| IT_CLU_001 | Req_005,Req_019~Req_021,Req_026,Req_040 | WARN_ARB_MGR -> IVI_GW -> CLU_HMI_CTRL 연동 검증 | 0xE200 수신 후 0x220 출력이 정책과 일치 |  |  |  |
| IT_TIMEOUT_001 | Req_024 | EmergencyAlert 1000ms 무갱신 타임아웃 연동 검증 | timeoutClear=1 생성, 출력이 안전 상태로 복귀 |  |  |  |
| IT_RECOVERY_001 | Req_033,Req_034 | 긴급 해제 후 이전 구간 상태 복귀 검증 | 중재 종료 후 Zone 컨텍스트 복귀 및 전환 완화 동작 |  |  |  |
| IT_SIL_001 | Req_041,Req_042,Req_043 | SIL 시나리오 실행/판정 연동 검증 | CAN+ETH 동시 조건에서 시나리오 판정 결과 기록 |  |  |  |

---

## 통합 테스트 추적 상세 표

| IT ID | 관련 Flow | 관련 Comm | 관련 Func | 관련 Req | 선행 UT | 합격 기준 |
|---|---|---|---|---|---|---|
| IT_FLOW_001 | Flow_001, Flow_002 | Comm_001, Comm_002 | Func_001~Func_004,Func_006,Func_010~Func_012 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010,Req_011,Req_012 | UT_ADAS_001, UT_GW_001 | 입력 프레임 -> 변환 프레임 -> 경고상태 반영 지연 100ms 이내 |
| IT_FLOW_002 | Flow_003 | Comm_003 | Func_007 | Req_007 | UT_NAV_001, UT_GW_001 | 구간 입력 변경 후 컨텍스트 즉시 반영 |
| IT_EMS_TX_001 | Flow_004 | Comm_004 | Func_017,Func_023 | Req_017,Req_023 | UT_EMS_POL_001, UT_EMS_RX_001 | Police Active/Clear 송수신 일치 |
| IT_EMS_TX_002 | Flow_005 | Comm_005 | Func_018,Func_023 | Req_018,Req_023 | UT_EMS_AMB_001, UT_EMS_RX_001 | Ambulance Active/Clear 송수신 일치 |
| IT_ARB_001 | Flow_006 | Comm_006 | Func_022,Func_025,Func_027~Func_032 | Req_022,Req_025,Req_027~Req_032 | UT_ARB_001 | 우선순위/동률 규칙 결과가 기대표와 일치 |
| IT_AMB_001 | Flow_007 | Comm_007 | Func_008,Func_009,Func_013~Func_016,Func_033~Func_039 | Req_008,Req_009,Req_013~Req_016,Req_033~Req_039 | UT_BCM_001, UT_OUT_GW_001 | AmbientMode/Color/Pattern 출력이 정책표와 일치 |
| IT_CLU_001 | Flow_008 | Comm_008 | Func_005,Func_019~Func_021,Func_026,Func_040 | Req_005,Req_019~Req_021,Req_026,Req_040 | UT_CLU_001, UT_OUT_GW_001 | WarningTextCode 출력 및 중복 억제 동작 일치 |
| IT_TIMEOUT_001 | Flow_006, Flow_007, Flow_008 | Comm_006, Comm_007, Comm_008 | Func_024,Func_033,Func_034,Func_040 | Req_024,Req_033,Req_034,Req_040 | UT_EMS_RX_001, UT_BCM_001, UT_CLU_001 | 1000ms 무갱신 후 안전 복귀 완료 |
| IT_RECOVERY_001 | Flow_006, Flow_007, Flow_008 | Comm_006, Comm_007, Comm_008 | Func_033,Func_034 | Req_033,Req_034 | UT_BCM_001 | 긴급 종료 후 직전 Zone 상태 정상 복원 |
| IT_SIL_001 | Flow_009 | Comm_009 | Func_041,Func_042,Func_043 | Req_041,Req_042,Req_043 | UT_ADAS_001~UT_CLU_001 | 시나리오 실행/결과 기록/로그 연동 완료 |

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

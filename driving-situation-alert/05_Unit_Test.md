# 단위 테스트 (Unit Test)

**Document ID**: PROJ-05-UT
**ISO 26262 Reference**: Part 6, Cl.9 (Software Unit Verification)
**ASPICE Reference**: SWE.4 (Software Unit Verification)
**Version**: 2.0
**Date**: 2026-02-26
**Status**: Draft
**Project Title**: 주행상황 연동 실시간 경고 시스템
**Subtitle**: (구간 인식, 긴급차량 경고시스템)

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 하단 (SWE.4) | `05_Unit_Test.md` | `04_SW_Implementation.md` | `06_Integration_Test.md` |

---

## 작성 원칙

- 본 문서는 모듈 단위 검증(유닛 단위) 결과를 정의한다.
- 공식 상단 표는 샘플 형식(`노드/분류/기능명/기능 설명/Pass/담당자/일자`)을 유지한다.
- 상세 추적(UT ID, Req/Func/Flow/Comm/Var)은 하단 표로 분리한다.
- 범위 외 항목(OTA/UDS/DoIP)은 포함하지 않는다.

---

## 단위 테스트 표 (공식 표준 양식)

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|---|---|---|---|---|---|---|
| ADAS_WARN_CTRL | 제어 | 주행/비주행 경고 활성 | 속도/주행상태/조향 입력 기반 경고 시작·해제·디바운스 검증 |  |  |  |
| NAV_CONTEXT_MGR | 제어 | 구간 컨텍스트 계산 | 구간/방향/거리 입력에 따른 컨텍스트 생성 검증 |  |  |  |
| EMS_POLICE_TX | 제어 | 경찰 긴급 알림 송신 | Police Active/ETA/Direction 기반 E100 송신 검증 |  |  |  |
| EMS_AMB_TX | 제어 | 구급 긴급 알림 송신 | Ambulance Active/ETA/Direction 기반 E100 송신 검증 |  |  |  |
| EMS_ALERT_RX | 제어 | 긴급 수신/해제/타임아웃 | Clear 처리 및 1000ms 타임아웃 해제 검증 |  |  |  |
| WARN_ARB_MGR | 제어 | 우선순위 중재 | Emergency>Zone, Ambulance>Police, ETA/SourceID 규칙 검증 |  |  |  |
| BCM_AMBIENT_CTRL | 제어 | 앰비언트 출력 정책 | 경고 레벨/타입 기반 색상·패턴·복귀 규칙 검증 |  |  |  |
| CLU_HMI_CTRL | 제어 | 클러스터 경고 정책 | 경고 원인/방향/종류/중복 억제/문구 길이 검증 |  |  |  |
| CHASSIS_GW | 제어 | CAN->ETH 변환 | 0x100/0x101 프레임 정규화 및 송신 주기 검증 |  |  |  |
| INFOTAINMENT_GW | 제어 | CAN->ETH 변환 | 0x110 프레임 정규화 및 송신 주기 검증 |  |  |  |
| BODY_GW | 제어 | ETH->CAN 변환 | E200 수신 후 0x210 송신 및 Fail-safe 검증 |  |  |  |
| IVI_GW | 제어 | ETH->CAN 변환 | E200 수신 후 0x220 송신 및 Fail-safe 검증 |  |  |  |
| SIL_TEST_CTRL | 검증 | 시나리오 실행/판정 | 시나리오 실행, 결과 기록, 로그 연계 검증 |  |  |  |

---

## 단위 테스트 추적 상세 표

| UT ID | 대상 모듈 | 검증 목적 | Req ID | Func ID | Flow/Comm | Var ID | 합격 기준 |
|---|---|---|---|---|---|---|---|
| UT_ADAS_001 | ADAS_WARN_CTRL | 경고 시작/해제/디바운스 로직 검증 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010,Req_011,Req_012 | Func_001,Func_002,Func_003,Func_004,Func_006,Func_010,Func_011,Func_012 | Flow_001,Flow_002 / Comm_001,Comm_002 | Var_012,Var_013,Var_014,Var_016 | 입력 변화 후 50ms 내 warningState 기대값 일치 |
| UT_NAV_001 | NAV_CONTEXT_MGR | 구간 컨텍스트 계산 검증 | Req_007 | Func_007 | Flow_003 / Comm_003 | Var_004,Var_005,Var_006,Var_015 | 입력 조합별 baseZoneContext 기대값 100% 일치 |
| UT_EMS_POL_001 | EMS_POLICE_TX | 경찰 긴급 송신 검증 | Req_017 | Func_017 | Flow_004 / Comm_004 | Var_007,Var_008,Var_009,Var_010,Var_011 | Active 시 100ms 주기 송신, Clear 전환 시 상태 반영 |
| UT_EMS_AMB_001 | EMS_AMB_TX | 구급 긴급 송신 검증 | Req_018 | Func_018 | Flow_005 / Comm_005 | Var_007,Var_008,Var_009,Var_010,Var_011 | Active 시 100ms 주기 송신, Clear 전환 시 상태 반영 |
| UT_EMS_RX_001 | EMS_ALERT_RX | 수신/해제/타임아웃 처리 검증 | Req_023,Req_024 | Func_023,Func_024 | Flow_006 / Comm_006 | Var_017,Var_020,Var_027 | 1000ms 무갱신 시 timeoutClear=1, emergencyContext clear |
| UT_ARB_001 | WARN_ARB_MGR | 중재 우선순위 검증 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | Func_022,Func_025,Func_027,Func_028,Func_029,Func_030,Func_031,Func_032 | Flow_006 / Comm_006 | Var_018,Var_019,Var_029 | 우선순위/동률규칙 결정 결과가 시나리오 기대값과 일치 |
| UT_BCM_001 | BCM_AMBIENT_CTRL | 앰비언트 정책 검증 | Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_033,Req_034,Req_035,Req_036,Req_037,Req_038,Req_039 | Func_008,Func_009,Func_013,Func_014,Func_015,Func_016,Func_033,Func_034,Func_035,Func_036,Func_037,Func_038,Func_039 | Flow_007 / Comm_007 | Var_021,Var_022,Var_023 | 모드/색상/패턴이 규칙표와 일치, 복귀/완화 동작 정상 |
| UT_CLU_001 | CLU_HMI_CTRL | 경고 문구 정책 검증 | Req_005,Req_019,Req_020,Req_021,Req_026,Req_040 | Func_005,Func_019,Func_020,Func_021,Func_026,Func_040 | Flow_008 / Comm_008 | Var_024,Var_028 | 문구 코드/중복 억제/길이 제한 규칙 충족 |
| UT_GW_001 | CHASSIS_GW, INFOTAINMENT_GW | 게이트웨이 변환 검증 | Req_007,Req_010,Req_011,Req_012 | Func_007,Func_010,Func_011,Func_012 | Flow_001,Flow_002,Flow_003 / Comm_001,Comm_002,Comm_003 | Var_001~Var_006,Var_012~Var_015 | CAN 입력 대비 ETH 변환값/주기 일치 |
| UT_OUT_GW_001 | BODY_GW, IVI_GW | ETH->CAN 출력 변환 검증 | Req_033,Req_034,Req_040 | Func_033,Func_034,Func_040 | Flow_007,Flow_008 / Comm_007,Comm_008 | Var_021~Var_024 | ETH 결과를 CAN 프레임으로 정확히 변환 송신 |
| UT_SIL_001 | SIL_TEST_CTRL | SIL 실행/판정 유닛 검증 | Req_041,Req_042,Req_043 | Func_041,Func_042,Func_043 | Flow_009 / Comm_009 | Var_025,Var_026 | 시나리오 실행/통신 조건 검증/결과 기록 로직 정상 |

---

## 06 연계 체크포인트

- `UT_*` 결과는 `06_Integration_Test.md`의 `IT_*` 시나리오 선행 조건으로 사용한다.
- `UT_EMS_RX_001`의 1000ms 타임아웃 결과는 `IT_ARB_001`, `IT_RECOVERY_001`의 전제 조건이다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-26 | 옵션1 아키텍처 기준으로 전면 재작성. OTA/UDS/DoIP 항목 제거, UT ID 체계(UT_ADAS_001 등) 및 Req/Func/Flow/Comm/Var 추적 표 추가 |

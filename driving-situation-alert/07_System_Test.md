# 시스템 테스트 (System Test)

**Document ID**: PROJ-07-ST
**ISO 26262 Reference**: Part 4, Cl.10 (System Integration and System Qualification Test)
**ASPICE Reference**: SYS.5 (System Qualification Test)
**Version**: 5.10
**Date**: 2026-03-02
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 상단 (SYS.5) | `07_System_Test.md` | `06_Integration_Test.md`, `01_Requirements.md` | 릴리즈/검수 |

---

## 작성 원칙

- 본 문서는 운전자 관점 E2E 시나리오로 요구사항 충족을 검증한다.
- 상단 표는 샘플 형식(`Scene ID/설명/Pass/담당자/일자`)을 유지한다.
- ST는 사용자/운전자 시나리오 중심으로 유지하고, 미세 경계값 판정은 UT/IT 근거를 참조한다.
- ST는 블랙박스 관점(입력 이벤트 -> 사용자 관찰 결과)으로 작성하며, 내부 구현 세부는 05/06 참조로 분리한다.
- 상세 추적은 하단 ST 추적표에서 `Req/VC/Func/Flow/Comm/Var/IT`로 연결한다.
- 검증 환경은 CANoe SIL, CAN+Ethernet으로 고정한다.
- 본 문서는 `FZ_001~FZ_012` 결과 반영 전 Baseline Draft이며, 측정값 확정 시 Pass/Fail를 기입한다.
- `ST_SIL_001`, `ST_SIL_002`, `ST_RESULT_001`, `ST_BASE_DIAG_001`은 Validation Harness 기반 검증 시나리오(검증 전용)다.
- ST 증적(로그/캡처/리포트)은 `canoe/logging/evidence/ST/` 경로 규칙으로 관리한다.

---

## 시스템 테스트 시나리오 (공식 표준 양식)

| Scene. ID | 설명 | Pass / Fail | 담당자 | 일자 |
|---|---|---|---|---|
| ST_SPEED_001 | 구간 제한속도 대비 속도 상승/감속 조건에서 경고 활성/해제가 요구대로 동작하는지 확인한다. |  |  |  |
| ST_ZONE_001 | 일반/스쿨존/고속 구간 전환 시 구간별 경고 정책이 즉시 반영되는지 확인한다. |  |  |  |
| ST_GUIDE_001 | 유도 구간에서 좌/우 방향 정보가 시각적으로 구분되어 표시되는지 확인한다. |  |  |  |
| ST_GUIDE_002 | 유도 구간 진입/전환/종료 시 경고가 깨지지 않고 기본 상태로 복귀되는지 확인한다. |  |  |  |
| ST_STEER_001 | 고속 구간 무조향 경고 발생 및 조향 복귀 시 해제 동작을 확인한다. |  |  |  |
| ST_EMS_001 | 경찰 긴급 접근 시 긴급 경고가 일반 경고보다 우선 표시되는지 확인한다. |  |  |  |
| ST_EMS_002 | 구급 긴급 접근 시 긴급 경고가 일반 경고보다 우선 표시되는지 확인한다. |  |  |  |
| ST_HMI_DIR_001 | 경찰 긴급 접근 방향(앞/좌/우/후)이 클러스터에 정확히 표시되는지 확인한다. |  |  |  |
| ST_HMI_DIR_002 | 구급 긴급 접근 방향(앞/좌/우/후)이 클러스터에 정확히 표시되는지 확인한다. |  |  |  |
| ST_ARB_ETA_001 | 동일 등급 경찰 긴급 알림 충돌 시 ETA 우선 규칙이 적용되는지 확인한다. |  |  |  |
| ST_ARB_ETA_002 | 동일 등급 구급 긴급 알림 충돌 시 ETA 우선 규칙이 적용되는지 확인한다. |  |  |  |
| ST_TIMEOUT_001 | 긴급 알림 1000ms 무갱신 시 안전 해제 및 복귀 동작을 확인한다. |  |  |  |
| ST_POLICY_001 | 긴급/구간 패턴·색상·문구 정책과 중복 팝업 억제가 요구대로 동작하는지 확인한다. |  |  |  |
| ST_SIL_001 | 물리 하드웨어 없이 CANoe SIL에서 핵심 시나리오 수행이 가능한지 확인한다. |  |  |  |
| ST_SIL_002 | CAN+Ethernet 동시 통신 조건에서 E2E 경고 체인이 유지되는지 확인한다. |  |  |  |
| ST_RESULT_001 | 시나리오별 합격/불합격 결과가 일관되게 기록·추적되는지 확인한다. |  |  |  |
| ST_BASE_PT_001 | 시동/기어/동력계 상태가 Powertrain 시나리오에서 안정적으로 연동되는지 확인한다. |  |  |  |
| ST_BASE_CH_001 | 가감속/조향/제동 입력이 Chassis 시나리오에서 안전 규칙대로 반영되는지 확인한다. |  |  |  |
| ST_BASE_BODY_001 | 비상등/창문/운전자상태 등 Body 시나리오가 의도한 동작으로 유지되는지 확인한다. |  |  |  |
| ST_BASE_IVI_001 | 클러스터 기본표시/안내/UI 상태가 Infotainment 시나리오에서 일관되게 유지되는지 확인한다. |  |  |  |
| ST_BASE_EXT_BODY_001 | HVAC/Seat/Mirror/Door/Wiper-Rain/Security 상태가 Body 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_EXT_IVI_001 | Audio Focus/Voice/TTS 상태가 Infotainment 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_DIAG_001 | 테스트/진단 요청-응답 및 결과 기록이 시나리오 종료까지 추적 가능하게 유지되는지 확인한다. |  |  |  |
| ST_BASE_001 | 차량 기본 기능(시동/기어/가감속/조향/비상등/창문/기본표시/도메인경계)이 시스템 수준에서 일관되게 동작하는지 확인한다. |  |  |  |

---

## 시스템 테스트 추적 상세 표

| ST ID | Req ID | VC ID | 관련 Func | 관련 Flow/Comm | 관련 Var | 선행 IT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| ST_SPEED_001 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010 | VC_001,VC_002,VC_003,VC_004,VC_006,VC_010 | Func_001,Func_002,Func_003,Func_004,Func_006,Func_010 | Flow_001,Flow_003 / Comm_001,Comm_003 | Var_012,Var_013,Var_016,Var_031 | IT_CORE_001 | 입력 변동 후 `150ms` 이내 경고 활성/해제 상태가 요구와 일치(`vehicleSpeed > speedLimit`) |
| ST_ZONE_001 | Req_007,Req_008,Req_009 | VC_007,VC_008,VC_009 | Func_007,Func_008,Func_009 | Flow_003,Flow_007 / Comm_003,Comm_007 | Var_015,Var_021 | IT_CORE_001, IT_OUT_001 | 구간 전환 후 `150ms` 이내 정책 반영, 출력 주기 `50ms` 유지 |
| ST_GUIDE_001 | Req_014,Req_039 | VC_014,VC_039 | Func_014,Func_039 | Flow_003,Flow_007 / Comm_003,Comm_007 | Var_005,Var_023 | IT_CORE_001, IT_OUT_001 | 좌/우 방향 구분 패턴이 명확히 출력 |
| ST_GUIDE_002 | Req_013,Req_015,Req_016,Req_037,Req_038 | VC_013,VC_015,VC_016,VC_037,VC_038 | Func_013,Func_015,Func_016,Func_037,Func_038 | Flow_007 / Comm_007 | Var_021,Var_022,Var_023 | IT_OUT_001, IT_TIMEOUT_001 | 진입/전환/종료 시 깜빡임 없이 복귀 |
| ST_STEER_001 | Req_011,Req_012 | VC_011,VC_012 | Func_011,Func_012 | Flow_002 / Comm_002 | Var_014,Var_016 | IT_CORE_001 | 무조향 경고 발생/해제가 각각 `150ms` 이내 반영 |
| ST_EMS_001 | Req_017,Req_019,Req_020,Req_021,Req_022 | VC_017,VC_019,VC_020,VC_021,VC_022 | Func_017,Func_019,Func_020,Func_021,Func_022 | Flow_004,Flow_006,Flow_008 / Comm_004,Comm_006,Comm_008 | Var_007,Var_008,Var_024 | IT_EMS_001, IT_ARB_001, IT_OUT_001 | 경찰 긴급 접근 입력 후 `150ms` 이내 우선 경고 및 HMI 표시 |
| ST_EMS_002 | Req_018,Req_019,Req_020,Req_021,Req_022 | VC_018,VC_019,VC_020,VC_021,VC_022 | Func_018,Func_019,Func_020,Func_021,Func_022 | Flow_005,Flow_006,Flow_008 / Comm_005,Comm_006,Comm_008 | Var_007,Var_008,Var_024 | IT_EMS_001, IT_ARB_001, IT_OUT_001 | 구급 긴급 접근 입력 후 `150ms` 이내 우선 경고 및 HMI 표시 |
| ST_HMI_DIR_001 | Req_020 | VC_020 | Func_020 | Flow_008 / Comm_008 | Var_024 | IT_OUT_001 | 경찰 방향 정보가 클러스터 경고 코드로 정확히 반영 |
| ST_HMI_DIR_002 | Req_020 | VC_020 | Func_020 | Flow_008 / Comm_008 | Var_024 | IT_OUT_001 | 구급 방향 정보가 클러스터 경고 코드로 정확히 반영 |
| ST_ARB_ETA_001 | Req_030,Req_031 | VC_030,VC_031 | Func_030,Func_031 | Flow_006 / Comm_006 | Var_009,Var_010,Var_019 | IT_ARB_001 | 경찰 알림 충돌 시 ETA 우선, 동률 시 SourceID 우선 적용 |
| ST_ARB_ETA_002 | Req_029,Req_030,Req_031 | VC_029,VC_030,VC_031 | Func_029,Func_030,Func_031 | Flow_006 / Comm_006 | Var_007,Var_009,Var_010,Var_019 | IT_ARB_001 | 구급/경찰 충돌 시 구급 우선 후 ETA/SourceID 규칙 적용 |
| ST_TIMEOUT_001 | Req_023,Req_024,Req_033,Req_034 | VC_023,VC_024,VC_033,VC_034 | Func_023,Func_024,Func_033,Func_034 | Flow_006,Flow_007,Flow_008 / Comm_006,Comm_007,Comm_008 | Var_017,Var_020,Var_021,Var_024 | IT_TIMEOUT_001 | `1000ms` 무갱신 해제 후 `150ms` 이내 복귀/완화 동작 정상 |
| ST_POLICY_001 | Req_005,Req_025,Req_026,Req_027,Req_028,Req_032,Req_035,Req_036,Req_040 | VC_005,VC_025,VC_026,VC_027,VC_028,VC_032,VC_035,VC_036,VC_040 | Func_005,Func_025,Func_026,Func_027,Func_028,Func_032,Func_035,Func_036,Func_040 | Flow_006,Flow_007,Flow_008 / Comm_006,Comm_007,Comm_008 | Var_018,Var_019,Var_022,Var_023,Var_024,Var_028,Var_029 | IT_ARB_001, IT_OUT_001 | 중재/표시 정책과 결정론이 요구 기준을 충족 |
| ST_SIL_001 | Req_041 | VC_041 | Func_041 | Flow_009 / Comm_009 | Var_025 | IT_SIL_001 | CANoe SIL 단독 환경에서 시나리오 실행 가능 |
| ST_SIL_002 | Req_042 | VC_042 | Func_042 | Flow_001~Flow_009 / Comm_001~Comm_009 | Var_001~Var_031 | IT_SIL_001 | CAN+Ethernet 동시 조건에서 통신/기능 체인 유지 |
| ST_RESULT_001 | Req_043 | VC_043 | Func_043 | Flow_009 / Comm_009 | Var_026 | IT_SIL_001 | 결과 판정 로그와 요약 상태가 일치 |
| ST_BASE_PT_001 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | Func_101,Func_102,Func_110 | Flow_101,Flow_204,Flow_105 / Comm_101,Comm_204,Comm_105 | Var_175~Var_182,Var_298~Var_304,Var_309~Var_314 | IT_BASE_PT_001 | 시동/기어 전환 후 동력계 상태가 `150ms` 이내 반영되고 도메인 경계 연동이 유지 |
| ST_BASE_CH_001 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | Func_103,Func_104,Func_105,Func_110 | Flow_102,Flow_201,Flow_105 / Comm_102,Comm_201,Comm_105 | Var_101~Var_120,Var_204~Var_237 | IT_BASE_CH_001 | 가감속/조향/제동 입력 이벤트가 안전 규칙대로 반영되고 상태 연동이 유지 |
| ST_BASE_BODY_001 | Req_106,Req_107,Req_108,Req_111 | VC_106,VC_107,VC_108,VC_111 | Func_106,Func_107,Func_108,Func_111 | Flow_103,Flow_202,Flow_105 / Comm_103,Comm_202,Comm_105 | Var_121~Var_146,Var_238~Var_267 | IT_BASE_BODY_001 | 비상등/창문/운전자상태 시나리오에서 출력과 상태가 기대값으로 유지 |
| ST_BASE_IVI_001 | Req_109,Req_111 | VC_109,VC_111 | Func_109,Func_111 | Flow_104,Flow_203,Flow_105 / Comm_104,Comm_203,Comm_105 | Var_147~Var_171,Var_268~Var_297 | IT_BASE_IVI_001 | 표시/UI 이벤트가 누락 없이 반영되고 50/100ms 주기 규칙을 만족 |
| ST_BASE_EXT_BODY_001 | Req_113,Req_114,Req_115,Req_116,Req_117,Req_118 | VC_113,VC_114,VC_115,VC_116,VC_117,VC_118 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Flow_202,Flow_105 / Comm_202,Comm_105 | Var_238~Var_267 | IT_BASE_EXT_BODY_001 | HVAC/Seat/Mirror/Door/Wiper-Rain/Security 상태가 `150ms` 이내 반영되고 범위/매핑 규칙을 만족 |
| ST_BASE_EXT_IVI_001 | Req_119 | VC_119 | Func_119 | Flow_203,Flow_105 / Comm_203,Comm_105 | Var_268~Var_271,Var_289~Var_290 | IT_BASE_EXT_IVI_001 | Audio Focus/Voice/TTS 상태가 `150ms` 이내 HMI 정책으로 반영되고 50/100ms 주기 규칙을 만족 |
| ST_BASE_DIAG_001 | Req_112 | VC_112 | Func_112 | Flow_106,Flow_205 / Comm_106,Comm_205 | Var_172~Var_174 | IT_BASE_DIAG_001 | 진단 요청-응답 및 결과 로그가 시나리오 단위로 추적 가능하게 기록 |
| ST_BASE_001 | Req_101~Req_119 | VC_101~VC_119 | Func_101~Func_119 | Flow_101~Flow_106,Flow_201~Flow_205 / Comm_101~Comm_106,Comm_201~Comm_205 | Var_101~Var_314 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001, IT_BASE_EXT_BODY_001, IT_BASE_EXT_IVI_001, IT_BASE_DIAG_001 | 차량 기본 기능 E2E 시나리오에서 입력/상태/표시/경계/판정 체인이 일관되게 유지 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 5.10 | 2026-03-02 | 차량 기본 기능 확장 추적 보강: `Req/VC/Func_113~119`를 반영한 `ST_BASE_EXT_BODY_001`, `ST_BASE_EXT_IVI_001` 추가 및 `ST_BASE_001` 범위 확장(Req_101~119). |
| 5.9 | 2026-03-02 | 증적 경로 규칙 고정: ST 실행 증적 저장 경로를 `canoe/logging/evidence/ST/`로 명시. |
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-23 | 구버전 Scene 구조 반영 |
| 3.0 | 2026-02-23 | 운전자 행동 중심 서술 전환 |
| 4.0 | 2026-02-24 | 구버전 OTA 시나리오 확장 |
| 5.0 | 2026-02-26 | 옵션1 아키텍처/Req_001~043 기준으로 전면 재작성. ST ID 체계 및 IT-Req 추적표 추가 |
| 5.1 | 2026-02-26 | 합격 기준을 150ms/1000ms 및 주기 기준으로 수치화하고, FZ 사전 점검 결과 반영 전 Draft 경계 문구 추가 |
| 5.2 | 2026-02-26 | VC 추적 강화를 위해 ST 상세 표에 VC ID 컬럼을 추가하고 Req-VC-ST 연결을 명시 |
| 5.3 | 2026-02-28 | ST_SPEED_001에 `speedLimit` 기반 과속 조건과 Flow_003/Comm_003/Var_031 연계를 반영. |
| 5.4 | 2026-02-28 | 차량 기본 기능 시스템 검증을 위해 `ST_BASE_001`(Req/VC/Func 101~112, Flow/Comm 101~106 및 201~205)을 추가. |
| 5.5 | 2026-02-28 | 06 문서 Lean IT 재구성 반영: ST 선행 IT 참조를 핵심 통합 체인(`IT_CORE/EMS/ARB/OUT/TIMEOUT/SIL/BASE`)으로 정렬. |
| 5.6 | 2026-02-28 | Lean IT 재구성 후 잔여 참조 ID 정리(`ST_POLICY_001` 선행 IT에서 구 ID 제거) 및 최신 IT 체계 동기화. |
| 5.7 | 2026-02-28 | 차량 기본 기능 확장 반영: `ST_BASE_001` 선행 IT를 도메인별 통합 ID(`IT_BASE_PT/CH/BODY/IVI/DIAG`)까지 연결. |
| 5.8 | 2026-02-28 | 확장된 요구/통신 기준 반영: 도메인별 시스템 시나리오(`ST_BASE_PT/CH/BODY/IVI/DIAG`) 추가 및 ST 작성원칙을 블랙박스(E2E) 중심으로 정렬. |

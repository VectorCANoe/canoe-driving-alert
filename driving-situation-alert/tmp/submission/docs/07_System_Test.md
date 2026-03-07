# 시스템 테스트 (System Test)

**Document ID**: PROJ-07-ST
**ISO 26262 Reference**: Part 4, Cl.10 (System Integration and System Qualification Test)
**ASPICE Reference**: SYS.5 (System Qualification Test)
**Version**: 5.19
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 상단 (SYS.5) | `07_System_Test.md` | `06_Integration_Test.md`, `01_Requirements.md` | 릴리즈/검수 |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 운전자 관점 E2E 시스템 시나리오(ST)를 정리한다.
- 제출본은 상단 공식 ST 표를 유지하고, 상세 추적은 대표 항목만 유지한다.
- 전수 ST/증빙 상세는 원문 07에서 관리한다.
- 판정 기준은 사용자 관찰 결과 중심으로 유지한다.
- Pre-Activation 라벨은 원문과 동일하게 유지한다.
- 대조군/우수성 비교 실험은 제출본 범위 밖으로 두고 Pass/Fail 중심으로 제시한다.
- 검증 배치 실행/리포트 생성은 `scripts/run.py verify batch` 기준(기본 `json,md`, 옵션 `csv`)으로 운영한다.

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
| ST_SIL_002 | CAN+Ethernet(또는 CAN 대체 백본) 동시 통신 조건에서 E2E 경고 체인이 유지되는지 확인한다. |  |  |  |
| ST_RESULT_001 | 시나리오별 합격/불합격 결과가 일관되게 기록·추적되는지 확인한다. |  |  |  |
| ST_BASE_PT_001 | 시동/기어/동력계 상태가 Powertrain 시나리오에서 안정적으로 연동되는지 확인한다. |  |  |  |
| ST_BASE_CH_001 | 가감속/조향/제동 입력이 Chassis 시나리오에서 안전 규칙대로 반영되는지 확인한다. |  |  |  |
| ST_BASE_BODY_001 | 비상등/창문 등 Body 시나리오가 의도한 동작으로 유지되는지 확인한다. |  |  |  |
| ST_BASE_IVI_001 | 클러스터 기본표시/안내/UI 상태가 Infotainment 시나리오에서 일관되게 유지되는지 확인한다. |  |  |  |
| ST_BASE_EXT_BODY_001 | HVAC/Seat/Mirror/Door/Wiper-Rain/Security 상태가 Body 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_EXT_IVI_001 | Audio Focus/Voice/TTS 상태가 Infotainment 확장 시나리오에서 일관되게 반영되는지 확인한다. |  |  |  |
| ST_BASE_DIAG_001 | 테스트/진단 요청-응답 및 결과 기록이 시나리오 종료까지 추적 가능하게 유지되는지 확인한다. |  |  |  |
| ST_V2_RISK_001 | 긴급차량 근접 위험도 기반 감속 보조 요청과 경고 출력 동기화가 일관되게 동작하는지 확인한다. (SIL Scenario 15/16/17/19) | Ready |  |  |
| ST_V2_FAILSAFE_001 | 도메인 경로 단절 시 자동 감속 보조 금지와 최소 경고 채널 유지 강등이 동작하는지 확인한다. (SIL Scenario 18) | Ready |  |  |
| ST_ADAS_OBJ_001 | 객체 목록 기반 TTC/교차로/합류 위험 경고와 신뢰도 저하 강등/이벤트 기록이 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_ALERT_EXT_001 | 방향지시등/주행모드/안전벨트 입력 기반 경보 보정, 접근거리 표시, 이벤트 기록·조회, 표시/음량 설정 반영이 E2E로 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_ROBUST_EXT_001 | 입력 유효성/신선도 보호, 상태전이 안정화, 채널 가용성·대체 출력, 오디오 경합/팝업 과밀/채널 동기 복원 정책이 E2E로 일관되게 동작하는지 확인한다. (Pre-Activation) | Planned |  |  |
| ST_BASE_001 | 차량 기본 기능(시동/기어/가감속/조향/비상등/창문/기본표시/도메인경계)이 시스템 수준에서 일관되게 동작하는지 확인한다. |  |  |  |

---

## 시스템 테스트 추적 상세 표

| ST ID | Req ID | VC ID | 관련 Func | 관련 Flow/Comm | 관련 Var | 선행 IT | 합격 기준 |
|---|---|---|---|---|---|---|---|
| ST_SPEED_001 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010 | VC_001,VC_002,VC_003,VC_004,VC_006,VC_010 | Func_001,Func_002,Func_003,Func_004,Func_006,Func_010 | Flow_001,Flow_003 / Comm_001,Comm_003 | Var_012,Var_013,Var_016,Var_031 | IT_CORE_001 | 입력 변동 후 `150ms` 이내 경고 활성/해제 상태가 요구와 일치(`vehicleSpeed > speedLimit`) |
| ST_ZONE_001 | Req_007,Req_008,Req_009 | VC_007,VC_008,VC_009 | Func_007,Func_008,Func_009 | Flow_003,Flow_007 / Comm_003,Comm_007 | Var_015,Var_021 | IT_CORE_001, IT_OUT_001 | 구간 전환 후 `150ms` 이내 정책 반영, 출력 주기 `50ms` 유지 |
| ST_GUIDE_001 | Req_014,Req_037 | VC_014,VC_037 | Func_014,Func_039 | Flow_003,Flow_007 / Comm_003,Comm_007 | Var_005,Var_023 | IT_CORE_001, IT_OUT_001 | 좌/우 방향 구분 패턴이 명확히 출력 |
| ST_GUIDE_002 | Req_013,Req_015,Req_016,Req_037 | VC_013,VC_015,VC_016,VC_037 | Func_013,Func_015,Func_016,Func_037,Func_038 | Flow_007 / Comm_007 | Var_021,Var_022,Var_023 | IT_OUT_001, IT_TIMEOUT_001 | 진입/전환/종료 시 깜빡임 없이 복귀 |
| ST_STEER_001 | Req_011,Req_012 | VC_011,VC_012 | Func_011,Func_012 | Flow_002 / Comm_002 | Var_014,Var_016 | IT_CORE_001 | 무조향 경고 발생/해제가 각각 `150ms` 이내 반영 |
| ST_EMS_001 | Req_017,Req_019,Req_020,Req_021,Req_022 | VC_017,VC_019,VC_020,VC_021,VC_022 | Func_017,Func_019,Func_020,Func_021,Func_022 | Flow_004,Flow_006,Flow_008 / Comm_004,Comm_006,Comm_008 | Var_007,Var_008,Var_024 | IT_EMS_001, IT_ARB_001, IT_OUT_001 | 경찰 긴급 접근 입력 후 `150ms` 이내 우선 경고 및 HMI 표시 |
| ST_EMS_002 | Req_017,Req_019,Req_020,Req_021,Req_022 | VC_017,VC_019,VC_020,VC_021,VC_022 | Func_018,Func_019,Func_020,Func_021,Func_022 | Flow_005,Flow_006,Flow_008 / Comm_005,Comm_006,Comm_008 | Var_007,Var_008,Var_024 | IT_EMS_001, IT_ARB_001, IT_OUT_001 | 구급 긴급 접근 입력 후 `150ms` 이내 우선 경고 및 HMI 표시 |
| ST_HMI_DIR_001 | Req_020 | VC_020 | Func_020 | Flow_008 / Comm_008 | Var_024 | IT_OUT_001 | 경찰 방향 정보가 클러스터 경고 코드로 정확히 반영 |
| ST_HMI_DIR_002 | Req_020 | VC_020 | Func_020 | Flow_008 / Comm_008 | Var_024 | IT_OUT_001 | 구급 방향 정보가 클러스터 경고 코드로 정확히 반영 |
| ST_ARB_ETA_001 | Req_030,Req_031 | VC_030,VC_031 | Func_030,Func_031 | Flow_006 / Comm_006 | Var_009,Var_010,Var_019 | IT_ARB_001 | 경찰 알림 충돌 시 ETA 우선, 동률 시 SourceID 우선 적용 |
| ST_ARB_ETA_002 | Req_029,Req_030,Req_031 | VC_029,VC_030,VC_031 | Func_029,Func_030,Func_031 | Flow_006 / Comm_006 | Var_007,Var_009,Var_010,Var_019 | IT_ARB_001 | 구급/경찰 충돌 시 구급 우선 후 ETA/SourceID 규칙 적용 |
| ST_TIMEOUT_001 | Req_023,Req_024,Req_033,Req_034 | VC_023,VC_024,VC_033,VC_034 | Func_023,Func_024,Func_033,Func_034 | Flow_006,Flow_007,Flow_008 / Comm_006,Comm_007,Comm_008 | Var_017,Var_020,Var_021,Var_024 | IT_TIMEOUT_001 | `1000ms` 무갱신 해제 후 `150ms` 이내 복귀/완화 동작 정상 |
| ST_POLICY_001 | Req_005,Req_025,Req_026,Req_027,Req_028,Req_032,Req_035,Req_040 | VC_005,VC_025,VC_026,VC_027,VC_028,VC_032,VC_035,VC_040 | Func_005,Func_025,Func_026,Func_027,Func_028,Func_032,Func_035,Func_036,Func_040 | Flow_006,Flow_007,Flow_008 / Comm_006,Comm_007,Comm_008 | Var_018,Var_019,Var_022,Var_023,Var_024,Var_028,Var_029 | IT_ARB_001, IT_OUT_001 | 중재/표시 정책과 결정론이 요구 기준을 충족 |
| ST_SIL_001 | Req_041 | VC_041 | Func_041 | Flow_009 / Comm_009 | Var_025 | IT_SIL_001 | CANoe SIL 단독 환경에서 시나리오 실행 가능 |
| ST_SIL_002 | Req_042 | VC_042 | Func_042 | Flow_001~Flow_009 / Comm_001~Comm_009 | Var_001~Var_031 | IT_SIL_001 | CAN+Ethernet(또는 CAN 대체 백본) 동시 조건에서 통신/기능 체인 유지 |
| ST_RESULT_001 | Req_043 | VC_043 | Func_043 | Flow_009 / Comm_009 | Var_026 | IT_SIL_001 | 결과 판정 로그와 요약 상태가 일치 |
| ST_BASE_PT_001 | Req_101,Req_102,Req_110 | VC_101,VC_102,VC_110 | Func_101,Func_102,Func_110 | Flow_101,Flow_204,Flow_105 / Comm_101,Comm_204,Comm_105 | Var_175~Var_182,Var_298~Var_304,Var_309~Var_314 | IT_BASE_PT_001 | 시동/기어 전환 후 동력계 상태가 `150ms` 이내 반영되고 도메인 경계 연동이 유지 |
| ST_BASE_CH_001 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | Func_103,Func_104,Func_105,Func_110 | Flow_102,Flow_201,Flow_105 / Comm_102,Comm_201,Comm_105 | Var_101~Var_120,Var_204~Var_237 | IT_BASE_CH_001 | 가감속/조향/제동 입력 이벤트가 안전 규칙대로 반영되고 상태 연동이 유지 |
| ST_BASE_BODY_001 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | Func_106,Func_107,Func_111 | Flow_103,Flow_202,Flow_105 / Comm_103,Comm_202,Comm_105 | Var_121~Var_146,Var_238~Var_267 | IT_BASE_BODY_001 | 비상등/창문 시나리오에서 출력과 상태가 기대값으로 유지 |
| ST_BASE_IVI_001 | Req_109,Req_111 | VC_109,VC_111 | Func_109,Func_111 | Flow_104,Flow_203,Flow_105 / Comm_104,Comm_203,Comm_105 | Var_147~Var_171,Var_268~Var_297 | IT_BASE_IVI_001 | 표시/UI 이벤트가 누락 없이 반영되고 50/100ms 주기 규칙을 만족 |
| ST_BASE_EXT_BODY_001 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Flow_202,Flow_105 / Comm_202,Comm_105 | Var_238~Var_267 | IT_BASE_EXT_BODY_001 | HVAC/Seat/Mirror/Door/Wiper-Rain/Security 상태가 `150ms` 이내 반영되고 범위/매핑 규칙을 만족 |
| ST_BASE_EXT_IVI_001 | Req_119 | VC_119 | Func_119 | Flow_203,Flow_105 / Comm_203,Comm_105 | Var_268~Var_271,Var_289~Var_290 | IT_BASE_EXT_IVI_001 | Audio Focus/Voice/TTS 상태가 `150ms` 이내 HMI 정책으로 반영되고 50/100ms 주기 규칙을 만족 |
| ST_BASE_DIAG_001 | Req_112 | VC_112 | Func_112 | Flow_106,Flow_205 / Comm_106,Comm_205 | Var_172~Var_174 | IT_BASE_DIAG_001 | 진단 요청-응답 및 결과 로그가 시나리오 단위로 추적 가능하게 기록 |
| ST_V2_RISK_001 | Req_120,Req_121,Req_125,Req_126,Req_123 | VC_120,VC_121,VC_125,VC_126,VC_123 | Func_120,Func_121,Func_125,Func_126,Func_123 | Flow_120,Flow_121,Flow_122,Flow_123 / Comm_120,Comm_121,Comm_122,Comm_123 | Var_320,Var_321,Var_322,Var_323,Var_324,Var_325 | IT_V2_RISK_001 | 위험도 산정 주기 `100ms`, 감속 보조 요청 생성/해제 `150ms` 이내, Ambient/Cluster 동기 오프셋 `<=50ms` (SIL Scenario 15/16/17/19) |
| ST_V2_FAILSAFE_001 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | Func_127,Func_128,Func_129 | Flow_124 / Comm_124 | Var_326,Var_327,Var_328,Var_329 | IT_V2_FAILSAFE_001 | 단절 감지 후 `150ms` 이내 failSafeMode 전환, 자동 감속 보조 0건, 최소 경고 채널 유지 (SIL Scenario 18) |
| ST_ADAS_OBJ_001 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_137,Req_138,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_137,VC_138,VC_139 | Func_130,Func_131,Func_132,Func_133,Func_134,Func_135,Func_136,Func_137,Func_138,Func_139 | Flow_130,Flow_131,Flow_132,Flow_133 / Comm_130,Comm_131,Comm_132,Comm_133 | Var_330,Var_331,Var_332,Var_333,Var_334,Var_335,Var_336,Var_337,Var_338,Var_339 | IT_ADAS_OBJ_001 | 객체 입력 반영 `100ms`, 경고/강등 반영 `150ms`, 이벤트 기록 누락 0건 및 우선순위 결정론 유지(Pre-Activation) |
| ST_BASE_ALERT_EXT_001 | Req_140,Req_141,Req_142,Req_143,Req_144,Req_145,Req_146,Req_147 | VC_140,VC_141,VC_142,VC_143,VC_144,VC_145,VC_146,VC_147 | Func_140,Func_141,Func_142,Func_143,Func_144,Func_145,Func_146,Func_147 | Flow_103,Flow_104,Flow_105,Flow_203,Flow_006,Flow_008 / Comm_103,Comm_104,Comm_105,Comm_203,Comm_006,Comm_008 | Var_009,Var_012,Var_024,Var_029,Var_133,Var_138,Var_139,Var_141,Var_155,Var_164,Var_166,Var_167,Var_168,Var_191,Var_192,Var_193,Var_268,Var_281,Var_282 | IT_BASE_ALERT_EXT_001 | 맥락 보정/거리 표시/이력 조회/설정 반영 체인이 E2E에서 수치 기준(`150ms`,`200ms`)과 기록 기준(누락 0건)을 충족(Pre-Activation) |
| ST_BASE_ROBUST_EXT_001 | Req_148,Req_149,Req_150,Req_151,Req_152,Req_153,Req_154,Req_155 | VC_148,VC_149,VC_150,VC_151,VC_152,VC_153,VC_154,VC_155 | Func_148,Func_149,Func_150,Func_151,Func_152,Func_153,Func_154,Func_155 | Flow_130,Flow_133,Flow_006,Flow_007,Flow_008,Flow_104,Flow_105,Flow_124,Flow_203 / Comm_130,Comm_133,Comm_006,Comm_007,Comm_008,Comm_104,Comm_105,Comm_124,Comm_203 | Var_330,Var_333,Var_334,Var_016,Var_020,Var_021,Var_024,Var_027,Var_028,Var_166,Var_167,Var_168,Var_180,Var_268,Var_269,Var_289,Var_296,Var_297,Var_326,Var_327,Var_328,Var_282 | IT_BASE_ROBUST_EXT_001 | 입력 유효성 필터링 `100ms`, stale/전이 안정화 `150ms`, 채널 가용성·대체 출력 `150ms`, 오디오 경합·팝업 과밀·채널 동기 복원 `150ms` 기준 충족(Pre-Activation) |
| ST_BASE_001 | Req_101~Req_107,Req_109~Req_119 | VC_101~VC_107,VC_109~VC_119 | Func_101~Func_107,Func_109~Func_119 | Flow_101~Flow_106,Flow_201~Flow_205 / Comm_101~Comm_106,Comm_201~Comm_205 | Var_101~Var_314 | IT_BASE_001, IT_BASE_PT_001, IT_BASE_CH_001, IT_BASE_BODY_001, IT_BASE_IVI_001, IT_BASE_EXT_BODY_001, IT_BASE_EXT_IVI_001, IT_BASE_DIAG_001 | 차량 기본 기능 E2E 시나리오에서 입력/상태/표시/경계/판정 체인이 일관되게 유지 |

---

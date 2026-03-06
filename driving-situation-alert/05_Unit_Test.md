# 단위 테스트 (Unit Test)

**Document ID**: PROJ-05-UT
**ISO 26262 Reference**: Part 6, Cl.9 (Software Unit Verification)
**ASPICE Reference**: SWE.4 (Software Unit Verification)
**Version**: 2.18
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 우측 하단 (SWE.4) | `05_Unit_Test.md` | `04_SW_Implementation.md` | `06_Integration_Test.md` |

---

## 작성 원칙

- 본 문서는 모듈 단위 검증(유닛 단위) 결과를 정의한다.
- 공식 상단 표는 샘플 형식(`노드/분류/기능명/기능 설명/Pass/담당자/일자`)을 유지한다.
- 상단 공식 표는 감사 일관성을 위해 `EMS_ALERT` 논리 단말 기준으로 표기한다.
- 상세 추적(UT ID, Req/VC/Func/Flow/Comm/Var)은 하단 표로 분리한다.
- 범위 외 항목(OTA/UDS/DoIP)은 포함하지 않는다.
- 본 문서는 `FZ_001~FZ_012` 결과 반영 전 Baseline Draft이며, 측정값 확정 시 Pass/Fail를 기입한다.
- 임시 주석(실행 제약): 현재 CANoe.CAN 라이선스 환경에서는 SIL 실행 시 Ethernet 구간을 CAN 대체 백본으로 검증하며, Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL` 관련 항목은 Validation Harness(검증 전용)이며 양산 사용자 기능으로 해석하지 않는다.
- UT 증적(로그/캡처/리포트)은 `canoe/logging/evidence/UT/` 경로 규칙으로 관리한다.
- UT 증적 포맷/채점 규칙은 `canoe/docs/operations/VERIFICATION_EVIDENCE_LOG_STANDARD.md`를 따른다.
- V2 확장 요구(`Req_120~Req_121, Req_123, Req_125~Req_129`)는 구현 활성 상태로 UT 항목을 관리하며, SIL 시나리오 15~19를 기준 케이스로 운영한다.
- ADAS 객체 인지 확장(`Req_130~Req_139`)은 Pre-Activation(설계 선반영) UT 항목(`UT_ADAS_OBJ_RISK_001`, `UT_ADAS_OBJ_SAFETY_001`)으로 관리한다.

### 수치화 기준 (Req/Flow 파생)

- `즉시` 요구는 기본적으로 `100ms 입력 주기 + 50ms 출력 주기`를 합산한 `150ms 이내` 반영으로 판정한다.
- 타임아웃 요구는 `Req_024`에 따라 `1000ms`를 절대 기준으로 판정한다.
- 주기 정합은 입력 `100ms`, 출력 `50ms`를 기준으로 판정한다.

### 현업 기준 최소 설계 규칙 (ASPICE SWE.4 반영)

- UT는 `Positive / Negative / Boundary` 3분류를 최소 유지한다.
- `UT 개수 >= Func 개수`는 필수 조건이 아니다. 필수 조건은 `Req/VC 추적 커버리지 100%`다.
- UT 사양에는 최소 `입력 조건`, `예상 결과`, `판정 기준(수치/조건)`을 포함한다.
- 추적성은 `소프트웨어 상세설계(03) -> UT 사양(05) -> UT 결과(실행 로그)` 양방향으로 유지한다.

---

## 단위 테스트 표 (공식 표준 양식)

| 노드 | 분류 | 기능명 | 기능 설명 | Pass/Fail | 담당자 | 일자 |
|---|---|---|---|---|---|---|
| 제어기 | 제어 | CHS_GW | CAN(0x2A0/0x2A1) 수신값을 ETH(0x510/0x511)로 100ms 주기 변환 송신 |  |  |  |
|  |  | INFOTAINMENT_GW | CAN(0x2A3) 구간/방향/거리/제한속도 입력을 ETH(0x512)로 100ms 주기 변환 송신 |  |  |  |
|  |  | ADAS_WARN_CTRL | 주행/비주행, 과속(vehicleSpeed>speedLimit), 무조향 조건을 판정해 150ms 이내 경고 상태 반영 |  |  |  |
|  |  | ADAS_WARN_CTRL + WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR (V2 확장) | 긴급차량 방향/ETA/자차속도 기반 위험도 산정, 감속 보조 요청/해제, Fail-safe 강등 동기화 | Ready |  |  |
|  |  | ADAS_WARN_CTRL + WARN_ARB_MGR + DOMAIN_BOUNDARY_MGR (ADAS 객체 확장, Planned) | 객체 목록 수용, TTC/상대속도 기반 단계화, 교차로/합류 위험 경고, 신뢰도 저하 강등/이벤트 기록 | Planned |  |  |
|  |  | NAV_CTX_MGR | roadZone/navDirection/zoneDistance/speedLimit 입력으로 컨텍스트 계산 및 speedLimitNorm 갱신 |  |  |  |
|  |  | EMS_ALERT | 경찰/구급 긴급 이벤트의 송신/수신/해제/타임아웃(1000ms) 모듈 로직을 유닛 단위로 검증 |  |  |  |
|  |  | WARN_ARB_MGR | Emergency>Zone, Ambulance>Police, ETA, SourceID 규칙으로 단일 경고 결과 결정 |  |  |  |
|  |  | BODY_GW | 중재 결과(E200)를 Ambient CAN(0x289)으로 50ms 주기 변환 송신 |  |  |  |
|  |  | IVI_GW | 중재 결과(E200)를 Cluster CAN(0x280)으로 50ms 주기 변환 송신 |  |  |  |
|  |  | AMBIENT_CTRL | selectedAlert 결과에 따라 ambientMode/color/pattern 정책 출력(전환 안정화 포함) |  |  |  |
|  |  | CLU_HMI_CTRL | warningTextCode/방향 표시/중복팝업 억제 정책 적용 |  |  |  |
|  |  | VAL_SCENARIO_CTRL | testScenario 실행, 통신 조건(CAN+Ethernet 또는 대체 백본) 판정, scenarioResult 기록 |  |  |  |
|  |  | VAL_BASELINE_CTRL | 차량 기본 기능(시동/기어/입력/표시) 단위 검증 및 결과 반영 |  |  |  |
| 가상 노드 (Simulator) | 입력 | Vehicle/Steering Input | `gVehicleSpeed`, `gDriveState`, `SteeringInput` 입력 생성 |  |  |  |
|  |  | Nav Context Input | `gRoadZone`, `gNavDirection`, `gZoneDistance`, `gSpeedLimit` 입력 생성 |  |  |  |
|  |  | Emergency Input | Police/Ambulance Active/Clear, ETA, Direction, SourceID 입력 생성 |  |  |  |
|  | 출력 | Ambient Output | `AmbientMode`, `AmbientColor`, `AmbientPattern` 출력 확인(50ms 주기) |  |  |  |
|  |  | Cluster Output | `WarningTextCode` 출력 확인(50ms 주기) |  |  |  |
|  |  | Scenario Result | `ScenarioResult` 및 로그 결과 확인 |  |  |  |

---

## 단위 테스트 추적 상세 표

| UT ID | 대상 모듈 | 검증 목적 | Req ID | VC ID | Func ID | Flow/Comm | Var ID | 합격 기준 |
|---|---|---|---|---|---|---|---|---|
| UT_ADAS_001 | ADAS_WARN_CTRL | 경고 시작/해제/디바운스 로직 검증 | Req_001,Req_002,Req_003,Req_004,Req_006,Req_010,Req_011,Req_012 | VC_001,VC_002,VC_003,VC_004,VC_006,VC_010,VC_011,VC_012 | Func_001,Func_002,Func_003,Func_004,Func_006,Func_010,Func_011,Func_012 | Flow_001,Flow_002,Flow_003 / Comm_001,Comm_002,Comm_003 | Var_012,Var_013,Var_014,Var_016,Var_031 | 입력 반영 후 `150ms` 이내 warningState 기대값 일치(입력 100ms + 출력 50ms) |
| UT_NAV_001 | NAV_CTX_MGR | 구간 컨텍스트 계산 검증 | Req_007,Req_010 | VC_007,VC_010 | Func_007,Func_010 | Flow_003 / Comm_003 | Var_004,Var_005,Var_006,Var_015,Var_030,Var_031 | 입력 조합별 baseZoneContext/speedLimitNorm 기대값 100% 일치 |
| UT_EMS_POL_001 | EMS_POLICE_TX | 경찰 긴급 송신 검증 | Req_017 | VC_017 | Func_017 | Flow_004 / Comm_004 | Var_007,Var_008,Var_009,Var_010,Var_011 | Active 시 `100ms` 주기 송신, Clear 전환 후 `150ms` 이내 반영 |
| UT_EMS_AMB_001 | EMS_AMB_TX | 구급 긴급 송신 검증 | Req_017 | VC_017 | Func_018 | Flow_005 / Comm_005 | Var_007,Var_008,Var_009,Var_010,Var_011 | Active 시 `100ms` 주기 송신, Clear 전환 후 `150ms` 이내 반영 |
| UT_EMS_RX_001 | EMS_ALERT_RX | 수신/해제/타임아웃 처리 검증 | Req_023,Req_024 | VC_023,VC_024 | Func_023,Func_024 | Flow_006 / Comm_006 | Var_017,Var_020,Var_027 | `1000ms` 무갱신 시 timeoutClear=1, clear 후 `150ms` 이내 출력 복귀 경로 반영 |
| UT_ARB_001 | WARN_ARB_MGR | 경보 우선순위 판정 검증 | Req_022,Req_025,Req_027,Req_028,Req_029,Req_030,Req_031,Req_032 | VC_022,VC_025,VC_027,VC_028,VC_029,VC_030,VC_031,VC_032 | Func_022,Func_025,Func_027,Func_028,Func_029,Func_030,Func_031,Func_032 | Flow_006 / Comm_006 | Var_018,Var_019,Var_029 | 우선순위/동률규칙 결정 결과가 시나리오 기대값과 일치 |
| UT_BCM_001 | AMBIENT_CTRL | 앰비언트 정책 검증 | Req_008,Req_009,Req_013,Req_014,Req_015,Req_016,Req_033,Req_034,Req_035,Req_037 | VC_008,VC_009,VC_013,VC_014,VC_015,VC_016,VC_033,VC_034,VC_035,VC_037 | Func_008,Func_009,Func_013,Func_014,Func_015,Func_016,Func_033,Func_034,Func_035,Func_036,Func_037,Func_038,Func_039 | Flow_007 / Comm_007 | Var_021,Var_022,Var_023 | 출력 `50ms` 주기 유지, 전환/복귀 시 불필요 토글 없이 정책표와 일치 |
| UT_CLU_001 | CLU_HMI_CTRL | 경고 문구 정책 검증 | Req_005,Req_019,Req_020,Req_021,Req_026,Req_040 | VC_005,VC_019,VC_020,VC_021,VC_026,VC_040 | Func_005,Func_019,Func_020,Func_021,Func_026,Func_040 | Flow_008 / Comm_008 | Var_024,Var_028 | 출력 `50ms` 주기 유지, 중복 억제 타이머 동작, 문구 정책 규칙 충족 |
| UT_GW_001 | CHS_GW, INFOTAINMENT_GW | 게이트웨이 변환 검증 | Req_007,Req_010,Req_011,Req_012 | VC_007,VC_010,VC_011,VC_012 | Func_007,Func_010,Func_011,Func_012 | Flow_001,Flow_002,Flow_003 / Comm_001,Comm_002,Comm_003 | Var_001~Var_006,Var_012~Var_015,Var_030,Var_031 | CAN 입력 대비 ETH 변환값 일치, 송신 주기 `100ms` 유지 |
| UT_OUT_GW_001 | BODY_GW, IVI_GW | ETH->CAN 출력 변환 검증 | Req_033,Req_034,Req_040 | VC_033,VC_034,VC_040 | Func_033,Func_034,Func_040 | Flow_007,Flow_008 / Comm_007,Comm_008 | Var_021~Var_024 | ETH 결과를 CAN 프레임으로 정확히 변환, CAN 출력 주기 `50ms` 유지 |
| UT_SIL_001 | VAL_SCENARIO_CTRL | SIL 실행/판정 유닛 검증 | Req_041,Req_042,Req_043 | VC_041,VC_042,VC_043 | Func_041,Func_042,Func_043 | Flow_009 / Comm_009 | Var_025,Var_026 | 시나리오 실행/통신 조건 검증/결과 기록 로직 정상 |
| UT_BASE_001 | ENG_CTRL,TCM,ACCEL_CTRL,BRK_CTRL,STEER_CTRL,HAZARD_CTRL,WINDOW_CTRL,DRV_STATE_MGR,CLU_BASE_CTRL,DOMAIN_ROUTER,DOMAIN_BOUNDARY_MGR,VAL_BASELINE_CTRL | 차량 기본 기능(시동/기어/입력/표시/도메인경계/SIL판정 + Body/IVI 확장 상태) 유닛 커버리지 총괄 검증 | Req_101~Req_107,Req_109~Req_119 | VC_101~VC_107,VC_109~VC_119 | Func_101~Func_107,Func_109~Func_119 | Flow_101~Flow_106,Flow_201~Flow_205 / Comm_101~Comm_106,Comm_201~Comm_205 | Var_101~Var_314 | 기본 기능 입력/표시/도메인경계/판정 동작이 요구 규칙과 일치 |
| UT_BASE_PT_001 | ENG_CTRL, TCM | 시동/기어/엔진/변속 기본 동작 검증 | Req_101,Req_102 | VC_101,VC_102 | Func_101,Func_102 | Flow_101,Flow_204 / Comm_101,Comm_204 | Var_175~Var_178,Var_181~Var_182,Var_189~Var_190,Var_298~Var_304,Var_309~Var_314 | 입력 반영 후 `150ms` 이내 상태/표시 일치, 주기 `100ms` 유지 |
| UT_BASE_CH_001 | ACCEL_CTRL, BRK_CTRL, STEER_CTRL, CHS_GW | 가감속/조향 입력 및 Chassis 상태 확장 동작 검증 | Req_103,Req_104,Req_105,Req_110 | VC_103,VC_104,VC_105,VC_110 | Func_103,Func_104,Func_105,Func_110 | Flow_102,Flow_201 / Comm_102,Comm_201 | Var_101~Var_120,Var_204~Var_237 | 입력 반영 후 `150ms` 이내 상태값 일치, 주기 `100ms` 유지 |
| UT_BASE_BODY_001 | HAZARD_CTRL, WINDOW_CTRL, DRV_STATE_MGR, BODY_GW | 차체 입력/출력(비상등/창문) 및 Body 확장 동작 검증 | Req_106,Req_107,Req_111 | VC_106,VC_107,VC_111 | Func_106,Func_107,Func_111 | Flow_103,Flow_202 / Comm_103,Comm_202 | Var_121~Var_146,Var_238~Var_267 | 상태 전이 규칙과 출력이 기대값 일치, 주기 `100ms` 유지 |
| UT_BASE_IVI_001 | CLU_BASE_CTRL, INFOTAINMENT_GW, IVI_GW | 클러스터 기본 표시 및 IVI 확장 동작 검증 | Req_109,Req_111 | VC_109,VC_111 | Func_109,Func_111 | Flow_104,Flow_203 / Comm_104,Comm_203 | Var_147~Var_171,Var_268~Var_297 | 표시 항목 누락 없음, `50/100ms` 주기 규칙 충족 |
| UT_BASE_EXT_BODY_001 | BODY_GW, DRV_STATE_MGR, WINDOW_CTRL, AMBIENT_CTRL | Body 확장 기능(HVAC/Seat/Mirror/Door/Wiper-Rain/Security) 유닛 검증 | Req_113,Req_116,Req_118 | VC_113,VC_116,VC_118 | Func_113,Func_114,Func_115,Func_116,Func_117,Func_118 | Flow_202 / Comm_202 | Var_238~Var_267 | 확장 상태/제어 프레임 수신 후 `150ms` 이내 정책 반영, 범위/매핑 규칙 일치 |
| UT_BASE_EXT_IVI_001 | CLU_HMI_CTRL, INFOTAINMENT_GW, IVI_GW | IVI 확장 기능(Audio Focus/Voice/TTS 상태) 유닛 검증 | Req_119 | VC_119 | Func_119 | Flow_203 / Comm_203 | Var_268~Var_271,Var_289~Var_290 | 오디오/음성 상태 수신 후 `150ms` 이내 HMI 정책 매핑 반영 |
| UT_BASE_GW_001 | DOMAIN_ROUTER, DOMAIN_BOUNDARY_MGR | 도메인 경계/라우팅 정책 적용 및 Health/Diag 경로 검증 | Req_110,Req_111 | VC_110,VC_111 | Func_110,Func_111 | Flow_105,Flow_205 / Comm_105,Comm_205 | Var_118~Var_120,Var_144~Var_146,Var_169~Var_171,Var_179~Var_180,Var_201~Var_203,Var_283~Var_286,Var_305~Var_308 | 도메인 경계 위반 없이 라우팅/진단 프레임이 규칙대로 전달 |
| UT_BASE_TEST_001 | VAL_BASELINE_CTRL, VAL_SCENARIO_CTRL | 차량 기본 기능 시나리오 실행/판정 기록 검증 | Req_112 | VC_112 | Func_112 | Flow_106 / Comm_106 | Var_172~Var_174,Var_025,Var_026 | 시나리오 실행 가능, 결과 판정/로그 일관성 유지 |
| UT_V2_RISK_001 | ADAS_WARN_CTRL, WARN_ARB_MGR | 긴급차량 근접 위험도 산정/감속 보조 요청/경고 동기화 검증 | Req_120,Req_121,Req_125,Req_126 | VC_120,VC_121,VC_125,VC_126 | Func_120,Func_121,Func_125,Func_126 | Flow_120,Flow_121,Flow_122 / Comm_120,Comm_121,Comm_122 | Var_320,Var_321,Var_322,Var_323 | 위험도 입력 갱신 후 `100ms` 주기 산정, 임계 초과 시 `150ms` 이내 감속 보조 요청 생성, 활성 상태에서 Ambient/Cluster 동기 오프셋 `<=50ms` (SIL Scenario 15/16/19) |
| UT_V2_RELEASE_001 | WARN_ARB_MGR | 운전자 개입(제동/조향) 시 감속 보조 요청 해제 검증 | Req_123 | VC_123 | Func_123 | Flow_123 / Comm_123 | Var_321,Var_324,Var_325 | 제동/조향 회피 입력 검출 후 `150ms` 이내 decelAssistReq=0 (SIL Scenario 17) |
| UT_V2_FAILSAFE_001 | DOMAIN_BOUNDARY_MGR | 도메인 경로 단절 시 자동 감속 보조 금지/강등 모드 전환 검증 | Req_127,Req_128,Req_129 | VC_127,VC_128,VC_129 | Func_127,Func_128,Func_129 | Flow_124 / Comm_124 | Var_326,Var_327,Var_328,Var_329 | 경로 단절 감지 후 `150ms` 이내 failSafeMode 전환, decelAssistReq=0 강제 유지 (SIL Scenario 18) |
| UT_ADAS_OBJ_RISK_001 | ADAS_WARN_CTRL, WARN_ARB_MGR | 객체 목록 수용/대표객체 선정/TTC·상대속도 단계화/교차로·합류 위험 경고/우선순위 정합 검증 | Req_130,Req_131,Req_132,Req_133,Req_134,Req_135,Req_136,Req_139 | VC_130,VC_131,VC_132,VC_133,VC_134,VC_135,VC_136,VC_139 | Func_130,Func_131,Func_132,Func_133,Func_134,Func_135,Func_136,Func_139 | Flow_130,Flow_131,Flow_132 / Comm_130,Comm_131,Comm_132 | Var_330,Var_331,Var_332,Var_334,Var_335,Var_336,Var_337,Var_338 | 객체 입력 후 `100ms` 내 위험 입력 반영, TTC 임계 시 `150ms` 내 경고 반영, 교차로/합류 분기 및 우선순위 결과가 규칙표와 일치 |
| UT_ADAS_OBJ_SAFETY_001 | DOMAIN_BOUNDARY_MGR, EMS_ALERT | 객체 신뢰도 저하 강등/자동감속 차단 및 객체 이벤트 기록 검증 | Req_137,Req_138 | VC_137,VC_138 | Func_137,Func_138 | Flow_133 / Comm_133 | Var_333,Var_334,Var_339 | 신뢰도 기준 미만 시 `150ms` 내 `decelAssistReq=0` 강제 및 강등 적용, 이벤트 로그 누락 0건 |

---

## 경계값 보강 케이스 (핵심)

| UT ID | 대상 | Req/VC | 케이스 유형 | 입력 조건 | 합격 기준 |
|---|---|---|---|---|---|
| UT_BND_024_A | EMS_ALERT_RX | Req_024 / VC_024 | Boundary- | 마지막 긴급 수신 후 `999ms` 경과 | `timeoutClear=0` 유지 |
| UT_BND_024_B | EMS_ALERT_RX | Req_024 / VC_024 | Boundary | 마지막 긴급 수신 후 `1000ms` 경과 | `timeoutClear=1` 단회 전환 |
| UT_BND_024_C | EMS_ALERT_RX | Req_024 / VC_024 | Boundary+ | 마지막 긴급 수신 후 `>1000ms` 유지 | 해제 상태 유지, 중복 토글 없음 |
| UT_BND_006_A | ADAS_WARN_CTRL | Req_006 / VC_006 | Boundary- | 동일 경고 재입력 간격 `<1000ms` | 재출력 억제 |
| UT_BND_006_B | ADAS_WARN_CTRL | Req_006 / VC_006 | Boundary | 동일 경고 재입력 간격 `=1000ms` | 재출력 1회 허용 |
| UT_BND_006_C | ADAS_WARN_CTRL | Req_006 / VC_006 | Boundary+ | 동일 경고 재입력 간격 `>1000ms` | 재출력 허용 |

---

## 06 연계 체크포인트

- `UT_*` 결과는 `06_Integration_Test.md`의 `IT_*` 시나리오 선행 조건으로 사용한다.
- `UT_EMS_RX_001`의 1000ms 타임아웃 결과는 `IT_TIMEOUT_001` 및 `IT_OUT_001`의 전제 조건이다.
- `UT_ADAS_OBJ_RISK_001`, `UT_ADAS_OBJ_SAFETY_001`은 `IT_ADAS_OBJ_001`(Pre-Activation)의 선행 조건으로 사용한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.18 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: `UT_ADAS_OBJ_RISK_001`, `UT_ADAS_OBJ_SAFETY_001`를 추가하고 `Req_130~Req_139` 추적 및 06 연계 체크포인트를 동기화. |
| 2.17 | 2026-03-06 | 미사용 체인 정리: `Req/VC/Func_108`을 `UT_BASE_001/UT_BASE_BODY_001` 추적 범위에서 제거하고 Baseline 범위를 `108 제외`로 동기화. |
| 2.16 | 2026-03-05 | Validation 노드 명칭을 `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`로 정리해 Req_041~043, Req_112 검증 체인 표기와 정합화. |
| 2.15 | 2026-03-03 | V2 UT를 구현 기준으로 전환: 대상 모듈을 `WARN_ARB_MGR` 중심으로 정정하고 SIL 시나리오 15~19 운용 기준을 반영. |
| 2.14 | 2026-03-03 | V2 추적 누락 보강: `UT_V2_RISK_001`에 `Req_125,Req_126/VC_125,VC_126/Func_125,Func_126/Flow_122/Comm_122/Var_322~323`를 포함해 05 문서 Req 커버리지를 닫음. |
| 2.13 | 2026-03-02 | V2 확장 제어 책임 분리 반영: V2 상단 항목을 `ADAS_WARN_CTRL + DECEL_ASSIST_CTRL`로 조정하고 `UT_V2_RISK_001/UT_V2_RELEASE_001` 대상 모듈을 정합화. |
| 2.12 | 2026-03-02 | V2 확장(Pre-Activation) UT 반영: `UT_V2_RISK_001`, `UT_V2_RELEASE_001`, `UT_V2_FAILSAFE_001` 추가 및 `Req_120~124` 추적 연계 반영. |
| 2.11 | 2026-03-02 | 작성 원칙에 CANoe.CAN 실행 제약(대체 백본 검증 후 Ethernet 재검증) 임시 주석을 추가하고, 상단 공식 표의 `EMS_ALERT`/`VAL_SCENARIO_CTRL` 설명을 유닛 검증 관점으로 정리. |
| 2.10 | 2026-03-02 | 차량 기본 기능 확장 추적 보강: `Req/VC/Func_113~119`를 `UT_BASE_001` 범위에 반영하고 `UT_BASE_EXT_BODY_001`, `UT_BASE_EXT_IVI_001`를 추가. |
| 2.9 | 2026-03-02 | 증적 경로 규칙 고정: UT 실행 증적 저장 경로를 `canoe/logging/evidence/UT/`로 명시. |
| 2.8 | 2026-03-01 | 상단 공식 표의 EMS 표기를 `EMS_ALERT` 논리 단말 기준으로 통일(내부 TX/RX 분해는 하단 UT 추적표 유지). |
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-26 | 옵션1 아키텍처 기준으로 전면 재작성. OTA/UDS/DoIP 항목 제거, UT ID 체계(UT_ADAS_001 등) 및 Req/Func/Flow/Comm/Var 추적 표 추가 |
| 2.1 | 2026-02-26 | 상단 표를 샘플의 블록형(제어기/가상노드 입력·출력) 구조로 재정렬하고, 합격 기준에 50ms/100ms/150ms/1000ms 수치 기준과 Draft 경계 문구를 반영 |
| 2.2 | 2026-02-26 | VC(Verification Criteria) 추적을 위해 UT 상세 표에 VC ID 컬럼을 추가하고 Req-VC-UT 연결을 명시 |
| 2.3 | 2026-02-28 | ASPICE SWE.4 기준 최소 케이스 설계 규칙(Positive/Negative/Boundary, 추적성)과 Req_024/Req_006 경계값 보강 케이스를 추가 |
| 2.4 | 2026-02-28 | 스쿨존 과속 정합을 위해 Nav 입력/UT 추적에 `speedLimit/speedLimitNorm`(Var_030/Var_031) 연계를 추가. |
| 2.5 | 2026-02-28 | 차량 기본 기능 확장 추적을 위해 `UT_BASE_001`(Req_101~112 / Func_101~112 / Comm_101~106,201~205)을 추가. |
| 2.6 | 2026-02-28 | 상단 공식 표를 기능/판정 기준 중심으로 구체화(100ms/50ms/150ms/1000ms)하고 차량 기본 기능 검증 항목을 반영. |
| 2.7 | 2026-02-28 | 단위 테스트 상세표에 차량 기본 기능 도메인 분해 케이스(`UT_BASE_PT/CH/BODY/IVI/GW/TEST`)를 추가해 ECU 기능 단위 검증을 강화. |

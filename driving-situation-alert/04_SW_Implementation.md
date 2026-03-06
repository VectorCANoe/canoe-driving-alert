# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 (Software Unit Design and Implementation)
**ASPICE Reference**: SWE.3 (Software Detailed Design and Unit Construction)
**Version**: 2.22
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 하단 (SWE.3) | `04_SW_Implementation.md` | `0304_System_Variables.md` | `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

---

## 작성 원칙

- 본 문서는 03/0301/0302/0303/0304 설계를 구현 단위(모듈/타이밍/예외처리)로 연결한다.
- 구현 상세는 코드 문법이 아니라 `입력/처리/출력/타이밍/예외` 계약으로 기록한다.
- 추적 체인은 `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`를 유지한다.
- 네트워크는 옵션1 아키텍처를 고정한다: `ETH_SW + CHS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 도메인 CAN`.
- 통신 원본은 분리 관리한다: CAN=`canoe/databases/chassis_can.dbc` + `canoe/databases/powertrain_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` (Validation frame `0x2A5/0x2A6`은 `chassis_can.dbc` 통합), Ethernet(논리 계약)=`canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`.
- 범위 외 항목(OTA/UDS/DoIP)은 구현 대상에서 제외한다.
- ASPICE SWE.3 BP1~BP8 관점에서 `상세 설계/인터페이스/동적행위/대안평가/추적성/합의/구현규칙`을 명시한다.
- SIL 단계에서는 Panel/sysvar 경유 자극을 허용하며, 통신 계약(0302/0303/0304)은 유지한 채 ETH `UdpSocket` 기반 입력으로 점진 전환한다.
- `VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`는 Validation Harness이며, `ETH_SW`/도메인 게이트웨이의 통신 변환 역할과 분리한다.
- ECU 명명 규칙은 `00e`를 SoT로 고정하고, RTE 생성명 규칙은 `00g_RTE_Name_Mapping_Standard.md`를 SoT로 고정한다.
- 본 문서는 `00e/00g` 정책의 구현 적용 참조 문서로 관리한다.
- 약어 충돌 방지 규칙: `EMS_AMB_TX`의 `AMB`는 `Ambulance` 의미의 구현 literal이며, `Ambient`는 항상 `AMBIENT` 풀토큰으로 표기한다.
- `project.sysvars`의 `UiRender/*`, `Test/*`, `V2X/policeDispatch`, `V2X/ambulanceDispatch`는 Verification-Harness 입력/렌더 변수로 관리하며 제품 Req 체인(01/03/05~07)과 분리한다.
- CANoe.CAN 환경에서는 Ethernet 일부 경로(E100/E200 모니터링 및 V2 확장)가 CAN-stub(0x1C0/0x1C1/0x1C2/0x1C3/0x1C4/0x111)로 대체 운반되며, 서비스 해석은 Ethernet 논리 계약 SoT를 우선한다.
- ADAS 객체 인지 확장(`Req_130~Req_139`)은 `Func_130~Func_139`, `Flow_130~Flow_133`, `Comm_130~Comm_133`, `Var_330~Var_339` Pre-Activation(설계 선반영) 상태로 유지하고 구현 착수 시 0302/0303/0304/05/06/07을 동일 커밋으로 동기화한다.
- 차량 경보 편의 확장(`Req_140~Req_147`)은 `Func_140~Func_147`, `Flow_103/104/105/203 + Flow_006/008`, `Comm_103/104/105/203 + Comm_006/008`, `Var_133/138~141/155/164/166~168/191~193/268/281/282` Pre-Activation(설계 선반영) 상태로 유지하고 구현 착수 시 0302/0303/0304/05/06/07을 동일 커밋으로 동기화한다.
- 경고 강건성·인지성 확장(`Req_148~Req_155`)은 `Func_148~Func_155`, `Flow_130/133 + Flow_006/007/008 + Flow_104/105/124/203`, `Comm_130/133 + Comm_006/007/008 + Comm_104/105/124/203`, `Var_330/333/334 + Var_016/020/021/024/027/028 + Var_180/326/327/328 + Var_166/167/168/268/269/289/296/297` Pre-Activation(설계 선반영) 상태로 유지하고 구현 착수 시 0302/0303/0304/05/06/07을 동일 커밋으로 동기화한다.
- Panel 구성은 `차량 화면 -> 제어 패널 -> 상태 모니터` 우선순위를 적용하고, UI는 표시/자극 전용 계층으로 유지한다.

---

## 1. 구현 아키텍처 요약

```text
Input CAN
  -> CHS_GW / INFOTAINMENT_GW (CAN->ETH 정규화)
  -> ETH_SW
  -> 중앙 경고코어 (ADAS_WARN_CTRL, NAV_CTX_MGR, EMS_ALERT, WARN_ARB_MGR)
  -> ETH_SW
  -> BODY_GW / IVI_GW (ETH->CAN 변환)
  -> AMBIENT_CTRL / CLU_HMI_CTRL

Emergency Source (logical terminal)
  -> EMS_ALERT (internal: EMS_POLICE_TX / EMS_AMB_TX)
  -> ETH_SW
  -> EMS_ALERT (internal: EMS_ALERT_RX)
```

## 1.1 아키텍처 대안 평가 요약 (SWE.3 BP4)

| 대안 | 구성 | 장점 | 한계 | 채택 여부 |
|---|---|---|---|---|
| Option 1 | ETH_SW + Domain GW + Domain CAN + 중앙 경고코어 | 도메인 확장성, Flow/Comm/Var 추적성 명확, SIL 검증 용이 | GW 구현 포인트 증가 | 채택 |
| Option 2 | 도메인 CAN 직접 연계 중심 (ETH 최소화) | 초기 구현 단순 | 긴급/구간 통합 중재 경로 가시성 저하, 향후 확장 제약 | 미채택 |
| Option 3 | 중앙집중 단일 CAN 백본 | 구성 단순 | 도메인 분리 약화, 병목/확장성/유지보수 리스크 | 미채택 |

## 1.2 고도화 아키텍처 적합성 점검

| 점검 항목 | Option 1(현재 채택) | Option 1A(고도화 대안: 이중 ETH 백본 + 이중화 GW) | 판단 |
|---|---|---|---|
| 요구사항(Req_001~043) 충족성 | 충족 | 충족 가능 | 현 단계는 Option 1 충분 |
| SIL 구현 난이도(CANoe) | 중간 | 높음 (이중화 제어/복구 시나리오 추가) | Option 1 유리 |
| 추적성 유지(Req->...->ST) | 높음 | 높음 | 동등 |
| 장애 허용성(단일 장애) | 중간 | 높음 | 장기적으로 1A 우수 |
| 현재 프로젝트 범위 적합성 | 높음 | 과설계 위험 | Option 1 유지 |

- 결론: 현재 스코프(멘토링/포트폴리오/SIL 검증)에서는 **Option 1이 최적안**이며, 장애 허용성 강화가 필요해지는 시점(예: HIL/실차 이전)에만 Option 1A를 도입한다.

---

## 2. 구현 모듈 명세 (공식 표준 양식)

| 구현 모듈 | 기능 상세 | 비고 |
|---|---|---|
|  |  | Core |
| ADAS_WARN_CTRL | 차량 상태 입력 기반 경고 조건 판정 및 경고 시작/종료 제어 | Func_001~004,006,010~012,130,131,136,148 |
| NAV_CTX_MGR | 구간/방향/거리 입력을 컨텍스트로 변환 | Func_007 |
| EMS_ALERT | 긴급알림 송신(Tx) 및 수신/해제/타임아웃(Rx) 통합 관리 | Func_017,018,023,024,144 |
| WARN_ARB_MGR | 긴급/구간 충돌 중재 및 최종 경고 컨텍스트 생성 | Func_022,025,027~032,140~142,149,150,152 |
|  |  | Gateway/Network |
| CHS_GW | Chassis CAN 입력 정규화 및 ETH 송신 | Flow_001,002 |
| INFOTAINMENT_GW | Infotainment CAN 입력(구간/방향/거리/제한속도) 정규화 및 ETH 송신 | Flow_003 |
| ETH_SW | ETH 경로 헬스 모니터링(메시지 age 기반 path health 판정) | Flow_001~008 |
| BODY_GW | 중재 결과 ETH 수신 후 Ambient CAN 송신 | Flow_007 |
| IVI_GW | 중재 결과 ETH 수신 후 Cluster CAN 송신 | Flow_008 |
|  |  | Output |
| AMBIENT_CTRL | 경고 레벨/타입 기반 앰비언트 패턴/색상 출력 | Func_008,009,013~016,033~039 |
| CLU_HMI_CTRL | 경고 문구/방향/유형 표시 및 중복 억제 | Func_005,019~021,026,040,143,145~147,153~155 |
|  |  | SIL Verification |
| VAL_SCENARIO_CTRL | 시나리오 실행, CAN+ETH 동시 검증, 결과 기록 | Func_041~043 |

- 상단 공식표는 감사 일관성을 위해 `EMS_ALERT` 논리 단말 기준으로 표기한다.
- 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`) 분해는 본문 상세 추적표(3장, 4장)에서 관리한다.
- 프레임 포워딩은 Ethernet 스위칭 인프라(실차 스위치 또는 SIL 네트워크 스택)가 담당하고, `ETH_SW` CAPL은 경로 상태 모니터링/진단 로직을 담당한다.

---

## 3. 코드 아티팩트 계획

| Module ID | Node | 구현 파일(계획) | 역할 |
|---|---|---|---|
| MOD_01 | ADAS_WARN_CTRL | `canoe/src/capl/logic/ADAS_WARN_CTRL.can` | 조건 판정/디바운스/트리거 |
| MOD_02 | NAV_CTX_MGR | `canoe/src/capl/logic/NAV_CTX_MGR.can` | 구간 컨텍스트 계산 |
| MOD_03 | EMS_POLICE_TX | `canoe/src/capl/ems/EMS_POLICE_TX.can` | 경찰 긴급 송신 |
| MOD_04 | EMS_AMB_TX | `canoe/src/capl/ems/EMS_AMB_TX.can` | 구급 긴급 송신 |
| MOD_05 | EMS_ALERT_RX | `canoe/src/capl/logic/EMS_ALERT_RX.can` | 긴급 수신/해제/타임아웃 |
| MOD_06 | WARN_ARB_MGR | `canoe/src/capl/logic/WARN_ARB_MGR.can` | 경보 우선순위 판정 |
| MOD_07 | CHS_GW | `canoe/src/capl/input/CHS_GW.can` | CAN->ETH 변환 |
| MOD_08 | INFOTAINMENT_GW | `canoe/src/capl/input/INFOTAINMENT_GW.can` | CAN->ETH 변환 |
| MOD_09 | BODY_GW | `canoe/src/capl/output/BODY_GW.can` | ETH->CAN 변환(Ambient) |
| MOD_10 | IVI_GW | `canoe/src/capl/output/IVI_GW.can` | ETH->CAN 변환(Cluster) |
| MOD_11 | AMBIENT_CTRL | `canoe/src/capl/output/AMBIENT_CTRL.can` | Ambient 출력 제어 |
| MOD_12 | CLU_HMI_CTRL | `canoe/src/capl/output/CLU_HMI_CTRL.can` | Cluster 경고 출력 |
| MOD_13 | VAL_SCENARIO_CTRL | `canoe/src/capl/input/` (Validation scenario controller module, canonical=`VAL_SCENARIO_CTRL`) | 테스트 실행/판정 |
| MOD_14 | ETH_SW | `canoe/src/capl/network/ETH_SW.can` | ETH 경로 상태 모니터(Validation/Fail-safe 지원) |
| MOD_15 | DOMAIN_BOUNDARY_MGR | `canoe/src/capl/ecu/DOMAIN_BOUNDARY_MGR.can` | 도메인 경로 헬스/Fail-safe 게이트 |

---

## 4. 기능-구현 추적 상세 표

| Func ID | Req ID | 구현 모듈 | 입력 (Flow/Comm/Var) | 출력 (Flow/Comm/Var) | Code Ref | 검증 링크 |
|---|---|---|---|---|---|---|
| Func_001 | Req_001 | ADAS_WARN_CTRL | Flow_001 / Comm_001 / vehicleSpeedNorm, driveStateNorm | Flow_006 / warningState | `MOD_01.F001` | UT_ADAS_001 |
| Func_002 | Req_002 | ADAS_WARN_CTRL | Flow_001 / Comm_001 / driveStateNorm | Flow_006 / warningState | `MOD_01.F002` | UT_ADAS_001 |
| Func_003 | Req_003 | ADAS_WARN_CTRL | Flow_001 / Comm_001 / vehicleSpeedNorm, baseZoneContext | Flow_006 / warningState | `MOD_01.F003` | UT_ADAS_001 |
| Func_004 | Req_004 | ADAS_WARN_CTRL | Flow_001 / Comm_001 / warningState | Flow_006 / warningState | `MOD_01.F004` | UT_ADAS_001 |
| Func_005 | Req_005 | CLU_HMI_CTRL | Flow_008 / Comm_008 / selectedAlertType | Flow_008 / warningTextCode | `MOD_12.F005` | UT_CLU_001 |
| Func_006 | Req_006 | ADAS_WARN_CTRL | Flow_001 / Comm_001 / warningState | Flow_006 / warningState | `MOD_01.F006` | UT_ADAS_001 |
| Func_007 | Req_007 | NAV_CTX_MGR | Flow_003 / Comm_003 / roadZone, navDirection, zoneDistance, speedLimit | Flow_003 / baseZoneContext, speedLimitNorm | `MOD_02.F007` | UT_NAV_001 |
| Func_008 | Req_008 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientMode | `MOD_11.F008` | UT_BCM_001 |
| Func_009 | Req_009 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientMode | `MOD_11.F009` | UT_BCM_001 |
| Func_010 | Req_010 | ADAS_WARN_CTRL | Flow_001,Flow_003 / Comm_001,Comm_003 / vehicleSpeedNorm, speedLimitNorm, baseZoneContext | Flow_006 / warningState | `MOD_01.F010` | UT_ADAS_001 |
| Func_011 | Req_011 | ADAS_WARN_CTRL | Flow_002 / Comm_002 / steeringInputNorm, baseZoneContext | Flow_006 / warningState | `MOD_01.F011` | UT_ADAS_001 |
| Func_012 | Req_012 | ADAS_WARN_CTRL | Flow_002 / Comm_002 / steeringInputNorm | Flow_006 / warningState | `MOD_01.F012` | UT_ADAS_001 |
| Func_013 | Req_013 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertType, navDirection | Flow_007 / ambientMode | `MOD_11.F013` | UT_BCM_001 |
| Func_014 | Req_014 | AMBIENT_CTRL | Flow_007 / Comm_007 / navDirection | Flow_007 / ambientPattern | `MOD_11.F014` | UT_BCM_001 |
| Func_015 | Req_015 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientPattern | `MOD_11.F015` | UT_BCM_001 |
| Func_016 | Req_016 | AMBIENT_CTRL | Flow_007 / Comm_007 / timeoutClear | Flow_007 / ambientMode | `MOD_11.F016` | UT_BCM_001 |
| Func_017 | Req_017 | EMS_POLICE_TX | SIL 입력 / emergencyType, eta, emergencyDirection | Flow_004 / Comm_004 / ETH_EmergencyAlert | `MOD_03.F017` | UT_EMS_POL_001 |
| Func_018 | Req_017 | EMS_AMB_TX | SIL 입력 / emergencyType, eta, emergencyDirection | Flow_005 / Comm_005 / ETH_EmergencyAlert | `MOD_04.F018` | UT_EMS_AMB_001 |
| Func_019 | Req_019 | CLU_HMI_CTRL | Flow_008 / Comm_008 / selectedAlertType | Flow_008 / warningTextCode | `MOD_12.F019` | UT_CLU_001 |
| Func_020 | Req_020 | CLU_HMI_CTRL | Flow_008 / Comm_008 / emergencyDirection | Flow_008 / warningTextCode | `MOD_12.F020` | UT_CLU_001 |
| Func_021 | Req_021 | CLU_HMI_CTRL | Flow_008 / Comm_008 / selectedAlertType | Flow_008 / warningTextCode | `MOD_12.F021` | UT_CLU_001 |
| Func_022 | Req_022 | WARN_ARB_MGR | Flow_006 / Comm_006 / emergencyContext, warningState, baseZoneContext | Flow_006,007,008 / selectedAlertLevel, selectedAlertType | `MOD_06.F022` | UT_ARB_001 |
| Func_023 | Req_023 | EMS_ALERT_RX | Flow_006 / Comm_006 / alertState, emergencyType | Flow_006 / emergencyContext | `MOD_05.F023` | UT_EMS_RX_001 |
| Func_024 | Req_024 | EMS_ALERT_RX | Flow_006 / Comm_006 / lastEmergencyRxMs | Flow_006 / timeoutClear | `MOD_05.F024` | UT_EMS_RX_001 |
| Func_025 | Req_025 | WARN_ARB_MGR | Flow_006 / Comm_006 / emergencyContext | Flow_006 / selectedAlertType | `MOD_06.F025` | UT_ARB_001 |
| Func_026 | Req_026 | CLU_HMI_CTRL | Flow_008 / Comm_008 / selectedAlertType, duplicatePopupGuard | Flow_008 / warningTextCode | `MOD_12.F026` | UT_CLU_001 |
| Func_027 | Req_027 | WARN_ARB_MGR | Flow_006 / Comm_006 / emergencyContext, warningState | Flow_006 / selectedAlertLevel | `MOD_06.F027` | UT_ARB_001 |
| Func_028 | Req_028 | WARN_ARB_MGR | Flow_006 / Comm_006 / emergencyContext | Flow_006 / selectedAlertLevel | `MOD_06.F028` | UT_ARB_001 |
| Func_029 | Req_029 | WARN_ARB_MGR | Flow_006 / Comm_006 / emergencyType | Flow_006 / selectedAlertType | `MOD_06.F029` | UT_ARB_001 |
| Func_030 | Req_030 | WARN_ARB_MGR | Flow_006 / Comm_006 / eta | Flow_006 / selectedAlertType | `MOD_06.F030` | UT_ARB_001 |
| Func_031 | Req_031 | WARN_ARB_MGR | Flow_006 / Comm_006 / sourceId | Flow_006 / selectedAlertType | `MOD_06.F031` | UT_ARB_001 |
| Func_032 | Req_032 | WARN_ARB_MGR | Flow_006 / Comm_006 / arbitrationSnapshotId | Flow_006 / selectedAlertLevel, selectedAlertType | `MOD_06.F032` | UT_ARB_001 |
| Func_033 | Req_033 | AMBIENT_CTRL | Flow_007 / Comm_007 / timeoutClear, baseZoneContext | Flow_007 / ambientMode | `MOD_11.F033` | UT_BCM_001 |
| Func_034 | Req_034 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientPattern | `MOD_11.F034` | UT_BCM_001 |
| Func_035 | Req_035 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertType | Flow_007 / ambientColor | `MOD_11.F035` | UT_BCM_001 |
| Func_036 | Req_035 | AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientPattern | `MOD_11.F036` | UT_BCM_001 |
| Func_037 | Req_037 | AMBIENT_CTRL | Flow_007 / Comm_007 / baseZoneContext | Flow_007 / ambientColor, ambientPattern | `MOD_11.F037` | UT_BCM_001 |
| Func_038 | Req_037 | AMBIENT_CTRL | Flow_007 / Comm_007 / baseZoneContext | Flow_007 / ambientColor, ambientPattern | `MOD_11.F038` | UT_BCM_001 |
| Func_039 | Req_037 | AMBIENT_CTRL | Flow_007 / Comm_007 / navDirection, baseZoneContext | Flow_007 / ambientColor, ambientPattern | `MOD_11.F039` | UT_BCM_001 |
| Func_040 | Req_040 | CLU_HMI_CTRL | Flow_008 / Comm_008 / warningTextCode | Flow_008 / warningTextCode | `MOD_12.F040` | UT_CLU_001 |
| Func_041 | Req_041 | VAL_SCENARIO_CTRL | Flow_009 / Comm_009 / testScenario | Flow_009 / scenarioResult | `MOD_13.F041` | ST_SIL_001 |
| Func_042 | Req_042 | VAL_SCENARIO_CTRL | Flow_009 / Comm_009 / testScenario | Flow_009 / scenarioResult | `MOD_13.F042` | ST_SIL_002 |
| Func_043 | Req_043 | VAL_SCENARIO_CTRL | Flow_009 / Comm_009 / scenarioResult | Flow_009 / scenarioResult | `MOD_13.F043` | ST_RESULT_001 |
| Func_101 | Req_101 | ENG_CTRL | Flow_101 / Comm_101 / IgnitionState, GearInput | Flow_101 / EngineState, EngineRpm | `ENG_CTRL.F101` | UT_BASE_PT_001 / IT_BASE_PT_001 |
| Func_102 | Req_102 | TCM | Flow_101 / Comm_101 / IgnitionState, GearInput | Flow_101 / GearState | `TCM.F102` | UT_BASE_PT_001 / IT_BASE_PT_001 |
| Func_103 | Req_103 | ACCEL_CTRL | Flow_102 / Comm_102 / AccelPedal | Flow_102 / AccelRequest, TorqueRequest | `ACCEL_CTRL.F103` | UT_BASE_CH_001 / IT_BASE_CH_001 |
| Func_104 | Req_104 | BRK_CTRL | Flow_102 / Comm_102 / BrakePedal | Flow_102 / BrakePressure, BrakeMode, AbsActive, EspActive | `BRK_CTRL.F104` | UT_BASE_CH_001 / IT_BASE_CH_001 |
| Func_105 | Req_105 | STEER_CTRL | Flow_102 / Comm_102 / steeringInput, SteeringTorque | Flow_102 / SteeringState, SteeringAssistLv | `STEER_CTRL.F105` | UT_BASE_CH_001 / IT_BASE_CH_001 |
| Func_106 | Req_106 | HAZARD_CTRL | Flow_103 / Comm_103 / HazardSwitch | Flow_103 / HazardState, HazardLampReq | `HAZARD_CTRL.F106` | UT_BASE_BODY_001 / IT_BASE_BODY_001 |
| Func_107 | Req_107 | WINDOW_CTRL | Flow_103 / Comm_103 / WindowCommand | Flow_103 / WindowState | `WINDOW_CTRL.F107` | UT_BASE_BODY_001 / IT_BASE_BODY_001 |
| Func_109 | Req_109 | CLU_BASE_CTRL | Flow_104 / Comm_104 / ClusterSpeed, ClusterGear, warningTextCode | Flow_104 / ClusterStatus | `CLU_BASE_CTRL.F109` | UT_BASE_IVI_001 / IT_BASE_IVI_001 |
| Func_110 | Req_110 | DOMAIN_ROUTER | Flow_105 / Comm_105 / RoutingPolicy, ChassisAliveCnt, BodyAliveCnt, InfoAliveCnt | Flow_105 / BodyGatewayRoute | `DOMAIN_ROUTER.F110` | UT_BASE_GW_001 / IT_BASE_GW_001 |
| Func_111 | Req_111 | DOMAIN_BOUNDARY_MGR | Flow_105 / Comm_105 / RoutingPolicy, BoundaryStatus | Flow_105 / BoundaryStatus | `MOD_15.F111` | UT_BASE_GW_001 / IT_BASE_GW_001 |
| Func_112 | Req_112 | VAL_BASELINE_CTRL | Flow_106 / Comm_106 / BaseScenarioId | Flow_106 / BaseScenarioResult | `VAL_BASELINE_CTRL.F112` | UT_BASE_TEST_001 / IT_BASE_DIAG_001 |
| Func_113 | Req_113 | BODY_GW | Flow_202 / Comm_202 / CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode | Flow_202 / CabinTemp | `MOD_09.F113` | UT_BASE_EXT_BODY_001 / IT_BASE_EXT_BODY_001 |
| Func_114 | Req_113 | DRV_STATE_MGR | Flow_202 / Comm_202 / DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel | Flow_202 / DriverStateInfo | `DRV_STATE_MGR.F114` | UT_BASE_EXT_BODY_001 / IT_BASE_EXT_BODY_001 |
| Func_115 | Req_113 | WINDOW_CTRL | Flow_202 / Comm_202 / MirrorFoldState, MirrorHeatState, MirrorAdjAxis | Flow_202 / WindowState | `WINDOW_CTRL.F115` | UT_BASE_EXT_BODY_001 / IT_BASE_EXT_BODY_001 |
| Func_116 | Req_116 | WINDOW_CTRL | Flow_202 / Comm_202 / DoorUnlockCmd, DoorLockState, DoorOpenWarn | Flow_202 / DoorStateMask | `WINDOW_CTRL.F116` | UT_BASE_EXT_BODY_001 / IT_BASE_EXT_BODY_001 |
| Func_117 | Req_116 | AMBIENT_CTRL | Flow_202 / Comm_202 / FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq | Flow_202 / WiperInterval | `MOD_11.F117` | UT_BASE_EXT_BODY_001 / IT_BASE_EXT_BODY_001 |
| Func_118 | Req_118 | DRV_STATE_MGR | Flow_202 / Comm_202 / ImmoState, AlarmArmed, AlarmTrigger, AlarmZone | Flow_202 / DriverStateInfo | `DRV_STATE_MGR.F118` | UT_BASE_EXT_BODY_001 / IT_BASE_EXT_BODY_001 |
| Func_119 | Req_119 | CLU_HMI_CTRL | Flow_203 / Comm_203 / AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId | Flow_203 / warningTextCode | `MOD_12.F119` | UT_BASE_EXT_IVI_001 / IT_BASE_EXT_IVI_001 |
| Func_120 | Req_120 | ADAS_WARN_CTRL | Flow_120 / Comm_120 / emergencyDirection, eta, vehicleSpeedNorm | Flow_120 / proximityRiskLevel | `MOD_01.F120` | UT_V2_RISK_001 / IT_V2_RISK_001 |
| Func_121 | Req_121 | WARN_ARB_MGR | Flow_120 / Flow_121 / proximityRiskLevel, failSafeMode, driveStateNorm | Flow_121 / decelAssistReq | `MOD_06.F121` | UT_V2_RISK_001 / UT_V2_RELEASE_001 / IT_V2_RISK_001 |
| Func_125,Func_126 | Req_125,Req_126 | WARN_ARB_MGR | Flow_122 / Comm_122 / decelAssistReq, selectedAlertType/Level | Flow_122 / selectedAlertType/Level | `MOD_06.F122` | UT_V2_RISK_001 / IT_V2_RISK_001 |
| Func_123 | Req_123 | WARN_ARB_MGR | Flow_123 / Comm_123 / steeringInputNorm, brakePedalNorm | Flow_123 / decelAssistReq | `MOD_06.F123` | UT_V2_RELEASE_001 / IT_V2_RISK_001 |
| Func_127,Func_128,Func_129 | Req_127,Req_128,Req_129 | DOMAIN_BOUNDARY_MGR | Flow_124 / Comm_124 / domainPathStatus, e2eHealthState | Flow_124 / decelAssistReq, failSafeMode | `MOD_15.F124` | UT_V2_FAILSAFE_001 / IT_V2_FAILSAFE_001 |
| Func_130 | Req_130 | ADAS_WARN_CTRL | Flow_130 / Comm_130 / objectTrackValid, objectRange, objectRelSpeed, objectConfidence | Flow_130 / objectTrackValid, objectRange, objectRelSpeed | `MOD_01.F130` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_131 | Req_131 | ADAS_WARN_CTRL | Flow_130 / Comm_130 / objectTrackValid, objectRange, objectRelSpeed | Flow_130 / objectRiskClass, objectTtcMin | `MOD_01.F131` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_132 | Req_132 | ADAS_WARN_CTRL | Flow_131 / Comm_131 / objectTtcMin, objectRiskClass | Flow_131 / selectedAlertLevel, objectRiskClass | `MOD_01.F132` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_133 | Req_133 | ADAS_WARN_CTRL | Flow_131 / Comm_131 / objectRelSpeed, objectRange, objectRiskClass | Flow_131 / selectedAlertLevel, objectRiskClass | `MOD_01.F133` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_134 | Req_134 | WARN_ARB_MGR | Flow_132 / Comm_132 / intersectionConflictFlag, objectRiskClass | Flow_132 / selectedAlertType, selectedAlertLevel | `MOD_06.F134` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_135 | Req_135 | WARN_ARB_MGR | Flow_132 / Comm_132 / mergeCutInFlag, objectRiskClass | Flow_132 / selectedAlertType, selectedAlertLevel | `MOD_06.F135` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_136 | Req_136 | ADAS_WARN_CTRL | Flow_131 / Comm_131 / objectTrackValid, objectAlertHoldMs, objectRiskClass | Flow_131 / selectedAlertLevel, objectRiskClass | `MOD_01.F136` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_137 | Req_137 | DOMAIN_BOUNDARY_MGR | Flow_133 / Comm_133 / objectConfidence, decelAssistReq | Flow_133 / decelAssistReq, selectedAlertLevel, failSafeMode | `MOD_15.F137` | UT_ADAS_OBJ_SAFETY_001 / IT_ADAS_OBJ_001 |
| Func_138 | Req_138 | EMS_ALERT | Flow_133 / Comm_133 / objectRiskClass, selectedAlertType, selectedAlertLevel | Flow_133 / objectEventCode | `MOD_05.F138` | UT_ADAS_OBJ_SAFETY_001 / IT_ADAS_OBJ_001 |
| Func_139 | Req_139 | WARN_ARB_MGR | Flow_132 / Comm_132 / objectRiskClass, emergencyContext, baseZoneContext | Flow_132 / selectedAlertType, selectedAlertLevel | `MOD_06.F139` | UT_ADAS_OBJ_RISK_001 / IT_ADAS_OBJ_001 |
| Func_140 | Req_140 | WARN_ARB_MGR | Flow_103 / Comm_103 / TurnLampState, selectedAlertType | Flow_006,Flow_008 / Comm_006,Comm_008 / selectedAlertType, warningTextCode | `MOD_06.F140` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_141 | Req_141 | WARN_ARB_MGR | Flow_105 / Comm_105 / DriveMode, EcoMode, SportMode, selectedAlertLevel | Flow_006 / Comm_006 / selectedAlertLevel | `MOD_06.F141` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_142 | Req_142 | WARN_ARB_MGR | Flow_103 / Comm_103 / DriverSeatBelt, PassengerSeatBelt, SeatBeltWarnLvl, selectedAlertLevel | Flow_006 / Comm_006 / selectedAlertLevel, selectedAlertType | `MOD_06.F142` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_143 | Req_143 | CLU_HMI_CTRL | Flow_008 / Comm_008 / eta, vehicleSpeedNorm, selectedAlertType | Flow_008 / Comm_008 / warningTextCode | `MOD_12.F143` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_144 | Req_144 | EMS_ALERT | Flow_006 / Comm_006 / selectedAlertType, selectedAlertLevel, warningTextCode | Flow_006 / Comm_006 / arbitrationSnapshotId | `MOD_05.F144` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_145 | Req_145 | CLU_HMI_CTRL | Flow_203 / Comm_203 / arbitrationSnapshotId, ClusterNotifType, ClusterNotifPrio | Flow_203 / Comm_203 / warningTextCode | `MOD_12.F145` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_146 | Req_146 | CLU_HMI_CTRL | Flow_104,Flow_203 / Comm_104,Comm_203 / ThemeMode, PopupType, PopupPriority, PopupActive | Flow_203 / Comm_203 / warningTextCode, ClusterNotifPrio | `MOD_12.F146` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_147 | Req_147 | CLU_HMI_CTRL | Flow_104,Flow_203 / Comm_104,Comm_203 / VolumeLevel, AudioFocusOwner | Flow_203 / Comm_203 / warningTextCode, ClusterNotifPrio | `MOD_12.F147` | UT_BASE_ALERT_EXT_001 / IT_BASE_ALERT_EXT_001 |
| Func_148 | Req_148 | ADAS_WARN_CTRL | Flow_130,Flow_133 / Comm_130,Comm_133 / objectTrackValid, objectConfidence, objectRiskClass | Flow_130,Flow_133 / Comm_130,Comm_133 / objectRiskClass, selectedAlertLevel | `MOD_01.F148` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_149 | Req_149 | WARN_ARB_MGR | Flow_006,Flow_105 / Comm_006,Comm_105 / lastEmergencyRxMs, timeoutClear, warningState, BoundaryStatus | Flow_006 / Comm_006 / warningState, selectedAlertLevel | `MOD_06.F149` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_150 | Req_150 | WARN_ARB_MGR | Flow_006 / Comm_006 / warningState, selectedAlertLevel, duplicatePopupGuard | Flow_006 / Comm_006 / selectedAlertLevel, selectedAlertType | `MOD_06.F150` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_151 | Req_151 | DOMAIN_BOUNDARY_MGR | Flow_105,Flow_124 / Comm_105,Comm_124 / domainPathStatus, e2eHealthState, BoundaryStatus | Flow_124 / Comm_124 / domainPathStatus, failSafeMode | `MOD_15.F151` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_152 | Req_152 | WARN_ARB_MGR | Flow_006,Flow_124 / Comm_006,Comm_124 / failSafeMode, selectedAlertType, selectedAlertLevel | Flow_007,Flow_008 / Comm_007,Comm_008 / ambientMode, warningTextCode | `MOD_06.F152` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_153 | Req_153 | CLU_HMI_CTRL | Flow_203 / Comm_203 / AudioFocusOwner, AudioDuckLevel, TtsState | Flow_008,Flow_203 / Comm_008,Comm_203 / warningTextCode, ClusterNotifPrio | `MOD_12.F153` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_154 | Req_154 | CLU_HMI_CTRL | Flow_104,Flow_203 / Comm_104,Comm_203 / PopupType, PopupPriority, PopupActive, duplicatePopupGuard | Flow_008,Flow_203 / Comm_008,Comm_203 / warningTextCode, ClusterNotifPrio | `MOD_12.F154` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |
| Func_155 | Req_155 | CLU_HMI_CTRL | Flow_008,Flow_203 / Comm_008,Comm_203 / ClusterSyncState, ClusterSyncSeq, selectedAlertType, selectedAlertLevel | Flow_008,Flow_203 / Comm_008,Comm_203 / warningTextCode, ClusterNotifPrio | `MOD_12.F155` | UT_BASE_ROBUST_EXT_001 / IT_BASE_ROBUST_EXT_001 |

---

## 4.1 Var ID 연결 보강표 (0304 기준)

| Var ID | Var Name | 주요 사용 모듈(04) | 관련 Flow/Comm |
|---|---|---|---|
| Var_001 | vehicleSpeed | CHS_GW | Flow_001 / Comm_001 |
| Var_002 | driveState | CHS_GW | Flow_001 / Comm_001 |
| Var_003 | steeringInput | CHS_GW | Flow_002 / Comm_002 |
| Var_004 | roadZone | INFOTAINMENT_GW, NAV_CTX_MGR | Flow_003 / Comm_003 |
| Var_005 | navDirection | INFOTAINMENT_GW, NAV_CTX_MGR, CLU_HMI_CTRL | Flow_003,008 / Comm_003,008 |
| Var_006 | zoneDistance | INFOTAINMENT_GW, NAV_CTX_MGR | Flow_003 / Comm_003 |
| Var_030 | speedLimit | INFOTAINMENT_GW, NAV_CTX_MGR, ADAS_WARN_CTRL | Flow_003 / Comm_003 |
| Var_007 | emergencyType | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, WARN_ARB_MGR | Flow_004~006 / Comm_004~006 |
| Var_008 | emergencyDirection | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, CLU_HMI_CTRL | Flow_004~006,008 / Comm_004~006,008 |
| Var_009 | eta | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, WARN_ARB_MGR | Flow_004~006 / Comm_004~006 |
| Var_010 | sourceId | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, WARN_ARB_MGR | Flow_004~006 / Comm_004~006 |
| Var_011 | alertState | EMS_ALERT_RX | Flow_004~006 / Comm_004~006 |
| Var_012 | vehicleSpeedNorm | ADAS_WARN_CTRL | Flow_001 / Comm_001 |
| Var_013 | driveStateNorm | ADAS_WARN_CTRL | Flow_001 / Comm_001 |
| Var_014 | steeringInputNorm | ADAS_WARN_CTRL | Flow_002 / Comm_002 |
| Var_031 | speedLimitNorm | NAV_CTX_MGR, ADAS_WARN_CTRL | Flow_003 / Comm_003 |
| Var_015 | baseZoneContext | NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR, AMBIENT_CTRL | Flow_003,006,007 / Comm_003,006,007 |
| Var_016 | warningState | ADAS_WARN_CTRL, WARN_ARB_MGR | Flow_006 / Comm_006 |
| Var_017 | emergencyContext | EMS_ALERT_RX, WARN_ARB_MGR | Flow_006 / Comm_006 |
| Var_018 | selectedAlertLevel | WARN_ARB_MGR, AMBIENT_CTRL | Flow_006,007 / Comm_006,007 |
| Var_019 | selectedAlertType | WARN_ARB_MGR, AMBIENT_CTRL, CLU_HMI_CTRL | Flow_006~008 / Comm_006~008 |
| Var_020 | timeoutClear | EMS_ALERT_RX, WARN_ARB_MGR, AMBIENT_CTRL | Flow_006,007 / Comm_006,007 |
| Var_021 | ambientMode | WARN_ARB_MGR, BODY_GW, AMBIENT_CTRL | Flow_007 / Comm_007 |
| Var_022 | ambientColor | BODY_GW, AMBIENT_CTRL | Flow_007 / Comm_007 |
| Var_023 | ambientPattern | BODY_GW, AMBIENT_CTRL | Flow_007 / Comm_007 |
| Var_024 | warningTextCode | WARN_ARB_MGR, IVI_GW, CLU_HMI_CTRL | Flow_008 / Comm_008 |
| Var_025 | testScenario | VAL_SCENARIO_CTRL | Flow_009 / Comm_009 |
| Var_026 | scenarioResult | VAL_SCENARIO_CTRL | Flow_009 / Comm_009 |
| Var_027 | lastEmergencyRxMs | EMS_ALERT_RX, WARN_ARB_MGR | Flow_006 / Comm_006 |
| Var_028 | duplicatePopupGuard | WARN_ARB_MGR, CLU_HMI_CTRL | Flow_008 / Comm_008 |
| Var_029 | arbitrationSnapshotId | WARN_ARB_MGR | Flow_006 / Comm_006 |
| Var_133 | TurnLampState | BODY_GW, WARN_ARB_MGR | Flow_103 / Comm_103 |
| Var_138 | DriverSeatBelt | BODY_GW, WARN_ARB_MGR | Flow_103 / Comm_103 |
| Var_139 | PassengerSeatBelt | BODY_GW, WARN_ARB_MGR | Flow_103 / Comm_103 |
| Var_140 | RearSeatBelt | BODY_GW | Flow_103 / Comm_103 |
| Var_141 | SeatBeltWarnLvl | BODY_GW, WARN_ARB_MGR | Flow_103 / Comm_103 |
| Var_155 | VolumeLevel | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_104 / Comm_104 |
| Var_164 | ThemeMode | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_104 / Comm_104 |
| Var_166 | PopupType | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_104 / Comm_104 |
| Var_167 | PopupPriority | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_104 / Comm_104 |
| Var_168 | PopupActive | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_104 / Comm_104 |
| Var_180 | BoundaryStatus | DOMAIN_ROUTER, DOMAIN_BOUNDARY_MGR | Flow_105,Flow_124 / Comm_105,Comm_124 |
| Var_191 | DriveMode | DOMAIN_ROUTER, WARN_ARB_MGR | Flow_105 / Comm_105 |
| Var_192 | EcoMode | DOMAIN_ROUTER, WARN_ARB_MGR | Flow_105 / Comm_105 |
| Var_193 | SportMode | DOMAIN_ROUTER, WARN_ARB_MGR | Flow_105 / Comm_105 |
| Var_268 | AudioFocusOwner | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_269 | AudioDuckLevel | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_281 | ClusterNotifType | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_282 | ClusterNotifPrio | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_289 | TtsState | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_296 | ClusterSyncState | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_297 | ClusterSyncSeq | INFOTAINMENT_GW, CLU_HMI_CTRL | Flow_203 / Comm_203 |
| Var_320 | proximityRiskLevel | ADAS_WARN_CTRL | Flow_120 / Comm_120 |
| Var_321 | decelAssistReq | WARN_ARB_MGR | Flow_121 / Comm_121 |
| Var_322 | selectedAlertLevel | WARN_ARB_MGR | Flow_122 / Comm_122 |
| Var_323 | selectedAlertType | WARN_ARB_MGR | Flow_122 / Comm_122 |
| Var_324 | steeringInputNorm | CHS_GW | Flow_123 / Comm_123 |
| Var_325 | brakePedalNorm | CHS_GW | Flow_123 / Comm_123 |
| Var_326 | domainPathStatus | DOMAIN_BOUNDARY_MGR | Flow_124 / Comm_124 |
| Var_327 | e2eHealthState | DOMAIN_BOUNDARY_MGR | Flow_124 / Comm_124 |
| Var_328 | failSafeMode | DOMAIN_BOUNDARY_MGR | Flow_124 / Comm_124 |
| Var_329 | decelAssistReq | DOMAIN_BOUNDARY_MGR | Flow_124 / Comm_124 |
| Var_330 | objectTrackValid | ADAS_WARN_CTRL | Flow_130 / Comm_130 |
| Var_331 | objectRange | ADAS_WARN_CTRL | Flow_130 / Comm_130 |
| Var_332 | objectRelSpeed | ADAS_WARN_CTRL | Flow_130 / Comm_130 |
| Var_333 | objectConfidence | ADAS_WARN_CTRL, DOMAIN_BOUNDARY_MGR | Flow_130,Flow_133 / Comm_130,Comm_133 |
| Var_334 | objectRiskClass | ADAS_WARN_CTRL, WARN_ARB_MGR, EMS_ALERT | Flow_131,Flow_132,Flow_133 / Comm_131,Comm_132,Comm_133 |
| Var_335 | objectTtcMin | ADAS_WARN_CTRL | Flow_131 / Comm_131 |
| Var_336 | intersectionConflictFlag | WARN_ARB_MGR | Flow_132 / Comm_132 |
| Var_337 | mergeCutInFlag | WARN_ARB_MGR | Flow_132 / Comm_132 |
| Var_338 | objectAlertHoldMs | ADAS_WARN_CTRL | Flow_131 / Comm_131 |
| Var_339 | objectEventCode | EMS_ALERT | Flow_133 / Comm_133 |

---

## 4.2 Verification-Harness 변수 (SIL 전용)

| 항목 | Namespace/Name | 용도 | 구현 모듈 | 제품 Req 체인 연결 |
|---|---|---|---|---|
| EMS 수동 디스패치 입력 | `V2X/policeDispatch`, `V2X/ambulanceDispatch` | Panel 버튼 기반 긴급 이벤트 주입(송신 트리거) | `EMS_POLICE_TX.can`, `EMS_AMB_TX.can` | 없음(검증 자극 전용) |
| 렌더 출력 버스 | `UiRender/*` (`renderMode`, `renderColor`, `renderPattern`, `renderTextCode`, `renderDirection`, `roadZoneColorCode`, `roadFlowDirection`, `vehicleObjectPos`, `emsBlinkPhase`, `ambientPulsePhase`, `icFlowPhase`, `activeAlertType`) | 패널 시각화 전용 파생 값 | `IVI_GW.can` | 없음(렌더 전용) |

- 본 표 항목은 `00c`의 `Verification-Harness` 분류를 따르며, 감사 시 제품 기능 요구 미연결 항목으로 해석하지 않는다.

---

## 5. 실행/타이밍 설계

| Task ID | 모듈 | 주기/트리거 | 입력 | 출력 | 타임아웃/조건 |
|---|---|---|---|---|---|
| TASK_001 | CHS_GW | 100ms 주기 | frmVehicleStateCanMsg, frmSteeringCanMsg | ethVehicleStateMsg, ethSteeringMsg | 연속 2주기 누락 시 Fault |
| TASK_002 | INFOTAINMENT_GW | 100ms 주기 | frmNavContextCanMsg | ethNavContextMsg | 연속 2주기 누락 시 일반구간 복귀 |
| TASK_003 | ADAS_WARN_CTRL | Event + 100ms 내부 평가 | vehicleSpeedNorm, driveStateNorm, steeringInputNorm | warningState, proximityRiskLevel | 비주행 상태 시 경고 억제 |
| TASK_004 | NAV_CTX_MGR | Event(입력 변경) | roadZone, navDirection, zoneDistance, speedLimit | baseZoneContext, speedLimitNorm | 입력 invalid 시 기본 컨텍스트/기본제한속도(30) |
| TASK_005 | EMS_POLICE_TX | 100ms 주기 | Police Active/ETA/Direction | ETH_EmergencyAlert | Active=0이면 Clear 송신 |
| TASK_006 | EMS_AMB_TX | 100ms 주기 | Ambulance Active/ETA/Direction | ETH_EmergencyAlert | Active=0이면 Clear 송신 |
| TASK_007 | EMS_ALERT_RX | Event 수신 + 10ms watchdog | ETH_EmergencyAlert | emergencyContext, timeoutClear | 1000ms 무갱신 시 timeoutClear=1 |
| TASK_008 | WARN_ARB_MGR | Event + 50ms 출력 | emergencyContext, warningState, baseZoneContext | selectedAlertLevel, selectedAlertType | Emergency 우선, 동률 규칙 적용 |
| TASK_009 | BODY_GW + AMBIENT_CTRL | 50ms 주기 | ethSelectedAlertMsg | frmAmbientControlMsg | CAN ACK 실패 시 안전 기본값 |
| TASK_010 | IVI_GW + CLU_HMI_CTRL | 50ms 주기 | ethSelectedAlertMsg | frmClusterWarningMsg | CAN ACK 실패 시 최소 안내 코드 |

---

## 6. 유닛 인터페이스 명세 (SWE.3 BP2)

| Interface ID | 제공 모듈 | 소비 모듈 | 데이터 | 연계 Flow/Comm | 제약 |
|---|---|---|---|---|---|
| IF_001 | CHS_GW | ADAS_WARN_CTRL | vehicleSpeedNorm, driveStateNorm | Flow_001 / Comm_001 | 100ms 주기, 값 invalid 시 기본값 처리 |
| IF_002 | CHS_GW | ADAS_WARN_CTRL | steeringInputNorm | Flow_002 / Comm_002 | 100ms 주기 |
| IF_003 | INFOTAINMENT_GW | NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | roadZone, navDirection, zoneDistance, speedLimit | Flow_003 / Comm_003 | 100ms 주기 |
| IF_004 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | EmergencyType, EmergencyDirection, ETA, SourceID, AlertState | Flow_004~006 / Comm_004~006 | 100ms 송신, 1000ms 타임아웃 감시 |
| IF_005 | WARN_ARB_MGR | BODY_GW, IVI_GW | selectedAlertLevel, selectedAlertType, timeoutClear | Flow_006~008 / Comm_006~008 | 50ms 출력 |
| IF_006 | BODY_GW | AMBIENT_CTRL | ambientMode, ambientColor, ambientPattern | Flow_007 / Comm_007 | CAN ACK 실패 시 Fail-safe 적용 |
| IF_007 | IVI_GW | CLU_HMI_CTRL | warningTextCode | Flow_008 / Comm_008 | CAN ACK 실패 시 최소 안내 코드 |
| IF_008 | VAL_SCENARIO_CTRL | VAL_SCENARIO_CTRL(Log/Panel) | testScenario, scenarioResult | Flow_009 / Comm_009 | Event 기반 기록 |

---

## 7. 동적 행위/상태 전이 (SWE.3 BP3)

| 상태 | 진입 조건 | 출력 동작 | 이탈 조건 | 관련 Func/Req |
|---|---|---|---|---|
| Idle | driveStateNorm=비주행 또는 warningState=0 | 출력 기본값 유지 | 주행 상태 진입 + 경고 조건 성립 | Func_001, Func_002 / Req_001, Req_002 |
| ZoneWarningActive | baseZoneContext 유효 + 경고 조건 성립 | selectedAlert* 생성, Ambient/Cluster 출력 | 경고 조건 해제 또는 Emergency 진입 | Func_003, Func_007, Func_008~016 / Req_003, Req_007~016 |
| EmergencyActive | EmergencyAlert Active 수신 | Emergency 우선 중재, 긴급 패턴 출력 | Clear 수신 또는 타임아웃 | Func_017~024, Func_028~031 / Req_017~024, Req_028~031 |
| ArbitrationActive | Zone + Emergency 동시 존재 | 우선순위 규칙 적용 후 단일 결과 출력 | Emergency 해제 또는 입력 조건 변경 | Func_022, Func_025, Func_027, Func_032 / Req_022, Req_025, Req_027, Req_032 |
| Recovery | timeoutClear=1 또는 Emergency 종료 | 직전 유효 Zone 상태 복귀, 전환 완화 | 복귀 완료 | Func_033, Func_034 / Req_033, Req_034 |
| SIL_Evaluation | testScenario 실행 시작 | 시나리오 판정 수행, 결과 기록 | 판정 완료 | Func_041~043 / Req_041~043 |

---

## 8. 예외/고장 처리 구현 규칙

| 장애 조건 | 감지 위치 | 구현 동작 | 추적 링크 |
|---|---|---|---|
| CHS_GW CAN->ETH 변환 실패 | CHS_GW watchdog | 마지막 정상값 1주기 유지 후 `warningState` 강등 | Req_001,Req_011 / Func_001,Func_011 / Flow_001,002 |
| INFOTAINMENT_GW CAN->ETH 변환 실패 | INFOTAINMENT_GW watchdog | `baseZoneContext` 일반구간 복귀, 유도 출력 해제 | Req_007,Req_016 / Func_007,Func_016 / Flow_003 |
| EmergencyAlert 1000ms 무갱신 | EMS_ALERT_RX timeout monitor | `timeoutClear=1`, `emergencyContext` clear | Req_024 / Func_024 / Flow_006 |
| BODY_GW CAN 송신 실패 | BODY_GW Tx ACK monitor | `ambientMode=0`으로 강등 후 최대 3회 재시도 | Req_033,Req_034 / Func_033,Func_034 / Flow_007 |
| IVI_GW CAN 송신 실패 | IVI_GW Tx ACK monitor | 최소 안내 코드로 1회 재송신 | Req_040 / Func_040 / Flow_008 |

---

## 9. 구현 산출물 검토 체크리스트

| 항목 | 기준 | 상태 |
|---|---|---|
| 스코프 정합 | CANoe SIL, CAN+Ethernet만 사용 | Defined |
| 아키텍처 정합 | 옵션1(ETH_SW+Domain GW+CAN) 고정 | Defined |
| Func 구현 커버리지 | Func_001~043, Func_101~119, Func_120~121, Func_123, Func_125~129, Func_130~155 Code Ref 존재 | Defined |
| Flow/Comm 정합 | 0302/0303과 ID/주기/조건 일치 | Defined |
| Var 정합 | 0304 표준 Name + Internal Name 매핑 반영 | Defined |
| 예외 처리 구현 | 5개 장애 규칙 구현 및 로그화 | Defined |
| 테스트 역추적 | UT/IT/ST에서 Code Ref 역추적 가능 | Defined |

---

## 10. 설계 평가/합의 증적 (SWE.3 BP4, BP7)

| Record ID | 유형 | 목적 | 저장 위치(계획) | 관련 BP |
|---|---|---|---|---|
| RVW_04_001 | Review record | 04 상세설계 검토(인터페이스/동적행위/예외) | `docs/review/04_design_review.md` | SWE.3.BP4 |
| COM_04_001 | Communication record | 합의된 상세설계 배포 및 변경 공지 | `docs/review/04_communication_log.md` | SWE.3.BP7 |
| TRC_04_001 | Traceability record | Req-Func-Flow-Comm-Var-Code-Test 양방향 추적 증적 | `docs/review/04_traceability_record.md` | SWE.3.BP5, BP6 |

---

## 11. 구현 규칙 기준 (SWE.3 BP8)

| 항목 | 규칙 | 근거 문서 |
|---|---|---|
| 모듈/노드 명명 | Node는 `UPPER_SNAKE_CASE`, 내부 상태는 `camelCase` 유지 | `00e_ECU_Naming_Standard.md`, `03_Function_definition.md` |
| 인터페이스 명명 | 상위 공식 변수명은 0304 표준 Name, 코드 내부는 Internal Name 병기 | `0304_System_Variables.md` |
| 주기/타임아웃 | CAN 입력 100ms, 출력 50ms, Emergency timeout 1000ms 고정 | `0302_NWflowDef.md`, `01_Requirements.md` |
| 예외 처리 | invalid 값 수신 시 fail-safe 기본값 적용 후 로그 기록 | `0304_System_Variables.md`, 본 문서 8장 |
| 범위 통제 | OTA/UDS/DoIP 로직/문구는 구현 범위에서 제외 | `00b_Project_Scope.md` |
| 추적성 유지 | 변경 시 `Req->Func->Flow->Comm->Var->Code->UT/IT/ST` 동시 갱신 | `00_VModel_Mapping.md`, `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

---

## 12. ECU 명명/RTE 매핑 운영 규칙 (명시 관리)

| 항목 | 구현 운영 규칙 | 산출물 |
|---|---|---|
| Canonical 사용 | 코드 모듈/노드/문서 식별자는 Canonical(`UPPER_SNAKE_CASE`)을 기본으로 사용 | CAPL 파일명, 노드명, 추적표 |
| 모델 매핑 | AUTOSAR 연계 대상은 `00g` 규칙에 따라 shortName/RTE 생성명을 병기 관리 | `00g` RTE Name Mapping |
| RTE 샘플 검토 | 신규 ECU/인터페이스 추가 시 RTE 생성명 샘플 2건 작성 및 길이 예산 점검 | 변경 검토 로그, 설계 리뷰 기록 |
| 변경 승인 경로 | 명명 정책 변경은 `00e`(ECU) 개정 -> `00g`(RTE) 개정 -> `04` 구현 반영 순으로 승인 | 개정 이력(00e/00g/04) |
| 타 문서 반영 원칙 | `01/03/0302/0303/0304/05/06/07`은 규칙 본문 없이 Canonical 사용만 유지 | 체인 문서 표기 정합 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.22 | 2026-03-06 | 경고 강건성·인지성 확장(Pre-Activation) 반영: `Func_148~Func_155` 구현 추적과 `Var_016/020/021/024/027/028/166/167/168/180/268/269/289/296/297/326/327/328/330/333/334` 보강표를 추가하고 05/06/07 연계 동기화 규칙을 작성 원칙에 반영. |
| 2.21 | 2026-03-06 | 차량 경보 편의 확장(Pre-Activation) 반영: `Func_140~Func_147` 구현 추적, `Var_133/138~141/155/164/166~168/191~193/268/281/282` 보강표 추가, 05/06/07 연계 동기화 규칙을 작성 원칙에 반영. |
| 2.20 | 2026-03-06 | ADAS 객체 인지 확장(Pre-Activation) 반영: `Func_130~Func_139` 구현 추적과 `Var_330~Var_339` 보강표를 추가하고 체인 동기화 규칙을 작성 원칙에 명시. |
| 2.19 | 2026-03-06 | 용어/범위 정리: Verification-Harness에서 Driver 네임스페이스 자극 문구/행을 제거하고 `고속 무조향 기반 경고` 제품 체인과 분리 경계를 명확화. |
| 2.18 | 2026-03-06 | 미사용 체인 정리: `Req_108/Func_108` 구현 추적 행을 제거하고 Body Baseline 경로를 `106/107/111` 기준으로 동기화. |
| 2.17 | 2026-03-05 | ECU/RTE 거버넌스를 `00e(ECU SoT)+00g(RTE SoT)+04(구현 참조)` 체계로 정리하고, 구현 단계 RTE 샘플 점검/승인 경로 규칙(12장)을 추가. |
| 2.16 | 2026-03-05 | Validation 노드 명칭(`VAL_SCENARIO_CTRL`/`VAL_BASELINE_CTRL`)과 DBC 통합 정책(`0x2A5/0x2A6 -> chassis_can.dbc`)을 구현 추적 표/원칙에 반영. |
| 2.15 | 2026-03-04 | 멘토링 체크리스트 반영: Panel 구성 우선순위(`차량 화면 -> 제어 패널 -> 상태 모니터`)와 UI-로직 분리 원칙을 작성 원칙에 명시. |
| 2.14 | 2026-03-04 | 구현 원칙 정합 보강: 통신 SoT에 `eth_backbone_can_stub.dbc`를 추가하고, CANoe.CAN 환경의 CAN-stub 대체 운반 규칙(0x1C0/0x1C1/0x1C2/0x1C3/0x1C4/0x111)과 Ethernet 논리 계약 우선 해석 원칙을 명시. |
| 2.13 | 2026-03-03 | 감사 추적성 보강: `Func_101~119` / `Req_101~119` 기능-구현 상세 행을 추가하고, UT/IT 링크(`UT_BASE_*`, `IT_BASE_*`)를 1:1로 연결. |
| 2.12 | 2026-03-03 | ETH_SW 역할을 구현 기준(경로 상태 모니터링)으로 명확화하고, 코드 아티팩트 경로를 `canoe/src/capl/*` 실제 경로로 정합화. |
| 2.11 | 2026-03-03 | Req_120~124 추적/타이밍 정합 반영: `Func_120~124` 및 `Var_320~329` 추적 항목 추가, `TASK_003`를 100ms 주기로 정합화, `DOMAIN_BOUNDARY_MGR`를 `MOD_15`로 반영. |
| 2.10 | 2026-03-02 | ISO26262/ASPICE 운영 경계 반영: SIL 전용 `Verification-Harness` 변수(`V2X/policeDispatch`, `V2X/ambulanceDispatch`, `Test/*`, `UiRender/*`)의 비제품 체인 분류를 작성 원칙/4.2 표로 명시. |
| 2.9 | 2026-03-01 | 상단 공식 표와 아키텍처 요약의 EMS 표기를 `EMS_ALERT` 논리 단말 기준으로 통일하고, 내부 TX/RX 모듈은 상세 추적표에서만 분리 관리. |
| 1.0 | 2026-02-23 | 초기 생성(구 스코프 기반) |
| 2.0 | 2026-02-26 | 옵션1 아키텍처 기준으로 전면 재작성. 구버전 OTA/UDS/DoIP 구현 항목 제거, Func_001~043 구현 추적 표 및 타이밍/예외 처리 규칙 정립 |
| 2.1 | 2026-02-26 | SWE.3 BP2/BP3 대응 인터페이스/상태전이 표와 SWE.3 BP4/BP7 증적 섹션 추가, Func_006 입력 추적 정합화 |
| 2.2 | 2026-02-26 | 05/06/07 레거시 상태를 반영하여 검증 링크를 Planned ID로 명시, 하위 문서 재작성 전제 정합화 |
| 2.3 | 2026-02-26 | BP4 대안평가 요약, Var ID 연결 보강표, BP8 구현 규칙 기준 섹션 추가로 00~03 대비 04 추적성 강화 |
| 2.4 | 2026-02-26 | SIL 입력 경로(sysvar)와 목표 ETH(UdpSocket) 전환 전략을 작성 원칙에 명시 |
| 2.5 | 2026-02-26 | 05~07 최신 상태 반영(레거시/Planned 문구 제거), 고도화 아키텍처 적합성 점검(Option 1 vs 1A) 추가 |
| 2.6 | 2026-02-28 | Req_010 정합을 위해 `speedLimit/speedLimitNorm`을 Func_007/Func_010, IF_003, TASK_004, Var 연결표에 반영. |
| 2.7 | 2026-02-28 | 통신 원본 분리 원칙(CAN DBC / Ethernet Interface Contract)을 작성 원칙에 반영. |
| 2.8 | 2026-02-28 | CAN SoT를 도메인 분리 DBC(`*_can.dbc`) 세트 기준으로 정합화. |

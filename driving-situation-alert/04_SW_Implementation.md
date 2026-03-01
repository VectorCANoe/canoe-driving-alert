# SW 구현 명세 (Software Implementation Specification)

**Document ID**: PROJ-04-SI
**ISO 26262 Reference**: Part 6, Cl.8 (Software Unit Design and Implementation)
**ASPICE Reference**: SWE.3 (Software Detailed Design and Unit Construction)
**Version**: 2.8
**Date**: 2026-02-28
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
- 네트워크는 옵션1 아키텍처를 고정한다: `ETH_SWITCH + CHASSIS_GW/INFOTAINMENT_GW/BODY_GW/IVI_GW + 도메인 CAN`.
- 통신 원본은 분리 관리한다: CAN=`canoe/databases/chassis_can.dbc` + `canoe/databases/powertrain_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/test_can.dbc`, Ethernet=`canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`.
- 범위 외 항목(OTA/UDS/DoIP)은 구현 대상에서 제외한다.
- ASPICE SWE.3 BP1~BP8 관점에서 `상세 설계/인터페이스/동적행위/대안평가/추적성/합의/구현규칙`을 명시한다.
- SIL 단계에서는 Panel/sysvar 경유 자극을 허용하며, 통신 계약(0302/0303/0304)은 유지한 채 ETH `UdpSocket` 기반 입력으로 점진 전환한다.
- `SIL_TEST_CTRL`/`VEHICLE_BASE_TEST_CTRL`는 Validation Harness이며, `ETH_SWITCH`/도메인 게이트웨이의 통신 변환 역할과 분리한다.

---

## 1. 구현 아키텍처 요약

```text
Input CAN
  -> CHASSIS_GW / INFOTAINMENT_GW (CAN->ETH 정규화)
  -> ETH_SWITCH
  -> 중앙 경고코어 (ADAS_WARN_CTRL, NAV_CONTEXT_MGR, EMS_ALERT, WARN_ARB_MGR)
  -> ETH_SWITCH
  -> BODY_GW / IVI_GW (ETH->CAN 변환)
  -> BCM_AMBIENT_CTRL / CLU_HMI_CTRL

Emergency Source (logical terminal)
  -> EMS_ALERT (internal: EMS_POLICE_TX / EMS_AMB_TX)
  -> ETH_SWITCH
  -> EMS_ALERT (internal: EMS_ALERT_RX)
```

## 1.1 아키텍처 대안 평가 요약 (SWE.3 BP4)

| 대안 | 구성 | 장점 | 한계 | 채택 여부 |
|---|---|---|---|---|
| Option 1 | ETH_SWITCH + Domain GW + Domain CAN + 중앙 경고코어 | 도메인 확장성, Flow/Comm/Var 추적성 명확, SIL 검증 용이 | GW 구현 포인트 증가 | 채택 |
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
| ADAS_WARN_CTRL | 차량 상태 입력 기반 경고 조건 판정 및 경고 시작/종료 제어 | Func_001~004,006,010~012 |
| NAV_CONTEXT_MGR | 구간/방향/거리 입력을 컨텍스트로 변환 | Func_007 |
| EMS_ALERT | 긴급알림 송신(Tx) 및 수신/해제/타임아웃(Rx) 통합 관리 | Func_017,018,023,024 |
| WARN_ARB_MGR | 긴급/구간 충돌 중재 및 최종 경고 컨텍스트 생성 | Func_022,025,027~032 |
|  |  | Gateway/Network |
| CHASSIS_GW | Chassis CAN 입력 정규화 및 ETH 송신 | Flow_001,002 |
| INFOTAINMENT_GW | Infotainment CAN 입력(구간/방향/거리/제한속도) 정규화 및 ETH 송신 | Flow_003 |
| ETH_SWITCH | Ethernet 프레임 분배 및 도메인 전달 | Flow_001~008 |
| BODY_GW | 중재 결과 ETH 수신 후 Ambient CAN 송신 | Flow_007 |
| IVI_GW | 중재 결과 ETH 수신 후 Cluster CAN 송신 | Flow_008 |
|  |  | Output |
| BCM_AMBIENT_CTRL | 경고 레벨/타입 기반 앰비언트 패턴/색상 출력 | Func_008,009,013~016,033~039 |
| CLU_HMI_CTRL | 경고 문구/방향/유형 표시 및 중복 억제 | Func_005,019~021,026,040 |
|  |  | SIL Verification |
| SIL_TEST_CTRL | 시나리오 실행, CAN+ETH 동시 검증, 결과 기록 | Func_041~043 |

- 상단 공식표는 감사 일관성을 위해 `EMS_ALERT` 논리 단말 기준으로 표기한다.
- 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`) 분해는 본문 상세 추적표(3장, 4장)에서 관리한다.

---

## 3. 코드 아티팩트 계획

| Module ID | Node | 구현 파일(계획) | 역할 |
|---|---|---|---|
| MOD_01 | ADAS_WARN_CTRL | `canoe/nodes/ADAS_WARN_CTRL.can` | 조건 판정/디바운스/트리거 |
| MOD_02 | NAV_CONTEXT_MGR | `canoe/nodes/NAV_CONTEXT_MGR.can` | 구간 컨텍스트 계산 |
| MOD_03 | EMS_POLICE_TX | `canoe/nodes/EMS_POLICE_TX.can` | 경찰 긴급 송신 |
| MOD_04 | EMS_AMB_TX | `canoe/nodes/EMS_AMB_TX.can` | 구급 긴급 송신 |
| MOD_05 | EMS_ALERT_RX | `canoe/nodes/EMS_ALERT_RX.can` | 긴급 수신/해제/타임아웃 |
| MOD_06 | WARN_ARB_MGR | `canoe/nodes/WARN_ARB_MGR.can` | 우선순위 중재 |
| MOD_07 | CHASSIS_GW | `canoe/nodes/CHASSIS_GW.can` | CAN->ETH 변환 |
| MOD_08 | INFOTAINMENT_GW | `canoe/nodes/INFOTAINMENT_GW.can` | CAN->ETH 변환 |
| MOD_09 | BODY_GW | `canoe/nodes/BODY_GW.can` | ETH->CAN 변환(Ambient) |
| MOD_10 | IVI_GW | `canoe/nodes/IVI_GW.can` | ETH->CAN 변환(Cluster) |
| MOD_11 | BCM_AMBIENT_CTRL | `canoe/nodes/BCM_AMBIENT_CTRL.can` | Ambient 출력 제어 |
| MOD_12 | CLU_HMI_CTRL | `canoe/nodes/CLU_HMI_CTRL.can` | Cluster 경고 출력 |
| MOD_13 | SIL_TEST_CTRL | `canoe/nodes/SIL_TEST_CTRL.can` | 테스트 실행/판정 |
| MOD_14 | ETH_SWITCH | CANoe Ethernet Backbone 설정 | 이더넷 분배 인프라 |

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
| Func_007 | Req_007 | NAV_CONTEXT_MGR | Flow_003 / Comm_003 / roadZone, navDirection, zoneDistance, speedLimit | Flow_003 / baseZoneContext, speedLimitNorm | `MOD_02.F007` | UT_NAV_001 |
| Func_008 | Req_008 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientMode | `MOD_11.F008` | UT_BCM_001 |
| Func_009 | Req_009 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientMode | `MOD_11.F009` | UT_BCM_001 |
| Func_010 | Req_010 | ADAS_WARN_CTRL | Flow_001,Flow_003 / Comm_001,Comm_003 / vehicleSpeedNorm, speedLimitNorm, baseZoneContext | Flow_006 / warningState | `MOD_01.F010` | UT_ADAS_001 |
| Func_011 | Req_011 | ADAS_WARN_CTRL | Flow_002 / Comm_002 / steeringInputNorm, baseZoneContext | Flow_006 / warningState | `MOD_01.F011` | UT_ADAS_001 |
| Func_012 | Req_012 | ADAS_WARN_CTRL | Flow_002 / Comm_002 / steeringInputNorm | Flow_006 / warningState | `MOD_01.F012` | UT_ADAS_001 |
| Func_013 | Req_013 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertType, navDirection | Flow_007 / ambientMode | `MOD_11.F013` | UT_BCM_001 |
| Func_014 | Req_014 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / navDirection | Flow_007 / ambientPattern | `MOD_11.F014` | UT_BCM_001 |
| Func_015 | Req_015 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientPattern | `MOD_11.F015` | UT_BCM_001 |
| Func_016 | Req_016 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / timeoutClear | Flow_007 / ambientMode | `MOD_11.F016` | UT_BCM_001 |
| Func_017 | Req_017 | EMS_POLICE_TX | SIL 입력 / emergencyType, eta, emergencyDirection | Flow_004 / Comm_004 / ETH_EmergencyAlert | `MOD_03.F017` | UT_EMS_POL_001 |
| Func_018 | Req_018 | EMS_AMB_TX | SIL 입력 / emergencyType, eta, emergencyDirection | Flow_005 / Comm_005 / ETH_EmergencyAlert | `MOD_04.F018` | UT_EMS_AMB_001 |
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
| Func_033 | Req_033 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / timeoutClear, baseZoneContext | Flow_007 / ambientMode | `MOD_11.F033` | UT_BCM_001 |
| Func_034 | Req_034 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientPattern | `MOD_11.F034` | UT_BCM_001 |
| Func_035 | Req_035 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertType | Flow_007 / ambientColor | `MOD_11.F035` | UT_BCM_001 |
| Func_036 | Req_036 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / selectedAlertLevel | Flow_007 / ambientPattern | `MOD_11.F036` | UT_BCM_001 |
| Func_037 | Req_037 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / baseZoneContext | Flow_007 / ambientColor, ambientPattern | `MOD_11.F037` | UT_BCM_001 |
| Func_038 | Req_038 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / baseZoneContext | Flow_007 / ambientColor, ambientPattern | `MOD_11.F038` | UT_BCM_001 |
| Func_039 | Req_039 | BCM_AMBIENT_CTRL | Flow_007 / Comm_007 / navDirection, baseZoneContext | Flow_007 / ambientColor, ambientPattern | `MOD_11.F039` | UT_BCM_001 |
| Func_040 | Req_040 | CLU_HMI_CTRL | Flow_008 / Comm_008 / warningTextCode | Flow_008 / warningTextCode | `MOD_12.F040` | UT_CLU_001 |
| Func_041 | Req_041 | SIL_TEST_CTRL | Flow_009 / Comm_009 / testScenario | Flow_009 / scenarioResult | `MOD_13.F041` | ST_SIL_001 |
| Func_042 | Req_042 | SIL_TEST_CTRL | Flow_009 / Comm_009 / testScenario | Flow_009 / scenarioResult | `MOD_13.F042` | ST_SIL_002 |
| Func_043 | Req_043 | SIL_TEST_CTRL | Flow_009 / Comm_009 / scenarioResult | Flow_009 / scenarioResult | `MOD_13.F043` | ST_RESULT_001 |

---

## 4.1 Var ID 연결 보강표 (0304 기준)

| Var ID | Var Name | 주요 사용 모듈(04) | 관련 Flow/Comm |
|---|---|---|---|
| Var_001 | vehicleSpeed | CHASSIS_GW | Flow_001 / Comm_001 |
| Var_002 | driveState | CHASSIS_GW | Flow_001 / Comm_001 |
| Var_003 | steeringInput | CHASSIS_GW | Flow_002 / Comm_002 |
| Var_004 | roadZone | INFOTAINMENT_GW, NAV_CONTEXT_MGR | Flow_003 / Comm_003 |
| Var_005 | navDirection | INFOTAINMENT_GW, NAV_CONTEXT_MGR, CLU_HMI_CTRL | Flow_003,008 / Comm_003,008 |
| Var_006 | zoneDistance | INFOTAINMENT_GW, NAV_CONTEXT_MGR | Flow_003 / Comm_003 |
| Var_030 | speedLimit | INFOTAINMENT_GW, NAV_CONTEXT_MGR, ADAS_WARN_CTRL | Flow_003 / Comm_003 |
| Var_007 | emergencyType | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, WARN_ARB_MGR | Flow_004~006 / Comm_004~006 |
| Var_008 | emergencyDirection | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, CLU_HMI_CTRL | Flow_004~006,008 / Comm_004~006,008 |
| Var_009 | eta | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, WARN_ARB_MGR | Flow_004~006 / Comm_004~006 |
| Var_010 | sourceId | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX, WARN_ARB_MGR | Flow_004~006 / Comm_004~006 |
| Var_011 | alertState | EMS_ALERT_RX | Flow_004~006 / Comm_004~006 |
| Var_012 | vehicleSpeedNorm | ADAS_WARN_CTRL | Flow_001 / Comm_001 |
| Var_013 | driveStateNorm | ADAS_WARN_CTRL | Flow_001 / Comm_001 |
| Var_014 | steeringInputNorm | ADAS_WARN_CTRL | Flow_002 / Comm_002 |
| Var_031 | speedLimitNorm | NAV_CONTEXT_MGR, ADAS_WARN_CTRL | Flow_003 / Comm_003 |
| Var_015 | baseZoneContext | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR, BCM_AMBIENT_CTRL | Flow_003,006,007 / Comm_003,006,007 |
| Var_016 | warningState | ADAS_WARN_CTRL, WARN_ARB_MGR | Flow_006 / Comm_006 |
| Var_017 | emergencyContext | EMS_ALERT_RX, WARN_ARB_MGR | Flow_006 / Comm_006 |
| Var_018 | selectedAlertLevel | WARN_ARB_MGR, BCM_AMBIENT_CTRL | Flow_006,007 / Comm_006,007 |
| Var_019 | selectedAlertType | WARN_ARB_MGR, BCM_AMBIENT_CTRL, CLU_HMI_CTRL | Flow_006~008 / Comm_006~008 |
| Var_020 | timeoutClear | EMS_ALERT_RX, WARN_ARB_MGR, BCM_AMBIENT_CTRL | Flow_006,007 / Comm_006,007 |
| Var_021 | ambientMode | BODY_GW, BCM_AMBIENT_CTRL | Flow_007 / Comm_007 |
| Var_022 | ambientColor | BODY_GW, BCM_AMBIENT_CTRL | Flow_007 / Comm_007 |
| Var_023 | ambientPattern | BODY_GW, BCM_AMBIENT_CTRL | Flow_007 / Comm_007 |
| Var_024 | warningTextCode | IVI_GW, CLU_HMI_CTRL | Flow_008 / Comm_008 |
| Var_025 | testScenario | SIL_TEST_CTRL | Flow_009 / Comm_009 |
| Var_026 | scenarioResult | SIL_TEST_CTRL | Flow_009 / Comm_009 |
| Var_027 | lastEmergencyRxMs | EMS_ALERT_RX | Flow_006 / Comm_006 |
| Var_028 | duplicatePopupGuard | CLU_HMI_CTRL | Flow_008 / Comm_008 |
| Var_029 | arbitrationSnapshotId | WARN_ARB_MGR | Flow_006 / Comm_006 |

---

## 5. 실행/타이밍 설계

| Task ID | 모듈 | 주기/트리거 | 입력 | 출력 | 타임아웃/조건 |
|---|---|---|---|---|---|
| TASK_001 | CHASSIS_GW | 100ms 주기 | frmVehicleStateCanMsg, frmSteeringCanMsg | ethVehicleStateMsg, ethSteeringMsg | 연속 2주기 누락 시 Fault |
| TASK_002 | INFOTAINMENT_GW | 100ms 주기 | frmNavContextCanMsg | ethNavContextMsg | 연속 2주기 누락 시 일반구간 복귀 |
| TASK_003 | ADAS_WARN_CTRL | Event + 10ms 내부 평가 | vehicleSpeedNorm, driveStateNorm, steeringInputNorm | warningState | 비주행 상태 시 경고 억제 |
| TASK_004 | NAV_CONTEXT_MGR | Event(입력 변경) | roadZone, navDirection, zoneDistance, speedLimit | baseZoneContext, speedLimitNorm | 입력 invalid 시 기본 컨텍스트/기본제한속도(30) |
| TASK_005 | EMS_POLICE_TX | 100ms 주기 | Police Active/ETA/Direction | ETH_EmergencyAlert | Active=0이면 Clear 송신 |
| TASK_006 | EMS_AMB_TX | 100ms 주기 | Ambulance Active/ETA/Direction | ETH_EmergencyAlert | Active=0이면 Clear 송신 |
| TASK_007 | EMS_ALERT_RX | Event 수신 + 10ms watchdog | ETH_EmergencyAlert | emergencyContext, timeoutClear | 1000ms 무갱신 시 timeoutClear=1 |
| TASK_008 | WARN_ARB_MGR | Event + 50ms 출력 | emergencyContext, warningState, baseZoneContext | selectedAlertLevel, selectedAlertType | Emergency 우선, 동률 규칙 적용 |
| TASK_009 | BODY_GW + BCM_AMBIENT_CTRL | 50ms 주기 | ethSelectedAlertMsg | frmAmbientControlMsg | CAN ACK 실패 시 안전 기본값 |
| TASK_010 | IVI_GW + CLU_HMI_CTRL | 50ms 주기 | ethSelectedAlertMsg | frmClusterWarningMsg | CAN ACK 실패 시 최소 안내 코드 |

---

## 6. 유닛 인터페이스 명세 (SWE.3 BP2)

| Interface ID | 제공 모듈 | 소비 모듈 | 데이터 | 연계 Flow/Comm | 제약 |
|---|---|---|---|---|---|
| IF_001 | CHASSIS_GW | ADAS_WARN_CTRL | vehicleSpeedNorm, driveStateNorm | Flow_001 / Comm_001 | 100ms 주기, 값 invalid 시 기본값 처리 |
| IF_002 | CHASSIS_GW | ADAS_WARN_CTRL | steeringInputNorm | Flow_002 / Comm_002 | 100ms 주기 |
| IF_003 | INFOTAINMENT_GW | NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | roadZone, navDirection, zoneDistance, speedLimit | Flow_003 / Comm_003 | 100ms 주기 |
| IF_004 | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | EmergencyType, EmergencyDirection, ETA, SourceID, AlertState | Flow_004~006 / Comm_004~006 | 100ms 송신, 1000ms 타임아웃 감시 |
| IF_005 | WARN_ARB_MGR | BODY_GW, IVI_GW | selectedAlertLevel, selectedAlertType, timeoutClear | Flow_006~008 / Comm_006~008 | 50ms 출력 |
| IF_006 | BODY_GW | BCM_AMBIENT_CTRL | ambientMode, ambientColor, ambientPattern | Flow_007 / Comm_007 | CAN ACK 실패 시 Fail-safe 적용 |
| IF_007 | IVI_GW | CLU_HMI_CTRL | warningTextCode | Flow_008 / Comm_008 | CAN ACK 실패 시 최소 안내 코드 |
| IF_008 | SIL_TEST_CTRL | SIL_TEST_CTRL(Log/Panel) | testScenario, scenarioResult | Flow_009 / Comm_009 | Event 기반 기록 |

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
| CHASSIS_GW CAN->ETH 변환 실패 | CHASSIS_GW watchdog | 마지막 정상값 1주기 유지 후 `warningState` 강등 | Req_001,Req_011 / Func_001,Func_011 / Flow_001,002 |
| INFOTAINMENT_GW CAN->ETH 변환 실패 | INFOTAINMENT_GW watchdog | `baseZoneContext` 일반구간 복귀, 유도 출력 해제 | Req_007,Req_016 / Func_007,Func_016 / Flow_003 |
| EmergencyAlert 1000ms 무갱신 | EMS_ALERT_RX timeout monitor | `timeoutClear=1`, `emergencyContext` clear | Req_024 / Func_024 / Flow_006 |
| BODY_GW CAN 송신 실패 | BODY_GW Tx ACK monitor | `ambientMode=0`으로 강등 후 최대 3회 재시도 | Req_033,Req_034 / Func_033,Func_034 / Flow_007 |
| IVI_GW CAN 송신 실패 | IVI_GW Tx ACK monitor | 최소 안내 코드로 1회 재송신 | Req_040 / Func_040 / Flow_008 |

---

## 9. 구현 산출물 검토 체크리스트

| 항목 | 기준 | 상태 |
|---|---|---|
| 스코프 정합 | CANoe SIL, CAN+Ethernet만 사용 | Defined |
| 아키텍처 정합 | 옵션1(ETH_SWITCH+Domain GW+CAN) 고정 | Defined |
| Func 구현 커버리지 | Func_001~Func_043 모두 Code Ref 존재 | Defined |
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
| 모듈/노드 명명 | Node는 `UPPER_SNAKE_CASE`, 내부 상태는 `camelCase` 유지 | `03_Function_definition.md`, `0304_System_Variables.md` |
| 인터페이스 명명 | 상위 공식 변수명은 0304 표준 Name, 코드 내부는 Internal Name 병기 | `0304_System_Variables.md` |
| 주기/타임아웃 | CAN 입력 100ms, 출력 50ms, Emergency timeout 1000ms 고정 | `0302_NWflowDef.md`, `01_Requirements.md` |
| 예외 처리 | invalid 값 수신 시 fail-safe 기본값 적용 후 로그 기록 | `0304_System_Variables.md`, 본 문서 8장 |
| 범위 통제 | OTA/UDS/DoIP 로직/문구는 구현 범위에서 제외 | `00b_Project_Scope.md` |
| 추적성 유지 | 변경 시 `Req->Func->Flow->Comm->Var->Code->UT/IT/ST` 동시 갱신 | `00_VModel_Mapping.md`, `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md` |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
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

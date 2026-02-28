# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.11
**Date**: 2026-02-28
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0301_SysFuncAnalysis.md` | `03_Function_definition.md` | `0302_NWflowDef.md` |

---

## 작성 원칙

- 본 문서는 03_Function_definition.md의 Func_001~Func_043을 노드 내부 동작 관점으로 분해한다.
- 각 노드의 입력-처리-출력을 명확히 정의해 0302의 Tx/Rx 흐름 설계로 연결한다.
- 요구사항(What) 문장을 반복하지 않고, 시스템 동작 로직(How)만 기술한다.
- 상단 표는 공식 표준 양식의 열 구성(노드/기능 상세/비고)을 유지한다.
- 상세 추적 정보(Func/Req/실제 입출력)는 하단 표에 분리한다.
- 옵션1 아키텍처를 고정한다: 중앙 경고코어 + Ethernet 백본(ETH_SWITCH) + 도메인 게이트웨이 + 도메인 CAN.
- 변수명은 0304 표준 Name(`vehicleSpeed`, `roadZone`, `speedLimit`) 기준으로 작성하고, 코드 별칭(`g*`)은 구현 문서에서만 사용한다.
- ECU 노드명은 ISO 기능 분리 원칙(센싱/판단/중재/출력/게이트웨이)을 따르고, OEM 레퍼런스는 `reference/dbc/level3_communication/reference/*.dbc`를 참고한다.

---

## 노드별 기능 명세 (공식 표준 양식)

| 노드 | 기능 상세 | 비고 |
|---|---|---|
|  |  | Powertrain |
| ADAS_WARN_CTRL | 차량 주행 상태 기반 경고 조건 판정 및 제어 상태 생성 | 경고 시작/해제 제어 |
| ENGINE_CTRL | 시동 상태 입력을 엔진 동작 상태로 반영 | 차량 기본 동작 |
| TRANSMISSION_CTRL | 기어 입력(P/R/N/D) 상태 유지 및 전달 | 차량 기본 동작 |
|  |  | Chassis |
| ACCEL_CTRL | 가속 페달 입력 상태 처리 | 차량 기본 동작 |
| BRAKE_CTRL | 브레이크 페달 입력 상태 처리 | 차량 기본 동작 |
| STEERING_CTRL | 조향 입력 상태 처리 | 차량 기본 동작 |
| EMS_ALERT_RX | 긴급 알림 수신 상태 및 해제 상태 관리 | 수신/타임아웃 해제 처리 |
| WARN_ARB_MGR | 긴급 경고와 구간 경고 충돌 시 우선순위 중재 수행 | Emergency > Zone, Ambulance > Police |
| EMS_POLICE_TX | 경찰 긴급차량 알림 생성 및 송신 제어 | EmergencyAlert 송신 제어 |
| EMS_AMB_TX | 구급 긴급차량 알림 생성 및 송신 제어 | EmergencyAlert 송신 제어 |
| SIL_TEST_CTRL | SIL 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드 |
| VEHICLE_BASE_TEST_CTRL | 차량 기본 기능 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드 |
|  |  | Network Infra |
| ETH_SWITCH | Ethernet 백본 스위칭 및 도메인 게이트웨이 전달 허브 | Ethernet 프레임 분배 |
| CHASSIS_GW | Chassis CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| INFOTAINMENT_GW | Infotainment CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| BODY_GW | 중재 결과 Ethernet 수신 후 Body CAN 출력 메시지 생성 | ETH->CAN 변환 |
| IVI_GW | 중재 결과 Ethernet 수신 후 Cluster CAN 출력 메시지 생성 | ETH->CAN 변환 |
| DOMAIN_GW_ROUTER | 도메인 간 입력/출력 프레임 전달 경로 관리 | Gateway Routing |
| DOMAIN_BOUNDARY_MGR | 도메인 통신 경계 정책 유지 및 충돌 차단 | Boundary Control |
|  |  | Body |
| BCM_AMBIENT_CTRL | 중재 결과 기반 앰비언트 경고 패턴 적용 | 색상/패턴 반영 |
| HAZARD_CTRL | 비상등 On/Off 상태 처리 | 차량 기본 동작 |
| WINDOW_CTRL | 창문 개폐 상태 처리 | 차량 기본 동작 |
| DRIVER_STATE_CTRL | 운전자 상태 입력 전달 | 차량 기본 동작 |
|  |  | Infotainment |
| NAV_CONTEXT_MGR | 내비게이션 구간/방향/거리/제한속도 기반 컨텍스트 갱신 | 구간 상태 전환 |
| CLU_HMI_CTRL | 운전자 경고 문구 및 안내 정보 표시 | 원인/방향/유형 표시 |
| CLUSTER_BASE_CTRL | 속도/기어/기본 상태 표시 | 차량 기본 동작 |
|  |  | Actual Device |
| Ambient Lights | 실제 앰비언트 장치가 제어 신호를 수신해 점등/패턴 동작 수행 | frmAmbientControlMsg(0x210) 반영 |
| Cluster Display | 실제 클러스터 장치가 경고 문구/상태를 표시 | frmClusterWarningMsg(0x220) 반영 |
| Navigation Panel | 사용자 입력(구간/방향/거리/제한속도) 제공 및 시각화 | Panel UI 입력 소스 |

---

## 기능 정의 상세 표 (추적성/입출력 정의)
| Func ID | Req ID | 실제 노드명 | 입력 (Input) | 처리 (Processing) | 출력 (Output) | 실제값 정의 |
|---|---|---|---|---|---|---|
| Func_007 | Req_007 | NAV_CONTEXT_MGR | roadZone, navDirection, zoneDistance, speedLimit | 구간 상태 판별 및 전환 컨텍스트 갱신 | baseZoneContext, speedLimitNorm | 입력: roadZone, navDirection, zoneDistance, speedLimit |
| Func_001~004,006,010~012 | Req_001~004,006,010~012 | ADAS_WARN_CTRL | vehicleSpeedNorm, speedLimitNorm, driveStateNorm, steeringInputNorm, baseZoneContext | 스쿨존 과속/고속 무조향 조건 판정, 경고 트리거 생성, 디바운스 | warningState | 입력: vehicleSpeedNorm, speedLimitNorm, driveStateNorm, steeringInputNorm, baseZoneContext |
| Func_013~016 | Req_013~Req_016 | BCM_AMBIENT_CTRL | selectedAlertType, selectedAlertLevel, navDirection, timeoutClear | 유도구간 진입 전환/방향 분기/전환 완화/종료 복귀 처리 | ambientMode, ambientPattern | 입력: selectedAlertType, selectedAlertLevel, navDirection, timeoutClear |
| Func_017 | Req_017 | EMS_POLICE_TX | testScenario | 경찰 긴급 알림 패킷 생성 및 송신 관리 | emergencyType, emergencyDirection, eta, sourceId, alertState, ETH_EmergencyAlert | 출력: ETH_EmergencyAlert(UDP) |
| Func_018 | Req_018 | EMS_AMB_TX | testScenario | 구급 긴급 알림 패킷 생성 및 송신 관리 | emergencyType, emergencyDirection, eta, sourceId, alertState, ETH_EmergencyAlert | 출력: ETH_EmergencyAlert(UDP) |
| Func_023,024 | Req_023,024 | EMS_ALERT_RX | alertState, emergencyType, lastEmergencyRxMs | 수신/해제 상태 관리, 1000ms 타임아웃 처리 | emergencyContext, timeoutClear | 입력: alertState, emergencyType, lastEmergencyRxMs |
| Func_022,025~032 | Req_022,025~032 | WARN_ARB_MGR | emergencyContext, warningState, baseZoneContext, emergencyType, eta, sourceId, arbitrationSnapshotId | 우선순위 중재 수행 | selectedAlertLevel, selectedAlertType | 입력: emergencyContext, warningState, baseZoneContext, emergencyType, eta, sourceId, arbitrationSnapshotId |
| Func_008,009,033~039 | Req_008,009,033~039 | BCM_AMBIENT_CTRL | selectedAlertLevel, selectedAlertType, navDirection, baseZoneContext, timeoutClear | 경고 등급별 색상/패턴 적용, 전환 완화, 복원 | ambientMode, ambientColor, ambientPattern | 출력: ambientMode, ambientColor, ambientPattern |
| Func_005,019~021,026,040 | Req_005,019~021,026,040 | CLU_HMI_CTRL | selectedAlertType, emergencyDirection, duplicatePopupGuard, warningTextCode | 경고 문구/종류/방향/양보 메시지 표시 | warningTextCode | 출력: warningTextCode |
| Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | SIL_TEST_CTRL | testScenario | 시나리오 실행, CAN+ETH 검증, 판정 기록 | scenarioResult | 출력: scenarioResult |
| Func_101 | Req_101 | ENGINE_CTRL | ignitionState | 시동 상태 반영 | engineState | 입력: ignitionState / 출력: engineState |
| Func_102 | Req_102 | TRANSMISSION_CTRL | gearInput | 기어 상태 반영 | gearState | 입력: gearInput / 출력: gearState |
| Func_103 | Req_103 | ACCEL_CTRL | accelPedal | 가속 입력 반영 | accelRequest | 입력: accelPedal / 출력: accelRequest |
| Func_104 | Req_104 | BRAKE_CTRL | brakePedal | 제동 입력 반영 | brakeRequest | 입력: brakePedal / 출력: brakeRequest |
| Func_105 | Req_105 | STEERING_CTRL | steeringInput | 조향 입력 반영 | steeringState | 입력: steeringInput / 출력: steeringState |
| Func_106 | Req_106 | HAZARD_CTRL | hazardSwitch | 비상등 기본 제어 | hazardState | 입력: hazardSwitch / 출력: hazardState |
| Func_107 | Req_107 | WINDOW_CTRL | windowCommand | 창문 기본 제어 | windowState | 입력: windowCommand / 출력: windowState |
| Func_108 | Req_108 | DRIVER_STATE_CTRL | driverStateLevel | 운전자 상태 전달 | driverStateInfo | 입력: driverStateLevel / 출력: driverStateInfo |
| Func_109 | Req_109 | CLUSTER_BASE_CTRL | vehicleSpeed, gearState, warningTextCode | 클러스터 기본 표시 | clusterBaseDisplay | 입력: vehicleSpeed, gearState / 출력: clusterBaseDisplay |
| Func_110 | Req_110 | DOMAIN_GW_ROUTER | domainInputFrames | 도메인 게이트웨이 전달 | domainOutputFrames | 입력: domainInputFrames / 출력: domainOutputFrames |
| Func_111 | Req_111 | DOMAIN_BOUNDARY_MGR | routingPolicy | 도메인 경계 유지 | boundaryStatus | 입력: routingPolicy / 출력: boundaryStatus |
| Func_112 | Req_112 | VEHICLE_BASE_TEST_CTRL | baseTestScenario | 차량 기본 기능 SIL 검증 | baseScenarioResult | 입력: baseTestScenario / 출력: baseScenarioResult |

## 2-1. Req-Func 1:1 감사 매핑 표

| Req ID | Func ID | 실제 노드명 | 기능명 |
|---|---|---|---|
| Req_001 | Func_001 | ADAS_WARN_CTRL | 주행시 경고엔진 활성 |
| Req_002 | Func_002 | ADAS_WARN_CTRL | 비주행 경고 억제 |
| Req_003 | Func_003 | ADAS_WARN_CTRL | 경고 시작 트리거 |
| Req_004 | Func_004 | ADAS_WARN_CTRL | 경고 종료 트리거 |
| Req_005 | Func_005 | CLU_HMI_CTRL | 경고 원인 전달 |
| Req_006 | Func_006 | ADAS_WARN_CTRL | 반복 경고 디바운스 |
| Req_007 | Func_007 | NAV_CONTEXT_MGR | 구간값 변경 반영 |
| Req_008 | Func_008 | BCM_AMBIENT_CTRL | 일반구간 정책 적용 |
| Req_009 | Func_009 | BCM_AMBIENT_CTRL | 스쿨존 강화 경고 |
| Req_010 | Func_010 | ADAS_WARN_CTRL | 스쿨존 과속 경고 |
| Req_011 | Func_011 | ADAS_WARN_CTRL | 고속 장시간 무조향 감지 |
| Req_012 | Func_012 | ADAS_WARN_CTRL | 무조향 경고 해제 |
| Req_013 | Func_013 | BCM_AMBIENT_CTRL | 유도구간 진입 전환 |
| Req_014 | Func_014 | BCM_AMBIENT_CTRL | 좌우 방향 구분 표시 |
| Req_015 | Func_015 | BCM_AMBIENT_CTRL | 구간 전환 완화 |
| Req_016 | Func_016 | BCM_AMBIENT_CTRL | 구간경고 종료 복귀 |
| Req_017 | Func_017 | EMS_POLICE_TX | 경찰 접근 경고 송신 |
| Req_018 | Func_018 | EMS_AMB_TX | 구급 접근 경고 송신 |
| Req_019 | Func_019 | CLU_HMI_CTRL | 긴급차량 종류 표시 |
| Req_020 | Func_020 | CLU_HMI_CTRL | 긴급차량 방향 표시 |
| Req_021 | Func_021 | CLU_HMI_CTRL | 양보 유도 메시지 |
| Req_022 | Func_022 | WARN_ARB_MGR | 긴급경고 우선 출력 |
| Req_023 | Func_023 | EMS_ALERT_RX | 종료 신호 처리 |
| Req_024 | Func_024 | EMS_ALERT_RX | 타임아웃 보호해제 |
| Req_025 | Func_025 | WARN_ARB_MGR | 다중긴급 단일선택 |
| Req_026 | Func_026 | CLU_HMI_CTRL | 중복 팝업 억제 |
| Req_027 | Func_027 | WARN_ARB_MGR | 충돌중재 개시 |
| Req_028 | Func_028 | WARN_ARB_MGR | 긴급>구간 우선 적용 |
| Req_029 | Func_029 | WARN_ARB_MGR | 구급>경찰 우선 적용 |
| Req_030 | Func_030 | WARN_ARB_MGR | ETA 우선 적용 |
| Req_031 | Func_031 | WARN_ARB_MGR | SourceID 동률판정 |
| Req_032 | Func_032 | WARN_ARB_MGR | 중재결과 결정론 보장 |
| Req_033 | Func_033 | BCM_AMBIENT_CTRL | 종료후 이전상태 복원 |
| Req_034 | Func_034 | BCM_AMBIENT_CTRL | 전환 깜빡임 완화 |
| Req_035 | Func_035 | BCM_AMBIENT_CTRL | 긴급 색상 정책 |
| Req_036 | Func_036 | BCM_AMBIENT_CTRL | 긴급 패턴 정책 |
| Req_037 | Func_037 | BCM_AMBIENT_CTRL | 스쿨존 패턴 정책 |
| Req_038 | Func_038 | BCM_AMBIENT_CTRL | 고속도로 패턴 정책 |
| Req_039 | Func_039 | BCM_AMBIENT_CTRL | 유도선 패턴 정책 |
| Req_040 | Func_040 | CLU_HMI_CTRL | 문구 길이 제한 |
| Req_041 | Func_041 | SIL_TEST_CTRL | SIL 시나리오 실행 |
| Req_042 | Func_042 | SIL_TEST_CTRL | CAN+ETH 동시 검증 |
| Req_043 | Func_043 | SIL_TEST_CTRL | 판정 결과 산출 |
| Req_101 | Func_101 | ENGINE_CTRL | 시동 상태 반영 |
| Req_102 | Func_102 | TRANSMISSION_CTRL | 기어 상태 반영 |
| Req_103 | Func_103 | ACCEL_CTRL | 가속 입력 반영 |
| Req_104 | Func_104 | BRAKE_CTRL | 제동 입력 반영 |
| Req_105 | Func_105 | STEERING_CTRL | 조향 입력 반영 |
| Req_106 | Func_106 | HAZARD_CTRL | 비상등 기본 제어 |
| Req_107 | Func_107 | WINDOW_CTRL | 창문 기본 제어 |
| Req_108 | Func_108 | DRIVER_STATE_CTRL | 운전자 상태 전달 |
| Req_109 | Func_109 | CLUSTER_BASE_CTRL | 클러스터 기본 표시 |
| Req_110 | Func_110 | DOMAIN_GW_ROUTER | 도메인 게이트웨이 전달 |
| Req_111 | Func_111 | DOMAIN_BOUNDARY_MGR | 도메인 경계 유지 |
| Req_112 | Func_112 | VEHICLE_BASE_TEST_CTRL | 차량 기본 기능 SIL 검증 |

---

## 3. 핵심 시나리오 동작 체인

| 시나리오 | 노드 동작 체인 | 연결 Func ID |
|---|---|---|
| 스쿨존 과속 | NAV_CONTEXT_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_007, Func_010, Func_027, Func_037, Func_040 |
| 고속도로 무조향 | NAV_CONTEXT_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_011, Func_012, Func_027, Func_038, Func_040 |
| 유도구간 방향 안내 | NAV_CONTEXT_MGR -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_013, Func_014, Func_039, Func_040 |
| 경찰 긴급차량 접근 | EMS_POLICE_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_017, Func_023, Func_022, Func_035, Func_019 |
| 구급 긴급차량 접근 | EMS_AMB_TX -> EMS_ALERT_RX -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_018, Func_023, Func_022, Func_035, Func_019 |
| 경찰+구급 동시 충돌 | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX -> WARN_ARB_MGR(우선순위/동률처리) -> 출력 노드 | Func_025~Func_031 |
| 긴급 해제 후 복귀 | EMS_ALERT_RX(해제/타임아웃) -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL/CLU_HMI_CTRL | Func_024, Func_033, Func_034 |

---

## 3-1. 네트워크 전달 체인 (옵션1 고정)

| 시나리오 | 네트워크 전달 체인 |
|---|---|
| Chassis 상태 입력 | SIL_TEST_CTRL -> Chassis CAN -> CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| Nav 구간 입력 | SIL_TEST_CTRL -> Infotainment CAN(roadZone/navDirection/zoneDistance/speedLimit) -> INFOTAINMENT_GW -> ETH_SWITCH -> NAV_CONTEXT_MGR/WARN_ARB_MGR |
| 긴급 신호 처리 | EMS_POLICE_TX/EMS_AMB_TX -> ETH_SWITCH -> EMS_ALERT_RX -> WARN_ARB_MGR |
| Ambient 출력 | WARN_ARB_MGR -> ETH_SWITCH -> BODY_GW -> Body CAN -> BCM_AMBIENT_CTRL |
| Cluster 출력 | WARN_ARB_MGR -> ETH_SWITCH -> IVI_GW -> Infotainment CAN -> CLU_HMI_CTRL |

---

## 4. 0302 연계 체크포인트

- 각 노드의 출력은 `0302_NWflowDef.md`에서 반드시 Flow ID로 정의한다.
- 최소 연계 규칙:
- `selectedAlertLevel/selectedAlertType` -> `frmAmbientControlMsg(0x210)` 송신 Flow 존재
- `selectedAlertLevel/selectedAlertType` -> `frmClusterWarningMsg(0x220)` 송신 Flow 존재
- `ETH_EmergencyAlert(0xE100)` 송신/수신/해제 Flow 존재
- 타임아웃(1000ms) 해제 Flow 존재

---

## 5. ECU 명명 기준 (ISO/OEM 정합)

| 분류 | 명명 규칙 | 현재 적용 예시 |
|---|---|---|
| Gateway | `*_GW` (도메인 경계 변환 역할) | CHASSIS_GW, INFOTAINMENT_GW, BODY_GW, IVI_GW |
| Controller | `*_CTRL` (기능 판단/제어 역할) | ADAS_WARN_CTRL, BCM_AMBIENT_CTRL, CLU_HMI_CTRL |
| Manager | `*_MGR` (중재/상태 관리 역할) | NAV_CONTEXT_MGR, WARN_ARB_MGR |
| Emergency Tx/Rx | `EMS_*_TX`, `EMS_*_RX` (긴급 송수신 역할) | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX |
| Test/SIL | `SIL_*` (검증 제어 역할) | SIL_TEST_CTRL |

- 적용 원칙: 문서/코드/DBC에서 노드명은 동일 식별자를 유지하고, 역할 구분은 접미사(`GW/CTRL/MGR/TX/RX`)로 고정한다.

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 2.0 | 2026-02-25 | 프로젝트 최신 스코프 기준 전면 재작성. 노드별 Input-Processing-Output 구조, Func/Req 연결, 핵심 시나리오 체인, 0302 연계 체크포인트 추가 |
| 3.0 | 2026-02-25 | 상단 공식 표준 양식 반영, 하단 상세 추적 표 분리 |
| 3.1 | 2026-02-25 | 상단 표를 이미지 표준 구조로 재정렬, 도메인 묶음(Powertrain/Chassis/Body/Infotainment/Actual Device) 반영 |
| 3.2 | 2026-02-25 | 상단 헤더를 표준(기능 상세)로 정렬, Actual Device를 실제 장치 기준으로 수정, Func_013~016 추적 보완 |
| 3.3 | 2026-02-25 | 옵션1 아키텍처 기준으로 Network Infra 노드(ETH_SWITCH/도메인 GW)와 네트워크 전달 체인 섹션 추가 |
| 3.4 | 2026-02-25 | Req_001~Req_043 / Func_001~Func_043 1:1 감사용 매핑 표(개별 행) 추가 |
| 3.5 | 2026-02-26 | Cluster 출력 전달체인을 Infotainment CAN 경로로 정합화(IVI_GW -> CLU_HMI_CTRL) |
| 3.6 | 2026-02-26 | 0304 표준 변수명 기준으로 상세 표기 통일(`g*` 별칭 제거) |
| 3.7 | 2026-02-28 | 03/0304 정합 기준으로 하단 상세표 입출력 변수를 재정렬(비정의 변수 제거, Core/State 변수명 통일) |
| 3.8 | 2026-02-28 | 스쿨존 과속 판정 정합을 위해 NAV/ADAS 입력에 `speedLimit/speedLimitNorm`을 반영하고 Navigation Panel 입력 항목을 확장. |
| 3.9 | 2026-02-28 | ISO/OEM 정합을 위한 ECU 명명 기준 섹션을 추가하고 노드 접미사 규칙(GW/CTRL/MGR/TX/RX)을 명문화. |
| 3.10 | 2026-02-28 | 차량 기본 기능 확장 대응으로 기본 차량 ECU 노드와 Req_101~Req_112 / Func_101~Func_112 매핑을 추가. |
| 3.11 | 2026-02-28 | 03 문서와의 노드 정합을 위해 `VEHICLE_BASE_TEST_CTRL`, `DOMAIN_GW_ROUTER`, `DOMAIN_BOUNDARY_MGR`를 상단 공식 노드 표에 추가. |

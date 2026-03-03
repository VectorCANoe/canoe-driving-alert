# 시스템 기능 분석 (System Function Analysis)

**Document ID**: PROJ-0301-SFA
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.19
**Date**: 2026-03-03
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0301_SysFuncAnalysis.md` | `03_Function_definition.md` | `0302_NWflowDef.md` |

---

## 작성 원칙

- 본 문서는 03_Function_definition.md의 Func_001~Func_124를 노드 내부 동작 관점으로 분해한다.
- V2 확장 요구(`Req_120~Req_124`)는 `Func_120~Func_124`로 구현 활성 상태에서 관리한다.
- 각 노드의 입력-처리-출력을 명확히 정의해 0302의 Tx/Rx 흐름 설계로 연결한다.
- 요구사항(What) 문장을 반복하지 않고, 시스템 동작 로직(How)만 기술한다.
- 상단 표는 공식 표준 양식의 열 구성(노드/기능 상세/비고)을 유지한다.
- 상세 추적 정보(Func/Req/실제 입출력)는 하단 표에 분리한다.
- 옵션1 아키텍처를 고정한다: 중앙 경고코어 + Ethernet 백본(ETH_SWITCH) + 도메인 게이트웨이 + 도메인 CAN.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- `SIL_TEST_CTRL`/`VEHICLE_BASE_TEST_CTRL`는 Validation Harness(검증 전용)이며, Gateway/도메인 통신 경로의 기능 노드로 해석하지 않는다.
- 변수명은 0304 표준 Name(`vehicleSpeed`, `roadZone`, `speedLimit`) 기준으로 작성하고, 코드 별칭(`g*`)은 구현 문서에서만 사용한다.
- ECU 노드명은 ISO 기능 분리 원칙(센싱/판단/중재/출력/게이트웨이)을 따르고, OEM 레퍼런스는 `reference/dbc/level3_communication/reference/*.dbc`를 참고한다.
- 제출 전 현대/기아 및 OEM 기준 명칭으로 일괄 대체하되, 추적 ID 체계는 유지한다.
- EMS는 상위 문서 계층에서 단일 논리 단말 `EMS_ALERT`로 관리하고, 내부 구현 모듈(TX/RX)은 하단 보강표에서만 분리한다.

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
| EMS_ALERT | 긴급 알림 송수신 상태 및 해제 상태 관리 | 송신/수신/타임아웃 통합 단말 |
| WARN_ARB_MGR | 긴급 경고와 구간 경고 충돌 시 우선순위 중재 및 감속 보조 요청/해제 수행 | Emergency > Zone, Ambulance > Police |
| SIL_TEST_CTRL | SIL 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드(Validation-only) |
| VEHICLE_BASE_TEST_CTRL | 차량 기본 기능 시나리오 실행 및 판정 결과 기록 | 검증 제어 가상노드(Validation-only) |
|  |  | Network Infra |
| ETH_SWITCH | Ethernet 백본 전달 인프라(시스템 관점) | 도메인 간 프레임 전달 경로 |
| CHASSIS_GW | Chassis CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| INFOTAINMENT_GW | Infotainment CAN 입력을 Ethernet 정규 메시지로 변환 | CAN->ETH 변환 |
| BODY_GW | 중재 결과 Ethernet 수신 후 Body CAN 출력 메시지 생성(HVAC/Seat/Mirror/Door/Wiper/Security 포함) | ETH->CAN 변환 |
| IVI_GW | 중재 결과 Ethernet 수신 후 Cluster CAN 출력 메시지 생성 | ETH->CAN 변환 |
| DOMAIN_GW_ROUTER | 도메인 간 입력/출력 프레임 전달 경로 관리 | Gateway Routing |
| DOMAIN_BOUNDARY_MGR | 도메인 통신 경계 정책 유지 및 충돌 차단 | Boundary Control |
|  |  | Body |
| BCM_AMBIENT_CTRL | 중재 결과 기반 앰비언트 경고 패턴 적용 | 색상/패턴 반영 |
| HAZARD_CTRL | 비상등 On/Off 상태 처리 | 차량 기본 동작 |
| WINDOW_CTRL | 창문/도어/미러 상태 처리 | 차량 기본 동작 |
| DRIVER_STATE_CTRL | 운전자/시트/보안 상태 입력 전달 | 차량 기본 동작 |
|  |  | Infotainment |
| NAV_CONTEXT_MGR | 내비게이션 구간/방향/거리/제한속도 기반 컨텍스트 갱신 | 구간 상태 전환 |
| CLU_HMI_CTRL | 운전자 경고 문구/안내 및 오디오 상태 정보 표시 | 원인/방향/유형/오디오 상태 표시 |
| CLUSTER_BASE_CTRL | 속도/기어/기본 상태 표시 | 차량 기본 동작 |
|  |  | Actual Device |
| Ambient Lights | 실제 앰비언트 장치가 제어 신호를 수신해 점등/패턴 동작 수행 | frmAmbientControlMsg(0x210) 반영 |
| Cluster Display | 실제 클러스터 장치가 경고 문구/상태를 표시 | frmClusterWarningMsg(0x220) 반영 |
| Navigation Panel | 사용자 입력(구간/방향/거리/제한속도) 제공 및 시각화 | Panel UI 입력 소스 |

- 시스템 아키텍처 관점에서 ETH_SWITCH는 백본 전달 인프라로 정의한다.
- 구현 관점의 ETH_SWITCH CAPL 역할(경로 헬스 모니터링)은 `04_SW_Implementation.md`에서 분리 관리한다.

---

## 기능 정의 상세 표 (추적성/입출력 정의)
| Func ID | Req ID | 실제 노드명 | 입력 (Input) | 처리 (Processing) | 출력 (Output) | 실제값 정의 |
|---|---|---|---|---|---|---|
| Func_007 | Req_007 | NAV_CONTEXT_MGR | roadZone, navDirection, zoneDistance, speedLimit | 구간 상태 판별 및 전환 컨텍스트 갱신 | baseZoneContext, speedLimitNorm | 입력: roadZone, navDirection, zoneDistance, speedLimit |
| Func_001~004,006,010~012 | Req_001~004,006,010~012 | ADAS_WARN_CTRL | vehicleSpeedNorm, speedLimitNorm, driveStateNorm, steeringInputNorm, baseZoneContext | 스쿨존 과속/고속 무조향 조건 판정, 경고 트리거 생성, 디바운스 | warningState | 입력: vehicleSpeedNorm, speedLimitNorm, driveStateNorm, steeringInputNorm, baseZoneContext |
| Func_013~016 | Req_013~Req_016 | BCM_AMBIENT_CTRL | selectedAlertType, selectedAlertLevel, navDirection, timeoutClear | 유도구간 진입 전환/방향 분기/전환 완화/종료 복귀 처리 | ambientMode, ambientPattern | 입력: selectedAlertType, selectedAlertLevel, navDirection, timeoutClear |
| Func_017 | Req_017 | EMS_ALERT | testScenario | 경찰 긴급 알림 패킷 생성 및 송신 관리(내부 Tx 모듈) | emergencyType, emergencyDirection, eta, sourceId, alertState, ETH_EmergencyAlert | 출력: ETH_EmergencyAlert(UDP) |
| Func_018 | Req_018 | EMS_ALERT | testScenario | 구급 긴급 알림 패킷 생성 및 송신 관리(내부 Tx 모듈) | emergencyType, emergencyDirection, eta, sourceId, alertState, ETH_EmergencyAlert | 출력: ETH_EmergencyAlert(UDP) |
| Func_023,024 | Req_023,024 | EMS_ALERT | alertState, emergencyType, lastEmergencyRxMs | 수신/해제 상태 관리, 1000ms 타임아웃 처리(내부 Rx 모듈) | emergencyContext, timeoutClear | 입력: alertState, emergencyType, lastEmergencyRxMs |
| Func_022,025~032 | Req_022,025~032 | WARN_ARB_MGR | emergencyContext, warningState, baseZoneContext, emergencyType, eta, sourceId, arbitrationSnapshotId | 우선순위 중재 수행 | selectedAlertLevel, selectedAlertType | 입력: emergencyContext, warningState, baseZoneContext, emergencyType, eta, sourceId, arbitrationSnapshotId |
| Func_008,009,033~039 | Req_008,009,033~039 | BCM_AMBIENT_CTRL | selectedAlertLevel, selectedAlertType, navDirection, baseZoneContext, timeoutClear | 경고 등급별 색상/패턴 적용, 전환 완화, 복원 | ambientMode, ambientColor, ambientPattern | 출력: ambientMode, ambientColor, ambientPattern |
| Func_005,019~021,026,040 | Req_005,019~021,026,040 | CLU_HMI_CTRL | selectedAlertType, emergencyDirection, duplicatePopupGuard, warningTextCode | 경고 문구/종류/방향/양보 메시지 표시 | warningTextCode | 출력: warningTextCode |
| Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | SIL_TEST_CTRL | testScenario | 시나리오 실행, CAN+ETH 검증, 판정 기록 | scenarioResult | 출력: scenarioResult |
| Func_101 | Req_101 | ENGINE_CTRL | IgnitionState | 시동 상태 반영 | EngineState | 입력: IgnitionState / 출력: EngineState |
| Func_102 | Req_102 | TRANSMISSION_CTRL | GearInput | 기어 상태 반영 | GearState | 입력: GearInput / 출력: GearState |
| Func_103 | Req_103 | ACCEL_CTRL | AccelPedal | 가속 입력 반영 | AccelRequest | 입력: AccelPedal / 출력: AccelRequest |
| Func_104 | Req_104 | BRAKE_CTRL | BrakePedal | 제동 입력 반영 | BrakePressure | 입력: BrakePedal / 출력: BrakePressure |
| Func_105 | Req_105 | STEERING_CTRL | steeringInput | 조향 입력 반영 | SteeringState | 입력: steeringInput / 출력: SteeringState |
| Func_106 | Req_106 | HAZARD_CTRL | HazardSwitch | 비상등 기본 제어 | HazardState | 입력: HazardSwitch / 출력: HazardState |
| Func_107 | Req_107 | WINDOW_CTRL | WindowCommand | 창문 기본 제어 | WindowState | 입력: WindowCommand / 출력: WindowState |
| Func_108 | Req_108 | DRIVER_STATE_CTRL | DriverStateLevel | 운전자 상태 전달 | DriverStateInfo | 입력: DriverStateLevel / 출력: DriverStateInfo |
| Func_109 | Req_109 | CLUSTER_BASE_CTRL | ClusterSpeed, ClusterGear, warningTextCode | 클러스터 기본 표시 | ClusterStatus | 입력: ClusterSpeed, ClusterGear, warningTextCode / 출력: ClusterStatus |
| Func_110 | Req_110 | DOMAIN_GW_ROUTER | RoutingPolicy | 도메인 게이트웨이 전달 | BodyGatewayRoute | 입력: RoutingPolicy / 출력: BodyGatewayRoute |
| Func_111 | Req_111 | DOMAIN_BOUNDARY_MGR | RoutingPolicy | 도메인 경계 유지 | BoundaryStatus | 입력: RoutingPolicy / 출력: BoundaryStatus |
| Func_112 | Req_112 | VEHICLE_BASE_TEST_CTRL | BaseScenarioId | 차량 기본 기능 SIL 검증 | BaseScnResult | 입력: BaseScenarioId / 출력: BaseScnResult |
| Func_113 | Req_113 | BODY_GW | CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode | HVAC 상태/제어 프레임 반영 | CabinTemp | 입력: CabinSetTemp, BlowerLevel, AcCompressorReq, VentMode / 출력: CabinTemp |
| Func_114 | Req_114 | DRIVER_STATE_CTRL | DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel | 시트 상태/제어 프레임 반영 | DriverStateInfo | 입력: DriverSeatPos, PassengerSeatPos, SeatHeatLevel, SeatVentLevel / 출력: DriverStateInfo |
| Func_115 | Req_115 | WINDOW_CTRL | MirrorFoldState, MirrorHeatState, MirrorAdjAxis | 미러 상태 프레임 반영 | WindowState | 입력: MirrorFoldState, MirrorHeatState, MirrorAdjAxis / 출력: WindowState |
| Func_116 | Req_116 | WINDOW_CTRL | DoorUnlockCmd, DoorLockState, DoorOpenWarn | 도어 제어/잠금/열림 상태 반영 | DoorStateMask | 입력: DoorUnlockCmd, DoorLockState, DoorOpenWarn / 출력: DoorStateMask |
| Func_117 | Req_117 | BCM_AMBIENT_CTRL | FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq | 와이퍼/우적 연동 상태 반영 | WiperInterval | 입력: FrontWiperState, RearWiperState, RainSensorLevel, AutoHeadlampReq / 출력: WiperInterval |
| Func_118 | Req_118 | DRIVER_STATE_CTRL | ImmoState, AlarmArmed, AlarmTrigger, AlarmZone | 이모빌라이저/경보 상태 반영 | DriverStateInfo | 입력: ImmoState, AlarmArmed, AlarmTrigger, AlarmZone / 출력: DriverStateInfo |
| Func_119 | Req_119 | CLU_HMI_CTRL | AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId | 오디오 포커스/음성비서/TTS 상태 반영 | warningTextCode | 입력: AudioFocusOwner, VoiceAssistState, TtsState, TtsLangId / 출력: warningTextCode |
| Func_120 | Req_120 | ADAS_WARN_CTRL | emergencyDirection, eta, vehicleSpeedNorm | 긴급차량 방향/ETA/자차속도 결합 기반 근접 위험도 산정 | proximityRiskLevel | 입력: emergencyDirection, eta, vehicleSpeedNorm / 출력: proximityRiskLevel |
| Func_121 | Req_121 | WARN_ARB_MGR | proximityRiskLevel, failSafeMode, driveStateNorm | 위험도 임계 초과 시 감속 보조 요청 생성 | decelAssistReq | 입력: proximityRiskLevel, failSafeMode, driveStateNorm / 출력: decelAssistReq |
| Func_122 | Req_122 | WARN_ARB_MGR | decelAssistReq, selectedAlertType, selectedAlertLevel | 감속 보조 활성 시 긴급 경고 우선 및 Ambient/Cluster 동기화 유지 | selectedAlertLevel, selectedAlertType | 입력: decelAssistReq, selectedAlertType, selectedAlertLevel / 출력: selectedAlertLevel, selectedAlertType |
| Func_123 | Req_123 | WARN_ARB_MGR | steeringInputNorm, brakePedalNorm | 운전자 제동/조향 회피 입력 시 감속 보조 요청 해제 | decelAssistReq | 입력: steeringInputNorm, brakePedalNorm / 출력: decelAssistReq |
| Func_124 | Req_124 | DOMAIN_BOUNDARY_MGR | domainPathStatus, e2eHealthState | 도메인 경로 단절 감지 시 자동 감속 보조 금지 + 최소 경고 채널 유지 | failSafeMode, decelAssistReq | 입력: domainPathStatus, e2eHealthState / 출력: failSafeMode, decelAssistReq |

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
| Req_017 | Func_017 | EMS_ALERT | 경찰 접근 경고 송신 |
| Req_018 | Func_018 | EMS_ALERT | 구급 접근 경고 송신 |
| Req_019 | Func_019 | CLU_HMI_CTRL | 긴급차량 종류 표시 |
| Req_020 | Func_020 | CLU_HMI_CTRL | 긴급차량 방향 표시 |
| Req_021 | Func_021 | CLU_HMI_CTRL | 양보 유도 메시지 |
| Req_022 | Func_022 | WARN_ARB_MGR | 긴급경고 우선 출력 |
| Req_023 | Func_023 | EMS_ALERT | 종료 신호 처리 |
| Req_024 | Func_024 | EMS_ALERT | 타임아웃 보호해제 |
| Req_025 | Func_025 | WARN_ARB_MGR | 다중긴급 단일선택 |
| Req_026 | Func_026 | CLU_HMI_CTRL | 중복 팝업 억제 |
| Req_027 | Func_027 | WARN_ARB_MGR | 충돌중재 적용 |
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
| Req_113 | Func_113 | BODY_GW | 공조 상태 반영 |
| Req_114 | Func_114 | DRIVER_STATE_CTRL | 시트 상태 반영 |
| Req_115 | Func_115 | WINDOW_CTRL | 미러 상태 반영 |
| Req_116 | Func_116 | WINDOW_CTRL | 도어 제어 상태 반영 |
| Req_117 | Func_117 | BCM_AMBIENT_CTRL | 와이퍼/우적 연동 반영 |
| Req_118 | Func_118 | DRIVER_STATE_CTRL | 보안 상태 반영 |
| Req_119 | Func_119 | CLU_HMI_CTRL | 오디오 상태 반영 |
| Req_120 | Func_120 | ADAS_WARN_CTRL | 긴급차량 근접 위험 판단 |
| Req_121 | Func_121 | WARN_ARB_MGR | 위험도 기반 감속 보조 요청 |
| Req_122 | Func_122 | WARN_ARB_MGR | 감속 보조-경고 동기화 |
| Req_123 | Func_123 | WARN_ARB_MGR | 운전자 개입 우선 해제 |
| Req_124 | Func_124 | DOMAIN_BOUNDARY_MGR | 도메인 경로 단절 강등(Fail-safe) |

---

## 3. 핵심 시나리오 동작 체인

| 시나리오 | 노드 동작 체인 | 연결 Func ID |
|---|---|---|
| 스쿨존 과속 | NAV_CONTEXT_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_007, Func_010, Func_027, Func_037, Func_040 |
| 고속도로 무조향 | NAV_CONTEXT_MGR -> ADAS_WARN_CTRL -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_011, Func_012, Func_027, Func_038, Func_040 |
| 유도구간 방향 안내 | NAV_CONTEXT_MGR -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_013, Func_014, Func_039, Func_040 |
| 경찰 긴급차량 접근 | EMS_ALERT(Police Tx) -> EMS_ALERT(Rx) -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_017, Func_023, Func_022, Func_035, Func_019 |
| 구급 긴급차량 접근 | EMS_ALERT(Amb Tx) -> EMS_ALERT(Rx) -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_018, Func_023, Func_022, Func_035, Func_019 |
| 경찰+구급 동시 충돌 | EMS_ALERT(Police Tx + Amb Tx) -> EMS_ALERT(Rx) -> WARN_ARB_MGR(우선순위/동률처리) -> 출력 노드 | Func_025~Func_031 |
| 긴급 해제 후 복귀 | EMS_ALERT(Rx 해제/타임아웃) -> WARN_ARB_MGR -> BCM_AMBIENT_CTRL/CLU_HMI_CTRL | Func_024, Func_033, Func_034 |
| 교차로/합류구간 근접위험 감속 보조 | EMS_ALERT(Rx) + ADAS_WARN_CTRL(위험도 산정) + WARN_ARB_MGR(보조요청/해제+경고 동기화) -> BRAKE_CTRL + BCM_AMBIENT_CTRL + CLU_HMI_CTRL | Func_120, Func_121, Func_122, Func_123 |
| 도메인 경로 단절 강등 | DOMAIN_BOUNDARY_MGR(경로 단절 감지) -> DOMAIN_GW_ROUTER -> WARN_ARB_MGR/출력노드 | Func_124 |

---

## 3-1. 네트워크 전달 체인 (옵션1 고정)

| 시나리오 | 네트워크 전달 체인 |
|---|---|
| Chassis 상태 입력 | SIL_TEST_CTRL -> Chassis CAN -> CHASSIS_GW -> ETH_SWITCH -> ADAS_WARN_CTRL |
| Nav 구간 입력 | SIL_TEST_CTRL -> Infotainment CAN(roadZone/navDirection/zoneDistance/speedLimit) -> INFOTAINMENT_GW -> ETH_SWITCH -> NAV_CONTEXT_MGR/WARN_ARB_MGR |
| 긴급 신호 처리 | EMS_ALERT(Tx) -> ETH_SWITCH -> EMS_ALERT(Rx) -> WARN_ARB_MGR |
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
| Emergency Terminal | `EMS_ALERT` (논리 단말), 내부 모듈은 `EMS_*_TX/RX`로 분리 | EMS_ALERT (internal: EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX) |
| Test/SIL | `SIL_*` (검증 제어 역할) | SIL_TEST_CTRL |

- 적용 원칙: 상위 문서(03/0301/0302/0303/0304)는 `EMS_ALERT` 논리 식별자를 기본으로 사용하고, 코드/DBC 구현 모듈 표기는 하단 보강표에서만 `EMS_*_TX/RX`로 표기한다.

### EMS 내부 모듈 매핑(감사 보강)

| 논리 노드 | 내부 모듈 | 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 이벤트 송신 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 이벤트 송신 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 이벤트 수신/해제/타임아웃 처리 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.19 | 2026-03-03 | ETH_SWITCH 역할을 시스템 관점으로 명확화하고, 구현 관점(헬스 모니터링)은 04 문서에서 분리 관리하도록 정합화. |
| 3.18 | 2026-03-03 | V2 확장 `Func_121/Func_123` 노드 소유를 `WARN_ARB_MGR`로 정정하고, 노드 표/Req-Func/시나리오 체인을 코드 구현 기준으로 동기화. |
| 3.17 | 2026-03-02 | 감사 정합 보강: 문서 범위를 `Func_001~Func_124`로 명확화하고 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구를 추가. |
| 3.16 | 2026-03-02 | V2 확장 제어 책임 분리: `DECEL_ASSIST_CTRL` 노드를 Chassis에 추가하고 `Func_121/Func_123` 실제 노드/시나리오 체인을 갱신. |
| 3.15 | 2026-03-02 | V2 확장(Pre-Activation) 반영: `Func_120~Func_124`(근접위험/감속보조/동기화/운전자개입해제/도메인단절강등) 상세표, Req-Func 매핑, 시나리오 체인 추가. |
| 3.14 | 2026-03-02 | `Func_101~Func_119` 상세표의 입출력 변수를 0304 표준 Name으로 정합화(`BaseScenarioId/BaseScnResult`, `AcCompressorReq`, `DoorUnlockCmd`, `ImmoState`, `TtsLangId` 등)하고 누락 변수명을 제거. |
| 3.13 | 2026-03-02 | V2 추적 밀도 보강 1차: `Req_113~Req_119`에 대응하는 `Func_113~Func_119`(HVAC/Seat/Mirror/Door/Wiper-Rain/Security/Audio)를 하단 상세표 및 1:1 감사 매핑에 추가. 상단 노드 설명도 기본 기능 확장 범위로 정합화. |
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
| 3.12 | 2026-03-01 | 멘토 피드백 반영: EMS 노드를 단일 논리 단말(`EMS_ALERT`)로 통합 표기하고, 내부 TX/RX 모듈은 하단 감사 보강표로 분리. |

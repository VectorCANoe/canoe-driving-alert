# 통신 명세서 (Communication Specification)

**Document ID**: PROJ-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 (Software Architectural Design)
**Version**: 3.26
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2) | `0303_Communication_Specification.md` | `0302_NWflowDef.md` | `0304_System_Variables.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 통신 계약(Comm) 중심으로 정리한다.
- 제출본은 상단 공식 Comm 표를 유지하고, 하단은 대표 행만 유지한다.
- ID/ETH 계약 상세는 원문 0303 및 00f/ETH 계약 문서를 참조한다.
- Comm-Flow 추적 키는 원문과 동일하게 유지한다.
- Pre-Activation 라벨은 원문과 동일하게 유지한다.

---

## CAN ID 배정 정책 (Project SoT)

- ID 상위 SoT는 `governance/00f_CAN_ID_Allocation_Standard.md`를 따른다.
- 본 장은 통신 스펙 관점의 실행 규칙만 요약한다.

| 규칙 | 정책 |
|---|---|
| 도메인 우선 분리 | CAN ID는 도메인별 블록(Chassis/Body/Infotainment/Powertrain/ADAS reserved)으로 우선 배정한다. |
| 논리 ID와 SIL Stub 분리 | Ethernet 논리 ID(`0xE100/0xE200/0xE210~0xE212`)와 CANoe SIL Stub ID(`0x1C3/0x1C4/0x111`)를 분리 표기한다. |
| 긴급 우선 해석 레벨 | `Req_022/028/029/030/031`의 기본 판정 축은 기능중재(`WARN_ARB_MGR`)이며, 버스 중재는 CAN ID 값으로만 결정한다. |
| Diag 명칭 해석 | 메시지명에 `Diag`가 포함되어도 Group 7 강제 배정 사유가 아니며, Owner/도메인 경계와 안전 경로를 우선 적용한다. |
| 충돌 회피 | 신규 ID 추가 시 기존 DBC ID와 중복 금지, 진단/검증 예약 구간과 충돌 금지 원칙을 따른다. |
| 확장성 | 기존 Flow/Comm 체인을 깨지 않도록 Comm 단위로 확장하고, 동일 변경에서 0302/0304/04/05~07 동시 갱신한다. |
| SoT 고정 | CAN ID SoT는 `canoe/databases/*.dbc`, Ethernet 계약 SoT는 `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`로 고정한다. |

---

## 통신 명세 표 (공식 표준 양식)

| Message | Identifier | DLC | Signal | signal bit position | Data 설명 | Data 범위 | Data 사용 |
|---|---|---|---|---|---|---|---|
| frmVehicleStateCanMsg | 0x2A0 | 2 | vehicleSpeed | 0~7 | 차량 속도 | 0~255 km/h | VAL_SCENARIO_CTRL -> CHS_GW 전달 |
|  |  |  | driveState | 8~9 | 주행 상태(PRND) | 0~3 | VAL_SCENARIO_CTRL -> CHS_GW 전달 |
| frmSteeringCanMsg | 0x2A1 | 1 | steeringInput | 0 | 조향 입력 여부 | 0~1 | VAL_SCENARIO_CTRL -> CHS_GW 전달 |
| frmPedalInputCanMsg | 0x2A2 | 2 | AccelPedal | 0~7 | 가속 페달 입력 | 0~100 % | VAL_SCENARIO_CTRL -> ACCEL_CTRL 전달 |
|  |  |  | BrakePedal | 8~15 | 브레이크 페달 입력 | 0~100 % | VAL_SCENARIO_CTRL -> BRK_CTRL 전달 |
| frmSteeringStateCanMsg | 0x100 | 1 | SteeringState | 0~1 | 조향 상태 | 0~3 | CHS_GW -> STEER_CTRL 전달 |
| frmWheelSpeedMsg | 0x101 | 4 | WheelSpdFL | 0~7 | 전륜 좌 휠속도 | 0~255 km/h | CHS_GW -> ACCEL_CTRL, BRK_CTRL, STEER_CTRL 전달 |
|  |  |  | WheelSpdFR | 8~15 | 전륜 우 휠속도 | 0~255 km/h | CHS_GW -> ACCEL_CTRL, BRK_CTRL, STEER_CTRL 전달 |
|  |  |  | WheelSpdRL | 16~23 | 후륜 좌 휠속도 | 0~255 km/h | CHS_GW -> ACCEL_CTRL, BRK_CTRL, STEER_CTRL 전달 |
|  |  |  | WheelSpdRR | 24~31 | 후륜 우 휠속도 | 0~255 km/h | CHS_GW -> ACCEL_CTRL, BRK_CTRL, STEER_CTRL 전달 |
| frmYawAccelMsg | 0x102 | 4 | YawRate | 0~15 | 요레이트 | 0~65535 deg/s | CHS_GW -> BRK_CTRL, STEER_CTRL 전달 |
|  |  |  | LatAccel | 16~31 | 횡가속도 | 0~65535 0.01m/s2 | CHS_GW -> BRK_CTRL, STEER_CTRL 전달 |
| frmBrakeStatusMsg | 0x120 | 2 | BrakePressure | 0~7 | 브레이크 압력 | 0~255 % | BRK_CTRL -> CHS_GW 전달 |
|  |  |  | BrakeMode | 8~9 | 브레이크 동작 모드 | 0~3 | BRK_CTRL -> CHS_GW 전달 |
|  |  |  | AbsActive | 10 | ABS 활성 상태 | 0~1 | BRK_CTRL -> CHS_GW 전달 |
|  |  |  | EspActive | 11 | ESP 활성 상태 | 0~1 | BRK_CTRL -> CHS_GW 전달 |
| frmAccelStatusMsg | 0x121 | 2 | AccelRequest | 0~7 | 가속 요청 | 0~100 % | ACCEL_CTRL -> CHS_GW 전달 |
|  |  |  | TorqueRequest | 8~15 | 토크 요청 | 0~255 Nm | ACCEL_CTRL -> CHS_GW 전달 |
| frmSteeringTorqueMsg | 0x122 | 2 | SteeringTorque | 0~11 | 조향 토크 | 0~4095 0.1Nm | STEER_CTRL -> CHS_GW 전달 |
|  |  |  | SteeringAssistLv | 12~15 | 조향 보조 레벨 | 0~15 | STEER_CTRL -> CHS_GW 전달 |
| frmChassisHealthMsg | 0x103 | 2 | ChassisAliveCnt | 0~7 | Chassis Alive Counter | 0~255 | CHS_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | ChassisDiagState | 8~11 | Chassis 진단 상태 | 0~15 | CHS_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | ChassisFailCode | 12~15 | Chassis 오류 코드 | 0~15 | CHS_GW -> VAL_SCENARIO_CTRL 전달 |
| frmNavContextCanMsg | 0x2A3 | 3 | roadZone | 0~1 | 구간 타입 | 0~3 | VAL_SCENARIO_CTRL -> INFOTAINMENT_GW 전달 |
|  |  |  | navDirection | 2~3 | 유도 방향 | 0~3 | VAL_SCENARIO_CTRL -> INFOTAINMENT_GW 전달 |
|  |  |  | zoneDistance | 8~15 | 구간 잔여 거리 | 0~255 m | VAL_SCENARIO_CTRL -> INFOTAINMENT_GW 전달 |
|  |  |  | speedLimit | 16~23 | 구간 제한속도 | 0~255 km/h | VAL_SCENARIO_CTRL -> INFOTAINMENT_GW 전달 |
| frmAmbientControlMsg | 0x260 | 1 | ambientMode | 0~2 | 앰비언트 모드 | 0~7 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | ambientColor | 3~5 | 앰비언트 색상 | 0~7 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | ambientPattern | 6~7 | 앰비언트 패턴 | 0~3 | BODY_GW -> AMBIENT_CTRL 전달 |
| frmHazardControlMsg | 0x261 | 1 | HazardSwitch | 0 | 비상등 스위치 | 0~1 | BODY_GW -> HAZARD_CTRL 전달 |
|  |  |  | HazardState | 1 | 비상등 상태 | 0~1 | BODY_GW -> HAZARD_CTRL 전달 |
| frmWindowControlMsg | 0x262 | 1 | WindowCommand | 0~1 | 창문 제어 명령 | 0~3 | BODY_GW -> WINDOW_CTRL 전달 |
|  |  |  | WindowState | 2~3 | 창문 상태 | 0~3 | BODY_GW -> WINDOW_CTRL 전달 |
| frmDoorStateMsg | 0x264 | 2 | DoorStateMask | 0~7 | 도어 상태 비트맵 | 0~255 | BODY_GW -> WINDOW_CTRL, DRV_STATE_MGR 전달 |
|  |  |  | DoorLockState | 8~9 | 도어 잠금 상태 | 0~3 | BODY_GW -> WINDOW_CTRL, DRV_STATE_MGR 전달 |
|  |  |  | ChildLockState | 10 | 아동 잠금 상태 | 0~1 | BODY_GW -> WINDOW_CTRL, DRV_STATE_MGR 전달 |
|  |  |  | DoorOpenWarn | 11 | 도어 열림 경고 | 0~1 | BODY_GW -> WINDOW_CTRL, DRV_STATE_MGR 전달 |
| frmLampControlMsg | 0x265 | 1 | HeadLampState | 0~1 | 전조등 상태 | 0~3 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | TailLampState | 2~3 | 후미등 상태 | 0~3 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | TurnLampState | 4~5 | 방향지시등 상태 | 0~3 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | HazardLampReq | 6 | 비상등 요청 | 0~1 | BODY_GW -> HAZARD_CTRL 전달 |
| frmWiperStateMsg | 0x266 | 1 | FrontWiperState | 0~1 | 전면 와이퍼 상태 | 0~3 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | RearWiperState | 2~3 | 후면 와이퍼 상태 | 0~3 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | WiperInterval | 4~7 | 와이퍼 인터벌 | 0~15 | BODY_GW -> AMBIENT_CTRL 전달 |
| frmSeatBeltStateMsg | 0x267 | 1 | DriverSeatBelt | 0 | 운전석 안전벨트 상태 | 0~1 | DRV_STATE_MGR -> BODY_GW, AMBIENT_CTRL 전달 |
|  |  |  | PassengerSeatBelt | 1 | 동승석 안전벨트 상태 | 0~1 | DRV_STATE_MGR -> BODY_GW, AMBIENT_CTRL 전달 |
|  |  |  | RearSeatBelt | 2~3 | 후석 안전벨트 상태 | 0~3 | DRV_STATE_MGR -> BODY_GW, AMBIENT_CTRL 전달 |
|  |  |  | SeatBeltWarnLvl | 4~5 | 안전벨트 경고 레벨 | 0~3 | DRV_STATE_MGR -> BODY_GW, AMBIENT_CTRL 전달 |
| frmCabinAirStateMsg | 0x268 | 2 | CabinTemp | 0~7 | 실내 온도 | 0~100 degC | DRV_STATE_MGR -> BODY_GW 전달 |
|  |  |  | AirQualityIndex | 8~15 | 실내 공기질 지수 | 0~255 | DRV_STATE_MGR -> BODY_GW 전달 |
| frmBodyHealthMsg | 0x269 | 2 | BodyAliveCnt | 0~7 | Body Alive Counter | 0~255 | BODY_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | BodyDiagState | 8~11 | Body 진단 상태 | 0~15 | BODY_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | BodyFailCode | 12~15 | Body 오류 코드 | 0~15 | BODY_GW -> VAL_SCENARIO_CTRL 전달 |
| frmClusterWarningMsg | 0x280 | 1 | warningTextCode | 0~7 | 클러스터 경고 코드 | 0~255 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmClusterBaseStateMsg | 0x281 | 2 | ClusterSpeed | 0~7 | 클러스터 표시 속도 | 0~255 km/h | IVI_GW -> CLU_BASE_CTRL 전달 |
|  |  |  | ClusterGear | 8~10 | 클러스터 표시 기어 | 0~7 | IVI_GW -> CLU_BASE_CTRL 전달 |
|  |  |  | ClusterStatus | 11~15 | 클러스터 기본 상태 | 0~31 | IVI_GW -> CLU_BASE_CTRL 전달 |
| frmNaviGuideStateMsg | 0x282 | 1 | GuideLaneState | 0~1 | 유도선 상태 | 0~3 | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
|  |  |  | GuideConfidence | 2~7 | 유도 신뢰도 | 0~63 | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
| frmMediaStateMsg | 0x283 | 2 | MediaSource | 0~2 | 미디어 소스 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | MediaState | 3~5 | 미디어 재생 상태 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | MuteState | 6 | 음소거 상태 | 0~1 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | VolumeLevel | 8~15 | 볼륨 레벨 | 0~100 % | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmCallStateMsg | 0x284 | 2 | CallState | 0~2 | 통화 상태 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | MicMute | 3 | 마이크 음소거 | 0~1 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | SignalQuality | 4~7 | 통신 품질 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | BtDeviceCount | 8~11 | 블루투스 연결 수 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmNavigationRouteMsg | 0x285 | 3 | RouteClass | 0~1 | 경로 분류 | 0~3 | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
|  |  |  | GuideType | 2~3 | 안내 유형 | 0~3 | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
|  |  |  | RouteProgress | 8~15 | 경로 진행률 | 0~100 % | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
|  |  |  | EtaMinutes | 16~23 | 도착 예상 시간(분) | 0~255 min | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
| frmClusterThemeMsg | 0x286 | 1 | ThemeMode | 0~2 | 클러스터 테마 모드 | 0~7 | IVI_GW -> CLU_BASE_CTRL 전달 |
|  |  |  | ClusterBrightness | 3~7 | 클러스터 밝기 | 0~31 | IVI_GW -> CLU_BASE_CTRL 전달 |
| frmHmiPopupStateMsg | 0x287 | 1 | PopupType | 0~3 | 팝업 유형 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | PopupPriority | 4~6 | 팝업 우선순위 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | PopupActive | 7 | 팝업 활성 상태 | 0~1 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmInfotainmentHealthMsg | 0x288 | 2 | InfoAliveCnt | 0~7 | Infotainment Alive Counter | 0~255 | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | InfoDiagState | 8~11 | Infotainment 진단 상태 | 0~15 | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | InfoFailCode | 12~15 | Infotainment 오류 코드 | 0~15 | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
| frmTestResultMsg | 0x2A5 | 1 | scenarioResult | 0 | 시나리오 판정 결과 | 0~1 | VAL_SCENARIO_CTRL -> - 전달 (Validation-only) |
| frmBaseTestResultMsg | 0x2A6 | 8 | BaseScenarioId | 0~7 | 기본 시나리오 ID | 0~255 | VAL_BASELINE_CTRL -> VAL_SCENARIO_CTRL 전달 (Validation-only) |
|  |  |  | BaseScenarioResult | 8 | 기본 시나리오 판정 | 0~1 | VAL_BASELINE_CTRL -> VAL_SCENARIO_CTRL 전달 |
| frmEmergencyBroadcastMsg | 0x1C0 | 4 | emergencyType | 0~3 | 긴급차량 타입 | 0~15 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (CAN-stub) |
|  |  |  | alertState | 4~5 | 긴급 상태 | 0~3 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (CAN-stub) |
|  |  |  | sourceId | 8~15 | 긴급 송신 주체 ID | 0~255 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (CAN-stub) |
|  |  |  | eta | 16~23 | 도달 예상 시간 | 0~255 s | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (CAN-stub) |
|  |  |  | emergencyDirection | 24~27 | 접근 방향 | 0~15 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (CAN-stub) |
| frmEmergencyMonitorMsg | 0x1C2 | 2 | emergencyContext | 0~7 | 긴급 컨텍스트 상태 | 0~255 | EMS_ALERT(Rx) -> CAN-stub 버스 운반(ETH_SW 모니터링) |
|  |  |  | TimeoutClearMon | 8 | 타임아웃 모니터 플래그 | 0~1 | EMS_ALERT(Rx) -> CAN-stub 버스 운반(ETH_SW 모니터링) |
| frmIgnitionEngineMsg | 0x2A8 | 1 | IgnitionState | 0 | 시동 입력 상태 | 0~1 | VAL_SCENARIO_CTRL -> ENG_CTRL 전달 |
|  |  |  | EngineState | 1~2 | 엔진 동작 상태 | 0~3 | VAL_SCENARIO_CTRL -> ENG_CTRL 전달 |
| frmGearStateMsg | 0x2A9 | 1 | GearInput | 0~2 | 기어 입력값 | 0~7 | VAL_SCENARIO_CTRL -> TCM 전달 |
|  |  |  | GearState | 3~5 | 기어 상태값 | 0~7 | VAL_SCENARIO_CTRL -> TCM 전달 |
| frmPowertrainGatewayMsg | 0x109 | 2 | RoutingPolicy | 0~7 | 도메인 라우팅 정책 | 0~255 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | BoundaryStatus | 8~15 | 도메인 경계 상태 | 0~255 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
| frmEngineSpeedTempMsg | 0x12A | 4 | EngineRpm | 0~15 | 엔진 회전수 | 0~65535 rpm | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
|  |  |  | CoolantTemp | 16~23 | 냉각수 온도 | 0~255 degC | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
|  |  |  | OilTemp | 24~31 | 엔진오일 온도 | 0~255 degC | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
| frmFuelBatteryStateMsg | 0x12B | 3 | FuelLevel | 0~7 | 연료 잔량 | 0~100 % | ENG_CTRL -> DOMAIN_ROUTER 전달 |
|  |  |  | BatterySoc | 8~15 | 배터리 SOC | 0~100 % | ENG_CTRL -> DOMAIN_ROUTER 전달 |
|  |  |  | ChargingState | 16~17 | 충전 상태 | 0~3 | ENG_CTRL -> DOMAIN_ROUTER 전달 |
| frmThrottleStateMsg | 0x12C | 2 | ThrottlePos | 0~7 | 스로틀 위치 | 0~100 % | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
|  |  |  | ThrottleReq | 8~15 | 스로틀 요청 | 0~100 % | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
| frmTransmissionTempMsg | 0x12D | 2 | TransOilTemp | 0~7 | 변속기 오일 온도 | 0~255 degC | TCM -> ENG_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | ClutchTemp | 8~15 | 클러치 온도 | 0~255 degC | TCM -> ENG_CTRL, DOMAIN_ROUTER 전달 |
| frmVehicleModeMsg | 0x10A | 2 | DriveMode | 0~2 | 주행 모드 | 0~7 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | EcoMode | 3 | 에코 모드 | 0~1 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | SportMode | 4 | 스포츠 모드 | 0~1 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | SnowMode | 5 | 스노우 모드 | 0~1 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | PowertrainState | 8~15 | 파워트레인 상태 | 0~255 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
| frmPowerLimitMsg | 0x10B | 2 | TorqueLimit | 0~7 | 토크 제한값 | 0~255 Nm | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | SpeedLimit | 8~15 | 속도 제한값 | 0~255 km/h | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
| frmCruiseStateMsg | 0x10C | 2 | CruiseState | 0~1 | 크루즈 상태 | 0~3 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | GapLevel | 2~3 | 차간 거리 레벨 | 0~3 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | CruiseSetSpeed | 8~15 | 크루즈 설정 속도 | 0~255 km/h | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
| frmPowertrainHealthMsg | 0x10D | 2 | PtAliveCnt | 0~7 | Powertrain Alive Counter | 0~255 | DOMAIN_ROUTER -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | PtDiagState | 8~11 | Powertrain 진단 상태 | 0~15 | DOMAIN_ROUTER -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | PtFailCode | 12~15 | Powertrain 오류 코드 | 0~15 | DOMAIN_ROUTER -> VAL_SCENARIO_CTRL 전달 |
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0~7 | 차량 속도 | 0~255 km/h | CHS_GW -> ADAS_WARN_CTRL 전달 (UDP) |
|  |  |  | driveState | 8~9 | 주행 상태(PRND) | 0~3 | CHS_GW -> ADAS_WARN_CTRL 전달 (UDP) |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 조향 입력 여부 | 0~1 | CHS_GW -> ADAS_WARN_CTRL 전달 (UDP) |
| ethNavContextMsg | 0x512 | 3 | roadZone | 0~1 | 구간 타입 | 0~3 | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
|  |  |  | navDirection | 2~3 | 유도 방향 | 0~3 | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
|  |  |  | zoneDistance | 8~15 | 구간 잔여 거리 | 0~255 m | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
|  |  |  | speedLimit | 16~23 | 구간 제한속도 | 0~255 km/h | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
| ETH_EmergencyAlert | 0xE100 | 4 | emergencyType | 0~1 | 긴급차량 종류 | 0~3 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (UDP) |
|  |  |  | emergencyDirection | 2~3 | 긴급차량 접근 방향 | 0~3 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (UDP) |
|  |  |  | eta | 8~15 | 도달 예상시간 | 0~255 s | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (UDP) |
|  |  |  | sourceId | 16~23 | 송신 주체 ID | 0~255 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (UDP) |
|  |  |  | alertState | 24 | 긴급 상태 | 0~1 | EMS_ALERT(Tx:Police/Ambulance) -> EMS_ALERT(Rx) 전달 (UDP) |
| ethSelectedAlertMsg | 0xE200 | 2 | selectedAlertLevel | 0~2 | 최종 경고 레벨 | 0~7 | WARN_ARB_MGR -> BODY_GW, IVI_GW 전달 (UDP) |
|  |  |  | selectedAlertType | 3~5 | 최종 경고 타입 | 0~7 | WARN_ARB_MGR -> BODY_GW, IVI_GW 전달 (UDP) |
|  |  |  | timeoutClear | 8 | 타임아웃 해제 플래그 | 0~1 | WARN_ARB_MGR -> BODY_GW, IVI_GW 전달 (UDP) |
| frmEpsStateMsg | 0x123 | 2 | EpsAssistState | 0~2 | EPS 보조 상태 | 0~7 | CHS_GW -> STEER_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | EpsFault | 3 | EPS 고장 상태 | 0~1 | CHS_GW -> STEER_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | EpsTorqueReq | 8~15 | EPS 토크 요청 | 0~255 0.1Nm | CHS_GW -> STEER_CTRL, DOMAIN_ROUTER 전달 |
| frmAbsStateMsg | 0x124 | 2 | AbsCtrlState | 0~2 | ABS 제어 상태 | 0~7 | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | AbsSlipLevel | 8~15 | ABS 슬립 레벨 | 0~255 | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
| frmEscStateMsg | 0x125 | 2 | EscCtrlState | 0~2 | ESC 제어 상태 | 0~7 | CHS_GW -> BRK_CTRL, STEER_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | YawCtrlReq | 8~15 | 요 모멘트 제어 요구 | 0~255 | CHS_GW -> BRK_CTRL, STEER_CTRL, DOMAIN_ROUTER 전달 |
| frmTcsStateMsg | 0x126 | 2 | TcsActive | 0 | TCS 활성 상태 | 0~1 | CHS_GW -> ACCEL_CTRL, BRK_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | TcsSlipRatio | 8~15 | TCS 슬립 비율 | 0~255 | CHS_GW -> ACCEL_CTRL, BRK_CTRL, DOMAIN_ROUTER 전달 |
| frmBrakeTempMsg | 0x127 | 2 | BrakeTempFL | 0~7 | 브레이크 전륜좌 온도 | 0~255 degC | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | BrakeTempFR | 8~15 | 브레이크 전륜우 온도 | 0~255 degC | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | BrakeTempRL | 16~23 | 브레이크 후륜좌 온도 | 0~255 degC | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | BrakeTempRR | 24~31 | 브레이크 후륜우 온도 | 0~255 degC | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
| frmSteeringAngleMsg | 0x128 | 2 | SteeringAngle | 0~15 | 조향각 | -720~720 deg | CHS_GW -> STEER_CTRL, ADAS_WARN_CTRL 전달 |
|  |  |  | SteeringAngleRate | 16~31 | 조향각속도 | -1024~1023 deg/s | CHS_GW -> STEER_CTRL, ADAS_WARN_CTRL 전달 |
| frmWheelPulseMsg | 0x104 | 2 | WheelPulseFL | 0~15 | 전륜좌 휠 펄스 | 0~65535 cnt | CHS_GW -> ACCEL_CTRL, BRK_CTRL, STEER_CTRL 전달 |
|  |  |  | WheelPulseFR | 16~31 | 전륜우 휠 펄스 | 0~65535 cnt | CHS_GW -> ACCEL_CTRL, BRK_CTRL, STEER_CTRL 전달 |
| frmSuspensionStateMsg | 0x105 | 2 | DamperMode | 0~2 | 댐퍼 모드 | 0~7 | CHS_GW -> DOMAIN_ROUTER 전달 |
|  |  |  | RideHeight | 8~15 | 차고 높이 | 0~255 mm | CHS_GW -> DOMAIN_ROUTER 전달 |
| frmTirePressureMsg | 0x106 | 4 | TirePressFL | 0~7 | 전륜좌 타이어 압력 | 0~255 kPa | CHS_GW -> DOMAIN_ROUTER 전달 |
|  |  |  | TirePressFR | 8~15 | 전륜우 타이어 압력 | 0~255 kPa | CHS_GW -> DOMAIN_ROUTER 전달 |
|  |  |  | TirePressRL | 16~23 | 후륜좌 타이어 압력 | 0~255 kPa | CHS_GW -> DOMAIN_ROUTER 전달 |
|  |  |  | TirePressRR | 24~31 | 후륜우 타이어 압력 | 0~255 kPa | CHS_GW -> DOMAIN_ROUTER 전달 |
| frmChassisDiagReqMsg | 0x2A4 | 3 | ChassisDiagReqId | 0~7 | Chassis 진단 요청 ID | 0~255 | VAL_SCENARIO_CTRL -> CHS_GW 전달 |
|  |  |  | ChassisDiagReqAct | 8 | Chassis 진단 요청 활성 | 0~1 | VAL_SCENARIO_CTRL -> CHS_GW 전달 |
| frmChassisDiagResMsg | 0x107 | 3 | ChassisDiagResId | 0~7 | Chassis 진단 응답 ID | 0~255 | CHS_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | ChassisDiagStatus | 8~11 | Chassis 진단 결과 | 0~15 | CHS_GW -> VAL_SCENARIO_CTRL 전달 |
| frmAdasChassisStatusMsg | 0x1C1 | 2 | AdasChassisState | 0~7 | ADAS 섀시 상태 코드 | 0~255 | ADAS_WARN_CTRL -> CAN-stub 버스 운반(상태 브로드캐스트) |
|  |  |  | AdasHealthLevel | 8~15 | ADAS 헬스 레벨 | 0~255 | ADAS_WARN_CTRL -> CAN-stub 버스 운반(상태 브로드캐스트) |
| frmBrakeWearMsg | 0x129 | 1 | BrakePadWearFL | 0~7 | 브레이크 패드 마모(전륜좌) | 0~100 % | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | BrakePadWearFR | 8~15 | 브레이크 패드 마모(전륜우) | 0~100 % | CHS_GW -> BRK_CTRL, DOMAIN_ROUTER 전달 |
| frmRoadFrictionMsg | 0x108 | 1 | RoadFrictionEst | 0~7 | 노면 마찰 추정치 | 0~255 | CHS_GW -> ADAS_WARN_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | SurfaceType | 8~11 | 노면 타입 | 0~15 | CHS_GW -> ADAS_WARN_CTRL, DOMAIN_ROUTER 전달 |
| frmHvacStateMsg | 0x26A | 2 | CabinSetTemp | 0~7 | 실내 설정 온도 | 0~63 degC | BODY_GW -> AMBIENT_CTRL, DRV_STATE_MGR 전달 |
|  |  |  | BlowerLevel | 8~11 | 블로워 레벨 | 0~15 | BODY_GW -> AMBIENT_CTRL, DRV_STATE_MGR 전달 |
| frmHvacActuatorMsg | 0x26B | 2 | VentMode | 0~2 | 공조 벤트 모드 | 0~7 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | AcCompressorReq | 3 | A/C 컴프레서 요청 | 0~1 | BODY_GW -> AMBIENT_CTRL 전달 |
| frmMirrorStateMsg | 0x26C | 1 | MirrorFoldState | 0 | 미러 폴딩 상태 | 0~1 | BODY_GW -> WINDOW_CTRL 전달 |
|  |  |  | MirrorHeatState | 1 | 미러 열선 상태 | 0~1 | BODY_GW -> WINDOW_CTRL 전달 |
|  |  |  | MirrorAdjAxis | 8~9 | 미러 조정 축 | 0~3 | BODY_GW -> WINDOW_CTRL 전달 |
| frmSeatStateMsg | 0x26D | 2 | DriverSeatPos | 0~7 | 운전석 시트 위치 | 0~255 | BODY_GW -> DRV_STATE_MGR 전달 |
|  |  |  | PassengerSeatPos | 8~15 | 동승석 시트 위치 | 0~255 | BODY_GW -> DRV_STATE_MGR 전달 |
| frmSeatControlMsg | 0x26E | 2 | SeatHeatLevel | 0~2 | 시트 히터 레벨 | 0~7 | BODY_GW -> DRV_STATE_MGR 전달 |
|  |  |  | SeatVentLevel | 3~5 | 시트 통풍 레벨 | 0~7 | BODY_GW -> DRV_STATE_MGR 전달 |
| frmDoorControlMsg | 0x26F | 1 | DoorUnlockCmd | 0~1 | 도어 언락 명령 | 0~3 | BODY_GW -> WINDOW_CTRL 전달 |
|  |  |  | TrunkOpenCmd | 2 | 트렁크 오픈 명령 | 0~1 | BODY_GW -> WINDOW_CTRL 전달 |
| frmInteriorLightMsg | 0x270 | 1 | InteriorLampMode | 0~2 | 실내등 모드 | 0~7 | BODY_GW -> AMBIENT_CTRL 전달 |
|  |  |  | InteriorLampLevel | 8~15 | 실내등 밝기 | 0~255 | BODY_GW -> AMBIENT_CTRL 전달 |
| frmRainLightAutoMsg | 0x271 | 1 | RainSensorLevel | 0~7 | 우적 센서 레벨 | 0~255 | BODY_GW -> AMBIENT_CTRL, WINDOW_CTRL 전달 |
|  |  |  | AutoHeadlampReq | 8 | 오토 헤드램프 요청 | 0~1 | BODY_GW -> AMBIENT_CTRL, WINDOW_CTRL 전달 |
| frmBcmDiagReqMsg | 0x272 | 3 | BcmDiagReqId | 0~7 | BCM 진단 요청 ID | 0~255 | VAL_SCENARIO_CTRL -> BODY_GW 전달 |
|  |  |  | BcmDiagReqAct | 8 | BCM 진단 요청 활성 | 0~1 | VAL_SCENARIO_CTRL -> BODY_GW 전달 |
| frmBcmDiagResMsg | 0x273 | 3 | BcmDiagResId | 0~7 | BCM 진단 응답 ID | 0~255 | BODY_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | BcmDiagStatus | 8~11 | BCM 진단 결과 | 0~15 | BODY_GW -> VAL_SCENARIO_CTRL 전달 |
| frmImmobilizerStateMsg | 0x274 | 1 | ImmoState | 0~1 | 이모빌라이저 상태 | 0~3 | BODY_GW -> DOMAIN_ROUTER, ENG_CTRL 전달 |
|  |  |  | KeyAuthState | 2~3 | 키 인증 상태 | 0~3 | BODY_GW -> DOMAIN_ROUTER, ENG_CTRL 전달 |
| frmAlarmStateMsg | 0x275 | 1 | AlarmArmed | 0 | 알람 경계 상태 | 0~1 | BODY_GW -> DRV_STATE_MGR, CLU_HMI_CTRL 전달 |
|  |  |  | AlarmTrigger | 1 | 알람 트리거 상태 | 0~1 | BODY_GW -> DRV_STATE_MGR, CLU_HMI_CTRL 전달 |
|  |  |  | AlarmZone | 8~11 | 알람 존 정보 | 0~15 | BODY_GW -> DRV_STATE_MGR, CLU_HMI_CTRL 전달 |
| frmBodyGatewayStateMsg | 0x276 | 2 | BodyGatewayLoad | 0~7 | Body GW 부하율 | 0~100 % | BODY_GW -> DOMAIN_ROUTER 전달 |
|  |  |  | BodyGatewayRoute | 8~15 | Body GW 라우팅 상태 | 0~255 | BODY_GW -> DOMAIN_ROUTER 전달 |
| frmBodyComfortStateMsg | 0x277 | 2 | ComfortMode | 0~2 | 컴포트 모드 | 0~7 | BODY_GW -> AMBIENT_CTRL, DRV_STATE_MGR 전달 |
|  |  |  | ChildSafetyState | 3 | 아동 안전 상태 | 0~1 | BODY_GW -> AMBIENT_CTRL, DRV_STATE_MGR 전달 |
| frmAudioFocusMsg | 0x289 | 1 | AudioFocusOwner | 0~2 | 오디오 포커스 소유자 | 0~7 | IVI_GW -> CLU_HMI_CTRL, CLU_BASE_CTRL 전달 |
|  |  |  | AudioDuckLevel | 8~15 | 오디오 덕킹 레벨 | 0~255 | IVI_GW -> CLU_HMI_CTRL, CLU_BASE_CTRL 전달 |
| frmVoiceAssistStateMsg | 0x28A | 1 | VoiceAssistState | 0~2 | 음성비서 상태 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | VoiceWakeSource | 8~11 | 음성 깨우기 소스 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmMapRenderStateMsg | 0x28B | 2 | MapZoomLevel | 0~7 | 지도 줌 레벨 | 0~255 | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
|  |  |  | MapTheme | 8~11 | 지도 테마 | 0~15 | INFOTAINMENT_GW -> NAV_CTX_MGR 전달 |
| frmRouteAlertMsg | 0x28C | 2 | NextTurnType | 0~3 | 다음 회전 유형 | 0~15 | INFOTAINMENT_GW -> NAV_CTX_MGR, CLU_HMI_CTRL 전달 |
|  |  |  | NextTurnDist | 8~15 | 다음 회전 잔여 거리 | 0~255 m | INFOTAINMENT_GW -> NAV_CTX_MGR, CLU_HMI_CTRL 전달 |
| frmTrafficEventMsg | 0x28D | 3 | TrafficEventType | 0~3 | 교통 이벤트 유형 | 0~15 | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL 전달 |
|  |  |  | TrafficSeverity | 4~6 | 교통 이벤트 심각도 | 0~7 | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL 전달 |
|  |  |  | TrafficDist | 8~15 | 이벤트 잔여 거리 | 0~255 m | INFOTAINMENT_GW -> NAV_CTX_MGR, ADAS_WARN_CTRL 전달 |
| frmPhoneProjectionMsg | 0x28E | 1 | ProjectionType | 0~2 | 프로젝션 유형 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | ProjectionState | 3~4 | 프로젝션 상태 | 0~3 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmClusterNotifMsg | 0x28F | 2 | ClusterNotifType | 0~3 | 클러스터 알림 유형 | 0~15 | IVI_GW -> CLU_HMI_CTRL, CLU_BASE_CTRL 전달 |
|  |  |  | ClusterNotifPrio | 4~6 | 클러스터 알림 우선순위 | 0~7 | IVI_GW -> CLU_HMI_CTRL, CLU_BASE_CTRL 전달 |
| frmIviDiagReqMsg | 0x2A7 | 3 | IviDiagReqId | 0~7 | IVI 진단 요청 ID | 0~255 | VAL_SCENARIO_CTRL -> INFOTAINMENT_GW 전달 (Validation-only) |
|  |  |  | IviDiagReqAct | 8 | IVI 진단 요청 활성 | 0~1 | VAL_SCENARIO_CTRL -> INFOTAINMENT_GW 전달 |
| frmIviDiagResMsg | 0x290 | 3 | IviDiagResId | 0~7 | IVI 진단 응답 ID | 0~255 | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | IviDiagStatus | 8~11 | IVI 진단 결과 | 0~15 | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
| frmMediaMetaMsg | 0x291 | 2 | MediaGenre | 0~3 | 미디어 장르 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | TrackProgress | 8~15 | 트랙 진행률 | 0~100 % | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmSpeechTtsStateMsg | 0x292 | 2 | TtsState | 0~2 | TTS 상태 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | TtsLangId | 8~15 | TTS 언어 ID | 0~255 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmConnectivityStateMsg | 0x293 | 2 | LteState | 0~2 | LTE 연결 상태 | 0~7 | INFOTAINMENT_GW -> NAV_CTX_MGR, CLU_HMI_CTRL 전달 |
|  |  |  | WifiState | 3 | Wi-Fi 연결 상태 | 0~1 | INFOTAINMENT_GW -> NAV_CTX_MGR, CLU_HMI_CTRL 전달 |
|  |  |  | BtState | 4 | Bluetooth 연결 상태 | 0~1 | INFOTAINMENT_GW -> NAV_CTX_MGR, CLU_HMI_CTRL 전달 |
| frmIviHealthDetailMsg | 0x294 | 2 | CpuLoad | 0~7 | IVI CPU 부하율 | 0~100 % | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | MemLoad | 8~15 | IVI 메모리 부하율 | 0~100 % | INFOTAINMENT_GW -> VAL_SCENARIO_CTRL 전달 |
| frmClusterSyncStateMsg | 0x295 | 2 | ClusterSyncState | 0~2 | 클러스터 동기화 상태 | 0~7 | IVI_GW -> CLU_BASE_CTRL 전달 |
|  |  |  | ClusterSyncSeq | 8~15 | 클러스터 동기화 시퀀스 | 0~255 | IVI_GW -> CLU_BASE_CTRL 전달 |
| frmEngineTorqueMsg | 0x12E | 2 | EngineTorqueAct | 0~15 | 엔진 실제 토크 | 0~65535 0.1Nm | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
|  |  |  | EngineTorqueReq | 16~31 | 엔진 요구 토크 | 0~65535 0.1Nm | ENG_CTRL -> TCM, DOMAIN_ROUTER 전달 |
| frmEngineLoadMsg | 0x12F | 1 | EngineLoad | 0~7 | 엔진 부하율 | 0~100 % | ENG_CTRL -> DOMAIN_ROUTER 전달 |
|  |  |  | ManifoldPressure | 8~15 | 흡기 매니폴드 압력 | 0~255 kPa | ENG_CTRL -> DOMAIN_ROUTER 전달 |
| frmTransShiftStateMsg | 0x130 | 2 | ShiftState | 0~2 | 변속 상태 | 0~7 | TCM -> ENG_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | ShiftInProgress | 3 | 변속 진행 상태 | 0~1 | TCM -> ENG_CTRL, DOMAIN_ROUTER 전달 |
|  |  |  | ShiftTargetGear | 8~10 | 목표 기어 | 0~7 | TCM -> ENG_CTRL, DOMAIN_ROUTER 전달 |
| frmPtDiagReqMsg | 0x2AA | 3 | PtDiagReqId | 0~7 | Powertrain 진단 요청 ID | 0~255 | VAL_SCENARIO_CTRL -> DOMAIN_ROUTER 전달 (Validation-only) |
|  |  |  | PtDiagReqAct | 8 | Powertrain 진단 요청 활성 | 0~1 | VAL_SCENARIO_CTRL -> DOMAIN_ROUTER 전달 |
| frmPtDiagResMsg | 0x10E | 3 | PtDiagResId | 0~7 | Powertrain 진단 응답 ID | 0~255 | DOMAIN_ROUTER -> VAL_SCENARIO_CTRL 전달 |
|  |  |  | PtDiagStatus | 8~11 | Powertrain 진단 결과 | 0~15 | DOMAIN_ROUTER -> VAL_SCENARIO_CTRL 전달 |
| frmThermalMgmtStateMsg | 0x131 | 2 | ThermalMode | 0~2 | 열관리 모드 | 0~7 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | FanSpeedCmd | 8~15 | 팬 속도 명령 | 0~255 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
| frmEnergyFlowStateMsg | 0x10F | 2 | RegenLevel | 0~3 | 회생 제동 레벨 | 0~15 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | EnergyFlowDir | 4~5 | 에너지 흐름 방향 | 0~3 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
| frmPowertrainCtrlAuthMsg | 0x110 | 1 | PtCtrlAuthState | 0~1 | 파워트레인 제어 권한 상태 | 0~3 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
|  |  |  | PtCtrlSource | 8~11 | 파워트레인 제어 출처 | 0~15 | DOMAIN_ROUTER -> ENG_CTRL, TCM 전달 |
---

## 통신 원본(Source of Truth) 매핑

| 구분 | 범위 | 원본 파일 | 비고 |
|---|---|---|---|
| Core CAN Profile | Comm_001, Comm_002, Comm_003, Comm_007, Comm_008, Comm_009 | `canoe/databases/chassis_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` | 경고 코어 체인 단일 원본(CAN-stub 포함) |
| Domain CAN Profile | Comm_101~Comm_106, Comm_201~Comm_205 | `canoe/databases/chassis_can.dbc` + `canoe/databases/powertrain_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` | 차량 기본 기능/도메인 분리 원본(CAN-stub 포함) |
| ADAS CAN Profile | Comm_120, Comm_201(일부) | `canoe/databases/adas_can.dbc` | ADAS 소유 프레임 원본 |
| ETH Stub Transport Profile | Comm_004, Comm_005, Comm_006, Comm_121, Comm_124 | `canoe/databases/eth_backbone_can_stub.dbc` | CANoe.CAN 환경 대체 운반 원본 |
| Ethernet Profile (Logical Contract) | Comm_004, Comm_005, Comm_006, Comm_120, Comm_121, Comm_124 (및 Comm_001~003/007~008의 ETH 구간) | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | UDP 활성 계약 단일 원본 |
| Ethernet Profile (Pending-PreActivation) | Comm_130~Comm_133 | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` (v1.2 예정) | `E213~E216` 계약 반영 전에는 참조 전용(활성 SoT 아님) |

---

## 통신 상세 추적 표 (Comm/Flow/Func/Req)

| Comm ID | Flow ID | Func ID | Req ID | Message(ID) | Tx Node | Rx Node | Protocol | Period | Clear/비고 |
|---|---|---|---|---|---|---|---|---|---|
| Comm_001 | Flow_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x2A0), ethVehicleStateMsg(0x510) | VAL_SCENARIO_CTRL, CHS_GW | CHS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 |
| Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x2A1), ethSteeringMsg(0x511) | VAL_SCENARIO_CTRL, CHS_GW | CHS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 |
| Comm_003 | Flow_003 | Func_007, Func_010 | Req_007, Req_010 | frmNavContextCanMsg(0x2A3), ethNavContextMsg(0x512) | VAL_SCENARIO_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리/제한속도 입력 갱신 |
| Comm_004 | Flow_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Police) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_005 | Flow_005 | Func_018 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Ambulance) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_006 | Flow_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032, Func_144, Func_149, Func_150, Func_152 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032, Req_144, Req_149, Req_150, Req_152 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT(Rx), WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | 1000ms 무갱신 시 timeoutClear=1 |
| Comm_007 | Flow_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039, Func_152 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_037, Req_152 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260) | WARN_ARB_MGR, BODY_GW | BODY_GW, AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_008 | Flow_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040, Func_143, Func_152, Func_155 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040, Req_143, Req_152, Req_155 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x280) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_009 | Flow_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x2A5) | VAL_SCENARIO_CTRL | VAL_SCENARIO_CTRL(Log/Panel) | CAN | Event | 판정 결과 기록 완료 시 종료 |
| Comm_120 | Flow_120 | Func_120 | Req_120 | ethEmergencyRiskMsg(0x1C3) | ADAS_WARN_CTRL | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | 100ms | 근접위험 산정 프레임 |
| Comm_121 | Flow_121 | Func_121 | Req_121 | ethDecelAssistReqMsg(0x1C4) | WARN_ARB_MGR | CHS_GW, BRK_CTRL, VAL_SCENARIO_CTRL | Ethernet(UDP) + CAN | Event + 50ms | 감속 보조 요청 프레임 |
| Comm_122 | Flow_122 | Func_125, Func_126 | Req_125, Req_126 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260), frmClusterWarningMsg(0x280) | WARN_ARB_MGR | BODY_GW, IVI_GW, AMBIENT_CTRL, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | 감속 보조 활성 경고 동기화 |
| Comm_123 | Flow_123 | Func_123 | Req_123 | frmPedalInputCanMsg(0x2A2), frmSteeringCanMsg(0x2A1), ethDecelAssistReqMsg(0x1C4) | CHS_GW, WARN_ARB_MGR | WARN_ARB_MGR, DOMAIN_ROUTER, BRK_CTRL | CAN + Ethernet(UDP) | Event + 100ms | 운전자 개입 시 보조 해제 |
| Comm_124 | Flow_124 | Func_127, Func_128, Func_129, Func_151, Func_152 | Req_127, Req_128, Req_129, Req_151, Req_152 | frmChassisHealthMsg(0x103), frmBodyHealthMsg(0x269), frmInfotainmentHealthMsg(0x288), ethFailSafeStateMsg(0x111) | CHS_GW, BODY_GW, INFOTAINMENT_GW, DOMAIN_BOUNDARY_MGR | DOMAIN_BOUNDARY_MGR, DOMAIN_ROUTER, WARN_ARB_MGR, BODY_GW, IVI_GW, VAL_SCENARIO_CTRL | CAN + Ethernet(UDP) | 100ms + Event | 경로 단절 강등/보조 금지 |
| Comm_130 | Flow_130 | Func_130, Func_131, Func_148 | Req_130, Req_131, Req_148 | ethObjectRiskInputMsg(0xE213) | CHS_GW, INFOTAINMENT_GW | ADAS_WARN_CTRL | Ethernet(UDP) | 100ms | 객체 목록/대표 위험 후보 입력 (Pre-Activation, ETH 계약 v1.2 대기) |
| Comm_131 | Flow_131 | Func_132, Func_133, Func_136 | Req_132, Req_133, Req_136 | ethObjectRiskStateMsg(0xE214) | ADAS_WARN_CTRL | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | 100ms + Event | TTC/상대속도/거리 기반 위험 상태 (Pre-Activation, ETH 계약 v1.2 대기) |
| Comm_132 | Flow_132 | Func_134, Func_135, Func_139 | Req_134, Req_135, Req_139 | ethObjectScenarioAlertMsg(0xE215), frmAmbientControlMsg(0x260), frmClusterWarningMsg(0x280) | WARN_ARB_MGR | BODY_GW, IVI_GW, AMBIENT_CTRL, CLU_HMI_CTRL | Ethernet(UDP) + CAN | Event + 50ms | 교차로/합류 객체 경고 및 우선순위 정합 (Pre-Activation, ETH 계약 v1.2 대기) |
| Comm_133 | Flow_133 | Func_137, Func_138, Func_148 | Req_137, Req_138, Req_148 | ethObjectSafetyStateMsg(0xE216) | DOMAIN_BOUNDARY_MGR, EMS_ALERT | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | Event | 신뢰도 강등 및 객체 이벤트 기록 (Pre-Activation, ETH 계약 v1.2 대기) |

---

## 하단 확장표 축소 (제출본)

- 상단 공식 통신 표와 `통신 상세 추적 표`를 제출 기준 본표로 유지한다.
- 도메인별 Comm 확장 전수표는 중복을 줄이기 위해 요약만 유지한다.
- 상세 전수 매핑은 원문 SoT(`driving-situation-alert/0303_Communication_Specification.md`)를 기준으로 관리한다.

| 구분 | 제출본 유지 내용 | 원문 SoT 참조 |
|---|---|---|
| 도메인별 통신 원본 | Domain CAN/ETH 논리 계약 분리 원칙 요약 | 0303 원문 `도메인별 통신 원본 확장 정의` |
| Vehicle Baseline 확장 | Comm_101~106, Comm_201~205 `Defined` 상태 유지 | 0303 원문 Baseline/Phase-B 확장 표 |
| V2 확장 | Comm_120~124 `Implemented` 상태 유지 | 0303 원문 V2 확장 표 |
| ADAS 객체 인지 확장 | Comm_130~133 `Planned(Pre-Activation)` 유지 | 0303 원문 ADAS 확장 표 |
| 활성 승격 조건 | `ETH_INTERFACE_CONTRACT.md v1.2`의 `E213~E216` 반영 시 활성 | 0303 원문 ADAS 확장 섹션 |

---

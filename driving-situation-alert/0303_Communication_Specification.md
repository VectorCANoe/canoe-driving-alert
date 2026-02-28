# 통신 명세서 (Communication Specification)

**Document ID**: PROJ-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 (Software Architectural Design)
**Version**: 3.4
**Date**: 2026-02-28
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2) | `0303_Communication_Specification.md` | `0302_NWflowDef.md` | `0304_System_Variables.md` |

---

## 작성 원칙

- 상단 표는 공식 샘플(`0303.md`)과 동일하게 `Message/Identifier/DLC/Signal/signal bit position/Data 설명/Data 범위/Data 사용` 열만 사용한다.
- `Identifier`는 순수 ID 값만 기재한다(예: `0x100`, `0xE100`).
- `DLC`는 순수 숫자만 기재한다.
- 상단 표의 `Signal`은 0304 표준 변수명(`vehicleSpeed` 등) 기준으로 작성하고, 코드/런타임 별칭(`g*`)은 하단 보강표에서만 관리한다.
- 0304에 아직 등재되지 않은 Vehicle Baseline 확장 신호는 DBC 원본 신호명(`AccelPedal`, `DriveMode` 등)으로 표기한다.
- CAN 통신 원본은 계층 분리로 관리한다: 코어 프로파일은 `canoe/network/dbc/emergency_system.dbc`, 도메인 확장 프로파일은 `canoe/network/dbc/emergency_system_*.dbc`, Ethernet 프로파일은 `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`를 사용한다.
- 본 설계는 Ethernet 백본(`ETH_SWITCH`) + 도메인 게이트웨이(`CHASSIS_GW`, `INFOTAINMENT_GW`, `BODY_GW`, `IVI_GW`) + 도메인 CAN 분배 구조를 사용한다.
- 하단 추적표는 `Comm ID -> Flow ID -> Func ID -> Req ID`를 유지한다.
- 제출 전 현대/기아 및 OEM 기준으로 설명/별칭은 정리하되, Message ID/DLC/Bit Position/Signal 식별자는 SoT 기준으로 고정 유지한다.
- 검증 범위는 CANoe SIL, CAN + Ethernet(UDP)로 고정한다.
- Vehicle Baseline(Req_101~Req_112) 통신(`Comm_101~Comm_106`)은 본 문서에서 확정 정의하고, 도메인 DBC는 이 정의를 구현 대상으로 사용한다.

---

## 통신 명세 표 (공식 표준 양식)

| Message | Identifier | DLC | Signal | signal bit position | Data 설명 | Data 범위 | Data 사용 |
|---|---|---|---|---|---|---|---|
| frmVehicleStateCanMsg | 0x100 | 2 | vehicleSpeed | 0~7 | 차량 속도 | 0~255 km/h | SIL_TEST_CTRL -> CHASSIS_GW 전달 |
|  |  |  | driveState | 8~9 | 주행 상태(PRND) | 0~3 | SIL_TEST_CTRL -> CHASSIS_GW 전달 |
| frmSteeringCanMsg | 0x101 | 1 | steeringInput | 0 | 조향 입력 여부 | 0~1 | SIL_TEST_CTRL -> CHASSIS_GW 전달 |
| frmPedalInputCanMsg | 0x102 | 2 | AccelPedal | 0~7 | 가속 페달 입력 | 0~100 % | SIL_TEST_CTRL -> ACCEL_CTRL 전달 |
|  |  |  | BrakePedal | 8~15 | 브레이크 페달 입력 | 0~100 % | SIL_TEST_CTRL -> BRAKE_CTRL 전달 |
| frmSteeringStateCanMsg | 0x103 | 1 | SteeringState | 0~1 | 조향 상태 | 0~3 | CHASSIS_GW -> STEERING_CTRL 전달 |
| frmWheelSpeedMsg | 0x104 | 4 | WheelSpdFL | 0~7 | 전륜 좌 휠속도 | 0~255 km/h | CHASSIS_GW -> ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL 전달 |
|  |  |  | WheelSpdFR | 8~15 | 전륜 우 휠속도 | 0~255 km/h | CHASSIS_GW -> ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL 전달 |
|  |  |  | WheelSpdRL | 16~23 | 후륜 좌 휠속도 | 0~255 km/h | CHASSIS_GW -> ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL 전달 |
|  |  |  | WheelSpdRR | 24~31 | 후륜 우 휠속도 | 0~255 km/h | CHASSIS_GW -> ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL 전달 |
| frmYawAccelMsg | 0x105 | 4 | YawRate | 0~15 | 요레이트 | 0~65535 deg/s | CHASSIS_GW -> BRAKE_CTRL, STEERING_CTRL 전달 |
|  |  |  | LatAccel | 16~31 | 횡가속도 | 0~65535 0.01m/s2 | CHASSIS_GW -> BRAKE_CTRL, STEERING_CTRL 전달 |
| frmBrakeStatusMsg | 0x106 | 2 | BrakePressure | 0~7 | 브레이크 압력 | 0~255 % | BRAKE_CTRL -> CHASSIS_GW 전달 |
|  |  |  | BrakeMode | 8~9 | 브레이크 동작 모드 | 0~3 | BRAKE_CTRL -> CHASSIS_GW 전달 |
|  |  |  | AbsActive | 10 | ABS 활성 상태 | 0~1 | BRAKE_CTRL -> CHASSIS_GW 전달 |
|  |  |  | EspActive | 11 | ESP 활성 상태 | 0~1 | BRAKE_CTRL -> CHASSIS_GW 전달 |
| frmAccelStatusMsg | 0x107 | 2 | AccelRequest | 0~7 | 가속 요청 | 0~100 % | ACCEL_CTRL -> CHASSIS_GW 전달 |
|  |  |  | TorqueRequest | 8~15 | 토크 요청 | 0~255 Nm | ACCEL_CTRL -> CHASSIS_GW 전달 |
| frmSteeringTorqueMsg | 0x108 | 2 | SteeringTorque | 0~11 | 조향 토크 | 0~4095 0.1Nm | STEERING_CTRL -> CHASSIS_GW 전달 |
|  |  |  | SteeringAssistLv | 12~15 | 조향 보조 레벨 | 0~15 | STEERING_CTRL -> CHASSIS_GW 전달 |
| frmChassisHealthMsg | 0x109 | 2 | ChassisAliveCnt | 0~7 | Chassis Alive Counter | 0~255 | CHASSIS_GW -> SIL_TEST_CTRL 전달 |
|  |  |  | ChassisDiagState | 8~11 | Chassis 진단 상태 | 0~15 | CHASSIS_GW -> SIL_TEST_CTRL 전달 |
|  |  |  | ChassisFailCode | 12~15 | Chassis 오류 코드 | 0~15 | CHASSIS_GW -> SIL_TEST_CTRL 전달 |
| frmNavContextCanMsg | 0x110 | 3 | roadZone | 0~1 | 구간 타입 | 0~3 | SIL_TEST_CTRL -> INFOTAINMENT_GW 전달 |
|  |  |  | navDirection | 2~3 | 유도 방향 | 0~3 | SIL_TEST_CTRL -> INFOTAINMENT_GW 전달 |
|  |  |  | zoneDistance | 8~15 | 구간 잔여 거리 | 0~255 m | SIL_TEST_CTRL -> INFOTAINMENT_GW 전달 |
|  |  |  | speedLimit | 16~23 | 구간 제한속도 | 0~255 km/h | SIL_TEST_CTRL -> INFOTAINMENT_GW 전달 |
| frmAmbientControlMsg | 0x210 | 1 | ambientMode | 0~2 | 앰비언트 모드 | 0~7 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | ambientColor | 3~5 | 앰비언트 색상 | 0~7 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | ambientPattern | 6~7 | 앰비언트 패턴 | 0~3 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
| frmHazardControlMsg | 0x211 | 1 | HazardSwitch | 0 | 비상등 스위치 | 0~1 | BODY_GW -> HAZARD_CTRL 전달 |
|  |  |  | HazardState | 1 | 비상등 상태 | 0~1 | BODY_GW -> HAZARD_CTRL 전달 |
| frmWindowControlMsg | 0x212 | 1 | WindowCommand | 0~1 | 창문 제어 명령 | 0~3 | BODY_GW -> WINDOW_CTRL 전달 |
|  |  |  | WindowState | 2~3 | 창문 상태 | 0~3 | BODY_GW -> WINDOW_CTRL 전달 |
| frmDriverStateMsg | 0x213 | 1 | DriverStateLevel | 0~2 | 운전자 상태 레벨 | 0~7 | BODY_GW -> DRIVER_STATE_CTRL 전달 |
|  |  |  | DriverStateInfo | 3~5 | 운전자 상태 정보 | 0~7 | BODY_GW -> DRIVER_STATE_CTRL 전달 |
| frmDoorStateMsg | 0x214 | 2 | DoorStateMask | 0~7 | 도어 상태 비트맵 | 0~255 | BODY_GW -> WINDOW_CTRL, DRIVER_STATE_CTRL 전달 |
|  |  |  | DoorLockState | 8~9 | 도어 잠금 상태 | 0~3 | BODY_GW -> WINDOW_CTRL, DRIVER_STATE_CTRL 전달 |
|  |  |  | ChildLockState | 10 | 아동 잠금 상태 | 0~1 | BODY_GW -> WINDOW_CTRL, DRIVER_STATE_CTRL 전달 |
|  |  |  | DoorOpenWarn | 11 | 도어 열림 경고 | 0~1 | BODY_GW -> WINDOW_CTRL, DRIVER_STATE_CTRL 전달 |
| frmLampControlMsg | 0x215 | 1 | HeadLampState | 0~1 | 전조등 상태 | 0~3 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | TailLampState | 2~3 | 후미등 상태 | 0~3 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | TurnLampState | 4~5 | 방향지시등 상태 | 0~3 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | HazardLampReq | 6 | 비상등 요청 | 0~1 | BODY_GW -> HAZARD_CTRL 전달 |
| frmWiperStateMsg | 0x216 | 1 | FrontWiperState | 0~1 | 전면 와이퍼 상태 | 0~3 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | RearWiperState | 2~3 | 후면 와이퍼 상태 | 0~3 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
|  |  |  | WiperInterval | 4~7 | 와이퍼 인터벌 | 0~15 | BODY_GW -> BCM_AMBIENT_CTRL 전달 |
| frmSeatBeltStateMsg | 0x217 | 1 | DriverSeatBelt | 0 | 운전석 안전벨트 상태 | 0~1 | DRIVER_STATE_CTRL -> BODY_GW, BCM_AMBIENT_CTRL 전달 |
|  |  |  | PassengerSeatBelt | 1 | 동승석 안전벨트 상태 | 0~1 | DRIVER_STATE_CTRL -> BODY_GW, BCM_AMBIENT_CTRL 전달 |
|  |  |  | RearSeatBelt | 2~3 | 후석 안전벨트 상태 | 0~3 | DRIVER_STATE_CTRL -> BODY_GW, BCM_AMBIENT_CTRL 전달 |
|  |  |  | SeatBeltWarnLvl | 4~5 | 안전벨트 경고 레벨 | 0~3 | DRIVER_STATE_CTRL -> BODY_GW, BCM_AMBIENT_CTRL 전달 |
| frmCabinAirStateMsg | 0x218 | 2 | CabinTemp | 0~7 | 실내 온도 | 0~100 degC | DRIVER_STATE_CTRL -> BODY_GW 전달 |
|  |  |  | AirQualityIndex | 8~15 | 실내 공기질 지수 | 0~255 | DRIVER_STATE_CTRL -> BODY_GW 전달 |
| frmBodyHealthMsg | 0x219 | 2 | BodyAliveCnt | 0~7 | Body Alive Counter | 0~255 | BODY_GW -> SIL_TEST_CTRL 전달 |
|  |  |  | BodyDiagState | 8~11 | Body 진단 상태 | 0~15 | BODY_GW -> SIL_TEST_CTRL 전달 |
|  |  |  | BodyFailCode | 12~15 | Body 오류 코드 | 0~15 | BODY_GW -> SIL_TEST_CTRL 전달 |
| frmClusterWarningMsg | 0x220 | 1 | warningTextCode | 0~7 | 클러스터 경고 코드 | 0~255 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmClusterBaseStateMsg | 0x221 | 2 | ClusterSpeed | 0~7 | 클러스터 표시 속도 | 0~255 km/h | IVI_GW -> CLUSTER_BASE_CTRL 전달 |
|  |  |  | ClusterGear | 8~10 | 클러스터 표시 기어 | 0~7 | IVI_GW -> CLUSTER_BASE_CTRL 전달 |
|  |  |  | ClusterStatus | 11~15 | 클러스터 기본 상태 | 0~31 | IVI_GW -> CLUSTER_BASE_CTRL 전달 |
| frmNaviGuideStateMsg | 0x222 | 1 | GuideLaneState | 0~1 | 유도선 상태 | 0~3 | INFOTAINMENT_GW -> NAV_CONTEXT_MGR 전달 |
|  |  |  | GuideConfidence | 2~7 | 유도 신뢰도 | 0~63 | INFOTAINMENT_GW -> NAV_CONTEXT_MGR 전달 |
| frmMediaStateMsg | 0x223 | 2 | MediaSource | 0~2 | 미디어 소스 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | MediaState | 3~5 | 미디어 재생 상태 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | MuteState | 6 | 음소거 상태 | 0~1 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | VolumeLevel | 8~15 | 볼륨 레벨 | 0~100 % | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmCallStateMsg | 0x224 | 2 | CallState | 0~2 | 통화 상태 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | MicMute | 3 | 마이크 음소거 | 0~1 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | SignalQuality | 4~7 | 통신 품질 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | BtDeviceCount | 8~11 | 블루투스 연결 수 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmNavigationRouteMsg | 0x225 | 3 | RouteClass | 0~1 | 경로 분류 | 0~3 | INFOTAINMENT_GW -> NAV_CONTEXT_MGR 전달 |
|  |  |  | GuideType | 2~3 | 안내 유형 | 0~3 | INFOTAINMENT_GW -> NAV_CONTEXT_MGR 전달 |
|  |  |  | RouteProgress | 8~15 | 경로 진행률 | 0~100 % | INFOTAINMENT_GW -> NAV_CONTEXT_MGR 전달 |
|  |  |  | EtaMinutes | 16~23 | 도착 예상 시간(분) | 0~255 min | INFOTAINMENT_GW -> NAV_CONTEXT_MGR 전달 |
| frmClusterThemeMsg | 0x226 | 1 | ThemeMode | 0~2 | 클러스터 테마 모드 | 0~7 | IVI_GW -> CLUSTER_BASE_CTRL 전달 |
|  |  |  | ClusterBrightness | 3~7 | 클러스터 밝기 | 0~31 | IVI_GW -> CLUSTER_BASE_CTRL 전달 |
| frmHmiPopupStateMsg | 0x227 | 1 | PopupType | 0~3 | 팝업 유형 | 0~15 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | PopupPriority | 4~6 | 팝업 우선순위 | 0~7 | IVI_GW -> CLU_HMI_CTRL 전달 |
|  |  |  | PopupActive | 7 | 팝업 활성 상태 | 0~1 | IVI_GW -> CLU_HMI_CTRL 전달 |
| frmInfotainmentHealthMsg | 0x228 | 2 | InfoAliveCnt | 0~7 | Infotainment Alive Counter | 0~255 | INFOTAINMENT_GW -> SIL_TEST_CTRL 전달 |
|  |  |  | InfoDiagState | 8~11 | Infotainment 진단 상태 | 0~15 | INFOTAINMENT_GW -> SIL_TEST_CTRL 전달 |
|  |  |  | InfoFailCode | 12~15 | Infotainment 오류 코드 | 0~15 | INFOTAINMENT_GW -> SIL_TEST_CTRL 전달 |
| frmTestResultMsg | 0x230 | 1 | scenarioResult | 0 | 시나리오 판정 결과 | 0~1 | SIL_TEST_CTRL -> - 전달 |
| frmBaseTestResultMsg | 0x231 | 2 | BaseScenarioId | 0~7 | 기본 시나리오 ID | 0~255 | VEHICLE_BASE_TEST_CTRL -> SIL_TEST_CTRL 전달 |
|  |  |  | BaseScnResult | 8 | 기본 시나리오 판정 | 0~1 | VEHICLE_BASE_TEST_CTRL -> SIL_TEST_CTRL 전달 |
| frmEmergencyMonitorMsg | 0x232 | 2 | emergencyContext | 0~7 | 긴급 컨텍스트 상태 | 0~255 | EMS_ALERT_RX -> SIL_TEST_CTRL, CHASSIS_GW 전달 |
|  |  |  | TimeoutClearMon | 8 | 타임아웃 모니터 플래그 | 0~1 | EMS_ALERT_RX -> SIL_TEST_CTRL, CHASSIS_GW 전달 |
| frmIgnitionEngineMsg | 0x300 | 1 | IgnitionState | 0 | 시동 입력 상태 | 0~1 | SIL_TEST_CTRL -> ENGINE_CTRL 전달 |
|  |  |  | EngineState | 1~2 | 엔진 동작 상태 | 0~3 | SIL_TEST_CTRL -> ENGINE_CTRL 전달 |
| frmGearStateMsg | 0x301 | 1 | GearInput | 0~2 | 기어 입력값 | 0~7 | SIL_TEST_CTRL -> TRANSMISSION_CTRL 전달 |
|  |  |  | GearState | 3~5 | 기어 상태값 | 0~7 | SIL_TEST_CTRL -> TRANSMISSION_CTRL 전달 |
| frmPowertrainGatewayMsg | 0x302 | 2 | RoutingPolicy | 0~7 | 도메인 라우팅 정책 | 0~255 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | BoundaryStatus | 8~15 | 도메인 경계 상태 | 0~255 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
| frmEngineSpeedTempMsg | 0x303 | 4 | EngineRpm | 0~15 | 엔진 회전수 | 0~65535 rpm | ENGINE_CTRL -> TRANSMISSION_CTRL, DOMAIN_GW_ROUTER 전달 |
|  |  |  | CoolantTemp | 16~23 | 냉각수 온도 | 0~255 degC | ENGINE_CTRL -> TRANSMISSION_CTRL, DOMAIN_GW_ROUTER 전달 |
|  |  |  | OilTemp | 24~31 | 엔진오일 온도 | 0~255 degC | ENGINE_CTRL -> TRANSMISSION_CTRL, DOMAIN_GW_ROUTER 전달 |
| frmFuelBatteryStateMsg | 0x304 | 3 | FuelLevel | 0~7 | 연료 잔량 | 0~100 % | ENGINE_CTRL -> DOMAIN_GW_ROUTER 전달 |
|  |  |  | BatterySoc | 8~15 | 배터리 SOC | 0~100 % | ENGINE_CTRL -> DOMAIN_GW_ROUTER 전달 |
|  |  |  | ChargingState | 16~17 | 충전 상태 | 0~3 | ENGINE_CTRL -> DOMAIN_GW_ROUTER 전달 |
| frmThrottleStateMsg | 0x305 | 2 | ThrottlePos | 0~7 | 스로틀 위치 | 0~100 % | ENGINE_CTRL -> TRANSMISSION_CTRL, DOMAIN_GW_ROUTER 전달 |
|  |  |  | ThrottleReq | 8~15 | 스로틀 요청 | 0~100 % | ENGINE_CTRL -> TRANSMISSION_CTRL, DOMAIN_GW_ROUTER 전달 |
| frmTransmissionTempMsg | 0x306 | 2 | TransOilTemp | 0~7 | 변속기 오일 온도 | 0~255 degC | TRANSMISSION_CTRL -> ENGINE_CTRL, DOMAIN_GW_ROUTER 전달 |
|  |  |  | ClutchTemp | 8~15 | 클러치 온도 | 0~255 degC | TRANSMISSION_CTRL -> ENGINE_CTRL, DOMAIN_GW_ROUTER 전달 |
| frmVehicleModeMsg | 0x307 | 2 | DriveMode | 0~2 | 주행 모드 | 0~7 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | EcoMode | 3 | 에코 모드 | 0~1 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | SportMode | 4 | 스포츠 모드 | 0~1 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | SnowMode | 5 | 스노우 모드 | 0~1 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | PowertrainState | 8~15 | 파워트레인 상태 | 0~255 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
| frmPowerLimitMsg | 0x308 | 2 | TorqueLimit | 0~7 | 토크 제한값 | 0~255 Nm | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | SpeedLimit | 8~15 | 속도 제한값 | 0~255 km/h | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
| frmCruiseStateMsg | 0x309 | 2 | CruiseState | 0~1 | 크루즈 상태 | 0~3 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | GapLevel | 2~3 | 차간 거리 레벨 | 0~3 | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
|  |  |  | CruiseSetSpeed | 8~15 | 크루즈 설정 속도 | 0~255 km/h | DOMAIN_GW_ROUTER -> ENGINE_CTRL, TRANSMISSION_CTRL 전달 |
| frmPowertrainHealthMsg | 0x30A | 2 | PtAliveCnt | 0~7 | Powertrain Alive Counter | 0~255 | DOMAIN_GW_ROUTER -> SIL_TEST_CTRL 전달 |
|  |  |  | PtDiagState | 8~11 | Powertrain 진단 상태 | 0~15 | DOMAIN_GW_ROUTER -> SIL_TEST_CTRL 전달 |
|  |  |  | PtFailCode | 12~15 | Powertrain 오류 코드 | 0~15 | DOMAIN_GW_ROUTER -> SIL_TEST_CTRL 전달 |
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0~7 | 차량 속도 | 0~255 km/h | CHASSIS_GW -> ADAS_WARN_CTRL 전달 (UDP) |
|  |  |  | driveState | 8~9 | 주행 상태(PRND) | 0~3 | CHASSIS_GW -> ADAS_WARN_CTRL 전달 (UDP) |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 조향 입력 여부 | 0~1 | CHASSIS_GW -> ADAS_WARN_CTRL 전달 (UDP) |
| ethNavContextMsg | 0x512 | 3 | roadZone | 0~1 | 구간 타입 | 0~3 | INFOTAINMENT_GW -> NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
|  |  |  | navDirection | 2~3 | 유도 방향 | 0~3 | INFOTAINMENT_GW -> NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
|  |  |  | zoneDistance | 8~15 | 구간 잔여 거리 | 0~255 m | INFOTAINMENT_GW -> NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
|  |  |  | speedLimit | 16~23 | 구간 제한속도 | 0~255 km/h | INFOTAINMENT_GW -> NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR 전달 (UDP) |
| ETH_EmergencyAlert | 0xE100 | 4 | emergencyType | 0~1 | 긴급차량 종류 | 0~3 | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX 전달 (UDP) |
|  |  |  | emergencyDirection | 2~3 | 긴급차량 접근 방향 | 0~3 | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX 전달 (UDP) |
|  |  |  | eta | 8~15 | 도달 예상시간 | 0~255 s | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX 전달 (UDP) |
|  |  |  | sourceId | 16~23 | 송신 주체 ID | 0~255 | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX 전달 (UDP) |
|  |  |  | alertState | 24 | 긴급 상태 | 0~1 | EMS_POLICE_TX + EMS_AMB_TX -> EMS_ALERT_RX 전달 (UDP) |
| ethSelectedAlertMsg | 0xE200 | 2 | selectedAlertLevel | 0~2 | 최종 경고 레벨 | 0~7 | WARN_ARB_MGR -> BODY_GW, IVI_GW 전달 (UDP) |
|  |  |  | selectedAlertType | 3~5 | 최종 경고 타입 | 0~7 | WARN_ARB_MGR -> BODY_GW, IVI_GW 전달 (UDP) |
|  |  |  | timeoutClear | 8 | 타임아웃 해제 플래그 | 0~1 | WARN_ARB_MGR -> BODY_GW, IVI_GW 전달 (UDP) |
---

## 하단 보강표 (감사/추적 전용)

- 상단 공식 표준 양식은 변경하지 않고 유지한다.
- 아래 표들은 추적성/감사 해석 명확화를 위한 하단 보강 정보다.

---

## 통신 원본(Source of Truth) 매핑

| 구분 | 범위 | 원본 파일 | 비고 |
|---|---|---|---|
| Core CAN Profile | Comm_001, Comm_002, Comm_003, Comm_007, Comm_008, Comm_009 | `canoe/network/dbc/emergency_system.dbc` | 경고 코어 체인 단일 원본 |
| Domain CAN Profile | Comm_101~Comm_106 | `canoe/network/dbc/emergency_system_chassis.dbc` + `canoe/network/dbc/emergency_system_powertrain.dbc` + `canoe/network/dbc/emergency_system_body.dbc` + `canoe/network/dbc/emergency_system_infotainment.dbc` | 차량 기본 기능/도메인 분리 원본 |
| Ethernet Profile | Comm_004, Comm_005, Comm_006 (및 Comm_001~003/007~008의 ETH 구간) | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | DBC 비대상, UDP 계약 단일 원본 |

---

## 통신 상세 추적 표 (Comm/Flow/Func/Req)

| Comm ID | Flow ID | Func ID | Req ID | Message(ID) | Tx Node | Rx Node | Protocol | Period | Clear/비고 |
|---|---|---|---|---|---|---|---|---|---|
| Comm_001 | Flow_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x100), ethVehicleStateMsg(0x510) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 |
| Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x101), ethSteeringMsg(0x511) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 |
| Comm_003 | Flow_003 | Func_007, Func_010 | Req_007, Req_010 | frmNavContextCanMsg(0x110), ethNavContextMsg(0x512) | SIL_TEST_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리/제한속도 입력 갱신 |
| Comm_004 | Flow_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_POLICE_TX | EMS_ALERT_RX | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_005 | Flow_005 | Func_018 | Req_018 | ETH_EmergencyAlert(0xE100) | EMS_AMB_TX | EMS_ALERT_RX | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_006 | Flow_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT_RX, WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | 1000ms 무갱신 시 timeoutClear=1 |
| Comm_007 | Flow_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_036, Req_037, Req_038, Req_039 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x210) | WARN_ARB_MGR, BODY_GW | BODY_GW, BCM_AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_008 | Flow_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x220) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_009 | Flow_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x230) | SIL_TEST_CTRL | SIL_TEST_CTRL(Log/Panel) | CAN | Event | 판정 결과 기록 완료 시 종료 |

---

## Comm_006 메시지 단계 분해 (감사용 명확화)

| 단계 | 상위 Comm ID | Message(ID) | Tx Node | Rx Node | 주기/조건 |
|---|---|---|---|---|---|
| Ingress | Comm_006 | ETH_EmergencyAlert(0xE100) | EMS_POLICE_TX, EMS_AMB_TX | EMS_ALERT_RX | 100ms, Active/Clear |
| Egress | Comm_006 | ethSelectedAlertMsg(0xE200) | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms |

- 주의: `Comm_006`은 입력(E100)과 출력(E200) 단계를 묶은 논리 Comm이며, 감사 시에는 위 단계 표를 기준으로 `Rx/Tx`를 분리 해석한다.

### 표준 Signal-별칭(g*) 매핑 (문서/코드 정합용)

| 표준 Signal(0303/0304) | 코드/런타임 별칭 |
|---|---|
| vehicleSpeed | gVehicleSpeed |
| driveState | gDriveState |
| steeringInput | SteeringInput |
| roadZone | gRoadZone |
| navDirection | gNavDirection |
| zoneDistance | gZoneDistance |
| speedLimit | gSpeedLimit |

---

## 도메인별 통신 원본 확장 정의 (DBC 병렬 작업 기준)

| Domain | 원본 파일(정의) | Comm 범위 | 핵심 Message |
|---|---|---|---|
| Core Integration CAN | `canoe/network/dbc/emergency_system.dbc` | Comm_001, Comm_002, Comm_003, Comm_007, Comm_008, Comm_009 | frmVehicleStateCanMsg, frmSteeringCanMsg, frmNavContextCanMsg, frmAmbientControlMsg, frmClusterWarningMsg, frmTestResultMsg |
| Chassis CAN | `canoe/network/dbc/emergency_system_chassis.dbc` | Comm_001, Comm_002, Comm_102, Comm_106, Comm_105(헬스) | frmVehicleStateCanMsg, frmSteeringCanMsg, frmPedalInputCanMsg, frmBrakeStatusMsg, frmAccelStatusMsg, frmSteeringTorqueMsg, frmBaseTestResultMsg, frmEmergencyMonitorMsg |
| Powertrain CAN | `canoe/network/dbc/emergency_system_powertrain.dbc` | Comm_101, Comm_105 | frmIgnitionEngineMsg, frmGearStateMsg, frmPowertrainGatewayMsg, frmEngineSpeedTempMsg, frmPowerLimitMsg, frmCruiseStateMsg |
| Body CAN | `canoe/network/dbc/emergency_system_body.dbc` | Comm_007, Comm_103, Comm_105 | frmAmbientControlMsg, frmHazardControlMsg, frmWindowControlMsg, frmDriverStateMsg, frmBodyHealthMsg |
| Infotainment CAN | `canoe/network/dbc/emergency_system_infotainment.dbc` | Comm_003, Comm_008, Comm_104, Comm_105 | frmNavContextCanMsg, frmClusterWarningMsg, frmClusterBaseStateMsg, frmClusterThemeMsg, frmHmiPopupStateMsg, frmInfotainmentHealthMsg |
| Ethernet UDP | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | Comm_004, Comm_005, Comm_006 | ethVehicleStateMsg, ethSteeringMsg, ethNavContextMsg, ETH_EmergencyAlert, ethSelectedAlertMsg |

---

## Vehicle Baseline 확장 Comm 정의 (Comm_101~Comm_106)

| Comm ID | Flow ID(0302 연계) | Func ID | Req ID | Message(ID) | Protocol | 주기 |
|---|---|---|---|---|---|---|
| Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | frmIgnitionEngineMsg(0x300), frmGearStateMsg(0x301), frmEngineSpeedTempMsg(0x303), frmTransmissionTempMsg(0x306) | CAN(Powertrain) | 100ms |
| Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | frmPedalInputCanMsg(0x102), frmSteeringStateCanMsg(0x103), frmBrakeStatusMsg(0x106), frmAccelStatusMsg(0x107), frmSteeringTorqueMsg(0x108) | CAN(Chassis) | 100ms |
| Comm_103 | Flow_103 | Func_106, Func_107, Func_108 | Req_106, Req_107, Req_108 | frmHazardControlMsg(0x211), frmWindowControlMsg(0x212), frmDriverStateMsg(0x213), frmSeatBeltStateMsg(0x217), frmCabinAirStateMsg(0x218) | CAN(Body) | 100ms |
| Comm_104 | Flow_104 | Func_109 | Req_109 | frmClusterBaseStateMsg(0x221), frmClusterThemeMsg(0x226), frmHmiPopupStateMsg(0x227) | CAN(Infotainment) | 50ms |
| Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | frmPowertrainGatewayMsg(0x302), frmVehicleModeMsg(0x307), frmPowerLimitMsg(0x308), frmCruiseStateMsg(0x309), frmChassisHealthMsg(0x109), frmBodyHealthMsg(0x219), frmInfotainmentHealthMsg(0x228) | CAN(도메인 경계/라우팅) | 100ms |
| Comm_106 | Flow_106 | Func_112 | Req_112 | frmBaseTestResultMsg(0x231), frmTestResultMsg(0x230) | CAN(Test) | Event |

- 주의: `Comm_101~Comm_106`은 현재 도메인 분리 DBC에서 정의된 실제 메시지 ID를 기준으로 고정하며, 도메인 간 이더넷 라우팅 구현은 04/코드 단계에서 추가 상세화한다.

---

## 메시지 규모 기준 (현업 BP 타깃)

| Domain/Profile | 현재 정의 메시지 수 | 현재 사용 ID 범위 | 확장 목표(Phase-B) |
|---|---|---|---|
| Core Integration CAN | 6 | 0x100/0x101/0x110/0x210/0x220/0x230 | 코어 유지(변경 최소화) |
| Chassis CAN | 13 | 0x100~0x109, 0x230~0x232 | 20~30 |
| Powertrain CAN | 11 | 0x300~0x30A | 15~25 |
| Body CAN | 10 | 0x210~0x219 | 15~25 |
| Infotainment CAN | 10 | 0x110, 0x220~0x228 | 20~30 |
| Ethernet UDP | 5 타입 | 0x510/0x511/0x512/0xE100/0xE200 | 8~12 타입 |

- 통합 목표: CAN 메시지 `80~120`, Ethernet 메시지 타입 `8~12`, 전체 통신 항목 `100+`.

---

## 0302/0304 연계 체크포인트

- `Comm ID`는 `0302_NWflowDef.md`의 `Flow ID`와 1:1 연결한다.
- `Comm_001~Comm_009`는 `0304_System_Variables.md`의 기존 Var 표와 즉시 연결되어야 하며, `Comm_101~Comm_106`는 0304 확장 개정 시 동일 규칙으로 추가 연결한다.
- `EmergencyAlert` Active/Clear 신호가 1000ms 타임아웃 규칙과 일치해야 한다.
- `selectedAlertLevel/selectedAlertType` 기반 Ambient/Cluster 출력 Comm이 모두 존재해야 한다.
- `ETH_SWITCH` 경유 Ethernet 신호가 각 도메인 게이트웨이에서 CAN 메시지로 정상 변환되어야 한다.
- `speedLimit` 신호는 Comm_003에서 NAV_CONTEXT_MGR와 ADAS_WARN_CTRL까지 연계되어야 한다.
- `Req_101~Req_112`는 Comm_101~Comm_106에서 누락 없이 연결되어야 한다.

---

## 통신 예외 처리 규칙

| Comm Group | 예외 조건 | Fail-safe 동작 | 검증 포인트 |
|---|---|---|---|
| Group_A(Comm_001,002) | CHASSIS_GW 변환 프레임 누락(연속 2주기) | ADAS_WARN_CTRL 입력 품질 플래그 저하, 경고 강등 모드 진입 | CAN 입력 정상 + ETH 변환 누락 시 동작 확인 |
| Group_B(Comm_003) | INFOTAINMENT_GW 변환 프레임 누락(연속 2주기) | NAV_CONTEXT_MGR를 일반구간 기본 컨텍스트로 복귀 | 유도구간 상태에서 변환 누락 주입 |
| Group_C(Comm_004~006) | EmergencyAlert 1000ms 무갱신 | `timeoutClear=1`, emergencyContext clear, 출력 복귀 | Req_024 타임아웃 검증 |
| Group_D(Comm_007) | BODY_GW CAN 송신 ACK 실패 | ambientMode를 안전 기본값(0)으로 전환 후 재전송 | CAN Tx fail 주입 테스트 |
| Group_E(Comm_008) | IVI_GW CAN 송신 ACK 실패 | warningTextCode를 최소 안내 코드로 축소 후 재전송 | Cluster 경고 축소 출력 확인 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 최신 프로젝트 스코프 반영 전면 재작성. Comm_001~Comm_009 및 Flow/Func/Req 1:1 추적 구조 반영, OTA/UDS/DoIP 제거 |
| 2.1 | 2026-02-25 | 공식 샘플 표기 스타일(Identifier/DLC 순수값)로 상단 표 정렬, Ethernet 백본+도메인 게이트웨이+CAN 분배 구조 반영 |
| 2.2 | 2026-02-25 | 상단 공식표 signal bit position을 개별 비트 행으로 전개하고 Comm별 통신 예외 처리 규칙 추가 |
| 2.3 | 2026-02-25 | navDirection 범위를 0304 변수 정의(0~3)와 정합되게 통일하고 ScenarioResult bit 행(0 단일 bit) 표기를 일치화 |
| 2.4 | 2026-02-26 | Cluster 경고 경로를 Infotainment CAN 기준으로 명확화(IVI_GW -> CLU_HMI_CTRL) |
| 2.5 | 2026-02-26 | Comm_006 단계 분해 표(E100 Ingress / E200 Egress) 추가로 감사 해석 모호성 제거 |
| 2.6 | 2026-02-26 | 상단 공식표 비변경 원칙을 명시하고 하단 보강표 구역(감사/추적 전용)으로 분리 |
| 2.7 | 2026-02-26 | 상단 Signal 명칭을 0304 표준명(vehicleSpeed 등)으로 통일하고, g* 별칭은 하단 매핑표로 분리 |
| 2.8 | 2026-02-28 | signal 케이스/명칭을 0304 표준명(`steeringInput/emergencyType/eta/sourceId` 등)으로 정합하고 `SelectedAlertContext` 잔여 표현 제거 |
| 2.9 | 2026-02-28 | Nav 컨텍스트 메시지(0x110/0x512)에 `speedLimit`(bit16, DLC=3)를 추가하고 Comm_003을 Req_010/Func_010까지 확장 정합. |
| 3.0 | 2026-02-28 | CAN/Ethernet 통신 원본 파일 분리 원칙을 명시하고 SoT 매핑 표를 추가(`emergency_system.dbc` / `ETH_INTERFACE_CONTRACT.md`). |
| 3.1 | 2026-02-28 | DBC 병렬 작업용 도메인 통신 원본 확장 계획과 Vehicle Baseline Comm 계획(Comm_101~106, 예약 ID)을 추가. |
| 3.2 | 2026-02-28 | Comm_101~106을 확정 정의로 전환하고 도메인별 메시지 규모 기준(총 CAN 80~120, 전체 100+)을 명시. |
| 3.3 | 2026-02-28 | 도메인 분리 DBC(`emergency_system_*`) 실 메시지(0x300~0x30A, 0x102~0x109, 0x211~0x228, 0x231~0x232)를 Comm_101~106에 반영하고 SoT 계층 매핑을 보강. |
| 3.4 | 2026-02-28 | 상단 공식표를 실메시지 기준(49 Message / 131 Signal)으로 확장하고 signal bit position을 범위 표기(`0~7`, `8~15`)로 정규화. |

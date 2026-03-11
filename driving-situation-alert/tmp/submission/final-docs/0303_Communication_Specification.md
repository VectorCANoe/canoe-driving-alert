# 통신 명세서 (Communication Specification)

**Document ID**: PROJ-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 (Software Architectural Design)
**Version**: 3.35
**Date**: 2026-03-09
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2) | `0303_Communication_Specification.md` | `0302_NWflowDef.md` | `0304_System_Variables.md` |

---

## 통신 명세 표 (공식 표준 양식)

| Message | Identifier | DLC | Signal | signal bit position | Data 설명 | Data 범위 | Data 사용 |
|---|---|---|---|---|---|---|---|
| frmVehicleStateCanMsg | 0x2A0 | 2 | vehicleSpeed | 0~7 | 차량 속도 | 0~255 km/h | Validation Harness에서 CGW에 전달 |
|  |  |  | driveState | 8~9 | 주행 상태(PRND) | 0~3 | Validation Harness에서 CGW에 전달 |
| frmSteeringCanMsg | 0x2A1 | 1 | steeringInput | 0 | 조향 입력 여부 | 0~1 | Validation Harness에서 CGW에 전달 |
| frmPedalInputCanMsg | 0x2A2 | 2 | AccelPedal | 0~7 | 가속 페달 입력 | 0~100 % | Validation Harness에서 VCU에 전달 |
|  |  |  | BrakePedal | 8~15 | 브레이크 페달 입력 | 0~100 % | Validation Harness에서 ESC에 전달 |
| frmSteeringStateCanMsg | 0x100 | 1 | SteeringState | 0~1 | 조향 상태 | 0~3 | CGW에서 MDPS에 전달 |
| frmWheelSpeedMsg | 0x101 | 4 | WheelSpdFL | 0~7 | 전륜 좌 휠속도 | 0~255 km/h | CGW에서 VCU, ESC, MDPS에 전달 |
|  |  |  | WheelSpdFR | 8~15 | 전륜 우 휠속도 | 0~255 km/h | CGW에서 VCU, ESC, MDPS에 전달 |
|  |  |  | WheelSpdRL | 16~23 | 후륜 좌 휠속도 | 0~255 km/h | CGW에서 VCU, ESC, MDPS에 전달 |
|  |  |  | WheelSpdRR | 24~31 | 후륜 우 휠속도 | 0~255 km/h | CGW에서 VCU, ESC, MDPS에 전달 |
| frmYawAccelMsg | 0x102 | 4 | YawRate | 0~15 | 요레이트 | 0~65535 deg/s | CGW에서 ESC, MDPS에 전달 |
|  |  |  | LatAccel | 16~31 | 횡가속도 | 0~65535 0.01m/s2 | CGW에서 ESC, MDPS에 전달 |
| frmBrakeStatusMsg | 0x120 | 2 | BrakePressure | 0~7 | 브레이크 압력 | 0~255 % | ESC에서 CGW에 전달 |
|  |  |  | BrakeMode | 8~9 | 브레이크 동작 모드 | 0~3 | ESC에서 CGW에 전달 |
|  |  |  | AbsActive | 10 | ABS 활성 상태 | 0~1 | ESC에서 CGW에 전달 |
|  |  |  | EspActive | 11 | ESC 활성 상태 | 0~1 | ESC에서 CGW에 전달 |
| frmAccelStatusMsg | 0x121 | 2 | AccelRequest | 0~7 | 가속 요청 | 0~100 % | VCU에서 CGW에 전달 |
|  |  |  | TorqueRequest | 8~15 | 토크 요청 | 0~255 Nm | VCU에서 CGW에 전달 |
| frmSteeringTorqueMsg | 0x122 | 2 | SteeringTorque | 0~11 | 조향 토크 | 0~4095 0.1Nm | MDPS에서 CGW에 전달 |
|  |  |  | SteeringAssistLv | 12~15 | 조향 보조 레벨 | 0~15 | MDPS에서 CGW에 전달 |
| frmChassisHealthMsg | 0x103 | 2 | ChassisAliveCnt | 0~7 | Chassis Alive Counter | 0~255 | CGW에서 Validation Harness에 전달 |
|  |  |  | ChassisDiagState | 8~11 | Chassis 진단 상태 | 0~15 | CGW에서 Validation Harness에 전달 |
|  |  |  | ChassisFailCode | 12~15 | Chassis 오류 코드 | 0~15 | CGW에서 Validation Harness에 전달 |
| frmNavContextCanMsg | 0x2A3 | 3 | roadZone | 0~1 | 구간 타입 | 0~3 | Validation Harness에서 IVI에 전달 |
|  |  |  | navDirection | 2~3 | 유도 방향 | 0~3 | Validation Harness에서 IVI에 전달 |
|  |  |  | zoneDistance | 8~15 | 구간 잔여 거리 | 0~255 m | Validation Harness에서 IVI에 전달 |
|  |  |  | speedLimit | 16~23 | 구간 제한속도 | 0~255 km/h | Validation Harness에서 IVI에 전달 |
| frmAmbientControlMsg | 0x260 | 1 | ambientMode | 0~2 | 앰비언트 모드 | 0~7 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | ambientColor | 3~5 | 앰비언트 색상 | 0~7 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | ambientPattern | 6~7 | 앰비언트 패턴 | 0~3 | BCM에서 앰비언트 제어에 전달 |
| frmHazardControlMsg | 0x261 | 1 | HazardSwitch | 0 | 비상등 스위치 | 0~1 | BCM에서 비상등 제어에 전달 |
|  |  |  | HazardState | 1 | 비상등 상태 | 0~1 | BCM에서 비상등 제어에 전달 |
| frmWindowControlMsg | 0x262 | 1 | WindowCommand | 0~1 | 창문 제어 명령 | 0~3 | BCM에서 창문 제어에 전달 |
|  |  |  | WindowState | 2~3 | 창문 상태 | 0~3 | BCM에서 창문 제어에 전달 |
| frmDoorStateMsg | 0x264 | 2 | DoorStateMask | 0~7 | 도어 상태 비트맵 | 0~255 | BCM에서 창문 제어와 차체 상태 관리에 전달 |
|  |  |  | DoorLockState | 8~9 | 도어 잠금 상태 | 0~3 | BCM에서 창문 제어와 차체 상태 관리에 전달 |
|  |  |  | ChildLockState | 10 | 아동 잠금 상태 | 0~1 | BCM에서 창문 제어와 차체 상태 관리에 전달 |
|  |  |  | DoorOpenWarn | 11 | 도어 열림 경고 | 0~1 | BCM에서 창문 제어와 차체 상태 관리에 전달 |
| frmLampControlMsg | 0x265 | 1 | HeadLampState | 0~1 | 전조등 상태 | 0~3 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | TailLampState | 2~3 | 후미등 상태 | 0~3 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | TurnLampState | 4~5 | 방향지시등 상태 | 0~3 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | HazardLampReq | 6 | 비상등 요청 | 0~1 | BCM에서 비상등 제어에 전달 |
| frmWiperStateMsg | 0x266 | 1 | FrontWiperState | 0~1 | 전면 와이퍼 상태 | 0~3 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | RearWiperState | 2~3 | 후면 와이퍼 상태 | 0~3 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | WiperInterval | 4~7 | 와이퍼 인터벌 | 0~15 | BCM에서 앰비언트 제어에 전달 |
| frmSeatBeltStateMsg | 0x267 | 1 | DriverSeatBelt | 0 | 운전석 안전벨트 상태 | 0~1 | BCM에서 차체 상태 판단과 앰비언트 제어에 사용 |
|  |  |  | PassengerSeatBelt | 1 | 동승석 안전벨트 상태 | 0~1 | BCM에서 차체 상태 판단과 앰비언트 제어에 사용 |
|  |  |  | RearSeatBelt | 2~3 | 후석 안전벨트 상태 | 0~3 | BCM에서 차체 상태 판단과 앰비언트 제어에 사용 |
|  |  |  | SeatBeltWarnLvl | 4~5 | 안전벨트 경고 레벨 | 0~3 | BCM에서 차체 상태 판단과 앰비언트 제어에 사용 |
| frmCabinAirStateMsg | 0x268 | 2 | CabinTemp | 0~7 | 실내 온도 | 0~100 degC | BCM에서 차체 상태 판단에 사용 |
|  |  |  | AirQualityIndex | 8~15 | 실내 공기질 지수 | 0~255 | BCM에서 차체 상태 판단에 사용 |
| frmBodyHealthMsg | 0x269 | 2 | BodyAliveCnt | 0~7 | Body Alive Counter | 0~255 | BCM에서 Validation Harness에 전달 |
|  |  |  | BodyDiagState | 8~11 | Body 진단 상태 | 0~15 | BCM에서 Validation Harness에 전달 |
|  |  |  | BodyFailCode | 12~15 | Body 오류 코드 | 0~15 | BCM에서 Validation Harness에 전달 |
| frmClusterWarningMsg | 0x280 | 1 | warningTextCode | 0~7 | 클러스터 경고 코드 | 0~255 | IVI에서 CLU에 전달 |
| frmClusterBaseStateMsg | 0x281 | 2 | ClusterSpeed | 0~7 | 클러스터 표시 속도 | 0~255 km/h | IVI에서 클러스터 기본 표시에 사용 |
|  |  |  | ClusterGear | 8~10 | 클러스터 표시 기어 | 0~7 | IVI에서 클러스터 기본 표시에 사용 |
|  |  |  | ClusterStatus | 11~15 | 클러스터 기본 상태 | 0~31 | IVI에서 클러스터 기본 표시에 사용 |
| frmNaviGuideStateMsg | 0x282 | 1 | GuideLaneState | 0~1 | 유도선 상태 | 0~3 | IVI에서 구간 안내 판단에 사용 |
|  |  |  | GuideConfidence | 2~7 | 유도 신뢰도 | 0~63 | IVI에서 구간 안내 판단에 사용 |
| frmMediaStateMsg | 0x283 | 2 | MediaSource | 0~2 | 미디어 소스 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | MediaState | 3~5 | 미디어 재생 상태 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | MuteState | 6 | 음소거 상태 | 0~1 | IVI에서 CLU에 전달 |
|  |  |  | VolumeLevel | 8~15 | 볼륨 레벨 | 0~100 % | IVI에서 CLU에 전달 |
| frmCallStateMsg | 0x284 | 2 | CallState | 0~2 | 통화 상태 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | MicMute | 3 | 마이크 음소거 | 0~1 | IVI에서 CLU에 전달 |
|  |  |  | SignalQuality | 4~7 | 통신 품질 | 0~15 | IVI에서 CLU에 전달 |
|  |  |  | BtDeviceCount | 8~11 | 블루투스 연결 수 | 0~15 | IVI에서 CLU에 전달 |
| frmNavigationRouteMsg | 0x285 | 3 | RouteClass | 0~1 | 경로 분류 | 0~3 | IVI에서 구간 안내 판단에 사용 |
|  |  |  | GuideType | 2~3 | 안내 유형 | 0~3 | IVI에서 구간 안내 판단에 사용 |
|  |  |  | RouteProgress | 8~15 | 경로 진행률 | 0~100 % | IVI에서 구간 안내 판단에 사용 |
|  |  |  | EtaMinutes | 16~23 | 도착 예상 시간(분) | 0~255 min | IVI에서 구간 안내 판단에 사용 |
| frmClusterThemeMsg | 0x286 | 1 | ThemeMode | 0~2 | 클러스터 테마 모드 | 0~7 | IVI에서 클러스터 기본 표시에 사용 |
|  |  |  | ClusterBrightness | 3~7 | 클러스터 밝기 | 0~31 | IVI에서 클러스터 기본 표시에 사용 |
| frmHmiPopupStateMsg | 0x287 | 1 | PopupType | 0~3 | 팝업 유형 | 0~15 | IVI에서 CLU에 전달 |
|  |  |  | PopupPriority | 4~6 | 팝업 우선순위 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | PopupActive | 7 | 팝업 활성 상태 | 0~1 | IVI에서 CLU에 전달 |
| frmInfotainmentHealthMsg | 0x288 | 2 | InfoAliveCnt | 0~7 | Infotainment Alive Counter | 0~255 | IVI에서 Validation Harness에 전달 |
|  |  |  | InfoDiagState | 8~11 | Infotainment 진단 상태 | 0~15 | IVI에서 Validation Harness에 전달 |
|  |  |  | InfoFailCode | 12~15 | Infotainment 오류 코드 | 0~15 | IVI에서 Validation Harness에 전달 |
| frmTestResultMsg | 0x2A5 | 1 | scenarioResult | 0 | 시나리오 판정 결과 | 0~1 | Validation Harness에서 시나리오 결과 확인에 사용 |
| frmBaseTestResultMsg | 0x2A6 | 8 | BaseScenarioId | 0~7 | 기본 시나리오 ID | 0~255 | Validation Harness에서 기본 시나리오 판정에 사용 |
|  |  |  | BaseScenarioResult | 8 | 기본 시나리오 판정 | 0~1 | Validation Harness에서 기본 시나리오 판정에 사용 |
| frmEmergencyBroadcastMsg | 0x1C0 | 4 | emergencyType | 0~3 | 긴급차량 타입 | 0~15 | V2X에서 긴급 알림 수신 경로로 전달 |
|  |  |  | Status | 4~5 | 긴급 상태 | 0~3 | V2X에서 긴급 알림 수신 경로로 전달 |
|  |  |  | SourceId | 8~15 | 긴급 송신 주체 ID | 0~255 | V2X에서 긴급 알림 수신 경로로 전달 |
|  |  |  | EtaSeconds | 16~23 | 도달 예상 시간 | 0~255 s | V2X에서 긴급 알림 수신 경로로 전달 |
|  |  |  | emergencyDirection | 24~27 | 접근 방향 | 0~15 | V2X에서 긴급 알림 수신 경로로 전달 |
| frmEmergencyMonitorMsg | 0x1C2 | 2 | emergencyContext | 0~7 | 긴급 컨텍스트 상태 | 0~255 | V2X에서 ETHB 상태 모니터링 경로로 전달 |
|  |  |  | TimeoutClearMon | 8 | 타임아웃 모니터 플래그 | 0~1 | V2X에서 ETHB 상태 모니터링 경로로 전달 |
| frmIgnitionEngineMsg | 0x2A8 | 1 | IgnitionState | 0 | 시동 입력 상태 | 0~1 | Validation Harness에서 EMS에 전달 |
|  |  |  | EngineState | 1~2 | 엔진 동작 상태 | 0~3 | Validation Harness에서 EMS에 전달 |
| frmGearStateMsg | 0x2A9 | 1 | GearInput | 0~2 | 기어 입력값 | 0~7 | Validation Harness에서 TCU에 전달 |
|  |  |  | GearState | 3~5 | 기어 상태값 | 0~7 | Validation Harness에서 TCU에 전달 |
| frmPowertrainGatewayMsg | 0x109 | 2 | RoutingPolicy | 0~7 | 도메인 라우팅 정책 | 0~255 | CGW에서 EMS, TCU에 전달 |
|  |  |  | BoundaryStatus | 8~15 | 도메인 경계 상태 | 0~255 | CGW에서 EMS, TCU에 전달 |
| frmEngineSpeedTempMsg | 0x12A | 4 | EngineRpm | 0~15 | 엔진 회전수 | 0~65535 rpm | EMS에서 TCU, CGW에 전달 |
|  |  |  | CoolantTemp | 16~23 | 냉각수 온도 | 0~255 degC | EMS에서 TCU, CGW에 전달 |
|  |  |  | OilTemp | 24~31 | 엔진오일 온도 | 0~255 degC | EMS에서 TCU, CGW에 전달 |
| frmFuelBatteryStateMsg | 0x12B | 3 | FuelLevel | 0~7 | 연료 잔량 | 0~100 % | EMS에서 CGW에 전달 |
|  |  |  | BatterySoc | 8~15 | 배터리 SOC | 0~100 % | EMS에서 CGW에 전달 |
|  |  |  | ChargingState | 16~17 | 충전 상태 | 0~3 | EMS에서 CGW에 전달 |
| frmThrottleStateMsg | 0x12C | 2 | ThrottlePos | 0~7 | 스로틀 위치 | 0~100 % | EMS에서 TCU, CGW에 전달 |
|  |  |  | ThrottleReq | 8~15 | 스로틀 요청 | 0~100 % | EMS에서 TCU, CGW에 전달 |
| frmTransmissionTempMsg | 0x12D | 2 | TransOilTemp | 0~7 | 변속기 오일 온도 | 0~255 degC | TCU에서 EMS, CGW에 전달 |
|  |  |  | ClutchTemp | 8~15 | 클러치 온도 | 0~255 degC | TCU에서 EMS, CGW에 전달 |
| frmVehicleModeMsg | 0x10A | 2 | DriveMode | 0~2 | 주행 모드 | 0~7 | CGW에서 EMS, TCU에 전달 |
|  |  |  | EcoMode | 3 | 에코 모드 | 0~1 | CGW에서 EMS, TCU에 전달 |
|  |  |  | SportMode | 4 | 스포츠 모드 | 0~1 | CGW에서 EMS, TCU에 전달 |
|  |  |  | SnowMode | 5 | 스노우 모드 | 0~1 | CGW에서 EMS, TCU에 전달 |
|  |  |  | PowertrainState | 8~15 | 파워트레인 상태 | 0~255 | CGW에서 EMS, TCU에 전달 |
| frmPowerLimitMsg | 0x10B | 2 | TorqueLimit | 0~7 | 토크 제한값 | 0~255 Nm | CGW에서 EMS, TCU에 전달 |
|  |  |  | SpeedLimit | 8~15 | 속도 제한값 | 0~255 km/h | CGW에서 EMS, TCU에 전달 |
| frmCruiseStateMsg | 0x10C | 2 | CruiseState | 0~1 | 크루즈 상태 | 0~3 | CGW에서 EMS, TCU에 전달 |
|  |  |  | GapLevel | 2~3 | 차간 거리 레벨 | 0~3 | CGW에서 EMS, TCU에 전달 |
|  |  |  | CruiseSetSpeed | 8~15 | 크루즈 설정 속도 | 0~255 km/h | CGW에서 EMS, TCU에 전달 |
| frmPowertrainHealthMsg | 0x10D | 2 | PtAliveCnt | 0~7 | Powertrain Alive Counter | 0~255 | CGW에서 Validation Harness에 전달 |
|  |  |  | PtDiagState | 8~11 | Powertrain 진단 상태 | 0~15 | CGW에서 Validation Harness에 전달 |
|  |  |  | PtFailCode | 12~15 | Powertrain 오류 코드 | 0~15 | CGW에서 Validation Harness에 전달 |
| ethVehicleStateMsg | 0x510 | 2 | vehicleSpeed | 0~7 | 차량 속도 | 0~255 km/h | CGW에서 ADAS에 전달 (UDP) |
|  |  |  | driveState | 8~9 | 주행 상태(PRND) | 0~3 | CGW에서 ADAS에 전달 (UDP) |
| ethSteeringMsg | 0x511 | 1 | steeringInput | 0 | 조향 입력 여부 | 0~1 | CGW에서 ADAS에 전달 (UDP) |
| ethNavContextMsg | 0x512 | 3 | roadZone | 0~1 | 구간 타입 | 0~3 | IVI에서 구간 판단과 경고 중재에 전달 (UDP) |
|  |  |  | navDirection | 2~3 | 유도 방향 | 0~3 | IVI에서 구간 판단과 경고 중재에 전달 (UDP) |
|  |  |  | zoneDistance | 8~15 | 구간 잔여 거리 | 0~255 m | IVI에서 구간 판단과 경고 중재에 전달 (UDP) |
|  |  |  | speedLimit | 16~23 | 구간 제한속도 | 0~255 km/h | IVI에서 구간 판단과 경고 중재에 전달 (UDP) |
| frmEmergencyBroadcastMsg | 0xE100 | 4 | emergencyType | 0~1 | 긴급차량 종류 | 0~3 | V2X 긴급 알림 송신 기능에서 V2X 긴급 알림 수신 기능에 전달 (UDP) |
|  |  |  | emergencyDirection | 2~3 | 긴급차량 접근 방향 | 0~3 | V2X 긴급 알림 송신 기능에서 V2X 긴급 알림 수신 기능에 전달 (UDP) |
|  |  |  | EtaSeconds | 8~15 | 도달 예상시간 | 0~255 s | V2X 긴급 알림 송신 기능에서 V2X 긴급 알림 수신 기능에 전달 (UDP) |
|  |  |  | SourceId | 16~23 | 송신 주체 ID | 0~255 | V2X 긴급 알림 송신 기능에서 V2X 긴급 알림 수신 기능에 전달 (UDP) |
|  |  |  | Status | 24 | 긴급 상태 | 0~1 | V2X 긴급 알림 송신 기능에서 V2X 긴급 알림 수신 기능에 전달 (UDP) |
| ethSelectedAlertMsg | 0x206 | 2 | selectedAlertLevel | 0~2 | 최종 경고 레벨 | 0~7 | ADAS에서 최종 경고 결과를 BCM, IVI에 전달 (UDP) |
|  |  |  | selectedAlertType | 3~5 | 최종 경고 타입 | 0~7 | ADAS에서 최종 경고 결과를 BCM, IVI에 전달 (UDP) |
|  |  |  | timeoutClear | 8 | 타임아웃 해제 플래그 | 0~1 | ADAS에서 최종 경고 결과를 BCM, IVI에 전달 (UDP) |
| frmEpsStateMsg | 0x123 | 2 | EpsAssistState | 0~2 | MDPS 보조 상태 | 0~7 | CGW에서 MDPS와 경계 판단 경로에 전달 |
|  |  |  | EpsFaultState | 3 | MDPS 고장 상태 | 0~1 | CGW에서 MDPS와 경계 판단 경로에 전달 |
|  |  |  | EpsTemp | 8~15 | MDPS 토크 요청 | 0~255 0.1Nm | CGW에서 MDPS와 경계 판단 경로에 전달 |
| frmAbsStateMsg | 0x124 | 2 | AbsCtrlState | 0~2 | ABS 제어 상태 | 0~7 | CGW에서 ESC와 경계 판단 경로에 전달 |
|  |  |  | AbsSlipLevel | 8~15 | ABS 슬립 레벨 | 0~255 | CGW에서 ESC와 경계 판단 경로에 전달 |
| frmEscStateMsg | 0x125 | 2 | EscCtrlState | 0~2 | ESC 제어 상태 | 0~7 | CGW에서 ESC, MDPS와 경계 판단 경로에 전달 |
|  |  |  | EscYawTarget | 8~15 | 요 모멘트 제어 요구 | 0~255 | CGW에서 ESC, MDPS와 경계 판단 경로에 전달 |
| frmTcsStateMsg | 0x126 | 2 | TcsCtrlState | 0 | TCS 활성 상태 | 0~1 | CGW에서 VCU, ESC와 경계 판단 경로에 전달 |
|  |  |  | TcsSlipRatio | 8~15 | TCS 슬립 비율 | 0~255 | CGW에서 VCU, ESC와 경계 판단 경로에 전달 |
| frmBrakeTempMsg | 0x127 | 2 | BrakeTempFL | 0~7 | 브레이크 전륜좌 온도 | 0~255 degC | CGW에서 ESC와 경계 판단 경로에 전달 |
|  |  |  | BrakeTempFR | 8~15 | 브레이크 전륜우 온도 | 0~255 degC | CGW에서 ESC와 경계 판단 경로에 전달 |
| frmSteeringAngleMsg | 0x128 | 2 | SteeringAngleRaw | 0~15 | 조향각 | -720~720 deg | CGW에서 MDPS와 ADAS에 전달 |
|  |  |  | SteeringAngleRaw | 16~31 | 조향각속도 | -1024~1023 deg/s | CGW에서 MDPS와 ADAS에 전달 |
| frmWheelPulseMsg | 0x104 | 2 | WheelPulseFront | 0~15 | 전륜좌 휠 펄스 | 0~65535 cnt | CGW에서 VCU, ESC, MDPS에 전달 |
|  |  |  | WheelPulseRear | 16~31 | 전륜우 휠 펄스 | 0~65535 cnt | CGW에서 VCU, ESC, MDPS에 전달 |
| frmSuspensionStateMsg | 0x105 | 2 | SuspensionMode | 0~2 | 댐퍼 모드 | 0~7 | CGW에서 경계 판단 경로에 전달 |
|  |  |  | SuspensionLevel | 8~15 | 차고 높이 | 0~255 mm | CGW에서 경계 판단 경로에 전달 |
| frmTirePressureMsg | 0x106 | 4 | TirePressFL | 0~7 | 전륜좌 타이어 압력 | 0~255 kPa | CGW에서 경계 판단 경로에 전달 |
|  |  |  | TirePressFR | 8~15 | 전륜우 타이어 압력 | 0~255 kPa | CGW에서 경계 판단 경로에 전달 |
|  |  |  | TirePressRL | 16~23 | 후륜좌 타이어 압력 | 0~255 kPa | CGW에서 경계 판단 경로에 전달 |
|  |  |  | TirePressRR | 24~31 | 후륜우 타이어 압력 | 0~255 kPa | CGW에서 경계 판단 경로에 전달 |
| frmChassisDiagReqMsg | 0x2A4 | 3 | ChsDiagServiceId | 0~7 | Chassis 진단 요청 ID | 0~255 | Validation Harness에서 CGW에 전달 |
|  |  |  | ChsDiagDidHigh | 8 | Chassis 진단 요청 활성 | 0~1 | Validation Harness에서 CGW에 전달 |
| frmChassisDiagResMsg | 0x107 | 3 | ChsDiagRespCode | 0~7 | Chassis 진단 응답 ID | 0~255 | CGW에서 Validation Harness에 전달 |
|  |  |  | ChsDiagData0 | 8~11 | Chassis 진단 결과 | 0~15 | CGW에서 Validation Harness에 전달 |
| frmAdasChassisStatusMsg | 0x1C1 | 2 | AdasChassisState | 0~7 | ADAS 섀시 상태 코드 | 0~255 | ADAS에서 SIL 대체 버스로 상태를 전달 |
|  |  |  | AdasHealthLevel | 8~15 | ADAS 헬스 레벨 | 0~255 | ADAS에서 SIL 대체 버스로 상태를 전달 |
| frmBrakeWearMsg | 0x129 | 1 | BrakePadWearLvl | 0~7 | 브레이크 패드 마모(전륜좌) | 0~100 % | CGW에서 ESC와 경계 판단 경로에 전달 |
|  |  |  | BrakePadWearLvl | 8~15 | 브레이크 패드 마모(전륜우) | 0~100 % | CGW에서 ESC와 경계 판단 경로에 전달 |
| frmRoadFrictionMsg | 0x108 | 1 | RoadFrictionCoef | 0~7 | 노면 마찰 추정치 | 0~255 | CGW에서 ADAS와 경계 판단 경로에 전달 |
| frmHvacStateMsg | 0x26A | 2 | CabinSetTemp | 0~7 | 실내 설정 온도 | 0~63 degC | BCM에서 앰비언트 제어와 차체 상태 판단에 전달 |
|  |  |  | BlowerLevel | 8~11 | 블로워 레벨 | 0~15 | BCM에서 앰비언트 제어와 차체 상태 판단에 전달 |
| frmHvacActuatorMsg | 0x26B | 2 | VentMode | 0~2 | 공조 벤트 모드 | 0~7 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | AcCompressorOn | 3 | A/C 컴프레서 요청 | 0~1 | BCM에서 앰비언트 제어에 전달 |
| frmMirrorStateMsg | 0x26C | 1 | MirrorFoldState | 0 | 미러 폴딩 상태 | 0~1 | BCM에서 창문 제어에 전달 |
|  |  |  | MirrorHeatState | 1 | 미러 열선 상태 | 0~1 | BCM에서 창문 제어에 전달 |
|  |  |  | MirrorAdjustAxis | 8~9 | 미러 조정 축 | 0~3 | BCM에서 창문 제어에 전달 |
| frmSeatStateMsg | 0x26D | 2 | DriverSeatPos | 0~7 | 운전석 시트 위치 | 0~255 | BCM에서 차체 상태 판단에 전달 |
|  |  |  | PassengerSeatPos | 8~15 | 동승석 시트 위치 | 0~255 | BCM에서 차체 상태 판단에 전달 |
| frmSeatControlMsg | 0x26E | 2 | SeatHeatLevel | 0~2 | 시트 히터 레벨 | 0~7 | BCM에서 차체 상태 판단에 전달 |
|  |  |  | SeatVentLevel | 3~5 | 시트 통풍 레벨 | 0~7 | BCM에서 차체 상태 판단에 전달 |
| frmDoorControlMsg | 0x26F | 1 | DoorControlCmd | 0~1 | 도어 언락 명령 | 0~3 | BCM에서 창문 제어에 전달 |
|  |  |  | ChildLockCmd | 2 | 트렁크 오픈 명령 | 0~1 | BCM에서 창문 제어에 전달 |
| frmInteriorLightMsg | 0x270 | 1 | CabinLightMode | 0~2 | 실내등 모드 | 0~7 | BCM에서 앰비언트 제어에 전달 |
|  |  |  | DomeLightLevel | 8~15 | 실내등 밝기 | 0~255 | BCM에서 앰비언트 제어에 전달 |
| frmRainLightAutoMsg | 0x271 | 1 | RainSenseLevel | 0~7 | 우적 센서 레벨 | 0~255 | BCM에서 앰비언트 제어와 창문 제어에 전달 |
|  |  |  | AutoLightState | 8 | 오토 헤드램프 요청 | 0~1 | BCM에서 앰비언트 제어와 창문 제어에 전달 |
| frmBcmDiagReqMsg | 0x272 | 3 | BcmDiagServiceId | 0~7 | BCM 진단 요청 ID | 0~255 | Validation Harness에서 BCM에 전달 |
|  |  |  | BcmDiagDidHigh | 8 | BCM 진단 요청 활성 | 0~1 | Validation Harness에서 BCM에 전달 |
| frmBcmDiagResMsg | 0x273 | 3 | BcmDiagRespCode | 0~7 | BCM 진단 응답 ID | 0~255 | BCM에서 Validation Harness에 전달 |
|  |  |  | BcmDiagData0 | 8~11 | BCM 진단 결과 | 0~15 | BCM에서 Validation Harness에 전달 |
| frmImmobilizerStateMsg | 0x274 | 1 | ImmobilizerState | 0~1 | 이모빌라이저 상태 | 0~3 | BCM에서 CGW, EMS에 전달 |
|  |  |  | KeyAuthState | 2~3 | 키 인증 상태 | 0~3 | BCM에서 CGW, EMS에 전달 |
| frmAlarmStateMsg | 0x275 | 1 | AlarmArmState | 0 | 알람 경계 상태 | 0~1 | BCM에서 차체 상태 판단과 CLU 표시에 전달 |
|  |  |  | IntrusionDetect | 1 | 알람 트리거 상태 | 0~1 | BCM에서 차체 상태 판단과 CLU 표시에 전달 |
| frmBodyGatewayStateMsg | 0x276 | 2 | BodyGwRouteState | 0~7 | Body GW 부하율 | 0~100 % | BCM에서 CGW에 전달 |
|  |  |  | BodyGwHealth | 8~15 | Body GW 라우팅 상태 | 0~255 | BCM에서 CGW에 전달 |
| frmBodyComfortStateMsg | 0x277 | 2 | ComfortProfile | 0~2 | 컴포트 모드 | 0~7 | BCM에서 앰비언트 제어와 차체 상태 판단에 전달 |
|  |  |  | ComfortStatus | 3 | 아동 안전 상태 | 0~1 | BCM에서 앰비언트 제어와 차체 상태 판단에 전달 |
| frmAudioFocusMsg | 0x289 | 1 | AudioFocusOwner | 0~2 | 오디오 포커스 소유자 | 0~7 | IVI에서 CLU 표시와 기본 표시에 사용 |
|  |  |  | AudioDuckingLvl | 8~15 | 오디오 덕킹 레벨 | 0~255 | IVI에서 CLU 표시와 기본 표시에 사용 |
| frmVoiceAssistStateMsg | 0x28A | 1 | VoiceAssistState | 0~2 | 음성비서 상태 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | WakeWordState | 8~11 | 음성 깨우기 소스 | 0~15 | IVI에서 CLU에 전달 |
| frmMapRenderStateMsg | 0x28B | 2 | ZoomLevel | 0~7 | 지도 줌 레벨 | 0~255 | IVI에서 구간 안내 판단에 사용 |
|  |  |  | MapRenderState | 8~11 | 지도 테마 | 0~15 | IVI에서 구간 안내 판단에 사용 |
| frmRouteAlertMsg | 0x28C | 2 | RouteAlertType | 0~3 | 다음 회전 유형 | 0~15 | IVI에서 구간 안내 판단과 CLU 표시에 사용 |
|  |  |  | RouteAlertEta | 8~15 | 다음 회전 잔여 거리 | 0~255 m | IVI에서 구간 안내 판단과 CLU 표시에 사용 |
| frmTrafficEventMsg | 0x28D | 3 | TrafficEventType | 0~3 | 교통 이벤트 유형 | 0~15 | IVI에서 구간 안내 판단과 ADAS에 전달 |
|  |  |  | TrafficSeverity | 4~6 | 교통 이벤트 심각도 | 0~7 | IVI에서 구간 안내 판단과 ADAS에 전달 |
|  |  |  | TrafficDistance | 8~15 | 이벤트 잔여 거리 | 0~255 m | IVI에서 구간 안내 판단과 ADAS에 전달 |
| frmPhoneProjectionMsg | 0x28E | 1 | ProjectionType | 0~2 | 프로젝션 유형 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | ProjectionState | 3~4 | 프로젝션 상태 | 0~3 | IVI에서 CLU에 전달 |
| frmClusterNotifMsg | 0x28F | 2 | ClusterNotifType | 0~3 | 클러스터 알림 유형 | 0~15 | IVI에서 CLU 표시와 기본 표시에 사용 |
|  |  |  | ClusterNotifArg | 4~6 | 클러스터 알림 우선순위 | 0~7 | IVI에서 CLU 표시와 기본 표시에 사용 |
| frmIviDiagReqMsg | 0x2A7 | 3 | IviDiagServiceId | 0~7 | IVI 진단 요청 ID | 0~255 | Validation Harness에서 IVI 진단 경로에 전달 |
|  |  |  | IviDiagDidHigh | 8 | IVI 진단 요청 활성 | 0~1 | Validation Harness에서 IVI에 전달 |
| frmIviDiagResMsg | 0x290 | 3 | IviDiagRespCode | 0~7 | IVI 진단 응답 ID | 0~255 | IVI에서 Validation Harness에 전달 |
|  |  |  | IviDiagData0 | 8~11 | IVI 진단 결과 | 0~15 | IVI에서 Validation Harness에 전달 |
| frmMediaMetaMsg | 0x291 | 2 | MediaTrackType | 0~3 | 미디어 장르 | 0~15 | IVI에서 CLU에 전달 |
|  |  |  | MediaRemainTime | 8~15 | 트랙 진행률 | 0~100 % | IVI에서 CLU에 전달 |
| frmSpeechTtsStateMsg | 0x292 | 2 | TtsState | 0~2 | TTS 상태 | 0~7 | IVI에서 CLU에 전달 |
|  |  |  | TtsQueueDepth | 8~15 | TTS 언어 ID | 0~255 | IVI에서 CLU에 전달 |
| frmConnectivityStateMsg | 0x293 | 2 | ConnectivityType | 0~2 | LTE 연결 상태 | 0~7 | IVI에서 구간 안내 판단과 CLU 표시에 사용 |
|  |  |  | ConnectivityState | 3 | Wi-Fi 연결 상태 | 0~1 | IVI에서 구간 안내 판단과 CLU 표시에 사용 |
|  |  |  | SignalBars | 4 | Bluetooth 연결 상태 | 0~1 | IVI에서 구간 안내 판단과 CLU 표시에 사용 |
| frmIviHealthDetailMsg | 0x294 | 2 | IviCpuLoad | 0~7 | IVI CPU 부하율 | 0~100 % | IVI에서 Validation Harness에 전달 |
|  |  |  | IviMemLoad | 8~15 | IVI 메모리 부하율 | 0~100 % | IVI에서 Validation Harness에 전달 |
| frmClusterSyncStateMsg | 0x295 | 2 | ClusterSyncState | 0~2 | 클러스터 동기화 상태 | 0~7 | IVI에서 클러스터 기본 표시에 사용 |
|  |  |  | ClusterSyncAge | 8~15 | 클러스터 동기화 시퀀스 | 0~255 | IVI에서 클러스터 기본 표시에 사용 |
| frmEngineTorqueMsg | 0x12E | 2 | EngineTorqueAct | 0~15 | 엔진 실제 토크 | 0~65535 0.1Nm | EMS에서 TCU, CGW에 전달 |
|  |  |  | EngineTorqueAct | 16~31 | 엔진 요구 토크 | 0~65535 0.1Nm | EMS에서 TCU, CGW에 전달 |
| frmEngineLoadMsg | 0x12F | 1 | EngineLoad | 0~7 | 엔진 부하율 | 0~100 % | EMS에서 CGW에 전달 |
| frmTransShiftStateMsg | 0x130 | 2 | ShiftState | 0~2 | 변속 상태 | 0~7 | TCU에서 EMS, CGW에 전달 |
|  |  |  | ShiftSlip | 3 | 변속 진행 상태 | 0~1 | TCU에서 EMS, CGW에 전달 |
|  |  |  | ShiftTargetGear | 8~10 | 목표 기어 | 0~7 | TCU에서 EMS, CGW에 전달 |
| frmPtDiagReqMsg | 0x2AA | 3 | PtDiagServiceId | 0~7 | Powertrain 진단 요청 ID | 0~255 | Validation Harness에서 CGW 진단 경로에 전달 |
|  |  |  | PtDiagDidHigh | 8 | Powertrain 진단 요청 활성 | 0~1 | Validation Harness에서 CGW에 전달 |
| frmPtDiagResMsg | 0x10E | 3 | PtDiagRespCode | 0~7 | Powertrain 진단 응답 ID | 0~255 | CGW에서 Validation Harness에 전달 |
|  |  |  | PtDiagData0 | 8~11 | Powertrain 진단 결과 | 0~15 | CGW에서 Validation Harness에 전달 |
| frmThermalMgmtStateMsg | 0x131 | 2 | ThermalMode | 0~2 | 열관리 모드 | 0~7 | CGW에서 EMS, TCU에 전달 |
|  |  |  | FanDuty | 8~15 | 팬 속도 명령 | 0~255 | CGW에서 EMS, TCU에 전달 |
| frmEnergyFlowStateMsg | 0x10F | 2 | RegenLevel | 0~3 | 회생 제동 레벨 | 0~15 | CGW에서 EMS, TCU에 전달 |
|  |  |  | EnergyFlowMode | 4~5 | 에너지 흐름 방향 | 0~3 | CGW에서 EMS, TCU에 전달 |
| frmPowertrainCtrlAuthMsg | 0x110 | 1 | CtrlAuthLevel | 0~1 | 파워트레인 제어 권한 상태 | 0~3 | CGW에서 EMS, TCU에 전달 |
|  |  |  | CtrlAuthSource | 8~11 | 파워트레인 제어 출처 | 0~15 | CGW에서 EMS, TCU에 전달 |
---



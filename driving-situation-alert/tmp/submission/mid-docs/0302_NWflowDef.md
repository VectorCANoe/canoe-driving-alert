# 네트워크 플로우 정의 (Network Flow Definition)

**Document ID**: PROJ-0302-NFD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.24
**Date**: 2026-03-07
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0302_NWflowDef.md` | `0301_SysFuncAnalysis.md` | `0303_Communication_Specification.md` |

## 작성 원칙

- 본 문서는 네트워크 흐름(Flow) 중심으로 정리한다.
- 상단 공식 Flow 표를 기준으로 전체 데이터 경로를 이해할 수 있게 구성한다.
- 도메인 간 전달 경계(GW 중심)와 운영 원칙을 명확히 보여준다.
- 상세 추적보다 네트워크 동작 흐름과 검증 가능성을 우선 제시한다.

---

## 심사위원 빠른 확인 (1분)

- 입력 경로: `Chassis CAN`, `Infotainment CAN`, `Emergency source`
- 코어 경로: `CHS_GW/INFOTAINMENT_GW -> ETH_SW -> ADAS_WARN_CTRL/NAV_CTX_MGR/EMS_ALERT/WARN_ARB_MGR`
- 출력 경로: `WARN_ARB_MGR -> BODY_GW/IVI_GW -> AMBIENT_CTRL/CLU_HMI_CTRL`
- 기준 주기: 입력 `100ms`, 출력 `50ms`, 긴급 타임아웃 `1000ms`
- 검증 포인트: 도메인 경계 유지, 경로 단절 없음, 경고 체인 연속성

---

## 네트워크 플로우 표 (공식 표준 양식)

| Channel | ID hex | Symbolic Name(message name) | Byte no. | Function | Bit no. | signal name | VAL_SCENARIO_CTRL | CHS_GW | INFOTAINMENT_GW | DOMAIN_ROUTER | ETH_SW | ADAS_WARN_CTRL | NAV_CTX_MGR | EMS_POLICE_TX | EMS_AMB_TX | EMS_ALERT_RX | WARN_ARB_MGR | BODY_GW | IVI_GW | AMBIENT_CTRL | CLU_HMI_CTRL | ENG_CTRL | TCM | ACCEL_CTRL | BRK_CTRL | STEER_CTRL | HAZARD_CTRL | WINDOW_CTRL | DRV_STATE_MGR | CLU_BASE_CTRL | VAL_BASELINE_CTRL | [비고] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chassis CAN | 0x2A0 | frmVehicleStateCanMsg | 0 | Vehicle State Check | 0~7 | vehicleSpeed | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Vehicle State Check | 8~9 | driveState | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x2A1 | frmSteeringCanMsg | 0 | Steering Input Check | 0 | steeringInput | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
| Chassis CAN | 0x2A2 | frmPedalInputCanMsg | 0 | Pedal Input Check | 0~7 | AccelPedal | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Pedal Input Check | 8~15 | BrakePedal | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x100 | frmSteeringStateCanMsg | 0 | Steering State Check | 0~1 | SteeringState |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  | CAN, 100ms |
| Chassis CAN | 0x101 | frmWheelSpeedMsg | 0 | Wheel Speed Check | 0~7 | WheelSpdFL |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Wheel Speed Check | 8~15 | WheelSpdFR |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
|  |  |  | 2 | Wheel Speed Check | 16~23 | WheelSpdRL |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
|  |  |  | 3 | Wheel Speed Check | 24~31 | WheelSpdRR |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x102 | frmYawAccelMsg | 0 | Yaw/Accel Check | 0~15 | YawRate |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Yaw/Accel Check | 16~31 | LatAccel |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x120 | frmBrakeStatusMsg | 0 | Brake Status Check | 0~7 | BrakePressure |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Brake Status Check | 8~9 | BrakeMode |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |
|  |  |  | 1 | Brake Status Check | 10 | AbsActive |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |
|  |  |  | 1 | Brake Status Check | 11 | EspActive |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |
| Chassis CAN | 0x121 | frmAccelStatusMsg | 0 | Accel Status Check | 0~7 | AccelRequest |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Accel Status Check | 8~15 | TorqueRequest |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x122 | frmSteeringTorqueMsg | 0 | Steering Torque Check | 0~11 | SteeringTorque |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Steering Torque Check | 12~15 | SteeringAssistLv |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |
| Chassis CAN | 0x103 | frmChassisHealthMsg | 0 | Chassis Health Check | 0~7 | ChassisAliveCnt | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Chassis Health Check | 8~11 | ChassisDiagState | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Chassis Health Check | 12~15 | ChassisFailCode | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x2A3 | frmNavContextCanMsg | 0 | Nav Context Check | 0~1 | roadZone | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Nav Context Check | 2~3 | navDirection | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Nav Context Check | 8~15 | zoneDistance | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Nav Context Check | 16~23 | speedLimit | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x260 | frmAmbientControlMsg | 0 | Ambient Pattern Control | 0~2 | ambientMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN, 50ms |
|  |  |  | 0 | Ambient Pattern Control | 3~5 | ambientColor |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Ambient Pattern Control | 6~7 | ambientPattern |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x261 | frmHazardControlMsg | 0 | Hazard Control | 0 | HazardSwitch |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  | Rx |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Hazard Control | 1 | HazardState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |
| Body CAN | 0x262 | frmWindowControlMsg | 0 | Window Control | 0~1 | WindowCommand |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 0 | Window Control | 2~3 | WindowState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x264 | frmDoorStateMsg | 0 | Door State Check | 0~7 | DoorStateMask |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | Door State Check | 8~9 | DoorLockState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |
|  |  |  | 1 | Door State Check | 10 | ChildLockState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |
|  |  |  | 1 | Door State Check | 11 | DoorOpenWarn |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |
| Body CAN | 0x265 | frmLampControlMsg | 0 | Lamp Control | 0~1 | HeadLampState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Lamp Control | 2~3 | TailLampState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Lamp Control | 4~5 | TurnLampState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Lamp Control | 6 | HazardLampReq |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |
| Body CAN | 0x266 | frmWiperStateMsg | 0 | Wiper State Check | 0~1 | FrontWiperState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Wiper State Check | 2~3 | RearWiperState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Wiper State Check | 4~7 | WiperInterval |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x267 | frmSeatBeltStateMsg | 0 | Seat Belt Check | 0 | DriverSeatBelt |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  | CAN, 100ms |
|  |  |  | 0 | Seat Belt Check | 1 | PassengerSeatBelt |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  |  |
|  |  |  | 0 | Seat Belt Check | 2~3 | RearSeatBelt |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  |  |
|  |  |  | 0 | Seat Belt Check | 4~5 | SeatBeltWarnLvl |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  |  |
| Body CAN | 0x268 | frmCabinAirStateMsg | 0 | Cabin Air Check | 0~7 | CabinTemp |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  | CAN, 100ms |
|  |  |  | 1 | Cabin Air Check | 8~15 | AirQualityIndex |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |
| Body CAN | 0x269 | frmBodyHealthMsg | 0 | Body Health Check | 0~7 | BodyAliveCnt | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Body Health Check | 8~11 | BodyDiagState | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Body Health Check | 12~15 | BodyFailCode | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x280 | frmClusterWarningMsg | 0 | Cluster Warning Display | 0~7 | warningTextCode |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 50ms |
| Infotainment CAN | 0x281 | frmClusterBaseStateMsg | 0 | Cluster Base Display | 0~7 | ClusterSpeed |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 1 | Cluster Base Display | 8~10 | ClusterGear |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
|  |  |  | 1 | Cluster Base Display | 11~15 | ClusterStatus |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x282 | frmNaviGuideStateMsg | 0 | Guide State Check | 0~1 | GuideLaneState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Guide State Check | 2~7 | GuideConfidence |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x283 | frmMediaStateMsg | 0 | Media State Check | 0~2 | MediaSource |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Media State Check | 3~5 | MediaState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Media State Check | 6 | MuteState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Media State Check | 8~15 | VolumeLevel |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x284 | frmCallStateMsg | 0 | Call State Check | 0~2 | CallState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Call State Check | 3 | MicMute |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Call State Check | 4~7 | SignalQuality |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Call State Check | 8~11 | BtDeviceCount |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x285 | frmNavigationRouteMsg | 0 | Route State Check | 0~1 | RouteClass |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Route State Check | 2~3 | GuideType |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Route State Check | 8~15 | RouteProgress |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Route State Check | 16~23 | EtaMinutes |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x286 | frmClusterThemeMsg | 0 | Cluster Theme Control | 0~2 | ThemeMode |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 0 | Cluster Theme Control | 3~7 | ClusterBrightness |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x287 | frmHmiPopupStateMsg | 0 | HMI Popup State | 0~3 | PopupType |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 50ms |
|  |  |  | 0 | HMI Popup State | 4~6 | PopupPriority |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | HMI Popup State | 7 | PopupActive |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x288 | frmInfotainmentHealthMsg | 0 | Infotainment Health Check | 0~7 | InfoAliveCnt | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Infotainment Health Check | 8~11 | InfoDiagState | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Infotainment Health Check | 12~15 | InfoFailCode | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN(Validation) | 0x2A5 | frmTestResultMsg | 0 | Scenario Result Report | 0 | scenarioResult | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Event |
| Chassis CAN(Validation) | 0x2A6 | frmBaseTestResultMsg | 0 | Base Result Report | 0~7 | BaseScenarioId | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx | Event |
|  |  |  | 1 | Base Result Report | 8 | BaseScenarioResult | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |
| Ethernet Backbone CAN Stub | 0x1C0 | frmEmergencyBroadcastMsg | 0 | Emergency Broadcast | 0~3 | emergencyType |  |  |  |  |  |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN-stub, 100ms |
|  |  |  | 0 | Emergency Broadcast | 4~5 | alertState |  |  |  |  |  |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Emergency Broadcast | 8~15 | sourceId |  |  |  |  |  |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Emergency Broadcast | 16~23 | eta |  |  |  |  |  |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 | Emergency Broadcast | 24~27 | emergencyDirection |  |  |  |  |  |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet Backbone CAN Stub | 0x1C2 | frmEmergencyMonitorMsg | 0 | Emergency Monitor | 0~7 | emergencyContext | Rx | Rx |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN-stub, 100ms |
|  |  |  | 1 | Emergency Monitor | 8 | TimeoutClearMon | Rx | Rx |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x2A8 | frmIgnitionEngineMsg | 0 | Ignition/Engine Check | 0 | IgnitionState | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Ignition/Engine Check | 1~2 | EngineState | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x2A9 | frmGearStateMsg | 0 | Gear State Check | 0~2 | GearInput | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Gear State Check | 3~5 | GearState | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x109 | frmPowertrainGatewayMsg | 0 | Gateway Routing Check | 0~7 | RoutingPolicy |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Gateway Routing Check | 8~15 | BoundaryStatus |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x12A | frmEngineSpeedTempMsg | 0 | Engine Thermal Check | 0~15 | EngineRpm |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Engine Thermal Check | 16~23 | CoolantTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 | Engine Thermal Check | 24~31 | OilTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x12B | frmFuelBatteryStateMsg | 0 | Fuel/Battery Check | 0~7 | FuelLevel |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Fuel/Battery Check | 8~15 | BatterySoc |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Fuel/Battery Check | 16~17 | ChargingState |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x12C | frmThrottleStateMsg | 0 | Throttle State Check | 0~7 | ThrottlePos |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Throttle State Check | 8~15 | ThrottleReq |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x12D | frmTransmissionTempMsg | 0 | Transmission Temp Check | 0~7 | TransOilTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Transmission Temp Check | 8~15 | ClutchTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x10A | frmVehicleModeMsg | 0 | Vehicle Mode Check | 0~2 | DriveMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Vehicle Mode Check | 3 | EcoMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Vehicle Mode Check | 4 | SportMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Vehicle Mode Check | 5 | SnowMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Vehicle Mode Check | 8~15 | PowertrainState |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x10B | frmPowerLimitMsg | 0 | Power Limit Check | 0~7 | TorqueLimit |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Power Limit Check | 8~15 | SpeedLimit |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x10C | frmCruiseStateMsg | 0 | Cruise State Check | 0~1 | CruiseState |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Cruise State Check | 2~3 | GapLevel |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Cruise State Check | 8~15 | CruiseSetSpeed |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x10D | frmPowertrainHealthMsg | 0 | Powertrain Health Check | 0~7 | PtAliveCnt | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Powertrain Health Check | 8~11 | PtDiagState | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Powertrain Health Check | 12~15 | PtFailCode | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0x510 | ethVehicleStateMsg | 0 | Gateway Normalized Vehicle State | 0~7 | vehicleSpeed |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | UDP, 100ms |
|  |  |  | 1 | Gateway Normalized Vehicle State | 8~9 | driveState |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0x511 | ethSteeringMsg | 0 | Gateway Normalized Steering | 0 | steeringInput |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | UDP, 100ms |
| Ethernet | 0x512 | ethNavContextMsg | 0 | Gateway Normalized Nav Context | 0~1 | roadZone |  |  | Tx |  | Rx | Rx | Rx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | UDP, 100ms |
|  |  |  | 0 | Gateway Normalized Nav Context | 2~3 | navDirection |  |  | Tx |  | Rx | Rx | Rx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Gateway Normalized Nav Context | 8~15 | zoneDistance |  |  | Tx |  | Rx | Rx | Rx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Gateway Normalized Nav Context | 16~23 | speedLimit |  |  | Tx |  | Rx | Rx | Rx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0xE100 | ETH_EmergencyAlert | 0 | Emergency Alert Tx/Rx | 0~1 | emergencyType |  |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | UDP, 100ms |
|  |  |  | 0 | Emergency Alert Tx/Rx | 2~3 | emergencyDirection |  |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Emergency Alert Tx/Rx | 8~15 | eta |  |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Emergency Alert Tx/Rx | 16~23 | sourceId |  |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 | Emergency Alert Tx/Rx | 24 | alertState |  |  |  |  | Rx |  |  | Tx | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet | 0xE200 | ethSelectedAlertMsg | 0 | Arbitration Result Distribution | 0~2 | selectedAlertLevel |  |  |  |  | Rx |  |  |  |  |  | Tx | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  | UDP, Event + 50ms |
|  |  |  | 0 | Arbitration Result Distribution | 3~5 | selectedAlertType |  |  |  |  | Rx |  |  |  |  |  | Tx | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Arbitration Result Distribution | 8 | timeoutClear |  |  |  |  | Rx |  |  |  |  |  | Tx | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x123 | frmEpsStateMsg | 0 | EPS State Check | 0~2 | EpsAssistState |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | EPS State Check | 3 | EpsFault |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |
|  |  |  | 1 | EPS State Check | 8~15 | EpsTorqueReq |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x124 | frmAbsStateMsg | 0 | ABS State Check | 0~2 | AbsCtrlState |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | ABS State Check | 8~15 | AbsSlipLevel |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x125 | frmEscStateMsg | 0 | ESC State Check | 0~2 | EscCtrlState |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | ESC State Check | 8~15 | YawCtrlReq |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x126 | frmTcsStateMsg | 0 | TCS State Check | 0 | TcsActive |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | TCS State Check | 8~15 | TcsSlipRatio |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x127 | frmBrakeTempMsg | 0 | Brake Temp Check | 0~7 | BrakeTempFL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Brake Temp Check | 8~15 | BrakeTempFR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
|  |  |  | 2 | Brake Temp Check | 16~23 | BrakeTempRL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
|  |  |  | 3 | Brake Temp Check | 24~31 | BrakeTempRR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x128 | frmSteeringAngleMsg | 0 | Steering Angle Check | 0~15 | SteeringAngle |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Steering Angle Check | 16~31 | SteeringAngleRate |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x104 | frmWheelPulseMsg | 0 | Wheel Pulse Check | 0~15 | WheelPulseFL |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Wheel Pulse Check | 16~31 | WheelPulseFR |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x105 | frmSuspensionStateMsg | 0 | Suspension State Check | 0~2 | DamperMode |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Suspension State Check | 8~15 | RideHeight |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x106 | frmTirePressureMsg | 0 | Tire Pressure Check | 0~7 | TirePressFL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Tire Pressure Check | 8~15 | TirePressFR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Tire Pressure Check | 16~23 | TirePressRL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 | Tire Pressure Check | 24~31 | TirePressRR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x2A4 | frmChassisDiagReqMsg | 0 | Chassis Diag Request | 0~7 | ChassisDiagReqId | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Chassis Diag Request | 8 | ChassisDiagReqAct | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x107 | frmChassisDiagResMsg | 0 | Chassis Diag Response | 0~7 | ChassisDiagResId | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Chassis Diag Response | 8~11 | ChassisDiagStatus | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ethernet Backbone CAN Stub | 0x1C1 | frmAdasChassisStatusMsg | 0 | ADAS Chassis Interface | 0~7 | AdasChassisState |  | Rx |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN-stub, 100ms |
|  |  |  | 1 | ADAS Chassis Interface | 8~15 | AdasHealthLevel |  | Rx |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x129 | frmBrakeWearMsg | 0 | Brake Wear Check | 0~7 | BrakePadWearFL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Brake Wear Check | 8~15 | BrakePadWearFR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x108 | frmRoadFrictionMsg | 0 | Road Friction Check | 0~7 | RoadFrictionEst |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Road Friction Check | 8~11 | SurfaceType |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x26A | frmHvacStateMsg | 0 | HVAC State Check | 0~7 | CabinSetTemp |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | HVAC State Check | 8~11 | BlowerLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x26B | frmHvacActuatorMsg | 0 | HVAC Actuator Check | 0~2 | VentMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | HVAC Actuator Check | 3 | AcCompressorReq |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x26C | frmMirrorStateMsg | 0 | Mirror State Check | 0 | MirrorFoldState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 0 | Mirror State Check | 1 | MirrorHeatState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
|  |  |  | 1 | Mirror State Check | 8~9 | MirrorAdjAxis |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x26D | frmSeatStateMsg | 0 | Seat State Check | 0~7 | DriverSeatPos |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | Seat State Check | 8~15 | PassengerSeatPos |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x26E | frmSeatControlMsg | 0 | Seat Control Check | 0~2 | SeatHeatLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Seat Control Check | 3~5 | SeatVentLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x26F | frmDoorControlMsg | 0 | Door Control Check | 0~1 | DoorUnlockCmd |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 0 | Door Control Check | 2 | TrunkOpenCmd |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x270 | frmInteriorLightMsg | 0 | Interior Light Check | 0~2 | InteriorLampMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | Interior Light Check | 8~15 | InteriorLampLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x271 | frmRainLightAutoMsg | 0 | Auto Rain/Light Check | 0~7 | RainSensorLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 1 | Auto Rain/Light Check | 8 | AutoHeadlampReq |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x272 | frmBcmDiagReqMsg | 0 | BCM Diag Request | 0~7 | BcmDiagReqId | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | BCM Diag Request | 8 | BcmDiagReqAct | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x273 | frmBcmDiagResMsg | 0 | BCM Diag Response | 0~7 | BcmDiagResId | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | BCM Diag Response | 8~11 | BcmDiagStatus | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x274 | frmImmobilizerStateMsg | 0 | Immobilizer State | 0~1 | ImmoState |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Immobilizer State | 2~3 | KeyAuthState |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x275 | frmAlarmStateMsg | 0 | Alarm State Check | 0 | AlarmArmed |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Alarm State Check | 1 | AlarmTrigger |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |
|  |  |  | 1 | Alarm State Check | 8~11 | AlarmZone |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x276 | frmBodyGatewayStateMsg | 0 | Body Gateway State | 0~7 | BodyGatewayLoad |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Body Gateway State | 8~15 | BodyGatewayRoute |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x277 | frmBodyComfortStateMsg | 0 | Body Comfort State | 0~2 | ComfortMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Body Comfort State | 3 | ChildSafetyState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Infotainment CAN | 0x289 | frmAudioFocusMsg | 0 | Audio Focus Check | 0~2 | AudioFocusOwner |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 100ms |
|  |  |  | 1 | Audio Focus Check | 8~15 | AudioDuckLevel |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x28A | frmVoiceAssistStateMsg | 0 | Voice Assist State | 0~2 | VoiceAssistState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Voice Assist State | 8~11 | VoiceWakeSource |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x28B | frmMapRenderStateMsg | 0 | Map Render State | 0~7 | MapZoomLevel |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Map Render State | 8~11 | MapTheme |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x28C | frmRouteAlertMsg | 0 | Route Alert Check | 0~3 | NextTurnType |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Route Alert Check | 8~15 | NextTurnDist |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x28D | frmTrafficEventMsg | 0 | Traffic Event Check | 0~3 | TrafficEventType |  |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Traffic Event Check | 4~6 | TrafficSeverity |  |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Traffic Event Check | 8~15 | TrafficDist |  |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x28E | frmPhoneProjectionMsg | 0 | Phone Projection Check | 0~2 | ProjectionType |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Phone Projection Check | 3~4 | ProjectionState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x28F | frmClusterNotifMsg | 0 | Cluster Notification | 0~3 | ClusterNotifType |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 0 | Cluster Notification | 4~6 | ClusterNotifPrio |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x2A7 | frmIviDiagReqMsg | 0 | IVI Diag Request | 0~7 | IviDiagReqId | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | IVI Diag Request | 8 | IviDiagReqAct | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x290 | frmIviDiagResMsg | 0 | IVI Diag Response | 0~7 | IviDiagResId | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | IVI Diag Response | 8~11 | IviDiagStatus | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x291 | frmMediaMetaMsg | 0 | Media Metadata Check | 0~3 | MediaGenre |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 100ms |
|  |  |  | 1 | Media Metadata Check | 8~15 | TrackProgress |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x292 | frmSpeechTtsStateMsg | 0 | TTS State Check | 0~2 | TtsState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 100ms |
|  |  |  | 1 | TTS State Check | 8~15 | TtsLangId |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x293 | frmConnectivityStateMsg | 0 | Connectivity State | 0~2 | LteState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Connectivity State | 3 | WifiState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Connectivity State | 4 | BtState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x294 | frmIviHealthDetailMsg | 0 | IVI Health Detail | 0~7 | CpuLoad | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | IVI Health Detail | 8~15 | MemLoad | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x295 | frmClusterSyncStateMsg | 0 | Cluster Sync State | 0~2 | ClusterSyncState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 1 | Cluster Sync State | 8~15 | ClusterSyncSeq |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
| Powertrain CAN | 0x12E | frmEngineTorqueMsg | 0 | Engine Torque Check | 0~15 | EngineTorqueAct |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Engine Torque Check | 16~31 | EngineTorqueReq |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x12F | frmEngineLoadMsg | 0 | Engine Load Check | 0~7 | EngineLoad |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Engine Load Check | 8~15 | ManifoldPressure |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x130 | frmTransShiftStateMsg | 0 | Transmission Shift Check | 0~2 | ShiftState |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Transmission Shift Check | 3 | ShiftInProgress |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Transmission Shift Check | 8~10 | ShiftTargetGear |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x2AA | frmPtDiagReqMsg | 0 | Powertrain Diag Request | 0~7 | PtDiagReqId | Tx |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Powertrain Diag Request | 8 | PtDiagReqAct | Tx |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x10E | frmPtDiagResMsg | 0 | Powertrain Diag Response | 0~7 | PtDiagResId | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Powertrain Diag Response | 8~11 | PtDiagStatus | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x131 | frmThermalMgmtStateMsg | 0 | Thermal Management | 0~2 | ThermalMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Thermal Management | 8~15 | FanSpeedCmd |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x10F | frmEnergyFlowStateMsg | 0 | Energy Flow Check | 0~3 | RegenLevel |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Energy Flow Check | 4~5 | EnergyFlowDir |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x110 | frmPowertrainCtrlAuthMsg | 0 | Powertrain Control Auth | 0~1 | PtCtrlAuthState |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Powertrain Control Auth | 8~11 | PtCtrlSource |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
---

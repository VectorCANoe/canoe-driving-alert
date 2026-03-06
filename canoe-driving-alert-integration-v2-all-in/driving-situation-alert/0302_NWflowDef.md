# 네트워크 플로우 정의 (Network Flow Definition)

**Document ID**: PROJ-0302-NFD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.14
**Date**: 2026-03-03
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0302_NWflowDef.md` | `0301_SysFuncAnalysis.md` | `0303_Communication_Specification.md` |

---

## 작성 원칙

- 상단 표는 공식 표준 양식(`Channel/ID hex/Symbolic Name/Byte/Function/Bit/signal/노드 TxRx`) 구조를 유지한다.
- 상단 표의 `Bit no.`는 가독성을 위해 범위 표기(예: `0~7`, `8~15`)를 사용하되, 상단 열 구성은 공식 샘플 구조를 유지한다.
- 상단 표의 `signal name`은 0304 표준 변수명(`vehicleSpeed` 등) 기준으로 작성하고, 코드/런타임 별칭(`g*`)은 하단 보강표에서만 관리한다.
- 0304에 아직 등재되지 않은 Vehicle Baseline 확장 신호는 DBC 원본 신호명(`AccelPedal`, `DriveMode` 등)으로 표기한다.
- 옵션1 아키텍처를 고정한다: `중앙 경고코어 + Ethernet 백본(ETH_SWITCH) + 도메인 게이트웨이 + 도메인 CAN`.
- 상세 추적 정보(`Flow/Func/Req/주기/활성/해제`)는 하단 표에 분리한다.
- CAN 신호 원본은 계층 분리로 관리한다: 도메인 프로파일은 `canoe/databases/chassis_can.dbc`, `canoe/databases/powertrain_can.dbc`, `canoe/databases/body_can.dbc`, `canoe/databases/infotainment_can.dbc`, `canoe/databases/test_can.dbc`를 사용하고, Ethernet 프로파일은 `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`를 사용한다.
- 검증 범위는 CANoe SIL, CAN + Ethernet(UDP)만 사용한다.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- OTA/UDS/DoIP 관련 플로우는 본 문서 범위에서 제외한다.
- `Flow_009`, `Flow_106`, `Flow_205`는 Validation Harness 경로(검증 전용)이며 양산 서비스 플로우와 구분한다.
- 제출 전 현대/기아 및 OEM 기준으로 설명/별칭은 정리하되, Flow/Comm/ID/signal 식별자는 SoT 기준으로 고정 유지한다.
- Vehicle Baseline(Req_101~Req_119) 플로우(`Flow_101~Flow_106`, `Flow_201~Flow_205`)는 본 문서에서 확정 정의하고, DBC는 이 정의를 구현 대상으로 사용한다.
- V2 확장 요구(`Req_120~Req_124`) 플로우(`Flow_120~Flow_124`)는 구현 활성 상태로 관리하며, 관련 DBC/코드/테스트를 동일 커밋에서 동기화한다.
- EMS는 상위 문서 레벨에서 논리 단말 `EMS_ALERT`로 표기하고, 상단 표의 `EMS_POLICE_TX/EMS_AMB_TX/EMS_ALERT_RX` 열은 내부 구현 모듈 분해 관점으로만 해석한다.

---

## 네트워크 플로우 표 (공식 표준 양식)

| Channel | ID hex | Symbolic Name(message name) | Byte no. | Function | Bit no. | signal name | SIL_TEST_CTRL | CHASSIS_GW | INFOTAINMENT_GW | DOMAIN_GW_ROUTER | ETH_SWITCH | ADAS_WARN_CTRL | NAV_CONTEXT_MGR | EMS_POLICE_TX | EMS_AMB_TX | EMS_ALERT_RX | WARN_ARB_MGR | BODY_GW | IVI_GW | BCM_AMBIENT_CTRL | CLU_HMI_CTRL | ENGINE_CTRL | TRANSMISSION_CTRL | ACCEL_CTRL | BRAKE_CTRL | STEERING_CTRL | HAZARD_CTRL | WINDOW_CTRL | DRIVER_STATE_CTRL | CLUSTER_BASE_CTRL | VEHICLE_BASE_TEST_CTRL | [비고] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chassis CAN | 0x100 | frmVehicleStateCanMsg | 0 | Vehicle State Check | 0~7 | vehicleSpeed | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Vehicle State Check | 8~9 | driveState | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x101 | frmSteeringCanMsg | 0 | Steering Input Check | 0 | steeringInput | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
| Chassis CAN | 0x102 | frmPedalInputCanMsg | 0 | Pedal Input Check | 0~7 | AccelPedal | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Pedal Input Check | 8~15 | BrakePedal | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x103 | frmSteeringStateCanMsg | 0 | Steering State Check | 0~1 | SteeringState |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  | CAN, 100ms |
| Chassis CAN | 0x104 | frmWheelSpeedMsg | 0 | Wheel Speed Check | 0~7 | WheelSpdFL |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Wheel Speed Check | 8~15 | WheelSpdFR |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
|  |  |  | 2 | Wheel Speed Check | 16~23 | WheelSpdRL |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
|  |  |  | 3 | Wheel Speed Check | 24~31 | WheelSpdRR |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x105 | frmYawAccelMsg | 0 | Yaw/Accel Check | 0~15 | YawRate |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Yaw/Accel Check | 16~31 | LatAccel |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x106 | frmBrakeStatusMsg | 0 | Brake Status Check | 0~7 | BrakePressure |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Brake Status Check | 8~9 | BrakeMode |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |
|  |  |  | 1 | Brake Status Check | 10 | AbsActive |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |
|  |  |  | 1 | Brake Status Check | 11 | EspActive |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |
| Chassis CAN | 0x107 | frmAccelStatusMsg | 0 | Accel Status Check | 0~7 | AccelRequest |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Accel Status Check | 8~15 | TorqueRequest |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x108 | frmSteeringTorqueMsg | 0 | Steering Torque Check | 0~11 | SteeringTorque |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Steering Torque Check | 12~15 | SteeringAssistLv |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |
| Chassis CAN | 0x109 | frmChassisHealthMsg | 0 | Chassis Health Check | 0~7 | ChassisAliveCnt | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Chassis Health Check | 8~11 | ChassisDiagState | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Chassis Health Check | 12~15 | ChassisFailCode | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x110 | frmNavContextCanMsg | 0 | Nav Context Check | 0~1 | roadZone | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Nav Context Check | 2~3 | navDirection | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Nav Context Check | 8~15 | zoneDistance | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Nav Context Check | 16~23 | speedLimit | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x210 | frmAmbientControlMsg | 0 | Ambient Pattern Control | 0~2 | ambientMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN, 50ms |
|  |  |  | 0 | Ambient Pattern Control | 3~5 | ambientColor |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Ambient Pattern Control | 6~7 | ambientPattern |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x211 | frmHazardControlMsg | 0 | Hazard Control | 0 | HazardSwitch |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  | Rx |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Hazard Control | 1 | HazardState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |
| Body CAN | 0x212 | frmWindowControlMsg | 0 | Window Control | 0~1 | WindowCommand |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 0 | Window Control | 2~3 | WindowState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x213 | frmDriverStateMsg | 0 | Driver State Check | 0~2 | DriverStateLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Driver State Check | 3~5 | DriverStateInfo |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x214 | frmDoorStateMsg | 0 | Door State Check | 0~7 | DoorStateMask |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | Door State Check | 8~9 | DoorLockState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |
|  |  |  | 1 | Door State Check | 10 | ChildLockState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |
|  |  |  | 1 | Door State Check | 11 | DoorOpenWarn |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |
| Body CAN | 0x215 | frmLampControlMsg | 0 | Lamp Control | 0~1 | HeadLampState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Lamp Control | 2~3 | TailLampState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Lamp Control | 4~5 | TurnLampState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Lamp Control | 6 | HazardLampReq |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |
| Body CAN | 0x216 | frmWiperStateMsg | 0 | Wiper State Check | 0~1 | FrontWiperState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Wiper State Check | 2~3 | RearWiperState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Wiper State Check | 4~7 | WiperInterval |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x217 | frmSeatBeltStateMsg | 0 | Seat Belt Check | 0 | DriverSeatBelt |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  | CAN, 100ms |
|  |  |  | 0 | Seat Belt Check | 1 | PassengerSeatBelt |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  |  |
|  |  |  | 0 | Seat Belt Check | 2~3 | RearSeatBelt |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  |  |
|  |  |  | 0 | Seat Belt Check | 4~5 | SeatBeltWarnLvl |  |  |  |  |  |  |  |  |  |  |  | Rx |  | Rx |  |  |  |  |  |  |  |  | Tx |  |  |  |
| Body CAN | 0x218 | frmCabinAirStateMsg | 0 | Cabin Air Check | 0~7 | CabinTemp |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  | CAN, 100ms |
|  |  |  | 1 | Cabin Air Check | 8~15 | AirQualityIndex |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |
| Body CAN | 0x219 | frmBodyHealthMsg | 0 | Body Health Check | 0~7 | BodyAliveCnt | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Body Health Check | 8~11 | BodyDiagState | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Body Health Check | 12~15 | BodyFailCode | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x220 | frmClusterWarningMsg | 0 | Cluster Warning Display | 0~7 | warningTextCode |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 50ms |
| Infotainment CAN | 0x221 | frmClusterBaseStateMsg | 0 | Cluster Base Display | 0~7 | ClusterSpeed |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 1 | Cluster Base Display | 8~10 | ClusterGear |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
|  |  |  | 1 | Cluster Base Display | 11~15 | ClusterStatus |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x222 | frmNaviGuideStateMsg | 0 | Guide State Check | 0~1 | GuideLaneState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Guide State Check | 2~7 | GuideConfidence |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x223 | frmMediaStateMsg | 0 | Media State Check | 0~2 | MediaSource |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Media State Check | 3~5 | MediaState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Media State Check | 6 | MuteState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Media State Check | 8~15 | VolumeLevel |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x224 | frmCallStateMsg | 0 | Call State Check | 0~2 | CallState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Call State Check | 3 | MicMute |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Call State Check | 4~7 | SignalQuality |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Call State Check | 8~11 | BtDeviceCount |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x225 | frmNavigationRouteMsg | 0 | Route State Check | 0~1 | RouteClass |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Route State Check | 2~3 | GuideType |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Route State Check | 8~15 | RouteProgress |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Route State Check | 16~23 | EtaMinutes |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x226 | frmClusterThemeMsg | 0 | Cluster Theme Control | 0~2 | ThemeMode |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 0 | Cluster Theme Control | 3~7 | ClusterBrightness |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x227 | frmHmiPopupStateMsg | 0 | HMI Popup State | 0~3 | PopupType |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 50ms |
|  |  |  | 0 | HMI Popup State | 4~6 | PopupPriority |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | HMI Popup State | 7 | PopupActive |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x228 | frmInfotainmentHealthMsg | 0 | Infotainment Health Check | 0~7 | InfoAliveCnt | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Infotainment Health Check | 8~11 | InfoDiagState | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Infotainment Health Check | 12~15 | InfoFailCode | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Test CAN | 0x230 | frmTestResultMsg | 0 | Scenario Result Report | 0 | scenarioResult | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Event |
| Test CAN | 0x231 | frmBaseTestResultMsg | 0 | Base Result Report | 0~7 | BaseScenarioId | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx | Event |
|  |  |  | 1 | Base Result Report | 8 | BaseScnResult | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |
| Test CAN | 0x232 | frmEmergencyMonitorMsg | 0 | Emergency Monitor | 0~7 | emergencyContext | Rx | Rx |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Emergency Monitor | 8 | TimeoutClearMon | Rx | Rx |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x300 | frmIgnitionEngineMsg | 0 | Ignition/Engine Check | 0 | IgnitionState | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Ignition/Engine Check | 1~2 | EngineState | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x301 | frmGearStateMsg | 0 | Gear State Check | 0~2 | GearInput | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Gear State Check | 3~5 | GearState | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x302 | frmPowertrainGatewayMsg | 0 | Gateway Routing Check | 0~7 | RoutingPolicy |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Gateway Routing Check | 8~15 | BoundaryStatus |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x303 | frmEngineSpeedTempMsg | 0 | Engine Thermal Check | 0~15 | EngineRpm |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Engine Thermal Check | 16~23 | CoolantTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 | Engine Thermal Check | 24~31 | OilTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x304 | frmFuelBatteryStateMsg | 0 | Fuel/Battery Check | 0~7 | FuelLevel |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Fuel/Battery Check | 8~15 | BatterySoc |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Fuel/Battery Check | 16~17 | ChargingState |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x305 | frmThrottleStateMsg | 0 | Throttle State Check | 0~7 | ThrottlePos |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Throttle State Check | 8~15 | ThrottleReq |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x306 | frmTransmissionTempMsg | 0 | Transmission Temp Check | 0~7 | TransOilTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Transmission Temp Check | 8~15 | ClutchTemp |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x307 | frmVehicleModeMsg | 0 | Vehicle Mode Check | 0~2 | DriveMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Vehicle Mode Check | 3 | EcoMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Vehicle Mode Check | 4 | SportMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Vehicle Mode Check | 5 | SnowMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Vehicle Mode Check | 8~15 | PowertrainState |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x308 | frmPowerLimitMsg | 0 | Power Limit Check | 0~7 | TorqueLimit |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Power Limit Check | 8~15 | SpeedLimit |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x309 | frmCruiseStateMsg | 0 | Cruise State Check | 0~1 | CruiseState |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Cruise State Check | 2~3 | GapLevel |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Cruise State Check | 8~15 | CruiseSetSpeed |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x30A | frmPowertrainHealthMsg | 0 | Powertrain Health Check | 0~7 | PtAliveCnt | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
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
| Chassis CAN | 0x10A | frmEpsStateMsg | 0 | EPS State Check | 0~2 | EpsAssistState |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | EPS State Check | 3 | EpsFault |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |
|  |  |  | 1 | EPS State Check | 8~15 | EpsTorqueReq |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x10B | frmAbsStateMsg | 0 | ABS State Check | 0~2 | AbsCtrlState |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | ABS State Check | 8~15 | AbsSlipLevel |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x10C | frmEscStateMsg | 0 | ESC State Check | 0~2 | EscCtrlState |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | ESC State Check | 8~15 | YawCtrlReq |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x10D | frmTcsStateMsg | 0 | TCS State Check | 0 | TcsActive |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | TCS State Check | 8~15 | TcsSlipRatio |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x10E | frmBrakeTempMsg | 0 | Brake Temp Check | 0~7 | BrakeTempFL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Brake Temp Check | 8~15 | BrakeTempFR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
|  |  |  | 2 | Brake Temp Check | 16~23 | BrakeTempRL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
|  |  |  | 3 | Brake Temp Check | 24~31 | BrakeTempRR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x10F | frmSteeringAngleMsg | 0 | Steering Angle Check | 0~15 | SteeringAngle |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Steering Angle Check | 16~31 | SteeringAngleRate |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x11A | frmWheelPulseMsg | 0 | Wheel Pulse Check | 0~15 | WheelPulseFL |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Wheel Pulse Check | 16~31 | WheelPulseFR |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx | Rx |  |  |  |  |  |  |
| Chassis CAN | 0x11B | frmSuspensionStateMsg | 0 | Suspension State Check | 0~2 | DamperMode |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Suspension State Check | 8~15 | RideHeight |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x11C | frmTirePressureMsg | 0 | Tire Pressure Check | 0~7 | TirePressFL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Tire Pressure Check | 8~15 | TirePressFR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 2 | Tire Pressure Check | 16~23 | TirePressRL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 3 | Tire Pressure Check | 24~31 | TirePressRR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x11D | frmChassisDiagReqMsg | 0 | Chassis Diag Request | 0~7 | ChassisDiagReqId | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Chassis Diag Request | 8 | ChassisDiagReqAct | Tx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x11E | frmChassisDiagResMsg | 0 | Chassis Diag Response | 0~7 | ChassisDiagResId | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Chassis Diag Response | 8~11 | ChassisDiagStatus | Rx | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x11F | frmAdasChassisStatusMsg | 0 | ADAS Chassis Interface | 0 | LateralCtrlAvail |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | ADAS Chassis Interface | 1 | LongitudinalCtrlAvail |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | ADAS Chassis Interface | 8~11 | ChassisCtrlMode |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Chassis CAN | 0x120 | frmBrakeWearMsg | 0 | Brake Wear Check | 0~7 | BrakePadWearFL |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Brake Wear Check | 8~15 | BrakePadWearFR |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |
| Chassis CAN | 0x121 | frmRoadFrictionMsg | 0 | Road Friction Check | 0~7 | RoadFrictionEst |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Road Friction Check | 8~11 | SurfaceType |  | Tx |  | Rx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x240 | frmHvacStateMsg | 0 | HVAC State Check | 0~7 | CabinSetTemp |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | HVAC State Check | 8~11 | BlowerLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x241 | frmHvacActuatorMsg | 0 | HVAC Actuator Check | 0~2 | VentMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | HVAC Actuator Check | 3 | AcCompressorReq |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x242 | frmMirrorStateMsg | 0 | Mirror State Check | 0 | MirrorFoldState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 0 | Mirror State Check | 1 | MirrorHeatState |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
|  |  |  | 1 | Mirror State Check | 8~9 | MirrorAdjAxis |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x243 | frmSeatStateMsg | 0 | Seat State Check | 0~7 | DriverSeatPos |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | Seat State Check | 8~15 | PassengerSeatPos |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x244 | frmSeatControlMsg | 0 | Seat Control Check | 0~2 | SeatHeatLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Seat Control Check | 3~5 | SeatVentLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x245 | frmDoorControlMsg | 0 | Door Control Check | 0~1 | DoorUnlockCmd |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 0 | Door Control Check | 2 | TrunkOpenCmd |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x246 | frmInteriorLightMsg | 0 | Interior Light Check | 0~2 | InteriorLampMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 1 | Interior Light Check | 8~15 | InteriorLampLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x247 | frmRainLightAutoMsg | 0 | Auto Rain/Light Check | 0~7 | RainSensorLevel |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  | CAN, 100ms |
|  |  |  | 1 | Auto Rain/Light Check | 8 | AutoHeadlampReq |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |
| Body CAN | 0x248 | frmBcmDiagReqMsg | 0 | BCM Diag Request | 0~7 | BcmDiagReqId | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | BCM Diag Request | 8 | BcmDiagReqAct | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x249 | frmBcmDiagResMsg | 0 | BCM Diag Response | 0~7 | BcmDiagResId | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | BCM Diag Response | 8~11 | BcmDiagStatus | Rx |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x24A | frmImmobilizerStateMsg | 0 | Immobilizer State | 0~1 | ImmoState |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Immobilizer State | 2~3 | KeyAuthState |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x24B | frmAlarmStateMsg | 0 | Alarm State Check | 0 | AlarmArmed |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Alarm State Check | 1 | AlarmTrigger |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |
|  |  |  | 1 | Alarm State Check | 8~11 | AlarmZone |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |
| Body CAN | 0x24C | frmBodyGatewayStateMsg | 0 | Body Gateway State | 0~7 | BodyGatewayLoad |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Body Gateway State | 8~15 | BodyGatewayRoute |  |  |  | Rx |  |  |  |  |  |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |
| Body CAN | 0x24D | frmBodyComfortStateMsg | 0 | Body Comfort State | 0~2 | ComfortMode |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  | CAN, 100ms |
|  |  |  | 0 | Body Comfort State | 3 | ChildSafetyState |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |  |
| Infotainment CAN | 0x260 | frmAudioFocusMsg | 0 | Audio Focus Check | 0~2 | AudioFocusOwner |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 100ms |
|  |  |  | 1 | Audio Focus Check | 8~15 | AudioDuckLevel |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x261 | frmVoiceAssistStateMsg | 0 | Voice Assist State | 0~2 | VoiceAssistState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Voice Assist State | 8~11 | VoiceWakeSource |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x262 | frmMapRenderStateMsg | 0 | Map Render State | 0~7 | MapZoomLevel |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Map Render State | 8~11 | MapTheme |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x263 | frmRouteAlertMsg | 0 | Route Alert Check | 0~3 | NextTurnType |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Route Alert Check | 8~15 | NextTurnDist |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x264 | frmTrafficEventMsg | 0 | Traffic Event Check | 0~3 | TrafficEventType |  |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Traffic Event Check | 4~6 | TrafficSeverity |  |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Traffic Event Check | 8~15 | TrafficDist |  |  | Tx |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x265 | frmPhoneProjectionMsg | 0 | Phone Projection Check | 0~2 | ProjectionType |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Phone Projection Check | 3~4 | ProjectionState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x266 | frmClusterNotifMsg | 0 | Cluster Notification | 0~3 | ClusterNotifType |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 0 | Cluster Notification | 4~6 | ClusterNotifPrio |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x267 | frmIviDiagReqMsg | 0 | IVI Diag Request | 0~7 | IviDiagReqId | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | IVI Diag Request | 8 | IviDiagReqAct | Tx |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x268 | frmIviDiagResMsg | 0 | IVI Diag Response | 0~7 | IviDiagResId | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | IVI Diag Response | 8~11 | IviDiagStatus | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x269 | frmMediaMetaMsg | 0 | Media Metadata Check | 0~3 | MediaGenre |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 100ms |
|  |  |  | 1 | Media Metadata Check | 8~15 | TrackProgress |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x26A | frmSpeechTtsStateMsg | 0 | TTS State Check | 0~2 | TtsState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  | CAN, 100ms |
|  |  |  | 1 | TTS State Check | 8~15 | TtsLangId |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  | Rx |  |  |  |  |  |  |  |  | Rx |  |  |
| Infotainment CAN | 0x26B | frmConnectivityStateMsg | 0 | Connectivity State | 0~2 | LteState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Connectivity State | 3 | WifiState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | 0 | Connectivity State | 4 | BtState |  |  | Tx |  |  |  | Rx |  |  |  |  |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x26C | frmIviHealthDetailMsg | 0 | IVI Health Detail | 0~7 | CpuLoad | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | IVI Health Detail | 8~15 | MemLoad | Rx |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Infotainment CAN | 0x26D | frmClusterSyncStateMsg | 0 | Cluster Sync State | 0~2 | ClusterSyncState |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  | CAN, 50ms |
|  |  |  | 1 | Cluster Sync State | 8~15 | ClusterSyncSeq |  |  |  |  |  |  |  |  |  |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  | Rx |  |  |
| Powertrain CAN | 0x30B | frmEngineTorqueMsg | 0 | Engine Torque Check | 0~15 | EngineTorqueAct |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 2 | Engine Torque Check | 16~31 | EngineTorqueReq |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x30C | frmEngineLoadMsg | 0 | Engine Load Check | 0~7 | EngineLoad |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Engine Load Check | 8~15 | ManifoldPressure |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Tx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x30D | frmTransShiftStateMsg | 0 | Transmission Shift Check | 0~2 | ShiftState |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Transmission Shift Check | 3 | ShiftInProgress |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  |  |
|  |  |  | 1 | Transmission Shift Check | 8~10 | ShiftTargetGear |  |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  | Rx | Tx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x30E | frmPtDiagReqMsg | 0 | Powertrain Diag Request | 0~7 | PtDiagReqId | Tx |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Powertrain Diag Request | 8 | PtDiagReqAct | Tx |  |  | Rx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x30F | frmPtDiagResMsg | 0 | Powertrain Diag Response | 0~7 | PtDiagResId | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | CAN, Event |
|  |  |  | 1 | Powertrain Diag Response | 8~11 | PtDiagStatus | Rx |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x310 | frmThermalMgmtStateMsg | 0 | Thermal Management | 0~2 | ThermalMode |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Thermal Management | 8~15 | FanSpeedCmd |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x311 | frmEnergyFlowStateMsg | 0 | Energy Flow Check | 0~3 | RegenLevel |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 0 | Energy Flow Check | 4~5 | EnergyFlowDir |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
| Powertrain CAN | 0x312 | frmPowertrainCtrlAuthMsg | 0 | Powertrain Control Auth | 0~1 | PtCtrlAuthState |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  | CAN, 100ms |
|  |  |  | 1 | Powertrain Control Auth | 8~11 | PtCtrlSource |  |  |  | Tx |  |  |  |  |  |  |  |  |  |  |  | Rx | Rx |  |  |  |  |  |  |  |  |  |
---

## 하단 보강표 (감사/추적 전용)

- 상단 공식 표준 양식은 변경하지 않고 유지한다.
- 아래 표들은 추적성/감사 해석 명확화를 위한 하단 보강 정보다.

---

## Flow 원본(Source of Truth) 매핑

| 계층 | 적용 Flow ID | 원본 파일(SoT) | 유지 규칙 |
|---|---|---|---|
| Core CAN Profile | Flow_001, Flow_002, Flow_003(CAN), Flow_007(CAN 0x210), Flow_008(CAN 0x220), Flow_009(CAN 0x230) | `canoe/databases/chassis_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/test_can.dbc` | 상단 공식표와 동일 ID/Signal 유지 |
| Core Ethernet Profile | Flow_001~Flow_008(Ethernet 구간) | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | E100/E200, 0x510/0x511/0x512 계약 우선 |
| Chassis Domain Profile | Flow_102, Flow_106(일부), Flow_105(헬스 연계), Flow_201 | `canoe/databases/chassis_can.dbc` | 0x100~0x121, 0x230~0x232 범위 준수 |
| Powertrain Domain Profile | Flow_101, Flow_105, Flow_204 | `canoe/databases/powertrain_can.dbc` | 0x300~0x312 범위 준수 |
| Body Domain Profile | Flow_103, Flow_105, Flow_202 | `canoe/databases/body_can.dbc` | 0x210~0x219, 0x240~0x24D 범위 준수 |
| Infotainment Domain Profile | Flow_104, Flow_105, Flow_203, Flow_205 | `canoe/databases/infotainment_can.dbc` | 0x110, 0x220~0x228, 0x260~0x26D 범위 준수 |

---

## 플로우 상세 추적 표 (Flow/Func/Req)

| Flow ID | Comm ID(0303 연계) | Func ID | Req ID | 관련 메시지(ID) | Tx Node | Rx Node | Channel | Period | Active Condition | Clear Condition |
|---|---|---|---|---|---|---|---|---|---|---|
| Flow_001 | Comm_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x100), ethVehicleStateMsg(0x510) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 | 경고 조건 해제 또는 입력 무효 |
| Flow_002 | Comm_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x101), ethSteeringMsg(0x511) | SIL_TEST_CTRL, CHASSIS_GW | CHASSIS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 | 조향 입력 검출 또는 경고 해제 |
| Flow_003 | Comm_003 | Func_007, Func_010 | Req_007, Req_010 | frmNavContextCanMsg(0x110), ethNavContextMsg(0x512) | SIL_TEST_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CONTEXT_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리/제한속도 입력 갱신 | 다음 컨텍스트 수신 시 갱신 |
| Flow_004 | Comm_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Police) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | Police_Active=1 | alertState=Clear 또는 송신 중지 |
| Flow_005 | Comm_005 | Func_018 | Req_018 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Ambulance) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | Ambulance_Active=1 | alertState=Clear 또는 송신 중지 |
| Flow_006 | Comm_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT(Rx), WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | EmergencyAlert 수신 또는 Zone 충돌 발생 | Clear 수신 또는 1000ms 무갱신 |
| Flow_007 | Comm_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_036, Req_037, Req_038, Req_039 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x210) | WARN_ARB_MGR, BODY_GW | BODY_GW, BCM_AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 | timeoutClear=1 또는 기본 상태 복귀 |
| Flow_008 | Comm_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x220) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 | alertState 해제 또는 문구 만료 |
| Flow_009 | Comm_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x230) | SIL_TEST_CTRL | SIL_TEST_CTRL(Log/Panel) | CAN | Event | 시나리오 실행 시작 | 판정 결과 기록 완료 (Validation-only) |
| Flow_120 | Comm_120 | Func_120 | Req_120 | ethEmergencyRiskMsg(0x313) | ADAS_WARN_CTRL | WARN_ARB_MGR, SIL_TEST_CTRL | Ethernet(UDP) | 100ms | emergencyDirection/ETA/vehicleSpeed 갱신 | 위험도 입력 무효 또는 긴급 해제 |
| Flow_121 | Comm_121 | Func_121 | Req_121 | ethDecelAssistReqMsg(0x314) | WARN_ARB_MGR | CHASSIS_GW, BRAKE_CTRL, SIL_TEST_CTRL | Ethernet(UDP) + CAN | Event + 50ms | proximityRiskLevel 임계 초과 | 임계 미만 또는 failSafeMode=1 |
| Flow_122 | Comm_122 | Func_122 | Req_122 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x210), frmClusterWarningMsg(0x220) | WARN_ARB_MGR | BODY_GW, IVI_GW, BCM_AMBIENT_CTRL, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | decelAssistReq=1 | decelAssistReq=0 또는 긴급 해제 |
| Flow_123 | Comm_123 | Func_123 | Req_123 | frmPedalInputCanMsg(0x102), frmSteeringCanMsg(0x101), ethDecelAssistReqMsg(0x314) | CHASSIS_GW, WARN_ARB_MGR | WARN_ARB_MGR, DOMAIN_GW_ROUTER, BRAKE_CTRL | CAN + Ethernet(UDP) | Event + 100ms | 운전자 제동/조향 회피 입력 검출 | decelAssistReq=0 전환 완료 |
| Flow_124 | Comm_124 | Func_124 | Req_124 | frmChassisHealthMsg(0x109), frmBodyHealthMsg(0x219), frmInfotainmentHealthMsg(0x228), ethFailSafeStateMsg(0x315) | CHASSIS_GW, BODY_GW, INFOTAINMENT_GW, DOMAIN_BOUNDARY_MGR | DOMAIN_BOUNDARY_MGR, DOMAIN_GW_ROUTER, WARN_ARB_MGR, BODY_GW, IVI_GW, SIL_TEST_CTRL | CAN + Ethernet(UDP) | 100ms + Event | domainPathStatus=FAILED 또는 forceFailSafe=1 | 경로 복구 + Health 정상화 |

---

## Flow_006 메시지 단계 분해 (감사용 명확화)

| 단계 | 상위 Flow ID | Message(ID) | Tx Node | Rx Node | 목적 |
|---|---|---|---|---|---|
| Ingress | Flow_006 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Police/Ambulance) | EMS_ALERT(Rx), WARN_ARB_MGR | 긴급 이벤트 수신/정규화 |
| Egress | Flow_006 | ethSelectedAlertMsg(0xE200) | WARN_ARB_MGR | BODY_GW, IVI_GW | 중재 결과 배포 |

- 주의: `Flow_006`은 긴급 수신(E100)과 중재 결과 배포(E200)를 하나의 논리 플로우로 묶은 항목이며, 감사 시에는 위 단계 표를 기준으로 해석한다.

### EMS 논리 단말-내부 모듈 매핑 (감사 보강)

| 논리 단말 | 내부 모듈 | 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 이벤트 송신 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 이벤트 송신 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 이벤트 수신/해제/타임아웃 |

### 표준명-별칭(g*) 매핑 (문서/코드 정합용)

| 표준 signal name(0302/0304) | 코드/런타임 별칭 |
|---|---|
| vehicleSpeed | gVehicleSpeed |
| driveState | gDriveState |
| steeringInput | SteeringInput |
| roadZone | gRoadZone |
| navDirection | gNavDirection |
| zoneDistance | gZoneDistance |
| speedLimit | gSpeedLimit |

---

## 도메인 네트워크 분리 기준 (확정)

| Domain Network | Gateway(경계 노드) | 대상 ECU/노드 | DBC 파일(정의) | ID 범위 | 연계 Flow |
|---|---|---|---|---|---|
| Core Integration CAN | CHASSIS_GW, INFOTAINMENT_GW, BODY_GW, IVI_GW | 경고 코어 체인 연계 노드 집합 | `canoe/databases/chassis_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/test_can.dbc` | 0x100/0x101/0x110/0x210/0x220/0x230 | Flow_001~Flow_009 |
| Chassis CAN | CHASSIS_GW | ACCEL_CTRL, BRAKE_CTRL, STEERING_CTRL, ADAS_WARN_CTRL 입력 경로 | `canoe/databases/chassis_can.dbc` | 0x100~0x121, 0x230~0x232 | Flow_001, Flow_002, Flow_102, Flow_106, Flow_201, Flow_121, Flow_123 |
| Powertrain CAN | DOMAIN_GW_ROUTER | ENGINE_CTRL, TRANSMISSION_CTRL | `canoe/databases/powertrain_can.dbc` | 0x300~0x312 | Flow_101, Flow_105, Flow_204 |
| Body CAN | BODY_GW | BCM_AMBIENT_CTRL, HAZARD_CTRL, WINDOW_CTRL, DRIVER_STATE_CTRL | `canoe/databases/body_can.dbc` | 0x210~0x219, 0x240~0x24D | Flow_007, Flow_103, Flow_105, Flow_202 |
| Infotainment CAN | INFOTAINMENT_GW, IVI_GW | NAV_CONTEXT_MGR, CLU_HMI_CTRL, CLUSTER_BASE_CTRL | `canoe/databases/infotainment_can.dbc` | 0x110, 0x220~0x228, 0x260~0x26D | Flow_003, Flow_008, Flow_104, Flow_105, Flow_203, Flow_205 |
| Ethernet UDP | ETH_SWITCH | EMS_ALERT(내부: EMS_POLICE_TX/EMS_AMB_TX/EMS_ALERT_RX), WARN_ARB_MGR, GW 집합 | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | 0x510/0x511/0x512/0xE100/0xE200 | Flow_004, Flow_005, Flow_006 |

---

## Vehicle Baseline 확장 Flow (확정)

| Flow ID | Comm ID(0303 연계) | Func ID | Req ID | 관련 메시지(ID) | 주 경로 | Period | 상태 |
|---|---|---|---|---|---|---|---|
| Flow_101 | Comm_101 | Func_101, Func_102 | Req_101, Req_102 | frmIgnitionEngineMsg(0x300), frmGearStateMsg(0x301), frmEngineSpeedTempMsg(0x303), frmTransmissionTempMsg(0x306) | Powertrain CAN(SIL_TEST_CTRL/ENGINE_CTRL/TRANSMISSION_CTRL) -> DOMAIN_GW_ROUTER | 100ms | Defined |
| Flow_102 | Comm_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | frmPedalInputCanMsg(0x102), frmSteeringStateCanMsg(0x103), frmBrakeStatusMsg(0x106), frmAccelStatusMsg(0x107), frmSteeringTorqueMsg(0x108) | Chassis CAN(SIL_TEST_CTRL/CHASSIS_GW/각 제어 ECU) | 100ms | Defined |
| Flow_103 | Comm_103 | Func_106, Func_107, Func_108 | Req_106, Req_107, Req_108 | frmHazardControlMsg(0x211), frmWindowControlMsg(0x212), frmDriverStateMsg(0x213), frmSeatBeltStateMsg(0x217), frmCabinAirStateMsg(0x218) | Body CAN(BODY_GW/HAZARD_CTRL/WINDOW_CTRL/DRIVER_STATE_CTRL) | 100ms | Defined |
| Flow_104 | Comm_104 | Func_109 | Req_109 | frmClusterBaseStateMsg(0x221), frmClusterThemeMsg(0x226), frmHmiPopupStateMsg(0x227) | Infotainment CAN(IVI_GW/CLUSTER_BASE_CTRL/CLU_HMI_CTRL) | 50ms | Defined |
| Flow_105 | Comm_105 | Func_110, Func_111 | Req_110, Req_111 | frmPowertrainGatewayMsg(0x302), frmVehicleModeMsg(0x307), frmPowerLimitMsg(0x308), frmCruiseStateMsg(0x309), frmChassisHealthMsg(0x109), frmBodyHealthMsg(0x219), frmInfotainmentHealthMsg(0x228) | Domain GW/Boundary 경로 상태 및 헬스 모니터 | 100ms | Defined |
| Flow_106 | Comm_106 | Func_112 | Req_112 | frmBaseTestResultMsg(0x231), frmTestResultMsg(0x230) | VEHICLE_BASE_TEST_CTRL/SIL_TEST_CTRL -> Test CAN 결과 기록 | Event | Defined (Validation-only) |

---

## Vehicle Baseline Phase-B 확장 Flow (Flow_201~Flow_205)

| Flow ID | Comm ID(0303 연계) | Func ID | Req ID | 관련 메시지(ID) | 주 경로 | Period | 상태 |
|---|---|---|---|---|---|---|---|
| Flow_201 | Comm_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | frmEpsStateMsg(0x10A), frmAbsStateMsg(0x10B), frmEscStateMsg(0x10C), frmTcsStateMsg(0x10D), frmBrakeTempMsg(0x10E), frmSteeringAngleMsg(0x10F), frmWheelPulseMsg(0x11A), frmSuspensionStateMsg(0x11B), frmTirePressureMsg(0x11C), frmChassisDiagReqMsg(0x11D), frmChassisDiagResMsg(0x11E), frmAdasChassisStatusMsg(0x11F), frmBrakeWearMsg(0x120), frmRoadFrictionMsg(0x121) | Chassis CAN(제어상태/노면상태/진단) -> CHASSIS_GW -> 도메인 연계 노드 | 100ms + Event | Defined |
| Flow_202 | Comm_202 | Func_106, Func_107, Func_108, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_108, Req_111, Req_113, Req_114, Req_115, Req_116, Req_117, Req_118 | frmHvacStateMsg(0x240), frmHvacActuatorMsg(0x241), frmMirrorStateMsg(0x242), frmSeatStateMsg(0x243), frmSeatControlMsg(0x244), frmDoorControlMsg(0x245), frmInteriorLightMsg(0x246), frmRainLightAutoMsg(0x247), frmBcmDiagReqMsg(0x248), frmBcmDiagResMsg(0x249), frmImmobilizerStateMsg(0x24A), frmAlarmStateMsg(0x24B), frmBodyGatewayStateMsg(0x24C), frmBodyComfortStateMsg(0x24D) | Body CAN(차체편의/실내환경/진단) -> BODY_GW -> 출력/상태 노드 | 100ms + Event | Defined |
| Flow_203 | Comm_203 | Func_109, Func_111, Func_119 | Req_109, Req_111, Req_119 | frmAudioFocusMsg(0x260), frmVoiceAssistStateMsg(0x261), frmMapRenderStateMsg(0x262), frmRouteAlertMsg(0x263), frmTrafficEventMsg(0x264), frmPhoneProjectionMsg(0x265), frmClusterNotifMsg(0x266), frmMediaMetaMsg(0x269), frmSpeechTtsStateMsg(0x26A), frmConnectivityStateMsg(0x26B), frmClusterSyncStateMsg(0x26D) | Infotainment CAN(안내/UI/연결상태) -> INFOTAINMENT_GW/IVI_GW -> NAV/HMI | 50/100ms | Defined |
| Flow_204 | Comm_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | frmEngineTorqueMsg(0x30B), frmEngineLoadMsg(0x30C), frmTransShiftStateMsg(0x30D), frmThermalMgmtStateMsg(0x310), frmEnergyFlowStateMsg(0x311), frmPowertrainCtrlAuthMsg(0x312) | Powertrain CAN(토크/열관리/변속상태) -> DOMAIN_GW_ROUTER -> 엔진/변속 노드 | 100ms | Defined |
| Flow_205 | Comm_205 | Func_112 | Req_112 | frmIviDiagReqMsg(0x267), frmIviDiagResMsg(0x268), frmIviHealthDetailMsg(0x26C), frmPtDiagReqMsg(0x30E), frmPtDiagResMsg(0x30F) | Test/Diag 경로(SIL_TEST_CTRL <-> 각 도메인 GW) | Event + 100ms | Defined (Validation-only) |

- 주의: `Flow_201~Flow_205`는 도메인 분리 DBC(`*_can.dbc`)와 동기화된 확정 플로우이며, 변경 시 0303/0304를 동일 커밋에서 함께 갱신한다.

## V2 확장 Flow (Implemented, Flow_120~Flow_124)

| Flow ID | Comm ID(0303 연계) | Func ID | Req ID | 관련 메시지(ID) | 주 경로 | Period | 상태 |
|---|---|---|---|---|---|---|---|
| Flow_120 | Comm_120 | Func_120 | Req_120 | ethEmergencyRiskMsg(0x313) | EMS_ALERT(Rx)/ADAS_WARN_CTRL -> WARN_ARB_MGR | 100ms | Implemented |
| Flow_121 | Comm_121 | Func_121 | Req_121 | ethDecelAssistReqMsg(0x314) | WARN_ARB_MGR -> CHASSIS_GW -> BRAKE_CTRL | Event + 50ms | Implemented |
| Flow_122 | Comm_122 | Func_122 | Req_122 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x210), frmClusterWarningMsg(0x220) | WARN_ARB_MGR -> BODY_GW/IVI_GW -> BCM_AMBIENT_CTRL/CLU_HMI_CTRL | 50ms | Implemented |
| Flow_123 | Comm_123 | Func_123 | Req_123 | frmPedalInputCanMsg(0x102), frmSteeringCanMsg(0x101), ethDecelAssistReqMsg(0x314) | CHASSIS_GW -> WARN_ARB_MGR -> DOMAIN_GW_ROUTER/BRAKE_CTRL | Event + 100ms | Implemented |
| Flow_124 | Comm_124 | Func_124 | Req_124 | frmChassisHealthMsg(0x109), frmBodyHealthMsg(0x219), frmInfotainmentHealthMsg(0x228), ethFailSafeStateMsg(0x315) | DOMAIN_BOUNDARY_MGR -> DOMAIN_GW_ROUTER -> WARN_ARB_MGR/BODY_GW/IVI_GW | 100ms + Event | Implemented |

- 주의: `Flow_120~Flow_124`는 V2 확장 구현 플로우다. 변경 시 0303/0304/05~07과 코드/DBC를 동일 커밋에서 동기화한다.

---

## 메시지/플로우 규모 목표 (현업 BP 기준)

| 프로파일 | 원본 파일 | 현재 정의 메시지 수 | ID 범위 |
|---|---|---|---|
| Chassis Domain CAN | `chassis_can.dbc` | 24 | 0x100~0x121, 0x230~0x232 |
| Powertrain Domain CAN | `powertrain_can.dbc` | 19 | 0x300~0x312 |
| Body Domain CAN | `body_can.dbc` | 24 | 0x210~0x219, 0x240~0x24D |
| Infotainment Domain CAN | `infotainment_can.dbc` | 24 | 0x110, 0x220~0x228, 0x260~0x26D |
| Test CAN | `test_can.dbc` | 3 | 0x230~0x232 |
| Ethernet Contract | `ETH_INTERFACE_CONTRACT.md` | 8 타입 | 0x510/0x511/0x512/0xE100/0xE200/0x313/0x314/0x315 |

| 항목 | 현재 정의(문서/원본) | 확장 목표(Phase-B) | 비고 |
|---|---|---|---|
| CAN Message | 94(도메인 확장 설계 기준) | 90~130 | 메시지 세분화 + 건강상태/진단 채널 확장 |
| Ethernet Message Type | 8 | 8~12 | UDP 계약 유지, 리스크/감속요청/Fail-safe 이벤트 포함 |
| Flow ID | 20(Flow_001~009,101~106,201~205) | 20+ | 서비스/기본기능 분리 유지 |
| ECU/노드 | 20+ | 24~32 | OEM 명칭 전환 시 식별자 유지 |

---

## 0303 연계 체크포인트

- 각 `Flow ID`는 `0303_Communication_Specification.md`의 `Comm ID`와 1:1로 연결한다.
- `selectedAlertLevel/selectedAlertType -> frmAmbientControlMsg(0x210)` 송신 Flow가 존재해야 한다.
- `selectedAlertLevel/selectedAlertType -> frmClusterWarningMsg(0x220)` 송신 Flow가 존재해야 한다.
- `ETH_EmergencyAlert(0xE100)` 송신/수신/해제 Flow가 존재해야 한다.
- 타임아웃(1000ms) 해제 Flow가 존재해야 한다.
- `ETH_SWITCH` 경유 신호가 `BODY_GW/IVI_GW`에서 CAN으로 분배되는 Flow가 존재해야 한다.
- `speedLimit` 신호가 `Flow_003/Comm_003`에서 `NAV_CONTEXT_MGR`와 `ADAS_WARN_CTRL`로 전달되어야 한다.
- `Req_101~Req_119`는 `Flow_101~Flow_106`, `Flow_201~Flow_205`에서 누락 없이 연결되어야 한다.
- `Req_120~Req_124`는 `Flow_120~Flow_124`로 구현 추적을 유지하고, 변경 시 0303/0304/05~07을 동일 커밋으로 동기화한다.

---

## 예외/장애 처리 규칙

| 장애 시나리오 | 감지 지점 | 처리 규칙 | 추적 링크 |
|---|---|---|---|
| CHASSIS_GW CAN->ETH 변환 실패 | CHASSIS_GW Tx watchdog | 마지막 정상값 1주기 유지 후 `WarningState` 강등, Fault 이벤트 기록 | Flow_001, Flow_002 / Comm_001, Comm_002 / Req_001, Req_011 |
| INFOTAINMENT_GW CAN->ETH 변환 실패 | INFOTAINMENT_GW Tx watchdog | `BaseZoneContext`를 일반구간으로 복귀하고 유도 경고 해제 | Flow_003 / Comm_003 / Req_007, Req_016 |
| EmergencyAlert 유실(1000ms 초과) | EMS_ALERT(Rx) timeout monitor | `timeoutClear=1` 생성 후 중재 결과 해제 전파 | Flow_006 / Comm_006 / Req_024 |
| BODY_GW CAN 송신 실패 | BODY_GW CAN Tx ack monitor | Ambient 출력을 안전 기본패턴으로 강등하고 재시도 3회 수행 | Flow_007 / Comm_007 / Req_033, Req_034 |
| IVI_GW CAN 송신 실패 | IVI_GW CAN Tx ack monitor | Cluster 경고코드를 최소 메시지(양보 안내)로 축소해 1회 재송신 | Flow_008 / Comm_008 / Req_040 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.14 | 2026-03-03 | V2 확장 플로우를 Implemented 상태로 전환하고 `Flow_120~124` 메시지 ID를 코드/DBC 실값(`0x313/0x314/0x315`) 및 실제 송수신 노드(`WARN_ARB_MGR` 중심)로 정정. |
| 3.13 | 2026-03-02 | 감사 정합 보강: 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구를 작성 원칙에 추가. |
| 3.12 | 2026-03-02 | V2 확장 제어 책임 분리 반영: `Flow_121/Flow_123`의 송신 노드를 `DECEL_ASSIST_CTRL`로 조정하고 Chassis CAN 경로 설명을 동기화. |
| 3.11 | 2026-03-02 | V2 확장(Pre-Activation) 반영: `Flow_120~Flow_124`(근접위험/감속보조/경고동기화/운전자개입해제/도메인단절강등) 추가 및 연계 체크포인트 보강. |
| 3.10 | 2026-03-02 | 0302/0303 최종 동기화 준비 반영: `Flow_201~Flow_205` 주의 문구를 병렬 작업 기준에서 DBC 동기화 운영 규칙으로 갱신. |
| 3.9 | 2026-03-02 | V2 추적 밀도 보강 1차: `Flow_202/Flow_203`의 Func/Req 매핑을 `Req_113~Req_119`, `Func_113~Func_119`까지 확장해 Body 확장 기능(HVAC/Seat/Mirror/Door/Wiper-Rain/Security) 및 Audio 상태 체인 정합을 반영. |
| 1.0 | 2026-02-23 | 초기 생성 |
| 2.0 | 2026-02-25 | 공식 표준 양식 기반으로 전면 재작성. CAN+Ethernet 범위 고정, OTA/UDS/DoIP 항목 제거, Flow/Func/Req 추적 표 추가 |
| 2.1 | 2026-02-25 | 공식 0302 표준 샘플 구조에 맞춰 상단 표를 재정렬하고, 하단 추적 표에 Comm 연계/메시지 ID/활성·해제 조건을 보강 |
| 2.2 | 2026-02-25 | 실문서 이관 시 Bit no. 행 단위(0/1/2...)로 확장 작성해야 함을 상단 공식표 하단 주석으로 추가 |
| 2.3 | 2026-02-25 | 옵션1 아키텍처(ETH_SWITCH + 도메인 GW + 도메인 CAN)로 네트워크 플로우 전면 통일 |
| 2.4 | 2026-02-25 | 상단 공식표 Bit no.를 개별 비트 행(0/1/2/...)으로 전개하고, GW/ETH/CAN 장애 처리 규칙 섹션 추가 |
| 2.5 | 2026-02-26 | Cluster 경고 메시지(0x220) 채널을 Infotainment CAN으로 정합화(IVI_GW -> CLU_HMI_CTRL 경로 기준) |
| 2.6 | 2026-02-26 | Flow_006 단계 분해 표(E100 Ingress / E200 Egress) 추가로 감사 해석 모호성 제거 |
| 2.7 | 2026-02-26 | 상단 공식표 비변경 원칙을 명시하고 하단 보강표 구역(감사/추적 전용)으로 분리 |
| 2.8 | 2026-02-26 | 상단 signal name을 0304 표준명(vehicleSpeed 등)으로 통일하고, g* 별칭은 하단 매핑표로 분리 |
| 2.9 | 2026-02-28 | signal 표기 케이스를 0304 표준명(`steeringInput/emergencyType/selectedAlertLevel` 등)으로 추가 정합, `SelectedAlertContext` 잔여 문구 제거 |
| 3.0 | 2026-02-28 | 스쿨존 과속 정밀 판정을 위해 `speedLimit` 신호를 0x110/0x512 상단 공식표와 Flow_003 하단 추적표에 반영. |
| 3.1 | 2026-02-28 | CAN/Ethernet 원본 파일 분리 원칙을 명시하고 Flow Source-of-Truth 매핑 표를 추가. |
| 3.2 | 2026-02-28 | DBC 병렬 작업용 도메인 네트워크 분리 설계표와 Vehicle Baseline 확장 Flow 계획(Flow_101~106)을 추가. |
| 3.3 | 2026-02-28 | Flow_101~106을 확정 상태(Defined)로 전환하고, 현업 기준 메시지/플로우 규모 목표(80~120 CAN 메시지)를 명시. |
| 3.4 | 2026-02-28 | 도메인 분리 DBC(`emergency_system_*`) 기준으로 Flow_101~106 메시지 번들을 실 ID로 확정하고, SoT/규모 기준을 실제 원본 수치(44 CAN + 5 ETH)로 갱신. |
| 3.5 | 2026-02-28 | 상단 공식표를 실메시지 기준(49 Message / 131 Signal)으로 확장하고, Bit no.를 범위 표기(`0~7`)로 정렬해 도메인별 통신 상세를 반영. |
| 3.6 | 2026-02-28 | 상단 공식표를 Phase-B 확장 포함(99 Message / 242 Signal)으로 보강하고 Flow_201~205/Comm_201~205를 추가해 현업형 메시지 규모(100+) 기준에 맞춤. |
| 3.7 | 2026-02-28 | SoT 경로를 실제 분리 DBC 파일명(`*_can.dbc`)으로 정합화하고, 도메인별 ID 범위 표기를 Phase-B 확장 범위와 일치하도록 통일. |
| 3.8 | 2026-03-01 | 멘토 피드백 반영: EMS를 논리 단말(`EMS_ALERT`) 기준으로 Flow/도메인표에 통합 표기하고, 내부 TX/RX 모듈은 하단 보강 매핑으로 분리. |

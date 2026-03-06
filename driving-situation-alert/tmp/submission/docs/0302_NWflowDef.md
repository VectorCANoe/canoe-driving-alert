# 네트워크 플로우 정의 (Network Flow Definition)

**Document ID**: PROJ-0302-NFD
**ISO 26262 Reference**: Part 4, Cl.7 (System Design)
**ASPICE Reference**: SYS.3 (System Architectural Design)
**Version**: 3.23
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 중단 (SYS.3) | `0302_NWflowDef.md` | `0301_SysFuncAnalysis.md` | `0303_Communication_Specification.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 상단 표는 공식 표준 양식(`Channel/ID hex/Symbolic Name/Byte/Function/Bit/signal/노드 TxRx`) 구조를 유지한다.
- 상단 표의 `Bit no.`는 가독성을 위해 범위 표기(예: `0~7`, `8~15`)를 사용하되, 상단 열 구성은 공식 샘플 구조를 유지한다.
- 상단 표의 `signal name`은 0304 표준 변수명(`vehicleSpeed` 등) 기준으로 작성하고, 코드/런타임 별칭(`g*`)은 하단 보강표에서만 관리한다.
- 0304에 아직 등재되지 않은 Vehicle Baseline 확장 신호는 DBC 원본 신호명(`AccelPedal`, `DriveMode` 등)으로 표기한다.
- 옵션1 아키텍처를 고정한다: `중앙 경고코어 + Ethernet 백본(ETH_SW) + 도메인 게이트웨이 + 도메인 CAN`.
- 상세 추적 정보(`Flow/Func/Req/주기/활성/해제`)는 하단 표에 분리한다.
- CAN 신호 원본은 계층 분리로 관리한다: 도메인 프로파일은 `canoe/databases/chassis_can.dbc`, `canoe/databases/powertrain_can.dbc`, `canoe/databases/body_can.dbc`, `canoe/databases/infotainment_can.dbc`, `canoe/databases/adas_can.dbc`, `canoe/databases/eth_backbone_can_stub.dbc`를 사용하고, Validation 결과 프레임(`0x2A5`,`0x2A6`)은 `chassis_can.dbc`에 통합 관리한다. Ethernet 논리 계약은 `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`를 사용한다.
- 검증 범위는 CANoe SIL, CAN + Ethernet(UDP)만 사용한다.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- CANoe.CAN 환경에서는 E100/E200 모니터링 경로와 V2 확장 경로 일부를 `eth_backbone_can_stub.dbc`(0x1C0/0x1C2/0x1C4/0x111)와 `adas_can.dbc`(0x1C1/0x1C3)로 분리 대체 운반한다.
- OTA/UDS/DoIP 관련 플로우는 본 문서 범위에서 제외한다.
- `Flow_009`, `Flow_106`, `Flow_205`는 Validation Harness 경로(검증 전용)이며 양산 서비스 플로우와 구분한다.
- 제출 전 현대/기아 및 OEM 기준으로 설명/별칭은 정리하되, Flow/Comm/ID/signal 식별자는 SoT 기준으로 고정 유지한다.
- ID notation rule (fixed): document primary references use Logical IDs (0xE210/0xE211/0xE212); CANoe SIL execution uses Stub IDs (0x1C3/0x1C4/0x111) per canoe/docs/operations/ETH_INTERFACE_CONTRACT.md.

- Vehicle Baseline(Req_101~Req_107, Req_109~Req_119) 플로우(`Flow_101~Flow_106`, `Flow_201~Flow_205`)는 본 문서에서 확정 정의하고, DBC는 이 정의를 구현 대상으로 사용한다.
- V2 확장 요구(`Req_120~Req_121`, `Req_123`, `Req_125~Req_129`) 플로우(`Flow_120~Flow_124`)는 구현 활성 상태로 관리하며, 관련 DBC/코드/테스트를 동일 커밋에서 동기화한다.
- ADAS 객체 인지 확장 요구(`Req_130~Req_139`) 플로우(`Flow_130~Flow_133`)는 Pre-Activation(설계 선반영) 상태로 관리하며, 구현 착수 시 0303/0304/04/05/06/07을 동일 커밋에서 동기화한다.
- `Flow_130~Flow_133` 활성 SoT 승격 조건은 `ETH_INTERFACE_CONTRACT.md v1.2`에 `E213~E216` 계약이 반영되는 것이다.
- EMS는 상위 문서 레벨에서 논리 단말 `EMS_ALERT`로 표기하고, 상단 표의 `EMS_POLICE_TX/EMS_AMB_TX/EMS_ALERT_RX` 열은 내부 구현 모듈 분해 관점으로만 해석한다.
- 약어 충돌 방지 규칙: `EMS_AMB_TX`의 `AMB`는 `Ambulance` 의미의 구현 literal이며, `Ambient`는 항상 `AMBIENT` 풀토큰으로 표기한다.
- `Req_108`은 Legacy 참조 요구로 관리하며 `Flow_202/Flow_105` 통합 결과를 상속 추적한다.

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

## Flow 원본(Source of Truth) 매핑

| 계층 | 적용 Flow ID | 원본 파일(SoT) | 유지 규칙 |
|---|---|---|---|
| Core CAN Profile | Flow_001, Flow_002, Flow_003(CAN), Flow_007(CAN 0x289), Flow_008(CAN 0x280), Flow_009(CAN 0x2A5) | `canoe/databases/chassis_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` | 상단 공식표와 동일 ID/Signal 유지(CAN-stub 포함) |
| Core Ethernet Profile | Flow_001~Flow_008(Ethernet 구간) | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | E100/E200, 0x510/0x511/0x512 계약 우선 |
| Chassis Domain Profile | Flow_102, Flow_106(일부), Flow_105(헬스 연계), Flow_201 | `canoe/databases/chassis_can.dbc` | 0x122~0x2A0(0x1C1 제외) 범위 준수 |
| ADAS Domain CAN Profile | Flow_120, Flow_201(일부) | `canoe/databases/adas_can.dbc` | 0x1C1/0x1C3 범위 준수 (ADAS 소유 프레임) |
| ETH Backbone CAN Stub Profile | Flow_004, Flow_005, Flow_006, Flow_121, Flow_124 | `canoe/databases/eth_backbone_can_stub.dbc` | 0x1C0/0x1C2/0x1C4/0x111 범위 준수 |
| ADAS Object Extension Profile (Pending) | Flow_130~Flow_133 | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` (v1.2 예정) | Pre-Activation, `E213~E216` 계약 반영 전에는 활성 SoT로 사용하지 않음 |
| Powertrain Domain Profile | Flow_101, Flow_105, Flow_204 | `canoe/databases/powertrain_can.dbc` | 0x110~0x2A8 범위 준수 |
| Body Domain Profile | Flow_103, Flow_105, Flow_202 | `canoe/databases/body_can.dbc` | 0x289~0x291, 0x277~0x292 범위 준수 |
| Infotainment Domain Profile | Flow_104, Flow_105, Flow_203, Flow_205 | `canoe/databases/infotainment_can.dbc` | 0x2A3, 0x280~0x288, 0x289~0x295 범위 준수 |

---

## 플로우 상세 추적 표 (Flow/Func/Req)

| Flow ID | Comm ID(0303 연계) | Func ID | Req ID | 관련 메시지(ID) | Tx Node | Rx Node | Channel | Period | Active Condition | Clear Condition |
|---|---|---|---|---|---|---|---|---|---|---|
| Flow_001 | Comm_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x2A0), ethVehicleStateMsg(0x510) | VAL_SCENARIO_CTRL, CHS_GW | CHS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 | 경고 조건 해제 또는 입력 무효 |
| Flow_002 | Comm_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x2A1), ethSteeringMsg(0x511) | VAL_SCENARIO_CTRL, CHS_GW | CHS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 | 조향 입력 검출 또는 경고 해제 |
| Flow_003 | Comm_003 | Func_007, Func_010 | Req_007, Req_010 | frmNavContextCanMsg(0x2A3), ethNavContextMsg(0x512) | VAL_SCENARIO_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리/제한속도 입력 갱신 | 다음 컨텍스트 수신 시 갱신 |
| Flow_004 | Comm_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Police) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | Police_Active=1 | alertState=Clear 또는 송신 중지 |
| Flow_005 | Comm_005 | Func_018 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Ambulance) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | Ambulance_Active=1 | alertState=Clear 또는 송신 중지 |
| Flow_006 | Comm_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032, Func_144, Func_149, Func_150, Func_152 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032, Req_144, Req_149, Req_150, Req_152 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT(Rx), WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | EmergencyAlert 수신 또는 Zone 충돌 발생 | Clear 수신 또는 1000ms 무갱신 |
| Flow_007 | Comm_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039, Func_152 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_037, Req_152 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260) | WARN_ARB_MGR, BODY_GW | BODY_GW, AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 | timeoutClear=1 또는 기본 상태 복귀 |
| Flow_008 | Comm_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040, Func_143, Func_152, Func_155 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040, Req_143, Req_152, Req_155 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x280) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 | alertState 해제 또는 문구 만료 |
| Flow_009 | Comm_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x2A5) | VAL_SCENARIO_CTRL | VAL_SCENARIO_CTRL(Log/Panel) | CAN | Event | 시나리오 실행 시작 | 판정 결과 기록 완료 (Validation-only) |
| Flow_120 | Comm_120 | Func_120 | Req_120 | ethEmergencyRiskMsg(0x1C3) | ADAS_WARN_CTRL | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | 100ms | emergencyDirection/ETA/vehicleSpeed 갱신 | 위험도 입력 무효 또는 긴급 해제 |
| Flow_121 | Comm_121 | Func_121 | Req_121 | ethDecelAssistReqMsg(0x1C4) | WARN_ARB_MGR | CHS_GW, BRK_CTRL, VAL_SCENARIO_CTRL | Ethernet(UDP) + CAN | Event + 50ms | proximityRiskLevel 임계 초과 | 임계 미만 또는 failSafeMode=1 |
| Flow_122 | Comm_122 | Func_125,Func_126 | Req_125,Req_126 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260), frmClusterWarningMsg(0x280) | WARN_ARB_MGR | BODY_GW, IVI_GW, AMBIENT_CTRL, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | decelAssistReq=1 | decelAssistReq=0 또는 긴급 해제 |
| Flow_123 | Comm_123 | Func_123 | Req_123 | frmPedalInputCanMsg(0x2A2), frmSteeringCanMsg(0x2A1), ethDecelAssistReqMsg(0x1C4) | CHS_GW, WARN_ARB_MGR | WARN_ARB_MGR, DOMAIN_ROUTER, BRK_CTRL | CAN + Ethernet(UDP) | Event + 100ms | 운전자 제동/조향 회피 입력 검출 | decelAssistReq=0 전환 완료 |
| Flow_124 | Comm_124 | Func_127,Func_128,Func_129,Func_151,Func_152 | Req_127,Req_128,Req_129,Req_151,Req_152 | frmChassisHealthMsg(0x103), frmBodyHealthMsg(0x269), frmInfotainmentHealthMsg(0x288), ethFailSafeStateMsg(0x111) | CHS_GW, BODY_GW, INFOTAINMENT_GW, DOMAIN_BOUNDARY_MGR | DOMAIN_BOUNDARY_MGR, DOMAIN_ROUTER, WARN_ARB_MGR, BODY_GW, IVI_GW, VAL_SCENARIO_CTRL | CAN + Ethernet(UDP) | 100ms + Event | domainPathStatus=FAILED 또는 forceFailSafe=1 | 경로 복구 + Health 정상화 |
| Flow_130 | Comm_130 | Func_130,Func_131,Func_148 | Req_130,Req_131,Req_148 | ethObjectRiskInputMsg(0xE213) | CHS_GW, INFOTAINMENT_GW | ADAS_WARN_CTRL | Ethernet(UDP) | 100ms | 객체 목록/자차 상태 갱신 | 객체 입력 무효 또는 유효 객체 0건 |
| Flow_131 | Comm_131 | Func_132,Func_133,Func_136 | Req_132,Req_133,Req_136 | ethObjectRiskStateMsg(0xE214) | ADAS_WARN_CTRL | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | 100ms + Event | TTC/상대속도/거리 기반 위험도 갱신 | TTC 임계 해제 + 유지시간 만료 |
| Flow_132 | Comm_132 | Func_134,Func_135,Func_139 | Req_134,Req_135,Req_139 | ethObjectScenarioAlertMsg(0xE215), frmAmbientControlMsg(0x260), frmClusterWarningMsg(0x280) | WARN_ARB_MGR | BODY_GW, IVI_GW, AMBIENT_CTRL, CLU_HMI_CTRL | Ethernet(UDP) + CAN | Event + 50ms | 교차로/합류 위험 조건 성립 | 조건 해제 또는 긴급 우선 경고 전환 |
| Flow_133 | Comm_133 | Func_137,Func_138,Func_148 | Req_137,Req_138,Req_148 | ethObjectSafetyStateMsg(0xE216) | DOMAIN_BOUNDARY_MGR, EMS_ALERT | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | Event | 객체 신뢰도 저하 또는 이벤트 발생 | 신뢰도 회복 + 이벤트 기록 완료 |

---

## 하단 확장표 축소 (제출본)

- 상단 공식 플로우 표와 `플로우 상세 추적 표`를 제출 기준 본표로 유지한다.
- 도메인별/단계별 확장 분해표는 중복을 줄이기 위해 요약만 남긴다.
- 상세 전수 매핑은 원문 SoT(`driving-situation-alert/0302_NWflowDef.md`)를 기준으로 관리한다.

| 구분 | 제출본 유지 내용 | 원문 SoT 참조 |
|---|---|---|
| 도메인 네트워크 분리 | Core/Domain 분리 원칙 + 주요 경로 요약 | 0302 원문 `도메인 네트워크 분리 기준` |
| Vehicle Baseline 확장 | Flow_101~106, Flow_201~205는 `Defined` 상태로 유지 | 0302 원문 Baseline/Phase-B 확장 표 |
| V2 확장 | Flow_120~124는 `Implemented` 상태로 유지 | 0302 원문 V2 확장 표 |
| ADAS 객체 인지 확장 | Flow_130~133는 `Planned(Pre-Activation)` 상태로 유지 | 0302 원문 ADAS 확장 표 |
| 동기화 규칙 | 변경 시 0303/0304/04/05/06/07 동시 반영 | TMP_HANDOFF + 원문 체인 |

---

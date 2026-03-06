# 통신 명세서 (Communication Specification)

**Document ID**: PROJ-0303-CS
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 (Software Architectural Design)
**Version**: 3.21
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2) | `0303_Communication_Specification.md` | `0302_NWflowDef.md` | `0304_System_Variables.md` |

---

## 작성 원칙

- 상단 표는 공식 샘플(`0303.md`)과 동일하게 `Message/Identifier/DLC/Signal/signal bit position/Data 설명/Data 범위/Data 사용` 열만 사용한다.
- `Identifier`는 순수 ID 값만 기재한다(예: `0x2A0`, `0xE100`).
- `DLC`는 순수 숫자만 기재한다.
- 상단 표의 `Signal`은 0304 표준 변수명(`vehicleSpeed` 등) 기준으로 작성하고, 코드/런타임 별칭(`g*`)은 하단 보강표에서만 관리한다.
- 0304에 아직 등재되지 않은 Vehicle Baseline 확장 신호는 DBC 원본 신호명(`AccelPedal`, `DriveMode` 등)으로 표기한다.
- CAN 통신 원본은 계층 분리로 관리한다: 도메인 프로파일은 `canoe/databases/chassis_can.dbc`, `canoe/databases/powertrain_can.dbc`, `canoe/databases/body_can.dbc`, `canoe/databases/infotainment_can.dbc`, `canoe/databases/adas_can.dbc`, `canoe/databases/eth_backbone_can_stub.dbc`를 사용하고, Validation 결과 프레임(`0x2A5`,`0x2A6`)은 `chassis_can.dbc`에 통합 관리한다. Ethernet 논리 계약은 `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`를 사용한다.
- 본 설계는 Ethernet 백본(`ETH_SW`) + 도메인 게이트웨이(`CHS_GW`, `INFOTAINMENT_GW`, `BODY_GW`, `IVI_GW`) + 도메인 CAN 분배 구조를 사용한다.
- 하단 추적표는 `Comm ID -> Flow ID -> Func ID -> Req ID`를 유지한다.
- 제출 전 현대/기아 및 OEM 기준으로 설명/별칭은 정리하되, Message ID/DLC/Bit Position/Signal 식별자는 SoT 기준으로 고정 유지한다.
- Message ID notation rule (fixed): architecture references use Logical IDs (0xE210/0xE211/0xE212) as primary; CANoe SIL implementation/test uses Stub IDs (0x1C3/0x1C4/0x111) per canoe/docs/operations/ETH_INTERFACE_CONTRACT.md.

- 검증 범위는 CANoe SIL, CAN + Ethernet(UDP)로 고정한다.
- 목표 설계는 옵션1(ETH 백본) 고정이며, CANoe.CAN 라이선스 제약 구간의 SIL 검증은 임시로 CAN 대체 백본을 사용하고 Ethernet 라이선스 확보 후 동일 케이스로 재검증한다.
- CANoe.CAN 환경에서는 Ethernet 일부 경로(E100/E200 모니터링 및 V2 확장)를 `eth_backbone_can_stub.dbc`(0x1C0/0x1C2/0x1C4/0x111)와 `adas_can.dbc`(0x1C1/0x1C3)로 분리 대체 운반한다.
- `Comm_009`, `Comm_106`, `Comm_205`는 Validation Harness 통신(검증 전용)이며 양산 통신과 구분한다.
- Vehicle Baseline(Req_101~Req_107, Req_109~Req_119) 통신(`Comm_101~Comm_106`, `Comm_201~Comm_205`)은 본 문서에서 확정 정의하고, 도메인 DBC는 이 정의를 구현 대상으로 사용한다.
- V2 확장 요구(`Req_120~Req_121`, `Req_123`, `Req_125~Req_129`) 통신(`Comm_120~Comm_124`)은 구현 활성 상태로 관리하며, DBC/코드/테스트를 동일 커밋에서 동기화한다.
- EMS는 상위 문서 레벨에서 논리 단말 `EMS_ALERT`로 표기하고, 내부 구현 모듈(`EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`)은 하단 보강표에서만 분리 관리한다.
- 약어 충돌 방지 규칙: `EMS_AMB_TX`의 `AMB`는 `Ambulance` 의미의 구현 literal이며, `Ambient`는 항상 `AMBIENT` 풀토큰으로 표기한다.
- Validation Harness 공통 프레임(`0x2A5`, `0x2A6`)은 독립 `test_can`이 아니라 `chassis_can.dbc`에 통합 관리한다.
- 제출 설명 시 `0x2A5/0x2A6`은 “Validation frame(Chassis 통합)”으로 명시해 도메인 오해를 방지한다.

---

## CAN ID 배정 정책 (Project SoT)

- ID 상위 SoT는 `00f_CAN_ID_Allocation_Standard.md`를 따른다.
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

## 하단 보강표 (감사/추적 전용)

- 상단 공식 표준 양식은 변경하지 않고 유지한다.
- 아래 표들은 추적성/감사 해석 명확화를 위한 하단 보강 정보다.

---

## 통신 원본(Source of Truth) 매핑

| 구분 | 범위 | 원본 파일 | 비고 |
|---|---|---|---|
| Core CAN Profile | Comm_001, Comm_002, Comm_003, Comm_007, Comm_008, Comm_009 | `canoe/databases/chassis_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` | 경고 코어 체인 단일 원본(CAN-stub 포함) |
| Domain CAN Profile | Comm_101~Comm_106, Comm_201~Comm_205 | `canoe/databases/chassis_can.dbc` + `canoe/databases/powertrain_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` | 차량 기본 기능/도메인 분리 원본(CAN-stub 포함) |
| ADAS CAN Profile | Comm_120, Comm_201(일부) | `canoe/databases/adas_can.dbc` | ADAS 소유 프레임 원본 |
| ETH Stub Transport Profile | Comm_004, Comm_005, Comm_006, Comm_121, Comm_124 | `canoe/databases/eth_backbone_can_stub.dbc` | CANoe.CAN 환경 대체 운반 원본 |
| Ethernet Profile (Logical Contract) | Comm_004, Comm_005, Comm_006, Comm_120, Comm_121, Comm_124 (및 Comm_001~003/007~008의 ETH 구간) | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | UDP 계약 단일 원본 |

---

## 통신 상세 추적 표 (Comm/Flow/Func/Req)

| Comm ID | Flow ID | Func ID | Req ID | Message(ID) | Tx Node | Rx Node | Protocol | Period | Clear/비고 |
|---|---|---|---|---|---|---|---|---|---|
| Comm_001 | Flow_001 | Func_001, Func_002, Func_003, Func_004, Func_006, Func_010 | Req_001, Req_002, Req_003, Req_004, Req_006, Req_010 | frmVehicleStateCanMsg(0x2A0), ethVehicleStateMsg(0x510) | VAL_SCENARIO_CTRL, CHS_GW | CHS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 속도/주행상태 입력 갱신 |
| Comm_002 | Flow_002 | Func_011, Func_012 | Req_011, Req_012 | frmSteeringCanMsg(0x2A1), ethSteeringMsg(0x511) | VAL_SCENARIO_CTRL, CHS_GW | CHS_GW, ADAS_WARN_CTRL | CAN + Ethernet(UDP) | 100ms | 조향 입력 갱신 |
| Comm_003 | Flow_003 | Func_007, Func_010 | Req_007, Req_010 | frmNavContextCanMsg(0x2A3), ethNavContextMsg(0x512) | VAL_SCENARIO_CTRL, INFOTAINMENT_GW | INFOTAINMENT_GW, NAV_CTX_MGR, ADAS_WARN_CTRL, WARN_ARB_MGR | CAN + Ethernet(UDP) | 100ms | 구간/방향/거리/제한속도 입력 갱신 |
| Comm_004 | Flow_004 | Func_017 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Police) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_005 | Flow_005 | Func_018 | Req_017 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Ambulance) | EMS_ALERT(Rx) | Ethernet(UDP) | 100ms | alertState=Clear 또는 송신 중지 |
| Comm_006 | Flow_006 | Func_022, Func_023, Func_024, Func_025, Func_027, Func_028, Func_029, Func_030, Func_031, Func_032 | Req_022, Req_023, Req_024, Req_025, Req_027, Req_028, Req_029, Req_030, Req_031, Req_032 | ETH_EmergencyAlert(0xE100), ethSelectedAlertMsg(0xE200) | EMS_ALERT(Rx), WARN_ARB_MGR | WARN_ARB_MGR, BODY_GW, IVI_GW | Ethernet(UDP) | Event + 50ms | 1000ms 무갱신 시 timeoutClear=1 |
| Comm_007 | Flow_007 | Func_008, Func_009, Func_013, Func_014, Func_015, Func_016, Func_033, Func_034, Func_035, Func_036, Func_037, Func_038, Func_039 | Req_008, Req_009, Req_013, Req_014, Req_015, Req_016, Req_033, Req_034, Req_035, Req_037 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260) | WARN_ARB_MGR, BODY_GW | BODY_GW, AMBIENT_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_008 | Flow_008 | Func_005, Func_019, Func_020, Func_021, Func_026, Func_040 | Req_005, Req_019, Req_020, Req_021, Req_026, Req_040 | ethSelectedAlertMsg(0xE200), frmClusterWarningMsg(0x280) | WARN_ARB_MGR, IVI_GW | IVI_GW, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | selectedAlertLevel/selectedAlertType 수신 |
| Comm_009 | Flow_009 | Func_041, Func_042, Func_043 | Req_041, Req_042, Req_043 | frmTestResultMsg(0x2A5) | VAL_SCENARIO_CTRL | VAL_SCENARIO_CTRL(Log/Panel) | CAN | Event | 판정 결과 기록 완료 시 종료 |
| Comm_120 | Flow_120 | Func_120 | Req_120 | ethEmergencyRiskMsg(0x1C3) | ADAS_WARN_CTRL | WARN_ARB_MGR, VAL_SCENARIO_CTRL | Ethernet(UDP) | 100ms | 근접위험 산정 프레임 |
| Comm_121 | Flow_121 | Func_121 | Req_121 | ethDecelAssistReqMsg(0x1C4) | WARN_ARB_MGR | CHS_GW, BRK_CTRL, VAL_SCENARIO_CTRL | Ethernet(UDP) + CAN | Event + 50ms | 감속 보조 요청 프레임 |
| Comm_122 | Flow_122 | Func_125, Func_126 | Req_125, Req_126 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260), frmClusterWarningMsg(0x280) | WARN_ARB_MGR | BODY_GW, IVI_GW, AMBIENT_CTRL, CLU_HMI_CTRL | Ethernet(UDP) + CAN | 50ms | 감속 보조 활성 경고 동기화 |
| Comm_123 | Flow_123 | Func_123 | Req_123 | frmPedalInputCanMsg(0x2A2), frmSteeringCanMsg(0x2A1), ethDecelAssistReqMsg(0x1C4) | CHS_GW, WARN_ARB_MGR | WARN_ARB_MGR, DOMAIN_ROUTER, BRK_CTRL | CAN + Ethernet(UDP) | Event + 100ms | 운전자 개입 시 보조 해제 |
| Comm_124 | Flow_124 | Func_127, Func_128, Func_129 | Req_127, Req_128, Req_129 | frmChassisHealthMsg(0x103), frmBodyHealthMsg(0x269), frmInfotainmentHealthMsg(0x288), ethFailSafeStateMsg(0x111) | CHS_GW, BODY_GW, INFOTAINMENT_GW, DOMAIN_BOUNDARY_MGR | DOMAIN_BOUNDARY_MGR, DOMAIN_ROUTER, WARN_ARB_MGR, BODY_GW, IVI_GW, VAL_SCENARIO_CTRL | CAN + Ethernet(UDP) | 100ms + Event | 경로 단절 강등/보조 금지 |

---

## Comm_006 메시지 단계 분해 (감사용 명확화)

| 단계 | 상위 Comm ID | Message(ID) | Tx Node | Rx Node | 주기/조건 |
|---|---|---|---|---|---|
| Ingress | Comm_006 | ETH_EmergencyAlert(0xE100) | EMS_ALERT(Tx:Police/Ambulance) | EMS_ALERT(Rx) | 100ms, Active/Clear |
| Egress | Comm_006 | ethSelectedAlertMsg(0xE200) | WARN_ARB_MGR | BODY_GW, IVI_GW | Event + 50ms |

- 주의: `Comm_006`은 입력(E100)과 출력(E200) 단계를 묶은 논리 Comm이며, 감사 시에는 위 단계 표를 기준으로 `Rx/Tx`를 분리 해석한다.

### EMS 논리 단말-내부 모듈 매핑 (감사 보강)

| 논리 단말 | 내부 모듈 | 역할 |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX | 경찰 긴급 이벤트 송신 |
| EMS_ALERT | EMS_AMB_TX | 구급 긴급 이벤트 송신 |
| EMS_ALERT | EMS_ALERT_RX | 긴급 이벤트 수신/해제/타임아웃 |

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

## 도메인별 통신 원본 확장 정의 (DBC 동기화 기준)

| Domain | 원본 파일(정의) | Comm 범위 | 핵심 Message |
|---|---|---|---|
| Core Integration CAN | `canoe/databases/chassis_can.dbc` + `canoe/databases/infotainment_can.dbc` + `canoe/databases/body_can.dbc` + `canoe/databases/adas_can.dbc` + `canoe/databases/eth_backbone_can_stub.dbc` | Comm_001, Comm_002, Comm_003, Comm_007, Comm_008, Comm_009 | frmVehicleStateCanMsg, frmSteeringCanMsg, frmNavContextCanMsg, frmAmbientControlMsg, frmClusterWarningMsg, frmTestResultMsg, frmEmergencyBroadcastMsg |
| Chassis CAN | `canoe/databases/chassis_can.dbc` | Comm_001, Comm_002, Comm_102, Comm_105(헬스), Comm_201 | frmVehicleStateCanMsg, frmSteeringCanMsg, frmPedalInputCanMsg, frmBrakeStatusMsg, frmAccelStatusMsg, frmSteeringTorqueMsg, frmEpsStateMsg, frmAbsStateMsg |
| ADAS CAN | `canoe/databases/adas_can.dbc` | Comm_120, Comm_201(일부) | frmAdasChassisStatusMsg, ethEmergencyRiskMsg |
| ETH Backbone CAN Stub | `canoe/databases/eth_backbone_can_stub.dbc` | Comm_004, Comm_005, Comm_006, Comm_121, Comm_124 | frmEmergencyBroadcastMsg, frmEmergencyMonitorMsg, ethDecelAssistReqMsg, ethFailSafeStateMsg |
| Powertrain CAN | `canoe/databases/powertrain_can.dbc` | Comm_101, Comm_105, Comm_204 | frmIgnitionEngineMsg, frmGearStateMsg, frmPowertrainGatewayMsg, frmEngineSpeedTempMsg, frmPowerLimitMsg, frmCruiseStateMsg, frmEngineTorqueMsg, frmEngineLoadMsg |
| Body CAN | `canoe/databases/body_can.dbc` | Comm_007, Comm_103, Comm_105, Comm_202 | frmAmbientControlMsg, frmHazardControlMsg, frmWindowControlMsg, frmBodyHealthMsg, frmHvacStateMsg, frmMirrorStateMsg |
| Infotainment CAN | `canoe/databases/infotainment_can.dbc` | Comm_003, Comm_008, Comm_104, Comm_105, Comm_203, Comm_205 | frmNavContextCanMsg, frmClusterWarningMsg, frmClusterBaseStateMsg, frmClusterThemeMsg, frmHmiPopupStateMsg, frmInfotainmentHealthMsg, frmAudioFocusMsg, frmMapRenderStateMsg |
| Ethernet UDP | `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md` | Comm_004, Comm_005, Comm_006, Comm_120, Comm_121, Comm_124 | ethVehicleStateMsg, ethSteeringMsg, ethNavContextMsg, ETH_EmergencyAlert, ethSelectedAlertMsg, ethEmergencyRiskMsg, ethDecelAssistReqMsg, ethFailSafeStateMsg |

---

## Vehicle Baseline 확장 Comm 정의 (Comm_101~Comm_106)

| Comm ID | Flow ID(0302 연계) | Func ID | Req ID | Message(ID) | Protocol | 주기 |
|---|---|---|---|---|---|---|
| Comm_101 | Flow_101 | Func_101, Func_102 | Req_101, Req_102 | frmIgnitionEngineMsg(0x2A8), frmGearStateMsg(0x2A9), frmEngineSpeedTempMsg(0x12A), frmTransmissionTempMsg(0x12D) | CAN(Powertrain) | 100ms |
| Comm_102 | Flow_102 | Func_103, Func_104, Func_105 | Req_103, Req_104, Req_105 | frmPedalInputCanMsg(0x2A2), frmSteeringStateCanMsg(0x100), frmBrakeStatusMsg(0x120), frmAccelStatusMsg(0x121), frmSteeringTorqueMsg(0x122) | CAN(Chassis) | 100ms |
| Comm_103 | Flow_103 | Func_106, Func_107 | Req_106, Req_107 | frmHazardControlMsg(0x261), frmWindowControlMsg(0x262), frmSeatBeltStateMsg(0x267), frmCabinAirStateMsg(0x268) | CAN(Body) | 100ms |
| Comm_104 | Flow_104 | Func_109 | Req_109 | frmClusterBaseStateMsg(0x281), frmClusterThemeMsg(0x286), frmHmiPopupStateMsg(0x287) | CAN(Infotainment) | 50ms |
| Comm_105 | Flow_105 | Func_110, Func_111 | Req_110, Req_111 | frmPowertrainGatewayMsg(0x109), frmVehicleModeMsg(0x10A), frmPowerLimitMsg(0x10B), frmCruiseStateMsg(0x10C), frmChassisHealthMsg(0x103), frmBodyHealthMsg(0x269), frmInfotainmentHealthMsg(0x288) | CAN(도메인 경계/라우팅) | 100ms |
| Comm_106 | Flow_106 | Func_112 | Req_112 | frmBaseTestResultMsg(0x2A6), frmTestResultMsg(0x2A5) | CAN(Chassis Validation frame) | Event |

- 주의: `Comm_101~Comm_106`은 도메인 분리 DBC(`*_can.dbc`)와 동기화된 확정 Comm 세트다. 라우팅 동작 변경 시 0302/0304와 함께 갱신한다.

## Vehicle Baseline Phase-B Comm 확장 정의 (Comm_201~Comm_205)

| Comm ID | Flow ID(0302 연계) | Func ID | Req ID | Message(ID) | Protocol | 주기 |
|---|---|---|---|---|---|---|
| Comm_201 | Flow_201 | Func_103, Func_104, Func_110 | Req_103, Req_104, Req_110 | frmEpsStateMsg(0x123), frmAbsStateMsg(0x124), frmEscStateMsg(0x125), frmTcsStateMsg(0x126), frmBrakeTempMsg(0x127), frmSteeringAngleMsg(0x128), frmWheelPulseMsg(0x104), frmSuspensionStateMsg(0x105), frmTirePressureMsg(0x106), frmChassisDiagReqMsg(0x2A4), frmChassisDiagResMsg(0x107), frmAdasChassisStatusMsg(0x1C1), frmBrakeWearMsg(0x129), frmRoadFrictionMsg(0x108) | CAN(Chassis + ETH Backbone CAN Stub) | 100ms + Event |
| Comm_202 | Flow_202 | Func_106, Func_107, Func_111, Func_113, Func_114, Func_115, Func_116, Func_117, Func_118 | Req_106, Req_107, Req_111, Req_113, Req_116, Req_118 | frmHvacStateMsg(0x26A), frmHvacActuatorMsg(0x26B), frmMirrorStateMsg(0x26C), frmSeatStateMsg(0x26D), frmSeatControlMsg(0x26E), frmDoorControlMsg(0x26F), frmInteriorLightMsg(0x270), frmRainLightAutoMsg(0x271), frmBcmDiagReqMsg(0x272), frmBcmDiagResMsg(0x273), frmImmobilizerStateMsg(0x274), frmAlarmStateMsg(0x275), frmBodyGatewayStateMsg(0x276), frmBodyComfortStateMsg(0x277) | CAN(Body) | 100ms + Event |
| Comm_203 | Flow_203 | Func_109, Func_111, Func_119 | Req_109, Req_111, Req_119 | frmAudioFocusMsg(0x289), frmVoiceAssistStateMsg(0x28A), frmMapRenderStateMsg(0x28B), frmRouteAlertMsg(0x28C), frmTrafficEventMsg(0x28D), frmPhoneProjectionMsg(0x28E), frmClusterNotifMsg(0x28F), frmMediaMetaMsg(0x291), frmSpeechTtsStateMsg(0x292), frmConnectivityStateMsg(0x293), frmClusterSyncStateMsg(0x295) | CAN(Infotainment) | 50/100ms |
| Comm_204 | Flow_204 | Func_101, Func_102, Func_110 | Req_101, Req_102, Req_110 | frmEngineTorqueMsg(0x12E), frmEngineLoadMsg(0x12F), frmTransShiftStateMsg(0x130), frmThermalMgmtStateMsg(0x131), frmEnergyFlowStateMsg(0x10F), frmPowertrainCtrlAuthMsg(0x110) | CAN(Powertrain) | 100ms |
| Comm_205 | Flow_205 | Func_112 | Req_112 | frmIviDiagReqMsg(0x2A7), frmIviDiagResMsg(0x290), frmIviHealthDetailMsg(0x294), frmPtDiagReqMsg(0x2AA), frmPtDiagResMsg(0x10E) | CAN(Validation/Diag) | Event + 100ms |

- 주의: `Comm_201~Comm_205`는 도메인 분리 DBC(`*_can.dbc`)와 동기화된 확정 Comm 세트이며, 변경 시 0302/0304를 동일 커밋에서 함께 갱신한다.

## V2 확장 Comm 정의 (Implemented, Comm_120~Comm_124)

| Comm ID | Flow ID(0302 연계) | Func ID | Req ID | Message(ID) | Protocol | 주기 |
|---|---|---|---|---|---|---|
| Comm_120 | Flow_120 | Func_120 | Req_120 | ethEmergencyRiskMsg(0x1C3) | Ethernet(UDP) | 100ms |
| Comm_121 | Flow_121 | Func_121 | Req_121 | ethDecelAssistReqMsg(0x1C4) | Ethernet(UDP) + CAN | Event + 50ms |
| Comm_122 | Flow_122 | Func_125, Func_126 | Req_125, Req_126 | ethSelectedAlertMsg(0xE200), frmAmbientControlMsg(0x260), frmClusterWarningMsg(0x280) | Ethernet(UDP) + CAN | 50ms |
| Comm_123 | Flow_123 | Func_123 | Req_123 | frmPedalInputCanMsg(0x2A2), frmSteeringCanMsg(0x2A1), ethDecelAssistReqMsg(0x1C4) | CAN + Ethernet(UDP) | Event + 100ms |
| Comm_124 | Flow_124 | Func_127, Func_128, Func_129 | Req_127, Req_128, Req_129 | frmChassisHealthMsg(0x103), frmBodyHealthMsg(0x269), frmInfotainmentHealthMsg(0x288), ethFailSafeStateMsg(0x111) | CAN + Ethernet(UDP) | 100ms + Event |

- 주의: `Comm_120~Comm_124`는 V2 확장 구현 Comm 세트다. 변경 시 0302/0304/05~07과 동일 커밋으로 동기화한다.

---

## 메시지 규모 기준 (현업 BP 타깃)

| Domain/Profile | 현재 정의 메시지 수 | 현재 사용 ID 범위 | 확장 목표(Phase-B) |
|---|---|---|---|
| Chassis CAN | 23 | 0x122~0x2A0(0x1C1 제외) | 24~30 |
| Body CAN | 24 | 0x289~0x291, 0x277~0x292 | 24~30 |
| Infotainment CAN | 24 | 0x2A3, 0x280~0x288, 0x289~0x295 | 24~30 |
| Powertrain CAN | 19 | 0x110~0x2A8 | 19~25 |
| Validation CAN (Chassis 통합) | 2 | 0x2A5~0x2A6 | 3~6 |
| ADAS CAN | 2 | 0x1C1, 0x1C3 | 2~6 |
| ETH Backbone CAN Stub | 4 | 0x1C0, 0x1C2, 0x1C4, 0x111 | 4~8 |
| Ethernet UDP | 8 타입 | 0x510/0x511/0x512/0xE100/0xE200/0x1C3/0x1C4/0x111 | 8~12 타입 |

- 통합 목표: CAN 메시지 `90~130`(CAN-stub 포함), Ethernet 메시지 타입 `5~12`, 전체 통신 항목 `100+`.

---

## 0302/0304 연계 체크포인트

- `Comm ID`는 `0302_NWflowDef.md`의 `Flow ID`와 1:1 연결한다.
- `Comm_001~Comm_009`, `Comm_101~Comm_106`, `Comm_201~Comm_205`는 `0304_System_Variables.md` Var 추적표와 동기화되어야 한다.
- `EmergencyAlert` Active/Clear 신호가 1000ms 타임아웃 규칙과 일치해야 한다.
- `selectedAlertLevel/selectedAlertType` 기반 Ambient/Cluster 출력 Comm이 모두 존재해야 한다.
- `ETH_SW` 경유 Ethernet 신호가 각 도메인 게이트웨이에서 CAN 메시지로 정상 변환되어야 한다.
- `speedLimit` 신호는 Comm_003에서 NAV_CTX_MGR와 ADAS_WARN_CTRL까지 연계되어야 한다.
- `Req_101~Req_107`, `Req_109~Req_119`는 Comm_101~Comm_106, Comm_201~Comm_205에서 누락 없이 연결되어야 한다.
- `Req_120~Req_121`, `Req_123`, `Req_125~Req_129`는 Comm_120~Comm_124 구현 체인으로 추적하고, 변경 시 0302/0304/05~07을 동일 커밋으로 동기화한다.

---

## 통신 예외 처리 규칙

| Comm Group | 예외 조건 | Fail-safe 동작 | 검증 포인트 |
|---|---|---|---|
| Group_A(Comm_001,002) | CHS_GW 변환 프레임 누락(연속 2주기) | ADAS_WARN_CTRL 입력 품질 플래그 저하, 경고 강등 모드 진입 | CAN 입력 정상 + ETH 변환 누락 시 동작 확인 |
| Group_B(Comm_003) | INFOTAINMENT_GW 변환 프레임 누락(연속 2주기) | NAV_CTX_MGR를 일반구간 기본 컨텍스트로 복귀 | 유도구간 상태에서 변환 누락 주입 |
| Group_C(Comm_004~006) | EmergencyAlert 1000ms 무갱신 | `timeoutClear=1`, emergencyContext clear, 출력 복귀 | Req_024 타임아웃 검증 |
| Group_D(Comm_007) | BODY_GW CAN 송신 ACK 실패 | ambientMode를 안전 기본값(0)으로 전환 후 재전송 | CAN Tx fail 주입 테스트 |
| Group_E(Comm_008) | IVI_GW CAN 송신 ACK 실패 | warningTextCode를 최소 안내 코드로 축소 후 재전송 | Cluster 경고 축소 출력 확인 |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| 3.21 | 2026-03-06 | 미사용 체인 정리: `Req_108/Func_108` 및 `frmDriverStateMsg(0x263)`를 Baseline Comm(103/202)·도메인 원본 표에서 제거하고 범위 문구를 `108 제외`로 동기화. |
| 3.20 | 2026-03-06 | 감사 해석 보강: 긴급 우선 요구의 기본 판정 축(기능중재)과 `Diag` 명칭/Group 7 비강제 규칙을 CAN ID 정책 요약표에 명시. |
| 3.19 | 2026-03-05 | 통신 문서 경계 정리: 본 문서에서는 CAN ID/메시지 규칙만 명시하고 ECU 명명은 `00e` SoT + `03`/`04` 참조 체계를 따르도록 정리. |
| 3.18 | 2026-03-05 | Validation 결과 프레임(`0x2A5`,`0x2A6`)의 관리 기준을 `chassis_can.dbc` 통합으로 전환하고 Validation 노드 명칭(`VAL_*`) 및 Comm 매체 표기를 정합화. |
| 3.17 | 2026-03-04 | 멘토링 체크리스트 반영: `test_can` 해석(Validation Harness 공통 DBC) 규칙과 CAN ID 배정 팀 룰(도메인/Stub/충돌회피/SoT)을 본문에 명시. |
| 3.16 | 2026-03-04 | DBC SoT 정합 보강: `eth_backbone_can_stub.dbc`를 통신 원본 매핑에 반영하고 0x1C0/0x1C1/0x1C2(및 0x1C3/0x1C4/0x111) CAN-stub 운반 경로를 상단표/Comm 표/규모표에 동기화. |
| 3.17 | 2026-03-05 | ADAS 도메인 분리 반영: `adas_can.dbc`를 추가하고 ADAS 소유 프레임(0x1C1/0x1C3)을 ETH Backbone CAN-stub에서 분리, 통신 원본표/도메인표를 동기화. |
| 3.15 | 2026-03-03 | ID 표기 기준 고정: 문서 본문은 Logical ID(0xE210/0xE211/0xE212)를 우선 표기하고, CANoe SIL 실행 ID는 Stub(0x1C3/0x1C4/0x111)로 병기하도록 작성 원칙을 보강. |
| 3.14 | 2026-03-03 | V2 확장 통신(`Comm_120~124`)을 Implemented 상태로 전환하고 메시지 ID/송수신 노드를 코드/DBC 실값(`0x1C3/0x1C4/0x111`, `WARN_ARB_MGR` 중심)으로 정정. |
| 3.13 | 2026-03-02 | 감사 정합 보강: 옵션1 설계 vs SIL 임시 CAN 대체 백본 검증 경계 문구를 작성 원칙에 추가. |
| 3.12 | 2026-03-02 | V2 확장 제어 책임 분리 반영: `Comm_121/Comm_123` 송수신 노드를 `DECEL_ASSIST_CTRL` 기준으로 조정. |
| 3.11 | 2026-03-02 | V2 확장(Pre-Activation) 반영: `Comm_120~Comm_124`(근접위험/감속보조/경고동기화/운전자개입해제/도메인단절강등) 추가 및 연계 체크포인트 보강. |
| 3.10 | 2026-03-02 | 0302/0303 최종 동기화 준비 반영: 도메인 통신 섹션 제목과 `Comm_101~106/201~205` 주의 문구를 병렬 작업 기준에서 DBC 동기화 운영 규칙으로 갱신. |
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
| 2.9 | 2026-02-28 | Nav 컨텍스트 메시지(0x2A3/0x512)에 `speedLimit`(bit16, DLC=3)를 추가하고 Comm_003을 Req_010/Func_010까지 확장 정합. |
| 3.0 | 2026-02-28 | CAN/Ethernet 통신 원본 파일 분리 원칙을 명시하고 SoT 매핑 표를 추가(`emergency_system.dbc` / `ETH_INTERFACE_CONTRACT.md`). |
| 3.1 | 2026-02-28 | DBC 병렬 작업용 도메인 통신 원본 확장 계획과 Vehicle Baseline Comm 계획(Comm_101~106, 예약 ID)을 추가. |
| 3.2 | 2026-02-28 | Comm_101~106을 확정 정의로 전환하고 도메인별 메시지 규모 기준(총 CAN 80~120, 전체 100+)을 명시. |
| 3.3 | 2026-02-28 | 도메인 분리 DBC(`emergency_system_*`) 실 메시지(0x126~0x2A8, 0x103~0x2A2, 0x288~0x28A, 0x1C2~0x2A6)를 Comm_101~106에 반영하고 SoT 계층 매핑을 보강. |
| 3.4 | 2026-02-28 | 상단 공식표를 실메시지 기준(49 Message / 131 Signal)으로 확장하고 signal bit position을 범위 표기(`0~7`, `8~15`)로 정규화. |
| 3.5 | 2026-02-28 | 상단 공식표를 Phase-B 확장 포함(99 Message / 242 Signal)으로 보강하고 Comm_201~205/Flow_201~205 연결 기준을 추가해 현업형 메시지 규모(100+)를 반영. |
| 3.6 | 2026-02-28 | SoT 경로를 실제 분리 DBC 파일명(`*_can.dbc`)으로 정합화하고, Core/Domain 통신 원본 매핑 표기 충돌을 해소. |
| 3.7 | 2026-02-28 | 0304 동기화 상태를 반영해 `Comm_101~106/201~205` 연계 체크포인트를 확정 문구로 갱신. |
| 3.8 | 2026-03-01 | 멘토 피드백 반영: EMS를 논리 단말(`EMS_ALERT`) 기준으로 Comm 표기 통합, 내부 TX/RX 모듈은 하단 보강 매핑으로 분리. |
| 3.9 | 2026-03-02 | V2 추적 밀도 보강 1차: `Comm_202/Comm_203` 매핑을 `Req_113~Req_119`, `Func_113~Func_119` 기준으로 확장해 Body/Infotainment 확장 신호의 요구-기능 연결을 명시. |

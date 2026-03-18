# 시스템 변수 정의 (System Variables)

**Document ID**: PROJ-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 / SWE.3
**Version**: 2.32
**Date**: 2026-03-18
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2/SWE.3) | `0304_System_Variables.md` | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

---

## 시스템 변수 표 (공식 표준 양식)

| ID | Namespace | Name | Data type | Min | Max | Initial Value | Description |
|---|---|---|---|---|---|---|---|
| 1 | Chassis | vehicleSpeed | uint32 | 0 | 255 | 0 | 차량 속도 입력값 |
| 2 | Chassis | driveState | uint32 | 0 | 3 | 0 | 주행 상태(P/R/N/D) 입력값 |
| 3 | Chassis | steeringInput | uint32 | 0 | 1 | 0 | 조향 입력 여부 |
| 4 | Infotainment | roadZone | uint32 | 0 | 3 | 0 | 구간 타입 입력값 |
| 5 | Infotainment | navDirection | uint32 | 0 | 3 | 0 | 내비게이션 방향 정보 |
| 6 | Infotainment | zoneDistance | uint32 | 0 | 255 | 0 | 구간 잔여 거리 |
| 7 | V2X | emergencyType | uint32 | 0 | 3 | 0 | 긴급차량 종류 |
| 8 | V2X | emergencyDirection | uint32 | 0 | 3 | 0 | 긴급차량 접근 방향 |
| 9 | V2X | EtaSeconds | uint32 | 0 | 255 | 0 | 긴급차량 ETA(유효값 0~255, 내부 invalid sentinel 65535) |
| 10 | V2X | SourceId | uint32 | 0 | 255 | 0 | 긴급 메시지 Source ID |
| 11 | V2X | Status | uint32 | 0 | 1 | 0 | 긴급 메시지 Active/Clear 상태 |
| 12 | Core | vehicleSpeedNorm | uint32 | 0 | 255 | 0 | 게이트웨이 정규화 후 차량 속도 |
| 13 | Core | driveStateNorm | uint32 | 0 | 3 | 0 | 게이트웨이 정규화 후 주행 상태 |
| 14 | Core | steeringInputNorm | uint32 | 0 | 1 | 0 | 게이트웨이 정규화 후 조향 입력 |
| 15 | Core | baseZoneContext | uint32 | 0 | 255 | 0 | 구간 컨텍스트 계산 결과 |
| 16 | Core | warningState | uint32 | 0 | 255 | 0 | 경고 조건 판정 상태 |
| 17 | Core | emergencyContext | uint32 | 0 | 255 | 0 | 긴급 수신 컨텍스트 상태 |
| 18 | Core | selectedAlertLevel | uint32 | 0 | 7 | 0 | 중재 결과 경고 레벨 |
| 19 | Core | selectedAlertType | uint32 | 0 | 7 | 0 | 중재 결과 경고 타입 |
| 20 | Core | timeoutClear | uint32 | 0 | 1 | 0 | 1000ms 무갱신 해제 플래그 |
| 21 | Body | ambientMode | uint32 | 0 | 7 | 0 | 앰비언트 제어 모드 |
| 22 | Body | ambientColor | uint32 | 0 | 7 | 0 | 앰비언트 색상 코드 |
| 23 | Body | ambientPattern | uint32 | 0 | 3 | 0 | 앰비언트 패턴 코드 |
| 24 | Cluster | warningTextCode | uint32 | 0 | 255 | 0 | 클러스터 경고 코드 |
| 25 | Test | testScenario | uint32 | 0 | 255 | 0 | SIL 테스트 시나리오 선택값(Validation-only) |
| 26 | Test | scenarioResult | uint32 | 0 | 1 | 0 | SIL 시나리오 Pass/Fail 결과(Validation-only) |
| 27 | CoreState | lastEmergencyRxMs | uint32 | 0 | 4294967295 | 0 | 마지막 긴급 신호 수신 시각(ms) |
| 28 | CoreState | duplicatePopupGuard | uint32 | 0 | 5000 | 0 | 중복 팝업 억제 타이머(ms) |
| 29 | CoreState | arbitrationSnapshotId | uint32 | 0 | 65535 | 0 | 중재 스냅샷 식별자 |
| 30 | Infotainment | speedLimit | uint32 | 0 | 255 | 30 | 구간 제한속도(km/h) |
| 31 | Core | speedLimitNorm | uint32 | 0 | 255 | 30 | 게이트웨이 정규화 후 구간 제한속도 |
| 32 | Core | proximityRiskLevel | uint32 | 0 | 100 | 0 | 긴급차량 근접 위험도 산정값 |
| 33 | Core | decelAssistReq | uint32 | 0 | 1 | 0 | CGW가 fail-safe 정책을 반영한 effective 감속 보조 요청 플래그 |
| 34 | Core | failSafeMode | uint32 | 0 | 2 | 0 | 경고 정보 전달 이상 강등 모드 |
| 35 | CoreState | warningPathStatus | uint32 | 0 | 2 | 0 | 경고 정보 전달 경로 상태(정상/열화/단절) |
| 36 | CoreState | e2eHealthState | uint32 | 0 | 2 | 0 | E2E 경로 헬스 상태 |
| 37 | Core | brakePedalNorm | uint32 | 0 | 100 | 0 | CHS_GW에서 정규화한 브레이크 입력 |
| 38 | Test | forceFailSafe | uint32 | 0 | 1 | 0 | Fail-safe 강제 주입(Validation-only) |
| 39 | Core | objectTrackValid | uint32 | 0 | 1 | 0 | 객체 추적 유효 플래그 |
| 40 | Core | objectRange | uint32 | 0 | 500 | 0 | 대표 위험 객체 상대 거리(m) |
| 41 | Core | objectRelSpeed | int32 | -200 | 200 | 0 | 대표 위험 객체 상대 속도(km/h) |
| 42 | Core | objectConfidence | uint32 | 0 | 100 | 0 | 객체 인지 신뢰도(%) |
| 43 | Core | objectRiskClass | uint32 | 0 | 7 | 0 | 객체 위험 분류 코드 |
| 44 | Core | objectTtcMin | uint32 | 0 | 10000 | 10000 | 대표 위험 객체 최소 TTC(ms) |
| 45 | Core | intersectionConflictFlag | uint32 | 0 | 1 | 0 | 교차로 측방 접근 충돌 플래그 |
| 46 | Core | mergeCutInFlag | uint32 | 0 | 1 | 0 | 합류/끼어들기 급간섭 플래그 |
| 47 | Core | objectAlertHoldMs | uint32 | 0 | 5000 | 300 | 객체 추적 손실 시 경고 유지시간(ms) |
| 48 | Core | objectEventCode | uint32 | 0 | 65535 | 0 | 객체 기반 경고 이벤트 코드 |
| 49 | Test | displayModeSetting | uint32 | 0 | 2 | 0 | 표시 모드 수동 설정 입력(Validation-only) |
| 50 | Test | alertVolumeSetting | uint32 | 0 | 100 | 50 | 경고 음량 수동 설정 입력(Validation-only) |
| 51 | Test | seatBeltOverride | uint32 | 0 | 2 | 0 | 안전벨트 상태 오버라이드 입력(Validation-only) |
| 52 | Test | historyQueryOffset | uint32 | 0 | 255 | 0 | 경고 이력 조회 오프셋 입력(Validation-only) |
| 53 | Test | historyQueryCode | uint32 | 0 | 65535 | 0 | 경고 이력 조회 코드 입력(Validation-only) |
| 54 | Test | turnLampOverride | uint32 | 0 | 2 | 0 | 방향지시등 상태 오버라이드 입력(Validation-only) |
| 55 | CoreState | emergencyIngressDirection | uint32 | 0 | 3 | 0 | V2X owner가 정규화한 긴급 접근 방향 메타데이터 |
| 56 | CoreState | emergencyIngressEtaSec | uint32 | 0 | 255 | 255 | V2X owner가 정규화한 긴급 접근 ETA 메타데이터 |
| 57 | CoreState | emergencyIngressSourceId | uint32 | 0 | 255 | 255 | V2X owner가 정규화한 긴급 메시지 Source ID 메타데이터 |
| 58 | Core | accelPedalNorm | uint32 | 0 | 100 | 0 | CHS_GW에서 정규화한 가속 페달 입력 |
| 59 | CoreState | selectedAlertDecisionLevel | uint32 | 0 | 7 | 0 | ADAS owner가 산출한 경고 decision 레벨(경계/Failsafe 적용 전) |
| 60 | CoreState | selectedAlertDecisionType | uint32 | 0 | 15 | 0 | ADAS owner가 산출한 경고 decision 타입(경계/Failsafe 적용 전) |
| 61 | CoreState | selectedAlertEffectiveLevel | uint32 | 0 | 7 | 0 | CGW owner가 경계/Failsafe 정책을 반영한 경고 effective 레벨 |
| 62 | CoreState | selectedAlertEffectiveType | uint32 | 0 | 15 | 0 | CGW owner가 경계/Failsafe 정책을 반영한 경고 effective 타입 |
| 63 | CoreState | selectedAlertGateReason | uint32 | 0 | 3 | 0 | 경고 effective shaping 원인(0=없음 1=timeout-clear 2=boundary-hold 3=fail-safe-floor) |
| 64 | V2X | ingressHeartbeat | uint32 | 0 | 65535 | 0 | V2X ingress freshness 추적용 heartbeat |
| 65 | CoreState | driverReleaseReason | uint32 | 0 | 3 | 0 | ADAS owner가 판단한 운전자 감속 해제 원인(0=없음 1=조향 개입 2=제동 개입 3=예약) |
| 101 | Chassis | AccelPedal | uint32 | 0 | 100 | 0 | 가속 페달 입력 |
| 102 | Chassis | BrakePedal | uint32 | 0 | 100 | 0 | 브레이크 페달 입력 |
| 103 | Chassis | SteeringState | uint32 | 0 | 3 | 0 | 조향 상태 |
| 104 | Chassis | WheelSpdFL | uint32 | 0 | 255 | 0 | 전륜 좌 휠속도 |
| 105 | Chassis | WheelSpdFR | uint32 | 0 | 255 | 0 | 전륜 우 휠속도 |
| 106 | Chassis | WheelSpdRL | uint32 | 0 | 255 | 0 | 후륜 좌 휠속도 |
| 107 | Chassis | WheelSpdRR | uint32 | 0 | 255 | 0 | 후륜 우 휠속도 |
| 108 | Chassis | YawRate | uint32 | 0 | 65535 | 0 | 요레이트 |
| 109 | Chassis | LatAccel | uint32 | 0 | 65535 | 0 | 횡가속도 |
| 110 | Chassis | BrakePressure | uint32 | 0 | 255 | 0 | 브레이크 압력 |
| 111 | Chassis | BrakeMode | uint32 | 0 | 3 | 0 | 브레이크 동작 모드 |
| 112 | Chassis | AbsActive | uint32 | 0 | 1 | 0 | ABS 활성 상태 |
| 113 | Chassis | EspActive | uint32 | 0 | 1 | 0 | ESC 활성 상태 |
| 114 | Chassis | AccelRequest | uint32 | 0 | 100 | 0 | 가속 요청 |
| 115 | Chassis | TorqueRequest | uint32 | 0 | 255 | 0 | 토크 요청 |
| 116 | Chassis | SteeringTorque | uint32 | 0 | 4095 | 0 | 조향 토크 |
| 117 | Chassis | SteeringAssistLv | uint32 | 0 | 15 | 0 | 조향 보조 레벨 |
| 118 | Chassis | ChassisAliveCnt | uint32 | 0 | 255 | 0 | Chassis Alive Counter |
| 119 | Chassis | ChassisDiagState | uint32 | 0 | 15 | 0 | Chassis 진단 상태 |
| 120 | Chassis | ChassisFailCode | uint32 | 0 | 15 | 0 | Chassis 오류 코드 |
| 121 | Body | HazardSwitch | uint32 | 0 | 1 | 0 | 비상등 스위치 |
| 122 | Body | HazardState | uint32 | 0 | 1 | 0 | 비상등 상태 |
| 123 | Body | WindowCommand | uint32 | 0 | 3 | 0 | 창문 제어 명령 |
| 124 | Body | WindowState | uint32 | 0 | 3 | 0 | 창문 상태 |
| 127 | Body | DoorStateMask | uint32 | 0 | 255 | 0 | 도어 상태 비트맵 |
| 128 | Body | DoorLockState | uint32 | 0 | 3 | 0 | 도어 잠금 상태 |
| 129 | Body | ChildLockState | uint32 | 0 | 1 | 0 | 아동 잠금 상태 |
| 130 | Body | DoorOpenWarn | uint32 | 0 | 1 | 0 | 도어 열림 경고 |
| 131 | Body | HeadLampState | uint32 | 0 | 3 | 0 | 전조등 상태 |
| 132 | Body | TailLampState | uint32 | 0 | 3 | 0 | 후미등 상태 |
| 133 | Body | TurnLampState | uint32 | 0 | 3 | 0 | 방향지시등 상태 |
| 134 | Body | HazardLampReq | uint32 | 0 | 1 | 0 | 비상등 요청 |
| 135 | Body | FrontWiperState | uint32 | 0 | 3 | 0 | 전면 와이퍼 상태 |
| 136 | Body | RearWiperState | uint32 | 0 | 3 | 0 | 후면 와이퍼 상태 |
| 137 | Body | WiperInterval | uint32 | 0 | 15 | 0 | 와이퍼 인터벌 |
| 138 | Body | DriverSeatBelt | uint32 | 0 | 1 | 0 | 운전석 안전벨트 상태 |
| 139 | Body | PassengerSeatBelt | uint32 | 0 | 1 | 0 | 동승석 안전벨트 상태 |
| 140 | Body | RearSeatBelt | uint32 | 0 | 3 | 0 | 후석 안전벨트 상태 |
| 141 | Body | SeatBeltWarnLvl | uint32 | 0 | 3 | 0 | 안전벨트 경고 레벨 |
| 142 | Body | CabinTemp | uint32 | 0 | 100 | 0 | 실내 온도 |
| 143 | Body | AirQualityIndex | uint32 | 0 | 255 | 0 | 실내 공기질 지수 |
| 144 | Body | BodyAliveCnt | uint32 | 0 | 255 | 0 | Body Alive Counter |
| 145 | Body | BodyDiagState | uint32 | 0 | 15 | 0 | Body 진단 상태 |
| 146 | Body | BodyFailCode | uint32 | 0 | 15 | 0 | Body 오류 코드 |
| 147 | Cluster | ClusterSpeed | uint32 | 0 | 255 | 0 | 클러스터 표시 속도 |
| 148 | Cluster | ClusterGear | uint32 | 0 | 7 | 0 | 클러스터 표시 기어 |
| 149 | Cluster | ClusterStatus | uint32 | 0 | 31 | 0 | 클러스터 기본 상태 |
| 150 | Infotainment | GuideLaneState | uint32 | 0 | 3 | 0 | 유도선 상태 |
| 151 | Infotainment | GuideConfidence | uint32 | 0 | 63 | 0 | 유도 신뢰도 |
| 152 | Infotainment | MediaSource | uint32 | 0 | 7 | 0 | 미디어 소스 |
| 153 | Infotainment | MediaState | uint32 | 0 | 7 | 0 | 미디어 재생 상태 |
| 154 | Infotainment | MuteState | uint32 | 0 | 1 | 0 | 음소거 상태 |
| 155 | Infotainment | VolumeLevel | uint32 | 0 | 100 | 0 | 볼륨 레벨 |
| 156 | Infotainment | CallState | uint32 | 0 | 7 | 0 | 통화 상태 |
| 157 | Infotainment | MicMute | uint32 | 0 | 1 | 0 | 마이크 음소거 |
| 158 | Infotainment | SignalQuality | uint32 | 0 | 15 | 0 | 통신 품질 |
| 159 | Infotainment | BtDeviceCount | uint32 | 0 | 15 | 0 | 블루투스 연결 수 |
| 160 | Infotainment | RouteClass | uint32 | 0 | 3 | 0 | 경로 분류 |
| 161 | Infotainment | GuideType | uint32 | 0 | 3 | 0 | 안내 유형 |
| 162 | Infotainment | RouteProgress | uint32 | 0 | 100 | 0 | 경로 진행률 |
| 163 | Infotainment | EtaMinutes | uint32 | 0 | 255 | 0 | 도착 예상 시간(분) |
| 164 | Cluster | ThemeMode | uint32 | 0 | 7 | 0 | 클러스터 테마 모드 |
| 165 | Cluster | ClusterBrightness | uint32 | 0 | 31 | 0 | 클러스터 밝기 |
| 166 | Cluster | PopupType | uint32 | 0 | 15 | 0 | 팝업 유형 |
| 167 | Cluster | PopupPriority | uint32 | 0 | 7 | 0 | 팝업 우선순위 |
| 168 | Cluster | PopupActive | uint32 | 0 | 1 | 0 | 팝업 활성 상태 |
| 169 | Infotainment | InfoAliveCnt | uint32 | 0 | 255 | 0 | Infotainment Alive Counter |
| 170 | Infotainment | InfoDiagState | uint32 | 0 | 15 | 0 | Infotainment 진단 상태 |
| 171 | Infotainment | InfoFailCode | uint32 | 0 | 15 | 0 | Infotainment 오류 코드 |
| 172 | Test | BaseScenarioId | uint32 | 0 | 255 | 0 | 기본 시나리오 ID |
| 173 | Test | BaseScenarioResult | uint32 | 0 | 1 | 0 | 기본 시나리오 판정 |
| 174 | Test | TimeoutClearMon | uint32 | 0 | 1 | 0 | 타임아웃 모니터 플래그 |
| 175 | Powertrain | IgnitionState | uint32 | 0 | 1 | 0 | 시동 입력 상태 |
| 176 | Powertrain | EngineState | uint32 | 0 | 3 | 0 | 엔진 동작 상태 |
| 177 | Powertrain | GearInput | uint32 | 0 | 7 | 0 | 기어 입력값 |
| 178 | Powertrain | GearState | uint32 | 0 | 7 | 0 | 기어 상태값 |
| 179 | Powertrain | RoutingPolicy | uint32 | 0 | 255 | 0 | 경고 정보 전달 라우팅 정책 |
| 180 | Powertrain | BoundaryStatus | uint32 | 0 | 255 | 0 | 경고 정보 전달 경계 상태 |
| 181 | Powertrain | EngineRpm | uint32 | 0 | 65535 | 0 | 엔진 회전수 |
| 182 | Powertrain | CoolantTemp | uint32 | 0 | 255 | 0 | 냉각수 온도 |
| 183 | Powertrain | OilTemp | uint32 | 0 | 255 | 0 | 엔진오일 온도 |
| 184 | Powertrain | FuelLevel | uint32 | 0 | 100 | 0 | 연료 잔량 |
| 185 | Powertrain | BatterySoc | uint32 | 0 | 100 | 0 | 배터리 SOC |
| 186 | Powertrain | ChargingState | uint32 | 0 | 3 | 0 | 충전 상태 |
| 187 | Powertrain | ThrottlePos | uint32 | 0 | 100 | 0 | 스로틀 위치 |
| 188 | Powertrain | ThrottleReq | uint32 | 0 | 100 | 0 | 스로틀 요청 |
| 189 | Powertrain | TransOilTemp | uint32 | 0 | 255 | 0 | 변속기 오일 온도 |
| 190 | Powertrain | ClutchTemp | uint32 | 0 | 255 | 0 | 클러치 온도 |
| 191 | Powertrain | DriveMode | uint32 | 0 | 7 | 0 | 주행 모드 |
| 192 | Powertrain | EcoMode | uint32 | 0 | 1 | 0 | 에코 모드 |
| 193 | Powertrain | SportMode | uint32 | 0 | 1 | 0 | 스포츠 모드 |
| 194 | Powertrain | SnowMode | uint32 | 0 | 1 | 0 | 스노우 모드 |
| 195 | Powertrain | PowertrainState | uint32 | 0 | 255 | 0 | 파워트레인 상태 |
| 196 | Powertrain | TorqueLimit | uint32 | 0 | 255 | 0 | 토크 제한값 |
| 197 | Powertrain | SpeedLimit | uint32 | 0 | 255 | 30 | 속도 제한값 |
| 198 | Powertrain | CruiseState | uint32 | 0 | 3 | 0 | 크루즈 상태 |
| 199 | Powertrain | GapLevel | uint32 | 0 | 3 | 0 | 차간 거리 레벨 |
| 200 | Powertrain | CruiseSetSpeed | uint32 | 0 | 255 | 0 | 크루즈 설정 속도 |
| 201 | Powertrain | PtAliveCnt | uint32 | 0 | 255 | 0 | Powertrain Alive Counter |
| 202 | Powertrain | PtDiagState | uint32 | 0 | 15 | 0 | Powertrain 진단 상태 |
| 203 | Powertrain | PtFailCode | uint32 | 0 | 15 | 0 | Powertrain 오류 코드 |
| 204 | Chassis | EpsAssistState | uint32 | 0 | 7 | 0 | MDPS 보조 상태 |
| 205 | Chassis | EpsFaultState | uint32 | 0 | 1 | 0 | MDPS 고장 상태 |
| 206 | Chassis | EpsTemp | uint32 | 0 | 255 | 0 | MDPS 온도 |
| 207 | Chassis | AbsCtrlState | uint32 | 0 | 7 | 0 | ABS 제어 상태 |
| 208 | Chassis | AbsSlipLevel | uint32 | 0 | 255 | 0 | ABS 슬립 레벨 |
| 209 | Chassis | EscCtrlState | uint32 | 0 | 7 | 0 | ESC 제어 상태 |
| 210 | Chassis | EscYawTarget | uint32 | 0 | 255 | 0 | 요 모멘트 제어 요구 |
| 211 | Chassis | TcsCtrlState | uint32 | 0 | 1 | 0 | TCS 활성 상태 |
| 212 | Chassis | TcsSlipRatio | uint32 | 0 | 255 | 0 | TCS 슬립 비율 |
| 213 | Chassis | BrakeTempFL | uint32 | 0 | 255 | 0 | 브레이크 전륜좌 온도 |
| 214 | Chassis | BrakeTempFR | uint32 | 0 | 255 | 0 | 브레이크 전륜우 온도 |
| 217 | Chassis | SteeringAngleRaw | int32 | -720 | 720 | 0 | 조향각 |
| 218 | Chassis | SteeringAngleRate | int32 | -1024 | 1023 | 0 | 조향각속도 |
| 219 | Chassis | WheelPulseFront | uint32 | 0 | 65535 | 0 | 전륜 휠 펄스 |
| 220 | Chassis | WheelPulseRear | uint32 | 0 | 65535 | 0 | 후륜 휠 펄스 |
| 221 | Chassis | SuspensionMode | uint32 | 0 | 7 | 0 | 댐퍼 모드 |
| 222 | Chassis | SuspensionLevel | uint32 | 0 | 255 | 0 | 차고 높이 |
| 223 | Chassis | TirePressFL | uint32 | 0 | 255 | 0 | 전륜좌 타이어 압력 |
| 224 | Chassis | TirePressFR | uint32 | 0 | 255 | 0 | 전륜우 타이어 압력 |
| 225 | Chassis | TirePressRL | uint32 | 0 | 255 | 0 | 후륜좌 타이어 압력 |
| 226 | Chassis | TirePressRR | uint32 | 0 | 255 | 0 | 후륜우 타이어 압력 |
| 227 | Chassis | ChsDiagServiceId | uint32 | 0 | 255 | 0 | Chassis 진단 요청 ID |
| 228 | Chassis | ChsDiagDidHigh | uint32 | 0 | 1 | 0 | Chassis 진단 요청 활성 |
| 229 | Chassis | ChsDiagRespCode | uint32 | 0 | 255 | 0 | Chassis 진단 응답 ID |
| 230 | Chassis | ChsDiagData0 | uint32 | 0 | 15 | 0 | Chassis 진단 결과 |
| 231 | Chassis | AdasChassisState | uint32 | 0 | 255 | 0 | ADAS 섀시 상태 코드 |
| 232 | Chassis | AdasHealthLevel | uint32 | 0 | 255 | 0 | ADAS 헬스 상태 코드 |
| 234 | Chassis | BrakePadWearFl | uint32 | 0 | 100 | 0 | 브레이크 패드 마모(전륜좌) |
| 235 | Chassis | BrakePadWearFr | uint32 | 0 | 100 | 0 | 브레이크 패드 마모(전륜우) |
| 236 | Chassis | RoadFrictionCoef | uint32 | 0 | 255 | 0 | 노면 마찰 추정치 |
| 238 | Body | CabinSetTemp | uint32 | 0 | 63 | 0 | 실내 설정 온도 |
| 239 | Body | BlowerLevel | uint32 | 0 | 15 | 0 | 블로워 레벨 |
| 240 | Body | VentMode | uint32 | 0 | 7 | 0 | 공조 벤트 모드 |
| 241 | Body | AcCompressorOn | uint32 | 0 | 1 | 0 | A/C 컴프레서 요청 |
| 242 | Body | MirrorFoldState | uint32 | 0 | 1 | 0 | 미러 폴딩 상태 |
| 243 | Body | MirrorHeatState | uint32 | 0 | 1 | 0 | 미러 열선 상태 |
| 244 | Body | MirrorAdjustAxis | uint32 | 0 | 3 | 0 | 미러 조정 축 |
| 245 | Body | DriverSeatPos | uint32 | 0 | 255 | 0 | 운전석 시트 위치 |
| 246 | Body | PassengerSeatPos | uint32 | 0 | 255 | 0 | 동승석 시트 위치 |
| 247 | Body | SeatHeatLevel | uint32 | 0 | 7 | 0 | 시트 히터 레벨 |
| 248 | Body | SeatVentLevel | uint32 | 0 | 7 | 0 | 시트 통풍 레벨 |
| 249 | Body | DoorControlCmd | uint32 | 0 | 3 | 0 | 도어 언락 명령 |
| 250 | Body | ChildLockCmd | uint32 | 0 | 1 | 0 | 아동 잠금 명령 |
| 251 | Body | CabinLightMode | uint32 | 0 | 7 | 0 | 실내등 모드 |
| 252 | Body | DomeLightLevel | uint32 | 0 | 255 | 0 | 실내등 밝기 |
| 253 | Body | RainSenseLevel | uint32 | 0 | 255 | 0 | 우적 센서 레벨 |
| 254 | Body | AutoLightState | uint32 | 0 | 1 | 0 | 오토 헤드램프 요청 |
| 255 | Body | BcmDiagServiceId | uint32 | 0 | 255 | 0 | BCM 진단 요청 ID |
| 256 | Body | BcmDiagDidHigh | uint32 | 0 | 1 | 0 | BCM 진단 요청 활성 |
| 257 | Body | BcmDiagRespCode | uint32 | 0 | 255 | 0 | BCM 진단 응답 ID |
| 258 | Body | BcmDiagData0 | uint32 | 0 | 15 | 0 | BCM 진단 결과 |
| 259 | Body | ImmobilizerState | uint32 | 0 | 3 | 0 | 이모빌라이저 상태 |
| 260 | Body | KeyAuthState | uint32 | 0 | 3 | 0 | 키 인증 상태 |
| 261 | Body | AlarmArmState | uint32 | 0 | 1 | 0 | 알람 경계 상태 |
| 262 | Body | IntrusionDetect | uint32 | 0 | 1 | 0 | 알람 트리거 상태 |
| 264 | Body | BodyGwRouteState | uint32 | 0 | 100 | 0 | Body GW 부하율 |
| 265 | Body | BodyGwHealth | uint32 | 0 | 255 | 0 | Body GW 라우팅 상태 |
| 266 | Body | ComfortProfile | uint32 | 0 | 7 | 0 | 컴포트 모드 |
| 267 | Body | ComfortStatus | uint32 | 0 | 1 | 0 | 아동 안전 상태 |
| 268 | Infotainment | AudioFocusOwner | uint32 | 0 | 7 | 0 | 오디오 포커스 소유자 |
| 269 | Infotainment | AudioDuckingLvl | uint32 | 0 | 255 | 0 | 오디오 덕킹 레벨 |
| 270 | Infotainment | VoiceAssistState | uint32 | 0 | 7 | 0 | 음성비서 상태 |
| 271 | Infotainment | WakeWordState | uint32 | 0 | 15 | 0 | 음성 깨우기 소스 |
| 272 | Infotainment | ZoomLevel | uint32 | 0 | 255 | 0 | 지도 줌 레벨 |
| 273 | Infotainment | MapRenderState | uint32 | 0 | 15 | 0 | 지도 테마 |
| 274 | Infotainment | RouteAlertType | uint32 | 0 | 15 | 0 | 다음 회전 유형 |
| 275 | Infotainment | RouteAlertEta | uint32 | 0 | 255 | 0 | 다음 회전 잔여 거리 |
| 276 | Infotainment | TrafficEventType | uint32 | 0 | 15 | 0 | 교통 이벤트 유형 |
| 277 | Infotainment | TrafficSeverity | uint32 | 0 | 7 | 0 | 교통 이벤트 심각도 |
| 278 | Infotainment | TrafficDistance | uint32 | 0 | 255 | 0 | 이벤트 잔여 거리 |
| 279 | Infotainment | ProjectionType | uint32 | 0 | 7 | 0 | 프로젝션 유형 |
| 280 | Infotainment | ProjectionState | uint32 | 0 | 3 | 0 | 프로젝션 상태 |
| 281 | Cluster | ClusterNotifType | uint32 | 0 | 15 | 0 | 클러스터 알림 유형 |
| 282 | Cluster | ClusterNotifArg | uint32 | 0 | 7 | 0 | 클러스터 알림 우선순위 |
| 283 | Infotainment | IviDiagServiceId | uint32 | 0 | 255 | 0 | IVI 진단 요청 ID |
| 284 | Infotainment | IviDiagDidHigh | uint32 | 0 | 1 | 0 | IVI 진단 요청 활성 |
| 285 | Infotainment | IviDiagRespCode | uint32 | 0 | 255 | 0 | IVI 진단 응답 ID |
| 286 | Infotainment | IviDiagData0 | uint32 | 0 | 15 | 0 | IVI 진단 결과 |
| 287 | Infotainment | MediaTrackType | uint32 | 0 | 15 | 0 | 미디어 장르 |
| 288 | Infotainment | MediaRemainTime | uint32 | 0 | 100 | 0 | 트랙 진행률 |
| 289 | Infotainment | TtsState | uint32 | 0 | 7 | 0 | TTS 상태 |
| 290 | Infotainment | TtsQueueDepth | uint32 | 0 | 255 | 0 | TTS 언어 ID |
| 291 | Infotainment | ConnectivityType | uint32 | 0 | 7 | 0 | LTE 연결 상태 |
| 292 | Infotainment | ConnectivityState | uint32 | 0 | 1 | 0 | Wi-Fi 연결 상태 |
| 293 | Infotainment | SignalBars | uint32 | 0 | 1 | 0 | Bluetooth 연결 상태 |
| 294 | Infotainment | IviCpuLoad | uint32 | 0 | 100 | 0 | IVI CPU 부하율 |
| 295 | Infotainment | IviMemLoad | uint32 | 0 | 100 | 0 | IVI 메모리 부하율 |
| 296 | Cluster | ClusterSyncState | uint32 | 0 | 7 | 0 | 클러스터 동기화 상태 |
| 297 | Cluster | ClusterSyncAge | uint32 | 0 | 255 | 0 | 클러스터 동기화 시퀀스 |
| 298 | Powertrain | EngineTorqueAct | uint32 | 0 | 65535 | 0 | 엔진 실제 토크 |
| 299 | Powertrain | EngineTorqueReq | uint32 | 0 | 65535 | 0 | 엔진 요구 토크 |
| 300 | Powertrain | EngineLoad | uint32 | 0 | 100 | 0 | 엔진 부하율 |
| 302 | Powertrain | ShiftState | uint32 | 0 | 7 | 0 | 변속 상태 |
| 303 | Powertrain | ShiftSlip | uint32 | 0 | 1 | 0 | 변속 진행 상태 |
| 304 | Powertrain | ShiftTargetGear | uint32 | 0 | 7 | 0 | 목표 기어 |
| 305 | Powertrain | PtDiagServiceId | uint32 | 0 | 255 | 0 | Powertrain 진단 요청 ID |
| 306 | Powertrain | PtDiagDidHigh | uint32 | 0 | 1 | 0 | Powertrain 진단 요청 활성 |
| 307 | Powertrain | PtDiagRespCode | uint32 | 0 | 255 | 0 | Powertrain 진단 응답 ID |
| 308 | Powertrain | PtDiagData0 | uint32 | 0 | 15 | 0 | Powertrain 진단 결과 |
| 309 | Powertrain | ThermalMode | uint32 | 0 | 7 | 0 | 열관리 모드 |
| 310 | Powertrain | FanDuty | uint32 | 0 | 255 | 0 | 팬 속도 명령 |
| 311 | Powertrain | RegenLevel | uint32 | 0 | 15 | 0 | 회생 제동 레벨 |
| 312 | Powertrain | EnergyFlowMode | uint32 | 0 | 3 | 0 | 에너지 흐름 방향 |
| 313 | Powertrain | CtrlAuthLevel | uint32 | 0 | 3 | 0 | 파워트레인 제어 권한 상태 |
| 314 | Powertrain | CtrlAuthSource | uint32 | 0 | 15 | 0 | 파워트레인 제어 출처 |
| 315 | Diag | SecurityState | uint32 | 0 | 3 | 0 | 진단 보안 상태(0=Unknown 1=Nominal 2=Restricted 3=Denied) |
| 316 | Diag | ServiceState | uint32 | 0 | 3 | 0 | 진단 서비스 상태(0=Unknown 1=Available 2=Unavailable 3=Degraded) |
| 317 | Diag | RouteOwner | uint32 | 0 | 3 | 0 | 진단 경로 소유 해석(0=None 1=SGW 2=DCM 3=RuntimeOwner) |
| 318 | Diag | ResponseKind | uint32 | 0 | 4 | 0 | 진단 응답 분류(0=None 1=Positive 2=Negative 3=Timeout 4=Unavailable) |
| 319 | Diag | ReasonCode | uint32 | 0 | 65535 | 0 | 진단 판정 근거 코드 |
| 320 | Diag | LastRequestTarget | uint32 | 0 | 255 | 0 | 최근 진단 요청 대상 코드 |
| 321 | Diag | LastRequestSid | uint32 | 0 | 255 | 0 | 최근 진단 요청 서비스 ID |
| 322 | Diag | LastRequestDidHigh | uint32 | 0 | 255 | 0 | 최근 진단 요청 DID 상위 바이트 |
| 323 | Diag | LastRequestDidLow | uint32 | 0 | 255 | 0 | 최근 진단 요청 DID 하위 바이트 |
| 324 | Diag | LastRequestSourceBus | uint32 | 0 | 255 | 0 | 최근 진단 요청 입력 버스 코드 |
| 325 | Diag | RequestCounter | uint32 | 0 | 2147483647 | 0 | 진단 요청 누적 카운터 |
| 326 | Diag | LastRequestTimeMs | uint32 | 0 | 4294967295 | 0 | 최근 진단 요청 시각(ms) |
| 327 | Diag | LastResponseTarget | uint32 | 0 | 255 | 0 | 최근 진단 응답 대상 코드 |
| 328 | Diag | LastResponseCode | uint32 | 0 | 255 | 0 | 최근 진단 응답 코드 |
| 329 | Diag | LastResponseData0 | uint32 | 0 | 255 | 0 | 최근 진단 응답 요약 데이터0 |
| 330 | Diag | LastResponseData1 | uint32 | 0 | 255 | 0 | 최근 진단 응답 요약 데이터1 |
| 331 | Diag | LastResponseOk | uint32 | 0 | 1 | 0 | 최근 진단 응답 양성 여부 |
| 332 | Diag | LastResponseSourceBus | uint32 | 0 | 255 | 0 | 최근 진단 응답 출력 버스 코드 |
| 333 | Diag | ResponseCounter | uint32 | 0 | 2147483647 | 0 | 진단 응답 누적 카운터 |
| 334 | Diag | LastResponseTimeMs | uint32 | 0 | 4294967295 | 0 | 최근 진단 응답 시각(ms) |
---

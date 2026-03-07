# 시스템 변수 정의 (System Variables)

**Document ID**: PROJ-0304-SV
**ISO 26262 Reference**: Part 6, Cl.7 (Software Architectural Design)
**ASPICE Reference**: SWE.2 / SWE.3
**Version**: 2.24
**Date**: 2026-03-06
**Status**: Draft
**Project Title**: 주행 상황 실시간 경고 시스템
**Subtitle**: 구간 정보 및 긴급차량 접근 기반 앰비언트·클러스터 경보

| V-Model 위치 | 현재 문서 | 상위 연결 | 하위 연결 |
|---|---|---|---|
| 좌측 하단 (SWE.2/SWE.3) | `0304_System_Variables.md` | `0303_Communication_Specification.md` | `04_SW_Implementation.md` |

---

> 제출용 축소본: 원본 SoT에서 제출 핵심만 발췌한 문서입니다.

## 작성 원칙

- 본 문서는 시스템 변수 사전 및 추적 관계를 정의한다.
- 제출본은 상단 공식 변수 표를 유지하고, 하단 추적은 대표 행만 유지한다.
- 전체 변수 전수 매핑은 원문 0304에서 관리한다.
- Var-Comm-Flow 추적 키는 원문과 동일하게 유지한다.
- Pre-Activation/Legacy 라벨은 원문과 동일하게 유지한다.

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
| 30 | Infotainment | speedLimit | uint32 | 0 | 255 | 30 | 구간 제한속도(km/h) |
| 7 | V2X | emergencyType | uint32 | 0 | 3 | 0 | 긴급차량 종류 |
| 8 | V2X | emergencyDirection | uint32 | 0 | 3 | 0 | 긴급차량 접근 방향 |
| 9 | V2X | eta | uint32 | 0 | 255 | 0 | 긴급차량 ETA(유효값 0~255, 내부 invalid sentinel 65535) |
| 10 | V2X | sourceId | uint32 | 0 | 255 | 0 | 긴급 메시지 Source ID |
| 11 | V2X | alertState | uint32 | 0 | 1 | 0 | 긴급 메시지 Active/Clear 상태 |
| 12 | Core | vehicleSpeedNorm | uint32 | 0 | 255 | 0 | 게이트웨이 정규화 후 차량 속도 |
| 13 | Core | driveStateNorm | uint32 | 0 | 3 | 0 | 게이트웨이 정규화 후 주행 상태 |
| 14 | Core | steeringInputNorm | uint32 | 0 | 1 | 0 | 게이트웨이 정규화 후 조향 입력 |
| 31 | Core | speedLimitNorm | uint32 | 0 | 255 | 30 | 게이트웨이 정규화 후 구간 제한속도 |
| 32 | Core | proximityRiskLevel | uint32 | 0 | 100 | 0 | 긴급차량 근접 위험도 산정값 |
| 33 | Core | decelAssistReq | uint32 | 0 | 1 | 0 | 감속 보조 요청 플래그 |
| 34 | Core | failSafeMode | uint32 | 0 | 2 | 0 | 도메인 경로 단절 강등 모드 |
| 35 | CoreState | domainPathStatus | uint32 | 0 | 2 | 0 | 도메인 경로 상태(정상/열화/단절) |
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
| 27 | CoreState | lastEmergencyRxMs | uint32 | 0 | 60000 | 0 | 마지막 긴급 신호 수신 시각(ms) |
| 28 | CoreState | duplicatePopupGuard | uint32 | 0 | 5000 | 0 | 중복 팝업 억제 타이머(ms) |
| 29 | CoreState | arbitrationSnapshotId | uint32 | 0 | 65535 | 0 | 중재 스냅샷 식별자 |
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
| 113 | Chassis | EspActive | uint32 | 0 | 1 | 0 | ESP 활성 상태 |
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
| 179 | Powertrain | RoutingPolicy | uint32 | 0 | 255 | 0 | 도메인 라우팅 정책 |
| 180 | Powertrain | BoundaryStatus | uint32 | 0 | 255 | 0 | 도메인 경계 상태 |
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
| 204 | Chassis | EpsAssistState | uint32 | 0 | 7 | 0 | EPS 보조 상태 |
| 205 | Chassis | EpsFault | uint32 | 0 | 1 | 0 | EPS 고장 상태 |
| 206 | Chassis | EpsTorqueReq | uint32 | 0 | 255 | 0 | EPS 토크 요청 |
| 207 | Chassis | AbsCtrlState | uint32 | 0 | 7 | 0 | ABS 제어 상태 |
| 208 | Chassis | AbsSlipLevel | uint32 | 0 | 255 | 0 | ABS 슬립 레벨 |
| 209 | Chassis | EscCtrlState | uint32 | 0 | 7 | 0 | ESC 제어 상태 |
| 210 | Chassis | YawCtrlReq | uint32 | 0 | 255 | 0 | 요 모멘트 제어 요구 |
| 211 | Chassis | TcsActive | uint32 | 0 | 1 | 0 | TCS 활성 상태 |
| 212 | Chassis | TcsSlipRatio | uint32 | 0 | 255 | 0 | TCS 슬립 비율 |
| 213 | Chassis | BrakeTempFL | uint32 | 0 | 255 | 0 | 브레이크 전륜좌 온도 |
| 214 | Chassis | BrakeTempFR | uint32 | 0 | 255 | 0 | 브레이크 전륜우 온도 |
| 215 | Chassis | BrakeTempRL | uint32 | 0 | 255 | 0 | 브레이크 후륜좌 온도 |
| 216 | Chassis | BrakeTempRR | uint32 | 0 | 255 | 0 | 브레이크 후륜우 온도 |
| 217 | Chassis | SteeringAngle | int32 | -720 | 720 | 0 | 조향각 |
| 218 | Chassis | SteeringAngleRate | int32 | -1024 | 1023 | 0 | 조향각속도 |
| 219 | Chassis | WheelPulseFL | uint32 | 0 | 65535 | 0 | 전륜좌 휠 펄스 |
| 220 | Chassis | WheelPulseFR | uint32 | 0 | 65535 | 0 | 전륜우 휠 펄스 |
| 221 | Chassis | DamperMode | uint32 | 0 | 7 | 0 | 댐퍼 모드 |
| 222 | Chassis | RideHeight | uint32 | 0 | 255 | 0 | 차고 높이 |
| 223 | Chassis | TirePressFL | uint32 | 0 | 255 | 0 | 전륜좌 타이어 압력 |
| 224 | Chassis | TirePressFR | uint32 | 0 | 255 | 0 | 전륜우 타이어 압력 |
| 225 | Chassis | TirePressRL | uint32 | 0 | 255 | 0 | 후륜좌 타이어 압력 |
| 226 | Chassis | TirePressRR | uint32 | 0 | 255 | 0 | 후륜우 타이어 압력 |
| 227 | Chassis | ChassisDiagReqId | uint32 | 0 | 255 | 0 | Chassis 진단 요청 ID |
| 228 | Chassis | ChassisDiagReqAct | uint32 | 0 | 1 | 0 | Chassis 진단 요청 활성 |
| 229 | Chassis | ChassisDiagResId | uint32 | 0 | 255 | 0 | Chassis 진단 응답 ID |
| 230 | Chassis | ChassisDiagStatus | uint32 | 0 | 15 | 0 | Chassis 진단 결과 |
| 231 | Chassis | AdasChassisState | uint32 | 0 | 255 | 0 | ADAS 섀시 상태 코드 |
| 232 | Chassis | AdasHealthLevel | uint32 | 0 | 255 | 0 | ADAS 헬스 상태 코드 |
| 234 | Chassis | BrakePadWearFL | uint32 | 0 | 100 | 0 | 브레이크 패드 마모(전륜좌) |
| 235 | Chassis | BrakePadWearFR | uint32 | 0 | 100 | 0 | 브레이크 패드 마모(전륜우) |
| 236 | Chassis | RoadFrictionEst | uint32 | 0 | 255 | 0 | 노면 마찰 추정치 |
| 237 | Chassis | SurfaceType | uint32 | 0 | 15 | 0 | 노면 타입 |
| 238 | Body | CabinSetTemp | uint32 | 0 | 63 | 0 | 실내 설정 온도 |
| 239 | Body | BlowerLevel | uint32 | 0 | 15 | 0 | 블로워 레벨 |
| 240 | Body | VentMode | uint32 | 0 | 7 | 0 | 공조 벤트 모드 |
| 241 | Body | AcCompressorReq | uint32 | 0 | 1 | 0 | A/C 컴프레서 요청 |
| 242 | Body | MirrorFoldState | uint32 | 0 | 1 | 0 | 미러 폴딩 상태 |
| 243 | Body | MirrorHeatState | uint32 | 0 | 1 | 0 | 미러 열선 상태 |
| 244 | Body | MirrorAdjAxis | uint32 | 0 | 3 | 0 | 미러 조정 축 |
| 245 | Body | DriverSeatPos | uint32 | 0 | 255 | 0 | 운전석 시트 위치 |
| 246 | Body | PassengerSeatPos | uint32 | 0 | 255 | 0 | 동승석 시트 위치 |
| 247 | Body | SeatHeatLevel | uint32 | 0 | 7 | 0 | 시트 히터 레벨 |
| 248 | Body | SeatVentLevel | uint32 | 0 | 7 | 0 | 시트 통풍 레벨 |
| 249 | Body | DoorUnlockCmd | uint32 | 0 | 3 | 0 | 도어 언락 명령 |
| 250 | Body | TrunkOpenCmd | uint32 | 0 | 1 | 0 | 트렁크 오픈 명령 |
| 251 | Body | InteriorLampMode | uint32 | 0 | 7 | 0 | 실내등 모드 |
| 252 | Body | InteriorLampLevel | uint32 | 0 | 255 | 0 | 실내등 밝기 |
| 253 | Body | RainSensorLevel | uint32 | 0 | 255 | 0 | 우적 센서 레벨 |
| 254 | Body | AutoHeadlampReq | uint32 | 0 | 1 | 0 | 오토 헤드램프 요청 |
| 255 | Body | BcmDiagReqId | uint32 | 0 | 255 | 0 | BCM 진단 요청 ID |
| 256 | Body | BcmDiagReqAct | uint32 | 0 | 1 | 0 | BCM 진단 요청 활성 |
| 257 | Body | BcmDiagResId | uint32 | 0 | 255 | 0 | BCM 진단 응답 ID |
| 258 | Body | BcmDiagStatus | uint32 | 0 | 15 | 0 | BCM 진단 결과 |
| 259 | Body | ImmoState | uint32 | 0 | 3 | 0 | 이모빌라이저 상태 |
| 260 | Body | KeyAuthState | uint32 | 0 | 3 | 0 | 키 인증 상태 |
| 261 | Body | AlarmArmed | uint32 | 0 | 1 | 0 | 알람 경계 상태 |
| 262 | Body | AlarmTrigger | uint32 | 0 | 1 | 0 | 알람 트리거 상태 |
| 263 | Body | AlarmZone | uint32 | 0 | 15 | 0 | 알람 존 정보 |
| 264 | Body | BodyGatewayLoad | uint32 | 0 | 100 | 0 | Body GW 부하율 |
| 265 | Body | BodyGatewayRoute | uint32 | 0 | 255 | 0 | Body GW 라우팅 상태 |
| 266 | Body | ComfortMode | uint32 | 0 | 7 | 0 | 컴포트 모드 |
| 267 | Body | ChildSafetyState | uint32 | 0 | 1 | 0 | 아동 안전 상태 |
| 268 | Infotainment | AudioFocusOwner | uint32 | 0 | 7 | 0 | 오디오 포커스 소유자 |
| 269 | Infotainment | AudioDuckLevel | uint32 | 0 | 255 | 0 | 오디오 덕킹 레벨 |
| 270 | Infotainment | VoiceAssistState | uint32 | 0 | 7 | 0 | 음성비서 상태 |
| 271 | Infotainment | VoiceWakeSource | uint32 | 0 | 15 | 0 | 음성 깨우기 소스 |
| 272 | Infotainment | MapZoomLevel | uint32 | 0 | 255 | 0 | 지도 줌 레벨 |
| 273 | Infotainment | MapTheme | uint32 | 0 | 15 | 0 | 지도 테마 |
| 274 | Infotainment | NextTurnType | uint32 | 0 | 15 | 0 | 다음 회전 유형 |
| 275 | Infotainment | NextTurnDist | uint32 | 0 | 255 | 0 | 다음 회전 잔여 거리 |
| 276 | Infotainment | TrafficEventType | uint32 | 0 | 15 | 0 | 교통 이벤트 유형 |
| 277 | Infotainment | TrafficSeverity | uint32 | 0 | 7 | 0 | 교통 이벤트 심각도 |
| 278 | Infotainment | TrafficDist | uint32 | 0 | 255 | 0 | 이벤트 잔여 거리 |
| 279 | Infotainment | ProjectionType | uint32 | 0 | 7 | 0 | 프로젝션 유형 |
| 280 | Infotainment | ProjectionState | uint32 | 0 | 3 | 0 | 프로젝션 상태 |
| 281 | Cluster | ClusterNotifType | uint32 | 0 | 15 | 0 | 클러스터 알림 유형 |
| 282 | Cluster | ClusterNotifPrio | uint32 | 0 | 7 | 0 | 클러스터 알림 우선순위 |
| 283 | Infotainment | IviDiagReqId | uint32 | 0 | 255 | 0 | IVI 진단 요청 ID |
| 284 | Infotainment | IviDiagReqAct | uint32 | 0 | 1 | 0 | IVI 진단 요청 활성 |
| 285 | Infotainment | IviDiagResId | uint32 | 0 | 255 | 0 | IVI 진단 응답 ID |
| 286 | Infotainment | IviDiagStatus | uint32 | 0 | 15 | 0 | IVI 진단 결과 |
| 287 | Infotainment | MediaGenre | uint32 | 0 | 15 | 0 | 미디어 장르 |
| 288 | Infotainment | TrackProgress | uint32 | 0 | 100 | 0 | 트랙 진행률 |
| 289 | Infotainment | TtsState | uint32 | 0 | 7 | 0 | TTS 상태 |
| 290 | Infotainment | TtsLangId | uint32 | 0 | 255 | 0 | TTS 언어 ID |
| 291 | Infotainment | LteState | uint32 | 0 | 7 | 0 | LTE 연결 상태 |
| 292 | Infotainment | WifiState | uint32 | 0 | 1 | 0 | Wi-Fi 연결 상태 |
| 293 | Infotainment | BtState | uint32 | 0 | 1 | 0 | Bluetooth 연결 상태 |
| 294 | Infotainment | CpuLoad | uint32 | 0 | 100 | 0 | IVI CPU 부하율 |
| 295 | Infotainment | MemLoad | uint32 | 0 | 100 | 0 | IVI 메모리 부하율 |
| 296 | Cluster | ClusterSyncState | uint32 | 0 | 7 | 0 | 클러스터 동기화 상태 |
| 297 | Cluster | ClusterSyncSeq | uint32 | 0 | 255 | 0 | 클러스터 동기화 시퀀스 |
| 298 | Powertrain | EngineTorqueAct | uint32 | 0 | 65535 | 0 | 엔진 실제 토크 |
| 299 | Powertrain | EngineTorqueReq | uint32 | 0 | 65535 | 0 | 엔진 요구 토크 |
| 300 | Powertrain | EngineLoad | uint32 | 0 | 100 | 0 | 엔진 부하율 |
| 301 | Powertrain | ManifoldPressure | uint32 | 0 | 255 | 0 | 흡기 매니폴드 압력 |
| 302 | Powertrain | ShiftState | uint32 | 0 | 7 | 0 | 변속 상태 |
| 303 | Powertrain | ShiftInProgress | uint32 | 0 | 1 | 0 | 변속 진행 상태 |
| 304 | Powertrain | ShiftTargetGear | uint32 | 0 | 7 | 0 | 목표 기어 |
| 305 | Powertrain | PtDiagReqId | uint32 | 0 | 255 | 0 | Powertrain 진단 요청 ID |
| 306 | Powertrain | PtDiagReqAct | uint32 | 0 | 1 | 0 | Powertrain 진단 요청 활성 |
| 307 | Powertrain | PtDiagResId | uint32 | 0 | 255 | 0 | Powertrain 진단 응답 ID |
| 308 | Powertrain | PtDiagStatus | uint32 | 0 | 15 | 0 | Powertrain 진단 결과 |
| 309 | Powertrain | ThermalMode | uint32 | 0 | 7 | 0 | 열관리 모드 |
| 310 | Powertrain | FanSpeedCmd | uint32 | 0 | 255 | 0 | 팬 속도 명령 |
| 311 | Powertrain | RegenLevel | uint32 | 0 | 15 | 0 | 회생 제동 레벨 |
| 312 | Powertrain | EnergyFlowDir | uint32 | 0 | 3 | 0 | 에너지 흐름 방향 |
| 313 | Powertrain | PtCtrlAuthState | uint32 | 0 | 3 | 0 | 파워트레인 제어 권한 상태 |
| 314 | Powertrain | PtCtrlSource | uint32 | 0 | 15 | 0 | 파워트레인 제어 출처 |
---

## 변수 대표 추적 표 (축소본)

- 제출본은 대표 Var만 유지하고, 전수 Var 추적은 원문 SoT(`driving-situation-alert/0304_System_Variables.md`)에서 관리한다.

| Var ID | 표준 Name | Owner | Comm/Flow | Func/Req(대표) | 갱신 규칙 |
|---|---|---|---|---|---|
| Var_001 | vehicleSpeed | CHS_GW | Comm_001 / Flow_001 | Func_001, Func_010 / Req_001, Req_010 | 100ms CAN 수신 |
| Var_012 | vehicleSpeedNorm | ADAS_WARN_CTRL | Comm_001 / Flow_001 | Func_001, Func_006 / Req_001, Req_006 | GW 정규화 수신 시 |
| Var_018 | selectedAlertLevel | WARN_ARB_MGR | Comm_006 / Flow_006 | Func_022, Func_027 / Req_022, Req_027 | 중재 결과 생성 시 |
| Var_021 | ambientMode | BODY_GW, AMBIENT_CTRL | Comm_007 / Flow_007 | Func_035 / Req_035 | 50ms 출력 갱신 |
| Var_024 | warningTextCode | IVI_GW, CLU_HMI_CTRL | Comm_008 / Flow_008 | Func_040, Func_155 / Req_040, Req_155 | 50ms 출력 갱신 |
| Var_027 | lastEmergencyRxMs | EMS_ALERT | Comm_004~006 / Flow_004~006 | Func_023, Func_024 / Req_023, Req_024 | E100 수신 시각 기록 |
| Var_133 | TurnLampState | BODY_GW | Comm_103 / Flow_103 | Func_140 / Req_140 | 100ms 수신 |
| Var_191 | DriveMode | DOMAIN_ROUTER | Comm_105 / Flow_105 | Func_141 / Req_141 | 100ms 수신 |
| Var_320 | proximityRiskLevel | ADAS_WARN_CTRL | Comm_120 / Flow_120 | Func_120 / Req_120 | 100ms 위험도 산정 |
| Var_328 | failSafeMode | DOMAIN_BOUNDARY_MGR | Comm_124 / Flow_124 | Func_127, Func_129 / Req_127, Req_129 | 단절 감지 즉시 |
| Var_330 | objectTrackValid | ADAS_WARN_CTRL | Comm_130 / Flow_130 | Func_130, Func_148 / Req_130, Req_148 | 객체 입력 수신 시 |
| Var_339 | objectEventCode | EMS_ALERT | Comm_133 / Flow_133 | Func_138 / Req_138 | 이벤트 기록 시 |

> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

0302 네트워크 플로우 표에 메세지별로 추가하면 좋을 것 같은 신호들 정리해봤습니다.

## 0302 추가버전 네트워크 플로우 표
Channel	ID hex	Symbolic Name(message name)	Byte no.	Function	Bit no.	signal name	SIL_TEST_CTRL	CHASSIS_GW	INFOTAINMENT_GW	ETH_SWITCH	ADAS_WARN_CTRL	NAV_CONTEXT_MGR	EMS_POLICE_TX	EMS_AMB_TX	EMS_ALERT_RX	WARN_ARB_MGR	BODY_GW	IVI_GW	BCM_AMBIENT_CTRL	CLU_HMI_CTRL	[비고]
Chassis CAN	0x100	frmVehicleStateCanMsg	0	Vehicle State Check	0	vehicleSpeed	Tx	Rx													CAN 입력, 100ms
Chassis CAN	0x100	frmVehicleStateCanMsg	0	Vehicle State Check	1	vehicleSpeedValid	Tx	Rx													1:valid/0:invalid
Chassis CAN	0x100	frmVehicleStateCanMsg	1	Vehicle State Check	0	driveState	Tx	Rx
Chassis CAN	0x100	frmVehicleStateCanMsg	1	Vehicle State Check	1	ignitionState	Tx	Rx													0:OFF/1:ON
Chassis CAN	0x100	frmVehicleStateCanMsg	1	Vehicle State Check	4~7	msgCounter	Tx	Rx													4bit rolling counter
Chassis CAN	0x101	frmSteeringCanMsg	0	Steering Input Check	0	SteeringInput	Tx	Rx													CAN 입력, 100ms
Infotainment CAN	0x110	frmNavContextCanMsg	0	Zone Context Check	0	roadZone	Tx		Rx												CAN 입력, 100ms
Infotainment CAN	0x110	frmNavContextCanMsg	0	Zone Context Check	2	navDirection	Tx		Rx
Infotainment CAN	0x110	frmNavContextCanMsg	0	Zone Context Check	3	mapMatched	Tx		Rx												1:matched,0:unmatched
Infotainment CAN	0x110	frmNavContextCanMsg	0	Zone Context Check	4~7	msgCounter	Tx		Rx												4bit rolling counter
Infotainment CAN	0x110	frmNavContextCanMsg	1	Zone Context Check	0	zoneDistance	Tx		Rx
Infotainment CAN	0x110	frmNavContextCanMsg	2~3	Zone Context Check	0~15	speedLimit	Tx		Rx												km/h (uint16)
Ethernet	0x510	ethVehicleStateMsg	0	Gateway Normalized Vehicle State	0	vehicleSpeed		Tx		Rx	Rx										UDP, 100ms
Ethernet	0x510	ethVehicleStateMsg	0	Gateway Normalized Vehicle State	1	vehicleSpeedValid		Tx		Rx	Rx										normalized valid
Ethernet	0x510	ethVehicleStateMsg	1	Gateway Normalized Vehicle State	0	driveState		Tx		Rx	Rx
Ethernet	0x510	ethVehicleStateMsg	2~5	Gateway Normalized Vehicle State	0~31	sourceTimestamp		Tx		Rx	Rx										ms
Ethernet	0x510	ethVehicleStateMsg	6	Gateway Normalized Vehicle State	0~7	aliveCounter		Tx		Rx	Rx										8bit rolling counter
Ethernet	0x510	ethVehicleStateMsg	7~8	Gateway Normalized Vehicle State	0~15	crc		Tx		Rx	Rx										16bit CRC
Ethernet	0x511	ethSteeringMsg	0	Gateway Normalized Steering	0	SteeringInput		Tx		Rx	Rx										UDP, 100ms
Ethernet	0x512	ethNavContextMsg	0	Gateway Normalized Nav Context	0	roadZone			Tx	Rx		Rx				Rx					UDP, 100ms
Ethernet	0x512	ethNavContextMsg	0	Gateway Normalized Nav Context	2	navDirection			Tx	Rx		Rx				Rx
Ethernet	0x512	ethNavContextMsg	0	Gateway Normalized Nav Context	3	mapMatched			Tx	Rx		Rx				Rx					1:matched,0:unmatched
Ethernet	0x512	ethNavContextMsg	1	Gateway Normalized Nav Context	0	zoneDistance			Tx	Rx		Rx				Rx
Ethernet	0x512	ethNavContextMsg	2~3	Gateway Normalized Nav Context	0~15	speedLimit			Tx	Rx		Rx				Rx					km/h (uint16)
Ethernet	0x512	ethNavContextMsg	4	Gateway Normalized Nav Context	0~7	aliveCounter			Tx	Rx		Rx				Rx					8bit rolling counter
Ethernet	0x512	ethNavContextMsg	5~8	Gateway Normalized Nav Context	0~31	timestamp			Tx	Rx		Rx				Rx					ms
Ethernet	0x512	ethNavContextMsg	9~10	Gateway Normalized Nav Context	0~15	crc			Tx	Rx		Rx				Rx					16bit CRC
Ethernet	0xE100	ETH_EmergencyAlert	0	Emergency Alert Tx/Rx	0	EmergencyType				Rx			Tx	Tx	Rx						UDP, 100ms
Ethernet	0xE100	ETH_EmergencyAlert	0	Emergency Alert Tx/Rx	2	EmergencyDirection				Rx			Tx	Tx	Rx
Ethernet	0xE100	ETH_EmergencyAlert	1	Emergency Alert Tx/Rx	0	ETA				Rx			Tx	Tx	Rx
Ethernet	0xE100	ETH_EmergencyAlert	2	Emergency Alert Tx/Rx	0	SourceID				Rx			Tx	Tx	Rx
Ethernet	0xE100	ETH_EmergencyAlert	3	Emergency Alert Tx/Rx	0	AlertState(Active/Clear)				Rx			Tx	Tx	Rx
Ethernet	0xE100	ETH_EmergencyAlert	3	Emergency Alert Tx/Rx	1~4	cancelReason				Rx			Tx	Tx	Rx						clear reason (0~15)
Ethernet	0xE100	ETH_EmergencyAlert	4~5	Emergency Alert Tx/Rx	0~15	eventId				Rx			Tx	Tx	Rx						16bit event id
Ethernet	0xE100	ETH_EmergencyAlert	6~7	Emergency Alert Tx/Rx	0~15	distanceToEvent				Rx			Tx	Tx	Rx						m (uint16)
Ethernet	0xE200	ethSelectedAlertMsg	0	Arbitration Result Distribution	0	AlertLevel				Rx						Tx	Rx	Rx			UDP, 50ms
Ethernet	0xE200	ethSelectedAlertMsg	0	Arbitration Result Distribution	3	AlertType				Rx						Tx	Rx	Rx
Ethernet	0xE200	ethSelectedAlertMsg	1	Arbitration Result Distribution	0	TimeoutClear				Rx						Tx	Rx	Rx
Ethernet	0xE200	ethSelectedAlertMsg	2	Arbitration Result Distribution	0~7	selectedSourceId				Rx						Tx	Rx	Rx			source id
Ethernet	0xE200	ethSelectedAlertMsg	3	Arbitration Result Distribution	0~1	displayTarget				Rx						Tx	Rx	Rx			0:CLU 1:IVI 2:Both
Ethernet	0xE200	ethSelectedAlertMsg	3	Arbitration Result Distribution	2~3	audibleTarget				Rx						Tx	Rx	Rx			0:off 1:buzzer 2:sound
Ethernet	0xE200	ethSelectedAlertMsg	3	Arbitration Result Distribution	4~7	fallbackReason				Rx						Tx	Rx	Rx			timeout/invalid/priority etc (0~15)
Ethernet	0xE200	ethSelectedAlertMsg	4~5	Arbitration Result Distribution	0~15	hmiDurationMs				Rx						Tx	Rx	Rx			ms (uint16)
Body CAN	0x210	frmAmbientControlMsg	0	Ambient Pattern Control	0	AmbientMode											Tx		Rx		CAN 출력, 50ms
Body CAN	0x210	frmAmbientControlMsg	0	Ambient Pattern Control	3	AmbientColor											Tx		Rx
Body CAN	0x210	frmAmbientControlMsg	0	Ambient Pattern Control	6	AmbientPattern											Tx		Rx
Body CAN	0x210	frmAmbientControlMsg	1	Ambient Pattern Control	0	ambientEnable											Tx		Rx		1:on 0:off
Body CAN	0x210	frmAmbientControlMsg	2	Ambient Pattern Control	0~7	patternSpeed											Tx		Rx		0~255
Infotainment CAN	0x220	frmClusterWarningMsg	0	Cluster Warning Display	0	WarningTextCode												Tx		Rx	CAN 출력, 50ms
Infotainment CAN	0x220	frmClusterWarningMsg	1	Cluster Warning Display	0~3	warningCategory												Tx		Rx	Speed/Emergency etc
Infotainment CAN	0x220	frmClusterWarningMsg	2~3	Cluster Warning Display	0~15	warningDurationMs												Tx		Rx	ms (uint16)
Test CAN	0x230	frmTestResultMsg	0	Scenario Result Report	0	ScenarioResult	Tx														Event
Test CAN	0x230	frmTestResultMsg	1	Scenario Result Report	0~7	failReason	Tx														reason code
Test CAN	0x230	frmTestResultMsg	2~5	Scenario Result Report	0~31	timestamp	Tx														ms


## 추가할 신호 추천
Channel	ID hex	Symbolic Name(message name)	Byte no.	Function	Bit no.	signal name	SIL_TEST_CTRL	CHASSIS_GW	INFOTAINMENT_GW	ETH_SWITCH	ADAS_WARN_CTRL	NAV_CONTEXT_MGR	EMS_POLICE_TX	EMS_AMB_TX	EMS_ALERT_RX	WARN_ARB_MGR	BODY_GW	IVI_GW	BCM_AMBIENT_CTRL	CLU_HMI_CTRL	[비고]

Chassis CAN	0x100	frmVehicleStateCanMsg	1	Vehicle State Check	1	vehicleSpeedValid	Tx	Rx													1:valid/0:invalid
Chassis CAN	0x100	frmVehicleStateCanMsg	1	Vehicle State Check	2	ignitionState	Tx	Rx													0:OFF/1:ON
Chassis CAN	0x100	frmVehicleStateCanMsg	1	Vehicle State Check	4~7	msgCounter	Tx	Rx													4bit rolling counter

Infotainment CAN	0x110	frmNavContextCanMsg	1	Zone Context Check	4~7	speedLimit	Tx		Rx												km/h
Infotainment CAN	0x110	frmNavContextCanMsg	2	Zone Context Check	0	mapMatched	Tx		Rx												1:matched
Infotainment CAN	0x110	frmNavContextCanMsg	2	Zone Context Check	4~7	msgCounter	Tx		Rx												4bit counter

Ethernet	0x510	ethVehicleStateMsg	2	Gateway Normalized Vehicle State	0~31	sourceTimestamp		Tx		Rx	Rx										ms
Ethernet	0x510	ethVehicleStateMsg	3	Gateway Normalized Vehicle State	0	vehicleSpeedValid		Tx		Rx	Rx										normalized valid
Ethernet	0x510	ethVehicleStateMsg	3	Gateway Normalized Vehicle State	8~15	aliveCounter		Tx		Rx	Rx										8bit
Ethernet	0x510	ethVehicleStateMsg	4	Gateway Normalized Vehicle State	0~15	crc		Tx		Rx	Rx										16bit CRC

Ethernet	0x512	ethNavContextMsg	2	Gateway Normalized Nav Context	0~15	speedLimit		 	Tx	Rx		Rx									km/h
Ethernet	0x512	ethNavContextMsg	2	Gateway Normalized Nav Context	16	mapMatched		 	Tx	Rx		Rx									1:matched
Ethernet	0x512	ethNavContextMsg	3	Gateway Normalized Nav Context	0~7	aliveCounter		 	Tx	Rx		Rx									8bit
Ethernet	0x512	ethNavContextMsg	3	Gateway Normalized Nav Context	8~23	crc		 	Tx	Rx		Rx									16bit
Ethernet	0x512	ethNavContextMsg	4	Gateway Normalized Nav Context	0~31	timestamp		 	Tx	Rx		Rx									ms

Ethernet	0xE100	ETH_EmergencyAlert	4	Emergency Alert	0~15	eventId				Rx		 	Tx	Tx	Rx						16bit event id
Ethernet	0xE100	ETH_EmergencyAlert	5	Emergency Alert	0~15	distanceToEvent				Rx		 	Tx	Tx	Rx						m
Ethernet	0xE100	ETH_EmergencyAlert	3	Emergency Alert	1~4	cancelReason				Rx		 	Tx	Tx	Rx						clear reason code

Ethernet	0xE200	ethSelectedAlertMsg	1	Arbitration Result Distribution	0~15	selectedSourceId				Rx						Tx	Rx	Rx			source node id
Ethernet	0xE200	ethSelectedAlertMsg	1	Arbitration Result Distribution	16~17	displayTarget				Rx						Tx	Rx	Rx			0:CLU 1:IVI 2:Both
Ethernet	0xE200	ethSelectedAlertMsg	1	Arbitration Result Distribution	18~19	audibleTarget				Rx						Tx	Rx	Rx			0:off 1:buzzer 2:sound
Ethernet	0xE200	ethSelectedAlertMsg	2	Arbitration Result Distribution	0~15	hmiDurationMs				Rx						Tx	Rx	Rx			ms
Ethernet	0xE200	ethSelectedAlertMsg	2	Arbitration Result Distribution	16~19	fallbackReason				Rx						Tx	Rx	Rx			timeout/invalid/priority

Body CAN	0x210	frmAmbientControlMsg	1	Ambient Pattern Control	0	ambientEnable											Tx		Rx		1:on
Body CAN	0x210	frmAmbientControlMsg	1	Ambient Pattern Control	8~15	patternSpeed											Tx		Rx		pattern speed

Infotainment CAN	0x220	frmClusterWarningMsg	1	Cluster Warning Display	0~3	warningCategory												Tx		Rx	Speed/Emergency
Infotainment CAN	0x220	frmClusterWarningMsg	2	Cluster Warning Display	0~15	warningDurationMs												Tx		Rx	ms

Test CAN	0x230	frmTestResultMsg	1	Scenario Result Report	0~7	failReason	Tx														reason code
Test CAN	0x230	frmTestResultMsg	2	Scenario Result Report	0~31	timestamp	Tx														ms


## 시스템 변수표
ID	Namespace	Name	Data type	Min	Max	Initial Value	Description
1	Chassis	vehicleSpeedValid	bool	0	1	0	차량 속도 유효 플래그 (0:invalid, 1:valid)
2	Chassis	ignitionState	enum	0	1	0	시동 상태 (0:OFF, 1:ON)
3	Chassis	msgCounter	uint8	0	15	0	VehicleState 메시지 4bit rolling counter

4	Infotainment	speedLimit	uint16	0	300	0	내비 기반 제한 속도 (km/h)
5	Infotainment	mapMatched	bool	0	1	0	지도 매칭 여부 (0:no, 1:matched)
6	Infotainment	msgCounterNav	uint8	0	15	0	NavContext 메시지 4bit rolling counter

7	Core	sourceTimestamp	uint32	0	4294967295	0	Gateway 수신 원본 타임스탬프(ms)
8	Core	vehicleSpeedValidNorm	bool	0	1	0	정규화 후 속도 유효 플래그
9	Core	aliveCounterVehicle	uint8	0	255	0	VehicleState Ethernet alive counter
10	Core	crcVehicle	uint16	0	65535	0	VehicleState Ethernet CRC

11	Core	speedLimitNorm	uint16	0	300	0	Gateway 정규화 후 제한속도
12	Core	mapMatchedNorm	bool	0	1	0	Gateway 정규화 후 map matched
13	Core	aliveCounterNav	uint8	0	255	0	NavContext Ethernet alive counter
14	Core	crcNav	uint16	0	65535	0	NavContext Ethernet CRC
15	Core	timestampNav	uint32	0	4294967295	0	NavContext 수신 시각(ms)

16	V2X	eventId	uint16	0	65535	0	긴급 이벤트 인스턴스 ID
17	V2X	distanceToEvent	uint16	0	10000	0	긴급 이벤트까지 거리(m)
18	V2X	cancelReason	uint8	0	15	0	긴급 이벤트 해제 사유 코드

19	Core	selectedSourceId	uint16	0	65535	0	중재 결과 선택된 소스 ID
20	Core	displayTarget	enum	0	2	0	표시 대상 (0:CLU, 1:IVI, 2:Both)
21	Core	audibleTarget	enum	0	2	0	음향 출력 대상 (0:off, 1:buzzer, 2:sound)
22	Core	hmiDurationMs	uint16	0	60000	0	HMI 표시 유지 시간(ms)
23	Core	fallbackReason	uint8	0	15	0	중재 fallback 사유 코드

24	Body	ambientEnable	bool	0	1	0	엠비언트 조명 활성 여부
25	Body	patternSpeed	uint8	0	255	0	엠비언트 패턴 속도

26	Cluster	warningCategory	enum	0	7	0	경고 카테고리 (Speed/Emergency 등)
27	Cluster	warningDurationMs	uint16	0	60000	0	경고 표시 유지 시간(ms)

28	Test	failReason	uint8	0	255	0	테스트 실패 원인 코드
29	Test	timestamp	uint32	0	4294967295	0	테스트 결과 기록 시간(ms)


## 변수표현 속성 보강 표
Name(표준)	Internal Name(구현)	Unit	Scale	Endian	Invalid Value	비고
vehicleSpeedValid	vehicleSpeedValid_CAN_IN	bool	1	Little	255	0:invalid, 1:valid
ignitionState	ignitionState_CAN_IN	enum	1	Little	255	0:OFF, 1:ON
msgCounter	msgCounter_CAN_IN	counter	1	Little	255	4bit rolling counter (0~15)

speedLimit	speedLimit_CAN_IN	km/h	1	Little	65535	제한속도 미수신/미매칭 시 invalid
mapMatched	mapMatched_CAN_IN	bool	1	Little	255	0:not matched, 1:matched
msgCounterNav	msgCounterNav_CAN_IN	counter	1	Little	255	4bit rolling counter (0~15)

sourceTimestamp	sourceTimestamp_ETH_CORE	ms	1	Little	4294967295	GW 수신 원본 타임스탬프 미기록 값
vehicleSpeedValidNorm	vehicleSpeedValidNorm_ETH_CORE	bool	1	Little	255	GW 정규화 후 속도 유효 플래그
aliveCounterVehicle	aliveCounterVehicle_ETH_CORE	counter	1	Little	255	UDP 누락 감지용 rolling counter (0~255)
crcVehicle	crcVehicle_ETH_CORE	crc16	1	Little	65535	CRC 미검증/미적용 시 invalid

speedLimitNorm	speedLimitNorm_ETH_CORE	km/h	1	Little	65535	GW 정규화 후 제한속도 invalid
mapMatchedNorm	mapMatchedNorm_ETH_CORE	bool	1	Little	255	GW 정규화 후 map matched
aliveCounterNav	aliveCounterNav_ETH_CORE	counter	1	Little	255	UDP 누락 감지용 rolling counter (0~255)
crcNav	crcNav_ETH_CORE	crc16	1	Little	65535	CRC 미검증/미적용 시 invalid
timestampNav	timestampNav_ETH_CORE	ms	1	Little	4294967295	수신 시각 미기록 값

eventId	eventId_ETH_IN	id	1	Little	65535	긴급 이벤트 인스턴스 식별자
distanceToEvent	distanceToEvent_ETH_IN	m	1	Little	65535	거리 미산출/미수신 시 invalid
cancelReason	cancelReason_ETH_IN	enum	1	Little	255	Clear 시 해제 사유 코드 (0~15 외 invalid)

selectedSourceId	selectedSourceId_ETH_CORE	id	1	Little	65535	중재 결과 선택된 소스 ID
displayTarget	displayTarget_ETH_CORE	enum	1	Little	255	0:CLU, 1:IVI, 2:Both
audibleTarget	audibleTarget_ETH_CORE	enum	1	Little	255	0:off, 1:buzzer, 2:sound
hmiDurationMs	hmiDurationMs_ETH_CORE	ms	1	Little	65535	HMI 표시 유지 시간(ms) 미설정 시 invalid
fallbackReason	fallbackReason_ETH_CORE	enum	1	Little	255	timeout/invalid/priority 등 (0~15 외 invalid)

ambientEnable	ambientEnable_CAN_OUT	bool	1	Little	255	0:off, 1:on
patternSpeed	patternSpeed_CAN_OUT	step	1	Little	255	패턴 속도 단계/비율(프로젝트 정의)

warningCategory	warningCategory_CAN_OUT	enum	1	Little	255	Speed/Emergency 등 카테고리 코드
warningDurationMs	warningDurationMs_CAN_OUT	ms	1	Little	65535	경고 표시 유지 시간(ms) 미설정 시 invalid

failReason	failReason_OUTPUT	code	1	Little	255	테스트 실패 원인 코드
timestamp	timestamp_OUTPUT	ms	1	Little	4294967295	결과 기록 시간 미기록 값

## 1) Chassis CAN 0x100 `frmVehicleStateCanMsg` (CAN 입력, 100ms)

**추가 추천 signals**

- `vehicleSpeedValid` (1b)

: 시스템 신뢰성 확보용으로 추가하면 좋을 것 같음

```cpp
if (vehicleSpeedValid == 1)
{
    if (vehicleSpeed > speedLimit)
        과속 경고
}
else
{
    과속 판단 안 함
}
```

- 이 속도는 **정상 계산/정상 수신된 값이다**
- 이 속도는 **신뢰 가능하다**

(자동차 소프트웨어는 ISO 26262 같은 기능 안전 체계 때문에 "이 값이 신뢰 가능한지?" 를 항상 분리해서 관리함.)

- `ignitionState` (OFF/ACC/ON/CRANK) (2~3b)

: 차량 시동 상태를 나타내는 신호

| 값 | 의미 |
| --- | --- |
| 0 | OFF (완전 꺼짐) |
| 1 | ACC (오디오만 켜짐) |
| 2 | ON (계기판/ECU 전원 활성) |
| 3 | CRANK (시동 거는 중) |

```cpp
//예시
if (ignitionState == ON && driveState == D)
    과속 판단 수행
```

- `msgCounter` (4b)

: 메시지가 정상적으로 연속 수신되는지 확인

(통신 끊김 / 드랍 / 순서 꼬임을 탐지하는 용도)

---

## 2) Infotainment CAN 0x110 `frmNavContextCanMsg` (CAN 입력, 100ms)

**추가 추천 signals**

- `speedLimit` (8~16b)

: vehicleSpeed > speedLimit → 과속 판단하려면 구체적인 제한 속도 값이 필요할

- `mapMatched` (1b)

: 현재 차량 위치가 지도 위의 정확한 도로 구간에 매칭이되었는지 확인하는 용도 (잘못된 도로의 속도제한을 쓰면 오경고 터짐)

- `msgCounter` (4b)

---

## 3) Ethernet 0x510 `ethVehicleStateMsg` (UDP, 100ms)

**추가 추천 signals (Gateway 정규화용)**

- `sourceTimestamp` (32b) *(수신 원본 시간)*

: CAN에서 받은 **원본 차량 속도 데이터가 생성된 시간**

(CAN → Gateway → Ethernet 과정에서 지연이 발생할 수 있음

오래된 속도값으로 과속 판단하면 오동작 가능)

- `vehicleSpeedValid` (1b)

: 속도 데이터가 정상인지 여부 (Invalid 입력 시 과속 판단 차단→오경고 방지)

- `aliveCounter` (8b)

: 메시지 순번 증가 카운터 (UCP는 패킷 드랍  될 수도 있음 → 누락 여부 감지 위해 필요)

- `crc` (16b)

:Ethernet payload 무결성 체크  (UDP는 신뢰성 보장 안 함)

---

## 4) Ethernet 0x511 `ethSteeringMsg` (UDP, 100ms)

**추가 추천 signals**

- `aliveCounter` (8b)
- `crc` (16b)
- `timestamp` (32b)

---

## 5) Ethernet 0x512 `ethNavContextMsg` (UDP, 100ms)

**추가 추천 signals**

- `speedLimit` (16b)
- `mapMatched` (1b)
- `aliveCounter` (8b)
- `crc` (16b)
- `timestamp` (32b)

: 네비 컨텍스트 데이터가 생성된 시간

---

## 6) Ethernet 0xE100 `ETH_EmergencyAlert` (UDP, 100ms)

**추가 추천 signals**

- `eventId` (16~32b)

: 개별 이벤트를 구분하는 번호

ex) 경찰차 1대 지나감→ 10초 후 다른 경찰차 접근

이건 서로 다른 이벤트임. 근데 emergencyType은 1로 같음 → eventId로 서로 다른 경찰차임을 구분

```cpp
eventId = 1001  (첫 번째 경찰차)
eventId = 1057  (두 번째 경찰차)
```

→ 중복 팝업 방지+새 이벤트 감지+로그 추적+ 중재 안정성

(근데 경찰차,구급차 각각 1대씩만 사용한다면 굳이 필요 없을 듯)

- `distanceToEvent` (16b)

: 현재 시민 차량의 위치와 긴급차 위치 간의 거리 (보통 m 단위)

- `cancelReason` (Clear 시) (4b)

: `alertState`가 `active → clear`로 바뀌는 순간에, “왜 clear 됐는지”를 4bit 코드로 알려주는 신호

예:

0 = 정상 종료

1 = 시간 초과

2 = 거리 초과

3 = 신뢰도 낮음

- `aliveCounter` (8b)
- `crc` (16b)

---

## 7) Ethernet 0xE200 `ethSelectedAlertMsg` (UDP, 50ms)

**추가 추천 signals (중재 결과 배포)**

- `selectedSourceId` (8~16b)
최종 경고가 **어느 입력 소스에서 왔는지**(긴급차인지, 과속인지 등) 식별하는 ID.

(같은 `selectedAlertType`라도 “어디서 온 경고인지”를 로그로 추적 가능

디버깅/테스트에서 “중재가 진짜 의도대로 동작했나?” 확인이 쉬움)

- `displayTarget` (CLU/IVI/Both) (2b)

: 이 경고를 어디 화면에 띄울지 결정

예)

0: off

1: buzzer(단순 부저)

2: sound(스피커/오디오)

3: both(필요시)

- `audibleTarget` (buzzer/sound/off) (2b)

: 경고음을 어떤 방식으로 낼지 지정

예)

0: off

1: buzzer(단순 부저)

2: sound(스피커/오디오)

3: both(필요시)

→ 경고 레벨에 따라 소리를 달리해야 UX가 안정적

→ 긴급차는 강한 사운드, 과속은 약한 부저 같은 정책 결과 메시지로 확정해줄 수 있음

- `hmiDurationMs` (16b)

: 경고 표시/사운드를 **얼마나 유지할지**(ms)

- `fallbackReason` (timeout/invalid/priority 등) (4b)

: 정상 흐름이 아니라, **대체/예외 처리로 선택된 이유**

예)

0: none(정상 선택)

1: timeout(다른 소스 끊김)

2: invalid(입력값 invalid)

3: priority rule(우선순위로 밀림)

4: duplicate guard(중복 방지)

5: manual override …

→ 왜 이 경고가 선택되었는지 한번에 설명 가능

- `aliveCounter` (8b)
- `crc` (16b)

---

## 8) Body CAN 0x210 `frmAmbientControlMsg` (CAN 출력, 50ms)

**추가 추천 signals**

- `ambientEnable` (1b)

: 엠비언트 조명을 **켜는지/끄는지**를 명확히 하는 스위치.
→ `ambientMode=0`을 “기본값/안전값”으로 쓰고 있지만,

그게 “OFF”인지 “기본 모드(흰색 고정)”인지 애매

→ Enable이 있으면 해석이 명확해짐:

`ambientEnable=0` → 무조건 OFF(출력 차단)

`ambientEnable=1` → 아래 Mode/Color/Pattern 설정 적용

- `patternSpeed` (8b)

: 패턴(점멸/흐름)의 **재생 속도**

→  `ambientPattern`이 “무슨 패턴인지(종류)”만 말해주고 “얼마나 빠르게”는 표현이 안 됨.

→ 경고 레벨이 높을수록 패턴을 빠르게 해서 긴급도를 표현 가능

---

## 9) Infotainment CAN 0x220 `frmClusterWarningMsg` (CAN 출력, 50ms)

**추가 추천 signals**

- `warningCategory` (Speed/Emergency 등) (3~4b)

- `warningDurationMs` (16b)

: 경고를 **몇 ms 동안 유지할지**

---

## 10) Test CAN 0x230 `frmTestResultMsg` (Event)

**추가 추천 signals**

- `failReason` (8b)

: Fail일 때 실패 원인 코드

예)

1 = timeout (기대 신호 미수신)

2 = wrong alert type (경고 타입 다름)

3 = wrong level (경고 레벨 다름)

4 = value out of range (측정값 범위 벗어남)

5 = wrong display target (표시 대상 다름

- `timestamp` (32b)

:결과가 기록된 시간 (ms)

→ 이벤트성 메시지는 언제 발생했는지가 중요

예) “과속 입력 주입 후 180ms에 경고가 떴다” 같은 분석 가능

---

## 만약 추가한다면 같이 추가해야 하는 신호 정리

- `speedLimit`은 **0x110 + 0x512 에 같이 넣어야함**
- `mapMatched`도 **0x110 + 0x512 에 같이 넣어야함**
- `msgCounter / aliveCounter / crc`는 “신뢰성 강조 옵션 세트”

- `vehicleSpeedValid`는 **0x100 + 0x510 세트**
- `sourceTimestamp / crc`는 “ETH만 추가해도 OK”
- `displayTarget + audibleTarget + hmiDurationMs`는 **E200 세트**

→“어디에/어떤 소리로/얼마나”가 한 덩어리 HMI 정책이기 때문에 세트로 넣으면 좋음

- `warningDurationMs(0x220)` 넣을 거면
→ 상위에서 결정된 `hmiDurationMs(E200)`와 **동일하거나 매핑 규칙이 있어야 자연스러움**.
- `warningCategory(0x220)`는 `selectedSourceId(E200)` 또는 `selectedAlertType` 매핑으로 결정 가능
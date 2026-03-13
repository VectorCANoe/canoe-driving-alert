# ESC 코드 설명

## 개요

이 문서는 [ESC.can](C:\Users\Kimtaekcheon\Documents\canoe-driving-alert\canoe\cfg\channel_assign\Chassis\ESC.can)의 현재 리팩터링된 구조를 기준으로, ESC 주기 로직이 어떤 입력을 받아 어떤 상태를 계산하고 어떤 메시지를 송신하는지 설명한다.

현재 코드는 다음 방향으로 정리되어 있다.

- 복잡한 조건식은 `is...` helper 함수로 분리
- 계산 규칙과 상태 선택은 `derive...` 함수로 분리
- 매직 넘버는 `variables` 블록의 `const int`로 상수화
- boolean처럼 쓰이는 값은 `is...` 이름으로 명확히 표현

즉, `tEscCycle` 본문은 세부 수식보다 “어떤 상태를 계산하고 어떤 메시지를 내보내는지”가 먼저 읽히도록 구성되어 있다.

## 입력과 내부 상태

ESC는 다음 입력을 받아 내부 상태를 유지한다.

### 1. 차량 상태 입력

`on message frmVehicleStateCanMsg`에서 다음 값을 갱신한다.

- `gSpeedNorm`
- `gDriveState`

두 값 모두 clamp 처리되어 내부 계산에서 안전한 범위로 유지된다.

### 2. 조향 입력

`on message frmSteeringCanMsg`에서는 `SteeringInput`을 읽어 `gIsSteeringInputActive`에 저장한다.

이 변수는 단순 숫자가 아니라 조향 입력 유무를 나타내는 boolean 플래그로 사용된다.

### 3. 브레이크 입력

`on message frmPedalInputCanMsg`에서는 `BrakePedal`을 읽어 `gBrakePedal`에 저장하고, 같은 값을 `@Core::brakePedalNorm`에도 반영한다.

즉, ESC 내부 계산과 시스템 공통 상태가 같은 브레이크 입력을 참조하게 된다.

## helper 함수 구조

리팩터링 후 `tEscCycle`에서 사용하는 주요 helper 함수는 다음과 같다.

### boolean 판단 함수

- `isAbsActiveCondition(...)`
- `isEspActiveCondition(...)`
- `isEscLogUpdateRequired(...)`

이 함수들은 복잡한 조건식을 본문에서 직접 읽지 않도록 감춘다.

### 상태/계산 함수

- `normalizeDecelAssistRequestFlag(...)`
- `applyAssistBrakePedalFloor(...)`
- `deriveBrakePressure(...)`
- `deriveAbsSlipLevel(...)`
- `deriveBrakeModeCode(...)`
- `deriveEscCtrlStateCode(...)`
- `deriveEscInterventionLevel(...)`
- `deriveSuspensionModeCode(...)`

이 함수들은 “무엇을 계산하는지”를 이름에서 드러내고, 실제 수식은 내부로 숨긴다.

## 주기 로직 설명

### 1. 감속 보조 요청을 정규화하고 최소 브레이크 페달을 보정한다

주기 시작 시 ESC는 `@Core::decelAssistReq`를 읽어 `isDecelAssistRequested`로 정규화한다.

그 다음 `applyAssistBrakePedalFloor(...)`를 사용해 `appliedBrakePedal`을 만든다.

의미는 다음과 같다.

- 감속 보조 요청이 없으면 현재 브레이크 페달 값을 그대로 사용
- 감속 보조 요청이 있고 브레이크 입력이 너무 작으면 최소 보조 제동 수준까지 끌어올림

즉, 운전자가 브레이크를 강하게 밟지 않았더라도 감속 보조 요청이 있으면 ESC가 일정 수준의 제동 기준을 확보하도록 만든다.

### 2. 브레이크 압력, ABS, ESP 관련 상태를 계산한다

그 다음 ESC는 다음 값을 계산한다.

- `brakePressure = deriveBrakePressure(appliedBrakePedal)`
- `isAbsActive = isAbsActiveCondition(appliedBrakePedal, gSpeedNorm)`
- `absSlip = deriveAbsSlipLevel(isAbsActive, appliedBrakePedal)`
- `isEspActive = isEspActiveCondition(appliedBrakePedal, gIsSteeringInputActive)`

즉, 현재 브레이크 입력과 속도, 조향 입력을 바탕으로 ABS/ESP 동작 여부와 관련 상태를 만든다.

### 3. yaw/lat accel용 보조 값을 만든다

이후에는 다음 값을 만든다.

- `yawRate`
- `latAccel`

현재 구현은 단순 모델이다.

- `yawRate`는 조향 입력 플래그에 비례
- `latAccel`은 현재 속도값을 그대로 사용

즉, 실제 동역학 모델이라기보다 SIL용 간단한 상태 생성 로직에 가깝다.

### 4. 바퀴 속도와 Yaw/Accel 메시지를 송신한다

다음 두 메시지를 먼저 만든다.

- `frmWheelSpeedMsg`
- `frmYawAccelMsg`

각 바퀴 속도는 현재 `gSpeedNorm`으로 채워지고, yaw/lat accel도 앞서 계산한 값을 사용한다.

즉, ESC는 현재 차속과 기초 동역학 상태를 먼저 외부에 publish한다.

### 5. 브레이크 상태 메시지를 구성한다

`frmBrakeStatusMsg`에는 다음이 들어간다.

- `BrakePressure`
- `BrakeMode`
- `AbsActive`
- `EspActive`

여기서 `BrakeMode`는 `deriveBrakeModeCode(...)`로 계산되며, 단순 pedal 값이 아니라 제동 상태 코드로 변환된다.

즉, 브레이크 입력 자체보다 ESC 관점의 브레이크 상태 표현을 송신하는 단계다.

### 6. Chassis health를 송신하고 alive counter를 증가시킨다

`frmChassisHealthMsg`에는 다음이 들어간다.

- `ChassisAliveCnt`
- `ChassisFailCode`

그 후 alive counter는 마스크를 유지하면서 증가한다.

즉, 주기적으로 chassis domain이 살아 있음을 외부에 알리는 heartbeat 역할을 한다.

### 7. ESC 상태 메시지를 구성한다

`frmEscStateMsg`에는 다음이 반영된다.

- `EscCtrlState = deriveEscCtrlStateCode(isEspActive)`
- `EscIntervention = deriveEscInterventionLevel(isEspActive, appliedBrakePedal)`
- `EscYawTarget = ESC_ESC_YAW_TARGET_DEFAULT`

즉, ESP 개입 여부와 개입 정도를 명시적인 상태 코드와 intervention 값으로 내보낸다.

### 8. 브레이크 온도와 브레이크 마모 수준을 송신한다

다음 두 메시지는 단순 모델 기반으로 만들어진다.

- `frmBrakeTempMsg`
- `frmBrakeWearMsg`

브레이크 온도는 기본 온도에 pedal 비례 증가분을 더하고, 브레이크 마모 수준은 현재 고정 기본값을 사용한다.

즉, 실제 물리 모델이라기보다 테스트 및 시각화용 상태 생성에 가깝다.

### 9. 서스펜션 상태와 노면 마찰 계수를 송신한다

ESC는 다음도 함께 송신한다.

- `frmSuspensionStateMsg`
- `frmRoadFrictionMsg`

`SuspensionMode`는 `deriveSuspensionModeCode(gDriveState)`로 계산된다. 즉, 현재 주행 상태 코드에 따라 기본 모드 또는 drive 모드를 선택한다.

### 10. 상태가 바뀐 경우에만 로그를 남긴다

마지막으로 `isEscLogUpdateRequired(gBrakePedal, isDecelAssistRequested)`가 참일 때만 로그를 출력한다.

비교 기준은 다음 두 값이다.

- 현재 브레이크 페달 값
- 현재 감속 보조 요청 플래그

즉, 매 주기마다 불필요하게 로그를 남기지 않고, 중요한 입력 상태가 바뀌었을 때만 로그를 남긴다.

## 정리

현재 ESC 로직의 핵심 흐름은 다음과 같다.

1. 차량 속도, 주행 상태, 조향 입력, 브레이크 입력 수신
2. 감속 보조 요청을 반영해 적용 브레이크 입력 계산
3. 브레이크 압력, ABS, ESP 상태 계산
4. wheel speed / yaw / brake status / health / ESC state 메시지 송신
5. brake temp / wear / suspension / friction 메시지 송신
6. 변화가 있을 때만 로그 출력
7. 다음 주기 예약

즉, 이 ESC 구현은 실제 제어기 모델이라기보다 SIL 환경에서 ESC 관련 chassis 상태를 만들어 다른 ECU와 패널이 사용할 수 있도록 주기적으로 publish하는 상태 생성 ECU라고 볼 수 있다.

# CGW 코드 설명

## 메시지 요약

### CAN Rx 메시지

| Message |
| --- |
| `frmChassisHealthMsg` |
| `frmBodyHealthMsg` |
| `frmInfotainmentHealthMsg` |

### CAN Tx 메시지

| Message |
| --- |
| 없음 |

### Ethernet Rx 메시지

| Message |
| --- |
| `ethMsgVehicleState` |
| `ethMsgNavContext` |
| `ethMsgSteering` |

### Ethernet Tx 메시지

| Message |
| --- |
| `ethMsgFailSafe` |
| `ethMsgObjectSafety` |

## 개요

이 문서는 [CGW.can](C:\Users\Kimtaekcheon\Documents\canoe-driving-alert\canoe\cfg\channel_assign\ETH_Backbone\CGW.can)의 `175~309`행에서 시작하는 `tBoundaryCheck` 타이머 블록이 어떤 작업을 하는지 설명한다.

현재 코드는 단순한 `if/else` 나열보다는 의미가 드러나는 helper 함수와 이름 규칙을 사용하도록 정리되어 있다. 특히 다음 규칙이 반영되어 있다.

- boolean처럼 동작하는 값: `is...`
- 상태 코드나 enum 성격의 값: `...Code`

예를 들어 `isBoundaryAlive`는 참/거짓 성격의 값이고, `warningPathStatusCode`, `e2eHealthStateCode`, `failSafeModeCode`, `routingPolicyCode`는 정해진 범위의 상태 코드를 의미한다.

## 작업 단위별 설명

### 1. 최신 입력들의 age를 계산한다

블록 시작부에서는 현재 시각 `nowMs`를 구한 뒤, 각 도메인과 입력의 마지막 수신 시각으로부터 age를 계산한다.

여기서 계산되는 값은 다음과 같다.

- `chassisAgeMs`
- `bodyAgeMs`
- `infoAgeMs`
- `gVehicleStateAgeMs`
- `gNavContextAgeMs`
- `gSteeringAgeMs`
- `gEmergencyMonAgeMs`

즉, 이후 상태 판단에 필요한 입력들이 얼마나 최근에 갱신되었는지를 먼저 수치로 정리하는 단계다.

### 2. Backbone boundary가 살아 있는지 판정한다

그 다음에는 `isBoundaryAlive`를 계산한다.

먼저 기본값을 `0`으로 두고, `isBoundaryAliveCondition(...)`이 참일 때만 `1`로 바꾼다.

이 함수는 다음 조건을 확인한다.

- `chassisAgeMs <= 300`
- `bodyAgeMs <= 300`
- `infoAgeMs <= 300`

즉, Chassis, Body, Infotainment 도메인의 heartbeat가 모두 일정 시간 안에 들어왔을 때만 backbone boundary를 정상으로 간주한다.

### 3. Warning path 상태 코드를 결정한다

이후에는 `warningPathStatusCode`를 계산한다.

먼저 `@Test::forceFailSafe`를 읽어 `isForceFailSafeRequested`로 정규화한 다음, `deriveWarningPathStatus(...)`를 호출한다.

이 함수의 판단 순서는 다음과 같다.

1. `isForceFailSafeRequested == 1` 이면 바로 broken 상태 코드 반환
2. `isWarningPathNormal(...)`이 참이면 normal 상태 코드 반환
3. `isWarningPathDegraded(...)`가 참이면 degraded 상태 코드 반환
4. 그 외에는 broken 상태 코드 반환

즉, 강제 fail-safe 요청 여부와 입력 신선도를 함께 반영해서 warning path의 상태를 하나의 코드로 정리한다.

### 4. Warning path 상태 코드를 E2E health와 fail-safe 모드 코드로 변환한다

`warningPathStatusCode`가 정해지면, 그 값을 바탕으로 다음 두 값을 계산한다.

- `e2eHealthStateCode = deriveE2eHealthState(warningPathStatusCode)`
- `failSafeModeCode = deriveFailSafeMode(warningPathStatusCode)`

즉, warning path 상태를 시스템이 바로 소비할 수 있는 health 코드와 fail-safe 모드 코드로 다시 매핑하는 단계다.

이 구조의 장점은 매핑 규칙이 본문에 흩어져 있지 않고, helper 함수 이름만으로 의미를 읽을 수 있다는 점이다.

### 5. Emergency context를 반영해 routing policy 코드를 결정한다

다음에는 `@Core::emergencyContext`를 읽어 `emergencyContextCode`로 정규화한 뒤, `deriveRoutingPolicy(...)`를 호출한다.

이 함수는 다음 기준으로 `routingPolicyCode`를 결정한다.

- fail-safe가 활성 상태이면 가장 보수적인 routing policy
- fail-safe가 아니고 emergency context가 있으면 emergency 기반 policy
- 그 외에는 normal policy

즉, 현재 시스템이 안전 모드인지, 비상 맥락이 존재하는지에 따라 이후 라우팅 정책을 선택한다.

### 6. 계산 결과를 Core와 CoreState에 반영한다

계산된 값들은 다음 시스템 변수에 기록된다.

- `@CoreState::domainBoundaryStatus = isBoundaryAlive`
- `@CoreState::warningPathStatus = warningPathStatusCode`
- `@CoreState::e2eHealthState = e2eHealthStateCode`
- `@CoreState::routingPolicy = routingPolicyCode`
- `@Core::failSafeMode = failSafeModeCode`

또한 `failSafeModeCode > 0`이면 `@Core::decelAssistReq`를 `0`으로 내려서 감속 보조 요청이 남아 있지 않도록 정리한다.

즉, 로컬 계산 결과를 시스템 공통 상태에 실제로 반영하는 단계다.

### 7. Fail-safe와 object safety 상태를 publish한다

그 다음에는 아래 두 함수를 호출한다.

- `publishFailSafeState(warningPathStatusCode, e2eHealthStateCode, failSafeModeCode, isBoundaryAlive)`
- `publishObjectSafetyState(failSafeModeCode)`

이 단계에서는 앞서 계산한 supervision 결과를 다른 ECU나 후속 로직이 사용할 수 있도록 전송한다.

특히 `publishObjectSafetyState(...)` 안에서도 `isObjectTrackValid`처럼 boolean 성격이 드러나는 이름을 사용해 object safety payload를 구성한다.

### 8. 상태가 달라졌을 때만 로그를 남긴다

마지막으로 `isBoundarySupervisionChanged(...)`를 호출해 이전 주기와 비교한다.

비교 대상은 다음과 같다.

- `isBoundaryAlive`
- `warningPathStatusCode`
- `e2eHealthStateCode`
- `failSafeModeCode`
- `routingPolicyCode`

이 중 하나라도 바뀌었을 때만 로그를 출력하고, 캐시 값도 다음과 같이 갱신한다.

- `gLastIsBoundaryAlive`
- `gLastWarningPathStatusCode`
- `gLastE2eHealthStateCode`
- `gLastFailSafeModeCode`
- `gLastRoutingPolicyCode`

즉, 변화가 있을 때만 상태와 age를 기록하는 edge-triggered logging 구조다.

### 9. 다음 주기를 예약한다

블록 마지막에서는 `setTimer(tBoundaryCheck, 100);`을 호출해 다음 boundary check를 `100ms` 뒤에 다시 실행하도록 예약한다.

즉, 이 supervision 로직은 100ms 주기로 반복된다.

## 정리

`tBoundaryCheck` 블록의 전체 흐름은 다음과 같다.

1. 입력 age 계산
2. `isBoundaryAlive` 판정
3. `warningPathStatusCode` 계산
4. `e2eHealthStateCode`, `failSafeModeCode` 계산
5. `routingPolicyCode` 계산
6. Core / CoreState 반영
7. fail-safe / object safety publish
8. 변화가 있을 때만 로그 출력
9. 다음 주기 예약

즉, 이 블록은 CGW가 경고 체인의 건강도를 주기적으로 감시하고, 그 결과를 명확한 상태 코드와 boolean 플래그 형태로 시스템 전반에 반영하는 감독용 타이머 블록이다.

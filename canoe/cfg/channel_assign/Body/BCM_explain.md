# BCM 코드 설명

## 개요

`BCM.can`은 Body 도메인 쪽의 기본 출력 상태를 주기적으로 구성하고 송신하는 코드다.

현재 리팩터링된 구조에서는 다음 세 층으로 역할이 나뉜다.

- 의미 있는 상수를 `variables` 블록의 `const int`로 정의
- 입력 정규화와 상태 결정을 helper 함수로 분리
- 실제 주기 송신은 `tBodyCycle`, `tBodyBase100` 두 타이머에서 수행

즉, 본문 타이머 함수는 “무엇을 송신하는가”에 집중하고, 세부 판단 규칙은 helper 함수가 담당하는 구조다.

## 주요 구성

### 1. 전역 상태와 상수 정의

`variables` 블록에는 다음 종류의 값이 있다.

- 타이머
- Ethernet 수신 관련 상태
- 마지막 앰비언트 출력 캐시
- backbone alert 입력 캐시
- 앰비언트 계산용 work 변수
- 매직넘버를 대체하는 `const int` 상수

특히 이번 구조에서는 앰비언트 색상, 패턴, seat belt 상태, lamp 상태, 기본 출력값이 모두 이름 있는 상수로 바뀌어 있다.

이 덕분에 코드에서 숫자 자체보다 “의미”를 먼저 읽을 수 있다.

### 2. Backbone alert 사용 여부 판단

`isUsingBackboneAlertState()`는 backbone에서 받은 alert 상태를 현재 사용할 수 있는지 판단한다.

이 함수는 다음을 확인한다.

- backbone alert timestamp가 존재하는지
- 마지막 backbone alert가 timeout 이내인지

즉, 최근에 Ethernet backbone에서 받은 경고 입력이 유효할 때만 그 상태를 우선 사용하게 된다.

### 3. 입력 정규화 함수들

다음 함수들은 입력값을 허용 범위 안으로 정리한다.

- `normalizeAmbientAlertLevel()`
- `normalizeAmbientAlertType()`
- `normalizeTimeoutClear()`
- `normalizeNavDirection()`
- `normalizeSeatBeltOverride()`

이 함수들의 목적은 본문 타이머 로직에서 직접 범위 비교를 반복하지 않도록 만드는 것이다.

즉, 타이머 함수는 “이 값을 어떻게 쓸지”만 보고, “이 값이 유효한지”는 helper가 먼저 처리한다.

### 4. 상태 결정 helper 함수들

현재 코드에서는 다음 판단 로직이 helper 함수로 분리돼 있다.

- `deriveHazardActiveState()`
- `deriveTurnLampState()`
- `deriveDriverSeatBeltState()`
- `derivePassengerSeatBeltState()`
- `deriveSeatBeltWarnLevel()`

이 함수들은 각각 다음 역할을 맡는다.

- hazard를 켜야 하는지
- 방향지시등을 어떤 상태로 둘지
- 운전석/동승석 안전벨트 상태를 어떻게 볼지
- 최종 seat belt warning level을 무엇으로 할지

즉, 이전처럼 긴 `if/else` 체인이 본문에 직접 보이지 않고, 의미 있는 이름으로 읽히도록 정리된 상태다.

### 5. 앰비언트 출력 계산 helper 함수들

앰비언트 출력 계산은 다음 두 함수로 분리돼 있다.

- `setAmbientOutputValues()`
- `resolveAmbientOutputValues()`

`setAmbientOutputValues()`는 계산된 세 값을 work 변수에 넣는 역할을 한다.

- `gAmbientModeWork`
- `gAmbientColorWork`
- `gAmbientPatternWork`

`resolveAmbientOutputValues()`는 실제 규칙을 담는다.

이 함수는 입력된 `alertLevel`, `alertType`, `timeoutClear`를 바탕으로:

- timeout clear면 앰비언트 출력 해제
- 고위험 긴급 경고면 긴급 색상/패턴 적용
- 스쿨존/고속도로/좌우 유도 경고면 각 타입별 고정 색상/패턴 적용
- 그 외 경고면 fallback 색상/패턴 적용

즉, 앰비언트 연출 규칙 전체를 한 함수 안에 모으고, 타이머 본문에서는 그 결과만 소비하도록 한 구조다.

## 타이머별 동작

### 6. `tBodyCycle`: 앰비언트 상태 갱신

`tBodyCycle`의 역할은 앰비언트 관련 상태를 계산해서 필요할 때만 송신하는 것이다.

이 타이머는 다음 순서로 동작한다.

1. backbone alert를 쓸지, Core arbitration 결과를 쓸지 결정
2. alert level / alert type / timeout clear 입력 정규화
3. `resolveAmbientOutputValues()` 호출로 앰비언트 mode/color/pattern 계산
4. `hasAmbientOutputChanged()`로 이전 출력과 비교
5. 값이 바뀐 경우에만:
   - `@Body::ambientMode`
   - `@Body::ambientColor`
   - `@Body::ambientPattern`
   - `frmAmbientControlMsg`
   를 갱신

즉, 이 타이머는 이벤트성 변화에 가까운 앰비언트 출력을 관리한다.

### 7. `tBodyBase100`: Body 기본 메시지 주기 송신

`tBodyBase100`은 Body 쪽 기본 상태를 100ms 주기로 송신하는 블록이다.

먼저 필요한 입력을 읽는다.

- hazard active 상태
- navigation direction
- seat belt override
- 현재 ambient mode

그 뒤 여러 메시지를 순서대로 채운다.

#### 7-1. Hazard / Window / Interior Light / Rain

다음 메시지들이 기본값 또는 현재 상태 기반으로 송신된다.

- `frmHazardControlMsg`
- `frmWindowControlMsg`
- `frmInteriorLightMsg`
- `frmRainLightAutoMsg`

여기서는 hazard 여부에 따라 비상등 상태가 정해지고, 실내등은 ambient mode와 연동된다.

#### 7-2. Door / Lamp

도어 상태는 기본 잠금/닫힘 쪽 값으로 송신된다.

램프 상태는 다음 값으로 구성된다.

- 전조등 상태
- 후미등 상태
- 방향지시등 상태
- 비상등 요청

특히 방향지시등은 `deriveTurnLampState()`가 계산하며, hazard가 우선이고 그다음 navigation direction을 반영한다.

#### 7-3. Seat Belt

안전벨트 메시지는 helper 함수 조합으로 구성된다.

- 운전석 belt 상태: `deriveDriverSeatBeltState()`
- 동승석 belt 상태: `derivePassengerSeatBeltState()`
- 최종 경고 레벨: `deriveSeatBeltWarnLevel()`

즉, override 입력과 hazard 상태를 조합해 최종 seat belt 경고를 만든다.

#### 7-4. CoreState 미러링

다음 값들은 다른 ECU가 참조할 수 있도록 `@CoreState`에 다시 반영된다.

- `turnLampState`
- `driverSeatBelt`
- `passengerSeatBelt`
- `seatBeltWarnLvl`

즉, 송신 메시지와 별개로 내부 공통 상태도 함께 유지한다.

#### 7-5. Cabin / Health / Seat / Door Control / Gateway / Comfort

그 뒤에는 기본 Body 관련 상태들이 계속 송신된다.

- 실내 환경 상태
- Body health 상태
- 시트 위치 상태
- 시트 제어 기본값
- 도어 제어 기본값
- Body gateway 상태
- Comfort 상태

마지막에는 `gBodyAliveCnt`를 증가시켜 health 메시지에 반영한다.

## 정리

리팩터링 이후 `BCM.can`은 다음 특징을 가진다.

1. 숫자 의미를 `const int` 이름으로 드러낸다.
2. 입력 정규화와 상태 판단을 helper 함수로 분리했다.
3. 앰비언트 출력 계산을 별도 함수에 모았다.
4. 주기 송신 본문은 “무엇을 송신하는가” 중심으로 읽히게 정리됐다.

즉, 현재 구조는 이전보다:

- 조건식의 의미를 읽기 쉽고
- 매직넘버를 해석하기 쉽고
- 각 블록의 책임을 구분하기 쉬운 형태라고 볼 수 있다.

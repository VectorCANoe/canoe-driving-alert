# SCC `publishCruiseState()` 설명

## 개요

`publishCruiseState()`는 현재 차량 상태와 위험 관련 Core 값을 읽어서 SCC 출력값을 계산한 뒤, 그 결과를 `frmCruiseStateMsg`로 송신하는 함수다.

주요 출력값은 다음 세 가지다.

- `CruiseState`
- `GapLevel`
- `CruiseSetSpeed`

## 단계별 설명

### 1. 제한속도 입력이 없으면 기본 제한속도를 사용한다.

함수는 먼저 `@Core::speedLimitNorm` 값을 읽는다.

이 값이 `0`이면 제한속도 입력이 아직 설정되지 않았다고 보고, `SCC_DEFAULT_SPEED_LIMIT_KPH`를 기본 제한속도로 대체한다.

이 단계의 목적은 이후 계산이 `0 km/h` 같은 비정상적인 기준값을 사용하지 않도록 막는 것이다.

### 2. SCC 기본 상태, gap 레벨, 설정 속도를 초기화한다.

다음으로 함수는 SCC 출력의 기본값을 잡는다.

- `cruiseState = SCC_STATE_OFF`
- `gapLevel = SCC_DEFAULT_GAP_LEVEL`
- `cruiseSetSpeed = speedLimit`

즉, 주행 조건이나 위험 조건을 아직 반영하기 전에 기본 동작을 먼저 정의하는 단계다.

### 3. 차량이 주행 중이고 fail-safe가 비활성일 때만 SCC를 활성화한다.

그다음 함수는 다음 두 조건을 확인한다.

- 차량이 `Drive` 상태인지
- fail-safe 모드가 비활성인지

이 두 조건이 모두 만족될 때만 SCC 상태를 `OFF`에서 `READY`로 바꾼다.

차량이 주행 중이 아니거나 시스템이 fail-safe 상태이면 SCC는 실질적으로 비활성 상태로 유지된다.

### 4. 고위험 상황에서는 gap을 더 벌리고 설정 속도를 더 크게 낮춘다.

함수는 이어서 현재 상황이 고위험인지 판단한다.

고위험은 다음 중 하나라도 만족하면 성립한다.

- `proximityRiskLevel`이 높음
- `selectedAlertLevel`이 높음
- `emergencyContext`에 긴급 상황이 존재함

이 경우 함수는 다음과 같이 동작한다.

- `cruiseState`를 `SCC_STATE_DECEL_CONTROL`로 변경
- gap 레벨을 더 크게 설정
- 현재 차량 속도에서 더 큰 폭으로 감속한 값을 설정 속도로 사용

즉, 이 블록은 가장 강한 SCC 대응을 담당한다.

### 5. 중위험 상황에서는 gap과 설정 속도만 완만하게 조정한다.

고위험은 아니지만 중위험 임계값 이상이면, 함수는 보다 완만한 보정을 적용한다.

이 경우에는 다음과 같이 동작한다.

- 고위험 분기보다 덜 공격적인 상태 유지
- gap 레벨 확대
- 설정 속도는 작은 폭으로만 감소

즉, 강한 감속 제어보다는 예방적 완화에 가까운 동작이다.

### 6. 설정 속도를 최소값과 제한속도 범위 안으로 보정한다.

설정 속도가 계산된 뒤에는 최종 보정 단계가 수행된다.

이 단계에서는 다음 조건을 보장한다.

- SCC가 활성 상태라면 설정 속도가 `SCC_MIN_CRUISE_SET_SPEED_KPH` 아래로 내려가지 않음
- 설정 속도가 현재 제한속도를 초과하지 않음
- 최종 값이 메시지에 담을 수 있는 `0..255` 범위 안에 들어감

즉, 앞에서 계산된 결과를 실제 송신 가능한 안전한 출력값으로 정리하는 단계다.

### 7. 계산된 SCC 상태를 출력 메시지로 송신한다.

마지막으로 함수는 계산된 값을 `frmCruiseStateMsg`에 채운다.

- `CruiseState`
- `GapLevel`
- `CruiseSetSpeed`

그다음 `output(mCruise)`를 호출해 메시지를 송신한다.

이 단계가 함수의 최종 결과다.

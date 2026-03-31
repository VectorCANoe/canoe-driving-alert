# Runtime Layer Separation Policy

원문:
- [../../contracts/layer-separation-policy.md](../../contracts/layer-separation-policy.md)

동기화 기준:
- `canonical english source`
- seam 이름, ECU 이름, message name, SysVar name은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 현재 개발 baseline과 계획 중인 target architecture를 반영합니다.
> 일부 runtime, diagnostic, verification 세부사항은 아직 구현 중이며 변경될 수 있습니다.

## 목적

이 문서는 active CANoe SIL baseline에서 `transport / decision / boundary / render / observer / diagnostic` 계층을 어떻게 분리할지 정의합니다.

이 문서가 답하는 질문은 다음과 같습니다.

- 어떤 node가 해당 seam의 business meaning owner인가
- 어떤 node가 그 seam을 transport 또는 route만 할 수 있는가
- 어떤 node가 observer 또는 validation 역할만 해야 하는가
- 어떤 seam이 operational, render-facing, diagnostic, validation-only인지

## 외부 기준

이 분리 원칙은 다음 공개 기준을 바탕으로 정리했습니다.

- Vector `CAPL Callback Interface in CANoe`
  - tester side와 ECU simulation side를 구분하고, target/channel을 명시적으로 다룹니다.
- Vector `Ethernet_E: DoIP`
  - diagnostic tester, diagnostic gateway, DoIP node를 구분합니다.
- AUTOSAR `Diagnostic Communication Manager`
  - external diagnostic tool과 onboard DCM을 구분하고, diagnostic state를 network-independent하게 관리합니다.
- AUTOSAR `PDU Router`
  - router는 I-PDU를 forward/routing하지만 payload 의미를 다시 정의하지 않습니다.
- ISO 13400-2
  - client tester, vehicle gateway, sub-component routing 구조를 정의합니다.

## 계층 모델

active baseline은 아래 여섯 계층으로 나눕니다.

- `Transport ingress`
  - meaning: raw network context 수신 및 freshness 정규화
  - typical owner: ingress owner
- `Functional decision`
  - meaning: warning, risk, assist 의미 결정
  - typical owner: decision owner
- `Boundary / override`
  - meaning: fail-safe, route, freshness 정책 적용
  - typical owner: gateway / boundary owner
- `Render / output`
  - meaning: body, display, cluster, audio로 결과 반영
  - typical owner: render owner
- `Observer / validation`
  - meaning: 이미 publish된 seam을 evidence/verdict 용도로 관측
  - typical owner: validation harness
- `Diagnostic semantic`
  - meaning: diagnostic state, session, security, response 의미 제공
  - typical owner: diagnostic owner

## 분리 규칙

### 1. logical seam마다 business owner는 하나

- 하나의 logical seam은 하나의 business owner만 가집니다.
- compatibility mirror, trace seam, validation observer는 ownership을 바꾸지 않습니다.
- validation injector가 존재해도 product owner가 바뀌면 안 됩니다.

### 2. transport와 decision ownership은 다릅니다

- transport를 수신한다고 decision owner가 되는 것은 아닙니다.
- gateway/router는 seam을 forward할 수 있지만 seam의 business meaning을 다시 정의하면 안 됩니다.

### 3. boundary policy는 중앙 authority가 가져야 합니다

- stale, timeout-clear, degraded, fail-safe는 하나의 boundary authority가 정의해야 합니다.
- downstream node는 그 상태를 소비해야 하며, 두 번째 freshness policy를 임의로 만들면 안 됩니다.

### 4. observer는 operational ownership에 개입하지 않습니다

- observer node는 published seam을 구독할 수 있습니다.
- 하지만 alternate product owner가 되면 안 됩니다.
- validation aggregation은 operational owner가 먼저 publish한 뒤에만 허용합니다.
- active validation lifecycle 밖에서는 observer seam이 reset-safe idle 상태를 유지해야 합니다.
- idle transport traffic이 validation observer reset 값을 덮어쓰면 안 됩니다.
- observer freshness나 receive timestamp는 실제 관측 transport 또는 owner-published seam 기준이어야 하며, 하네스가 synthetic하게 추정해서는 안 됩니다.

### 5. diagnostic semantic과 request/response route는 분리합니다

- compact semantic seam은 둘 수 있습니다.
- 하지만 그 semantic seam을 actual network request/response route의 대체물로 취급하면 안 됩니다.

### 6. validation-only stimulus는 명시적으로 유지합니다

- `TEST_SCN`은 SIL에서 validation-only transport stimulus를 넣을 수 있습니다.
- 이 예외는 product owner를 테스트하기 위한 것이며, ownership 재할당을 의미하지 않습니다.
- `TEST_SCN`은 시험 verdict 상태를 계산할 수 있지만, 그 verdict는 owner가 publish한 seam과 시험 출력 기준으로만 도출해야 합니다.
- product owner가 값을 publish하지 못할 때 `TEST_SCN`이 fallback semantic owner가 되어서는 안 됩니다.
- `TEST_BAS`는 observer 결과를 집계할 수 있지만, 관측 seam의 alternate product meaning을 합성해서는 안 됩니다.
- 하네스는 scenario timing을 오케스트레이션할 수 있지만, product owner가 이미 clear한 semantic state를 하네스가 계속 살려 두어서는 안 됩니다.

## 현재 프로젝트 적용

### Emergency / V2X path

- `ETH_EmergencyAlert`
  - product owner: `V2X`
  - transport role: raw emergency ingress contract
  - observer role: trace only
  - validation-only exception: `TEST_SCN`이 validation ingress stimulus로 emit할 수 있으나 product owner는 여전히 `V2X`
- `Core::emergencyContext`
  - product owner: `V2X`
  - transport role: normalized internal semantic
  - observer role: `TEST_BAS`, evidence tool
  - validation-only exception: 없음
- `CoreState::emergencyIngressDirection / emergencyIngressEtaSec / emergencyIngressSourceId`
  - product owner: `V2X`
  - transport role: normalized ingress metadata seam
  - observer role: `TEST_BAS`, evidence tool
  - validation-only exception: 없음
- `V2X::ingressHeartbeat`
  - product owner: `V2X`
  - transport role: ingress freshness heartbeat
  - observer role: `TEST_BAS`, evidence tool
  - validation-only exception: 없음
- `ETH_EmergencyMonitor`
  - product owner: `V2X`
  - transport role: transport-monitor publication
  - observer role: `TEST_BAS`, trace observer
  - validation-only exception: 없음
- `CoreState::selectedAlertDecisionLevel / selectedAlertDecisionType`
  - product owner: `ADAS`
  - transport role: functional selected-alert decision seam
  - observer role: `TEST_BAS`, evidence tool
  - validation-only exception: 없음
- `CoreState::selectedAlertEffectiveLevel / selectedAlertEffectiveType / selectedAlertGateReason`
  - product owner: `CGW`
  - transport role: selected-alert effective seam
  - observer role: `TEST_BAS`, evidence tool
  - validation-only exception: 없음
- `ethSelectedAlertMsg`
  - product owner: `ADAS`
  - transport role: active selected-alert state relay
  - observer role: `TEST_BAS`, evidence tool
  - validation-only exception: 없음
- `@Core::decelAssistDecisionReq`
  - product owner: `ADAS`
  - transport role: internal decision seam
  - observer role: `TEST_BAS`, debug trace
  - validation-only exception: 없음
- `CoreState::driverReleaseReason`
  - product owner: `ADAS`
  - transport role: 운전자 개입 해제 seam
  - observer role: `TEST_BAS`, debug trace
  - validation-only exception: 없음
- `@Core::decelAssistReq / CoreState::decelGateReason`
  - product owner: `CGW`
  - transport role: effective assist seam
  - observer role: `TEST_BAS`, debug trace
  - validation-only exception: 없음
- `ethFailSafeStateMsg / warningPathStatus`
  - product owner: `CGW`
  - transport role: boundary-health publication
  - observer role: `TEST_BAS`, trace observer
  - validation-only exception: `TEST_SCN::ValidationOverride`는 test-only

### Render / output path

- visual warning level/type
  - product owner: `IVI`, `HUD`, `CLU`
  - required input: `CoreState::selectedAlertEffective*` + documented compatibility fallback
- ambient / body warning actuation
  - product owner: `BCM`
  - required input: CGW effective selected-alert state + CGW boundary health
- audio focus / ducking / volume guidance
  - product owner: `AMP`, `IVI`, `VCS`
  - required input: CGW effective selected-alert state + user policy input

규칙:

- render node는 owner-published result seam을 소비합니다.
- render consumer는 `effective -> decision -> compatibility fallback` 순서로 읽는 것을 기본으로 합니다.
- render node가 emergency ingress owner가 되면 안 됩니다.
- render / decision node는 raw `V2X::*` transport mirror보다 `CoreState` normalized ingress metadata를 우선 소비해야 합니다.
- raw ingress 직접 참조는 documented compatibility path일 때만 허용합니다.
- `TEST_SCN`이 직접 emergency transport frame을 주입하는 동안에는 `Test::compat*` dispatch compatibility 입력을 비워 둡니다. dispatch compatibility stimulus는 dispatch-only 검증 경로에서만 사용하며 `V2X::*` owner mirror에 직접 쓰면 안 됩니다.

### Diagnostic path

- network request / response route
  - owner: requester + gateway + ECU server path
  - role: 실제 transport/addressing flow
- `Diag::*` semantic seam
  - owner: `SGW` + `DCM`
  - role: diagnostic status/result 의미를 compact하게 관측
- `EXT_DIAG`
  - owner: logical external requester / observer surface
  - role: 현재 baseline에서는 `Diag::*`만 읽고 새 backbone payload contract는 추가하지 않음

## 현재 backbone producer boundary 규칙

active baseline은 backbone seam에서 producer identity를 유지해야 합니다.

- `ETH_EmergencyAlert`: `TEST_SCN`
- `ethObjectRiskInputMsg`: `TEST_SCN`
- `ETH_EmergencyMonitor`: `V2X`
- `ethSelectedAlertMsg`: `ADAS`
- `ethDecelAssistReqMsg`: `ADAS`
- `ethObjectRiskStateMsg`: `ADAS`
- `ethObjectScenarioAlertMsg`: `ADAS`
- `ethFailSafeStateMsg`: `CGW`
- `ethObjectSafetyStateMsg`: `CGW`
- `ethValidationOverride`: `TEST_SCN`

의미:

- backbone consumer는 source ownership을 확인한 뒤에만 authoritative frame으로 취급해야 합니다.
- self-originated transport는 strict self-source check로 배제해야 합니다.
- 예상과 다른 external source는 SIL continuity를 위해 trace 후 수용할 수 있지만, 그것이 second logical owner가 되어서는 안 됩니다.
- message ID만 같다고 해서 같은 authority로 보면 안 됩니다.

## 읽는 순서

1. `contracts/layer-separation-policy.md`
2. `contracts/owner-route.md`
3. `contracts/ethernet-interface.md`
4. `contracts/communication-matrix.md`
5. `contracts/multibus-policy.md`

## 갱신 규칙

seam 역할이 바뀌면 다음 순서로 갱신합니다.

1. `contracts/layer-separation-policy.md`
2. `contracts/owner-route.md`
3. `contracts/ethernet-interface.md`
4. `contracts/communication-matrix.md`
5. `contracts/multibus-policy.md`
6. runtime CAPL / verification asset

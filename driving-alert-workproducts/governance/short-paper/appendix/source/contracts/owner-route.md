# Owner / Bus / Timeout / Route Contract

원문:
- [../../contracts/owner-route.md](../../contracts/owner-route.md)

동기화 기준:
- `5d83ee7f`
- seam 이름, owner, bus 이름은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 현재 개발 baseline과 계획 중인 target architecture를 반영합니다.
> runtime, diagnostic, verification 세부사항 가운데 일부는 아직 구현 중이며 변경될 수 있습니다.

## 목적

이 문서는 주요 runtime seam마다 누가 owner인지, 어떤 bus가 적용되는지, 그리고 timeout authority와 route authority가 누구인지 정의합니다.

## 계약 차원

- `Owner`: 해당 seam의 business meaning을 소유하는 runtime authority
- `Bus`: active baseline에서 사용하는 primary transport 또는 observation seam
- `Timeout authority`: stale-state, clear, fail-safe 동작을 결정하는 runtime authority
- `Route authority`: cross-domain delivery와 forwarding을 제어하는 runtime authority

## 규칙

- 하나의 logical seam은 하나의 explicit owner를 가져야 합니다
- cross-domain forwarding이 개입되면 owner와 route authority는 달라질 수 있습니다
- timeout 및 clear 동작은 transport만으로 추정하지 말고 명시적으로 정의해야 합니다
- 계층 분리와 observer 분리 원칙은 `contracts/layer-separation-policy.md`를 따릅니다
- foreign-domain CAN visibility는 `contracts/multibus-policy.md`를 따릅니다
- 상세 frame-level ownership은 `contracts/communication-matrix.md`에서 관리합니다

## 현재 seam 기준선

- Navigation context
  - owner: `IVI`
  - bus: `Infotainment CAN`
  - timeout authority: `IVI`
  - route authority: cross-domain delivery가 필요할 때 `CGW`
  - note: road zone, direction, distance, speed-limit context
- Emergency context
  - owner: `V2X`
  - bus: `Ethernet backbone + normalized Core/CoreState seam`
  - timeout authority: `CGW`
  - route authority: `CGW`
  - note: emergency source, direction, ETA, active/clear context
- Arbitration decision
  - owner: `ADAS`
  - bus: local runtime + `CoreState::selectedAlertDecision*`
  - timeout authority: `ADAS`
  - route authority: cross-domain forwarding 시 `CGW`
  - note: gateway shaping 이전 selected alert level/type
- Arbitration effective result
  - owner: `CGW`
  - bus: `CoreState::selectedAlertEffective*` + published output seam
  - timeout authority: `CGW`
  - route authority: `CGW`
  - note: boundary, timeout-clear, fail-safe shaping 이후 selected alert level/type
- Decel decision
  - owner: `ADAS`
  - bus: local runtime + `@Core::decelAssistDecisionReq` + `CoreState::driverReleaseReason`
  - timeout authority: `ADAS`
  - route authority: cross-domain forwarding 시 `CGW`
  - note: 운전자 개입 해제 의미를 먼저 정리하는 seam
- Decel effective result
  - owner: `CGW`
  - bus: `@Core::decelAssistReq` + `CoreState::decelGateReason`
  - timeout authority: `CGW`
  - route authority: `CGW`
  - note: fail-safe 적용 후 최종 감속 보조 요청과 gate reason
- Render warning state
  - owner: `IVI`, `CLU`, `HUD`, `AMP`
  - bus: local render output + `CoreState::selectedAlertEffective*` consumer seam
  - timeout authority: 각 render owner
  - route authority: 없음
  - note: render owner는 `effective -> decision -> compatibility fallback` 순서로 소비하며 ingress/gateway owner가 되지 않음
- Body ambient / hazard output
  - owner: `BCM`
  - bus: body output + `CoreState::selectedAlertEffective*` consumer seam
  - timeout authority: `BCM`
  - route authority: 없음
  - note: local body policy와 effective selected-alert state를 함께 소비
- Boundary health
  - owner: `CGW`
  - bus: `Ethernet backbone`
  - timeout authority: `CGW`
  - route authority: `CGW`
  - note: fail-safe and cross-domain health summary
- Scenario result
  - owner: `TEST_SCN`
  - bus: test harness seam
  - timeout authority: `TEST_SCN`
  - route authority: 없음
  - note: per-scenario verdict and trace anchor
- Baseline result
  - owner: `TEST_BAS`
  - bus: SysVar-only seam
  - timeout authority: `TEST_BAS`
  - route authority: 없음
  - note: aggregate baseline verdict and health summary

## 사용 규칙

seam-level authority 판단은 이 문서를 기준으로 합니다.
해당 seam이 transport, decision, boundary, render, observer, diagnostic semantic 가운데 무엇인지 먼저 판단할 때는 `contracts/layer-separation-policy.md`를 먼저 봅니다.
frame-level ownership을 확인할 때는 `contracts/communication-matrix.md`를 사용합니다.

## 개발 메모

위 seam 표는 active baseline의 현재 계획 계약입니다.
개발 중 seam의 transport 또는 ownership이 바뀌면, 그 변경을 공식으로 취급하기 전에 먼저 이 문서를 갱신해야 합니다.

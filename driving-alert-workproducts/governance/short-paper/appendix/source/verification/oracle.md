# Oracle

원문:
- [../../verification/oracle.md](../../verification/oracle.md)

동기화 기준:
- `5d83ee7f`
- oracle layer 이름, SysVar 이름, contract 문서 이름은 canonical technical identifier로 유지합니다.

> [!IMPORTANT]
> 이 문서는 CANoe SIL baseline이 올바른지 판정하는 layered oracle model을 정의합니다.
> PASS는 단일 signal이 아니라 contract, behavior, harness, evidence가 함께 맞아야 성립합니다.

## 목적

이 문서는 CANoe SIL baseline의 정합성을 판정할 때 사용하는 oracle model을 정의합니다.

oracle은 단일 signal check가 아닙니다.
아래 네 계층이 모두 일치해야 true PASS로 봅니다.

- contract
- behavior
- harness
- evidence

## Oracle 모델

- Contract oracle
  - source: communication matrix, owner/route contract, multibus policy, interface contract
  - pass expectation: runtime이 문서화된 owner, bus, route, timeout, observation seam을 따릅니다.
- ECU behavior oracle
  - source: ECU classification, panel/sysvar contract, diagnostic-sysvar contract
  - pass expectation: 각 active ECU 또는 surface가 문서화된 responsibility boundary 안에서 동작합니다.
- Scenario oracle
  - source: acceptance criteria
  - pass expectation: scenario result가 기대한 alert, clear, fail-safe, routing behavior와 일치합니다.
- Harness oracle
  - source: `TEST_SCN`, `TEST_BAS`, native Test Unit verdict
  - pass expectation: native harness verdict가 기대 scenario result와 일치합니다.
- Evidence oracle
  - source: evidence policy와 captured artifact
  - pass expectation: evidence package가 review와 traceability에 충분합니다.

## Oracle source

- `../architecture/ecu-classification.md`
- `../contracts/communication-matrix.md`
- `../contracts/owner-route.md`
- `../contracts/multibus-policy.md`
- `../contracts/panel-sysvar-contract.md`
- `../contracts/diagnostic-sysvar-contract.md`
- `acceptance-criteria.md`
- `execution-guide.md`
- `evidence-policy.md`

## 현재 판정 규칙

검증 항목이 true PASS가 되려면 아래가 모두 참이어야 합니다.

1. runtime이 문서화된 contract path를 따를 것
2. ECU 또는 surface behavior가 문서화된 ownership boundary 안에 있을 것
3. scenario result가 acceptance criteria와 일치할 것
4. harness verdict가 그 기대 결과와 일치할 것
5. 필요한 evidence가 존재하고 review 가능할 것

즉 harness verdict만 PASS라고 해서 전체 PASS가 되는 것은 아닙니다.

예:
- verdict는 PASS인데 contract path가 문서화되지 않음
- verdict는 PASS인데 required evidence가 없음
- 출력은 한 번 맞아 보이지만 repeatability 또는 timeout rule이 실패함

## Harness 기반 oracle 해석

현재 baseline이 쓰는 핵심 seam은 아래와 같습니다.

- `Test::scenarioResult`: `TEST_SCN`이 기록하는 scenario-level PASS/FAIL
- `Test::baseScenarioResult`: `TEST_BAS`가 기록하는 aggregate baseline verdict
- `Test::baseFlowCoverageMask`: review completeness를 위한 coverage summary
- `Test::baseTraceSnapshotId`: evidence navigation용 trace anchor
- `Test::baseTestHealth`: harness trustworthiness를 판단하는 health summary

## 현재 oracle 경계

active oracle은 아래 범위에 한정합니다.

- CANoe SIL
- CAN + Ethernet runtime seam
- 현재 문서화된 product surface와 validation surface

이 문서는 미래의 모든 ECU와 모든 customer test case가 완전히 커버되었다고 주장하지 않습니다.

## 개발 메모

향후 프로젝트 전체 test architecture가 customer workproduct chain 기준으로 다시 정리되더라도, 아래 구조는 유지해야 합니다.

- layered oracle structure
- product behavior와 validation behavior의 분리
- PASS는 contract, behavior, harness, evidence가 모두 동의해야 한다는 원칙

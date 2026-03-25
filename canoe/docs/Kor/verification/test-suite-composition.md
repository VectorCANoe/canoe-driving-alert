# Test Suite Composition

원문:
- [../../verification/test-suite-composition.md](../../verification/test-suite-composition.md)

동기화 기준:
- `5d83ee7f`
- suite ID, test asset ID, physical path는 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 현재 CANoe SIL executable baseline의 active suite composition을 정의합니다.
> CAPL asset이 추가, 이름 변경, retire 이동을 하면 같은 baseline에서 suite도 함께 갱신해야 합니다.

## 목적

이 문서는 현재 native CANoe test baseline을 실행할 때 사용하는 active level suite를 정의합니다.

suite boundary는 과거 umbrella reviewer row가 아니라, 실제 executable asset 기준으로 구성합니다.

## Active level suite

- `TS_CANOE_UT_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_UT_ACTIVE_BASELINE/TS_CANOE_UT_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: active 상태이며 retire되지 않은 모든 `TC_CANOE_UT_*` asset
- `TS_CANOE_IT_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_IT_ACTIVE_BASELINE/TS_CANOE_IT_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: active 상태이며 retire되지 않은 모든 `TC_CANOE_IT_*` asset
- `TS_CANOE_ST_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_ST_ACTIVE_BASELINE/TS_CANOE_ST_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: active 상태이며 retire되지 않은 모든 `TC_CANOE_ST_*` asset

## Active campaign suite

- `TS_CANOE_FULL_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_FULL_ACTIVE_BASELINE/TS_CANOE_FULL_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: 현재 `UT`, `IT`, `ST` active suite를 ordered wrapper로 묶은 campaign entry point

## Inclusion rule

- `canoe/tests/modules/test_units/` 아래 실제 존재하는 asset만 포함합니다
- `canoe/tests/modules/test_units/retire/` 아래 자산은 모두 제외합니다
- umbrella reviewer ID를 suite member로 직접 넣지 않습니다
- exact executable asset을 suite member로 사용합니다

## Composition rule

- `UT` suite는 unit-level executable asset을 묶습니다
- `IT` suite는 integration-level executable asset을 묶습니다
- `ST` suite는 system-level executable asset을 묶습니다
- `FULL` suite는 세 active level suite를 하나의 campaign entry point로 묶습니다
- suite membership은 asset-based이며, 하나의 executable asset이 의도적으로 여러 reviewer row를 닫는 경우 여러 exact row를 함께 커버할 수 있습니다

## Update rule

- reviewer row가 exact row로 split되더라도 executable asset set이 바뀌지 않으면 suite membership은 그대로 둘 수 있습니다
- asset이 retire되면 같은 change set에서 해당 suite에서도 제거해야 합니다
- 새 executable asset이 active가 되면 reviewer-facing status를 `Ready`로 바꾸기 전에 먼저 해당 suite에 추가해야 합니다

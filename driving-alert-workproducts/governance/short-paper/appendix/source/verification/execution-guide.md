# 실행 가이드

원문:
- [../../verification/execution-guide.md](../../verification/execution-guide.md)

동기화 기준:
- `5d83ee7f`
- technical identifier, test asset ID, SysVar 이름은 원문과 동일하게 유지합니다.

> [!IMPORTANT]
> 이 문서는 현재 개발 baseline과 계획 중인 target architecture를 반영합니다.
> runtime, diagnostic, verification 세부사항 가운데 일부는 아직 구현 중이며 변경될 수 있습니다.

## 목적

이 문서는 현재 native CANoe SIL 검증 자산의 실행 흐름을 정의합니다.

다음 항목에 대한 공식 실행 기준 문서입니다.

- Test Unit 등록과 실행
- `TEST_SCN`, `TEST_BAS`를 통한 harness 상호작용
- native execution 이후 evidence 수집

## 검증 모델

현재 baseline은 `harness-first execution model`을 사용합니다.

- `TEST_SCN`: scenario stimulus를 주입하고 scenario 단위 verdict 상태를 설정합니다.
- `TEST_BAS`: `Test::base*` summary variable을 통해 baseline 결과를 집계합니다.
- native CANoe Test Unit asset: 선택한 verification package를 CANoe 내부에서 실행합니다.

## 현재 active native asset

현재 active native execution baseline으로 유지하는 자산은 아래 두 개입니다.

1. `canoe/tests/modules/test_units/TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION`
2. `canoe/tests/modules/test_units/TC_CANOE_IT_V2_011_FAILSAFE_MIN_WARNING`

이 자산은 `현재 baseline`을 뜻할 뿐이며, 미래 전체 test architecture가 완성되었다는 의미는 아닙니다.

## Harness contract

현재 실행 흐름은 아래 harness variable에 의존합니다.

- `Test::scenarioCommand`: one-shot execution trigger
- `Test::scenarioCommandAck`: accepted command identifier
- `Test::scenarioResult`: `TEST_SCN`이 기록하는 scenario 단위 verdict
- `Test::baseScenarioId`: baseline aggregation에 사용하는 scenario identifier
- `Test::baseScenarioResult`: `TEST_BAS`가 기록하는 baseline PASS/FAIL 결과
- `Test::baseFlowCoverageMask`: baseline coverage summary
- `Test::baseTraceSnapshotId`: baseline trace anchor
- `Test::baseTestHealth`: baseline harness health summary

## 표준 실행 절차

1. CANoe GUI에서 active configuration을 엽니다.
2. 필요한 runtime node, database, panel asset, SysVar surface가 모두 준비되었는지 확인합니다.
3. CANoe Test Unit 환경에 대응하는 `*.vtestunit.yaml` 자산을 등록합니다.
4. GUI bulk import가 필요하면 `canoe/tests/modules/test_units/assign/` 아래 wrapper folder를 사용합니다.
5. measurement를 시작합니다.
6. 선택한 native Test Unit을 실행합니다.
7. scenario 단위 verdict와 baseline summary verdict를 모두 확인합니다.
8. evidence policy가 요구하는 report, screenshot, supporting evidence를 저장합니다.

## 현재 매핑

- `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION`
  - scope: school-zone warning-selection path
  - runtime check: `selectedAlert*`, `warningPathStatus`, `failSafeMode`, `warningTextCode`
- `TC_CANOE_IT_V2_011_FAILSAFE_MIN_WARNING`
  - scope: boundary fail-safe path
  - runtime check: `failSafeMode`, `decelAssistReq`, `selectedAlert*`, `warningTextCode`, `Test::baseScenarioId`, `Test::baseScenarioResult`

## 기대 산출물

공식 native execution은 필요에 따라 아래 산출물을 남겨야 합니다.

- compile-clean 결과
- native test verdict
- native report path
- screenshot 또는 GUI capture
- evidence policy가 요구하는 write-window 또는 trace support

## 경계

이 문서는 아래 항목을 정의하지 않습니다.

- 최종 customer-facing test architecture
- CANoe native execution surface 밖의 packaging ownership
- `05/06/07` 전체 세트의 광범위한 재설계

이 영역은 이후 customer workproduct baseline을 기준으로 다시 설계될 수 있습니다.

## 개발 메모

현재 가이드는 active CANoe surface에 대해 유효한 execution baseline입니다. 다만 프로젝트 전체 test architecture는 이후 customer 문서 체인을 기준으로 다시 재구성될 수 있습니다.

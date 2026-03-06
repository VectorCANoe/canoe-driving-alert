# 문서-코드 정합 게이트 리포트

- Generated at: `{{generated_at}}`
- Commit: `{{commit_sha}}`
- Branch: `{{branch}}`
- Gate Result: `{{gate_result}}`

## 1) Req 커버리지 (01 기준)

{{req_coverage_table}}

## 2) Func 커버리지 (03 기준)

{{func_coverage_table}}

## 3) 구현 정합 (CAPL / CFG / DBC)

{{impl_summary}}

## 4) 경고/조치 항목

{{issues}}

## 5) 비고

- `06_Integration_Test.md`는 Lean IT 운영 방침에 따라 `핵심 통합 체인` 위주 커버리지로 관리할 수 있다.
- Validation Harness(`SIL_TEST_CTRL`, `VEHICLE_BASE_TEST_CTRL`)는 검증 전용(Non-Production) 계층으로 관리한다.

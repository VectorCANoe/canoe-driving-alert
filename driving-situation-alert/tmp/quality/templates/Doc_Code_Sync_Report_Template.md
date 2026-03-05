> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

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
- Validation Harness(`VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL`)는 검증 전용(Non-Production) 계층으로 관리한다.

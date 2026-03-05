> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

# 문서-코드 정합 게이트 리포트

- Generated at: `2026-03-03 17:55:16 UTC`
- Commit: `cce7711`
- Branch: `integration/v2-all-in`
- Gate Result: `PASS`

## 1) Req 커버리지 (01 기준)

| Doc | Covered | Total | Status |
| --- | --- | --- | --- |
| 03 | 67 | 67 | PASS |
| 0301 | 67 | 67 | PASS |
| 0302 | 67 | 67 | PASS |
| 0303 | 67 | 67 | PASS |
| 0304 | 67 | 67 | PASS |
| 05 | 67 | 67 | PASS |
| 07 | 67 | 67 | PASS |
| 06 | 67 | 67 | PASS |

## 2) Func 커버리지 (03 기준)

| Doc | Covered | Total | Status |
| --- | --- | --- | --- |
| 0301 | 67 | 67 | PASS |
| 0302 | 67 | 67 | PASS |
| 0303 | 67 | 67 | PASS |
| 0304 | 67 | 67 | PASS |

## 3) 구현 정합 (CAPL / CFG / DBC)

| Item | Coverage | Status |
| --- | --- | --- |
| CAPL node files | 26/26 | PASS |
| CFG node links | 26/26 | PASS |
| Split DBC files | 5/5 | PASS |
| CFG absolute path hygiene | 0 forbidden path | PASS |

## 4) 경고/조치 항목

- ?놁쓬

## 5) 비고

- `06_Integration_Test.md`는 Lean IT 운영 방침에 따라 `핵심 통합 체인` 위주 커버리지로 관리할 수 있다.
- Validation Harness(`SIL_TEST_CTRL`, `VEHICLE_BASE_TEST_CTRL`)는 검증 전용(Non-Production) 계층으로 관리한다.

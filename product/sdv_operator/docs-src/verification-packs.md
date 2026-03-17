# Verification Packs

`CANoe Test Verification Console`은 native test harness 자체를 만들지 않습니다.  
대신 현재 CANoe에서 고정된 active suite를 **pack**으로 읽고, Dev2 batch/archive와 reviewer-facing 05/06/07 매핑을 같은 운영 축으로 묶습니다.

## Active suite pack 구조

1. `ts_canoe_ut_active_baseline`
- `UT Active Baseline`
- 05 Unit Test exact executable baseline
- official closeout tier
- source:
  - `driving-alert-workproducts/05_Unit_Test.md`
  - `canoe/tests/modules/test_units/README.md`
  - `canoe/docs/verification/test-asset-mapping.md`
  - `canoe/docs/verification/evidence-policy.md`

2. `ts_canoe_it_active_baseline`
- `IT Active Baseline`
- 06 Integration Test exact executable baseline
- official closeout tier
- source:
  - `driving-alert-workproducts/06_Integration_Test.md`
  - `canoe/tests/modules/test_suites/README.md`
  - `canoe/docs/verification/test-asset-mapping.md`
  - `canoe/docs/verification/evidence-policy.md`

3. `ts_canoe_st_active_baseline`
- `ST Active Baseline`
- 07 System Test exact executable baseline
- official closeout tier
- source:
  - `driving-alert-workproducts/07_System_Test.md`
  - `canoe/tests/modules/test_suites/README.md`
  - `canoe/docs/verification/test-asset-mapping.md`
  - `canoe/docs/verification/evidence-policy.md`

4. `ts_canoe_full_active_baseline`
- `FULL Active Baseline`
- UT/IT/ST active wrapper 기준
- regression-only tier
- source:
  - `canoe/tests/modules/test_suites/README.md`
  - `canoe/docs/verification/execution-guide.md`
  - `canoe/docs/verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`
  - `canoe/docs/verification/evidence-policy.md`

## 해석 기준

- suite count와 wrapper 기준은 `test_suites/README.md`가 우선입니다.
- official closeout authority는 `UT / IT / ST`만 갖습니다.
- `FULL`은 regression-only이며 `05/06/07`의 직접적인 PASS/FAIL seed를 대체하지 않습니다.
- official 05/06/07과 native asset/oracle/evidence 매핑은 `test-asset-mapping.md`가 우선입니다.
- `RET_IT_*`, `RET_ST_*` 같은 retired umbrella row는 active baseline closeout seed에서 제외합니다.
- native 실행 순서와 harness 기준은 `execution-guide.md`가 우선입니다.
- candidate verdict와 evidence seed 규칙은 `evidence-policy.md`가 우선입니다.
- reviewer-facing closeout tier 경계는 `VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`가 우선입니다.

## Campaign profile 연결

각 pack은 별도 campaign profile로 바로 실행할 수 있습니다.

- `ut_active_baseline`
- `it_active_baseline`
- `st_active_baseline`
- `full_active_baseline`

profile source:
- `product/sdv_operator/config/campaign_profiles.json`

matrix source:
- `product/sdv_operator/config/verification_pack_matrix.json`

## Console에서 하는 일

Console은 다음만 담당합니다.

- 어떤 pack/profile을 실행했는지 기록
- `run_id / campaign_id / profile_id / pack_id`를 결과물에 넣기
- native report, surface bundle, execution manifest, archive를 같은 run 기준으로 묶기

Console이 하지 않는 일:

- CANoe native test authoring 대체
- Jenkins scheduler 대체

## 권장 읽기 순서

1. `Campaign Profiles`
2. `Verification Packs`
3. `canoe/tests/modules/test_suites/README.md`
4. `canoe/docs/verification/test-asset-mapping.md`
5. `canoe/docs/verification/execution-guide.md`

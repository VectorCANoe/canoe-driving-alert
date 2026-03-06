# Verification Evidence Score Report

- Generated: 2026-03-06 17:32:56
- Input: `canoe\logging\evidence\UT\20260306_qa\verification_log.csv`
- Output CSV: `canoe\tmp\reports\verification\ut_20260306_qa_scored.csv`

## Summary
- Total: 6
- PASS: 0
- FAIL: 6

## Tier Breakdown
| Tier | Total | PASS | FAIL |
| --- | ---: | ---: | ---: |
| IT | 2 | 0 | 2 |
| ST | 2 | 0 | 2 |
| UT | 2 | 0 | 2 |

## Parse Errors
- L2 UT_ADAS_001: latency/input/output missing
- L3 UT_EMS_RX_001: latency/input/output missing
- L4 IT_OUT_001: latency/input/output missing
- L5 IT_BASE_PT_001: latency/input/output missing
- L6 ST_TIMEOUT_001: latency/input/output missing
- L7 ST_V2_FAILSAFE_001: latency/input/output missing

## Metadata Errors
- L2 UT_ADAS_001: run_date invalid or missing
- L3 UT_EMS_RX_001: run_date invalid or missing
- L4 IT_OUT_001: run_date invalid or missing
- L5 IT_BASE_PT_001: run_date invalid or missing
- L6 ST_TIMEOUT_001: run_date invalid or missing
- L7 ST_V2_FAILSAFE_001: run_date invalid or missing

## Axis Errors
- L2 UT_ADAS_001: logic_verdict missing
- L2 UT_ADAS_001: comm_verdict missing
- L3 UT_EMS_RX_001: logic_verdict missing
- L3 UT_EMS_RX_001: comm_verdict missing
- L4 IT_OUT_001: logic_verdict missing
- L4 IT_OUT_001: comm_verdict missing
- L5 IT_BASE_PT_001: logic_verdict missing
- L5 IT_BASE_PT_001: comm_verdict missing
- L6 ST_TIMEOUT_001: logic_verdict missing
- L6 ST_TIMEOUT_001: comm_verdict missing
- L7 ST_V2_FAILSAFE_001: logic_verdict missing
- L7 ST_V2_FAILSAFE_001: comm_verdict missing

## Failed Rows
- UT_ADAS_001 (UT): latency=None rule=LE:150 (latency missing)
- UT_EMS_RX_001 (UT): latency=None rule=BETWEEN:1000:1300 (latency missing)
- IT_OUT_001 (IT): latency=None rule=LE:150 (latency missing)
- IT_BASE_PT_001 (IT): latency=None rule=LE:100 (latency missing)
- ST_TIMEOUT_001 (ST): latency=None rule=BETWEEN:1000:1300 (latency missing)
- ST_V2_FAILSAFE_001 (ST): latency=None rule=LE:150 (latency missing)

## Gate Result
- `FAIL`

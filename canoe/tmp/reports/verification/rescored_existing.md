# Verification Evidence Score Report

- Generated: 2026-03-06 17:36:33
- Input: `canoe\tmp\reports\verification\scored_verification_log.csv`
- Output CSV: `canoe\tmp\reports\verification\rescored_existing.csv`

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

## Metadata Errors
- L2 UT_ADAS_001: owner missing
- L2 UT_ADAS_001: run_date invalid or missing
- L3 UT_EMS_RX_001: owner missing
- L3 UT_EMS_RX_001: run_date invalid or missing
- L4 IT_OUT_001: owner missing
- L4 IT_OUT_001: run_date invalid or missing
- L5 IT_BASE_PT_001: owner missing
- L5 IT_BASE_PT_001: run_date invalid or missing
- L6 ST_TIMEOUT_001: owner missing
- L6 ST_TIMEOUT_001: run_date invalid or missing
- L7 ST_V2_FAILSAFE_001: owner missing
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
- UT_ADAS_001 (UT): latency=120.0 rule=LE:150 (latency <= 150.0)
- UT_EMS_RX_001 (UT): latency=1080.0 rule=BETWEEN:1000:1300 (1000.0 <= latency <= 1300.0)
- IT_OUT_001 (IT): latency=140.0 rule=LE:150 (latency <= 150.0)
- IT_BASE_PT_001 (IT): latency=95.0 rule=LE:100 (latency <= 100.0)
- ST_TIMEOUT_001 (ST): latency=1110.0 rule=BETWEEN:1000:1300 (1000.0 <= latency <= 1300.0)
- ST_V2_FAILSAFE_001 (ST): latency=145.0 rule=LE:150 (latency <= 150.0)

## Gate Result
- `FAIL`

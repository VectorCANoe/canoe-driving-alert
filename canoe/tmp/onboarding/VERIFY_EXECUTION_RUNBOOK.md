# Verify Execution Runbook (Dev Team)

## 1) One-Time

- Prepare run folder:
```powershell
python scripts/run.py verify prepare --run-id <RUN_ID>
```

## 2) CANoe Execution (Manual)

- Run UT/IT/ST scenarios in CANoe.
- No-panel trigger (recommended):
```powershell
python scripts/run.py scenario run --id <SCENARIO_ID>
```
- Save Write Window logs to:
  - `canoe/logging/evidence/UT/<RUN_ID>/raw_write_window.txt`
  - `canoe/logging/evidence/IT/<RUN_ID>/raw_write_window.txt`
  - `canoe/logging/evidence/ST/<RUN_ID>/raw_write_window.txt`
- Ensure logs include `[EVIDENCE_OUT]` lines.

## 3) Preflight Check

```powershell
python scripts/run.py verify status --run-id <RUN_ID>
```

- Expected before finalize:
  - `Overall: READY_FOR_FINALIZE` or `SCORED_READY`
  - No missing marker warning

## 4) One-Shot Finalize

```powershell
python scripts/run.py verify finalize --run-id <RUN_ID> --owner DEV1
```

Outputs:
- tier scored logs: `canoe/logging/evidence/<UT|IT|ST>/<RUN_ID>/verification_log_scored.csv`
- run insight: `canoe/tmp/reports/verification/run_insight_report.md`
- doc fill template: `canoe/tmp/reports/verification/doc_fill_template.csv`

## 5) Apply to 05/06/07

- Use `doc_fill_template.csv`:
  - `pass_fail` -> Pass/Fail
  - `owner` -> 담당자
  - `run_date` -> 일자
  - `evidence_*` -> 증빙 링크
- Rows with `action_required != APPLY_TO_DOC` are unresolved.

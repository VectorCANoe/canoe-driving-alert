# Verification Insight Playbook

## 1) Goal

Run CANoe SIL verification with a repeatable CLI flow and produce:

- scored evidence (`PASS/FAIL`)
- timing KPI and risk hotspots
- actionable next steps for 05/06/07 evidence binding

## 2) Scope Boundary

- CANoe remains execution and source log system.
- CLI performs collection/scoring/insight reporting.
- Panel and Unity are visualization evidence only (manual/semi-automatic capture).

## 3) Standard Execution Flow

1. Prepare run folders
```powershell
python scripts/run.py verify prepare --run-id 20260307_1030
```

2. Execute scenarios in CANoe and save Write Window raw log into:
- `canoe/logging/evidence/<UT|IT|ST>/<run-id>/raw_write_window.txt`

3. Fill and score each tier
```powershell
python scripts/run.py verify fill-score --tier UT --run-id 20260307_1030 --owner DEV1
python scripts/run.py verify fill-score --tier IT --run-id 20260307_1030 --owner DEV1
python scripts/run.py verify fill-score --tier ST --run-id 20260307_1030 --owner DEV1
```

4. Build run-level insight report
```powershell
python scripts/run.py verify insight --run-id 20260307_1030
```

5. Build 05/06/07 doc binding bundle
```powershell
python scripts/run.py verify bind-doc --run-id 20260307_1030
```

6. Build 05/06/07 doc fill template (Pass/Fail, owner, date, evidence links)
```powershell
python scripts/run.py verify fill-template --run-id 20260307_1030 --owner-fallback DEV1
```

7. Optional baseline comparison
```powershell
python scripts/run.py verify insight --run-id 20260307_1030 --baseline-run-id 20260306_qa
```

## 4) Output Artifacts

Per tier (`UT/IT/ST`):

- `verification_log_filled.csv`
- `verification_log_scored.csv`
- `verification_report.md`
- `verification_report.json`

Run-level:

- `canoe/tmp/reports/verification/run_insight_report.md`
- `canoe/tmp/reports/verification/run_insight_report.json`
- `canoe/tmp/reports/verification/doc_binding_bundle.csv`
- `canoe/tmp/reports/verification/doc_binding_bundle.md`
- `canoe/tmp/reports/verification/doc_binding_bundle.json`
- `canoe/tmp/reports/verification/doc_fill_template.csv`
- `canoe/tmp/reports/verification/doc_fill_template.md`

## 5) Insight Interpretation Rules

1. Gate Result
- `PASS`: no hard fail in scored rows
- `FAIL`: at least one scored row failed

2. Near-Limit PASS
- PASS row with low timing margin (default <= 15ms)
- Treat as pre-failure risk and stabilize scheduling/jitter

3. Timing Budget Utilization
- `latency / rule upper-bound`
- High ratio means low safety margin even if currently PASS

4. Scenario Hotspot
- scenario sorted by latency p95
- prioritize top hotspots for CAPL and comm-path tuning

5. Baseline Comparison
- classify into `REGRESSED / IMPROVED / STABLE`
- default threshold: 5ms

## 6) Evidence Binding (05/06/07)

Bind scored outputs by test ID:

- pass/fail value from `computed_verdict`
- evidence link from `evidence_log_path`, `evidence_capture_path`
- supporting rationale from run-level insight report (hotspot/regression/recommendation)

## 7) Operational Notes

- `verify insight` requires scored CSV per tier; run `fill-score` first.
- Keep strict metadata/axis checks enabled unless explicitly waived.
- Do not edit CANoe `*.cfg` by script (GUI-first rule).

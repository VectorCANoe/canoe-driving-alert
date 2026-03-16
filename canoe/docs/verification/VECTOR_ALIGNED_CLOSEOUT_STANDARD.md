# Vector-Aligned Verification Closeout Standard

## 1. Purpose

This standard defines the official operating model for CANoe SIL verification closeout in this repository.

It fixes:
- execution authority
- run/evidence path layout
- post-run automation boundary
- PASS/FAIL state transition rule
- FAIL disposition format
- reviewer approval flow

## 2. Vector-Aligned Principles

This standard follows Vector's public guidance and product positioning:

1. `CANoe` is the core execution platform for simulation, stimulation, testing, and analysis.
2. `vTESTstudio`/native test assets are the authoritative automated test assets.
3. Native test execution produces the authoritative test report artifact.
4. CANoe remains an open platform and may be integrated with external toolchains, CI, and lab environments.
5. External automation may collect, normalize, and bind artifacts, but it must not replace native execution or native report authority.

## 3. Source References

Primary official sources used for this operating model:

1. Vector, CANoe as the core platform for executing tests and simulating/stimulating the environment  
   https://medical.vector.com/articles/simulation-of-surrounding-systems-for-the-extracorporeal-life-support-system-rotaflow
2. Vector, vTESTstudio supports reusable tests and automatic test reports  
   https://medical.vector.com/articles/vteststudio-comfortable-design-of-automated-test-sequences-for-embedded-systems
3. Vector, CANoe is a scalable platform from development to system-level tests  
   https://medical.vector.com/
4. Vector, CANoe open interfaces and extensibility allow integration into toolchains, CI, and lab environments  
   https://medical.vector.com/articles/sdc-validation
5. Vector tutorial snippet, test execution is started in CANoe and the resulting test report is opened afterward  
   https://support.vector.com/sys_attachment.do?sys_id=3a157dec876401d0b9f233770cbb354b

## 4. Execution Authority

### 4.1 Authoritative execution layer

The authoritative execution layer is:
- CANoe measurement
- CANoe Test Configuration
- native test assets
- native Vector report output

### 4.2 External automation boundary

External automation is limited to:
- run folder initialization
- native report collection
- Write Window evidence parsing
- verdict normalization
- document binding bundle generation
- fill template generation

External automation must not:
- replace CANoe native execution
- overwrite native verdict authority
- directly change official `05/06/07` verdict without reviewer approval

## 5. Tier Model

### 5.1 Official closeout tiers

Official closeout tiers:
- `UT`
- `IT`
- `ST`

These tiers are the only tiers that may directly drive official `PASS/FAIL` state transitions in:
- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`
- `00g_Master_Test_Matrix.md`

### 5.2 Regression tier

`FULL` is regression-only.

Rules:
- `FULL` must use a separate run/configuration context.
- `FULL` must not be executed concurrently with `UT/IT/ST`.
- `FULL` does not replace per-ID closeout evidence from `UT/IT/ST`.
- `FULL` may be attached as additional regression evidence only.

## 6. Run Model

### 6.1 Standard execution sequence

1. `prepare`
2. CANoe GUI measurement start
3. CANoe GUI test execution
4. GUI Write Window export to canonical incoming path
5. `post-run`
6. `bind-doc`
7. `fill-template`
8. reviewer approval
9. official document update

### 6.2 GUI-first rule

The following remain GUI-authoritative:
- `.cfg` open/save/save as
- `.cfg.ini`, `.stcfg`
- measurement start/stop
- test execution start
- native report generation

## 7. Canonical Evidence Paths

### 7.1 Canonical evidence root

`canoe/logging/evidence/`

### 7.2 Per-run root

Per run:
- `canoe/logging/evidence/UT/<run_id>/`
- `canoe/logging/evidence/IT/<run_id>/`
- `canoe/logging/evidence/ST/<run_id>/`
- `canoe/logging/evidence/FULL/<run_id>/`

### 7.3 Canonical incoming drop root

Write Window export must be stored only at:
- `canoe/logging/evidence/incoming/UT/raw_write_window.txt`
- `canoe/logging/evidence/incoming/IT/raw_write_window.txt`
- `canoe/logging/evidence/incoming/ST/raw_write_window.txt`
- `canoe/logging/evidence/incoming/FULL/raw_write_window.txt`

Legacy `canoe/tmp/write_window/` is migration fallback only.

### 7.4 Required per-run artifacts

Minimum required artifacts for `UT/IT/ST` closeout:
- `verification_log.csv`
- `capture_index.csv`
- `raw_write_window.txt`
- `native_reports/`
- `native_report_manifest.json`

Recommended artifacts:
- `captures/`
- CAN/Ethernet trace exports
- scored summary outputs
- doc binding bundle
- fill template bundle

## 8. Native Report Rule

The native CANoe/Vector report is the authoritative execution artifact.

Rules:
- collect the summary `Report_<TIER>_ACTIVE_BASELINE.vtestreport`
- collect available per-test `Report_*.vtestreport`
- collect matching report settings files
- store them under the run-local `native_reports/` tree

No custom external script may replace native report verdict generation.

## 9. PASS/FAIL State Transition Rule

### 9.1 Candidate verdict

Automation may generate only a candidate verdict.

Candidate verdict is based on:
- native run existence
- `verification_log.csv`
- parsed evidence
- computed scoring
- document binding alignment

### 9.2 Final verdict

Official final verdict may be changed only after reviewer approval.

Required conditions:
- native report exists
- evidence row exists for the official test ID
- candidate verdict is not empty
- evidence links are present
- failure, if any, has a disposition record

## 10. FAIL Disposition Standard

Every `FAIL` or `ERROR` row requires a disposition record.

Required fields:
- `tier`
- `test_id`
- `scenario_id`
- `native_asset`
- `run_id`
- `failure_class`
- `symptom`
- `root_cause_summary`
- `reproduction_steps`
- `native_report_path`
- `evidence_log_path`
- `trace_or_capture_path`
- `fix_status`
- `retest_required`
- `retest_run_id`
- `final_decision`
- `owner`
- `reviewer`
- `decision_date`

## 11. Reviewer Approval Flow

### 11.1 Candidate generation

Automation generates:
- scored verification log
- doc binding bundle
- fill template

### 11.2 Engineering review

Validation/test owner reviews:
- candidate verdict
- evidence completeness
- failure disposition if present

### 11.3 Document approval

Document owner updates official `05/06/07` and `00g` only after review approval.

## 12. Operating Commands

Standard flow:

```powershell
python scripts/quality/run_verification_pipeline.py prepare --run-id <RUN_ID>
python scripts/quality/run_verification_pipeline.py post-run --run-id <RUN_ID> --tier <UT|IT|ST|FULL> --owner <OWNER>
python scripts/quality/run_verification_pipeline.py bind-doc --run-id <RUN_ID>
python scripts/quality/run_verification_pipeline.py fill-template --run-id <RUN_ID>
```

## 13. Project-Specific Decisions

This repository uses the following project-specific constraints on top of Vector guidance:

1. verification scope is fixed to CANoe SIL, CAN + Ethernet only
2. `UT/IT/ST` are the only official closeout tiers
3. `FULL` is regression-only
4. official document verdict changes remain reviewer-approved, not fully automatic


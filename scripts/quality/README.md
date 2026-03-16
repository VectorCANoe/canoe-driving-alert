# Quality Scripts

Main tools:

- `run_verification_pipeline.py`:
  - `prepare`
  - `smoke`
  - `fill-score`
  - `insight`
  - `bind-doc`
  - `fill-template`
  - `status`
  - `finalize`
- `export_junit_from_batch.py`
- `build_surface_evidence_bundle.py`
- `materialize_verification_artifacts.py`
- `evidence_score_gate.py`
- `build_evidence_from_write_window.py`
- `init_evidence_run.py`
- `package clean --scope staging --yes`
- Gate scripts moved to: `scripts/gates/`

Canonical verification inputs:

- Official test docs:
  - `driving-alert-workproducts/05_Unit_Test.md`
  - `driving-alert-workproducts/06_Integration_Test.md`
  - `driving-alert-workproducts/07_System_Test.md`
- Native asset mapping:
  - `canoe/docs/verification/test-asset-mapping.md`
- Native executable asset source:
  - `canoe/tests/modules/test_units/<asset>/<asset>.can`

Current policy:

- `canoe/AGENT/` and legacy `TMP` evidence sandboxes are reference-only.
- Official `00~07` docs and root `canoe/` assets are the canonical verification SoT.
- `init_evidence_run.py` seeds `verification_log.csv` directly from the official docs and current native assets.
- `expected` is extracted from the official `05/06/07` tables.
- `rule_type` / `rule_ms` are deterministic seeds derived from official table text, not vector/RAG inference.
- Rows with ambiguous timing semantics stay marked for manual confirmation in `note`.

Note:

- `build_evidence_from_write_window.py` parses `[EVIDENCE_OUT]` as key/value pairs.
- `build_evidence_from_write_window.py` also collects current `release` evidence field from `[EVIDENCE_OUT]`.
- `evidence_score_gate.py` now outputs CSV + Markdown + JSON summary with:
  - latency distribution KPI
  - near-limit PASS detection
  - failure reason distribution
  - optional baseline regression comparison
- `build_run_insight_report.py` outputs run-level UT/IT/ST merged insight:
  - tier coverage and hotspot scenarios
  - timing budget utilization ranking
  - recommendation section for next actions
- `build_doc_binding_bundle.py` outputs 05/06/07 binding matrix:
  - READY / DOC_ONLY / EVIDENCE_ONLY status
  - doc ID and scored evidence row alignment
  - carry-forward fields for closeout:
    - `scenario_id`
    - `native_asset`
    - `expected`
    - `rule_type`
    - `rule_ms`
  - csv/json/md bundle for document team handoff
- `build_doc_fill_template.py` outputs 05/06/07 doc fill template:
  - Pass/Fail, owner, date, evidence links per test ID
  - closeout carry-forward:
    - `scenario_id`
    - `native_asset`
    - `expected`
    - `rule_type`
    - `rule_ms`
  - action-required flag for missing evidence or missing doc IDs
  - READY rows without final verdict are flagged as `REVIEW_READY_ROW`
  - csv/md bundle for direct document update work
- `init_evidence_run.py` now produces:
  - `verification_log.csv` with `native_asset`, `scenario_id`, `expected`, `rule_type`, `rule_ms`
  - `capture_index.csv`
  - empty `raw_write_window.txt`
  - seeded rows based on current official IDs and `launchScenarioAndWait(...)` calls
- `check_run_readiness.py` outputs run readiness report:
  - template/raw/scored existence by UT/IT/ST
  - evidence marker count (`[EVIDENCE_OUT]`)
  - overall status (`NOT_PREPARED`, `PREPARED_PARTIAL`, `READY_FOR_FINALIZE`, `SCORED_READY`)
- CLI readiness gate report output:
  - `canoe/tmp/reports/verification/cli_readiness_gate.json`
  - `canoe/tmp/reports/verification/cli_readiness_gate.md`
- `export_junit_from_batch.py` outputs Jenkins-ingestible JUnit XML:
  - `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`
- `build_surface_evidence_bundle.py` outputs reviewer-facing surface ECU rollups:
  - `canoe/tmp/reports/verification/surface_evidence_bundle.json`
  - `canoe/tmp/reports/verification/surface_evidence_bundle.md`
  - `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.json`
  - `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.md`
  - input SoT:
    - `product/sdv_operator/config/surface_ecu_inventory.json`
    - `product/sdv_operator/config/surface_traceability_profile.json`
    - `canoe/tmp/reports/verification/dev_completeness_smoke.csv`
  - output meaning:
    - execution key: `run_id / phase / owner / run_date`
    - stable review key: `Req ID / Test Case ID / Scenario ID / Surface ECU`
  - verdict policy:
    - `product/sdv_operator/config/verification_phase_policy.json`
- `materialize_verification_artifacts.py` re-packs staging outputs into stable archive layout:
  - `artifacts/verification_runs/<run_id>/<phase>/reports/*`
  - `artifacts/verification_runs/<run_id>/<phase>/surface/<bundle_key>/*`
  - `artifacts/verification_runs/<run_id>/<phase>/native_reports/**/*`
  - `artifacts/verification_runs/<run_id>/<phase>/evidence/<UT|IT|ST>/**/*`
  - `artifacts/verification_runs/<run_id>/<phase>/manifests/artifact_manifest.json`
  - `artifacts/verification_runs/<run_id>/<phase>/manifests/execution_manifest.json`
- This allows CAPL evidence lines to add fields without breaking parsing.
- Gate purpose/CI mapping reference: `product/sdv_operator/docs-src/maintenance.md`
- `canoe/tmp/reports/verification`는 staging output 전용이며 Git 추적 대상이 아닙니다.

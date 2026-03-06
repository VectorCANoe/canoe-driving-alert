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
- `evidence_score_gate.py`
- `build_evidence_from_write_window.py`
- `init_evidence_run.py`
- Gate scripts moved to: `scripts/gates/`

Note:

- `build_evidence_from_write_window.py` parses `[EVIDENCE_OUT]` as key/value pairs.
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
  - csv/json/md bundle for document team handoff
- `build_doc_fill_template.py` outputs 05/06/07 doc fill template:
  - Pass/Fail, owner, date, evidence links per test ID
  - action-required flag for missing evidence or missing doc IDs
  - csv/md bundle for direct document update work
- `check_run_readiness.py` outputs run readiness report:
  - template/raw/scored existence by UT/IT/ST
  - evidence marker count (`[EVIDENCE_OUT]`)
  - overall status (`NOT_PREPARED`, `PREPARED_PARTIAL`, `READY_FOR_FINALIZE`, `SCORED_READY`)
- CLI readiness gate report output:
  - `canoe/tmp/reports/verification/cli_readiness_gate.json`
  - `canoe/tmp/reports/verification/cli_readiness_gate.md`
- This allows CAPL evidence lines to add fields without breaking parsing.
- Gate purpose/CI mapping reference: `scripts/GATE_MATRIX.md`

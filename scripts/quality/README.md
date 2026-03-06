# Quality Scripts

Main tools:

- `run_verification_pipeline.py`:
  - `prepare`
  - `smoke`
  - `fill-score`
  - `insight`
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
- CLI readiness gate report output:
  - `canoe/tmp/reports/verification/cli_readiness_gate.json`
  - `canoe/tmp/reports/verification/cli_readiness_gate.md`
- This allows CAPL evidence lines to add fields without breaking parsing.
- Gate purpose/CI mapping reference: `scripts/GATE_MATRIX.md`

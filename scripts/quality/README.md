# Quality Scripts

Main tools:

- `run_verification_pipeline.py`:
  - `prepare`
  - `smoke`
  - `fill-score`
- `doc_code_sync_gate.py`
- `cfg_hygiene_gate.py`
- `check_capl_sync.py`
- `evidence_score_gate.py`
- `build_evidence_from_write_window.py`
- `init_evidence_run.py`

Note:

- `build_evidence_from_write_window.py` parses `[EVIDENCE_OUT]` as key/value pairs.
- This allows CAPL evidence lines to add fields without breaking parsing.

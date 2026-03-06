# Scripts Layout

This folder is organized by purpose.

## `scripts/quality/`
- Quality gates and validation utilities.
- Active CI gate:
  - `scripts/quality/doc_code_sync_gate.py`
- Push-time CANoe text hygiene gate:
  - `scripts/quality/cfg_hygiene_gate.py`
- DBC validation helpers:
  - `scripts/quality/dbc/test_dbc_validation.py`
- CAPL mirror sync gate:
  - `scripts/quality/check_capl_sync.py`
- Evidence score gate:
  - `scripts/quality/evidence_score_gate.py`
- Evidence run bootstrap:
  - `scripts/quality/init_evidence_run.py`
- Write-window evidence auto fill:
  - `scripts/quality/build_evidence_from_write_window.py`
- Development completeness smoke check:
  - `scripts/quality/dev_completeness_smoke.py`

## `scripts/canoe/`
- CANoe configuration and CAPL linkage helpers.
- Includes:
  - `attach_capl.py`
  - `check_nodes.py`
  - `fix_nodes.py`
  - `reload_cfg.py`
  - `reload_wait.py`
  - `setup_canoe_config.py`

## `scripts/docs/`
- Document generation/refactor helpers used during writing iterations.
- Includes completion/expand/fix/restructure utilities.

## `scripts/report/`
- Report conversion/export helpers.

## Compatibility
- `scripts/doc_code_sync_gate.py` is a wrapper kept for backward compatibility.
- Preferred entrypoint is `scripts/quality/doc_code_sync_gate.py`.

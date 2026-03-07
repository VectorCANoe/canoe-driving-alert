# Script Inventory and CLI Classification

This file defines how current script assets are classified before CLI productization.

## 1) Script Roots

- `scripts/`: project-level automation (quality gates, verification, CANoe maintenance, docs/report helpers)
- `canoe/scripts/`: CANoe panel/Unity bridge and simulator utilities

## 2) Classification

- `A-CORE`:
  - Stable and should be exposed via official CLI commands.
- `B-OPS`:
  - Operational helpers; exposed only for advanced users.
- `C-EXPERIMENT`:
  - Optional/experimental tooling; keep as direct script usage.
- `D-LEGACY`:
  - Historical or one-off generation scripts; not part of daily CLI.

## 3) Current Mapping

### A-CORE (Expose in CLI)

- `scripts/run.py`
- `scripts/quality/run_verification_pipeline.py`
- `scripts/quality/init_evidence_run.py`
- `scripts/quality/build_evidence_from_write_window.py`
- `scripts/quality/evidence_score_gate.py`
- `scripts/quality/build_run_insight_report.py`
- `scripts/quality/build_doc_binding_bundle.py`
- `scripts/quality/build_doc_fill_template.py`
- `scripts/quality/check_run_readiness.py`
- `scripts/quality/dev_completeness_smoke.py`
- `scripts/gates/doc_code_sync_gate.py`
- `scripts/gates/cfg_hygiene_gate.py`
- `scripts/gates/check_capl_sync.py`
- `scripts/gates/cli_readiness_gate.py`

### B-OPS (Advanced group in CLI, hidden from basic quick-start)

- `scripts/canoe/attach_capl.py`
- `scripts/canoe/check_nodes.py`
- `scripts/canoe/fix_nodes.py`
- `scripts/canoe/reload_cfg.py`
- `scripts/canoe/reload_wait.py`
- `scripts/canoe/setup_canoe_config.py`
- `scripts/canoe/send_scenario_command.py`
- `canoe/scripts/navigation_simulator.py`
- `canoe/scripts/audit_panel_bindings.py`
- `canoe/scripts/check_panel_split_status.py`
- `canoe/scripts/sync_unity_integration.py`
- `canoe/scripts/verify_unity_integration_sync.py`
- `canoe/scripts/unity_standard_pipeline.py`
- `canoe/scripts/unity_renderer_bridge.py`
- `canoe/scripts/unity_renderer_mock_sender.py`
- `canoe/scripts/build_unity_skin_pack.py`
- `canoe/scripts/generate_macro_skin_assets.py`
- `scripts/release/build_sdv_exe.py`

### C-EXPERIMENT (Direct only, no official CLI surface yet)

- `canoe/scripts/fix_cfg_paths.py` (cfg direct patch style)
- `canoe/scripts/fix_new_cfg.py` (cfg direct patch style)

### D-LEGACY (Keep, but not in new CLI scope)

- `scripts/docs/*.py` (bulk document generation/refactor scripts)
- `scripts/report/*.py` (report conversion utilities)
- `scripts/quality/dbc/test_dbc_validation.py` (can be called via tests, not end-user CLI command first)

## 4) CLI Exposure Policy

- Basic users only see `A-CORE`.
- `B-OPS` commands are available under an explicit namespace (e.g. `ops` / `unity`) and documented as advanced.
- `C-EXPERIMENT` stays excluded from official CLI help until migrated to safe interfaces.
- `D-LEGACY` remains script-level until explicit modernization.

## 5) CI Usage Snapshot

Current GitHub workflows call `scripts/run.py`:

- `.github/workflows/doc-code-sync-gate.yml` -> `python scripts/run.py gate doc-sync`
- `.github/workflows/cfg-hygiene-gate.yml` -> `python scripts/run.py gate cfg-hygiene` + `python scripts/run.py gate capl-sync`
- `.github/workflows/cli-readiness-gate.yml` -> `python scripts/run.py gate cli-readiness`

Target direction:

- CI should call the official CLI entrypoint (`scripts/run.py` now, packaged CLI later).

## 6) Command Contract (Frozen Baseline)

Canonical:

- `python scripts/run.py scenario run --id <0..255>`
- `python scripts/run.py verify prepare --run-id <RUN_ID>`
- `python scripts/run.py verify smoke --owner <OWNER>`
- `python scripts/run.py verify fill-score --tier <UT|IT|ST> --run-id <RUN_ID> --owner <OWNER>`
- `python scripts/run.py verify insight --run-id <RUN_ID> [--baseline-run-id <RUN_ID>]`
- `python scripts/run.py verify bind-doc --run-id <RUN_ID>`
- `python scripts/run.py verify fill-template --run-id <RUN_ID>`
- `python scripts/run.py verify status --run-id <RUN_ID>`
- `python scripts/run.py verify finalize --run-id <RUN_ID> --owner <OWNER>`
- `python scripts/run.py gate doc-sync`
- `python scripts/run.py gate cfg-hygiene`
- `python scripts/run.py gate capl-sync`
- `python scripts/run.py gate cli-readiness`
- `python scripts/run.py package build-exe --mode <onefolder|onefile>`

Compatibility aliases remain enabled during transition:

- `scenario-run`
- `verify-prepare`, `verify-smoke`, `verify-fill-score`, `verify-insight`, `verify-bind-doc`
- `verify-fill-template`
- `verify-status`
- `verify-finalize`
- `gate-doc-sync`, `gate-cfg-hygiene`, `gate-capl-sync`

## 7) Packaging Baseline (F3)

- `pyproject.toml` defines installable CLI entrypoint:
  - `sdv = sdv_cli:main`
- `sdv_cli.py` resolves repository root and delegates to `scripts/run.py`.
- Local install command:
  - `python -m pip install -e .`

# Reference Docs Index

This folder contains non-daily strategy notes, intake records, and supporting references.

## Start Here

Open these only when the active task needs background support:

1. `REFERENCE_SELECTION.md`
2. `MENTOR_PRIORITY_BP.md`
3. `CAPL_coding_guideline.md`

## Current Buckets

- `REFERENCE_SELECTION.md`
  - rules for choosing which references to trust
- `MENTOR_PRIORITY_BP.md`
  - mentor-driven priority interpretation
- `CAPL_coding_guideline.md`
  - coding guidance reference
- `OEM_SURFACE_ECU_EXPANSION_PLAN_2026-03-09.md`
  - Dev1 vehicle-program surface ECU expansion baseline using local OEM/OpenDBC references
- `OEM_ECU_CANDIDATE_BANK_2026-03-09.md`
  - expanded OEM ECU candidate screening table from local reference DBC and legacy samples
- `OEM_WIDE_SURFACE_ECU_INVENTORY_V1_2026-03-09.md`
  - widened 30+ surface ECU inventory for OEM-scale vehicle-program framing
- `OEM_ACTIVE_TARGET_PROFILE_2026-03-09.md`
  - active Dev1 target profile: `100` surface ECUs, `54` deep runtimes, `8` core custom surfaces, `4` validation/test elements
- `OEM_100_ECU_PROGRAM_BANK_2026-03-09.md`
  - active surface inventory bank for 100-scale OEM vehicle-program framing
- `OEM_PLACEHOLDER_WAVE1_2026-03-09.md`
  - materialized placeholder wave: `13` deep anchors + `87` shallow placeholders = `100` visible CAPL nodes
- `OEM_PLACEHOLDER_NAMING_AUDIT_2026-03-09.md`
  - audit of the 100-node placeholder bank against OEM/HKG-style surface naming
- `ECU_PARALLEL_EXECUTION_STRATEGY_2026-03-09.md`
  - active Dev1 execution split: domain-wave development first, placeholder breadth second
- `PRIMARY56_RUNTIME26_MAPPING_2026-03-09.md`
  - executable Dev1 mapping baseline from the active runtime set into the `56` primary reviewer-facing ECU surfaces
- `LICENSE_REFERENCE_REPORT.md`
  - license/reference inventory
- `OPEN_SOURCE_INTAKE_POLICY.md`
  - OSS intake boundary
- `OSS_PANEL_REFERENCE_INDEX.md`
  - panel-side OSS references

## Working Rule

- This folder is not part of the daily active SoT surface.
- If a note becomes part of the daily working path, move or link it from a more active folder.
- For the current reset cycle:
  - use `OEM_ACTIVE_TARGET_PROFILE_2026-03-09.md` as the active Dev1 sizing target
  - use `OEM_100_ECU_PROGRAM_BANK_2026-03-09.md` as the active breadth source bank
  - use `OEM_PLACEHOLDER_WAVE1_2026-03-09.md` as the current visible node materialization baseline
- [RUNTIME_ABSORPTION_STATUS_2026-03-09.md](RUNTIME_ABSORPTION_STATUS_2026-03-09.md) - current Dev1 absorption boundary and GUI cleanup queue.
- [OEM_RUNTIME_ANCHOR_NAMING_AUDIT_2026-03-09.md](OEM_RUNTIME_ANCHOR_NAMING_AUDIT_2026-03-09.md) - recheck of remaining runtime anchors and OEM-normalized names.
- [RUNTIME_RENAME_SPLIT_PLAN_2026-03-09.md](RUNTIME_RENAME_SPLIT_PLAN_2026-03-09.md) - split between source/file rename targets and GUI-only rename targets.

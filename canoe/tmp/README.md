# canoe/tmp

Temporary working area for CANoe-side artifacts.

## Structure
- `assets/screenshots/`: local screenshots and quick captures (ignored by git)
- `backups/cfg/`: local backup files from config recovery (ignored by git)
- `backups/sysvars/`: local sysvar backup snapshots (ignored by git)
- `reports/dbc/`: DBC split/quality reports
- `reports/contracts/`: manual contract verification reports
- `reports/oss/`: OSS intake/audit reports
- `snapshots/`: markdown snapshots for temporary state notes
- `dbc_compare/`: DBC comparison workspace and generated backups

## Keep at root
- `mentor_priority_gate_report.md`
  - Used as default output path by `canoe/tools/validate_mentor_priority.py`

## Rules
- Keep this directory for working artifacts and evidence drafts only.
- Do not store canonical requirements/architecture SoT here.
- If a report becomes stable and referenced by process docs, move it to `canoe/docs/operations/`.

# tools

Utility scripts for CANoe project maintenance.

## Manual-first policy
- DBC quality is decided by human review, not by script output.
- `driving-situation-alert` documents are the source of truth.
- Scripts in this folder are support tools only.

## `generate_dbc_from_docs.py`
- Purpose: generate baseline/split DBC drafts from latest 0303/0304 docs.
- Output path: `canoe/databases/`
- Limitation: parser assumes stable Markdown headings/table formats.
- Required practice: always compare generated DBC with current document intent and CAPL/runtime usage.

## `validate_mentor_priority.py`
- Purpose: enforce mentor-priority gates for active CAN/ETH contract.
- Inputs:
  - Active split DBC set (`chassis/powertrain/body/infotainment/test`)
  - Ethernet contract (`canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`)
- Outputs:
  - Ownership matrix: `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`
  - Gate report: `canoe/tmp/mentor_priority_gate_report.md`
- Exit code:
  - `0` = pass
  - `2` = gate failed

## AI usage note
- If an AI agent runs tools in this folder, it must verify document template compatibility first.
- If an AI agent runs tools in this folder, it must treat generated files as draft artifacts.
- If an AI agent runs tools in this folder, it must request or perform manual verification before integration.

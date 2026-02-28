# tools

Utility scripts for CANoe project maintenance.

## Manual-first policy
- DBC quality is decided by human review, not by script output.
- `driving-situation-alert` documents are the source of truth.
- Scripts in this folder are support tools only.

## `generate_dbc_from_docs.py`
- Purpose: generate baseline/split DBC drafts from latest 0303/0304 docs.
- Output path: `canoe/network/dbc/`
- Limitation: parser assumes stable Markdown headings/table formats.
- Required practice: always compare generated DBC with current document intent and CAPL/runtime usage.

## AI usage note
- If an AI agent runs tools in this folder, it must verify document template compatibility first.
- If an AI agent runs tools in this folder, it must treat generated files as draft artifacts.
- If an AI agent runs tools in this folder, it must request or perform manual verification before integration.

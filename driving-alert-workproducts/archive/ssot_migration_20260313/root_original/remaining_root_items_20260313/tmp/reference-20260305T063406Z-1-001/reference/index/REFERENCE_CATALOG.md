# Reference Catalog (Local RAG Vault)

Updated: 2026-03-05
Location: `driving-situation-alert/reference/`

## Purpose
- Internal + external reference originals for continuous lookup.
- Local-only storage (excluded from Git tracking).

## Structure
- `internal/`
  - `root_reference/` (copied from repository `reference/`)
  - `meeting_notes/` (copied from `docs/meeting-notes/`)
  - `project_docs/` (AGENTS/TMP_HANDOFF snapshots + mentoring docs)
- `standards/`
  - Linux CAN/ISO-TP documentation pages
  - AUTOSAR RS General PDF (available version)
- `industry/`
  - Kvaser / CSS Electronics CAN, CAN FD, DBC, J1939 articles
- `papers/`
  - CAN schedulability and CAN-security related papers (PDF)
- `opensource/`
  - `opendbc`, `can-utils`, `python-can`, `cantools`, `canmatrix`

## Download Sources
- `tmp/url_list.txt`
- `tmp/url_list_extra.txt`
- Fail log (if any): `tmp/download_failed.log`, `tmp/download_failed_extra.log`

## Note
- Some external URLs can return 404 by release/version policy changes.
- If needed, refresh URLs and re-run bulk download.

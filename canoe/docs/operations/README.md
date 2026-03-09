# Operations Docs Index

This folder contains CANoe-side process, verification, and reference documents.

The active top-level surface is intentionally small.
Most dated, one-off, or topic-specific documents are now grouped under subfolders.

## Start Here

Open these first:

1. `DEV_DOC_ENTRYPOINT.md`
2. `ETH_INTERFACE_CONTRACT.md`
3. `CAN_MESSAGE_OWNERSHIP_MATRIX.md`
4. `MULTIBUS_ASSIGNMENT_POLICY.md`
5. `VERIFICATION_EVIDENCE_LOG_STANDARD.md`
6. `CLI_PRODUCTIZATION_BP.md`

## Top-Level Active Docs

These remain at the top level because they are part of normal working flow:

- `DEV_DOC_ENTRYPOINT.md`
- `ETH_INTERFACE_CONTRACT.md`
- `CAN_MESSAGE_OWNERSHIP_MATRIX.md`
- `MULTIBUS_ASSIGNMENT_POLICY.md`
- `VERIFICATION_EVIDENCE_LOG_STANDARD.md`
- `CLI_PRODUCTIZATION_BP.md`
- `README.md`

## Subfolders

### `verification/`
Verification-specific runbooks and pass criteria.

Current closeout anchor:

- `verification/FINAL_PHASE_EXECUTION_FLOW.md`
- `verification/README.md`

### `audit/`
Audit, runtime review, sync queue, and dated review snapshots.

Primary index:

- `audit/README.md`

### `panel/`
Panel/XVP guidance, reference matrix, and panel-specific checklists.

Primary index:

- `panel/README.md`

### `unity/`
Unity and external-renderer bridge references.

Primary index:

- `unity/README.md`

### `reference/`
Strategy notes, intake notes, guideline-style references, and non-daily supporting docs.

Primary index:

- `reference/README.md`

## Operating Rule

When adding a new document to this area:

1. keep it at top level only if it belongs to daily active flow
2. otherwise place it directly in the appropriate subfolder
3. do not create new dated top-level notes unless they are part of the active surface

## Complexity Rule

A developer should be able to understand the folder by looking at:

- top-level active docs
- one task-specific subfolder

If they need to scan dozens of mixed files, the structure is failing.

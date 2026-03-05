# Open Source Intake Policy (CANoe-IVI-OTA)

Document ID: CANOE-OSS-POLICY
Version: 1.0
Date: 2026-03-01
Status: Active
Scope: `canoe/` implementation and reference intake

## 1. Purpose
This policy defines how external open-source references are evaluated and used in this project.
Goal is to accelerate implementation while preserving traceability, license compliance, and rollback safety.

## 2. Storage Rules
- External references must be stored under `canoe/reference/oss/`.
- Vendor sample bundles must be stored under `canoe/reference/vector_samples_19_4_10/` (or versioned sibling folder).
- Reference folders are read-only for development decisions unless explicitly curated into project code.

## 3. License Gate (Mandatory)
- Green: MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0
  - Allowed for code-level adaptation with attribution.
- Yellow: MPL-2.0, LGPL-family
  - Allowed for pattern/reference and integration-level use.
  - Direct source copy requires separate review and obligations check.
- Red: GPL-family (without explicit exception) or unknown/mixed unresolved license
  - No direct code copy into project runtime code.
  - Reference-only usage is allowed.

## 4. Adoption Principles (Non-negotiable)
- No wholesale overwrite from references.
- Apply partial changes only, with narrow commit scope.
- Keep domain-separated DBC topology (`*_can.dbc`) intact.
- Preserve 1:1 traceability chain:
  - Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST
- Every imported pattern must record source path and adaptation rationale in commit message or linked report.

## 5. Double-check Checklist (Required)
Before merging any adaptation from external reference:
1. Verify sender/receiver ownership alignment against `CAN_MESSAGE_OWNERSHIP_MATRIX.md`.
2. Verify active v2 cfg node linkage coverage vs `canoe/src/capl/**/*.can`.
3. Verify non-reserved signal assignments for output messages.
4. Verify no domain merge/regression in DBC set.
5. Verify test evidence trace hook exists (05/06/07 chain target).

## 6. Current Intake Sources
- Vector samples: `canoe/reference/vector_samples_19_4_10`
- Legacy internal references: `reference/legacy/capl_nodes`
- OSS references: `canoe/reference/oss/*`

## 7. Enforcement
If policy conflicts with ad-hoc implementation speed, policy wins.
Exceptions must be documented in `canoe/tmp` with owner/date and explicit rollback plan.


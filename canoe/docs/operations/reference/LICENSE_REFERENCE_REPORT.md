# License Reference Report

Document ID: CANOE-LICENSE-REF-REPORT  
Date: 2026-03-07  
Status: Active (Operational Reference)

## 1) Purpose

Provide one operational reference for license handling boundaries across:

- project-authored code/docs,
- vendor-commercial tools and sample assets,
- open-source references.

This file is a project process reference, not legal advice.

## 2) Asset Classification

| Asset Class | Example Path | Typical License Basis | Redistribution Policy |
|---|---|---|---|
| Project-authored assets | `canoe/src/**`, `driving-situation-alert/**`, `scripts/**` | Project policy / bootcamp agreement | Allowed by project governance |
| Vendor tool dependency | Vector CANoe executable/runtime | Vendor EULA / contract | Do not redistribute tool binaries or installer assets in repo |
| Vendor sample bundles | `reference/vector_samples_19_4_10/**` | Vendor sample terms / EULA context | Treat as reference-only unless explicit redistribution permission exists |
| OSS references | `canoe/reference/oss/**` | OSS license per package | Allowed per intake policy and license gate obligations |

## 3) Required References

- Open source intake policy:
  - `canoe/docs/operations/reference/OPEN_SOURCE_INTAKE_POLICY.md`
- Gate matrix:
  - `scripts/GATE_MATRIX.md`
- Git ownership of gate/workflow policy:
  - `.github/CODEOWNERS`
- Local vendor sample-included notice path:
  - `reference/vector_samples_19_4_10/`

## 4) Current Risk Notes

1. `reference/vector_samples_19_4_10/` is a large vendor sample bundle and may include mixed third-party notices.
2. If this repository is shared beyond internal/contract scope, redistribute only after verifying explicit permission for bundled vendor samples.
3. Keep vendor samples out of runtime code path; use them for pattern/reference only.

## 5) Operational Controls

1. `.gitignore` must include vendor sample path(s):
   - `reference/vector_samples_19_4_10/`
2. Before merging external reference adaptations:
   - run `python scripts/run.py gate doc-sync`
   - run `python scripts/run.py gate cfg-hygiene`
3. If vendor sample assets are already tracked in Git:
   - plan a dedicated cleanup change (`git rm --cached -r ...`) with team approval,
   - keep this as a separate commit from functional changes.

## 6) Decision Guidance (Quick)

- "Should CANoe Vector license/EULA be added into this repo?"
  - Add **notice/reference links**, yes.
  - Commit vendor EULA texts/binaries blindly, no.
- "Should vector sample bundle be excluded from Git?"
  - Yes, by default.
  - If already tracked, remove in a dedicated cleanup step after coordination.

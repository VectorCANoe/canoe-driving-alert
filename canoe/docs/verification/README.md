# Verification Docs

This folder defines the active verification documents for the CANoe SIL baseline.

## Active Docs

- `execution-guide.md`
  - native CANoe Test Unit registration and execution flow
- `acceptance-criteria.md`
  - SIL pass/fail criteria
- `oracle.md`
  - oracle definition for contract, behavior, harness, and evidence checks
- `evidence-policy.md`
  - evidence logging and completion policy
- `test-asset-mapping.md`
  - official mapping from `05/06/07` IDs to native assets, oracle, and evidence
- `diagnostic-coverage.md`
  - current official diagnostic-linked verification scope
- `native-test-asset-naming.md`
  - naming rule for executable native CANoe test assets
- `diagnostic-seam-design.md`
  - minimum seam design for the current diagnostic-linked scope

## Working Rule

- Keep this folder limited to execution, verdict, oracle, and evidence rules.
- Keep temporary team coordination and packaging ownership outside this folder.

## Current diagnostic execution baseline

The active diagnostic verification baseline is currently anchored to four official items:
`UT_063`, `UT_064`, `IT_027`, and `ST_038`.
Their current `TEST_SCN` scenario bindings are `203`, `204`, `205`, and `202` respectively.
Producer wiring is in place in `SGW.can`, `DCM.can`, and `TEST_SCN.can`; compile and runtime evidence remain separate pending gates.

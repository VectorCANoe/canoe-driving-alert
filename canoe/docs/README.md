# CANoe Documentation

This folder provides the official developer documentation for the CANoe SIL baseline. It explains how the runtime surface is structured, how interfaces are contracted, how verification is executed, and how results are judged.

## Language Packs

- `English (canonical)`
  - this folder is the authoritative source for CANoe-side developer documentation
- `한국어 문서 묶음`
  - `Kor/README.md`
  - key contracts and verification guides mirrored in Korean for internal operator and reviewer use
  - technical identifiers, IDs, and asset names remain aligned to the English canonical docs

## Start Here

1. `architecture/ecu-classification.md`
2. `architecture/surface-runtime-verification-map.md`
3. `architecture/ecu-flow-appendix.md`
4. `architecture/skeleton.md`
5. `contracts/layer-separation-policy.md`
6. `contracts/communication-matrix.md`
7. `contracts/owner-route.md`
8. `verification/oracle.md`

## Curated Delivery Set

Use this shortlist when you need the actual provided document subset rather than the full reference tree.

- English key contracts
  - `contracts/communication-matrix.md`
  - `contracts/layer-separation-policy.md`
  - `contracts/owner-route.md`
  - `contracts/multibus-policy.md`
  - `contracts/ethernet-interface.md`
  - `contracts/panel-sysvar-contract.md`
  - `contracts/diagnostic-matrix.md`
  - `contracts/diagnostic-sysvar-contract.md`
- English key verification docs
  - `verification/test-asset-mapping.md`
  - `verification/execution-guide.md`
  - `verification/oracle.md`
  - `verification/acceptance-criteria.md`
  - `verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`
  - `verification/evidence-policy.md`
  - `verification/diagnostic-coverage.md`
- Korean key pack
  - `Kor/README.md`
  - `Kor/contracts/communication-matrix.md`
  - `Kor/contracts/layer-separation-policy.md`
  - `Kor/contracts/owner-route.md`
  - `Kor/contracts/multibus-policy.md`
  - `Kor/contracts/ethernet-interface.md`
  - `Kor/contracts/panel-sysvar-contract.md`
  - `Kor/contracts/diagnostic-matrix.md`
  - `Kor/contracts/diagnostic-sysvar-contract.md`
  - `Kor/verification/test-asset-mapping.md`
  - `Kor/verification/execution-guide.md`
  - `Kor/verification/oracle.md`
  - `Kor/verification/acceptance-criteria.md`
  - `Kor/verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`
  - `Kor/verification/evidence-policy.md`
  - `Kor/verification/diagnostic-coverage.md`
  - `../tests/modules/test_units/README.ko.md`
  - `../tests/modules/test_suites/README.ko.md`

## Architecture

- `architecture/ecu-classification.md`
- `architecture/surface-runtime-verification-map.md`
- `architecture/ecu-flow-appendix.md`
- `architecture/skeleton.md`
- `architecture/master_book/README.md`
  - full ECU master-book asset pack
  - 101-ECU cards, grouped SVG views, and feature/action signal-flow companions

## Contracts

- `contracts/communication-matrix.md`
- `contracts/layer-separation-policy.md`
- `contracts/owner-route.md`
- `contracts/multibus-policy.md`
- `contracts/ethernet-interface.md`
- `contracts/ethernet-backbone.md`
- `contracts/panel-sysvar-contract.md`
- `contracts/diagnostic-description.md`
- `contracts/diagnostic-matrix.md`
- `contracts/diagnostic-sysvar-contract.md`

## Verification

- `verification/test-asset-mapping.md`
- `verification/execution-guide.md`
- `verification/oracle.md`
- `verification/acceptance-criteria.md`
- `verification/VECTOR_ALIGNED_CLOSEOUT_STANDARD.md`
- `verification/evidence-policy.md`
- `verification/diagnostic-coverage.md`
- `verification/diagnostic-seam-design.md`
- `verification/native-test-asset-naming.md`
- `verification/test-suite-composition.md`

## Operations

- `operations/gui-operations.md`
- `operations/sync-rule.md`
- `operations/run-procedure.md`

## Simulation and Test Workflow

1. Read `architecture/` to understand the runtime shape and ECU roles.
2. Read `contracts/` to identify owners, routes, timeout behavior, and interface boundaries.
3. Use `operations/` when applying GUI-first changes or syncing `src/capl` with `cfg/channel_assign`.
4. Run and judge verification with `verification/execution-guide.md`, `verification/acceptance-criteria.md`, `verification/oracle.md`, and `verification/evidence-policy.md`.

## Test Result Handling

- `verification/oracle.md`
  - defines what must be true for a result to be accepted as correct
- `verification/acceptance-criteria.md`
  - defines scenario-level PASS or FAIL conditions
- `verification/evidence-policy.md`
  - defines what evidence must be retained for review
- `verification/execution-guide.md`
  - defines how native CANoe test execution is performed for this baseline

## Related Documents

- `../README.md`
  - external entry point for the CANoe repository surface
- `../cfg/GUI_ONLY_OPERATIONS.md`
  - GUI-first constraints for CANoe configuration handling

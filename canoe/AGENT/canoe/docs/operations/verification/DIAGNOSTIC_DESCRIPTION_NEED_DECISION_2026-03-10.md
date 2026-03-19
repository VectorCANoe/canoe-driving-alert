# Diagnostic Description Need Decision (2026-03-10)

## Question

Can Dev1 and Dev2 proceed using finalized `00~07` documents only, without a separate diagnostic description layer?

## Decision

No.

The finalized `00~07` set is sufficient for:
- scope
- traceability
- ECU ownership direction
- verification mapping

But it is still insufficient as an **executable diagnostic contract** for:
- Dev1 testcase oracle wiring
- Dev2 pipeline key freeze
- tester-driven per-ECU request/response interpretation

Therefore a lightweight **Basic Diagnostic Description** is still required.

## What 00~07 Already Covers

The current docs team baseline already defines diagnostic scope and traceability well enough for program-level control.

Examples verified on current `origin/main`:
- `01_Requirements.md`
  - A1 infrastructure/integration scope references `CGW`, `ETH_BACKBONE`, `DCM`, `IBOX`, `SGW`
  - system/diagnostic verification IDs already exist
- `0302_NWflowDef.md`
  - request/response message flow exists for Chassis / BCM / IVI / Powertrain diagnostic paths
- `0303_Communication_Specification.md`
  - diagnostic request/response frames, IDs, signal fields, and direction are defined
- `0304_System_Variables.md`
  - diagnostic-related state variables are mapped for Chassis / Body / Infotainment / Powertrain
- `05/06/07`
  - diagnostic UT/IT/ST IDs and pass criteria references already exist

## What 00~07 Does Not Provide

The finalized docs do **not** yet provide a compact, tester-facing, execution-ready diagnostic description table with all of the following in one place:
- ECU canonical short name
- request frame name
- response frame name
- SID
- DID
- expected positive response code
- timeout rule
- source bus / target bus
- coverage tier (`FULL` / `BASIC` / `DEFERRED`)
- Dev2 aggregation key mapping

This means `00~07` is strong as SoT, but weak as a direct runbook for:
- native diagnostic testcase oracle implementation
- Dev2 Jenkins/TUI/CLI result normalization

## Why A Basic Diagnostic Description Is Still Needed

A lightweight description layer gives:
- a single compact execution contract for Dev1 and Dev2
- a stable source for testcase asserts
- a stable source for pipeline result keys
- a migration path toward CDD/ODX/PDX later

It should remain below `00~07` in authority:
- `00~07` = program/canonical SoT
- Basic Diagnostic Description = execution-side derived contract

## Recommended Ownership

- Docs team:
  - keep `00~07` as canonical SoT
- Dev1:
  - create and maintain the Basic Diagnostic Description in `canoe/docs/operations/verification/`
  - wire testcase oracle/asserts from it
- Dev2:
  - freeze pipeline aggregation keys from it and from `Diag::*`

## Immediate Next Step

Create a compact table-driven Basic Diagnostic Description for the currently implemented diagnostic responders first, then expand if needed.

# Runtime Skeleton

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document describes the planned runtime skeleton of the active CANoe baseline.

## Scope

- input surface
- runtime layers
- transport seams
- test-harness placement
- evidence handoff points

## Target Structure

1. Surface layer
- panel and system-variable inputs under `project/panel/` and `project/sysvars/`
- scenario control inputs for SIL execution

2. Runtime layer
- CAPL source of truth under `src/capl/`
- GUI import mirror under `cfg/channel_assign/`
- domain logic that normalizes inputs and computes alert state

3. Contract layer
- domain CAN contracts from the active DBC set
- Ethernet backbone seams for cross-domain delivery and health signaling
- stable panel and diagnostic observation seams

4. Verification layer
- scenario orchestration via `TEST_SCN`
- baseline aggregation via `TEST_BAS`
- native CANoe Test Unit assets for UT and IT proof
- evidence capture through verdict, log, report, and screenshot outputs

## Runtime Blocks

| Block | Role | Main assets |
| --- | --- | --- |
| Input capture | ingest panel, sysvar, domain CAN, and Ethernet context | `project/panel/`, `project/sysvars/`, CAPL input handlers |
| Normalization | convert raw signals into stable runtime state | `src/capl/logic/`, domain ECU logic |
| Boundary authority | apply cross-domain ownership, route, timeout, and health rules | `CGW`, boundary-state logic, route contract |
| Alert decision | compute selected alert, clear, and fail-safe outcome | core alert logic, arbitration logic |
| Output publish | emit CAN, Ethernet, and panel-readable status | domain ECU publishers, Ethernet helpers, SysVar mirrors |
| Verification harness | drive scenarios, aggregate verdict, and prepare evidence seams | `TEST_SCN`, `TEST_BAS`, native Test Unit assets |

## Design Rules

- keep business semantics separate from transport
- keep `src/capl/` as the source of truth and `cfg/channel_assign/` as the GUI mirror
- keep reviewer-facing seams readable through stable contracts and SysVars
- keep harness logic explicit instead of hiding verdict logic inside transport handlers

## Current Development Note

The skeleton above is the target operating shape for the current CANoe baseline.
If a specific ECU path or test harness asset is still under implementation, treat the documented structure as the expected integration direction rather than a guarantee of final implementation detail.
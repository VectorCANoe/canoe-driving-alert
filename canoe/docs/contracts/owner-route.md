# Owner / Bus / Timeout / Route Contract

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines who owns each major runtime seam and which bus, timeout authority, and route authority apply.

## Contract Dimensions

| Dimension | Meaning |
| --- | --- |
| Owner | the runtime authority that owns the business meaning of the seam |
| Bus | the primary transport or observation seam used for the active baseline |
| Timeout authority | the runtime authority that decides stale-state, clear, or fail-safe behavior |
| Route authority | the runtime authority that controls cross-domain delivery and forwarding |

## Rules

- one logical seam must have one explicit owner
- owner and route authority may be different when cross-domain forwarding is involved
- timeout and clear behavior must be explicit, not inferred from transport alone
- layer and observer separation follows `contracts/layer-separation-policy.md`
- foreign-domain CAN visibility follows `contracts/multibus-policy.md`
- detailed frame-level ownership stays in `contracts/communication-matrix.md`

## Current Seam Table

| Seam | Owner | Primary bus | Timeout authority | Route authority | Notes |
| --- | --- | --- | --- | --- | --- |
| Navigation context | `IVI` | Infotainment CAN | `IVI` | `CGW` when cross-domain delivery is required | road zone, direction, distance, speed-limit context |
| Emergency context | `V2X` | Ethernet backbone + normalized `Core/CoreState` seam | `CGW` boundary authority | `CGW` | emergency source, direction, ETA, active/clear context |
| Arbitration decision | `ADAS` | local runtime + `CoreState::selectedAlertDecision*` seam | `ADAS` | `CGW` for cross-domain forwarding | selected alert level/type before gateway boundary or fail-safe shaping |
| Arbitration effective result | `CGW` | `CoreState::selectedAlertEffective*` seam + published output seam | `CGW` | `CGW` | selected alert level/type after boundary, timeout-clear, and fail-safe shaping |
| Decel decision | `ADAS` | local runtime + `@Core::decelAssistDecisionReq` + `CoreState::driverReleaseReason` | `ADAS` | `CGW` for cross-domain forwarding | driver intervention is reflected here before boundary/fail-safe effective gating |
| Decel effective result | `CGW` | `@Core::decelAssistReq` + `CoreState::decelGateReason` | `CGW` | `CGW` | fail-safe effective request and final gate reason |
| Render warning state | `IVI`, `CLU`, `HUD`, `AMP` | local render output + `CoreState::selectedAlertEffective*` consumer seam | each render owner | none | render owners consume `effective -> decision -> compatibility fallback` in that order and do not become ingress or gateway owners |
| Body ambient / hazard output | `BCM` | body output + `CoreState::selectedAlertEffective*` consumer seam | `BCM` | none | body warning actuation consumes `effective -> decision -> compatibility fallback` plus local body policy |
| Boundary health | `CGW` | Ethernet backbone | `CGW` | `CGW` | fail-safe and cross-domain health summary |
| Scenario result | `TEST_SCN` | test harness seam | `TEST_SCN` | none | per-scenario verdict and trace anchor |
| Baseline result | `TEST_BAS` | SysVar-only seam | `TEST_BAS` | none | aggregate baseline verdict and health summary |

## Usage Rule

Use this document for seam-level authority decisions.
Use `contracts/layer-separation-policy.md` first when the question is whether a seam is transport, decision, boundary, render, observer, or diagnostic semantic.
Use `contracts/communication-matrix.md` when the question is frame-level ownership.

## Development Note

The seam table above is the current planned contract for the active baseline.
If a seam changes transport or ownership during development, update this document before treating the change as official.

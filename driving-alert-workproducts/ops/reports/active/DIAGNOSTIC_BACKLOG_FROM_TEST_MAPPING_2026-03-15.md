# Diagnostic Backlog from Test Mapping

> [!IMPORTANT]
> This document is the current diagnostic backlog extracted from the active test mapping.
> It includes only the items that currently require diagnostic visibility for a strong official PASS/FAIL decision.
> It does not mean the diagnostic assets already exist.

## 1. Purpose

This backlog separates the current `Diagnostic Needed? = Yes` items from the `05`, `06`, and `07` mapping draft.

Use this document to decide:

- which verification items truly require diagnostic depth now
- which verdicts remain weak without explicit diagnostic state visibility
- which future diagnostic matrix rows must be implemented first

## 2. Current `Yes` scope

The current project keeps `Yes` intentionally narrow.

Use `Yes` only when:

- the verdict depends on diagnostic or security state itself
- visible behavior, trace, sysvar, and native report are not enough to make the official verdict strong

Boundary, fail-safe, timeout, and restore scenarios are currently judged on the normal oracle/evidence path unless diagnostic state itself is part of the verdict.

## 3. Active diagnostic backlog

| Source ID | Candidate native asset | Why diagnostic is needed now | Required diagnostic focus |
|---|---|---|---|
| `UT_063` | `TEST_SCN SGW security preset` | security-related state injection cannot stay as a strong official verdict without explicit security-state interpretation | security-state explanation, gateway ownership, route-control impact |
| `UT_064` | `TEST_SCN DCM diagnostic preset` | diagnostic-state injection alone is not enough once real diagnostic flows are introduced into the verdict chain | diagnostic-state reason, later SID/DID linkage, tester interpretation basis |
| `IT_027` | `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG` | service, security, and diagnostic state interaction is too weak if judged only by visible output and trace | service-state cause, route ownership, diagnostic-state explanation |
| `ST_038` | `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT` | the system-level verdict directly depends on service, security, and diagnostic context rather than only user-visible behavior | diagnostic-state cause, route ownership, security/service reason |

## 4. Recommended implementation order

1. diagnostic-state injection basis
   - `UT_063`
   - `UT_064`

2. integrated runtime/service/security verdict
   - `IT_027`

3. system-level diagnostic-context verdict
   - `ST_038`

## 5. Recommended future matrix fields

The first diagnostic matrix built from this backlog should include:

- `ECU`
- `ReqFrame`
- `RespFrame`
- `SID`
- `DID/DTC`
- `PositiveResp`
- `NegativeResp`
- `Timeout`
- `SourceBus`
- `TargetBus`
- `CoverageTier`

Later, expand with:

- `session control`
- `security access`
- `NRC policy`
- `gateway route ownership`
- `ECU DID catalog`
- `ODX/CDD-based tester interpretation`

## 6. Current decision

At the current project stage:

- keep the diagnostic backlog intentionally small
- judge non-diagnostic scenarios on the normal oracle/evidence path
- add diagnostic depth only where the official verdict actually depends on diagnostic or security state

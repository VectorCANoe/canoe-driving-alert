# Diagnostic Coverage

> [!IMPORTANT]
> This document is the current development baseline for diagnostic-linked verification in CANoe SIL.
> It may change as diagnostic seams, tester behavior, and service-state contracts are finalized.

## 1. Purpose

This document defines the current official diagnostic verification scope.

It intentionally stays narrow.

At the current project stage, diagnostic depth is required only where the official verdict depends on:

- security state
- diagnostic state
- service state that cannot be explained strongly by normal runtime evidence alone

All other test items remain on the normal oracle and evidence path.

## 2. Current coverage rule

Use diagnostic-linked verification only when both conditions are true:

1. visible behavior, trace, sysvar, and native report are not enough for a strong verdict
2. the verdict directly depends on diagnostic or security context

Do not expand diagnostic scope for:

- normal HMI output verification
- ordinary timeout clear verification
- fail-safe entry or recovery that is already judged by the current oracle/evidence path
- transport observation that is already visible in trace

## 3. Current official diagnostic scope

| Source ID | Candidate native asset | Why diagnostic coverage is required now | Required coverage focus |
|---|---|---|---|
| `UT_063` | `TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE` | security-related state injection cannot remain a strong official verdict without explicit security-state interpretation | security-state explanation, gateway ownership, route-control impact |
| `UT_064` | `TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE` | diagnostic-state injection alone is not enough once real diagnostic flows are introduced into the verdict chain | diagnostic-state reason, request/response summary basis, tester interpretation basis |
| `IT_040` | `TC_CANOE_IT_EXT_040_SERVICE_SECURITY_DIAG` | service, security, and diagnostic state interaction is too weak if judged only by visible output and trace | service-state cause, route ownership, external diagnostic summary |
| `ST_043` | `TC_CANOE_ST_EXT_043_SERVICE_SECURITY_DIAG_CONTEXT` | the system-level verdict directly depends on service, security, and diagnostic context rather than only user-visible behavior | diagnostic-state cause, route ownership, external diagnostic summary |

## 4. Recommended implementation order

1. diagnostic-state injection basis
   - `UT_063`
   - `UT_064`

2. integrated runtime and service-state verdict
   - `IT_040`

3. system-level diagnostic-context verdict
   - `ST_043`

## 5. Minimum matrix fields

The first diagnostic matrix built for this project should include:

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

## 6. Later expansion

Expand only after the current official coverage is stable.

Possible later fields are:

- `session control`
- `security access`
- `NRC policy`
- `gateway route ownership`
- `ECU DID catalog`
- `ODX/CDD-based tester interpretation`

These are future deepening fields, not current entry criteria.

## 7. Relationship to other verification documents

Use this document together with:

- `test-asset-mapping.md`
- `oracle.md`
- `execution-guide.md`
- `acceptance-criteria.md`
- `evidence-policy.md`
- `../contracts/diagnostic-matrix.md`

## Current executable diagnostic baseline (2026-03-15)

- `UT_063`: `TEST_SCN` scenario `203` drives SGW diagnostic context and validates `Diag::SecurityState` plus `Diag::RouteOwner`.
- `UT_064`: `TEST_SCN` scenario `204` drives DCM diagnostic context and validates request/response summary fields including `LastRequest*`, `LastResponse*`, `ResponseKind`, and `ReasonCode`.
- `IT_040`: `TEST_SCN` scenario `205` validates the integrated SGW/DCM seam for service, security, route, and external diagnostic request/response context.
- `ST_043`: `TEST_SCN` scenario `202` validates nominal -> degraded -> blocked progression, final blocked diagnostic context, and external diagnostic request/response summary.
- Current status is `producer wiring complete / compile and runtime evidence pending` for all four items.

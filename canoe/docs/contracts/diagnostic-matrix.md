# Diagnostic Matrix

> [!IMPORTANT]
> This document is the current development baseline for the diagnostic contract matrix in CANoe SIL.
> It may change as diagnostic seams, tester behavior, and service-state contracts are finalized.

## 1. Purpose

This document defines the minimum official diagnostic matrix for the current project baseline.

The matrix is intentionally small.

It covers only the diagnostic-linked verification items that are currently required for a strong official verdict.

## 2. Minimum matrix fields

The current minimum matrix fields are:

1. `ECU`
2. `ReqFrame`
3. `RespFrame`
4. `SID`
5. `DID/DTC`
6. `PositiveResp`
7. `NegativeResp`
8. `Timeout`
9. `SourceBus`
10. `TargetBus`
11. `CoverageTier`

These fields are enough to establish:

- who owns the diagnostic interaction
- what request and response path is observed
- whether the current verdict expects positive, negative, or timeout behavior
- what bus boundary is involved
- how deep the current coverage needs to go

## 3. Current official matrix

| Source ID | ECU | ReqFrame | RespFrame | SID | DID/DTC | PositiveResp | NegativeResp | Timeout | SourceBus | TargetBus | CoverageTier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `UT_063` | `SGW` | `TBD_DIAG_REQ_SGW_SECURITY` | `TBD_DIAG_RESP_SGW_SECURITY` | `TBD` | `TBD` | `Y` | `Y` | `Y` | `ETH_Backbone` | `ETH_Backbone` | `Tier-1 Security State` |
| `UT_064` | `DCM` | `TBD_DIAG_REQ_DCM_STATE` | `TBD_DIAG_RESP_DCM_STATE` | `TBD` | `TBD` | `Y` | `Y` | `Y` | `ETH_Backbone` | `ETH_Backbone` | `Tier-1 Diagnostic State` |
| `IT_027` | `SGW + DCM + runtime owner` | `TBD_DIAG_REQ_SERVICE_SECURITY` | `TBD_DIAG_RESP_SERVICE_SECURITY` | `TBD` | `TBD` | `Y` | `Y` | `Y` | `ETH_Backbone` | `ETH_Backbone` | `Tier-2 Integrated Runtime State` |
| `ST_038` | `system-level diagnostic context` | `TBD_DIAG_REQ_SYSTEM_CONTEXT` | `TBD_DIAG_RESP_SYSTEM_CONTEXT` | `TBD` | `TBD` | `Y` | `Y` | `Y` | `ETH_Backbone` | `ETH_Backbone` | `Tier-3 System Verdict Context` |

## 4. Field interpretation rule

1. `ReqFrame` and `RespFrame` may stay `TBD_*` until the exact runtime path is fixed.
2. `SID` and `DID/DTC` may stay `TBD` until the first concrete tester flow is approved.
3. `PositiveResp`, `NegativeResp`, and `Timeout` show whether the verdict must distinguish that response class.
4. `CoverageTier` expresses how deep the diagnostic explanation must go.

Recommended tier meaning:

- `Tier-1`
  - single ECU or single state interpretation
- `Tier-2`
  - integrated runtime and ownership interpretation
- `Tier-3`
  - system-level verdict explanation

## 5. Future deepening fields

After the minimum matrix is stable, the following fields may be added:

1. `session control`
2. `security access`
3. `NRC policy`
4. `gateway route ownership`
5. `ECU DID catalog`
6. `ODX/CDD-based tester interpretation`

These are not current entry criteria.

They are later deepening fields.

## 6. Relationship to other documents

Use this document together with:

- `diagnostic-description.md`
- `diagnostic-sysvar-contract.md`
- `../verification/diagnostic-coverage.md`
- `../verification/diagnostic-seam-design.md`

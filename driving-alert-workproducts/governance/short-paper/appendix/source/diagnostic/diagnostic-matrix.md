# Diagnostic Matrix

원문:
- [../../contracts/diagnostic-matrix.md](../../contracts/diagnostic-matrix.md)

동기화 기준:
- `5d83ee7f`
- request/response frame 이름, SID, DID/DTC, coverage tier 이름은 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 CANoe SIL baseline에서 공식 verdict를 설명하기 위해 필요한 최소 diagnostic matrix를 정의합니다.
> diagnostic seam, tester flow, service-state contract가 고정되기 전까지 일부 항목은 변경될 수 있습니다.

## 1. 목적

이 문서는 현재 프로젝트 baseline에서 반드시 유지해야 하는 최소 diagnostic matrix를 정의합니다.

이 matrix는 의도적으로 작게 유지합니다.

대상은 현재 official verdict를 강하게 설명하기 위해 diagnostic 근거가 꼭 필요한 항목만입니다.

## 2. 최소 matrix 필드

현재 minimum matrix 필드는 다음과 같습니다.

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

이 필드만으로도 다음을 설명할 수 있습니다.

- diagnostic interaction의 owner가 누구인지
- request/response path를 어디에서 관찰하는지
- 현재 verdict가 positive, negative, timeout을 구분해야 하는지
- 어떤 bus boundary가 개입되는지
- 현재 diagnostic 설명 깊이가 어느 tier까지 필요한지

## 3. 현재 공식 matrix

### 3.1 Route and identity

| Test ID | ECU 범위 |
|---|---|
| `UT_063` | `SGW` |
| `UT_064` | `DCM` |
| `IT_040` | `SGW + DCM + runtime owner` |
| `ST_043` | system-level diagnostic context |

| Test ID | Request Frame |
|---|---|
| `UT_063` | `TBD_DIAG_REQ_SGW_SECURITY` |
| `UT_064` | `TBD_DIAG_REQ_DCM_STATE` |
| `IT_040` | `TBD_DIAG_REQ_SERVICE_SECURITY` |
| `ST_043` | `TBD_DIAG_REQ_SYSTEM_CONTEXT` |

| Test ID | Response Frame |
|---|---|
| `UT_063` | `TBD_DIAG_RESP_SGW_SECURITY` |
| `UT_064` | `TBD_DIAG_RESP_DCM_STATE` |
| `IT_040` | `TBD_DIAG_RESP_SERVICE_SECURITY` |
| `ST_043` | `TBD_DIAG_RESP_SYSTEM_CONTEXT` |

| Test ID | SID / DID-DTC | Coverage Tier |
|---|---|---|
| `UT_063` | `TBD / TBD` | `Tier-1 Security State` |
| `UT_064` | `TBD / TBD` | `Tier-1 Diagnostic State` |
| `IT_040` | `TBD / TBD` | `Tier-2 Integrated Runtime State` |
| `ST_043` | `TBD / TBD` | `Tier-3 System Verdict Context` |

### 3.2 Response coverage

| Test ID | Response Class | Bus Path |
|---|---|---|
| `UT_063` | `Pos / Neg / Timeout` | `ETH_Backbone` |
| `UT_064` | `Pos / Neg / Timeout` | `ETH_Backbone` |
| `IT_040` | `Pos / Neg / Timeout` | `ETH_Backbone` |
| `ST_043` | `Pos / Neg / Timeout` | `ETH_Backbone` |

## 4. 필드 해석 규칙

1. `ReqFrame`과 `RespFrame`은 정확한 runtime path가 고정되기 전까지 `TBD_*` 상태로 둘 수 있습니다.
2. `SID`와 `DID/DTC`는 첫 concrete tester flow가 승인되기 전까지 `TBD` 상태로 둘 수 있습니다.
3. `PositiveResp`, `NegativeResp`, `Timeout`은 verdict가 해당 response class를 구분해야 하는지를 나타냅니다.
4. `CoverageTier`는 diagnostic 설명이 어느 수준까지 내려가야 하는지를 표현합니다.

권장 tier 의미는 다음과 같습니다.

- `Tier-1`
  - 단일 ECU 또는 단일 state 해석 수준
- `Tier-2`
  - integrated runtime과 ownership 해석 수준
- `Tier-3`
  - system-level verdict explanation 수준

## 5. 향후 심화 필드

minimum matrix가 안정화된 뒤에는 다음 필드를 추가할 수 있습니다.

1. `session control`
2. `security access`
3. `NRC policy`
4. `gateway route ownership`
5. `ECU DID catalog`
6. `ODX/CDD-based tester interpretation`

이 항목들은 현재 entry criteria는 아닙니다.

추후 diagnostic 심화 단계에서만 추가합니다.

## 6. 관련 문서

이 문서는 다음 문서와 함께 사용합니다.

- `diagnostic-description.md`
- `diagnostic-sysvar-contract.md`
- `../verification/diagnostic-coverage.md`
- `../verification/diagnostic-seam-design.md`

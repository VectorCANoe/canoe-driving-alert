# Diagnostic Coverage

원문:
- [../../verification/diagnostic-coverage.md](../../verification/diagnostic-coverage.md)

동기화 기준:
- `5d83ee7f`
- native asset 이름과 diagnostic-linked source ID는 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 CANoe SIL baseline에서 diagnostic-linked verification이 실제로 필요한 범위를 정의합니다.
> diagnostic seam, tester behavior, service-state contract가 바뀌면 coverage 범위도 함께 조정될 수 있습니다.

## 1. 목적

이 문서는 현재 official verdict에서 diagnostic verification이 필요한 범위를 정의합니다.

범위는 의도적으로 좁게 유지합니다.

현재 프로젝트 단계에서 diagnostic depth가 필요한 경우는 다음과 같습니다.

- security state가 verdict의 직접 근거인 경우
- diagnostic state가 verdict의 직접 근거인 경우
- normal runtime evidence만으로는 service state를 강하게 설명할 수 없는 경우

이 외 항목은 normal oracle과 evidence path로 판단합니다.

## 2. 현재 coverage 규칙

diagnostic-linked verification은 다음 두 조건이 모두 참일 때만 사용합니다.

1. visible behavior, trace, sysvar, native report만으로는 strong verdict가 부족할 때
2. verdict가 diagnostic 또는 security context에 직접 의존할 때

다음 항목에는 diagnostic scope를 불필요하게 확장하지 않습니다.

- 일반 HMI output verification
- ordinary timeout clear verification
- 현재 oracle/evidence path만으로 판단 가능한 fail-safe entry 또는 recovery
- trace만으로 이미 보이는 transport observation

## 3. 현재 공식 diagnostic scope

| Source ID | Candidate native asset | 현재 diagnostic coverage가 필요한 이유 | 요구 coverage 초점 |
|---|---|---|---|
| `UT_063` | `TC_CANOE_UT_EXT_016_SGW_SECURITY_STATE` | security-related state injection은 explicit security-state interpretation 없이는 strong official verdict가 되기 어렵습니다 | security-state explanation, gateway ownership, route-control impact |
| `UT_064` | `TC_CANOE_UT_EXT_017_DCM_DIAGNOSTIC_STATE` | real diagnostic flow가 verdict chain에 들어오면 diagnostic-state injection만으로는 설명력이 부족합니다 | diagnostic-state reason, SID/DID linkage basis, tester interpretation basis |
| `IT_040` | `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG` | visible output과 trace만으로는 service/security/diagnostic 상호작용을 충분히 설명하기 어렵습니다 | service-state cause, route ownership, diagnostic-state explanation |
| `ST_043` | `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT` | system-level verdict가 user-visible behavior만이 아니라 service/security/diagnostic context에 직접 의존합니다 | diagnostic-state cause, route ownership, security/service reason |

## 4. 권장 구현 순서

1. diagnostic-state injection basis
   - `UT_063`
   - `UT_064`

2. integrated runtime and service-state verdict
   - `IT_040`

3. system-level diagnostic-context verdict
   - `ST_043`

## 5. Minimum matrix fields

이 프로젝트에서 처음 구성하는 diagnostic matrix는 최소한 다음 필드를 포함해야 합니다.

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

## 6. 이후 확장

현재 official coverage가 안정화된 뒤에만 확장합니다.

추후 확장 가능한 필드는 다음과 같습니다.

- `session control`
- `security access`
- `NRC policy`
- `gateway route ownership`
- `ECU DID catalog`
- `ODX/CDD-based tester interpretation`

이 필드들은 future deepening fields이며, 현재 entry criteria는 아닙니다.

## 7. 관련 verification 문서

이 문서는 다음 문서와 함께 사용합니다.

- `test-asset-mapping.md`
- `oracle.md`
- `execution-guide.md`
- `acceptance-criteria.md`
- `evidence-policy.md`
- `../contracts/diagnostic-matrix.md`

## 현재 executable diagnostic baseline (2026-03-15)

- `UT_063`: `TEST_SCN` scenario `203`이 SGW diagnostic context를 구동하고 `Diag::SecurityState`와 `Diag::RouteOwner`를 검증합니다.
- `UT_064`: `TEST_SCN` scenario `204`가 DCM diagnostic context를 구동하고 `LastRequestSid`, `ResponseKind`, `ReasonCode`, `LastResponseCode`, `LastResponseOk`를 검증합니다.
- `IT_040`: `TEST_SCN` scenario `205`가 service/security/route/response context에 대한 integrated SGW/DCM seam을 검증합니다.
- `ST_043`: `TEST_SCN` scenario `202`가 nominal -> degraded -> blocked progression과 최종 blocked diagnostic context를 검증합니다.
- 현재 상태는 네 항목 모두 `producer wiring complete / compile and runtime evidence pending` 입니다.

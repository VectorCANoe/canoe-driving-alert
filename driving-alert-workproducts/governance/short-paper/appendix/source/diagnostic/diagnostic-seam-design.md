# Diagnostic Seam Design

원문:
- [../../verification/diagnostic-seam-design.md](../../verification/diagnostic-seam-design.md)

동기화 기준:
- `5d83ee7f`
- reserved seam 이름과 `Diag::*` identifier는 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 diagnostic-linked verification seam의 최소 설계 기준을 정의합니다.
> CANoe diagnostic hook, sysvar contract, tester interpretation이 고정되면 내용도 함께 조정될 수 있습니다.

## 1. 목적

이 문서는 현재 official diagnostic scope를 위해 필요한 minimum seam design을 정의합니다.

현재 official scope는 의도적으로 좁게 유지되며 다음 항목으로 제한됩니다.

- `UT_063`
- `UT_064`
- `IT_040`
- `ST_043`

이 항목들은 normal oracle/evidence path만으로는 부족하고, diagnostic 또는 security state visibility가 더 강하게 필요합니다.

## 2. 설계 원칙

1. 모든 internal state가 아니라 verdict-critical state만 노출합니다.
2. business semantics와 transport detail을 분리합니다.
3. seam 값은 CANoe native report, sysvar snapshot, write-window evidence에서 읽기 쉬워야 합니다.
4. 가능하면 `UT -> IT -> ST`로 올라가도 같은 seam 의미를 유지합니다.
5. official verdict scope가 바뀌지 않는 한 diagnostic seam을 일반 `No` 항목으로 확장하지 않습니다.

## 3. 최소 seam field

minimum seam set은 다음 질문에 답할 수 있어야 합니다.

- 현재 어떤 security 또는 diagnostic state가 active인지
- 어떤 route owner 또는 gateway owner가 active인지
- 마지막 request/response class가 무엇이었는지
- verdict가 timeout, denial, unavailable service state 때문에 막혔는지

권장 minimum field:

- `diag_state`
- `security_state`
- `service_state`
- `route_owner`
- `last_sid`
- `last_did_or_dtc`
- `response_kind`
- `timeout_flag`
- `source_bus`
- `target_bus`
- `reason_code`

위 이름은 semantic field 이름이며, 최종 implementation identifier를 강제하는 것은 아닙니다.

## 4. 현재 0304-aligned seam candidate

현재 system-variable baseline은 `0304_System_Variables.md`와 `Diag::*`를 통해 필요한 seam의 일부를 이미 노출하고 있습니다.

먼저 다음 기존 variable을 우선 활용합니다.

- fail-safe state
  - `Core::failSafeMode`
- path health
  - `CoreState::warningPathStatus`
  - `CoreState::e2eHealthState`
- route and boundary condition
  - `Powertrain::RoutingPolicy`
  - `Powertrain::BoundaryStatus`
  - `Body::BodyGwHealth`
- diagnostic request identity
  - `Diag::LastRequestTarget`
  - `Diag::LastRequestSid`
  - `Diag::LastRequestDidHigh`
  - `Diag::LastRequestDidLow`
  - `Diag::LastRequestSourceBus`
  - `Diag::RequestCounter`
  - `Diag::LastRequestTimeMs`
- diagnostic response identity
  - `Diag::LastResponseTarget`
  - `Diag::LastResponseCode`
  - `Diag::LastResponseData0`
  - `Diag::LastResponseData1`
  - `Diag::LastResponseOk`
  - `Diag::LastResponseSourceBus`
  - `Diag::ResponseCounter`
  - `Diag::LastResponseTimeMs`
- ECU-local diagnostic state hint
  - `Chassis::ChassisDiagState`
  - `Body::BodyDiagState`
  - `Infotainment::InfoDiagState`
  - `Powertrain::PtDiagState`
- ECU-local diagnostic request/response hint
  - `Chassis::ChsDiagServiceId`, `Chassis::ChsDiagRespCode`
  - `Body::BcmDiagServiceId`, `Body::BcmDiagRespCode`
  - `Infotainment::IviDiagServiceId`, `Infotainment::IviDiagRespCode`
  - `Powertrain::PtDiagServiceId`, `Powertrain::PtDiagRespCode`

이 변수들만으로도 skeleton wiring과 evidence capture는 시작할 수 있습니다.

다만 모든 official diagnostic verdict를 깔끔하게 설명하기에는 아직 부족합니다.

## 5. 현재 reserved seam addition

다음 semantic field는 verification용 `Diag::*` 아래에 reserved seam으로 유지합니다.

producer wiring은 아직 진행 중일 수 있습니다.

- `Diag::SecurityState`
  - `UT_063`, `IT_040`, `ST_043`는 indirect interpretation만으로는 부족하고 stable security verdict seam이 필요합니다.
- `Diag::ServiceState`
  - integrated service-context verdict를 mixed runtime side effect만으로 판단하면 설명력이 약합니다.
- `Diag::RouteOwner`
  - 현재 route/boundary health 표면만으로는 ownership explanation이 충분히 강하지 않습니다.
- `Diag::ResponseKind`
  - `Positive / Negative / Timeout / Unavailable`를 verdict-facing 의미로 안정적으로 해석해야 합니다.
- `Diag::ReasonCode`
  - diagnostic-linked decision의 이유를 짧고 안정적으로 설명해야 합니다.

## 6. 남아 있는 meaning-level gap

지금 남은 gap은 variable reservation 자체가 아닙니다.

핵심은 producer-side semantic wiring입니다.

- semantic producer wiring
  - runtime 또는 harness logic이 reserved seam을 일관되게 써줘야 합니다.
- stable enum meaning
  - `UT`, `IT`, `ST` 전 구간에서 seam 값의 해석이 동일해야 합니다.
- trace correlation rule
  - seam update가 `Diag::*` request/response mirror와 write-window evidence와 연동돼야 합니다.

## 7. Baseline enum contract

`UT`부터 `ST`까지 one stable numeric interpretation을 사용합니다.

| Seam | Value | Meaning |
|---|---:|---|
| `Diag::SecurityState` | `0` | unavailable or inactive |
| `Diag::SecurityState` | `1` | session open or degraded security context |
| `Diag::SecurityState` | `2` | authorized and route-usable |
| `Diag::SecurityState` | `3` | denied, faulted, or fail-safe-blocked |
| `Diag::ServiceState` | `0` | unavailable |
| `Diag::ServiceState` | `1` | degraded |
| `Diag::ServiceState` | `2` | available |
| `Diag::RouteOwner` | `0` | none or unknown |
| `Diag::RouteOwner` | `1` | `SGW` |
| `Diag::RouteOwner` | `2` | `DCM` |
| `Diag::RouteOwner` | `3` | integrated warning path |
| `Diag::ResponseKind` | `0` | none |
| `Diag::ResponseKind` | `1` | positive |
| `Diag::ResponseKind` | `2` | negative |
| `Diag::ResponseKind` | `3` | timeout |
| `Diag::ResponseKind` | `4` | unavailable or denied |
| `Diag::ReasonCode` | `0` | none |
| `Diag::ReasonCode` | `1` | boundary down |
| `Diag::ReasonCode` | `2` | fail-safe active |
| `Diag::ReasonCode` | `3` | service degraded |
| `Diag::ReasonCode` | `4` | policy denied |
| `Diag::ReasonCode` | `5` | response timeout |
| `Diag::ReasonCode` | `6` | route mismatch |

## 8. 현재 official scope별 seam design

### `UT_063`

- seam question
  - security preset이 의도한 security state와 ownership context로 해석됐는가
- minimum required fields
  - current: `Powertrain::RoutingPolicy`, `Body::BodyGwHealth`
  - reserved: `Diag::SecurityState`, `Diag::RouteOwner`, `Diag::ReasonCode`
- primary evidence path
  - write window + trace + sysvar snapshot

### `UT_064`

- seam question
  - diagnostic preset이 의도한 diagnostic state와 request class로 해석됐는가
- minimum required fields
  - current: `Diag::LastRequestSid`, `Diag::LastResponseCode`, `Diag::LastResponseOk`
  - reserved: ECU-local diag state + `Diag::ResponseKind`, `Diag::ReasonCode`
- primary evidence path
  - write window + trace + sysvar snapshot

### `IT_040`

- seam question
  - integrated service, security, diagnostic context가 기대한 runtime verdict로 수렴하는가
- minimum required fields
  - current: `Diag::*`, ECU-local `*DiagState`, `Powertrain::RoutingPolicy`
  - reserved: `Diag::ServiceState`, `Diag::SecurityState`, `Diag::RouteOwner`
- primary evidence path
  - native report + trace + write window + sysvar snapshot

### `ST_043`

- seam question
  - system-level service/security/diagnostic context가 최종 scenario verdict를 정당하게 설명하는가
- minimum required fields
  - current: `Diag::*`, ECU-local `*DiagState`, `CoreState::warningPathStatus`
  - reserved: `Diag::ServiceState`, `Diag::SecurityState`, `Diag::RouteOwner`, `Diag::ReasonCode`
- primary evidence path
  - native report + trace + write window + sysvar snapshot

## 9. Planned assertion profile

### `UT_063`

- nominal assert
  - `SecurityState=2`, `RouteOwner=3 or 1`
- degraded or blocked assert
  - degraded: `SecurityState=3`, `RouteOwner=1`
  - blocked: `SecurityState=3`, `RouteOwner=1`
- current blocker
  - executable via `TEST_SCN` scenario `203`

### `UT_064`

- nominal assert
  - `LastRequestSid=0x22`, `ResponseKind=1`, `ReasonCode=0`
- degraded or blocked assert
  - degraded: `ResponseKind=2`, `ReasonCode=3`
  - blocked: `ResponseKind=4`, `ReasonCode=2`
- current blocker
  - executable via `TEST_SCN` scenario `204`

### `IT_040`

- nominal assert
  - `ServiceState=2`, `SecurityState=2`, `RouteOwner=3`, `ResponseKind=1`, `ReasonCode=0`
- degraded or blocked assert
  - degraded: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=3`
  - blocked: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=2`
- current blocker
  - executable via `TEST_SCN` scenario `205`

### `ST_043`

- nominal assert
  - scenario verdict remains explainable with `ServiceState=2`, `SecurityState=2`, `RouteOwner=3`, `ReasonCode=0`
- degraded or blocked assert
  - degraded: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=3`
  - blocked: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=2`
- current blocker
  - executable via `TEST_SCN` scenario `202`

## 10. Publisher ownership baseline

reserved seam은 producer를 하나로 제한합니다.

- `SGW.can`
  - `Diag::SecurityState`
  - `Diag::RouteOwner`
- `DCM.can`
  - `Diag::ServiceState`
  - `Diag::ResponseKind`
  - `Diag::ReasonCode`
  - `Diag::LastRequestSid`
  - `Diag::LastResponseCode`
  - `Diag::LastResponseOk`

## 11. ST_043 scenario stimulus contract

첫 executable `ST_043` scenario는 세 phase만 사용합니다.

1. nominal context
   - boundary healthy
   - fail-safe inactive
   - service available
   - expected seam: `ServiceState=2`, `SecurityState=2`, `RouteOwner=3`, `ReasonCode=0`
2. degraded context
   - emergency refresh intentionally degraded
   - `warningPathStatus=1`, `failSafeMode=1`
   - expected seam: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=3`
3. blocked context
   - explicit fail-safe active
   - expected seam: `ServiceState=1`, `SecurityState=3`, `RouteOwner=1`, `ReasonCode=2`

system-level testcase는 visible behavior와 seam explanation이 세 phase 모두에서 일치할 때만 pass로 봅니다.

## 12. Response interpretation baseline

첫 implementation baseline은 다음 네 종류만 구분합니다.

- positive completion
- negative completion
- timeout
- unavailable service or denied state

`response_kind`에 권장하는 semantic value:

- `Positive`
- `Negative`
- `Timeout`
- `Unavailable`

현재 official coverage가 안정화되기 전에는 full NRC catalog로 확장하지 않습니다.

## 13. 구현 순서

1. `UT_063`
   - `Diag::SecurityState` wiring
   - `Diag::RouteOwner` wiring
2. `UT_064`
   - ECU-local diagnostic state interpretation wiring
   - `Diag::ResponseKind` wiring
3. `IT_040`
   - `Diag::ServiceState` wiring
   - shared ownership interpretation 재사용
4. `ST_043`
   - system-level diagnostic-context verdict seam 연결

## 14. Expansion gate

다음 중 하나가 true가 될 때만 이 seam set을 확장합니다.

1. official verdict가 session 또는 security access stage에 직접 의존할 때
2. reviewer가 SID, DID, DTC, NRC 수준 설명을 요구할 때
3. gateway route ownership이 formal acceptance의 일부가 될 때
4. ODX/CDD-based tester interpretation이 현재 baseline에 필요해질 때

## 15. 관련 verification 문서

이 문서는 다음 문서와 함께 사용합니다.

- `diagnostic-coverage.md`
- `test-asset-mapping.md`
- `oracle.md`
- `diagnostic-sysvar-contract.md`

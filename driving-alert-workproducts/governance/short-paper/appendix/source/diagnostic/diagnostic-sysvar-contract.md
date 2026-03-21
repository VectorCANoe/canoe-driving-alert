# Diagnostic SysVar Contract

원문:
- [../../contracts/diagnostic-sysvar-contract.md](../../contracts/diagnostic-sysvar-contract.md)

동기화 기준:
- `5d83ee7f`
- `Diag::*` 이름과 개별 SysVar 식별자는 canonical technical string으로 유지합니다.

> [!IMPORTANT]
> 이 문서는 `Diag::*` system variable이 diagnostic observation contract로 어떻게 사용되는지를 정의합니다.
> runtime path와 diagnostic seam 구현이 바뀌면 이 문서도 함께 갱신해야 합니다.

## 1. 목적

이 문서는 `Diag::*` namespace로 노출되는 stable diagnostic observation contract를 정의합니다.

목적은 diagnostic request/response evidence를 다음 소비자에게 안정적으로 노출하는 것입니다.

- verification logic
- trace reviewer
- panel 또는 tool observer

단, 제품 runtime을 임시 debug wiring으로 오염시키지 않는 범위에서만 사용합니다.

## 2. 범위

이 계약은 다음 active namespace를 대상으로 합니다.

- `project/sysvars/project.sysvars` 안의 `Diag`

이 문서는 의미와 사용 규칙을 정의하며, 개별 UDS service의 상세 payload를 모두 설명하지는 않습니다.

## 3. Namespace baseline

현재 active diagnostic namespace는 `Diag` 입니다.

여기에는 request mirror, response mirror, counter, timestamp, verdict-facing semantic seam이 포함됩니다.

## 4. Request-side contract

| SysVar | 의미 | 전형적 producer | 전형적 consumer |
|---|---|---|---|
| `Diag::LastRequestTarget` | 가장 최근 diagnostic request의 target ECU 또는 service code | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestSid` | 가장 최근 request의 service identifier | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestDidHigh` | 가장 최근 request의 DID high byte | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestDidLow` | 가장 최근 request의 DID low byte | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestSourceBus` | request가 발생한 source bus code | diagnostic tester / harness path | verification and evidence tools |
| `Diag::RequestCounter` | 누적 request count | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestTimeMs` | 가장 최근 request timestamp(ms) | diagnostic tester / harness path | verification and evidence tools |

## 5. Response-side contract

| SysVar | 의미 | 전형적 producer | 전형적 consumer |
|---|---|---|---|
| `Diag::LastResponseTarget` | 가장 최근 diagnostic response의 target ECU 또는 service code | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseCode` | 가장 최근 response의 response code | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseData0` | evidence 요약용 첫 번째 response payload byte | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseData1` | evidence 요약용 두 번째 response payload byte | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseOk` | 가장 최근 response의 positive/negative flag | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseSourceBus` | response가 발생한 source bus code | diagnostic response handler | verification and evidence tools |
| `Diag::ResponseCounter` | 누적 response count | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseTimeMs` | 가장 최근 response timestamp(ms) | diagnostic response handler | verification and evidence tools |

## 6. Verdict-facing seam contract

| SysVar | 의미 | 전형적 producer | 전형적 consumer |
|---|---|---|---|
| `Diag::SecurityState` | verification용 현재 security interpretation | diagnostic/security seam producer | verification and evidence tools |
| `Diag::ServiceState` | verification용 현재 service availability interpretation | diagnostic/service seam producer | verification and evidence tools |
| `Diag::RouteOwner` | 가장 최근 diagnostic-linked verdict의 active route ownership interpretation | gateway/runtime diagnostic seam producer | verification and evidence tools |
| `Diag::ResponseKind` | 가장 최근 diagnostic-linked verdict의 semantic response class | diagnostic response handler | verification and evidence tools |
| `Diag::ReasonCode` | diagnostic-linked decision의 compact verdict-facing reason code | diagnostic/service/security seam producer | verification and evidence tools |

이 변수들은 verdict 설명을 위한 semantic seam입니다.

이 변수들만으로 full transport trace나 full tester payload review를 대체할 수는 없습니다.

## 7. 계약 규칙

### 7.1 `Diag::*`는 observation contract입니다

`Diag::*`는 diagnostic runtime에서 실제로 발생한 내용을 관찰 가능하게 만드는 mirror입니다.

diagnostic 의미를 `Diag::*` 안에만 고정해두면 안 됩니다.

제품 동작 자체는 여전히 실제 diagnostic runtime path에서 구현되어야 합니다.

### 7.2 Counter는 누적값입니다

`RequestCounter`와 `ResponseCounter`는 active session/runtime scope의 cumulative mirror입니다.

boolean flag처럼 재사용하면 안 됩니다.

### 7.3 Timestamp 단위는 ms입니다

`LastRequestTimeMs`와 `LastResponseTimeMs`는 millisecond timestamp입니다.

tooling과 evidence review 전반에서 이 단위를 유지해야 합니다.

### 7.4 Bus code 해석은 일관돼야 합니다

`LastRequestSourceBus`와 `LastResponseSourceBus`는 producer와 consumer가 같은 code mapping을 공유할 때만 유효합니다.

bus-code enum이 바뀌면 관련 runtime/test helper와 이 문서를 함께 갱신해야 합니다.

### 7.5 Response summary field는 evidence 보조용입니다

`LastResponseData0`와 `LastResponseData1`은 summary mirror입니다.

빠른 evidence 확인이나 smoke validation에는 유용하지만, deeper analysis가 필요할 때 full diagnostic payload trace를 대체하지는 못합니다.

### 7.6 Verdict-facing seam은 semantic seam입니다

`SecurityState`, `ServiceState`, `RouteOwner`, `ResponseKind`, `ReasonCode`는 official verdict를 reviewer-facing 관점에서 읽기 쉽게 만들기 위한 seam입니다.

구현 세부값을 무제한으로 덤프하는 표면으로 쓰면 안 됩니다.

작고 안정적인 semantic vocabulary를 유지하는 것이 원칙입니다.

## 8. Verification 사용 방식

`Diag::*`는 다음 용도로 사용합니다.

- request 송신 여부 smoke 확인
- response 수신 여부 smoke 확인
- positive / negative / timeout expectation에 대한 pass/fail gating
- trace, write-window, evidence 간 correlation
- 현재 official diagnostic scope에 대한 verdict-facing explanation

full transport trace가 필요한 상황에서는 `Diag::*`만을 유일한 증거로 사용하면 안 됩니다.

## 9. 갱신 규칙

diagnostic runtime path가 바뀌면 다음 순서로 갱신합니다.

1. `Diag::*` producer/consumer logic 갱신
2. variable surface가 바뀌면 `project/sysvars/project.sysvars` 갱신
3. 이 contract 문서 갱신
4. 변경된 evidence semantics를 사용하는 verification 문서 갱신

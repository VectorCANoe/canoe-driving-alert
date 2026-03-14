# Diagnostic SysVar Contract

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## 1. Purpose

This document defines the stable diagnostic observation contract exposed through `Diag::*` system variables.

The goal is to keep diagnostic request/response evidence visible to:

- validation logic
- trace reviewers
- panel or tool observers

without turning product runtime code into ad-hoc debug wiring.

## 2. Scope

This contract covers the active `Diag` namespace in:

- `project/sysvars/project.sysvars`

This document defines meaning and usage rules, not service-specific UDS content.

## 3. Namespace baseline

The active diagnostic namespace is:

- `Diag`

It contains request mirrors, response mirrors, counters, and timestamps.

## 4. Request-side contract

| SysVar | Meaning | Typical producer | Typical consumer |
|---|---|---|---|
| `Diag::LastRequestTarget` | target ECU or service code of the most recent diagnostic request | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestSid` | service identifier of the most recent request | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestDidHigh` | DID high byte for the most recent request | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestDidLow` | DID low byte for the most recent request | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestSourceBus` | source bus code used for the request | diagnostic tester / harness path | verification and evidence tools |
| `Diag::RequestCounter` | monotonic request count | diagnostic tester / harness path | verification and evidence tools |
| `Diag::LastRequestTimeMs` | most recent request timestamp in ms | diagnostic tester / harness path | verification and evidence tools |

## 5. Response-side contract

| SysVar | Meaning | Typical producer | Typical consumer |
|---|---|---|---|
| `Diag::LastResponseTarget` | target ECU or service code of the most recent response | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseCode` | response code of the most recent response | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseData0` | first response payload byte for summary observation | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseData1` | second response payload byte for summary observation | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseOk` | positive/negative result flag for the latest response | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseSourceBus` | source bus code used for the response | diagnostic response handler | verification and evidence tools |
| `Diag::ResponseCounter` | monotonic response count | diagnostic response handler | verification and evidence tools |
| `Diag::LastResponseTimeMs` | most recent response timestamp in ms | diagnostic response handler | verification and evidence tools |

## 6. Contract rules

### 6.1 `Diag::*` is an observation contract

`Diag::*` exists to mirror what happened.

It must not become the only place where diagnostic meaning lives.

Product behavior should still be implemented through the actual diagnostic runtime path.

### 6.2 Counters are cumulative

`RequestCounter` and `ResponseCounter` are cumulative mirrors for the active session/runtime scope.

Do not reuse them as boolean flags.

### 6.3 Timestamps are in milliseconds

`LastRequestTimeMs` and `LastResponseTimeMs` are millisecond timestamps.

Keep this unit stable across tooling and evidence review.

### 6.4 Bus-code interpretation must stay consistent

`LastRequestSourceBus` and `LastResponseSourceBus` are valid only if all producers and consumers use the same code mapping.

If the bus-code enum changes, update this document and the matching runtime/test helpers together.

### 6.5 Response summary fields are for evidence, not full payload transport

`LastResponseData0` and `LastResponseData1` are summary mirrors.

They are useful for quick evidence and smoke validation, but they do not replace a full diagnostic payload trace when deeper analysis is required.

## 7. Verification usage

Use `Diag::*` for:

- smoke confirmation that a request was sent
- smoke confirmation that a response returned
- pass/fail gating for positive or negative response expectation
- evidence correlation with trace and write-window logs

Do not use `Diag::*` as the only proof when a full transport trace is required.

## 8. Update rule

If a diagnostic runtime path changes:

1. update the `Diag::*` producer/consumer logic
2. update `project/sysvars/project.sysvars` if the variable surface changes
3. update this contract document
4. update verification documents that depend on the changed evidence semantics

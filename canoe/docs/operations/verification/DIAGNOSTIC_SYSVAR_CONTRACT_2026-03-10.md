# Diagnostic SysVar Contract (Dev1 -> Dev2)

## Purpose

`Diag::*` is the stable verification surface for tester-driven diagnostics.

Dev2 should consume these system variables for pipeline assertions and evidence packaging instead of parsing ECU-specific diagnostic response frames one by one.

## Producer Path

1. `TEST_SCN` sends a diagnostic request frame.
2. `TEST_SCN` mirrors the request into `Diag::*`.
3. Target ECU responds on its local diagnostic response frame.
4. `TEST_SCN` receives the response frame and mirrors the response into `Diag::*`.

This keeps the tester-facing contract stable even if individual ECU req/res message names expand later.

## SysVar Contract

### Request Mirror

| SysVar | Meaning |
| --- | --- |
| `Diag::LastRequestTarget` | Target ECU code |
| `Diag::LastRequestSid` | Service identifier |
| `Diag::LastRequestDidHigh` | DID high byte |
| `Diag::LastRequestDidLow` | DID low byte |
| `Diag::LastRequestSourceBus` | Bus code of the request path |
| `Diag::RequestCounter` | Monotonic request counter |
| `Diag::LastRequestTimeMs` | Request timestamp in ms |

### Response Mirror

| SysVar | Meaning |
| --- | --- |
| `Diag::LastResponseTarget` | Responding ECU code |
| `Diag::LastResponseCode` | Response code (`0x62`, `0x7F`, etc.) |
| `Diag::LastResponseData0` | Response payload byte 0 |
| `Diag::LastResponseData1` | Response payload byte 1 |
| `Diag::LastResponseOk` | `1` for positive response, else `0` |
| `Diag::LastResponseSourceBus` | Bus code of the response path |
| `Diag::ResponseCounter` | Monotonic response counter |
| `Diag::LastResponseTimeMs` | Response timestamp in ms |

## Target Codes

| Code | ECU |
| --- | --- |
| `1` | `IVI` |
| `2` | `CLU` |
| `3` | `ADAS` |
| `4` | `VCU` |
| `5` | `ESC` |
| `6` | `BCM` |
| `7` | `TMU` |
| `8` | `DATC` |
| `9` | `SCC` |
| `10` | `HUD` |
| `11` | `AMP` |
| `12` | `DMS` |
| `13` | `OMS` |
| `14` | `V2X` |
| `15` | `CGW` |
| `16` | `SGW` |
| `17` | `DCM` |
| `18` | `ABS` |
| `19` | `EPB` |
| `20` | `TPMS` |
| `21` | `SAS` |
| `22` | `VSM` |
| `23` | `EHB` |
| `24` | `ECS` |
| `25` | `CDC` |
| `26` | `ACU` |
| `27` | `ODS` |
| `28` | `SMK` |
| `29` | `AFLS` |
| `30` | `WIP` |

## Bus Codes

| Code | Bus |
| --- | --- |
| `1` | `ETH_Backbone` |
| `2` | `Powertrain` |
| `3` | `Chassis` |
| `4` | `Body` |
| `5` | `Infotainment` |
| `6` | `ADAS` |

## Dev2 Consumption Rule

- Primary pass/fail logic for diagnostic smoke tests should read `Diag::*`.
- ECU-specific response frames are still valid as low-level evidence, but they should be treated as supporting artifacts.
- For CI packaging, prefer:
  - target code
  - SID
  - DID high/low
  - response code
  - positive/negative flag
  - request/response timestamps

## Notes

- `TEST_SCN` is the tester-side mirror owner.
- This contract is verification-only and does not change product runtime ownership.

# Diagnostic Tester Coverage 2026-03-10

## Purpose
- Capture the current `TEST_SCN` diagnostic tester coverage for Dev2 automation and CANoe native test expansion.
- Keep the diagnostic path split explicit:
  - `TEST_SCN` = tester / harness
  - local ECU = diagnostic responder
  - `CGW` / `SGW` / `DCM` = backbone diagnostic path services

## Current Tester
- Tester node: `TEST_SCN`
- Trigger path: `sendBaselineDiagRequest(int scenarioId)`
- DID pattern:
  - SID = `0x22`
  - DID high = `0xF1`
  - DID low = `scenarioId`

## Current Request/Response Coverage
| Request | Response | Responder |
|---|---|---|
| `frmIviDiagReqMsg` | `frmIviDiagResMsg` | `IVI` |
| `frmCluDiagReqMsg` | `frmCluDiagResMsg` | `CLU` |
| `frmAdasDiagReqMsg` | `frmAdasDiagResMsg` | `ADAS` |
| `frmPtDiagReqMsg` | `frmPtDiagResMsg` | `VCU` |
| `frmChassisDiagReqMsg` | `frmChassisDiagResMsg` | `ESC` |
| `frmBcmDiagReqMsg` | `frmBcmDiagResMsg` | `BCM` |
| `frmTmuDiagReqMsg` | `frmTmuDiagResMsg` | `TMU` |
| `frmDatcDiagReqMsg` | `frmDatcDiagResMsg` | `DATC` |
| `frmSccDiagReqMsg` | `frmSccDiagResMsg` | `SCC` |
| `frmHudDiagReqMsg` | `frmHudDiagResMsg` | `HUD` |
| `frmAmpDiagReqMsg` | `frmAmpDiagResMsg` | `AMP` |
| `frmDmsDiagReqMsg` | `frmDmsDiagResMsg` | `DMS` |
| `frmOmsDiagReqMsg` | `frmOmsDiagResMsg` | `OMS` |
| `frmAbsDiagReqMsg` | `frmAbsDiagResMsg` | `ABS` |
| `frmEpbDiagReqMsg` | `frmEpbDiagResMsg` | `EPB` |
| `frmTpmsDiagReqMsg` | `frmTpmsDiagResMsg` | `TPMS` |
| `frmSasDiagReqMsg` | `frmSasDiagResMsg` | `SAS` |
| `frmVsmDiagReqMsg` | `frmVsmDiagResMsg` | `VSM` |
| `frmEhbDiagReqMsg` | `frmEhbDiagResMsg` | `EHB` |
| `frmEcsDiagReqMsg` | `frmEcsDiagResMsg` | `ECS` |
| `frmCdcDiagReqMsg` | `frmCdcDiagResMsg` | `CDC` |
| `frmAcuDiagReqMsg` | `frmAcuDiagResMsg` | `ACU` |
| `frmOdsDiagReqMsg` | `frmOdsDiagResMsg` | `ODS` |
| `frmSmkDiagReqMsg` | `frmSmkDiagResMsg` | `SMK` |
| `frmAflsDiagReqMsg` | `frmAflsDiagResMsg` | `AFLS` |
| `frmWipDiagReqMsg` | `frmWipDiagResMsg` | `WIP` |
| `ethV2xDiagReqMsg` | `ethV2xDiagResMsg` | `V2X` |
| `ethCgwDiagReqMsg` | `ethCgwDiagResMsg` | `CGW` |
| `ethSgwDiagReqMsg` | `ethSgwDiagResMsg` | `SGW` |
| `ethDcmDiagReqMsg` | `ethDcmDiagResMsg` | `DCM` |

## Coverage Summary
- Full responder tier: `17`
- Basic responder tier: `13`
- Total tester-driven req/res paths: `30`

## Lightweight Responder Pattern
- Each local ECU stores:
  - pending flag
  - last SID
  - DID high
  - DID low
- The ECU publishes its diagnostic response on its normal cycle timer.
- Response rule:
  - SID `0x22` -> response code `0x62`
  - otherwise -> response code `0x7F`
- DID bytes are echoed in `Data0` / `Data1`

## Scope Notes
- This is not a full UDS/DoIP stack.
- This is an ECU-local SIL responder baseline for:
  - request routing
  - ownership verification
  - Dev2 batch execution
  - Jenkins evidence collection

## Next Expansion
1. Add negative response cases by DID range
2. Add timeout / retry assertions in native CANoe tests
3. Add session-state gating for selected responders

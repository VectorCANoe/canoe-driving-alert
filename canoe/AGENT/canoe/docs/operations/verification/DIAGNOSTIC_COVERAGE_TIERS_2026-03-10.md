# Diagnostic Coverage Tiers 2026-03-10

## Purpose
- Split the current ECU-local diagnostic baseline into `FULL`, `BASIC`, and `DEFERRED` tiers.
- Give Dev2 a stable expectation for tester-driven execution and evidence packaging.

## Tier Definitions
- `FULL`
  - richer responder already aligned with runtime ownership
  - request/response path is part of the current diagnostic baseline
  - suitable for Dev2 automation and native CANoe test expansion
- `BASIC`
  - lightweight ECU-local responder
  - request echoes DID bytes and returns `0x62` for SID `0x22`, otherwise `0x7F`
  - intended to prove ownership, routing, and minimal diagnostic health
- `DEFERRED`
  - no tester-driven request/response path yet
  - keep for later expansion after GUI compile and integration stabilization

## FULL Tier
- `IVI`
- `CLU`
- `ADAS`
- `VCU`
- `ESC`
- `BCM`
- `TMU`
- `DATC`
- `SCC`
- `HUD`
- `AMP`
- `DMS`
- `OMS`
- `V2X`
- `CGW`
- `SGW`
- `DCM`

## BASIC Tier
- `ABS`
- `EPB`
- `TPMS`
- `SAS`
- `VSM`
- `EHB`
- `ECS`
- `CDC`
- `ACU`
- `ODS`
- `SMK`
- `AFLS`
- `WIP`

## DEFERRED Tier
- all other active surface ECUs without tester-driven request/response coverage
- current examples:
  - `EMS`
  - `TCU`
  - `MDPS`
  - `RSPA`
  - `SPAS`
  - `AVM`
  - `FRADAR`
  - `SRR_FL`
  - `SRR_FR`
  - `SRR_RL`
  - `SRR_RR`
  - `PARK_ULTRASONIC`

## Working Rule
- Do not try to make every visible ECU `FULL` tier at once.
- Expand in this order:
  1. active runtime owners used by native CANoe tests
  2. domain-controller and backbone service ECUs
  3. high-value leaf ECUs with user-visible output
  4. remaining placeholder or low-value leaf ECUs

## Dev2 Consumption
- `TEST_SCN` remains the tester node.
- Dev2 may treat:
  - `FULL` as stable diagnostic automation targets
  - `BASIC` as minimal regression coverage targets
  - `DEFERRED` as backlog only

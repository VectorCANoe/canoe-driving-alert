# OEM 4-Layer ECU Classification (2026-03-10)

## Why This Exists

This is not a GUI-first domain rewrite.

Purpose:
1. make the current 100-node bank readable in OEM terms
2. separate central gateway, domain controller, leaf ECU, and validation roles
3. give Dev1 a stable architectural baseline before any further GUI regrouping or SoT rewrite

Meaning:
- current code already shows these layers
- the problem was not lack of structure, but lack of explicit classification
- this document is a reading layer first, not a forced CANoe topology rewrite

## What Changes Now

Nothing in `canoe/cfg/*.cfg` must be changed only because this document exists.

Immediate effect:
- Dev1 uses this classification when deciding runtime ownership
- Docs team can later propagate this model into SoT
- GUI regrouping, if needed, should follow this model instead of inventing a new one

## Layer 1. Central Gateway / Backbone Services

These nodes own the central backbone, security, diagnostic edge, and recording/service plane.

- `CGW`
- `SGW`
- `DCM`
- `IBOX`
- `ETHB`
- `EDR`

## Layer 2. Domain Controller / Primary Runtime Anchors

These are the main domain-facing runtime anchors. They own primary domain state, publish key seam data, and sit above many leaf ECU functions.

- `EMS`
- `TCU`
- `VCU`
- `ESC`
- `MDPS`
- `BCM`
- `DATC`
- `IVI`
- `CLU`
- `TMU`
- `ADAS`
- `SCC`
- `V2X`

## Layer 3. Leaf ECU / Feature ECU / Local Runtime Surfaces

These nodes represent local functions, option features, comfort modules, ADAS leaves, and narrow service surfaces.

### Powertrain / Electrical Leafs
- `_4WD`, `BAT_BMS`, `FPCM`, `LVR`, `ISG`, `EOP`, `EWP`, `OBC`, `DCDC`, `MCU`, `INVERTER`, `CPC`

### Chassis / Safety Leafs
- `ABS`, `EPB`, `TPMS`, `SAS`, `ECS`, `ACU`, `ODS`, `VSM`, `EHB`, `CDC`, `ASM`, `RWS`

### Body / Comfort Leafs
- `SMK`, `AFLS`, `AHLS`, `WIP`, `SRF`, `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`, `TGM`, `SEAT_DRV`, `SEAT_PASS`, `MIR`, `BSEC`, `RATC`, `HLM`, `CSM`, `ADM`, `PTG`, `BIO`, `MSC`

### IVI / HMI / Service Leafs
- `HUD`, `AMP`, `PGS`, `NAV`, `VCS`, `RSE`, `DKEY`, `OTA`, `CPAY`, `PAK`

### ADAS / Parking / Sensor Leafs
- `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `FCAM`, `FRADAR`, `SRR_FL`, `SRR_FR`, `SRR_RL`, `SRR_RR`, `PUS`, `DMS`, `OMS`, `AEB`, `PKM`, `RPC`, `RRM`, `SPM`, `HWP`, `LDR`, `TRM`

## Layer 4. Validation / Test

These are not product ECUs. They are validation harness/runtime test surfaces.

- `TEST_SCN`
- `TEST_BAS`

## Code-Level Interpretation

This model is visible in current code.

Examples:
- `VCU`, `IVI`, `MDPS`, `ADAS`, `V2X` directly publish backbone seam messages
- `CGW` supervises boundary, health, and fail-safe instead of relaying every raw payload
- `TEST_SCN` sees almost the full system as tester/harness
- `TEST_BAS` is a summary aggregator, not a raw multi-domain collector

## Design Rule Going Forward

1. surface ECU naming follows OEM-style short names
2. central gateway/service nodes remain distinct from domain controllers
3. leaf ECU breadth can grow without forcing every leaf into central gateway ownership
4. validation/test stays explicitly separated from product ECU layers

## Operational Consequence

If GUI grouping is changed later, use this order:
1. Central Gateway / Backbone Services
2. Domain Controllers
3. Leaf ECUs
4. Validation / Test

Do not regroup GUI directly by implementation helper/module names.

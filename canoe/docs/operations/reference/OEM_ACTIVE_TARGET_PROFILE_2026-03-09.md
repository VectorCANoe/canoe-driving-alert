# OEM Active Target Profile (2026-03-09)

## Active Target

Use this as the real execution profile for the current reset cycle.

1. Total vehicle surface inventory
- target: `100`
- chosen baseline: `100`

2. Deep active runtime implementation
- target: `12~18`
- chosen baseline: `16`

3. Core custom / differentiating ECU surfaces
- target: `6~10`
- chosen baseline: `8`

4. Validation / harness / test stack
- target: `3~6`
- chosen baseline: `4`

## Why This Profile Replaces The Old 32/41/27 Split

- `32` primary was too small and made the vehicle look shallow.
- A real OEM-style reviewer surface must show most of the vehicle in the first layer.
- The correct tradeoff is:
  - widen the primary layer
  - keep deep runtime narrow
  - keep premium/option surfaces placeholder-first

## Active Layering Rule

Treat the active `100` surface inventory as three simultaneous layers:

1. `Primary reviewer surface`
- `56`
- first-line ECU set used in top-level architecture views and reviewer-facing summaries

2. `Secondary vehicle breadth`
- `28`
- still part of the active vehicle program, but shown mainly in domain trees and decomposition views

3. `Premium / option / next-wave surface`
- `16`
- active in the bank, but placeholder-first unless promoted

This keeps the architecture wide without making the top layer look like a thin demo.

## Active 100-Surface Vehicle Inventory Profile

### Layer 1. Primary Reviewer Surface (`56`)

- `CGW`
- `ETH_BACKBONE`
- `DCM`
- `IBOX`
- `SECURITY_GATEWAY`
- `ECM`
- `TCM`
- `VCU`
- `AWD_4WD`
- `BAT_BMS`
- `FPCM`
- `LVR`
- `ISG`
- `EOP`
- `EWP`
- `ESP`
- `EPS`
- `ABS`
- `EPB`
- `TPMS`
- `SAS`
- `ECS`
- `ACU`
- `ODS`
- `VSM`
- `EHB`
- `CDC`
- `BCM`
- `HVAC`
- `SMK`
- `AFLS`
- `LIGHTING_ECU`
- `WIPER_MODULE`
- `SUNROOF_MODULE`
- `DOOR_FL`
- `DOOR_FR`
- `TAILGATE_MODULE`
- `IVI`
- `CLUSTER`
- `HUD`
- `TMU`
- `AMP`
- `PGS`
- `NAV_MODULE`
- `DIGITAL_KEY`
- `ADAS`
- `V2X`
- `SCC`
- `LDWS_LKAS`
- `FCA`
- `BCW`
- `LCA`
- `SPAS`
- `RSPA`
- `AVM`
- `FCAM`

### Layer 2. Secondary Vehicle Breadth (`28`)

- `FRADAR`
- `SRR_FL`
- `SRR_FR`
- `SRR_RL`
- `SRR_RR`
- `PARK_ULTRASONIC`
- `DMS`
- `OMS`
- `DOOR_RL`
- `DOOR_RR`
- `SEAT_DRV`
- `SEAT_PASS`
- `MIRROR_MODULE`
- `BODY_SECURITY_MODULE`
- `VOICE_ASSIST`
- `RSE`
- `VALIDATION_HARNESS`
- `OBC`
- `DCDC`
- `MCU`
- `INVERTER`
- `CHARGE_PORT_CTRL`
- `AIR_SUSPENSION`
- `RWS`
- `NIGHT_VISION`
- `AEB_DOMAIN`
- `PARK_MASTER`
- `OTA_MASTER`

### Layer 3. Premium / Option Program Surface (`16`)

- `TRAILER_CTRL`
- `HEADLAMP_LEVELING`
- `AUTO_DOOR_CTRL`
- `POWER_TAILGATE_CTRL`
- `MASSAGE_SEAT_CTRL`
- `REAR_CLIMATE_MODULE`
- `CABIN_SENSING`
- `BIOMETRIC_AUTH`
- `CARPAY_CTRL`
- `PHONE_AS_KEY`
- `EDGE_LOGGER`
- `ROAD_PREVIEW_CAMERA`
- `LIDAR`
- `REAR_RADAR_MASTER`
- `SURROUND_PARK_MASTER`
- `HIGHWAY_PILOT`

Vehicle surface total: `100`

## Chosen 16 Deep Runtime Surfaces

1. `CGW`
2. `ETH_BACKBONE`
3. `ECM`
4. `TCM`
5. `VCU`
6. `ESP`
7. `EPS`
8. `BCM`
9. `IVI`
10. `CLUSTER`
11. `ADAS`
12. `V2X`
13. `VALIDATION_HARNESS`
14. `SCC`
15. `TMU`
16. `SECURITY_GATEWAY`

## Chosen 8 Core Custom Surfaces

1. `ADAS`
2. `V2X`
3. `BCM`
4. `CLUSTER`
5. `IVI`
6. `CGW`
7. `VALIDATION_HARNESS`
8. `SCC`

## Chosen 4 Validation / Test Stack Elements

1. `VALIDATION_HARNESS`
2. `VAL_SCENARIO_CTRL`
3. `VAL_BASELINE_CTRL`
4. `CANOE_NATIVE_TEST_SUITE`

## Trim-Down Fallback

If implementation pressure rises later, the first trim-down target is:

- surface inventory: `52`
- deep runtime: `14`
- core custom surfaces: `8`
- validation / test: `4`

## Relationship To The 100 ECU Bank

- `OEM_100_ECU_PROGRAM_BANK_2026-03-09.md` is the active surface source bank.
- This file is the active execution profile for using that 100-bank in practice.
- Rule:
  - active architecture breadth follows the `100` bank
  - active deep implementation stays controlled at `16`
  - premium/option layer stays placeholder-first unless promoted
  - trim-down is allowed later, but breadth-first framing comes first now

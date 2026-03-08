# OEM Active Target Profile (2026-03-09)

## Active Target

Use this as the real program target for the current repository shape.

1. Total vehicle surface inventory
- target: `100`
- chosen baseline: `100`

2. Deep active runtime implementation
- target: `12~18`
- chosen baseline: `14`

3. Core custom / differentiating ECU surfaces
- target: `6~10`
- chosen baseline: `8`

4. Validation / harness / test stack
- target: `3~6`
- chosen baseline: `4`

## Why 100 Is Now The Active Surface Target

- The project is being reset toward an OEM-scale vehicle program surface.
- Growing later from `52` to `100` would force another naming and grouping rewrite.
- Locking the `100` surface bank now is cheaper while the reset cost is still low.
- Deep runtime remains narrow, so breadth increases without exploding implementation cost.

## Active Layering Rule

Treat the active `100` surface inventory as three simultaneous layers:

1. `Primary reviewer surface`
- `32`
- first-line ECU set used in top-level architecture views and reviewer-facing summaries

2. `Secondary vehicle breadth`
- `41`
- shown in domain trees and OEM-scale vehicle decomposition views

3. `Premium / option / next-wave surface`
- `27`
- still active in the program bank, but placeholder-first unless promoted

This keeps the architecture wide without pretending that all `100` ECUs are deep runtimes.

## Active 100-Surface Vehicle Inventory Profile

### Layer 1. Primary Reviewer Surface (`32`)

- `CGW`
- `ETH_BACKBONE`
- `DCM`
- `IBOX`
- `ECM`
- `TCM`
- `VCU`
- `AWD_4WD`
- `BAT_BMS`
- `FPCM`
- `LVR`
- `ESP`
- `EPS`
- `ABS`
- `EPB`
- `TPMS`
- `SAS`
- `ACU`
- `BCM`
- `HVAC`
- `SMK`
- `LIGHTING_ECU`
- `IVI`
- `CLUSTER`
- `HUD`
- `TMU`
- `ADAS`
- `V2X`
- `SCC`
- `LDWS_LKAS`
- `FCA`
- `AVM`

### Layer 2. Secondary Vehicle Breadth (`41`)

- `SECURITY_GATEWAY`
- `ISG`
- `EOP`
- `EWP`
- `ECS`
- `ODS`
- `VSM`
- `EHB`
- `CDC`
- `AFLS`
- `WIPER_MODULE`
- `SUNROOF_MODULE`
- `DOOR_FL`
- `DOOR_FR`
- `DOOR_RL`
- `DOOR_RR`
- `TAILGATE_MODULE`
- `SEAT_DRV`
- `SEAT_PASS`
- `MIRROR_MODULE`
- `BODY_SECURITY_MODULE`
- `AMP`
- `PGS`
- `NAV_MODULE`
- `VOICE_ASSIST`
- `RSE`
- `DIGITAL_KEY`
- `BCW`
- `LCA`
- `SPAS`
- `RSPA`
- `FCAM`
- `FRADAR`
- `SRR_FL`
- `SRR_FR`
- `SRR_RL`
- `SRR_RR`
- `PARK_ULTRASONIC`
- `DMS`
- `OMS`
- `VALIDATION_HARNESS`

### Layer 3. Premium / Option Program Surface (`27`)

- `OBC`
- `DCDC`
- `MCU`
- `INVERTER`
- `CHARGE_PORT_CTRL`
- `AIR_SUSPENSION`
- `RWS`
- `NIGHT_VISION`
- `AEB_DOMAIN`
- `HIGHWAY_PILOT`
- `PARK_MASTER`
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
- `OTA_MASTER`
- `EDGE_LOGGER`
- `ROAD_PREVIEW_CAMERA`
- `LIDAR`
- `REAR_RADAR_MASTER`
- `SURROUND_PARK_MASTER`

Vehicle surface total: `100`

## Chosen 14 Deep Runtime Surfaces

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
14. `SCC` (next deep target)

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

## Relationship To The 100 ECU Bank

- `OEM_100_ECU_PROGRAM_BANK_2026-03-09.md` is now the active surface source bank.
- This file is the active execution profile for using that 100-bank in practice.
- Rule:
  - active architecture breadth follows the `100` bank
  - active deep implementation stays controlled at `14`
  - premium/option layer stays placeholder-first unless promoted

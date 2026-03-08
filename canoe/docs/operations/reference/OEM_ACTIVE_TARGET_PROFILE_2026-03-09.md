# OEM Active Target Profile (2026-03-09)

## Active Target

Use this as the real program target for the current repository shape.

1. Total vehicle surface inventory
- target: `40~60`
- chosen baseline: `52`

2. Deep active runtime implementation
- target: `12~18`
- chosen baseline: `14`

3. Core custom / differentiating ECU surfaces
- target: `6~10`
- chosen baseline: `8`

4. Validation / harness / test stack
- target: `3~6`
- chosen baseline: `4`

## Why This Is Better Than Using 100 As The Active Target

- `100` is useful as a reserve bank, not as the active implementation target.
- `52` is wide enough to read like a vehicle program.
- `14` deep runtimes is still maintainable.
- This keeps breadth high and implementation cost controlled.

## Chosen 52-Surface Vehicle Inventory

### Infrastructure / Integration (`4`)

1. `CGW`
2. `ETH_BACKBONE`
3. `DCM`
4. `IBOX`

### Powertrain (`7`)

1. `ECM`
2. `TCM`
3. `VCU`
4. `AWD_4WD`
5. `BAT_BMS`
6. `FPCM`
7. `LVR`

### Chassis / Safety (`10`)

1. `ESP`
2. `EPS`
3. `ABS`
4. `EPB`
5. `TPMS`
6. `SAS`
7. `ECS`
8. `ACU`
9. `ODS`
10. `VSM`

### Body / Comfort (`11`)

1. `BCM`
2. `HVAC`
3. `SMK`
4. `AFLS`
5. `LIGHTING_ECU`
6. `DOOR_MODULE`
7. `SEAT_MODULE`
8. `WIPER_MODULE`
9. `SUNROOF_MODULE`
10. `MIRROR_MODULE`
11. `BODY_SECURITY_MODULE`

### IVI / HMI / Connectivity (`7`)

1. `IVI`
2. `CLUSTER`
3. `HUD`
4. `TMU`
5. `AMP`
6. `NAV_MODULE`
7. `DIGITAL_KEY`

### ADAS / V2X (`13`)

1. `ADAS`
2. `V2X`
3. `SCC`
4. `LDWS_LKAS`
5. `FCA`
6. `BCW`
7. `LCA`
8. `SPAS`
9. `AVM`
10. `FCAM`
11. `FRADAR`
12. `DMS`
13. `OMS`

Vehicle surface total: `52`

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

- `OEM_100_ECU_PROGRAM_BANK_2026-03-09.md` stays as the reserve bank.
- This file is the active implementation target.
- Rule:
  - active work follows this file
  - future breadth expansion can still draw from the 100-bank file

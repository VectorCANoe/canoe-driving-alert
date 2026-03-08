# OEM Wide Surface ECU Inventory V1 (2026-03-09)

## Purpose

- Expand the visible vehicle-program surface well beyond the previous `20+` level.
- Give the project the shape of a full OEM vehicle architecture while keeping deep implementation focused.
- Select only the ECU surfaces that are useful for a believable complete-vehicle view.

## Selection Rule

This inventory is for:

- vehicle architecture breadth
- GUI/domain grouping planning
- presentation and runtime refactor direction

This inventory is **not** equal to:

- deep CAPL implementation count
- immediate DBC ownership count
- immediate GUI rename count

## Target Shape

- visible surface ECUs: `36`
- deep active runtime surfaces: `13~15`
- light breadth surfaces: `20+`
- core custom feature surfaces: `6~8`

## 1. Infrastructure / Integration

| Surface ECU | Depth | Notes |
|---|---|---|
| `CGW` | Deep | central gateway and domain routing |
| `ETH_BACKBONE` | Deep | Ethernet transport / health |
| `DCM` | Light | diagnostics / service surface |
| `IBOX` | Light | info box / junction / integration surface |

## 2. Powertrain

| Surface ECU | Depth | Notes |
|---|---|---|
| `ECM` | Deep | engine control |
| `TCM` | Deep | transmission control |
| `VCU` | Deep | longitudinal vehicle control |
| `AWD_4WD` | Light | drivetrain torque split |
| `BAT_BMS` | Light | battery / battery sensing |
| `FPCM` | Light | fuel pump control |
| `LVR` | Light | electronic shift lever |

## 3. Chassis / Safety

| Surface ECU | Depth | Notes |
|---|---|---|
| `ESP` | Deep | brake / stability |
| `EPS` | Deep | steering assist |
| `ABS` | Light | braking sub-surface / wheel-speed family |
| `EPB` | Light | electric parking brake |
| `TPMS` | Light | tire pressure monitoring |
| `SAS` | Light | steering angle sensing |
| `ECS` | Light | active suspension |
| `ACU` | Light | airbag controller |
| `ODS` | Light | occupant detection |

## 4. Body / Comfort

| Surface ECU | Depth | Notes |
|---|---|---|
| `BCM` | Deep | body control / comfort / ambient |
| `HVAC` | Light | climate/DATC |
| `SMK` | Light | smart key |
| `DOOR_MODULE` | Light | door/lock/latch |
| `SEAT_MODULE` | Light | seat/belt/occupant |
| `LIGHTING_ECU` | Light | lighting breadth surface |
| `AFLS` | Light | adaptive front lighting |
| `PSB` | Light | pre-safe seat belt |

## 5. IVI / HMI / Connectivity

| Surface ECU | Depth | Notes |
|---|---|---|
| `IVI` | Deep | infotainment / navigation |
| `CLUSTER` | Deep | cluster / warnings |
| `HUD` | Light | head-up display |
| `TMU` | Light | telematics / connectivity |
| `PGS` | Light | parking guidance |

## 6. ADAS / V2X / Parking

| Surface ECU | Depth | Notes |
|---|---|---|
| `ADAS` | Deep | risk evaluation / arbitration core |
| `V2X` | Deep | emergency/V2X path |
| `SCC` | Light, optional deep later | smart cruise control |
| `LDWS_LKAS` | Light | lane departure / lane keeping |
| `FCA` | Light | forward collision avoidance |
| `BCW` | Light | blind-spot warning |
| `LCA` | Light | lane change assist |
| `SPAS` | Light | smart parking assist |
| `AVM` | Light | around-view monitor |
| `FCAM` | Light | front camera surface |
| `FRADAR` | Light | front radar surface |

## 7. Validation

| Surface ECU | Depth | Notes |
|---|---|---|
| `VALIDATION_HARNESS` | Deep | non-production test/harness surface |

## Count Check

- Infrastructure / Integration: `4`
- Powertrain: `7`
- Chassis / Safety: `9`
- Body / Comfort: `8`
- IVI / HMI / Connectivity: `5`
- ADAS / V2X / Parking: `11`
- Validation: `1`

Total visible surface ECUs: `45`

## Practical Trim Rule

The full bank above is intentionally wide.

For the main reviewer-facing top layer, trim to the following `32`-surface set first:

### Primary Top Layer (`32`)

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
- `ECS`
- `ACU`
- `ODS`
- `BCM`
- `HVAC`
- `SMK`
- `DOOR_MODULE`
- `SEAT_MODULE`
- `LIGHTING_ECU`
- `IVI`
- `CLUSTER`
- `HUD`
- `TMU`
- `ADAS`
- `V2X`

### Second-Wave Surface (`13`)

- `AFLS`
- `PSB`
- `PGS`
- `SCC`
- `LDWS_LKAS`
- `FCA`
- `BCW`
- `LCA`
- `SPAS`
- `AVM`
- `FCAM`
- `FRADAR`
- `VALIDATION_HARNESS`

## Implementation Rule

Only these should stay deep right now:

- `CGW`
- `ETH_BACKBONE`
- `ECM`
- `TCM`
- `VCU`
- `ESP`
- `EPS`
- `BCM`
- `IVI`
- `CLUSTER`
- `ADAS`
- `V2X`
- `VALIDATION_HARNESS`

Optional 14th and 15th deep targets later:

- `SCC`
- `TMU`

## Short Conclusion

- Yes, the ECU surface should be much larger than the previous `20+` baseline.
- No, that does not mean the deep runtime must explode.
- The correct OEM-like shape is:
  - `30+ visible surfaces`
  - `13~15 deep runtime surfaces`
  - `6~8 core custom feature surfaces`

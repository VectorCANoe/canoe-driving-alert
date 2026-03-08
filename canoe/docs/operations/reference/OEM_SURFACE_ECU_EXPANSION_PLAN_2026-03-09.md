# OEM Surface ECU Expansion Plan (2026-03-09)

## Decision Summary

- Keep the network principle:
  - `domain CAN + CGW + Ethernet backbone`
- Do **not** try to deeply implement `20~30` ECUs.
- Do expose `20~30` logical surface ECUs so the project reads like a vehicle program, not a single feature demo.
- Keep `12~14` active runtime modules deep.
- Concentrate the real custom logic in `5~8` core feature ECUs.

## Why This Change Is Needed

- The current project reads too much like implementation modules and too little like a vehicle program.
- Reviewer-facing surface should show vehicle ECUs first.
- Runtime modules remain below the surface for CAPL ownership, debug value, and traceability.

## Reference Rule

Use the local OEM/OpenDBC references only for:

1. surface ECU taxonomy
2. common OEM abbreviations
3. breadth planning of a full vehicle program

Do **not** use them directly as:

1. active message ownership SoT
2. direct signal mapping SoT
3. direct runtime node structure

Local reference evidence already available in this repository:

- `reference/dbc/level3_communication/reference/hyundai_kia_base.dbc`
- `reference/dbc/level3_communication/reference/hyundai_2015_ccan.dbc`
- `reference/dbc/level3_communication/reference/hyundai_2015_mcan.dbc`

Representative OEM-style ECU names observed there:

- `BCM`
- `CGW`
- `EMS`
- `TCU`
- `ABS`
- `ESC`
- `MDPS`
- `EPB`
- `TPMS`
- `DATC`
- `ACU`
- `SMK`
- `CLU`
- `TMU`
- `HUD`
- `SCC`
- `LDWS_LKAS`
- `AVM`
- `_4WD`

## Architecture Decision

### Keep

- `domain CAN + Ethernet backbone + gateway`
- reviewer-facing surface ECU model
- runtime module split where ownership/debug value is real
- separate validation harness

### Do Not Do

- do not rebuild the project into a flat single-feature architecture
- do not add deep CAPL logic for every placeholder ECU
- do not copy OpenDBC node names blindly into runtime without ownership review

## Surface Layering Rule

We will use three layers, not one flat ECU list.

### Layer A. Primary Surface ECU

- reviewer-facing top-level vehicle architecture
- shown first in GUI, diagrams, and presentation
- limited to the ECUs that define the main vehicle story

### Layer B. Secondary OEM Breadth ECU

- still visible in a full vehicle architecture
- helps the project read like an OEM program
- usually no deep custom CAPL logic in this cycle
- may remain placeholder/lightweight

### Layer C. Runtime/Internal Module

- `_GW`, `_CTRL`, `_MGR`, `_TX`, `_RX`
- implementation-facing only
- not promoted to top-level reviewer surface unless they truly represent a standalone ECU

## OEM Alias Normalization Rule

Do not blindly surface every OEM abbreviation as an independent top-level ECU.

Use the following normalization policy:

| OEM/Reference Name | Current Program Surface | Treatment |
|---|---|---|
| `EMS` | `ECM` | top-level alias normalization |
| `TCU` | `TCM` | top-level alias normalization |
| `MDPS` | `EPS` | top-level alias normalization |
| `DATC` / `FATC` | `HVAC` | top-level alias normalization |
| `ABS` | `ESP` sub-surface | keep as secondary breadth or internal detail |
| `CGW` | `CGW` | keep top-level |
| `CLU` | `CLUSTER` | top-level alias normalization |
| `TMU` | `TMU` | secondary breadth surface |
| `SCC` | `SCC` | secondary ADAS breadth surface |
| `ACU` | `ACU` | secondary safety breadth surface |
| `SMK` | `SMK` | secondary body breadth surface |
| `_4WD` | `AWD_4WD` | secondary powertrain breadth surface |

Rule:

- If the OEM abbreviation already reads like a real ECU and improves readability, keep it.
- If the OEM abbreviation is too signal-centric or supplier-centric, normalize it to a clearer surface ECU.

## Recommended Surface ECU Inventory

Target range for the final vehicle-program surface:

- visible surface ECUs: `26~30`
- deep active runtime modules: `12~14`
- core custom feature ECUs: `5~8`

### 1. Infrastructure Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `CGW` | Active | Deep | central gateway / domain routing / boundary |
| `ETH_BACKBONE` | Active | Deep | Ethernet transport health / backbone monitor |
| `DCM` | Placeholder | Light | diagnostic communication manager surface |

### 2. Powertrain Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `ECM` | Active | Deep | engine control |
| `TCM` | Active | Deep | transmission control |
| `VCU` | Active | Deep | longitudinal vehicle control |
| `AWD_4WD` | Placeholder | Light | torque split / drivetrain breadth surface |
| `BAT_BMS` | Placeholder | Light | battery / battery sensing breadth surface |
| `LVR` | Placeholder | Light | electronic gear lever breadth surface |

### 3. Chassis Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `ESP` | Active | Deep | brake / stability |
| `EPS` | Active | Deep | steering |
| `ABS` | Placeholder | Light | brake sub-surface / wheel-speed breadth surface |
| `EPB` | Placeholder | Light | electric parking brake |
| `TPMS` | Placeholder | Light | tire pressure monitoring |
| `SAS` | Placeholder | Light | steering angle sensing surface |
| `ECS` | Placeholder | Light | active suspension breadth surface |
| `EVP` | Placeholder | Light | electric vacuum pump breadth surface |

### 4. Body / Comfort Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `BCM` | Active | Deep | body / ambient / comfort control |
| `HVAC` | Placeholder | Light | climate / DATC breadth surface |
| `SMK` | Placeholder | Light | smart key |
| `ACU` | Placeholder | Light | airbag controller |
| `DOOR_MODULE` | Placeholder | Light | door / lock / latch surface |
| `SEAT_MODULE` | Placeholder | Light | seat / belt / occupancy surface |
| `LIGHTING_ECU` | Placeholder | Light | exterior/interior lighting breadth surface |

### 5. IVI / HMI Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `IVI` | Active | Deep | head unit / navigation / infotainment |
| `CLUSTER` | Active | Deep | cluster / warning / display |
| `HUD` | Placeholder | Light | head-up display breadth surface |
| `TMU` | Placeholder | Light | telematics / connectivity unit |

### 6. ADAS / V2X Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `ADAS` | Active | Deep | risk evaluation / warning arbitration |
| `V2X` | Active | Deep | emergency/V2X path |
| `SCC` | Placeholder | Light | smart cruise control / longitudinal ADAS breadth |
| `FCAM` | Placeholder | Light | front camera surface |
| `FRADAR` | Placeholder | Light | front radar surface |
| `AVM` | Placeholder | Light | around-view monitor / parking breadth surface |
| `LKA_LDW` | Placeholder | Light | lane keeping / lane departure breadth surface |

### 7. Validation Surface

| Surface ECU | Status | Runtime Depth | Notes |
|---|---|---|---|
| `VALIDATION_HARNESS` | Active | Deep | `VAL_*`, non-production only |

## Count Check

- Surface ECU total in this plan: `30`
- Deep active runtime target:
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
- Result: `13 deep surfaces + 11 light placeholder surfaces`
- Result: `13 deep surfaces + 17 light breadth surfaces`

This is within the intended project shape.

## Secondary OEM Breadth Candidate Bank

These are useful for a believable OEM architecture, but they should **not** all become deep runtime targets in this cycle.

### Powertrain / Driveline Candidate Bank

| Candidate | Typical Meaning | Recommended Role In This Project |
|---|---|---|
| `EMS` | engine management system | alias to `ECM` |
| `TCU` | transmission control unit | alias to `TCM` |
| `_4WD` | all-wheel-drive control | keep as `AWD_4WD` breadth surface |
| `LPI` | LPG fuel system | optional supplier/powertrain sub-surface only |
| `FPCM` | fuel pump control module | internal/sub-surface only unless fuel story is added |
| `DI_BOX` | injector driver box | internal/sub-surface only |
| `REA` | rotary electronic actuator / turbo actuator | internal/sub-surface only |
| `OPI` | oil pump inverter | internal/sub-surface only |
| `BAT` / battery sensing | battery/bms surface | expose as `BAT_BMS` breadth surface if needed |
| `LVR` | electronic lever | keep as light breadth surface |

### Chassis / Safety Candidate Bank

| Candidate | Typical Meaning | Recommended Role In This Project |
|---|---|---|
| `ABS` | anti-lock brake system | secondary chassis surface under `ESP` family |
| `ESC` | stability control | already represented by `ESP` top-level surface |
| `MDPS` | motor driven power steering | alias to `EPS` |
| `EPB` | electronic parking brake | light breadth surface |
| `ECS` | electronic control suspension | light breadth surface |
| `ACU` | airbag control unit | light safety breadth surface |
| `SAS` | steering angle sensor | light chassis sensing breadth surface |
| `TPMS` | tire pressure monitoring | light chassis sensing breadth surface |
| `EVP` | electric vacuum pump | light chassis/actuation breadth surface |

## Promotion Rule

An OEM candidate is promoted to top-level surface only if at least one of these is true:

1. it helps the reader understand the whole-vehicle architecture
2. it is a common OEM ECU name seen across references
3. it may later own a distinct DBC/message family
4. it would plausibly exist as a separate controller in a production vehicle

An OEM candidate stays out of top-level surface if:

1. it is mainly a sub-function or actuator detail
2. it would dilute the current vehicle story
3. it has no realistic place in current CAN/Ethernet ownership
4. it would force unnecessary deep runtime work now

## Core Custom Feature ECU Focus

The real project differentiation should stay concentrated here:

1. `ADAS`
2. `V2X`
3. `BCM`
4. `CLUSTER`
5. `IVI`
6. `CGW`
7. `VALIDATION_HARNESS`

Optional 8th depth candidate:

8. `SCC`

## Runtime Guidance

### Keep Deep Now

- `ENG_CTRL -> ECM`
- `TCM -> TCM`
- `ACCEL_CTRL -> VCU`
- `BRK_CTRL -> ESP`
- `STEER_CTRL -> EPS`
- `BODY_GW`, `AMBIENT_CTRL` -> `BCM`
- `IVI_GW` -> `IVI`
- `CLU_HMI_CTRL` -> `CLUSTER`
- `ADAS_WARN_CTRL`, `WARN_ARB_MGR` -> `ADAS`
- `CHS_GW`, `INFOTAINMENT_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` -> `CGW`
- `ETH_SW -> ETH_BACKBONE`
- `EMS_ALERT_RX` (+ later fold producers) -> `V2X`
- `VAL_* -> VALIDATION_HARNESS`

### Merge Candidate

- `HAZARD_CTRL`
- `WINDOW_CTRL`
- `DRV_STATE_MGR`
- `NAV_CTX_MGR`
- `CLU_BASE_CTRL`
- `EMS_POLICE_TX`
- `EMS_AMB_TX`

### Placeholder Only For Now

- `HVAC`
- `SMK`
- `ACU`
- `DOOR_MODULE`
- `SEAT_MODULE`
- `LIGHTING_ECU`
- `HUD`
- `TMU`
- `SCC`
- `FCAM`
- `FRADAR`
- `AVM`
- `TPMS`
- `EPB`
- `SAS`
- `AWD_4WD`
- `DCM`

## Test Planning Guidance

Target number of native/system-visible tests:

- `3~6`

Recommended set:

1. `School Zone Overspeed`
2. `Emergency Vehicle Yield`
3. `Domain Boundary Fail-safe`
4. `BCM Ambient + Cluster Consistency`
5. `ADAS Object Risk Pre-Activation Path`
6. `Validation Harness Regression Batch`

## Recommended Next Step For Dev1

1. Freeze this surface inventory in `canoe/` as the Dev1 implementation baseline.
2. Do not add SoT changes directly from Dev1.
3. Start runtime work in this order:
   - `BCM` fold candidates
   - `IVI/CLUSTER` fold candidates
   - `V2X` producer fold
4. Leave GUI surface rename until the runtime grouping is technically ready.

## Short Rule

- `OpenDBC tells us what a vehicle usually looks like.`
- `Our runtime decides what we actually implement deeply.`
- `Surface breadth grows first; deep custom logic stays focused.`

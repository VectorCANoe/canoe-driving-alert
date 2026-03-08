# OEM ECU Candidate Bank (2026-03-09)

## Purpose

- Capture additional OEM-style ECU candidates before Dev1 runtime refactor starts.
- Separate:
  - `top-level surface ECU`
  - `secondary breadth surface`
  - `alias to existing surface`
  - `do-not-promote / internal only`

This is a Dev1-side architecture intake note under `canoe/`.
It is **not** a SoT rewrite document.

## Key Rule

Do not promote an ECU candidate only because the abbreviation exists in a reference DBC.

Promote only when all three are mostly true:

1. it improves whole-vehicle readability
2. it plausibly exists as a separate production ECU
3. it does not force unnecessary deep implementation in this cycle

## Category Review

### 1. Powertrain Candidates

| Candidate | Meaning | Decision | Reason |
|---|---|---|---|
| `EMS` | Engine Management System | Alias -> `ECM` | OEM-realistic, but current project surface is clearer as `ECM` |
| `TCU` | Transmission Control Unit | Alias -> `TCM` | same role family, avoid duplicate top-level naming |
| `_4WD` | 4WD / torque split control | Secondary breadth surface | good breadth signal, no deep implementation now |
| `LPI` | LPG injection | Do not promote now | fuel-type specific, too narrow for current vehicle story |
| `FPCM` | Fuel Pump Control Module | Internal / optional sub-surface | plausible ECU, but not needed as top-level now |
| `DI_BOX` | injector driver box | Internal only | supplier/implementation-facing, poor reviewer surface |
| `REA` | rotary electronic actuator | Internal only | actuator detail, not a strong top-level ECU |
| `OPI` | oil pump inverter | Internal only | powertrain sub-device, not needed on the main surface |
| `BAT_BMS` | battery / BMS style surface | Secondary breadth surface | useful if electrification breadth is desired |
| `LVR` | electronic lever | Secondary breadth surface | visible cabin control breadth candidate |

### 2. Chassis / Safety Candidates

| Candidate | Meaning | Decision | Reason |
|---|---|---|---|
| `ABS` | anti-lock braking | Secondary breadth surface under `ESP` family | useful for vehicle realism, but not separate deep runtime now |
| `ESC` | stability control | Alias -> `ESP` | keep one top-level stability surface |
| `MDPS` | motor-driven power steering | Alias -> `EPS` | keep one steering surface |
| `EPB` | electronic parking brake | Secondary breadth surface | OEM-realistic, light placeholder suitable |
| `ECS` | electronic control suspension | Secondary breadth surface | suspension breadth is useful, no deep logic needed |
| `ACU` | airbag control unit | Secondary breadth surface | strong safety ECU, breadth value high |
| `SAS` | steering angle sensor | Secondary breadth surface | believable chassis sensing ECU |
| `TPMS` | tire pressure monitoring | Secondary breadth surface | breadth value high, low implementation burden |
| `EVP` | electric vacuum pump | Do not promote now | actuator/support ECU, low reviewer value |

### 3. ADAS Candidates

| Candidate | Meaning | Decision | Reason |
|---|---|---|---|
| `SCC` | smart cruise control | Secondary breadth surface, optional 8th deep target | very OEM-like and aligns with future ADAS expansion |
| `LDWS_LKAS` | lane departure / lane keeping | Secondary breadth surface | strong ADAS breadth, but do not deepen now |
| `FCA` | forward collision avoidance | Secondary breadth surface | useful future-facing ADAS label |
| `BCW` | blind-spot collision warning | Secondary breadth surface | good breadth surface if side-risk story is needed |
| `LCA` | lane change assist | Secondary breadth surface | reasonable, but overlaps with BCW/BSD family |
| `SPAS` | smart parking assist | Secondary breadth surface | OEM-realistic parking stack surface |
| `RSPA` | remote smart parking assist | Do not promote now | too specific unless remote parking becomes a scenario |
| `AVM` | around-view monitor | Secondary breadth surface | useful parking/HMI breadth |
| `SNV` | smart night vision | Do not promote now | too far from current scope |

### 4. Body / Comfort / HMI / Connectivity Candidates

| Candidate | Meaning | Decision | Reason |
|---|---|---|---|
| `BCM` | body control module | Top-level surface ECU | already core to current project |
| `CLU` | cluster | Alias -> `CLUSTER` | normalize to clearer top-level surface |
| `DATC` | digital automatic temperature control | Alias -> `HVAC` | clearer cabin-climate surface |
| `SMK` | smart key module | Secondary breadth surface | good body breadth candidate |
| `AFLS` | adaptive front lighting | Secondary breadth surface | lighting breadth value is strong |
| `AAF` | active air flap | Do not promote now | too powertrain/thermal subfunction-specific |
| `PSB` | pre-safe seat belt | Secondary breadth surface under seat/occupant safety | useful safety breadth, but not top-level main ECU |
| `PGS` | parking guidance system | Secondary breadth surface or sub-surface under HMI/parking | useful if parking story is shown |
| `TMU` | telematics control unit | Secondary breadth surface | strong connectivity breadth value |
| `IBOX` | intelligent junction/info box | Alias / secondary infra-HMI candidate | depends on whether connectivity stack is centralized or CGW/TMU/IVI split |
| `ODS` | occupant detection system | Secondary breadth surface | good safety/body breadth candidate |
| `HUD` | head-up display | Secondary breadth surface | belongs to HMI, not ADAS |

## Recommended Promotion Set

### Keep As Current Top-Level Deep Surface

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

### Promote As Secondary Breadth Surface

- `HVAC`
- `SMK`
- `ACU`
- `DOOR_MODULE`
- `SEAT_MODULE`
- `LIGHTING_ECU`
- `HUD`
- `TMU`
- `SCC`
- `LDWS_LKAS`
- `FCA`
- `BCW`
- `LCA`
- `SPAS`
- `AVM`
- `TPMS`
- `EPB`
- `SAS`
- `ECS`
- `AWD_4WD`
- `BAT_BMS`
- `LVR`
- `ODS`
- `AFLS`

### Keep As Alias / Normalized Name

- `EMS -> ECM`
- `TCU -> TCM`
- `MDPS -> EPS`
- `ESC -> ESP`
- `CLU -> CLUSTER`
- `DATC -> HVAC`

### Do Not Promote In Current Cycle

- `LPI`
- `FPCM`
- `DI_BOX`
- `REA`
- `OPI`
- `EVP`
- `RSPA`
- `SNV`
- `AAF`

## Architecture Reading Rule

When presenting the vehicle as an OEM-scale program:

1. show the deep top-level surfaces first
2. show secondary breadth surfaces as lighter ECUs
3. keep alias names only as reference notes
4. keep implementation modules completely below the surface

## Short Conclusion

- The user-provided list is useful.
- It should expand the **surface inventory**, not the **deep runtime count**.
- The project should look broad at the vehicle level and focused at the implementation level.

## OEM Placeholder Naming Audit (2026-03-09)

This audit checks whether the 100-node visible bank follows OEM/HKG-style surface naming.

## 1. Decision

The current bank was **not fully aligned**.

- deep runtime anchors were already acceptable
- a subset of placeholder surfaces still used descriptive English names
- those descriptive names are acceptable for internal planning, but not ideal for reviewer-facing OEM surface views

## 2. High-Confidence Renames Applied

These names were normalized immediately because local Hyundai/Kia reference files contain direct or near-direct equivalents.

| Previous | Current | Basis |
| --- | --- | --- |
| `AWD_4WD` | `_4WD` | direct HKG reference BU |
| `HVAC` | `DATC` | direct HKG reference BU |
| `LIGHTING_ECU` | `AHLS` | direct HKG reference BU |
| `SECURITY_GATEWAY` | `SGW` | accepted industry abbreviation for security gateway surface |
| `EDGE_LOGGER` | `EDR` | accepted automotive event recorder abbreviation |

## 3. Good Surface Names (Keep)

These already look correct enough for OEM/HKG-style surface naming.

- `CGW`
- `EMS`
- `TCU`
- `VCU`
- `ESC`
- `MDPS`
- `BCM`
- `IVI`
- `CLU`
- `ADAS`
- `V2X`
- `DCM`
- `IBOX`
- `TMU`
- `ABS`
- `EPB`
- `TPMS`
- `SAS`
- `ECS`
- `ACU`
- `ODS`
- `FPCM`
- `LVR`
- `SCC`
- `LDWS_LKAS`
- `FCA`
- `BCW`
- `LCA`
- `SPAS`
- `RSPA`
- `AVM`
- `FCAM`
- `FRADAR`
- `HUD`
- `PGS`
- `AFLS`

## 4. Remaining Generic Placeholder Exceptions

These names still read more like internal breadth placeholders than OEM-grade surface ECUs.

- `AEB_DOMAIN`
- `AUTO_DOOR_CTRL`
- `BODY_SECURITY_MODULE`
- `CARPAY_CTRL`
- `CHARGE_PORT_CTRL`
- `DIGITAL_KEY`
- `ETH_BACKBONE`
- `MASSAGE_SEAT_CTRL`
- `MIRROR_MODULE`
- `NAV_MODULE`
- `OTA_MASTER`
- `PARK_MASTER`
- `PHONE_AS_KEY`
- `POWER_TAILGATE_CTRL`
- `REAR_CLIMATE_MODULE`
- `REAR_RADAR_MASTER`
- `SUNROOF_MODULE`
- `SURROUND_PARK_MASTER`
- `TAILGATE_MODULE`
- `TRAILER_CTRL`
- `VOICE_ASSIST`
- `WIPER_MODULE`

## 5. Handling Rule

- Keep these remaining names in the visible bank for breadth accounting.
- Do **not** treat them as final reviewer-facing names yet.
- For architecture review:
  - `primary surface` should emphasize the already normalized OEM-style names
  - remaining generic exceptions should stay in `secondary/premium` buckets until aliasing is finalized

## 6. Next Rename Gate

Before renaming the remaining generic exceptions:

1. find a strong local HKG/reference equivalent, or
2. define a project-wide compact alias table once and apply it consistently

Do not rename them one-by-one ad hoc.

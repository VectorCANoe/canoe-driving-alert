# OEM 100 ECU Program Bank (2026-03-09)

## Decision

Yes, the architecture surface can be expanded much more.

Use this model:

- `Base vehicle inventory`: `72` surface ECUs
- `Validation surface`: `1`
- `Premium option bank`: `27`
- `Grand total inventory bank`: `100`

This is now the active surface architecture bank.
It is **not** a commitment to deeply implement 100 runtimes.

## Why This Is Reasonable

- A real vehicle program is much broader than the currently active feature set.
- The reviewer should read the project as a complete vehicle architecture, not a single scenario demo.
- Breadth can be modeled now while deep implementation stays limited.

## Execution Rule

Keep these separate:

1. `Surface inventory breadth`
2. `Deep runtime implementation`
3. `Core custom feature focus`

Recommended implementation depth remains:

- deep runtime surfaces: `14~16`
- core custom feature surfaces: `6~8`

## Surface Type Tag (for reviewer clarity)

To avoid confusing functional/service surfaces with physical ECU modules, use these tags:

- `PHYSICAL`: typical domain ECU/controller in OEM architecture
- `FUNCTION_SURFACE`: feature/service surface name shown for architecture breadth
- `INFRA_SERVICE`: integration/governance/logging/security service surface
- `VALIDATION`: test/harness surface only

Representative non-physical surfaces in this bank:

- `CPAY`, `PAK`, `EDGE_LOGGER`, `AEB`, `HWP`, `SPM`

These remain placeholder-first unless explicitly promoted.

## Activation Rule

- Treat this document as the active surface inventory bank for the reset cycle.
- Use [OEM_ACTIVE_TARGET_PROFILE_2026-03-09.md](./OEM_ACTIVE_TARGET_PROFILE_2026-03-09.md) to decide:
  - which `100` surfaces are primary reviewer-facing
  - which remain placeholder-first
  - which are promoted to deep runtime

## A. Base Vehicle Inventory (`72`)

### A1. Infrastructure / Integration (`5`)

1. `CGW`
2. `ETHB`
3. `DCM`
4. `IBOX`
5. `SGW`

### A2. Powertrain (`10`)

1. `EMS`
2. `TCU`
3. `VCU`
4. `_4WD`
5. `BAT_BMS`
6. `FPCM`
7. `LVR`
8. `ISG`
9. `EOP`
10. `EWP`

### A3. Chassis / Safety (`12`)

1. `ESC`
2. `MDPS`
3. `ABS`
4. `EPB`
5. `TPMS`
6. `SAS`
7. `ECS`
8. `ACU`
9. `ODS`
10. `VSM`
11. `EHB`
12. `CDC`

### A4. Body / Comfort (`16`)

1. `BCM`
2. `DATC`
3. `SMK`
4. `AFLS`
5. `AHLS`
6. `WIP`
7. `SRF`
8. `DOOR_FL`
9. `DOOR_FR`
10. `DOOR_RL`
11. `DOOR_RR`
12. `TGM`
13. `SEAT_DRV`
14. `SEAT_PASS`
15. `MIR`
16. `BSEC`

### A5. IVI / HMI / Connectivity (`10`)

1. `IVI`
2. `CLU`
3. `HUD`
4. `TMU`
5. `AMP`
6. `PGS`
7. `NAV`
8. `VCS`
9. `RSE`
10. `DKEY`

### A6. ADAS / V2X / Parking (`19`)

1. `ADAS`
2. `V2X`
3. `SCC`
4. `LDWS_LKAS`
5. `FCA`
6. `BCW`
7. `LCA`
8. `SPAS`
9. `RSPA`
10. `AVM`
11. `FCAM`
12. `FRADAR`
13. `SRR_FL`
14. `SRR_FR`
15. `SRR_RL`
16. `SRR_RR`
17. `PUS`
18. `DMS`
19. `OMS`

Base vehicle inventory total: `72`

## B. Validation Surface (`1`)

1. `VALIDATION_HARNESS`

Inventory subtotal with validation: `73`

## C. Premium Option Bank (`27`)

These are realistic additional surfaces for a higher trim / premium / technology-heavy program.

1. `OBC`
2. `DCDC`
3. `MCU`
4. `INVERTER`
5. `CPC`
6. `ASM`
7. `RWS`
8. `NIGHT_VISION`
9. `AEB`
10. `HWP`
11. `PKM`
12. `TRM`
13. `HLM`
14. `ADM`
15. `PTG`
16. `MSC`
17. `RATC`
18. `CSM`
19. `BIO`
20. `CPAY`
21. `PAK`
22. `OTA`
23. `EDR`
24. `RPC`
25. `LDR`
26. `RRM`
27. `SPM`

Grand total inventory bank: `100`

## D. Practical Layering

### Layer 1. Primary Reviewer Surface (`56`)

Use these first in the main architecture tree:

- `CGW`
- `ETHB`
- `DCM`
- `IBOX`
- `SGW`
- `EMS`
- `TCU`
- `VCU`
- `_4WD`
- `BAT_BMS`
- `FPCM`
- `LVR`
- `ISG`
- `EOP`
- `EWP`
- `ESC`
- `MDPS`
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
- `DATC`
- `SMK`
- `AFLS`
- `AHLS`
- `WIP`
- `SRF`
- `DOOR_FL`
- `DOOR_FR`
- `TGM`
- `IVI`
- `CLU`
- `HUD`
- `TMU`
- `AMP`
- `PGS`
- `NAV`
- `DKEY`
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

Use these in category views, domain trees, and optional system maps:

- `FRADAR`
- `SRR_FL`
- `SRR_FR`
- `SRR_RL`
- `SRR_RR`
- `PUS`
- `DMS`
- `OMS`
- `DOOR_RL`
- `DOOR_RR`
- `SEAT_DRV`
- `SEAT_PASS`
- `MIR`
- `BSEC`
- `VCS`
- `RSE`
- `VALIDATION_HARNESS`
- `OBC`
- `DCDC`
- `MCU`
- `INVERTER`
- `CPC`
- `ASM`
- `RWS`
- `NIGHT_VISION`
- `AEB`
- `PKM`
- `OTA`

### Layer 3. Premium Option Bank (`16`)

Keep these active in the surface bank, but placeholder-first unless promoted.

- `TRM`
- `HLM`
- `ADM`
- `PTG`
- `MSC`
- `RATC`
- `CSM`
- `BIO`
- `CPAY`
- `PAK`
- `EDR`
- `RPC`
- `LDR`
- `RRM`
- `SPM`
- `HWP`

## E. Deep Runtime Commitment

Keep deep runtime scope controlled even with 100-bank breadth.

### Deep Now (`16`)

- `CGW`
- `ETHB`
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
- `VALIDATION_HARNESS`
- `SCC`
- `TMU`
- `SGW`

## F. Core Custom Feature Focus (`8`)

1. `ADAS`
2. `V2X`
3. `BCM`
4. `CLU`
5. `IVI`
6. `CGW`
7. `VALIDATION_HARNESS`
8. `SCC`

## Short Conclusion

- Yes, `50` is still small if the goal is to look like a complete OEM vehicle program.
- Use `72 + 1 + 27 = 100` as the active surface bank.
- Keep actual deep implementation narrow and status-controlled.


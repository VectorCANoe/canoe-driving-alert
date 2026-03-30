# ECU Group Network View (2026-03-28)

Subtitle: Grouped reading layer between the full overview map and the per-ECU catalog.

## Purpose

This note groups the current runtime into clusters that move together in one vehicle story.
Use it as the grouped reading layer between the overview map and the ECU cards.

## Group 1. Base Vehicle Dynamics

### Primary nodes

- `VCU`
- `ESC`
- `MDPS`
- `TCU`
- `EMS`

### Main path

`Input surface -> vehicle motion owners -> gateway, assist, and display readers`

### Why this group matters

- This is the base vehicle state producer set.
- If this group drifts, downstream assist and display behavior also drifts.

### Reading focus

- steering command/readback unification
- speed preset vs real pedal ownership
- brake pressure stability before AEB assist overlay

## Group 2. ADAS / AEB / Brake Assist

### Primary nodes

- `ADAS`
- `SCC`
- `V2X`
- `AEB`
- `ESC`
- `EHB`
- `VSM`

### Main path

`route, vehicle, V2X, and object context -> ADAS -> AEB -> chassis intervention`

### Why this group matters

- This is the main intervention and warning-decision cluster.
- It is the main cluster to read when multiple assist reactions appear at once.

### Reading focus

- `AEB` is the producer
- `ESC`, `EHB`, `VSM` are simultaneous consumers
- one profile step can look like multiple ECU reactions at once

## Group 3. Display / Warning / Audio Output

### Primary nodes

- `CGW`
- `IVI`
- `CLU`
- `BCM`
- `AMP`

### Main path

`selected alert state -> gateway gating -> IVI / CLU / BCM / AMP`

### Why this group matters

- Ownership here is mostly stable.
- Perceived output issues usually come from upstream decision/gate paths, not local display ownership.

## Group 4. Body / Comfort / Ambient

### Primary nodes

- `BCM`
- `DATC`
- `WIP`
- `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`
- `SEAT_DRV`, `SEAT_PASS`
- `SRF`
- `AHLS`, `AFLS`

### Main path

`body and comfort input -> BCM / body leaves -> ambient and cabin response`

### Why this group matters

- Wider than the current input surface
- important for comfort/context consistency
- lower priority than dynamics/AEB for first-pass runtime stabilization

## Group 5. Validation / Scenario Overlay

### Primary nodes

- `TEST_SCN`
- `TEST_BAS`

### Rule

- `TEST_SCN` stays scenario-focused
- `TEST_BAS` stays validation/base-summary focused
- neither should become the hidden owner of normal vehicle behavior

## Group 6. Backbone / Gateway / Diagnostics

### Primary nodes

- `CGW`
- `ETHB`
- `DCM`
- `IBOX`
- `SGW`
- `EDR`
- `EXT_DIAG`
- `OTA`, `DKEY`, `CPAY`, `PAK`, `TMU`

### Main path

`domain state / service requests -> CGW / ETHB / DCM / SGW / IBOX -> routed gateway, diagnostic, and external service surfaces`

### Why this group matters

- This group is easy to under-document because it is less visible than dynamics or ADAS.
- But external service, diagnostic, and gateway reasoning become unreadable if this cluster is omitted.

## Reading Priority

1. `ADAS / AEB / ESC / EHB / VSM`
2. `VCU / ESC / MDPS`
3. `CGW / IVI / CLU / BCM / AMP`
4. body/comfort breadth surfaces
5. gateway / diagnostic / service surfaces

## Companion Assets

- matrix: `ECU_NETWORK_MASTER_MATRIX_2026-03-28.md`
- full overview: `svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_2026-03-28.svg`
- high-level risk map: `svg/CORE_COUPLED_ECU_GROUP_MAP_2026-03-28.svg`
- dynamics: `svg/GROUP_01_BASE_VEHICLE_DYNAMICS_2026-03-28.svg`
- ADAS/AEB: `svg/GROUP_02_ADAS_AEB_BRAKE_ASSIST_2026-03-28.svg`
- output: `svg/GROUP_03_DISPLAY_WARNING_AUDIO_2026-03-28.svg`
- body/ambient: `svg/GROUP_04_BODY_COMFORT_AMBIENT_2026-03-28.svg`
- validation/scenario: `svg/GROUP_05_VALIDATION_SCENARIO_2026-03-28.svg`
- backbone/diagnostics: `svg/GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_2026-03-28.svg`
- master book: `ECU_METADATA_BOOK_2026-03-28.md`
- generated ECU network flow cards: `ECU_CARD_INDEX_2026-03-28.md`
- detailed signal-flow source: `flows/signal/STEERING_TURN_SIGNAL_FLOW_2026-03-28.puml`
- detailed signal-flow preview: `svg/flows/signal/STEERING_TURN_SIGNAL_FLOW_2026-03-28.svg`

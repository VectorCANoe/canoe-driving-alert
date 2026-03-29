# ECU Group Network View (2026-03-28)

## Purpose

This note groups the current runtime into clusters that actually move together at runtime.
It is not a replacement for `0302`; it is a runtime reading layer.

## Group 1. Base Vehicle Dynamics

### Primary nodes

- `VCU`
- `ESC`
- `MDPS`
- `TCU`
- `EMS`

### Main path

`Input_Console -> Cmd::* -> VCU / ESC / MDPS -> frmVehicleStateCanMsg / frmBrakeStatusMsg / frmSteeringTorqueMsg -> CGW / ADAS / IVI / CLU`

### Why this group matters

- This is the base vehicle state producer set.
- If this group is unstable, every ADAS/HMI judgment becomes noisy.

### Current focus

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

`route context + vehicle state + V2X/perception -> ADAS -> decel assist / risk -> AEB StopReq/DecelProfile/DomainHealth -> ESC/EHB/VSM`

### Why this group matters

- This is the strongest current coupled-intervention cluster.
- It is the most likely source of "red brake stutter" or stepped intervention feel.

### Current risk read

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

`ADAS effective/gated state -> CGW gate reason -> IVI / CLU / BCM / AMP -> text / ambient / audio / display`

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

`Cmd::* / body state -> BCM/body leaves -> body readback -> ambient / comfort / cabin display`

### Why this group matters

- Wider than the current input surface
- important for comfort/context consistency
- lower priority than dynamics/AEB for immediate runtime stabilization

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

## Immediate Debug Priority

1. `ADAS / AEB / ESC / EHB / VSM`
2. `VCU / ESC / MDPS`
3. `CGW / IVI / CLU / BCM / AMP`
4. body/comfort breadth surfaces
5. gateway / diagnostic / service surfaces

## Immediate Artifact Link

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
- action signal flow sample: `flows/STEERING_TURN_SIGNAL_FLOW_2026-03-28.puml`
- action signal flow preview: `svg/flows/STEERING_TURN_SIGNAL_FLOW_2026-03-28.svg`

# Logical ECU Surface Mapping V1 (2026-03-08)

## Core Principle

- Not every CAPL node should be shown as a production ECU.
- Many active nodes are implementation modules, not top-level vehicle ECUs.
- The reset goal is to keep the runtime where it helps, while simplifying the public ECU surface.

## Mapping Rules

| Action | Meaning |
|---|---|
| Keep as surface ECU | Keep visible as a production-style ECU |
| Fold into surface ECU | Keep runtime module, but hide it under a larger logical ECU |
| Infrastructure only | Treat as backbone/gateway infrastructure, not a feature ECU |
| Validation only | Keep separate from production architecture |

## Runtime Node to Surface ECU Map

| Current Runtime Node | Current Role | Production-Style Surface ECU | Action | Reason |
|---|---|---|---|---|
| ENG_CTRL | Engine state/runtime | ECM | Keep as surface ECU | Clear powertrain ECU role |
| TCM | Transmission control | TCM | Keep as surface ECU | Already production-style |
| ACCEL_CTRL | Pedal/throttle request logic | ECM or VCU | Fold into surface ECU | Not a realistic standalone ECU surface |
| BRK_CTRL | Brake/pressure logic | ESC / IBC | Fold into surface ECU | Production projects usually surface brake/stability ECU, not raw brake module |
| STEER_CTRL | Steering logic | EPS | Fold into surface ECU | Better surfaced as EPS |
| CHS_GW | Chassis CAN normalization | CGW / Chassis Gateway | Infrastructure only | Gateway function, not vehicle feature ECU |
| EMS_POLICE_TX | Emergency producer | V2X / EMS ECU | Fold into surface ECU | Internal producer module |
| EMS_AMB_TX | Emergency producer | V2X / EMS ECU | Fold into surface ECU | Internal producer module |
| EMS_ALERT_RX | Emergency receive/timeout | V2X / EMS ECU | Fold into surface ECU | Internal receiver module |
| ADAS_WARN_CTRL | ADAS risk evaluation | ADAS ECU / ADAS Fusion | Fold into surface ECU | Core feature logic, but better grouped |
| WARN_ARB_MGR | Alert arbitration | ADAS ECU / Warning Fusion | Fold into surface ECU | Core feature logic, but not a surface ECU name |
| NAV_CTX_MGR | Navigation context logic | IVI / Navigation ECU | Fold into surface ECU | Application module, not surface ECU |
| INFOTAINMENT_GW | IVI CAN normalization | CGW / IVI Gateway | Infrastructure only | Gateway function |
| IVI_GW | Cluster frame producer | IVI Head Unit or Cluster Gateway | Fold into surface ECU | Presentation transport module |
| CLU_HMI_CTRL | Cluster warning/HMI logic | Cluster ECU | Fold into surface ECU | Better surfaced as Cluster ECU |
| CLU_BASE_CTRL | Cluster base state | Cluster ECU | Fold into surface ECU | Same surface as cluster |
| BODY_GW | Body output gateway | BCM / Body Gateway | Fold into surface ECU | Gateway/output packaging, not final surface |
| AMBIENT_CTRL | Ambient output owner | BCM / Lighting ECU | Fold into surface ECU | Better under BCM/Lighting surface |
| HAZARD_CTRL | Hazard function | BCM | Fold into surface ECU | Body function, not separate top-level ECU |
| WINDOW_CTRL | Window/door/mirror function | BCM / Door Module | Fold into surface ECU | Body domain function |
| DRV_STATE_MGR | seat/belt/security state | BCM / Occupant Module | Fold into surface ECU | Body state aggregation, not reviewer-facing ECU |
| DOMAIN_ROUTER | powertrain/body route logic | CGW | Infrastructure only | Routing logic |
| DOMAIN_BOUNDARY_MGR | path health/fail-safe boundary | CGW / Backbone Manager | Infrastructure only | Boundary/fail-safe infra |
| ETH_SW | Ethernet health/backbone monitor | CGW / Backbone | Infrastructure only | Transport/backbone infra |
| VAL_SCENARIO_CTRL | validation harness | Validation Harness | Validation only | Non-production |
| VAL_BASELINE_CTRL | validation harness | Validation Harness | Validation only | Non-production |

## Recommended Production-Style Surface Inventory

### Network / Backbone
- `CGW`
- `ETH_BACKBONE`

### Powertrain
- `ECM`
- `TCM`

### Chassis
- `ESC` or `IBC`
- `EPS`

### Body
- `BCM`
- `HVAC`
- optional split later: `Door Module`, `Seat Module`, `Lighting Module`

### Infotainment / HMI
- `IVI`
- `Cluster`
- `Navigation`

### ADAS / V2X
- `ADAS ECU`
- `V2X ECU`
- optional later: `Front Camera`, `Front Radar`, `Park Assist`

### Validation
- `Validation Harness` (never treated as production ECU)

## Recommended Reset Strategy

### Stage 1
- Rebuild docs and GUI around the surface inventory above.
- Keep runtime modules mostly intact.

### Stage 2
- Only merge runtime code where the split has no ownership/debug value.
- Do not merge simply for naming convenience.

### Stage 3
- If needed, add thin vehicle-wide stubs for breadth.
- Do not build deep custom logic for all of them.

## Why This Is Better

- Reviewers will see a vehicle architecture, not an implementation tree.
- The project becomes readable at first glance.
- The existing CAPL investment is preserved.
- Future Ethernet cutover becomes easier because surface ECUs stay stable while internal transport modules evolve.

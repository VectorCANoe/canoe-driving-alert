# Runtime Absorption Status (2026-03-09)

## Final status

Wrapper absorption for the current runtime wave is complete.

### Absorbed into `BCM`
- hazard handling
- window command handling
- driver-state forwarding
- ambient output handling

### Absorbed into `IVI`
- infotainment gateway ingress
- navigation context handling

### Absorbed into `CLU`
- baseline cluster display helper

### Absorbed into `V2X`
- police dispatch producer
- ambulance dispatch producer

### Absorbed into `ADAS`
- warning arbitration helper

## Active runtime anchors to keep split

| Runtime anchor | Reason |
| --- | --- |
| `EMS` | engine management owner |
| `TCU` | transmission owner |
| `VCU` | propulsion / accel command owner |
| `ESC` | brake / stability owner |
| `MDPS` | steering owner |
| `CHGW` | chassis ingress normalization, synthesis, and chassis diag boundary |
| `PTGW` | powertrain routing policy and drive-mode boundary |
| `CGW` | cross-domain health, fail-safe, and boundary authority |
| `ETHM` | backbone freshness monitor |
| `BCM` | body output owner |
| `IVI` | infotainment output owner |
| `CLU` | cluster output owner |
| `ADAS` | integrated risk / warning / assist decision owner |
| `V2X` | integrated V2X ingress / emergency context owner |
| `VAL_SCENARIO_CTRL` | validation orchestrator |
| `VAL_BASELINE_CTRL` | validation result aggregator |

## Current policy
- absorb helper/runtime-wrapper nodes
- keep ECU anchors and infrastructure anchors split
- do not add new ECUs until this anchor set is stable in GUI and compile flow

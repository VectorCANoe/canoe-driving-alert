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
| `CGW` | cross-domain health, fail-safe, and boundary authority |
| `BCM` | body output owner |
| `IVI` | infotainment output owner |
| `CLU` | cluster output owner |
| `ADAS` | integrated risk / warning / assist decision owner |
| `V2X` | integrated V2X ingress / emergency context owner |
| `TEST_SCN` | validation orchestrator |
| `TEST_BAS` | validation result aggregator |

Anchor count: `13` (product runtime `11` + validation runtime `2`)

## Historical rename closure

- `CHGW`, `PTGW`, `ETHM` are not active runtime anchors in the current tree.
- related responsibilities are now covered by:
  - `VCU` (vehicle/powertrain seam publication)
  - `MDPS` (steering seam publication)
  - `CGW` (boundary/freshness/fail-safe authority)

## Current policy
- absorb helper/runtime-wrapper nodes
- keep ECU anchors and infrastructure anchors split
- keep placeholder surfaces compile-safe and non-traffic by default
- do not promote placeholder to deep runtime without owner/ID/contract closure

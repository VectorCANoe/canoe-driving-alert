# OEM Runtime Anchor Naming Audit (2026-03-09)

## Scope

This audit verifies that the **current active runtime anchor names** align with:

1. OEM-style reviewer readability
2. runtime ownership boundaries
3. current active code baseline (`56521c2`)

## Current Active Runtime Set

- Product runtime anchors (`11`):
  - `EMS`, `TCU`, `VCU`, `ESC`, `MDPS`, `CGW`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`
- Validation-only runtime (`2`):
  - `TST_SCN`, `TST_BAS`

## Summary Decision

| Runtime Node | Keep Split | Surface Mapping | Decision | Reason |
| --- | --- | --- | --- | --- |
| `EMS` | Yes | `ECM` | Keep | engine state owner |
| `TCU` | Yes | `TCM` | Keep | transmission owner |
| `VCU` | Yes | `VCU` | Keep | vehicle/powertrain seam owner |
| `ESC` | Yes | `ESP` | Keep | brake/stability owner |
| `MDPS` | Yes | `EPS` | Keep | steering owner |
| `CGW` | Yes | `CGW` | Keep | cross-domain boundary/fail-safe authority |
| `BCM` | Yes | `BCM` | Keep | body output owner |
| `IVI` | Yes | `IVI` | Keep | infotainment owner |
| `CLU` | Yes | `CLUSTER` | Keep | cluster display owner |
| `ADAS` | Yes | `ADAS` | Keep | risk/decision owner |
| `V2X` | Yes | `V2X` | Keep | emergency ingress/context owner |
| `TST_SCN` | Yes | `VALIDATION_HARNESS` | Keep | validation orchestrator |
| `TST_BAS` | Yes | `VALIDATION_HARNESS` | Keep | validation result aggregator |

## Historical Labels (Retired)

The following labels were intermediate audit artifacts and are no longer active runtime names:

- `CHGW`
- `PTGW`
- `ETHM`

Related concerns are currently handled by:

- `VCU` (vehicle/powertrain seam publication)
- `MDPS` (steering seam publication)
- `CGW` (boundary/freshness/fail-safe authority)

## Structural Finding

No urgent naming defect was found in the current active runtime set.

The remaining risk is not naming but governance consistency:

- keep `surface vs runtime vs validation` separation explicit in docs
- do not promote placeholder nodes directly to deep runtime without owner/ID/contract closure

## Action

1. Keep this audit as the naming baseline for current runtime anchors.
2. Treat placeholder ECU expansion as surface-only unless promoted by wave plan.
3. Update sync scripts (`check_capl_sync.py`) to the new active inventory policy.

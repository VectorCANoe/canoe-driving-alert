# ECU Architecture Reset Grouping V1 (2026-03-08)

## Decision Goal

- Reset the project around production-style logical ECU surfaces.
- Separate three layers explicitly:
  - Logical ECU Surface
  - Runtime Node / Implementation Module
  - Validation Harness

## Findings

1. The current active runtime split is not fundamentally wrong.
2. The current naming is too implementation-driven on the visible surface.
3. `_TX/_RX/_MGR/_CTRL` is acceptable for internal modules, but weak as top-level ECU presentation.
4. Legacy samples are stronger in public-facing ECU naming, but weaker in runtime robustness.

## Recommended Logical ECU Groups

| Logical ECU Surface | Keep as Separate Runtime Modules | Why |
|---|---|---|
| EMS_ALERT | EMS_POLICE_TX, EMS_AMB_TX, EMS_ALERT_RX | One logical emergency terminal, multiple transport/producer-consumer modules |
| ADAS | ADAS_WARN_CTRL, WARN_ARB_MGR | One logical warning domain, but decision engine and arbitration should remain split |
| NAV_IVI | NAV_CTX_MGR, INFOTAINMENT_GW, IVI_GW, CLU_HMI_CTRL, CLU_BASE_CTRL | Navigation + cluster/IVI experience surface |
| BODY_BCM | BODY_GW, AMBIENT_CTRL, HAZARD_CTRL, WINDOW_CTRL, DRV_STATE_MGR | One body/body-control surface, multiple output/state modules |
| CHASSIS | CHS_GW, ACCEL_CTRL, BRK_CTRL, STEER_CTRL | Vehicle dynamics/chassis surface |
| POWERTRAIN | ENG_CTRL, TCM, DOMAIN_ROUTER | Powertrain surface with routing owned here for now |
| BACKBONE_GW | ETH_SW, DOMAIN_BOUNDARY_MGR | Network/backbone/boundary infrastructure |
| VALIDATION | VAL_SCENARIO_CTRL, VAL_BASELINE_CTRL | Validation-only harness, not production ECU |

## Merge / Keep Rules

### Keep Split

- `ADAS_WARN_CTRL` and `WARN_ARB_MGR`
- `BODY_GW` and `AMBIENT_CTRL`
- `IVI_GW` and `CLU_HMI_CTRL`
- `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX`
- `VAL_SCENARIO_CTRL` and `VAL_BASELINE_CTRL`

Reason:
- owner clarity
- debug traceability
- message direction clarity
- validation harness separation

### Candidate for Surface Merge Only

- `EMS_ALERT`
- `ADAS`
- `NAV_IVI`
- `BODY_BCM`
- `CHASSIS`
- `POWERTRAIN`
- `BACKBONE_GW`
- `VALIDATION`

Meaning:
- show as one logical group in GUI/doc/presentation
- keep runtime modules behind the surface mapping

## Naming Direction

| Layer | Naming Rule |
|---|---|
| Logical ECU Surface | short production-style names (`EMS`, `ADAS`, `IVI`, `BCM`, `CHS`, `PT`, `CGW`, `VAL`) |
| Runtime Node | current canonical/runtime names may remain during reset |
| Internal Module | `_TX/_RX/_MGR/_CTRL` allowed |

## Immediate Recommendation

1. Approve logical grouping first.
2. Build a `surface name -> runtime module` mapping table.
3. Only after that decide whether CANoe GUI node/group names should change.
4. Do not merge runtime code just to make the GUI look simpler.

## Next Reset Task

- Produce the full `active node -> logical ECU surface -> runtime role -> owner rationale` matrix.

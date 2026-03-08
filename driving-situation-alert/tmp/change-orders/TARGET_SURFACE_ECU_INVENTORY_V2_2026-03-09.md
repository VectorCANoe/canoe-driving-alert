# Target Surface ECU Inventory V2 (2026-03-09)

## Purpose

- Provide the mandatory second sheet required by `ECU_RESET_CLASSIFICATION_MATRIX_2026-03-09.md`.
- Freeze the production-style logical ECU surface before GUI rename and before `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04` rewrite.
- Keep runtime implementation modules intact unless the matrix explicitly marks them as merge targets.

## Coverage Check

- Active runtime nodes reviewed from `canoe/src/capl` (excluding `v1_legacy`): `26`
- Matrix rows in `ECU_RESET_CLASSIFICATION_MATRIX_2026-03-09.md`: `26`
- Result: current active runtime inventory is fully covered by the matrix (`26/26`, gap `0`).

## Layer Rule

1. Infrastructure Layer
- Network and boundary surfaces shown for architecture readability.
- These are not feature ECUs.

2. Production-Style Surface ECU Layer
- Reviewer-facing vehicle ECU surface.
- This is the layer that should dominate GUI, presentation, and upper SoT docs.

3. Runtime Implementation Layer
- `_CTRL/_MGR/_TX/_RX/_GW` modules remain below the surface.
- This layer stays visible in `04` and code mapping, not in reviewer-facing top-level structure.

4. Validation Layer
- Explicitly separated from production architecture.

## Target Surface ECU Inventory

### Infrastructure Surface

| Surface | Type | Status | Notes |
|---|---|---|---|
| `CGW` | Infrastructure | Active | Central/domain gateway surface |
| `ETH_BACKBONE` | Infrastructure | Active | Backbone transport/health surface |

### Production-Style Surface ECU

| Surface ECU | Layer | Runtime Status | Main Responsibility | Current Active Runtime Mapping |
|---|---|---|---|---|
| `ECM` | Powertrain | Active | engine/pedal/torque powertrain control | `ENG_CTRL`, `ACCEL_CTRL` |
| `TCM` | Powertrain | Active | transmission control | `TCM` |
| `ESC` | Chassis | Active by folded runtime | brake/stability surface | `BRK_CTRL` |
| `EPS` | Chassis | Active by folded runtime | steering assist/torque surface | `STEER_CTRL` |
| `BCM` | Body | Active by folded runtime | body function and ambient/body gateway ownership | `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` |
| `HVAC` | Body | Placeholder surface | cabin comfort/air management breadth surface | no dedicated active runtime yet |
| `IVI` | IVI/HMI | Active by folded runtime | IVI/navigation/service surface | `NAV_CTX_MGR`, `IVI_GW` |
| `CLUSTER` | IVI/HMI | Active by folded runtime | cluster display/HMI surface | `CLU_HMI_CTRL`, `CLU_BASE_CTRL` |
| `ADAS_ECU` | ADAS | Active by folded runtime | risk evaluation and warning arbitration | `ADAS_WARN_CTRL`, `WARN_ARB_MGR` |
| `V2X_ECU` | V2X | Active by folded runtime | emergency/V2X receive-produce logic | `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` |
| `VALIDATION_HARNESS` | Validation | Active | non-production scenario/baseline control | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` |

### Optional Future Surface (Do Not Block Current Reset)

| Surface | Status | When to Activate |
|---|---|---|
| `DOOR_MODULE` | Optional | only if body split is approved later |
| `LIGHTING_ECU` | Optional | only if ambient/lighting ownership needs separate reviewer surface |
| `OCCUPANT_MODULE` | Optional | only if driver/seat/belt logic needs standalone body sub-surface |
| `NAVIGATION` | Optional | only if IVI and navigation are split in approved surface policy |
| `WARNING_FUSION_ECU` | Optional | only if ADAS arbitration is intentionally separated from ADAS surface |
| `EMS_ALERT` | Optional logical alias | use as logical terminal label in upper docs only if `V2X_ECU` naming is not yet approved |

## Surface ECU -> Runtime Nodes

| Surface ECU | Runtime Nodes | Runtime Split Policy |
|---|---|---|
| `CGW` | `CHS_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR`, `INFOTAINMENT_GW` | Keep split |
| `ETH_BACKBONE` | `ETH_SW` | Keep split |
| `ECM` | `ENG_CTRL`, `ACCEL_CTRL` | Keep `ENG_CTRL`, `ACCEL_CTRL` = merge candidate |
| `TCM` | `TCM` | Keep split |
| `ESC` | `BRK_CTRL` | Merge candidate |
| `EPS` | `STEER_CTRL` | Merge candidate |
| `BCM` | `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` | Keep `BODY_GW`, `AMBIENT_CTRL`, `DRV_STATE_MGR`; `HAZARD_CTRL`, `WINDOW_CTRL` = merge candidate |
| `IVI` | `NAV_CTX_MGR`, `IVI_GW` | Keep `IVI_GW`; `NAV_CTX_MGR` = merge candidate |
| `CLUSTER` | `CLU_HMI_CTRL`, `CLU_BASE_CTRL` | Keep `CLU_HMI_CTRL`; `CLU_BASE_CTRL` = merge candidate |
| `ADAS_ECU` | `ADAS_WARN_CTRL`, `WARN_ARB_MGR` | Keep split |
| `V2X_ECU` | `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` | Merge candidate |
| `VALIDATION_HARNESS` | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` | Keep split |

## Must Merge / Keep Split / Optional Matrix

### Keep Split

- `CHS_GW`
- `DOMAIN_ROUTER`
- `DOMAIN_BOUNDARY_MGR`
- `INFOTAINMENT_GW`
- `ETH_SW`
- `ENG_CTRL`
- `TCM`
- `BODY_GW`
- `AMBIENT_CTRL`
- `DRV_STATE_MGR`
- `IVI_GW`
- `CLU_HMI_CTRL`
- `ADAS_WARN_CTRL`
- `WARN_ARB_MGR`
- `VAL_SCENARIO_CTRL`
- `VAL_BASELINE_CTRL`

### Merge Candidate

- `ACCEL_CTRL`
- `BRK_CTRL`
- `STEER_CTRL`
- `HAZARD_CTRL`
- `WINDOW_CTRL`
- `CLU_BASE_CTRL`
- `NAV_CTX_MGR`
- `EMS_POLICE_TX`
- `EMS_AMB_TX`
- `EMS_ALERT_RX`

### Optional / Deferred Surface Only

- `HVAC`
- `DOOR_MODULE`
- `LIGHTING_ECU`
- `OCCUPANT_MODULE`
- `NAVIGATION`
- `WARNING_FUSION_ECU`

## Immediate Use Rule

1. Use this inventory to decide the visible ECU surface in GUI and presentation.
2. Do not merge runtime code solely for naming convenience.
3. If a runtime node is `Keep split`, preserve it in CAPL and only hide it below the surface layer.
4. If a runtime node is `Merge candidate`, document first, then merge only after Dev1 code review approval.
5. `HVAC` remains a surface breadth placeholder and must not block current reset if no dedicated runtime exists.

## Recommended Next Step

1. Freeze this sheet together with the classification matrix.
2. Rewrite `00e` so it explicitly separates:
   - surface ECU name
   - runtime implementation module
   - validation harness
3. Rewrite `0301/0302/0303/0304/04` using this inventory as the primary surface baseline.
4. Rename GUI surface last.

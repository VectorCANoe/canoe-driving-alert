# Runtime Absorption Status (2026-03-09)

## Purpose
This note fixes the Dev1 runtime absorption boundary after the first OEM ECU consolidation wave.
It exists to prevent unnecessary merges in the `CGW/Infra` layer and to separate:
- absorbed implementation modules
- runtime anchors that must remain split
- GUI cleanup items that require CANoe GUI work later

## Absorption Completed

### BCM
- runtime anchor: `BODY_GW`
- absorbed modules:
  - `HAZARD_CTRL`
  - `WINDOW_CTRL`
  - `DRV_STATE_MGR`
  - `AMBIENT_CTRL`

### IVI
- runtime anchor: `IVI_GW`
- absorbed modules:
  - `NAV_CTX_MGR`
  - `INFOTAINMENT_GW`

### CLUSTER
- runtime anchor: `CLU_HMI_CTRL`
- absorbed modules:
  - `CLU_BASE_CTRL`

### V2X
- runtime anchor: `EMS_ALERT_RX`
- absorbed modules:
  - `EMS_POLICE_TX`
  - `EMS_AMB_TX`

### ADAS
- runtime anchor: `ADAS_WARN_CTRL`
- absorbed modules:
  - `WARN_ARB_MGR`

## Runtime Anchors To Keep Split
The following nodes are not merge targets in the current wave.
They are retained because they carry a distinct runtime responsibility.

| Runtime Node | Surface ECU | Why It Stays Split |
| --- | --- | --- |
| `CHS_GW` | `CGW` | input normalization and chassis gateway boundary |
| `DOMAIN_ROUTER` | `CGW` | routing policy and cross-domain powertrain relay |
| `DOMAIN_BOUNDARY_MGR` | `CGW` | domain health, e2e state, fail-safe authority |
| `ETH_SW` | `ETH_BACKBONE` | Ethernet-path freshness/health monitor |
| `ENG_CTRL` | `ECM` | powertrain owner runtime |
| `TCM` | `TCM` | transmission owner runtime |
| `ACCEL_CTRL` | `VCU` | acceleration command owner |
| `BRK_CTRL` | `ESP` | brake command owner |
| `STEER_CTRL` | `EPS` | steering command owner |
| `VAL_SCENARIO_CTRL` | `VALIDATION_HARNESS` | scenario orchestration harness |
| `VAL_BASELINE_CTRL` | `VALIDATION_HARNESS` | baseline result aggregation harness |

## GUI Cleanup Queue
These wrappers remain in runtime only because Dev1 must not patch CANoe `.cfg` directly.
They should be removed or hidden from the GUI surface after logical ECU grouping is finalized.

- `HAZARD_CTRL`
- `WINDOW_CTRL`
- `DRV_STATE_MGR`
- `AMBIENT_CTRL`
- `INFOTAINMENT_GW`
- `NAV_CTX_MGR`
- `CLU_BASE_CTRL`
- `EMS_POLICE_TX`
- `EMS_AMB_TX`
- `WARN_ARB_MGR`

## Next Dev1 Step
Move from absorption to expansion.

1. Keep the runtime anchors above intact.
2. Add new placeholder/light ECU nodes only where the OEM surface inventory needs breadth.
3. Implement deep logic only in the fixed active runtime set.

## Non-Overlap Rule With Dev2
- Dev1: `canoe/` runtime absorption, new ECU runtime anchors, native CANoe tests
- Dev2: `scripts/`, `product/sdv_operator/`, evidence packaging, CI/Jenkins integration
- Docs: `driving-situation-alert/`

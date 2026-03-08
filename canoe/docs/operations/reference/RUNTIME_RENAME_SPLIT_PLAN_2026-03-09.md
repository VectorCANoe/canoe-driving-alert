# Runtime Rename Split Plan (2026-03-09)

## Purpose
This note separates two different rename waves for Dev1.

1. `runtime file rename`
   - actual CAPL file / runtime canonical name change
   - do only for runtime anchors that will remain after the absorption wave
2. `GUI surface rename only`
   - no source/file rename
   - hide absorbed wrappers or present them only through their parent surface ECU label

This prevents over-renaming wrappers that should disappear later.

## A. Runtime File Rename Candidates
These nodes remain as real runtime anchors after absorption.
They justify actual CAPL/file rename in a later rename wave.

| Current Runtime Node | Current CAPL Role | Target OEM-Normalized Runtime Name | Parent Surface ECU | Action | Reason |
| --- | --- | --- | --- | --- | --- |
| `ENG_CTRL` | engine owner runtime | `ECM_CTRL` | `ECM` | file rename candidate | current name is generic control name, not OEM-style ECU anchor |
| `ACCEL_CTRL` | propulsion / accel command owner | `VCU_CTRL` | `VCU` | file rename candidate | belongs to vehicle control unit surface, not standalone accel ECU |
| `BRK_CTRL` | brake command owner | `ESP_CTRL` | `ESP` | file rename candidate | active brake/stability runtime is closer to ESP/ESC anchor |
| `STEER_CTRL` | steering command owner | `EPS_CTRL` | `EPS` | file rename candidate | current role matches EPS runtime anchor |
| `CHS_GW` | chassis-domain normalization + diag + state synthesis | `CHASSIS_DOMAIN_CTRL` | `CHASSIS_DOMAIN_CTRL` | file rename candidate | not a central gateway; current name understates owner role |
| `DOMAIN_ROUTER` | powertrain-domain routing / drive mode / health | `PT_DOMAIN_CTRL` | `PT_DOMAIN_CTRL` | file rename candidate | not a central gateway; current name is implementation-heavy |
| `DOMAIN_BOUNDARY_MGR` | cross-domain safety / fail-safe authority | `DOMAIN_BOUNDARY_CTRL` | `DOMAIN_BOUNDARY_CTRL` | file rename candidate | runtime anchor remains, but `MGR` is internal-module style |
| `ETH_SW` | Ethernet freshness/age monitor | `ETH_PATH_MONITOR` | `ETH_BACKBONE` | file rename candidate | current name implies switching/routing that the code does not perform |
| `BODY_GW` | BCM runtime anchor | `BCM_CTRL` | `BCM` | file rename candidate | body output owner is now effectively BCM controller |
| `IVI_GW` | IVI runtime anchor | `IVI_CTRL` | `IVI` | file rename candidate | now owns IVI route/diag/navigation outputs beyond a pure gateway |
| `CLU_HMI_CTRL` | cluster runtime anchor | `CLUSTER_CTRL` | `CLUSTER` | file rename candidate | primary cluster owner should read as cluster ECU, not HMI submodule |
| `ADAS_WARN_CTRL` | integrated ADAS warning runtime | `ADAS_CTRL` | `ADAS` | file rename candidate | arbitration already absorbed; current name is too narrow |
| `EMS_ALERT_RX` | integrated V2X runtime anchor | `V2X_CTRL` | `V2X` | file rename candidate | now owns both producers and receiver path; `RX` is misleading |

## B. Keep Name For Now
These remain as real runtime nodes, but the current names are acceptable enough to defer file rename.

| Runtime Node | Decision | Reason |
| --- | --- | --- |
| `TCM` | keep | already OEM-style and surface-aligned |
| `VAL_SCENARIO_CTRL` | keep | validation harness role is explicit and useful |
| `VAL_BASELINE_CTRL` | keep | validation result aggregation role is explicit |

## C. GUI Surface Rename Only Candidates
These are already absorbed or wrapper-only.
Do not spend time renaming source files.
Hide them from the reviewer-facing GUI surface or group them under the parent ECU.

| Current Wrapper / Residual Node | Parent Surface ECU | GUI Policy | Source/File Rename? | Reason |
| --- | --- | --- | --- | --- |
| `HAZARD_CTRL` | `BCM` | hide under BCM | no | wrapper only |
| `WINDOW_CTRL` | `BCM` | hide under BCM | no | wrapper only |
| `DRV_STATE_MGR` | `BCM` | hide under BCM | no | wrapper only |
| `AMBIENT_CTRL` | `BCM` | hide under BCM | no | wrapper only |
| `INFOTAINMENT_GW` | `IVI` | hide under IVI | no | wrapper only |
| `NAV_CTX_MGR` | `IVI` | hide under IVI | no | wrapper only |
| `CLU_BASE_CTRL` | `CLUSTER` | hide under CLUSTER | no | wrapper only |
| `EMS_POLICE_TX` | `V2X` | hide under V2X | no | wrapper only |
| `EMS_AMB_TX` | `V2X` | hide under V2X | no | wrapper only |
| `WARN_ARB_MGR` | `ADAS` | hide under ADAS | no | wrapper only |

## D. Rename Order
1. finish GUI hide/group treatment for wrapper-only nodes
2. rename runtime anchors in source + `cfg/channel_assign` mirrors
3. only after that, reflect the same names in CANoe GUI node labels

## E. Dev2 Non-Overlap
Dev2 can work in parallel only on:
- `scripts/`
- `product/sdv_operator/`
- evidence/report grouping using the target surface ECU names above

Dev2 must not rename CAPL files or edit `canoe/` runtime sources.

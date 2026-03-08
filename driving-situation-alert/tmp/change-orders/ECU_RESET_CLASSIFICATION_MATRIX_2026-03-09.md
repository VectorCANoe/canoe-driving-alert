# ECU Reset Classification Matrix (2026-03-09)

## Purpose

- Freeze the decision process before runtime refactor starts.
- Classify every active runtime node into one of these buckets:
  - `Keep as Surface ECU`
  - `Fold into Parent Surface ECU`
  - `Infrastructure Only`
  - `Validation Only`
- Use this matrix as the mandatory review artifact before GUI rename, node merge, or document rewrite.

## Review Rule

1. Read the current node name.
2. Read the code and runtime responsibility.
3. Decide the parent logical ECU.
4. Decide whether the runtime split should stay or be merged later.
5. Update review status only after code confirmation.

## Classification Matrix

| Current Runtime Node | CAPL Path | Current Role | Target Parent Surface ECU | Surface Decision | Runtime Decision | Rationale | Review Status |
|---|---|---|---|---|---|---|---|
| ENG_CTRL | `ecu/ENG_CTRL.can` | engine state / powertrain state | `ECM` | Keep as Surface ECU | Keep split | owns engine-state lifecycle and broadcasts multiple powertrain frames, so it already behaves like a reviewer-facing engine ECU | Code Reviewed |
| TCM | `ecu/TCM.can` | transmission control | `TCM` | Keep as Surface ECU | Keep split | owns gear/drive-mode dependent transmission outputs and already matches production-style transmission ECU naming | Code Reviewed |
| ACCEL_CTRL | `ecu/ACCEL_CTRL.can` | pedal/throttle request logic | `VCU` | Keep as Surface ECU | Keep split | acts as the SIL longitudinal plant and vehicle-state source; surface should be a generic vehicle control ECU rather than the implementation name `ACCEL_CTRL` | Code Reviewed |
| BRK_CTRL | `ecu/BRK_CTRL.can` | brake pressure / brake state | `ESP` | Keep as Surface ECU | Keep split | already owns brake, ABS, ESC, and decel-assist actuation outputs; strong production-style brake/stability ECU candidate | Code Reviewed |
| STEER_CTRL | `ecu/STEER_CTRL.can` | steering state / torque | `EPS` | Keep as Surface ECU | Keep split | owns steering command/state frame identity and reads like a simple but valid steering ECU once surfaced as `EPS` | Code Reviewed |
| CHS_GW | `input/CHS_GW.can` | chassis CAN normalization / gateway | `CGW` | Infrastructure Only | Keep split | consumes chassis ingress frames and normalizes them into `Core::*`; explicit gateway/normalization responsibility should stay split | Code Reviewed |
| DOMAIN_ROUTER | `ecu/DOMAIN_ROUTER.can` | domain route logic | `CGW` | Infrastructure Only | Keep split | derives routing policy, vehicle mode, and cross-domain powertrain gateway frames; integration/router logic should remain infrastructure only | Code Reviewed |
| DOMAIN_BOUNDARY_MGR | `ecu/DOMAIN_BOUNDARY_MGR.can` | path health / boundary / fail-safe | `CGW` | Infrastructure Only | Keep split | owns domain health, path status, and fail-safe gating across domains; clear infrastructure/boundary manager rather than a customer-facing ECU | Code Reviewed |
| ETH_SW | `network/ETH_SW.can` | Ethernet backbone monitor | `ETH_BACKBONE` | Infrastructure Only | Keep split | monitors freshness/health of the backbone path and does not act like a feature ECU; should stay a pure backbone/infrastructure element | Code Reviewed |
| INFOTAINMENT_GW | `input/INFOTAINMENT_GW.can` | infotainment CAN normalization | `CGW` | Infrastructure Only | Keep split | ingests nav-context CAN frames and normalizes IVI state into shared runtime variables; explicit ingress gateway role | Code Reviewed |
| BODY_GW | `output/BODY_GW.can` | body output frame producer | `BCM` | Fold into Parent Surface ECU | Keep split | packages body-domain outputs from `Core::*`/`Body::*` state but is not a credible top-level production ECU name; keep as internal BCM output module | Code Reviewed |
| IVI_GW | `output/IVI_GW.can` | cluster/HMI frame producer | `IVI` | Fold into Parent Surface ECU | Keep split | packages IVI-originated cluster/HMI/audio frames; valuable internal split, but too implementation-oriented for the surface ECU layer | Code Reviewed |
| AMBIENT_CTRL | `output/AMBIENT_CTRL.can` | ambient output owner | `BCM` | Fold into Parent Surface ECU | Keep split | owns ambient/body-lighting output semantics and diagnostics, but still reads best as an internal BCM feature/output module rather than a top-level ECU label | Code Reviewed |
| HAZARD_CTRL | `ecu/HAZARD_CTRL.can` | hazard basic body function | `BCM` | Fold into Parent Surface ECU | Merge candidate | only manages blink phase from received body frames; too small and too body-local to justify a standalone ECU surface | Code Reviewed |
| WINDOW_CTRL | `ecu/WINDOW_CTRL.can` | window/door/mirror state | `BCM` | Fold into Parent Surface ECU | Merge candidate | mostly mirrors received door/window states into a door-control frame; better treated as an internal BCM comfort subfunction | Code Reviewed |
| DRV_STATE_MGR | `ecu/DRV_STATE_MGR.can` | seat/belt/security state | `BCM` | Fold into Parent Surface ECU | Merge candidate | current file is an inactive placeholder with no meaningful runtime behavior, so it should not survive as a top-level ECU | Code Reviewed |
| CLU_HMI_CTRL | `output/CLU_HMI_CTRL.can` | cluster warning/HMI state owner | `Cluster` | Keep as Surface ECU | Keep split | owns displayed warning code, duplicate guard, history, and cluster-facing state; best nucleus for a production-style cluster ECU | Code Reviewed |
| CLU_BASE_CTRL | `ecu/CLU_BASE_CTRL.can` | cluster base display state | `Cluster` | Fold into Parent Surface ECU | Merge candidate | only tracks base display/sync status and should be absorbed into the main cluster ECU once the surface is renamed | Code Reviewed |
| NAV_CTX_MGR | `logic/NAV_CTX_MGR.can` | navigation context logic | `IVI` | Fold into Parent Surface ECU | Merge candidate | pure context-derivation logic that maps IVI/navigation inputs into `Core::*`; not strong enough as a standalone reviewer-facing ECU | Code Reviewed |
| ADAS_WARN_CTRL | `logic/ADAS_WARN_CTRL.can` | risk evaluation / trigger generation | `ADAS ECU` | Fold into Parent Surface ECU | Keep split | owns TTC/object-risk evaluation and warning trigger preparation; strong internal debug value, weak standalone ECU surface value | Code Reviewed |
| WARN_ARB_MGR | `logic/WARN_ARB_MGR.can` | arbitration / final warning selection | `ADAS ECU` | Fold into Parent Surface ECU | Keep split | owns final alert arbitration, hysteresis, and fail-safe policy; should stay a split runtime stage but not a top-level ECU label | Code Reviewed |
| EMS_POLICE_TX | `ems/EMS_POLICE_TX.can` | emergency police producer | `V2X ECU` | Fold into Parent Surface ECU | Merge candidate | tiny dispatch producer with no independent bus or lifecycle identity; should become an internal producer path under one V2X/emergency ECU | Code Reviewed |
| EMS_AMB_TX | `ems/EMS_AMB_TX.can` | emergency ambulance producer | `V2X ECU` | Fold into Parent Surface ECU | Merge candidate | tiny dispatch producer with no independent bus or lifecycle identity; should become an internal producer path under one V2X/emergency ECU | Code Reviewed |
| EMS_ALERT_RX | `logic/EMS_ALERT_RX.can` | emergency receive/timeout | `V2X ECU` | Fold into Parent Surface ECU | Keep split (merge base) | owns watchdog, priority selection, timeout clear, and event trace; best nucleus for a future single V2X ECU runtime even if producers are folded in | Code Reviewed |
| VAL_SCENARIO_CTRL | `input/VAL_SCENARIO_CTRL.can` | validation harness scenario control | `Validation Harness` | Validation Only | Keep split | drives scenario presets, baseline diagnostic requests, and test-only locks; must remain explicitly non-production | Code Reviewed |
| VAL_BASELINE_CTRL | `ecu/VAL_BASELINE_CTRL.can` | validation baseline aggregator | `Validation Harness` | Validation Only | Keep split | aggregates `frmTestResultMsg` into baseline validation output and must remain isolated from production ECU naming | Code Reviewed |

## Immediate Use

- This matrix must be updated first during node-by-node code review.
- No GUI renaming should happen before the relevant rows are upgraded from `Initial` to `Code Reviewed`.
- No runtime node merge should happen before the relevant rows are upgraded from `Code Reviewed` to `Approved for Refactor`.

## Target Surface ECU Inventory (Reviewed V1)

| Target Surface ECU | Current Runtime Nodes | Surface Type | Initial Refactor Direction |
|---|---|---|---|
| `ECM` | `ENG_CTRL` | Production ECU | keep as standalone surface ECU |
| `TCM` | `TCM` | Production ECU | keep as standalone surface ECU |
| `VCU` | `ACCEL_CTRL` | Production ECU | rename surface, keep runtime split for now |
| `ESP` | `BRK_CTRL` | Production ECU | rename surface, keep runtime split |
| `EPS` | `STEER_CTRL` | Production ECU | rename surface, keep runtime split |
| `BCM` | `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` | Production ECU | keep `BODY_GW` and `AMBIENT_CTRL` internal splits, fold the rest |
| `IVI` | `IVI_GW`, `NAV_CTX_MGR` | Production ECU | keep `IVI_GW` split, merge `NAV_CTX_MGR` inward |
| `Cluster` | `CLU_HMI_CTRL`, `CLU_BASE_CTRL` | Production ECU | keep `CLU_HMI_CTRL` as main runtime, absorb `CLU_BASE_CTRL` later |
| `ADAS ECU` | `ADAS_WARN_CTRL`, `WARN_ARB_MGR` | Core Feature ECU | keep both splits internally, hide implementation names from surface |
| `V2X ECU` | `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` | Core Feature ECU | promote `EMS_ALERT_RX` as merge base and fold TX producers inward |
| `CGW` | `CHS_GW`, `INFOTAINMENT_GW`, `DOMAIN_ROUTER`, `DOMAIN_BOUNDARY_MGR` | Infrastructure ECU | keep split; present as gateway/backbone infrastructure, not feature ECU |
| `ETH_BACKBONE` | `ETH_SW` | Infrastructure ECU | keep as explicit backbone monitor/infrastructure element |
| `Validation Harness` | `VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL` | Validation Only | keep fully separate from production ECU layer |

## Next Step

1. Freeze this inventory as the review baseline for GUI surface naming.
2. Decide which parent surfaces become reviewer-facing primary actors in docs and demos:
   - core feature ECUs
   - baseline vehicle ECUs
   - infrastructure ECUs
3. Only after that:
   - rename GUI surface labels
   - merge selected runtime nodes
   - rewrite `00e -> 0301 -> 0302 -> 0303 -> 0304 -> 04`

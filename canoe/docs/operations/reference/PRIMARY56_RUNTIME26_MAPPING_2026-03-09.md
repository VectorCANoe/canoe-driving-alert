# Primary-56 to Runtime-26 Mapping (2026-03-09)

## Purpose

- Freeze the first executable mapping between:
  - the `56` primary reviewer-facing surface ECUs
  - the current `26` active runtime nodes under `canoe/src/capl`
- Use this document before any runtime merge, GUI surface rename, or node absorption work.

## Scope Rule

- Primary reviewer-facing surface ECUs: `56`
- Current active runtime nodes: `26`
- Important exception:
  - `VAL_SCENARIO_CTRL`
  - `VAL_BASELINE_CTRL`
  do not belong to the `56` primary production surface.
  They stay under the secondary validation surface:
  - `VALIDATION_HARNESS`

## Summary

1. Primary surfaces with an active runtime anchor: `13`
2. Primary surfaces still placeholder-only: `43`
3. Validation-only runtime surfaces outside the primary-56 set: `1`
4. Current active runtime nodes:
   - `24` map into the primary-56 set
   - `2` map into `VALIDATION_HARNESS`

## A. Primary-56 Coverage Table

| Primary Surface ECU | Category | Mapped Active Runtime Node(s) | Current Status | Next Refactor Direction |
|---|---|---|---|---|
| `CGW` | Infrastructure | `CHS_GW`, `INFOTAINMENT_GW`, `DOMAIN_ROUTER` | Anchored | keep runtime split, expose one gateway surface |
| `ETH_BACKBONE` | Infrastructure | `ETH_SW` | Anchored | keep as explicit backbone runtime |
| `DCM` | Infrastructure | - | Placeholder | add later only if diagnostics breadth is needed |
| `IBOX` | Infrastructure | - | Placeholder | keep surface-only for now |
| `SECURITY_GATEWAY` | Infrastructure | `DOMAIN_BOUNDARY_MGR` | Anchored | keep split as boundary/security runtime |
| `ECM` | Powertrain | `ENG_CTRL` | Anchored | keep as standalone runtime ECU |
| `TCM` | Powertrain | `TCM` | Anchored | keep as standalone runtime ECU |
| `VCU` | Powertrain | `ACCEL_CTRL` | Anchored | rename surface only first, keep runtime split |
| `AWD_4WD` | Powertrain | - | Placeholder | surface breadth only |
| `BAT_BMS` | Powertrain | - | Placeholder | surface breadth only |
| `FPCM` | Powertrain | - | Placeholder | surface breadth only |
| `LVR` | Powertrain | - | Placeholder | surface breadth only |
| `ISG` | Powertrain | - | Placeholder | surface breadth only |
| `EOP` | Powertrain | - | Placeholder | surface breadth only |
| `EWP` | Powertrain | - | Placeholder | surface breadth only |
| `ESP` | Chassis/Safety | `BRK_CTRL` | Anchored | keep as standalone runtime ECU |
| `EPS` | Chassis/Safety | `STEER_CTRL` | Anchored | keep as standalone runtime ECU |
| `ABS` | Chassis/Safety | - | Placeholder | currently folded into `ESP` surface breadth |
| `EPB` | Chassis/Safety | - | Placeholder | surface breadth only |
| `TPMS` | Chassis/Safety | - | Placeholder | surface breadth only |
| `SAS` | Chassis/Safety | - | Placeholder | surface breadth only |
| `ECS` | Chassis/Safety | - | Placeholder | surface breadth only |
| `ACU` | Chassis/Safety | - | Placeholder | surface breadth only |
| `ODS` | Chassis/Safety | - | Placeholder | surface breadth only |
| `VSM` | Chassis/Safety | - | Placeholder | surface breadth only |
| `EHB` | Chassis/Safety | - | Placeholder | surface breadth only |
| `CDC` | Chassis/Safety | - | Placeholder | surface breadth only |
| `BCM` | Body/Comfort | `BODY_GW`, `AMBIENT_CTRL`, `HAZARD_CTRL`, `WINDOW_CTRL`, `DRV_STATE_MGR` | Anchored | absorb `HAZARD/WINDOW/DRV_STATE`, keep `BODY_GW/AMBIENT` split first |
| `HVAC` | Body/Comfort | - | Placeholder | surface breadth only |
| `SMK` | Body/Comfort | - | Placeholder | surface breadth only |
| `AFLS` | Body/Comfort | - | Placeholder | surface breadth only |
| `LIGHTING_ECU` | Body/Comfort | - | Placeholder | surface breadth only |
| `WIPER_MODULE` | Body/Comfort | - | Placeholder | surface breadth only |
| `SUNROOF_MODULE` | Body/Comfort | - | Placeholder | surface breadth only |
| `DOOR_FL` | Body/Comfort | - | Placeholder | surface breadth only |
| `DOOR_FR` | Body/Comfort | - | Placeholder | surface breadth only |
| `TAILGATE_MODULE` | Body/Comfort | - | Placeholder | surface breadth only |
| `IVI` | IVI/HMI | `IVI_GW`, `NAV_CTX_MGR` | Anchored | keep `IVI_GW`, absorb `NAV_CTX_MGR` later |
| `CLUSTER` | IVI/HMI | `CLU_HMI_CTRL`, `CLU_BASE_CTRL` | Anchored | keep `CLU_HMI_CTRL`, absorb `CLU_BASE_CTRL` later |
| `HUD` | IVI/HMI | - | Placeholder | surface breadth only |
| `TMU` | IVI/HMI | - | Placeholder | deep-next placeholder, no active runtime yet |
| `AMP` | IVI/HMI | - | Placeholder | surface breadth only |
| `PGS` | IVI/HMI | - | Placeholder | surface breadth only |
| `NAV_MODULE` | IVI/HMI | - | Placeholder | represented inside `IVI` for now |
| `DIGITAL_KEY` | IVI/HMI | - | Placeholder | surface breadth only |
| `ADAS` | ADAS/V2X | `ADAS_WARN_CTRL`, `WARN_ARB_MGR` | Anchored | keep both runtimes split under one ADAS surface |
| `V2X` | ADAS/V2X | `EMS_POLICE_TX`, `EMS_AMB_TX`, `EMS_ALERT_RX` | Anchored | keep `EMS_ALERT_RX` as merge base, fold TX producers inward |
| `SCC` | ADAS/V2X | - | Placeholder | next deep candidate after ADAS/V2X cleanup |
| `LDWS_LKAS` | ADAS/V2X | - | Placeholder | surface breadth only |
| `FCA` | ADAS/V2X | - | Placeholder | surface breadth only |
| `BCW` | ADAS/V2X | - | Placeholder | surface breadth only |
| `LCA` | ADAS/V2X | - | Placeholder | surface breadth only |
| `SPAS` | ADAS/V2X | - | Placeholder | surface breadth only |
| `RSPA` | ADAS/V2X | - | Placeholder | surface breadth only |
| `AVM` | ADAS/V2X | - | Placeholder | surface breadth only |
| `FCAM` | ADAS/V2X | - | Placeholder | surface breadth only |

## B. Runtime-26 Assignment Table

| Active Runtime Node | CAPL Path | Assigned Surface ECU | Surface Bucket | Runtime Policy | Notes |
|---|---|---|---|---|---|
| `ENG_CTRL` | `ecu/ENG_CTRL.can` | `ECM` | Primary-56 | Keep split | already reads like a real engine ECU runtime |
| `TCM` | `ecu/TCM.can` | `TCM` | Primary-56 | Keep split | already production-like |
| `ACCEL_CTRL` | `ecu/ACCEL_CTRL.can` | `VCU` | Primary-56 | Keep split | rename surface first |
| `BRK_CTRL` | `ecu/BRK_CTRL.can` | `ESP` | Primary-56 | Keep split | brake/stability nucleus |
| `STEER_CTRL` | `ecu/STEER_CTRL.can` | `EPS` | Primary-56 | Keep split | steering nucleus |
| `CHS_GW` | `input/CHS_GW.can` | `CGW` | Primary-56 | Keep split | chassis ingress gateway |
| `INFOTAINMENT_GW` | `input/INFOTAINMENT_GW.can` | `CGW` | Primary-56 | Keep split | IVI ingress gateway |
| `DOMAIN_ROUTER` | `ecu/DOMAIN_ROUTER.can` | `CGW` | Primary-56 | Keep split | cross-domain routing owner |
| `DOMAIN_BOUNDARY_MGR` | `ecu/DOMAIN_BOUNDARY_MGR.can` | `SECURITY_GATEWAY` | Primary-56 | Keep split | best fit for boundary/security role |
| `ETH_SW` | `network/ETH_SW.can` | `ETH_BACKBONE` | Primary-56 | Keep split | backbone health/freshness monitor |
| `BODY_GW` | `output/BODY_GW.can` | `BCM` | Primary-56 | Keep split | internal BCM output module |
| `AMBIENT_CTRL` | `output/AMBIENT_CTRL.can` | `BCM` | Primary-56 | Keep split | internal BCM ambient module |
| `HAZARD_CTRL` | `ecu/HAZARD_CTRL.can` | `BCM` | Primary-56 | Merge candidate | absorb later into BCM runtime |
| `WINDOW_CTRL` | `ecu/WINDOW_CTRL.can` | `BCM` | Primary-56 | Merge candidate | absorb later into BCM runtime |
| `DRV_STATE_MGR` | `ecu/DRV_STATE_MGR.can` | `BCM` | Primary-56 | Merge candidate | placeholder-level body state runtime |
| `IVI_GW` | `output/IVI_GW.can` | `IVI` | Primary-56 | Keep split | internal IVI frame producer |
| `NAV_CTX_MGR` | `logic/NAV_CTX_MGR.can` | `IVI` | Primary-56 | Merge candidate | absorb later into IVI runtime |
| `CLU_HMI_CTRL` | `output/CLU_HMI_CTRL.can` | `CLUSTER` | Primary-56 | Keep split | main cluster runtime owner |
| `CLU_BASE_CTRL` | `ecu/CLU_BASE_CTRL.can` | `CLUSTER` | Primary-56 | Merge candidate | absorb later into cluster runtime |
| `ADAS_WARN_CTRL` | `logic/ADAS_WARN_CTRL.can` | `ADAS` | Primary-56 | Keep split | risk/trigger stage |
| `WARN_ARB_MGR` | `logic/WARN_ARB_MGR.can` | `ADAS` | Primary-56 | Keep split | arbitration stage |
| `EMS_POLICE_TX` | `ems/EMS_POLICE_TX.can` | `V2X` | Primary-56 | Merge candidate | fold into V2X producer stack |
| `EMS_AMB_TX` | `ems/EMS_AMB_TX.can` | `V2X` | Primary-56 | Merge candidate | fold into V2X producer stack |
| `EMS_ALERT_RX` | `logic/EMS_ALERT_RX.can` | `V2X` | Primary-56 | Keep split / merge base | nucleus for future single V2X runtime |
| `VAL_SCENARIO_CTRL` | `input/VAL_SCENARIO_CTRL.can` | `VALIDATION_HARNESS` | Secondary Validation | Keep split | non-production harness only |
| `VAL_BASELINE_CTRL` | `ecu/VAL_BASELINE_CTRL.can` | `VALIDATION_HARNESS` | Secondary Validation | Keep split | non-production harness only |

## C. Immediate Refactor Order

1. `BCM`
- absorb:
  - `HAZARD_CTRL`
  - `WINDOW_CTRL`
  - `DRV_STATE_MGR`
- keep split first:
  - `BODY_GW`
  - `AMBIENT_CTRL`

2. `IVI`
- absorb:
  - `NAV_CTX_MGR`
- keep split first:
  - `IVI_GW`

3. `CLUSTER`
- absorb:
  - `CLU_BASE_CTRL`
- keep split first:
  - `CLU_HMI_CTRL`

4. `V2X`
- absorb:
  - `EMS_POLICE_TX`
  - `EMS_AMB_TX`
- keep split first:
  - `EMS_ALERT_RX`

5. `ADAS`
- keep split first:
  - `ADAS_WARN_CTRL`
  - `WARN_ARB_MGR`
- do not merge before other folds stabilize

## D. Decision Rule

- If a runtime node has its own clear ECU identity, keep it split.
- If it is only an internal producer/consumer/helper under one parent ECU, absorb it.
- If it is gateway/backbone/boundary logic, keep it split but present it as infrastructure.
- If it is validation-only, keep it outside the production primary surface.

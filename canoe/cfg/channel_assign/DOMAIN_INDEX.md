# V2 Domain CAPL Index

This file documents domain-oriented CAPL ownership for the v2 runtime profile.

## Runtime SoT
- v2 runtime cfg: `canoe/cfg/CAN_v2_topology_wip.cfg`
- v2 runtime CAPL source: `canoe/cfg/channel_assign/**`
- shared sysvars: `canoe/project/sysvars/project.sysvars`
- mirrored CAPL tree: `canoe/src/capl/**` (must remain 1:1 synchronized)
- sync gate command: `python scripts/run.py gate capl-sync`

## Domain -> CAPL Files

### ETH_Backbone
- `ADAS_WARN_CTRL.can`
- `DOMAIN_BOUNDARY_MGR.can`
- `EMS_ALERT_RX.can`
- `EMS_AMB_TX.can`
- `EMS_POLICE_TX.can`
- `ETH_SW.can`
- `NAV_CTX_MGR.can`
- `VAL_SCENARIO_CTRL` (validation scenario controller)
- `WARN_ARB_MGR.can`

### Infotainment
- `CLU_BASE_CTRL.can`
- `CLU_HMI_CTRL.can`
- `INFOTAINMENT_GW.can`
- `IVI_GW.can`

### Body
- `AMBIENT_CTRL.can`
- `BODY_GW.can`
- `DRV_STATE_MGR.can`
- `HAZARD_CTRL.can`
- `WINDOW_CTRL.can`

### Powertrain
- `DOMAIN_ROUTER.can`
- `ENG_CTRL.can`
- `TCM.can`

### Chassis
- `ACCEL_CTRL.can`
- `BRK_CTRL.can`
- `CHS_GW.can`
- `STEER_CTRL.can`
- `VAL_BASELINE_CTRL` (validation baseline controller)

## Legacy Category Mirror (`src/capl`)
- `ecu`: vehicle/chassis/body/powertrain controller-side modules
- `ems`: emergency TX modules
- `input`: gateway ingress and test harness ingress modules
- `logic`: arbitration and warning logic modules
- `network`: backbone switch/transport monitoring module
- `output`: HMI/IVI/body output adapter modules

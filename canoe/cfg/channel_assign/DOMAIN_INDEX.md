# V2 Domain CAPL Index

This file documents domain-oriented CAPL ownership for the v2 runtime profile.

## Runtime SoT
- v2 runtime cfg: `canoe/cfg/CAN_v2_topology_wip.cfg`
- v2 runtime CAPL source: `canoe/cfg/channel_assign/**`
- shared sysvars: `canoe/project/sysvars/project.sysvars`
- legacy-style mirrored CAPL tree: `canoe/src/capl/**`

## Domain -> CAPL Files

### ETH_Backbone
- `ADAS_WARN_CTRL.can`
- `DOMAIN_BOUNDARY_MGR.can`
- `EMS_ALERT_RX.can`
- `EMS_AMB_TX.can`
- `EMS_POLICE_TX.can`
- `ETH_SWITCH.can`
- `NAV_CONTEXT_MGR.can`
- `SIL_TEST_CTRL.can`
- `WARN_ARB_MGR.can`

### Infotainment
- `CLUSTER_BASE_CTRL.can`
- `CLU_HMI_CTRL.can`
- `INFOTAINMENT_GW.can`
- `IVI_GW.can`

### Body
- `BCM_AMBIENT_CTRL.can`
- `BODY_GW.can`
- `DRIVER_STATE_CTRL.can`
- `HAZARD_CTRL.can`
- `WINDOW_CTRL.can`

### Powertrain
- `DOMAIN_GW_ROUTER.can`
- `ENGINE_CTRL.can`
- `TRANSMISSION_CTRL.can`

### Chassis
- `ACCEL_CTRL.can`
- `BRAKE_CTRL.can`
- `CHASSIS_GW.can`
- `STEERING_CTRL.can`
- `VEHICLE_BASE_TEST_CTRL.can`

## Legacy Category Mirror (`src/capl`)
- `ecu`: vehicle/chassis/body/powertrain controller-side modules
- `ems`: emergency TX modules
- `input`: gateway ingress and test harness ingress modules
- `logic`: arbitration and warning logic modules
- `network`: backbone switch/transport monitoring module
- `output`: HMI/IVI/body output adapter modules



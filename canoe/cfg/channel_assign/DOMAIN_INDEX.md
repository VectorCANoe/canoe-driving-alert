# V2 Domain CAPL Index

This file documents the active runtime CAPL inventory after wrapper absorption and OEM abbreviation normalization.

## Runtime SoT
- v2 runtime cfg: `canoe/cfg/CAN_v2_topology_wip.cfg`
- runtime source: `canoe/src/capl/**`
- GUI import mirror: `canoe/cfg/channel_assign/**`
- shared sysvars: `canoe/project/sysvars/project.sysvars`

## Active domain inventory

### ETH_Backbone
- `CGW.can`
- `ETHM.can`
- `V2X.can`
- `VAL_SCENARIO_CTRL.can`

### ADAS
- `ADAS.can`

### Infotainment
- `IVI.can`
- `CLU.can`

### Body
- `BCM.can`

### Powertrain
- `EMS.can`
- `TCU.can`
- `PTGW.can`

### Chassis
- `CHGW.can`
- `VCU.can`
- `ESC.can`
- `MDPS.can`
- `VAL_BASELINE_CTRL.can`

## Validation summary
- active runtime anchors: `14`
- validation-only nodes: `2`
- absorbed wrapper-only nodes left in active tree: `0`

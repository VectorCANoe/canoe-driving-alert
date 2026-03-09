# V2 Domain CAPL Index

This file documents the visible runtime and placeholder CAPL inventory after wrapper absorption and OEM abbreviation normalization.

## Runtime SoT
- v2 runtime cfg: `canoe/cfg/CAN_v2_topology_wip.cfg`
- runtime source: `canoe/src/capl/**`
- GUI import mirror: `canoe/cfg/channel_assign/**`
- shared sysvars: `canoe/project/sysvars/project.sysvars`

## Visible domain inventory

### ETH_Backbone
- `CGW.can`
- `V2X.can`
- `VAL_SCENARIO_CTRL.can`
- `ETH_BACKBONE.can`
- `DCM.can`
- `IBOX.can`
- `SECURITY_GATEWAY.can`
- `EDGE_LOGGER.can`

### ADAS
- `ADAS.can`
- `SCC.can`
- `LDWS_LKAS.can`
- `FCA.can`
- `BCW.can`
- `LCA.can`
- `SPAS.can`
- `RSPA.can`
- `AVM.can`
- `FCAM.can`
- `FRADAR.can`
- `SRR_FL.can`
- `SRR_FR.can`
- `SRR_RL.can`
- `SRR_RR.can`
- `PARK_ULTRASONIC.can`
- `DMS.can`
- `OMS.can`
- `AEB_DOMAIN.can`
- `PARK_MASTER.can`
- `ROAD_PREVIEW_CAMERA.can`
- `LIDAR.can`
- `REAR_RADAR_MASTER.can`
- `SURROUND_PARK_MASTER.can`
- `HIGHWAY_PILOT.can`
- `TRAILER_CTRL.can`

### Infotainment
- `IVI.can`
- `CLU.can`
- `HUD.can`
- `TMU.can`
- `AMP.can`
- `PGS.can`
- `NAV_MODULE.can`
- `VOICE_ASSIST.can`
- `RSE.can`
- `DIGITAL_KEY.can`
- `CARPAY_CTRL.can`
- `PHONE_AS_KEY.can`
- `OTA_MASTER.can`

### Body
- `BCM.can`
- `HVAC.can`
- `SMK.can`
- `AFLS.can`
- `LIGHTING_ECU.can`
- `WIPER_MODULE.can`
- `SUNROOF_MODULE.can`
- `DOOR_FL.can`
- `DOOR_FR.can`
- `DOOR_RL.can`
- `DOOR_RR.can`
- `TAILGATE_MODULE.can`
- `SEAT_DRV.can`
- `SEAT_PASS.can`
- `MIRROR_MODULE.can`
- `BODY_SECURITY_MODULE.can`
- `HEADLAMP_LEVELING.can`
- `AUTO_DOOR_CTRL.can`
- `POWER_TAILGATE_CTRL.can`
- `MASSAGE_SEAT_CTRL.can`
- `REAR_CLIMATE_MODULE.can`
- `CABIN_SENSING.can`
- `BIOMETRIC_AUTH.can`

### Powertrain
- `EMS.can`
- `TCU.can`
- `AWD_4WD.can`
- `BAT_BMS.can`
- `FPCM.can`
- `LVR.can`
- `ISG.can`
- `EOP.can`
- `EWP.can`
- `OBC.can`
- `DCDC.can`
- `MCU.can`
- `INVERTER.can`
- `CHARGE_PORT_CTRL.can`

### Chassis
- `VCU.can`
- `ESC.can`
- `MDPS.can`
- `VAL_BASELINE_CTRL.can`
- `ABS.can`
- `EPB.can`
- `TPMS.can`
- `SAS.can`
- `ECS.can`
- `ACU.can`
- `ODS.can`
- `VSM.can`
- `EHB.can`
- `CDC.can`
- `AIR_SUSPENSION.can`
- `RWS.can`

## Validation summary
- deep runtime anchors: `13`
- validation-only nodes: `2`
- placeholder surface nodes: `87`
- total visible nodes: `100`

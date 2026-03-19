# DBC Comparison Report: generated_script vs manual_curated

- Generated set: `canoe/tmp/dbc_compare/generated_script`
- Manual set: `canoe/tmp/dbc_compare/manual_curated`

## emergency_system.dbc

- Text lines: generated=143, manual=155
- Node count: generated=13, manual=25
- Message count: generated=6, manual=6

### Structural differences
- Manual-only nodes: ACCEL_CTRL, BRAKE_CTRL, CLUSTER_BASE_CTRL, DOMAIN_BOUNDARY_MGR, DOMAIN_GW_ROUTER, DRIVER_STATE_CTRL, ENGINE_CTRL, HAZARD_CTRL, STEERING_CTRL, TRANSMISSION_CTRL, VEHICLE_BASE_TEST_CTRL, WINDOW_CTRL
- ID 0x110: signal Reserved1 missing in manual
- ID 0x110: signal gSpeedLimit differs gen(start=16,len=2,min=0,max=255) manual(start=16,len=8,min=0,max=255)

### Text diff (first 80 lines)
```diff
--- generated/emergency_system.dbc
+++ manual/emergency_system.dbc
@@ -29,7 +29,7 @@
 
 BS_:
 
-BU_: SIL_TEST_CTRL CHASSIS_GW Vector__XXX INFOTAINMENT_GW BODY_GW BCM_AMBIENT_CTRL IVI_GW CLU_HMI_CTRL EMS_POLICE_TX EMS_AMB_TX EMS_ALERT_RX WARN_ARB_MGR NAV_CONTEXT_MGR
+BU_: SIL_TEST_CTRL CHASSIS_GW INFOTAINMENT_GW EMS_POLICE_TX EMS_AMB_TX EMS_ALERT_RX WARN_ARB_MGR BODY_GW IVI_GW BCM_AMBIENT_CTRL CLU_HMI_CTRL ENGINE_CTRL TRANSMISSION_CTRL ACCEL_CTRL BRAKE_CTRL STEERING_CTRL HAZARD_CTRL WINDOW_CTRL DRIVER_STATE_CTRL NAV_CONTEXT_MGR CLUSTER_BASE_CTRL VEHICLE_BASE_TEST_CTRL DOMAIN_GW_ROUTER DOMAIN_BOUNDARY_MGR Vector__XXX
 
 BO_ 256 frmVehicleStateCanMsg: 2 SIL_TEST_CTRL
  SG_ gVehicleSpeed    : 0|8@1+ (1,0) [0|255] "km/h" CHASSIS_GW
@@ -45,8 +45,7 @@
  SG_ gNavDirection    : 2|2@1+ (1,0) [0|3] "" INFOTAINMENT_GW
  SG_ Reserved0        : 4|4@1+ (1,0) [0|0] "" Vector__XXX
  SG_ gZoneDistance    : 8|8@1+ (1,0) [0|255] "m" INFOTAINMENT_GW
- SG_ gSpeedLimit      : 16|2@1+ (1,0) [0|255] "km/h" INFOTAINMENT_GW
- SG_ Reserved1        : 18|6@1+ (1,0) [0|0] "" Vector__XXX
+ SG_ gSpeedLimit      : 16|8@1+ (1,0) [0|255] "km/h" INFOTAINMENT_GW
 
 BO_ 528 frmAmbientControlMsg: 1 BODY_GW
  SG_ AmbientMode      : 0|3@1+ (1,0) [0|7] "" BCM_AMBIENT_CTRL
@@ -60,19 +59,31 @@
  SG_ ScenarioResult   : 0|1@1+ (1,0) [0|1] "" Vector__XXX
  SG_ Reserved0        : 1|7@1+ (1,0) [0|0] "" Vector__XXX
 
-CM_ BU_ SIL_TEST_CTRL "SIL test controller for CAN input injection and scenario result logging.";
-CM_ BU_ CHASSIS_GW "Gateway: Chassis CAN input normalization to core variables.";
-CM_ BU_ Vector__XXX "Reserved node for unused or filler signals.";
-CM_ BU_ INFOTAINMENT_GW "Gateway: Infotainment CAN input normalization to core variables.";
-CM_ BU_ BODY_GW "Gateway: selected alert to Body CAN (0x210).";
-CM_ BU_ BCM_AMBIENT_CTRL "Ambient controller ECU (consumer of 0x210).";
-CM_ BU_ IVI_GW "Gateway: selected alert to Infotainment CAN (0x220).";
-CM_ BU_ CLU_HMI_CTRL "Cluster HMI ECU (consumer of 0x220).";
-CM_ BU_ EMS_POLICE_TX "Emergency producer node (Police) on Ethernet domain contract.";
-CM_ BU_ EMS_AMB_TX "Emergency producer node (Ambulance) on Ethernet domain contract.";
-CM_ BU_ EMS_ALERT_RX "Emergency receiver/timeout monitor for arbitration.";
-CM_ BU_ WARN_ARB_MGR "Central arbitration manager (Emergency vs Navigation context).";
-CM_ BU_ NAV_CONTEXT_MGR "Navigation context manager node.";
+CM_ BU_ SIL_TEST_CTRL       "SIL test controller for CAN input injection and scenario result logging.";
+CM_ BU_ CHASSIS_GW          "Gateway: Chassis CAN input normalization to core variables.";
+CM_ BU_ INFOTAINMENT_GW     "Gateway: Infotainment CAN input normalization to core variables.";
+CM_ BU_ EMS_POLICE_TX       "Emergency producer node (Police) on Ethernet domain contract.";
+CM_ BU_ EMS_AMB_TX          "Emergency producer node (Ambulance) on Ethernet domain contract.";
+CM_ BU_ EMS_ALERT_RX        "Emergency receiver/timeout monitor for arbitration.";
+CM_ BU_ WARN_ARB_MGR        "Central arbitration manager (Emergency vs Navigation context).";
+CM_ BU_ BODY_GW             "Gateway: selected alert to Body CAN (0x210).";
+CM_ BU_ IVI_GW              "Gateway: selected alert to Infotainment CAN (0x220).";
+CM_ BU_ BCM_AMBIENT_CTRL    "Ambient controller ECU (consumer of 0x210).";
+CM_ BU_ CLU_HMI_CTRL        "Cluster HMI ECU (consumer of 0x220).";
+CM_ BU_ ENGINE_CTRL         "Vehicle baseline node for ignition and engine-state handling (Req_101).";
+CM_ BU_ TRANSMISSION_CTRL   "Vehicle baseline node for gear-state handling (Req_102).";
+CM_ BU_ ACCEL_CTRL          "Vehicle baseline node for acceleration pedal handling (Req_103).";
+CM_ BU_ BRAKE_CTRL          "Vehicle baseline node for brake pedal handling (Req_104).";
+CM_ BU_ STEERING_CTRL       "Vehicle baseline node for steering handling (Req_105).";
+CM_ BU_ HAZARD_CTRL         "Vehicle baseline node for hazard switch handling (Req_106).";
+CM_ BU_ WINDOW_CTRL         "Vehicle baseline node for window state handling (Req_107).";
+CM_ BU_ DRIVER_STATE_CTRL   "Vehicle baseline node for driver-state forwarding (Req_108).";
+CM_ BU_ NAV_CONTEXT_MGR     "Navigation context manager node (Flow_003 owner).";
+CM_ BU_ CLUSTER_BASE_CTRL   "Vehicle baseline cluster display node (Req_109).";
+CM_ BU_ VEHICLE_BASE_TEST_CTRL "Vehicle baseline SIL test control node (Req_112).";
+CM_ BU_ DOMAIN_GW_ROUTER    "Domain gateway routing manager (Req_110).";
+CM_ BU_ DOMAIN_BOUNDARY_MGR "Domain boundary policy manager (Req_111).";
+CM_ BU_ Vector__XXX         "Reserved node for unused or filler signals.";
 
 CM_ BO_ 256 "Chassis CAN input: vehicle speed and drive state.";
 CM_ BO_ 257 "Chassis CAN input: steering input state.";
@@ -82,6 +93,7 @@
 CM_ BO_ 560 "Scenario pass/fail result for SIL traceability.";
 
 CM_ "Scope: This DBC defines CAN-domain frames only. Ethernet contracts (E100/E200, 0x510/0x511/0x512) are maintained in CAPL/sysvar interface specifications.";
+CM_ "Post-mentoring alignment: node inventory expanded to include Req_101~Req_112 baseline architecture.";
 
 BA_DEF_ BO_ "GenMsgCycleTime" INT 0 10000;
 BA_DEF_DEF_ "GenMsgCycleTime" 0;
```

## emergency_system_body.dbc

- Text lines: generated=72, manual=73
- Node count: generated=7, manual=7
- Message count: generated=1, manual=1

### Structural differences
- None

### Text diff (first 80 lines)
```diff
--- generated/emergency_system_body.dbc
+++ manual/emergency_system_body.dbc
@@ -29,24 +29,25 @@
 
 BS_:
 
-BU_: BODY_GW BCM_AMBIENT_CTRL HAZARD_CTRL WINDOW_CTRL DRIVER_STATE_CTRL WARN_ARB_MGR Vector__XXX
+BU_: BODY_GW BCM_AMBIENT_CTRL WARN_ARB_MGR HAZARD_CTRL WINDOW_CTRL DRIVER_STATE_CTRL Vector__XXX
 
 BO_ 528 frmAmbientControlMsg: 1 BODY_GW
  SG_ AmbientMode      : 0|3@1+ (1,0) [0|7] "" BCM_AMBIENT_CTRL
  SG_ AmbientColor     : 3|3@1+ (1,0) [0|7] "" BCM_AMBIENT_CTRL
  SG_ AmbientPattern   : 6|2@1+ (1,0) [0|3] "" BCM_AMBIENT_CTRL
 
-CM_ BU_ BODY_GW "Gateway: selected alert to Body CAN (0x210).";
+CM_ BU_ BODY_GW          "Gateway: selected alert to Body CAN (0x210).";
 CM_ BU_ BCM_AMBIENT_CTRL "Ambient controller ECU (consumer of 0x210).";
-CM_ BU_ HAZARD_CTRL "Baseline vehicle function node for hazard switch handling.";
-CM_ BU_ WINDOW_CTRL "Baseline vehicle function node for window command handling.";
-CM_ BU_ DRIVER_STATE_CTRL "Baseline vehicle function node for driver-state forwarding.";
-CM_ BU_ WARN_ARB_MGR "Central arbitration manager (Emergency vs Navigation context).";
-CM_ BU_ Vector__XXX "Reserved node for unused or filler signals.";
+CM_ BU_ WARN_ARB_MGR     "Central arbitration manager (upstream logic owner).";
+CM_ BU_ HAZARD_CTRL      "Vehicle baseline node for hazard switch handling (Req_106).";
+CM_ BU_ WINDOW_CTRL      "Vehicle baseline node for window state handling (Req_107).";
+CM_ BU_ DRIVER_STATE_CTRL "Vehicle baseline node for driver-state forwarding (Req_108).";
+CM_ BU_ Vector__XXX      "Reserved node for unused or filler signals.";
 
 CM_ BO_ 528 "Body CAN output: ambient mode/color/pattern.";
 
 CM_ "Domain split: body CAN network from emergency_system.dbc baseline.";
+CM_ "Post-mentoring alignment: body domain includes baseline hazard/window/driver-state nodes.";
 
 BA_DEF_ BO_ "GenMsgCycleTime" INT 0 10000;
 BA_DEF_DEF_ "GenMsgCycleTime" 0;
```

## emergency_system_chassis.dbc

- Text lines: generated=83, manual=84
- Node count: generated=7, manual=7
- Message count: generated=3, manual=3

### Structural differences
- None

### Text diff (first 80 lines)
```diff
--- generated/emergency_system_chassis.dbc
+++ manual/emergency_system_chassis.dbc
@@ -29,7 +29,7 @@
 
 BS_:
 
-BU_: SIL_TEST_CTRL CHASSIS_GW Vector__XXX ACCEL_CTRL BRAKE_CTRL STEERING_CTRL VEHICLE_BASE_TEST_CTRL
+BU_: SIL_TEST_CTRL CHASSIS_GW ACCEL_CTRL BRAKE_CTRL STEERING_CTRL VEHICLE_BASE_TEST_CTRL Vector__XXX
 
 BO_ 256 frmVehicleStateCanMsg: 2 SIL_TEST_CTRL
  SG_ gVehicleSpeed    : 0|8@1+ (1,0) [0|255] "km/h" CHASSIS_GW
@@ -45,18 +45,19 @@
  SG_ Reserved0        : 1|7@1+ (1,0) [0|0] "" Vector__XXX
 
 CM_ BU_ SIL_TEST_CTRL "SIL test controller for CAN input injection and scenario result logging.";
-CM_ BU_ CHASSIS_GW "Gateway: Chassis CAN input normalization to core variables.";
-CM_ BU_ Vector__XXX "Reserved node for unused or filler signals.";
-CM_ BU_ ACCEL_CTRL "Baseline vehicle function node for acceleration input handling.";
-CM_ BU_ BRAKE_CTRL "Baseline vehicle function node for brake input handling.";
-CM_ BU_ STEERING_CTRL "Baseline vehicle function node for steering input handling.";
-CM_ BU_ VEHICLE_BASE_TEST_CTRL "Baseline SIL test controller for vehicle basic functions.";
+CM_ BU_ CHASSIS_GW    "Gateway: Chassis CAN input normalization to core variables.";
+CM_ BU_ ACCEL_CTRL    "Vehicle baseline node for acceleration pedal handling (Req_103).";
+CM_ BU_ BRAKE_CTRL    "Vehicle baseline node for brake pedal handling (Req_104).";
+CM_ BU_ STEERING_CTRL "Vehicle baseline node for steering handling (Req_105).";
+CM_ BU_ VEHICLE_BASE_TEST_CTRL "Vehicle baseline SIL test control node (Req_112).";
+CM_ BU_ Vector__XXX   "Reserved node for unused or filler signals.";
 
 CM_ BO_ 256 "Chassis CAN input: vehicle speed and drive state.";
 CM_ BO_ 257 "Chassis CAN input: steering input state.";
 CM_ BO_ 560 "Scenario pass/fail result for SIL traceability.";
 
 CM_ "Domain split: chassis CAN network from emergency_system.dbc baseline.";
+CM_ "Post-mentoring alignment: domain node set expanded with Req_101~Req_112 baseline nodes.";
 
 BA_DEF_ BO_ "GenMsgCycleTime" INT 0 10000;
 BA_DEF_DEF_ "GenMsgCycleTime" 0;
```

## emergency_system_infotainment.dbc

- Text lines: generated=76, manual=76
- Node count: generated=7, manual=7
- Message count: generated=2, manual=2

### Structural differences
- ID 0x110: signal Reserved1 missing in manual
- ID 0x110: signal gSpeedLimit differs gen(start=16,len=2,min=0,max=255) manual(start=16,len=8,min=0,max=255)

### Text diff (first 80 lines)
```diff
--- generated/emergency_system_infotainment.dbc
+++ manual/emergency_system_infotainment.dbc
@@ -29,31 +29,31 @@
 
 BS_:
 
-BU_: SIL_TEST_CTRL INFOTAINMENT_GW Vector__XXX IVI_GW CLU_HMI_CTRL NAV_CONTEXT_MGR CLUSTER_BASE_CTRL
+BU_: SIL_TEST_CTRL INFOTAINMENT_GW IVI_GW CLU_HMI_CTRL NAV_CONTEXT_MGR CLUSTER_BASE_CTRL Vector__XXX
 
 BO_ 272 frmNavContextCanMsg: 3 SIL_TEST_CTRL
  SG_ gRoadZone        : 0|2@1+ (1,0) [0|3] "" INFOTAINMENT_GW
  SG_ gNavDirection    : 2|2@1+ (1,0) [0|3] "" INFOTAINMENT_GW
  SG_ Reserved0        : 4|4@1+ (1,0) [0|0] "" Vector__XXX
  SG_ gZoneDistance    : 8|8@1+ (1,0) [0|255] "m" INFOTAINMENT_GW
- SG_ gSpeedLimit      : 16|2@1+ (1,0) [0|255] "km/h" INFOTAINMENT_GW
- SG_ Reserved1        : 18|6@1+ (1,0) [0|0] "" Vector__XXX
+ SG_ gSpeedLimit      : 16|8@1+ (1,0) [0|255] "km/h" INFOTAINMENT_GW
 
 BO_ 544 frmClusterWarningMsg: 1 IVI_GW
  SG_ WarningTextCode  : 0|8@1+ (1,0) [0|255] "" CLU_HMI_CTRL
 
-CM_ BU_ SIL_TEST_CTRL "SIL test controller for CAN input injection and scenario result logging.";
+CM_ BU_ SIL_TEST_CTRL   "SIL test controller for CAN input injection.";
 CM_ BU_ INFOTAINMENT_GW "Gateway: Infotainment CAN input normalization to core variables.";
-CM_ BU_ Vector__XXX "Reserved node for unused or filler signals.";
-CM_ BU_ IVI_GW "Gateway: selected alert to Infotainment CAN (0x220).";
-CM_ BU_ CLU_HMI_CTRL "Cluster HMI ECU (consumer of 0x220).";
-CM_ BU_ NAV_CONTEXT_MGR "Navigation context manager node.";
-CM_ BU_ CLUSTER_BASE_CTRL "Cluster baseline display manager node.";
+CM_ BU_ IVI_GW          "Gateway: selected alert to Infotainment CAN (0x220).";
+CM_ BU_ CLU_HMI_CTRL    "Cluster HMI ECU (consumer of 0x220).";
+CM_ BU_ NAV_CONTEXT_MGR "Navigation context manager node (Flow_003 owner).";
+CM_ BU_ CLUSTER_BASE_CTRL "Vehicle baseline cluster display node (Req_109).";
+CM_ BU_ Vector__XXX     "Reserved node for unused or filler signals.";
 
 CM_ BO_ 272 "Infotainment CAN input: road zone, direction, distance, and speed limit.";
 CM_ BO_ 544 "Infotainment CAN output: cluster warning text code.";
 
 CM_ "Domain split: infotainment CAN network from emergency_system.dbc baseline.";
+CM_ "Post-mentoring alignment: infotainment domain node set expanded for baseline cluster context.";
 
 BA_DEF_ BO_ "GenMsgCycleTime" INT 0 10000;
 BA_DEF_DEF_ "GenMsgCycleTime" 0;
```

## emergency_system_powertrain.dbc

- Text lines: generated=41, manual=42
- Node count: generated=4, manual=5
- Message count: generated=0, manual=0

### Structural differences
- Manual-only nodes: SIL_TEST_CTRL

### Text diff (first 80 lines)
```diff
--- generated/emergency_system_powertrain.dbc
+++ manual/emergency_system_powertrain.dbc
@@ -29,13 +29,14 @@
 
 BS_:
 
-BU_: ENGINE_CTRL TRANSMISSION_CTRL DOMAIN_GW_ROUTER Vector__XXX
+BU_: SIL_TEST_CTRL ENGINE_CTRL TRANSMISSION_CTRL DOMAIN_GW_ROUTER Vector__XXX
 
-CM_ BU_ ENGINE_CTRL "Baseline vehicle function node for ignition/engine state handling.";
-CM_ BU_ TRANSMISSION_CTRL "Baseline vehicle function node for gear state handling.";
-CM_ BU_ DOMAIN_GW_ROUTER "Domain gateway router for inter-domain frame routing policy.";
+CM_ BU_ SIL_TEST_CTRL "SIL test controller (powertrain-domain CAN input reserved).";
+CM_ BU_ ENGINE_CTRL "Vehicle baseline node for ignition and engine-state handling (Req_101).";
+CM_ BU_ TRANSMISSION_CTRL "Vehicle baseline node for gear-state handling (Req_102).";
+CM_ BU_ DOMAIN_GW_ROUTER "Domain gateway routing manager (Req_110).";
 CM_ BU_ Vector__XXX "Reserved node for unused or filler signals.";
 
 CM_ "Domain split: powertrain CAN network from emergency_system.dbc baseline.";
-CM_ "Current baseline has no dedicated powertrain CAN frame.";
-CM_ "Reserved for engine/gear/brake related CAN frames from Req_101~Req_112 expansion.";
+CM_ "Current baseline has no dedicated powertrain CAN frame. This file is reserved for expansion (engine/gear/brake related frames).";
+CM_ "Post-mentoring alignment target: Req_101~Req_112 expansion frames to be added after 0302/0303 comm IDs are finalized.";
```


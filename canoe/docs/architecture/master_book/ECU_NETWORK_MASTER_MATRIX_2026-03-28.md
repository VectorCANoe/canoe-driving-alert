# ECU Network Master Matrix (2026-03-28)

## Purpose

This is an internal engineering matrix for reading the live CANoe runtime as a coupled ECU network.

It bridges four official SoT documents that are correct individually but harder to read as one runtime picture:

- `0301_SysFuncAnalysis.md`: ECU responsibility
- `0302_NWflowDef.md`: ECU-by-message Tx/Rx surface
- `0303_Communication_Specification.md`: signal meaning
- `0304_System_Variables.md`: internal sysvar/state seams

This matrix is intentionally ECU-centric and runtime-centric.

## Source Priority

1. `canoe/src/capl/**/*.can`
2. `scripts/gates/check_runtime_seam_ownership.py`
3. `canoe/tests/modules/test_units/**`
4. `driving-alert-workproducts/0301~0304`
5. `canoe/docs/contracts/**` and `canoe/docs/verification/**`

## Inventory Basis

- Runtime node source: `canoe/src/capl/**/*.can`
- Current runtime node count: `101`
- Test-unit directory count: `171`
- Surface breadth reference: `OEM_100_ECU_PROGRAM_BANK_2026-03-09.md`
- Layer reference: `OEM_4_LAYER_ECU_CLASSIFICATION_2026-03-10.md`

## A. Core Coupled ECU Matrix

These are the nodes that currently matter most for dynamics, alert arbitration, display/output, and the input-console runtime path.

| ECU | Layer / Role | Owner / primary seam | Primary Rx message(s) | Primary Tx message(s) | Linked ECU(s) | Primary sysvar / readback | Representative test asset | Primary doc source | Current gap / risk |
|---|---|---|---|---|---|---|---|---|---|
| `VCU` | Powertrain controller | `Chassis::vehicleSpeed`, `Chassis::driveState`, `Chassis::throttlePosition` | `frmPedalInputCanMsg`, `frmGearStateMsg`, `frmNavModuleStateMsg`, `frmWheelSpeedMsg`, `frmIgnitionEngineMsg` | `frmVehicleStateCanMsg`, `frmAccelStatusMsg`, `frmWheelPulseMsg` | `NAV`, `CGW`, `ADAS`, `IVI`, `ESC`, `TCU`, `EMS`, `TEST_SCN` | `@Chassis::vehicleSpeed`, `@Chassis::driveState`, `@Chassis::throttlePosition` | `TC_CANOE_IT_020_POWERTRAIN_DRIVE_BASELINE`, `TC_CANOE_UT_EXT_017_CHS_DYNAMICS_EXT` | `0301`, `0302`, `0303`, `04_SW_Implementation` | Manual speed target and pedal dynamics can still fight if cross-domain assist logic reasserts stale hints. |
| `ESC` | Chassis brake controller | `Chassis::brakePressure`, `Chassis::brakeLamp`, `Chassis::absActive` | `frmVehicleStateCanMsg`, `frmPedalInputCanMsg`, `frmAebDomainStateMsg` | `frmBrakeStatusMsg`, `frmEscStateMsg`, `frmWheelSpeedMsg`, `frmYawAccelMsg` | `VCU`, `MDPS`, `ADAS`, `EHB`, `VSM`, `CGW` | `@Chassis::brakePressure`, `@Chassis::brakeLamp` | `TC_CANOE_IT_022_CHASSIS_BRAKE_BASELINE`, `TC_CANOE_UT_EXT_016_CHS_BRAKE_EXT` | `0301`, `0302`, `0303`, `04_SW_Implementation` | `assistPressureFloor` is the strongest current dynamics risk. |
| `MDPS` | Chassis steering controller | steering state / steering torque | `frmVehicleStateCanMsg`, steering state inputs | `frmSteeringTorqueMsg`, `frmEpsStateMsg` | `CGW`, `ADAS`, `CLU` | `@Chassis::steeringAngle`, `@Display::steeringFrame` | `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE`, `TC_CANOE_UT_INP_028_VEHICLE_STEERING` | `0301`, `0302`, `0303` | Steering path is mostly coherent after command/readback unification. |
| `CGW` | Central gateway / gatekeeper | `CoreState::selectedAlertGateReason`, boundary/failsafe state | `frmVehicleStateCanMsg`, `frmBodyGatewayStateMsg`, health/failsafe inputs | domain route / gateway status outputs | `ADAS`, `IVI`, `BCM`, `CLU`, `VCU`, `EMS`, `TCU` | `@CoreState::selectedAlertGateReason` | `TC_CANOE_UT_CORE_001_CGW_CHS_GW`, `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW`, `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` | `0301`, `0302`, `04_SW_Implementation` | Gateway ownership is clean, but many downstream behaviors depend on its gate reason. |
| `ADAS` | Alert arbitration / decel assist | `Core::selectedAlertType`, ADAS decision seams | `frmVehicleStateCanMsg`, `frmBrakeStatusMsg`, route context, V2X/perception inputs | ADAS domain state, decel assist request, selected alert decision | `CGW`, `AEB`, `IVI`, `BCM`, `CLU`, `AMP`, `SCC` | selected alert decision / effective state seams | `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST`, `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION`, `TC_CANOE_IT_EXT_039_ADAS_PERCEPTION_CONTEXT` | `0301`, `0302`, `0303`, `04_SW_Implementation` | Needs to be read together with `AEB`, not in isolation. |
| `SCC` | Longitudinal assist support | longitudinal assist state | vehicle state / path / distance context | SCC support state for ADAS | `ADAS`, `VCU` | SCC-related assist state seams | `TC_CANOE_UT_INP_052_SCC_INPUT` | `0301`, `04_SW_Implementation` | Support-state coupling matters more than standalone bus ownership. |
| `V2X` | Emergency ingress / V2X alert | emergency ingress context, V2X animation/output seams | emergency ingress sources / context inputs | V2X alert outputs, ingress state | `ADAS`, `IVI`, `BCM`, `AMP` | `V2X::v2xFrame`, `V2X::MyCarFrame`, `V2X::AmbFrame` | `TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN` | `0301`, `0302`, `0303` | External ingress is stable; arbitration happens later in ADAS/CGW. |
| `AEB` | AEB domain controller | `frmAebDomainStateMsg` | `frmFcaStateMsg`, `frmAdasDomainStateMsg` | `frmAebDomainStateMsg` | `ADAS`, `FCA`, `ESC`, `EHB`, `VSM` | StopReq / DecelProfile / DomainHealth path | `TC_CANOE_ST_EXT_022_INTERSECTION_DECEL`, `TC_CANOE_ST_EXT_023_MERGE_DECEL` | `0302`, `0303`, runtime code | This is the main source of brake-step behavior. |
| `EHB` | Brake assist leaf | local AEB pressure command | `frmBrakeStatusMsg`, `frmAebDomainStateMsg` | local assist/brake state | `ESC`, `VSM` | local brake assist state | `TC_CANOE_UT_INP_032_EHB_INPUT` | `0301`, runtime code | Coupled consumer; reacts to the same AEB profile as `ESC`. |
| `VSM` | Stability intervention leaf | intervention / control state | `frmEscStateMsg`, `frmAebDomainStateMsg`, `frmVehicleStateCanMsg` | local stability/intervention state | `ESC`, `EHB`, `AEB` | local intervention state | `TC_CANOE_UT_INP_033_VSM_INPUT` | `0301`, runtime code | Shares the same decel profile thresholds; contributes to perceived brake pulse. |
| `IVI` | HMI/domain display gateway | text/render route state | `frmVehicleStateCanMsg`, route context, selected alert state | cluster warning/base display, map/service outputs | `CGW`, `CLU`, `AMP`, `BCM`, `NAV`, `TMU` | `Cluster::warningTextCode`, IVI display/output seams | `TC_CANOE_UT_CORE_013_IVI_GW_ROUTE`, `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING`, `TC_CANOE_UT_OUT_071_IVI_HMI` | `0301`, `0302`, `0303`, `04_SW_Implementation` | Display path is structurally sound; problems are usually upstream. |
| `BCM` | Body / ambient owner | body comfort and ambient outputs | body control/state inputs, selected alert state | ambient, lamp, window, door state outputs | `IVI`, `CGW`, `CLU`, `AMP`, body leaf ECUs | `Body::blinkLeft`, `Body::blinkRight`, `Body::frontWiperAnimFrame`, `Body::ambientMode` | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY`, `TC_CANOE_UT_OUT_070_BCM_AMBIENT`, `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` | `0301`, `0302`, `0303`, `0304` | Ambient and comfort breadth are wider than the current input-console surface. |
| `CLU` | Cluster owner | cluster warning/base display | selected alert state, vehicle state | `warningTextCode`, cluster base state, steering frame | `IVI`, `CGW`, `MDPS`, `VCU` | `Cluster::warningTextCode`, `Display::steeringFrame` | `TC_CANOE_UT_OUT_072_CLU_DISPLAY`, `TC_CANOE_UT_EXT_007_CLU_CONTEXT_ADJUST` | `0301`, `0302`, `0303` | Output ownership is clean. |
| `AMP` | Audio output owner | render volume / audio output | selected alert state, IVI audio focus | rendered volume/audio output | `IVI`, `BCM` | `UiRender::renderVolumLevel`, `CoreState::baseVolume` | `TC_CANOE_UT_OUT_074_AMP_AUDIO` | `0301`, `0302`, `0303` | Audio path is stable; alert priority path matters more than bus mapping. |
| `TEST_SCN` | Validation / scenario harness | `Test::*` scenario control | Input-console scenario commands | scenario result / ack / lock state | all scenario-aware ECUs | `Test::scenarioCommand`, `Test::scenarioActiveId`, `Test::scenarioResult` | scenario and baseline IT/ST suites | `0301` note, panel/runtime contracts | Should stay scenario-focused; not a general product owner. |
| `TEST_BAS` | Validation / baseline harness | validation routing / summary | general validation inputs, panel router include | baseline summary / compat outputs | `VCU`, `ESC`, `IVI`, `BCM`, validation outputs | validation summary seams | baseline UT/IT/ST suites | runtime contracts, validation docs | Keep separated from production ownership. |

## B. 101-Node Runtime Bank By Layer

This section freezes the current `101` compileable runtime anchors as the internal breadth baseline.
Detailed Rx/Tx fill should prioritize the core coupled nodes above first, then extend outward by layer.

### Layer 1. Central Gateway / Backbone / Validation

| Node set | Notes |
|---|---|
| `CGW`, `ETHB`, `DCM`, `IBOX`, `SGW`, `EDR` | central gateway, backbone service, diagnostic/security edge |
| `EXT_DIAG` | external diagnostic observation surface |
| `TEST_BAS`, `TEST_SCN` | validation-only nodes; keep separate from product ECU ownership |

### Layer 2. Domain Controller / Primary Runtime Anchors

| Node set | Notes |
|---|---|
| `EMS`, `TCU`, `VCU` | powertrain anchors |
| `ESC`, `MDPS` | chassis control anchors |
| `BCM`, `DATC` | body/comfort anchors |
| `IVI`, `CLU`, `TMU` | HMI/display/connectivity anchors |
| `ADAS`, `SCC`, `V2X` | warning/arbitration/support anchors |

### Layer 3. Leaf / Feature / Local Runtime Surfaces

| Domain | Node set |
|---|---|
| Powertrain / electrical | `_4WD`, `BAT_BMS`, `FPCM`, `LVR`, `ISG`, `EOP`, `EWP`, `OBC`, `DCDC`, `MCU`, `INVERTER`, `CPC` |
| Chassis / safety | `ABS`, `EPB`, `TPMS`, `SAS`, `ECS`, `ACU`, `ODS`, `VSM`, `EHB`, `CDC`, `ASM`, `RWS` |
| Body / comfort | `SMK`, `AFLS`, `AHLS`, `WIP`, `SRF`, `DOOR_FL`, `DOOR_FR`, `DOOR_RL`, `DOOR_RR`, `TGM`, `SEAT_DRV`, `SEAT_PASS`, `MIR`, `BSEC`, `RATC`, `HLM`, `CSM`, `ADM`, `PTG`, `BIO`, `MSC` |
| IVI / service | `HUD`, `AMP`, `PGS`, `NAV`, `VCS`, `RSE`, `DKEY`, `OTA`, `CPAY`, `PAK` |
| ADAS / parking / sensing | `LDWS_LKAS`, `FCA`, `BCW`, `LCA`, `SPAS`, `RSPA`, `AVM`, `FCAM`, `FRADAR`, `SRR_FL`, `SRR_FR`, `SRR_RL`, `SRR_RR`, `PUS`, `DMS`, `OMS`, `AEB`, `PKM`, `RPC`, `RRM`, `SPM`, `HWP`, `LDR`, `TRM` |

## C. Test-Asset Link Hints For Promoted Nodes

These are the strongest current node-to-test links discovered directly from `canoe/tests/modules/test_units/**`.

| Node | Representative test asset(s) |
|---|---|
| `CGW` | `TC_CANOE_UT_CORE_001_CGW_CHS_GW`, `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW`, `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` |
| `ADAS` | `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST`, `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION`, `TC_CANOE_IT_EXT_039_ADAS_PERCEPTION_CONTEXT` |
| `VCU` | `TC_CANOE_IT_020_POWERTRAIN_DRIVE_BASELINE`, `TC_CANOE_UT_EXT_017_CHS_DYNAMICS_EXT` |
| `ESC` | `TC_CANOE_IT_022_CHASSIS_BRAKE_BASELINE`, `TC_CANOE_UT_EXT_016_CHS_BRAKE_EXT` |
| `MDPS` | `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE`, `TC_CANOE_UT_INP_028_VEHICLE_STEERING` |
| `NAV` | `TC_CANOE_UT_CORE_009_NAV_CTX_MGR`, `TC_CANOE_UT_INP_029_NAV_CONTEXT` |
| `BCM` | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY`, `TC_CANOE_UT_OUT_070_BCM_AMBIENT` |
| `IVI` | `TC_CANOE_UT_CORE_013_IVI_GW_ROUTE`, `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING`, `TC_CANOE_UT_OUT_071_IVI_HMI` |
| `CLU` | `TC_CANOE_UT_OUT_072_CLU_DISPLAY`, `TC_CANOE_UT_EXT_007_CLU_CONTEXT_ADJUST` |
| `AMP` | `TC_CANOE_UT_OUT_074_AMP_AUDIO` |
| `SGW` | `TC_CANOE_UT_EXT_063_SGW_SECURITY_STATE` |
| `DCM` | `TC_CANOE_UT_EXT_064_DCM_DIAGNOSTIC_STATE` |
| `VSM` | `TC_CANOE_UT_INP_033_VSM_INPUT` |
| `EHB` | `TC_CANOE_UT_INP_032_EHB_INPUT` |

## D. Current Gaps To Close Next

1. Fill per-ECU Rx/Tx/message/test rows for Layer 3 leaf nodes in wave order, not randomly.
2. Add a direct cross-reference from each promoted ECU row to the exact `0302` message rows and `0303` signal rows.
3. Separate `stable network ownership issue` from `runtime dynamics issue`.
4. Treat `AEB -> ESC/EHB/VSM` as the first coupled dynamics trace cluster.

## E. Reading Rule

When a reviewer or engineer asks "what moves together?" use this order:

1. `Core coupled ECU matrix`
2. `ECU_GROUP_NETWORK_VIEW_2026-03-28.md`
3. `svg/CORE_COUPLED_ECU_GROUP_MAP_2026-03-28.svg`
4. then drop down to official SoT `0301~0304`

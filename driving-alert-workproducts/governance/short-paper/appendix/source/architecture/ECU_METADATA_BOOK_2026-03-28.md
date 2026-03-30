# Vehicle ECU Architecture and Interaction Reference (2026-03-28)

Subtitle: CANoe SIL baseline reference for CAN and Ethernet behavior.

Vehicle ECU architecture and interaction reference for the active CANoe SIL baseline.
This book brings overview maps, action flows, and ECU cards into one reading sequence.

## Table Of Contents

1. Book Intent
2. Reading Guide
3. Visual Opening
4. System Narrative
5. Group Snapshot
6. Action-Flow Pack
7. ECU Catalog

## Book Intent

This book explains the CANoe runtime architecture through overview maps, action flows, and per-ECU cards.
The structure is behavior-first: system overview and action flows come before the ECU catalog.
Each ECU page is a reading aid for role, contracts, linked ECU, and representative runtime behavior.

## Reading Guide

1. Start with the overview SVG to understand the full 101-ECU surface.
2. Move into the grouped architecture view to see domain-level bundling.
3. Read the canonical action flows to understand behavior chains.
4. Move into per-ECU cards after the behavior context is clear.

### Core Reading Path

1. [Overview SVG](svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_2026-03-28.svg)
2. [Group View](ECU_GROUP_NETWORK_VIEW_2026-03-28.md)
3. [Action Flow Index](ACTION_FLOW_INDEX_2026-03-28.md)
4. [ECU to Flow Matrix](ECU_ACTION_FLOW_MATRIX_2026-03-28.md)
5. [ECU Card Index](ECU_CARD_INDEX_2026-03-28.md)

### Index Map

- [Action Flow Index](ACTION_FLOW_INDEX_2026-03-28.md): use this to find one canonical behavior chapter quickly.
- [ECU to Flow Matrix](ECU_ACTION_FLOW_MATRIX_2026-03-28.md): use this to move from one ECU to its primary and supporting flows.
- [ECU Card Index](ECU_CARD_INDEX_2026-03-28.md): use this to jump directly into `p1/p2/p3/p4` card pages.
- [Signal Flow Index](SIGNAL_FLOW_INDEX_2026-03-28.md): use this only when exact runtime names and detailed signal routes are needed.

<div style="page-break-before: always;"></div>

## Visual Opening

Start with the full 101-ECU overview before zooming into grouped figures, action flows, and per-ECU cards.

![](svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_2026-03-28.svg)

## System Narrative

- Runtime surface inventory: `101` ECU
- Canonical behavior pack: `20` action flows
- Meaningful behavior is not organized as 101 independent flows.
- One action flow crosses multiple ECU, and one ECU participates in multiple action flows.
- This book therefore uses three layers: overview architecture, action-flow atlas, and per-ECU catalog with detailed signal companions.

### Book Parts

- Part I. Architecture narrative: overview map, grouped view, and action-flow pack.
- Part II. ECU catalog: 101 ECU overview pages with one or more reference pages.

<div style="page-break-before: always;"></div>

## Group Snapshot

### Group 01 Base Vehicle Dynamics

The base vehicle dynamics group consolidates steering, braking, propulsion, and chassis health into one controllable runtime lane.

- Included domains: `Chassis, Powertrain`
- Representative action flows: `FLOW_01~05 (5 flows)`

![](svg/GROUP_01_BASE_VEHICLE_DYNAMICS_2026-03-28.svg)

### Group 02 ADAS AEB Brake Assist

The ADAS group collects perception, collision risk, parking assist, and intervention logic into one behavior-decision layer.

- Included domains: `ADAS`
- Representative action flows: `FLOW_06~10 (5 flows)`

![](svg/GROUP_02_ADAS_AEB_BRAKE_ASSIST_2026-03-28.svg)

### Group 03 Display Warning Audio

The display and alert group turns selected warning state into visible, audible, and service-facing user output.

- Included domains: `Infotainment`
- Representative action flows: `FLOW_11~15 (5 flows)`

![](svg/GROUP_03_DISPLAY_WARNING_AUDIO_2026-03-28.svg)

### Group 04 Body Comfort Ambient

The body and comfort group amplifies warning context through lighting, entry, ambient, climate, and comfort-domain state.

- Included domains: `Body`
- Representative action flows: `FLOW_16~18 (3 flows)`

![](svg/GROUP_04_BODY_COMFORT_AMBIENT_2026-03-28.svg)

### Group 05 Validation Scenario

The validation group isolates scenario injection and verdict readback so test orchestration stays separate from normal feature ownership.

- Included domains: `ETH_Backbone`
- Representative action flows: `FLOW_19`

![](svg/GROUP_05_VALIDATION_SCENARIO_2026-03-28.svg)

### Group 06 Backbone Gateway Diagnostics

The backbone and diagnostics group routes runtime state, service traffic, and external interfaces without becoming a hidden feature owner.

- Included domains: `ETH_Backbone`
- Representative action flows: `FLOW_20`

![](svg/GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_2026-03-28.svg)

<div style="page-break-before: always;"></div>

## Action-Flow Pack

The canonical action-flow pack is the behavior atlas for this project.
Use it to understand why multiple ECU cards point back to the same flow family.

- [Action Flow Index](ACTION_FLOW_INDEX_2026-03-28.md)
- [ECU to Flow Matrix](ECU_ACTION_FLOW_MATRIX_2026-03-28.md)
- Flow figures are embedded below so the main body can be read in one sequence.

### Dynamics

These flows explain how driver input, vehicle state, brake intervention, and propulsion feedback stay aligned on the runtime surface.

#### `FLOW_01` Steering Control Readback

Manual steering input is normalized, published as steering state, and rendered back into the steering readback path.

- User outcome: Steering bar, steering angle readback, and wheel feedback move together without drift.
- Primary ECU bank: `CGW, CLU, ESC, MDPS, RWS, SAS`
- Representative signals: `Steering Angle Cmd, Steering Angle, Steering State Can, Steering Torque`

![](svg/flows/action/FLOW_01_STEERING_CONTROL_READBACK_2026-03-28.svg)

#### `FLOW_02` Brake Stability Response

Brake request, AEB pressure intent, and stability outputs are synchronized across chassis brake owners and downstream readers.

- User outcome: Brake intervention feels coordinated and the driver sees consistent brake and stability state feedback.
- Primary ECU bank: `ABS, AEB, EHB, EPB, ESC, FCA, VCU, VSM`
- Representative signals: `AEB Domain State, Brake Status, Brake Temp, Wheel Speed`

![](svg/flows/action/FLOW_02_BRAKE_STABILITY_RESPONSE_2026-03-28.svg)

#### `FLOW_03` Propulsion Energy Status

Powertrain and energy ECUs consolidate drive, torque, battery, and charging state into the central propulsion state lane.

- User outcome: Vehicle mode, energy state, and propulsion readiness appear as one coherent status surface.
- Primary ECU bank: `BAT_BMS, CPC, DCDC, EMS, EOP, EWP, FPCM, INVERTER, ISG, LVR, MCU, OBC, TCU, VCU, _4WD`
- Representative signals: `Bat Bms State, State Can, Powertrain Gateway, Speed`

![](svg/flows/action/FLOW_03_PROPULSION_ENERGY_STATUS_2026-03-28.svg)

#### `FLOW_04` Cruise Speed Support

Cruise and longitudinal support state moves from support controllers into vehicle speed management and driver-facing outputs.

- User outcome: Cruise support state is readable, timely, and aligned between control and HMI.
- Primary ECU bank: `EMS, SCC, TCU, VCU`
- Representative signals: `Cruise Set Speed, Cruise State, State Can, Support State`

![](svg/flows/action/FLOW_04_CRUISE_SPEED_SUPPORT_2026-03-28.svg)

#### `FLOW_05` Chassis Sensor Health

Wheel, angle, suspension, and chassis leaf signals are collected so downstream control and visibility stay health-aware.

- User outcome: Chassis sensing and readiness stay visible and synchronized across control and display surfaces.
- Primary ECU bank: `ABS, ACU, ASM, CDC, ECS, EHB, EPB, ESC, MDPS, ODS, RWS, SAS, TPMS, VCU, VSM`
- Representative signals: `Steering Angle, Wheel Speed, Tire Pressure, Suspension State`

![](svg/flows/action/FLOW_05_CHASSIS_SENSOR_HEALTH_2026-03-28.svg)

### ADAS

These flows show how sensing, fusion, and assist logic become one coherent intervention and warning chain.

#### `FLOW_06` Object Risk Fusion

Radar, camera, lidar, and perception nodes are fused into one object-risk lane for ADAS warning and assist decisions.

- User outcome: Object-risk interpretation is unified before any warning or assist output is shown to the driver.
- Primary ECU bank: `ADAS, AEB, AVM, BCW, DMS, FCA, FCAM, FRADAR, HWP, LCA, LDR, LDWS_LKAS, OMS, PKM, PUS, RPC, RRM, RSPA, SCC, SPAS, SPM, SRR_FL, SRR_FR, SRR_RL, SRR_RR, TRM`
- Representative signals: `Object Risk, Lane State, ADAS Domain State, Alert Level`

![](svg/flows/action/FLOW_06_OBJECT_RISK_FUSION_2026-03-28.svg)

#### `FLOW_07` AEB Decel Intervention

AEB stop intent, decel profile, and downstream chassis response are connected as one intervention chain.

- User outcome: AEB behavior reads as one intervention story instead of separate ECU reactions.
- Primary ECU bank: `ADAS, AEB, EHB, ESC, FCA, SCC, VSM`
- Representative signals: `Fca State, AEB Domain State, Decel Assist Request, Brake Status`

![](svg/flows/action/FLOW_07_AEB_DECEL_INTERVENTION_2026-03-28.svg)

#### `FLOW_08` Lane and Surround Keeping

Lane keeping, blind-spot, and surround sensing work together to support steering and warning decisions.

- User outcome: Lane and surround warnings appear as one steering-side assistance behavior.
- Primary ECU bank: `ADAS, BCW, LCA, LDWS_LKAS, SRR_FL, SRR_FR, SRR_RL, SRR_RR`
- Representative signals: `Lane State, Blind Spot State, Steering State Can, Warning Text Code`

![](svg/flows/action/FLOW_08_LANE_SURROUND_KEEPING_2026-03-28.svg)

#### `FLOW_09` Parking and Surround Assist

Parking cameras, ultrasonic sensing, and parking controllers feed one parking-assist behavior chain.

- User outcome: Parking guidance and surround assistance feel like one guided maneuver story.
- Primary ECU bank: `ADAS, AVM, PKM, PUS, RPC, RRM, RSPA, SPAS, SPM`
- Representative signals: `Parking State, Ultrasonic State, Camera State, Maneuver Status`

![](svg/flows/action/FLOW_09_PARKING_SURROUND_ASSIST_2026-03-28.svg)

#### `FLOW_10` Driver Monitor and Occupant Risk

Driver state and occupant perception are fed into the warning lane before output arbitration happens.

- User outcome: Driver-state and occupant warnings are visible, audible, and consistent with the active context.
- Primary ECU bank: `DMS, OMS`
- Representative signals: `Driver State, Occupant State, Alert Type, Base Volume`

![](svg/flows/action/FLOW_10_DRIVER_MONITOR_OCCUPANT_2026-03-28.svg)

### Display and Alert

These flows turn selected alert state into cluster, HUD, audio, navigation, and service-facing user output.

#### `FLOW_11` Navigation Zone Context Ingress

Map and telematics context enters the runtime and becomes zone-aware alert context for downstream selection and HMI.

- User outcome: Zone-aware warning behavior is traceable from map context ingress to the final driver cue.
- Primary ECU bank: `AMP, CLU, HUD, IVI, NAV, RSE, TMU, VCS`
- Representative signals: `Navigation Context Can, Navigation Module State, Road Zone State, Alert Type`

![](svg/flows/action/FLOW_11_NAV_ZONE_CONTEXT_INGRESS_2026-03-28.svg)

#### `FLOW_12` V2X Emergency Ingress

Emergency-vehicle ingress arrives through the V2X lane and is routed into the warning decision chain.

- User outcome: Emergency-vehicle alerts have a clear ingress point and an explainable output path.
- Primary ECU bank: `AMP, CGW, ETHB, HUD, V2X`
- Representative signals: `V2X, ETH Emergency Alert, Alert Level, Warning Text Code`

![](svg/flows/action/FLOW_12_V2X_EMERGENCY_INGRESS_2026-03-28.svg)

#### `FLOW_13` Alert Arbitration and Gate

Multiple warning candidates are reduced into one selected alert with explicit gateway and display semantics.

- User outcome: Only one alert meaning survives to the user-facing surfaces, and the gate reason remains explainable.
- Primary ECU bank: `AMP, CGW, CLU, HUD, IVI, TMU, V2X, VCS`
- Representative signals: `Alert Type, Alert Level, Alert Gate Reason, Warning Text Code`

![](svg/flows/action/FLOW_13_ALERT_ARBITRATION_GATE_2026-03-28.svg)

#### `FLOW_14` Cluster, HUD, and Audio Output

Selected warning state is rendered into cluster, HUD, and audio output without diverging message semantics.

- User outcome: Visual and audio warning channels stay aligned instead of competing with each other.
- Primary ECU bank: `AMP, CLU, HUD, IVI, TMU, VCS`
- Representative signals: `Warning Text Code, Steering, Volume Level, Base Volume`

![](svg/flows/action/FLOW_14_CLUSTER_HUD_AUDIO_OUTPUT_2026-03-28.svg)

#### `FLOW_15` Service and Access HMI

Digital-key, payment, OTA, and related service surfaces are orchestrated through one HMI-facing service chain.

- User outcome: Service-facing screens read like one digital-access ecosystem, not isolated widgets.
- Primary ECU bank: `CPAY, DKEY, IVI, NAV, OTA, PAK, PGS, RSE, TMU, VCS`
- Representative signals: `Service State, Key Presence, Payment Context, OTA Readiness`

![](svg/flows/action/FLOW_15_SERVICE_ACCESS_HMI_2026-03-28.svg)

### Body and Comfort

These flows describe how body, comfort, and ambient actuators amplify or support the selected runtime state.

#### `FLOW_16` Body Ambient Warning Output

Body lighting, ambient, wiper, and exterior cues amplify the selected warning state in the comfort domain.

- User outcome: Ambient and body warning outputs reinforce the selected alert instead of acting independently.
- Primary ECU bank: `ADM, AFLS, AHLS, BCM, BIO, HLM, MIR, MSC, PTG, SRF, TGM, WIP`
- Representative signals: `Ambient Mode, Blink Left, Blink Right, Front Wiper Anim`

![](svg/flows/action/FLOW_16_BODY_AMBIENT_WARNING_2026-03-28.svg)

#### `FLOW_17` Access, Security, and Entry

Key, access, security, and door controllers are connected into one vehicle-entry behavior chain.

- User outcome: Entry, lock, and security behavior can be read as one access story from request to result.
- Primary ECU bank: `BCM, BSEC, CSM, DKEY, DOOR_FL, DOOR_FR, DOOR_RL, DOOR_RR, PAK, PGS, SMK`
- Representative signals: `Key Presence, Door Lock State, Entry Authorization, Body Security State`

![](svg/flows/action/FLOW_17_ACCESS_SECURITY_ENTRY_2026-03-28.svg)

#### `FLOW_18` Comfort, Climate, and Seat

Climate and seat controllers are orchestrated as one comfort-domain runtime surface with body and HMI visibility.

- User outcome: Comfort-domain status is discoverable without hunting across separate climate and seat surfaces.
- Primary ECU bank: `BCM, DATC, RATC, SEAT_DRV, SEAT_PASS`
- Representative signals: `Climate State, Seat State, Comfort Visibility, Body Comfort Mode`

![](svg/flows/action/FLOW_18_COMFORT_CLIMATE_SEAT_2026-03-28.svg)

### Validation

These flows keep scenario control and verdict readback inside a dedicated validation lane.

#### `FLOW_19` Validation Scenario Control

Scenario command, injected state, and verdict readback are kept inside a dedicated validation control story.

- User outcome: Validation control remains an explicit harness story instead of leaking into product ownership.
- Primary ECU bank: `TEST_BAS, TEST_SCN`
- Representative signals: `Scenario Command, Scenario Active Id, Scenario Result, Validation Summary Seams`

![](svg/flows/action/FLOW_19_VALIDATION_SCENARIO_CONTROL_2026-03-28.svg)

### Backbone

These flows describe how gateway, diagnostics, and Ethernet-facing services route state across domains.

#### `FLOW_20` Backbone, Diagnostic, and Service Routing

Gateway, backbone, diagnostics, and service-facing surfaces route runtime state without becoming hidden feature owners.

- User outcome: Backbone and diagnostic behavior is readable as one routing story instead of scattered support nodes.
- Primary ECU bank: `CGW, DCM, EDR, ETHB, EXT_DIAG, IBOX, SGW, TEST_BAS, TEST_SCN, V2X`
- Representative signals: `Diagnostic Request, Diagnostic Response, Gateway State, Service Routing State`

![](svg/flows/action/FLOW_20_BACKBONE_DIAGNOSTIC_SERVICE_2026-03-28.svg)

<div style="page-break-before: always;"></div>

## ECU Catalog

The catalog below is grouped by architecture group so the book reads as one system story instead of a flat asset list.
Each ECU section keeps one human-readable sentence, one overview page, one or more reference pages, and one representative detailed signal flow.

<div style="page-break-before: always;"></div>

## Group 01 Base Vehicle Dynamics

The base vehicle dynamics group consolidates steering, braking, propulsion, and chassis health into one controllable runtime lane.

- Included domains: `Chassis, Powertrain`

![](svg/GROUP_01_BASE_VEHICLE_DYNAMICS_2026-03-28.svg)

### `ABS`

Publishes anti-lock brake state and brake intervention feedback for chassis and ADAS consumers

![](svg/ecu_cards/ECU_CARD_ABS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ABS_2026-03-28_P2.svg)

- Representative detailed signal flow: `BRAKE_LAMP_AND_ABS_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/BRAKE_LAMP_AND_ABS_SIGNAL_FLOW_2026-03-28.svg)

### `ACU`

Publishes crash and restraint state so gateway, body, and warning surfaces can react to occupant-safety events

![](svg/ecu_cards/ECU_CARD_ACU_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ACU_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg)

### `ASM`

Publishes air-suspension state so chassis and ADAS readers can adapt ride and stability behavior

![](svg/ecu_cards/ECU_CARD_ASM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ASM_2026-03-28_P2.svg)

- Representative detailed signal flow: `ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.svg)

### `CDC`

Publishes damping-control state and diagnostics for chassis health and adaptation readers

![](svg/ecu_cards/ECU_CARD_CDC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_CDC_2026-03-28_P2.svg)

- Representative detailed signal flow: `ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.svg)

### `ECS`

Publishes electronic suspension state for chassis health and downstream ride-control consumers

![](svg/ecu_cards/ECU_CARD_ECS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ECS_2026-03-28_P2.svg)

- Representative detailed signal flow: `ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.svg)

### `EHB`

Coupled consumer of AEB state rather than an independent decision origin

![](svg/ecu_cards/ECU_CARD_EHB_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EHB_2026-03-28_P2.svg)

- Representative detailed signal flow: `AEB_PRESSURE_TO_EHB_COMMAND_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AEB_PRESSURE_TO_EHB_COMMAND_SIGNAL_FLOW_2026-03-28.svg)

### `EPB`

Publishes parking-brake state and diagnostics for cluster and validation readers

![](svg/ecu_cards/ECU_CARD_EPB_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EPB_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `ESC`

Consumes vehicle and AEB state, then publishes brake and stability state to downstream readers

![](svg/ecu_cards/ECU_CARD_ESC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ESC_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_ESC_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_ESC_2026-03-28_P4.svg)

- Representative detailed signal flow: `ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.svg)

### `MDPS`

Steering state must stay aligned across manual command, owner readback, and display frame

![](svg/ecu_cards/ECU_CARD_MDPS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_MDPS_2026-03-28_P2.svg)

- Representative detailed signal flow: `STEERING_INPUT_TO_MDPS_STATE_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/STEERING_INPUT_TO_MDPS_STATE_SIGNAL_FLOW_2026-03-28.svg)

### `ODS`

Publishes occupant-detection state for body and gateway safety decisions

![](svg/ecu_cards/ECU_CARD_ODS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ODS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg)

### `RWS`

Publishes rear-wheel steering state so steering and stability consumers stay aligned

![](svg/ecu_cards/ECU_CARD_RWS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_RWS_2026-03-28_P2.svg)

- Representative detailed signal flow: `ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.svg)

### `SAS`

Publishes steering-angle sensor state for steering control, stability logic, and validation visibility

![](svg/ecu_cards/ECU_CARD_SAS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SAS_2026-03-28_P2.svg)

- Representative detailed signal flow: `STEERING_INPUT_TO_SAS_ANGLE_RAW_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/STEERING_INPUT_TO_SAS_ANGLE_RAW_SIGNAL_FLOW_2026-03-29.svg)

### `TPMS`

Publishes tire-pressure and wheel-health state for chassis visibility and warning surfaces

![](svg/ecu_cards/ECU_CARD_TPMS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TPMS_2026-03-28_P2.svg)

- Representative detailed signal flow: `WHEEL_SPEED_TO_TPMS_TIRE_PRESSURE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/WHEEL_SPEED_TO_TPMS_TIRE_PRESSURE_SIGNAL_FLOW_2026-03-29.svg)

### `VCU`

Primary dynamics producer for speed, drive state, and throttle interpretation

![](svg/ecu_cards/ECU_CARD_VCU_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_VCU_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_VCU_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_VCU_2026-03-28_P4.svg)

- Representative detailed signal flow: `VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29.svg)

### `VSM`

Consumes ESC and AEB domain state to produce local stability intervention behavior

![](svg/ecu_cards/ECU_CARD_VSM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_VSM_2026-03-28_P2.svg)

- Representative detailed signal flow: `ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.svg)

### `BAT_BMS`

Publishes battery and energy state so propulsion, charging, and display surfaces share one EV health view

![](svg/ecu_cards/ECU_CARD_BAT_BMS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_BAT_BMS_2026-03-28_P2.svg)

- Representative detailed signal flow: `BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28.svg)

### `CPC`

Publishes central propulsion coordination state for downstream powertrain readers

![](svg/ecu_cards/ECU_CARD_CPC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_CPC_2026-03-28_P2.svg)

- Representative detailed signal flow: `BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28.svg)

### `DCDC`

Publishes DC-DC converter state for energy distribution and charging-health visibility

![](svg/ecu_cards/ECU_CARD_DCDC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DCDC_2026-03-28_P2.svg)

- Representative detailed signal flow: `BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28.svg)

### `EMS`

Publishes engine and propulsion health state for vehicle control and display readers

![](svg/ecu_cards/ECU_CARD_EMS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EMS_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_EMS_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_EMS_2026-03-28_P4.svg)

- Representative detailed signal flow: `VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29.svg)

### `EOP`

Publishes oil-pump state for propulsion support and thermal-health visibility

![](svg/ecu_cards/ECU_CARD_EOP_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EOP_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg)

### `EWP`

Publishes electric water-pump state for thermal support and propulsion-health readers

![](svg/ecu_cards/ECU_CARD_EWP_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EWP_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg)

### `FPCM`

Publishes fuel-pump control state for propulsion support and diagnostic visibility

![](svg/ecu_cards/ECU_CARD_FPCM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_FPCM_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg)

### `INVERTER`

Publishes inverter state and power-conversion feedback for propulsion-control consumers

![](svg/ecu_cards/ECU_CARD_INVERTER_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_INVERTER_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg)

### `ISG`

Publishes starter-generator state for propulsion readiness and energy coordination

![](svg/ecu_cards/ECU_CARD_ISG_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ISG_2026-03-28_P2.svg)

- Representative detailed signal flow: `VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29.svg)

### `LVR`

Publishes lever or range-selection state for drive-mode and propulsion coordination

![](svg/ecu_cards/ECU_CARD_LVR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_LVR_2026-03-28_P2.svg)

- Representative detailed signal flow: `VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29.svg)

### `MCU`

Publishes motor-control state for torque delivery and EV propulsion coordination

![](svg/ecu_cards/ECU_CARD_MCU_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_MCU_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg)

### `OBC`

Publishes on-board charger state for charging status and energy visibility

![](svg/ecu_cards/ECU_CARD_OBC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_OBC_2026-03-28_P2.svg)

- Representative detailed signal flow: `OBC_BMS_TEMP_TO_CPC_TARGET_SOC_THERMAL_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/OBC_BMS_TEMP_TO_CPC_TARGET_SOC_THERMAL_SIGNAL_FLOW_2026-03-29.svg)

### `TCU`

Publishes transmission state for longitudinal control and driver-facing vehicle status

![](svg/ecu_cards/ECU_CARD_TCU_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TCU_2026-03-28_P2.svg)

- Representative detailed signal flow: `VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29.svg)

### `_4WD`

Publishes four-wheel-drive engagement state for propulsion coordination and chassis awareness

![](svg/ecu_cards/ECU_CARD__4WD_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD__4WD_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg)

<div style="page-break-before: always;"></div>

## Group 02 ADAS AEB Brake Assist

The ADAS group collects perception, collision risk, parking assist, and intervention logic into one behavior-decision layer.

- Included domains: `ADAS`

![](svg/GROUP_02_ADAS_AEB_BRAKE_ASSIST_2026-03-28.svg)

### `ADAS`

Consumes route, chassis, and emergency context, then emits selected alert and assist intent

![](svg/ecu_cards/ECU_CARD_ADAS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ADAS_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_ADAS_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_ADAS_2026-03-28_P4.svg)

- Representative detailed signal flow: `AEB_BRAKE_ASSIST_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AEB_BRAKE_ASSIST_SIGNAL_FLOW_2026-03-28.svg)

### `AEB`

One AEB profile change can appear as multiple simultaneous chassis ECU reactions

![](svg/ecu_cards/ECU_CARD_AEB_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_AEB_2026-03-28_P2.svg)

- Representative detailed signal flow: `ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.svg)

### `AVM`

Publishes around-view monitor state for parking and display consumers

![](svg/ecu_cards/ECU_CARD_AVM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_AVM_2026-03-28_P2.svg)

- Representative detailed signal flow: `ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg)

### `BCW`

Publishes blind-spot warning state for alert selection and driver warning output

![](svg/ecu_cards/ECU_CARD_BCW_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_BCW_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `DMS`

Publishes driver monitoring state so assist and warning logic can react to attention loss

![](svg/ecu_cards/ECU_CARD_DMS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DMS_2026-03-28_P2.svg)

- Representative detailed signal flow: `DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28.svg)

### `FCA`

Publishes forward-collision assist state and request feedback for braking and warning consumers

![](svg/ecu_cards/ECU_CARD_FCA_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_FCA_2026-03-28_P2.svg)

- Representative detailed signal flow: `OBJECT_RISK_TO_FCA_REQUEST_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/OBJECT_RISK_TO_FCA_REQUEST_SIGNAL_FLOW_2026-03-28.svg)

### `FCAM`

Publishes forward-camera perception state for object-risk and highway-ready decisions

![](svg/ecu_cards/ECU_CARD_FCAM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_FCAM_2026-03-28_P2.svg)

- Representative detailed signal flow: `OBJECT_INPUT_TO_FCAM_CAMERA_STATE_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/OBJECT_INPUT_TO_FCAM_CAMERA_STATE_SIGNAL_FLOW_2026-03-28.svg)

### `FRADAR`

Publishes front-radar perception state for object fusion and assist decisions

![](svg/ecu_cards/ECU_CARD_FRADAR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_FRADAR_2026-03-28_P2.svg)

- Representative detailed signal flow: `OBJECT_RISK_TO_WARNING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/OBJECT_RISK_TO_WARNING_SIGNAL_FLOW_2026-03-28.svg)

### `HWP`

Publishes highway-pilot readiness and state for driver-monitor, cluster, and assist consumers

![](svg/ecu_cards/ECU_CARD_HWP_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_HWP_2026-03-28_P2.svg)

- Representative detailed signal flow: `DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28.svg)

### `LCA`

Publishes lane-change assist state for warning and driver-guidance outputs

![](svg/ecu_cards/ECU_CARD_LCA_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_LCA_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `LDR`

Publishes lidar perception state for object fusion and path-readiness consumers

![](svg/ecu_cards/ECU_CARD_LDR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_LDR_2026-03-28_P2.svg)

- Representative detailed signal flow: `OBJECT_SAFETY_TO_LDR_HEALTH_RANGE_BUCKET_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/OBJECT_SAFETY_TO_LDR_HEALTH_RANGE_BUCKET_SIGNAL_FLOW_2026-03-29.svg)

### `LDWS_LKAS`

Publishes lane-departure and lane-keeping state for warning and steering-support consumers

![](svg/ecu_cards/ECU_CARD_LDWS_LKAS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_LDWS_LKAS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `OMS`

Publishes occupant-monitoring state for body safety and alert decisions

![](svg/ecu_cards/ECU_CARD_OMS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_OMS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg)

### `PKM`

Publishes parking-master state for parking-assist orchestration and HMI visibility

![](svg/ecu_cards/ECU_CARD_PKM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_PKM_2026-03-28_P2.svg)

- Representative detailed signal flow: `ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg)

### `PUS`

Publishes parking-ultrasonic state for parking assist and body or IVI readers

![](svg/ecu_cards/ECU_CARD_PUS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_PUS_2026-03-28_P2.svg)

- Representative detailed signal flow: `ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg)

### `RPC`

Publishes road-preview camera state for ADAS control-adaptation readers

![](svg/ecu_cards/ECU_CARD_RPC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_RPC_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `RRM`

Publishes rear-radar master state for surround awareness and warning selection

![](svg/ecu_cards/ECU_CARD_RRM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_RRM_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `RSPA`

Publishes remote smart parking-assist state for chassis, assist, and display consumers

![](svg/ecu_cards/ECU_CARD_RSPA_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_RSPA_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `SCC`

SCC support behavior feeds ADAS and VCU rather than directly owning output HMI

![](svg/ecu_cards/ECU_CARD_SCC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SCC_2026-03-28_P2.svg)

- Representative detailed signal flow: `RISK_LEVEL_TO_SCC_CRUISE_MODULATION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/RISK_LEVEL_TO_SCC_CRUISE_MODULATION_SIGNAL_FLOW_2026-03-28.svg)

### `SPAS`

Publishes smart parking-assist state for steering-support and parking HMI consumers

![](svg/ecu_cards/ECU_CARD_SPAS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SPAS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `SPM`

Publishes surround parking-master state for parking coordination and HMI output

![](svg/ecu_cards/ECU_CARD_SPM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SPM_2026-03-28_P2.svg)

- Representative detailed signal flow: `ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg)

### `SRR_FL`

Publishes front-left corner radar state for surround fusion and parking or lane-assist consumers

![](svg/ecu_cards/ECU_CARD_SRR_FL_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SRR_FL_2026-03-28_P2.svg)

- Representative detailed signal flow: `MERGE_CONFLICT_TO_SRR_SIDE_RISK_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/MERGE_CONFLICT_TO_SRR_SIDE_RISK_SIGNAL_FLOW_2026-03-28.svg)

### `SRR_FR`

Publishes front-right corner radar state for surround fusion and parking or lane-assist consumers

![](svg/ecu_cards/ECU_CARD_SRR_FR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SRR_FR_2026-03-28_P2.svg)

- Representative detailed signal flow: `ACCESS_AUTH_TO_DOOR_FR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/ACCESS_AUTH_TO_DOOR_FR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `SRR_RL`

Publishes rear-left corner radar state for surround fusion and parking or lane-assist consumers

![](svg/ecu_cards/ECU_CARD_SRR_RL_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SRR_RL_2026-03-28_P2.svg)

- Representative detailed signal flow: `CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RL_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RL_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `SRR_RR`

Publishes rear-right corner radar state for surround fusion and parking or lane-assist consumers

![](svg/ecu_cards/ECU_CARD_SRR_RR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SRR_RR_2026-03-28_P2.svg)

- Representative detailed signal flow: `CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `TRM`

Publishes trailer-management state for ADAS and vehicle-state consumers

![](svg/ecu_cards/ECU_CARD_TRM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TRM_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

<div style="page-break-before: always;"></div>

## Group 03 Display Warning Audio

The display and alert group turns selected warning state into visible, audible, and service-facing user output.

- Included domains: `Infotainment`

![](svg/GROUP_03_DISPLAY_WARNING_AUDIO_2026-03-28.svg)

### `AMP`

Receives gated audio intent from IVI/BCM and renders the final alert volume

![](svg/ecu_cards/ECU_CARD_AMP_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_AMP_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_FOCUS_TO_AMP_DUCKING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AUDIO_FOCUS_TO_AMP_DUCKING_SIGNAL_FLOW_2026-03-28.svg)

### `CLU`

Consumes selected alert state and vehicle state to build cluster-facing output

![](svg/ecu_cards/ECU_CARD_CLU_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_CLU_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_CLU_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_CLU_2026-03-28_P4.svg)

- Representative detailed signal flow: `AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_POPUP_SYNC_TO_CLU_DUPLICATE_GUARD_SIGNAL_FLOW_2026-03-29.svg)

### `CPAY`

Publishes connected payment service state for IVI and service-surface readers

![](svg/ecu_cards/ECU_CARD_CPAY_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_CPAY_2026-03-28_P2.svg)

- Representative detailed signal flow: `CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29.svg)

### `DKEY`

Publishes digital-key service state for IVI and access-service consumers

![](svg/ecu_cards/ECU_CARD_DKEY_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DKEY_2026-03-28_P2.svg)

- Representative detailed signal flow: `DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29.svg)

### `HUD`

Renders selected warning and driver-guidance state into the head-up display surface

![](svg/ecu_cards/ECU_CARD_HUD_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_HUD_2026-03-28_P2.svg)

- Representative detailed signal flow: `CLUSTER_WARNING_TO_HUD_WARNING_CODE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CLUSTER_WARNING_TO_HUD_WARNING_CODE_SIGNAL_FLOW_2026-03-29.svg)

### `IVI`

Routes gated alert state into visible display, map, and audio focus paths

![](svg/ecu_cards/ECU_CARD_IVI_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_IVI_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_IVI_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_IVI_2026-03-28_P4.svg)

- Representative detailed signal flow: `CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29.svg)

### `NAV`

Publishes navigation context and route state for zone-aware warning and assist consumers

![](svg/ecu_cards/ECU_CARD_NAV_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_NAV_2026-03-28_P2.svg)

- Representative detailed signal flow: `NAV_STATE_TO_IVI_BACKBONE_NAV_CONTEXT_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/NAV_STATE_TO_IVI_BACKBONE_NAV_CONTEXT_SIGNAL_FLOW_2026-03-29.svg)

### `OTA`

Publishes over-the-air service state for IVI and backbone service visibility

![](svg/ecu_cards/ECU_CARD_OTA_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_OTA_2026-03-28_P2.svg)

- Representative detailed signal flow: `CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29.svg)

### `PAK`

Publishes passive-access key state for service and access consumers

![](svg/ecu_cards/ECU_CARD_PAK_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_PAK_2026-03-28_P2.svg)

- Representative detailed signal flow: `DIGITAL_KEY_AND_SIGNAL_BARS_TO_PAK_PROXIMITY_LATENCY_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/DIGITAL_KEY_AND_SIGNAL_BARS_TO_PAK_PROXIMITY_LATENCY_SIGNAL_FLOW_2026-03-29.svg)

### `PGS`

Publishes parking-guidance system state for IVI and parking HMI readers

![](svg/ecu_cards/ECU_CARD_PGS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_PGS_2026-03-28_P2.svg)

- Representative detailed signal flow: `ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg)

### `RSE`

Publishes rear-seat entertainment state for infotainment service visibility

![](svg/ecu_cards/ECU_CARD_RSE_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_RSE_2026-03-28_P2.svg)

- Representative detailed signal flow: `ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg)

### `TMU`

Publishes telematics and remote-service state for IVI, climate, and navigation consumers

![](svg/ecu_cards/ECU_CARD_TMU_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TMU_2026-03-28_P2.svg)

- Representative detailed signal flow: `CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CONNECTIVITY_AND_IVI_HEALTH_TO_TMU_SERVICE_MODE_SIGNAL_FLOW_2026-03-29.svg)

### `VCS`

Publishes voice and connected-speech state for audio and IVI service consumers

![](svg/ecu_cards/ECU_CARD_VCS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_VCS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AUDIO_FOCUS_TMU_NOTIF_TO_VCS_VOICE_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/AUDIO_FOCUS_TMU_NOTIF_TO_VCS_VOICE_STATE_SIGNAL_FLOW_2026-03-29.svg)

<div style="page-break-before: always;"></div>

## Group 04 Body Comfort Ambient

The body and comfort group amplifies warning context through lighting, entry, ambient, climate, and comfort-domain state.

- Included domains: `Body`

![](svg/GROUP_04_BODY_COMFORT_AMBIENT_2026-03-28.svg)

### `ADM`

Publishes automatic door control state for body comfort and access surfaces

![](svg/ecu_cards/ECU_CARD_ADM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ADM_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `AFLS`

Publishes adaptive front-lighting state for body lighting and driver-visibility consumers

![](svg/ecu_cards/ECU_CARD_AFLS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_AFLS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28.svg)

### `AHLS`

Publishes automatic high-beam lighting state for body lighting and visibility surfaces

![](svg/ecu_cards/ECU_CARD_AHLS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_AHLS_2026-03-28_P2.svg)

- Representative detailed signal flow: `AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28.svg)

### `BCM`

Owns comfort and ambient outputs while bridging body leaf ECU state back to HMI

![](svg/ecu_cards/ECU_CARD_BCM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_BCM_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_BCM_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_BCM_2026-03-28_P4.svg)

- Representative detailed signal flow: `AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg)

### `BIO`

Publishes biometric authentication state for access and security consumers

![](svg/ecu_cards/ECU_CARD_BIO_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_BIO_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `BSEC`

Publishes body security and alarm state for access, warning, and service visibility

![](svg/ecu_cards/ECU_CARD_BSEC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_BSEC_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `CSM`

Publishes cabin sensing state for access, security, and comfort decisions

![](svg/ecu_cards/ECU_CARD_CSM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_CSM_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `DATC`

Publishes HVAC and climate-control state for comfort-domain and telematics readers

![](svg/ecu_cards/ECU_CARD_DATC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DATC_2026-03-28_P2.svg)

- Representative detailed signal flow: `CABIN_AIR_TEMP_TO_DATC_DEFOG_VENT_MODE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CABIN_AIR_TEMP_TO_DATC_DEFOG_VENT_MODE_SIGNAL_FLOW_2026-03-29.svg)

### `DOOR_FL`

Publishes front-left door state for access, security, and comfort visibility

![](svg/ecu_cards/ECU_CARD_DOOR_FL_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DOOR_FL_2026-03-28_P2.svg)

- Representative detailed signal flow: `DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29.svg)

### `DOOR_FR`

Publishes front-right door state for access, security, and comfort visibility

![](svg/ecu_cards/ECU_CARD_DOOR_FR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DOOR_FR_2026-03-28_P2.svg)

- Representative detailed signal flow: `ACCESS_AUTH_TO_DOOR_FR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/ACCESS_AUTH_TO_DOOR_FR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `DOOR_RL`

Publishes rear-left door state for access, security, and comfort visibility

![](svg/ecu_cards/ECU_CARD_DOOR_RL_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DOOR_RL_2026-03-28_P2.svg)

- Representative detailed signal flow: `CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RL_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RL_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `DOOR_RR`

Publishes rear-right door state for access, security, and comfort visibility

![](svg/ecu_cards/ECU_CARD_DOOR_RR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DOOR_RR_2026-03-28_P2.svg)

- Representative detailed signal flow: `CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/CHILD_LOCK_AND_ACCESS_AUTH_TO_DOOR_RR_UNLOCK_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `HLM`

Publishes headlamp-leveling state for lighting visibility and body diagnostics

![](svg/ecu_cards/ECU_CARD_HLM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_HLM_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `MIR`

Publishes mirror state for body comfort and driver-visibility surfaces

![](svg/ecu_cards/ECU_CARD_MIR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_MIR_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg)

### `MSC`

Publishes massage-seat control state for seat comfort and HMI visibility

![](svg/ecu_cards/ECU_CARD_MSC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_MSC_2026-03-28_P2.svg)

- Representative detailed signal flow: `SEAT_COMFORT_TO_MASSAGE_INTENSITY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/SEAT_COMFORT_TO_MASSAGE_INTENSITY_SIGNAL_FLOW_2026-03-28.svg)

### `PTG`

Publishes power-tailgate state for access and body comfort visibility

![](svg/ecu_cards/ECU_CARD_PTG_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_PTG_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `RATC`

Publishes rear-climate state for rear-cabin comfort and HMI readers

![](svg/ecu_cards/ECU_CARD_RATC_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_RATC_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg)

### `SEAT_DRV`

Publishes driver-seat state for comfort control and HMI visibility

![](svg/ecu_cards/ECU_CARD_SEAT_DRV_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SEAT_DRV_2026-03-28_P2.svg)

- Representative detailed signal flow: `DRIVER_SEAT_CMD_TO_SEAT_DRV_POSITION_COMFORT_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/DRIVER_SEAT_CMD_TO_SEAT_DRV_POSITION_COMFORT_SIGNAL_FLOW_2026-03-29.svg)

### `SEAT_PASS`

Publishes passenger-seat state for comfort control and HMI visibility

![](svg/ecu_cards/ECU_CARD_SEAT_PASS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SEAT_PASS_2026-03-28_P2.svg)

- Representative detailed signal flow: `PASSENGER_SEAT_CMD_TO_SEAT_PASS_POSITION_COMFORT_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/PASSENGER_SEAT_CMD_TO_SEAT_PASS_POSITION_COMFORT_SIGNAL_FLOW_2026-03-29.svg)

### `SMK`

Publishes smart-key and immobilizer state for access security and validation readers

![](svg/ecu_cards/ECU_CARD_SMK_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SMK_2026-03-28_P2.svg)

- Representative detailed signal flow: `DIGITAL_KEY_AND_DRIVE_STATE_TO_SMK_AUTH_GATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/DIGITAL_KEY_AND_DRIVE_STATE_TO_SMK_AUTH_GATE_SIGNAL_FLOW_2026-03-29.svg)

### `SRF`

Publishes sunroof state for comfort control and body visibility

![](svg/ecu_cards/ECU_CARD_SRF_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SRF_2026-03-28_P2.svg)

- Representative detailed signal flow: `AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg)

### `TGM`

Publishes tailgate state for body access and comfort visibility

![](svg/ecu_cards/ECU_CARD_TGM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TGM_2026-03-28_P2.svg)

- Representative detailed signal flow: `DKEY_ACCESS_TO_TGM_TAILGATE_STATE_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/DKEY_ACCESS_TO_TGM_TAILGATE_STATE_SIGNAL_FLOW_2026-03-29.svg)

### `WIP`

Publishes wiper state and diagnostics for body visibility and warning surfaces

![](svg/ecu_cards/ECU_CARD_WIP_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_WIP_2026-03-28_P2.svg)

- Representative detailed signal flow: `RAIN_LIGHT_AND_WIPER_CMD_TO_WIPER_ANIM_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/RAIN_LIGHT_AND_WIPER_CMD_TO_WIPER_ANIM_SIGNAL_FLOW_2026-03-29.svg)

<div style="page-break-before: always;"></div>

## Group 05 Validation Scenario

The validation group isolates scenario injection and verdict readback so test orchestration stays separate from normal feature ownership.

- Included domains: `ETH_Backbone`

![](svg/GROUP_05_VALIDATION_SCENARIO_2026-03-28.svg)

### `TEST_BAS`

Aggregates scenario results and publishes baseline validation summaries

![](svg/ecu_cards/ECU_CARD_TEST_BAS_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TEST_BAS_2026-03-28_P2.svg)

- Representative detailed signal flow: `SCENARIO_LOCK_TO_MANUAL_OVERRIDE_RELEASE_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/SCENARIO_LOCK_TO_MANUAL_OVERRIDE_RELEASE_SIGNAL_FLOW_2026-03-28.svg)

### `TEST_SCN`

Scenario entry point for validation presets, stop/manual logic, and scenario verdict readback

![](svg/ecu_cards/ECU_CARD_TEST_SCN_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_TEST_SCN_2026-03-28_P2.svg)

![](svg/ecu_cards/ECU_CARD_TEST_SCN_2026-03-28_P3.svg)

![](svg/ecu_cards/ECU_CARD_TEST_SCN_2026-03-28_P4.svg)

- Representative detailed signal flow: `TMU_ACCESS_TO_DKEY_STATE_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/TMU_ACCESS_TO_DKEY_STATE_SIGNAL_FLOW_2026-03-28.svg)

<div style="page-break-before: always;"></div>

## Group 06 Backbone Gateway Diagnostics

The backbone and diagnostics group routes runtime state, service traffic, and external interfaces without becoming a hidden feature owner.

- Included domains: `ETH_Backbone`

![](svg/GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_2026-03-28.svg)

### `CGW`

Bridges domain outputs toward IVI, CLU, BCM, and AMP while enforcing gate logic

![](svg/ecu_cards/ECU_CARD_CGW_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_CGW_2026-03-28_P2.svg)

- Representative detailed signal flow: `NAV_AGE_TO_CGW_BOUNDARY_ROUTING_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/NAV_AGE_TO_CGW_BOUNDARY_ROUTING_SIGNAL_FLOW_2026-03-29.svg)

### `DCM`

Publishes diagnostic manager state for service routing and diagnostic visibility

![](svg/ecu_cards/ECU_CARD_DCM_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_DCM_2026-03-28_P2.svg)

- Representative detailed signal flow: `BOUNDARY_ROUTE_CONTEXT_TO_DCM_SECURITY_SESSION_POLICY_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/BOUNDARY_ROUTE_CONTEXT_TO_DCM_SECURITY_SESSION_POLICY_SIGNAL_FLOW_2026-03-29.svg)

### `EDR`

Publishes event-data recorder state for fail-safe logging and service readers

![](svg/ecu_cards/ECU_CARD_EDR_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EDR_2026-03-28_P2.svg)

- Representative detailed signal flow: `FAILSAFE_MODE_TO_EDR_STORAGE_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/FAILSAFE_MODE_TO_EDR_STORAGE_SIGNAL_FLOW_2026-03-28.svg)

### `ETHB`

Publishes Ethernet backbone state for service routing and link-health visibility

![](svg/ecu_cards/ECU_CARD_ETHB_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_ETHB_2026-03-28_P2.svg)

- Representative detailed signal flow: `DIAG_STAGE_TO_ETHB_SERVICE_SECURITY_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/DIAG_STAGE_TO_ETHB_SERVICE_SECURITY_SIGNAL_FLOW_2026-03-28.svg)

### `EXT_DIAG`

Publishes external diagnostic session state for service routing and workshop ingress

![](svg/ecu_cards/ECU_CARD_EXT_DIAG_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_EXT_DIAG_2026-03-28_P2.svg)

- Representative detailed signal flow: `DIAG_ROUTE_OWNER_TO_GATEWAY_OPEN_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/DIAG_ROUTE_OWNER_TO_GATEWAY_OPEN_SIGNAL_FLOW_2026-03-28.svg)

### `IBOX`

Publishes in-vehicle connectivity hub state for service-link visibility

![](svg/ecu_cards/ECU_CARD_IBOX_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_IBOX_2026-03-28_P2.svg)

- Representative detailed signal flow: `NAV_AND_FAILSAFE_CONTEXT_TO_IBOX_ROUTE_SERVICE_FLAGS_SIGNAL_FLOW_2026-03-29`

![](svg/flows/signal/NAV_AND_FAILSAFE_CONTEXT_TO_IBOX_ROUTE_SERVICE_FLAGS_SIGNAL_FLOW_2026-03-29.svg)

### `SGW`

Publishes secure-gateway state for service routing and access-control visibility

![](svg/ecu_cards/ECU_CARD_SGW_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_SGW_2026-03-28_P2.svg)

- Representative detailed signal flow: `SERVICE_CONTEXT_TO_SGW_ROUTE_OWNER_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/SERVICE_CONTEXT_TO_SGW_ROUTE_OWNER_SIGNAL_FLOW_2026-03-28.svg)

### `V2X`

Owns emergency ingress context before ADAS and CGW perform prioritization

![](svg/ecu_cards/ECU_CARD_V2X_2026-03-28.svg)

![](svg/ecu_cards/ECU_CARD_V2X_2026-03-28_P2.svg)

- Representative detailed signal flow: `V2X_PRIORITY_ARBITRATION_SIGNAL_FLOW_2026-03-28`

![](svg/flows/signal/V2X_PRIORITY_ARBITRATION_SIGNAL_FLOW_2026-03-28.svg)


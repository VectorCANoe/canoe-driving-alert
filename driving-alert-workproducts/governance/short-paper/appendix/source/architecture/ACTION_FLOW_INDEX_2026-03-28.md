# Action Flow Index (2026-03-28)

Subtitle: Canonical behavior index for the 20 action-flow chapters.

This is the canonical action-flow summary pack for the official ECU master book.
It covers only the `FLOW_01~20` SVG-only behavior chapters used by the master-book body.
It is intentionally separate from the detailed signal-flow triplet layer under `flows/signal/*.puml`, `svg/flows/signal/<signal-flow>.svg`, and `png/flows/signal/*.png`.
Each flow is behavior-first and can be reused by multiple ECU sections in the book.

## ADAS

### `FLOW_06` Object Risk Fusion

- SVG: `svg/flows/action/FLOW_06_OBJECT_RISK_FUSION_2026-03-28.svg`
- Related ECU count: `26`
- Related ECU bank: `ADAS, AEB, AVM, BCW, DMS, FCA, FCAM, FRADAR, HWP, LCA, LDR, LDWS_LKAS, OMS, PKM, PUS, RPC, RRM, RSPA, SCC, SPAS, SPM, SRR_FL, SRR_FR, SRR_RL, SRR_RR, TRM`
- Summary: Radar, camera, lidar, and perception nodes are fused into one object-risk lane for ADAS warning and assist decisions.

### `FLOW_07` AEB Decel Intervention

- SVG: `svg/flows/action/FLOW_07_AEB_DECEL_INTERVENTION_2026-03-28.svg`
- Related ECU count: `7`
- Related ECU bank: `ADAS, AEB, EHB, ESC, FCA, SCC, VSM`
- Summary: AEB stop intent, decel profile, and downstream chassis response are connected as one intervention chain.

### `FLOW_08` Lane and Surround Keeping

- SVG: `svg/flows/action/FLOW_08_LANE_SURROUND_KEEPING_2026-03-28.svg`
- Related ECU count: `8`
- Related ECU bank: `ADAS, BCW, LCA, LDWS_LKAS, SRR_FL, SRR_FR, SRR_RL, SRR_RR`
- Summary: Lane keeping, blind-spot, and surround sensing work together to support steering and warning decisions.

### `FLOW_09` Parking and Surround Assist

- SVG: `svg/flows/action/FLOW_09_PARKING_SURROUND_ASSIST_2026-03-28.svg`
- Related ECU count: `9`
- Related ECU bank: `ADAS, AVM, PKM, PUS, RPC, RRM, RSPA, SPAS, SPM`
- Summary: Parking cameras, ultrasonic sensing, and parking controllers feed one parking-assist behavior chain.

### `FLOW_10` Driver Monitor and Occupant Risk

- SVG: `svg/flows/action/FLOW_10_DRIVER_MONITOR_OCCUPANT_2026-03-28.svg`
- Related ECU count: `2`
- Related ECU bank: `DMS, OMS`
- Summary: Driver state and occupant perception are fed into the warning lane before output arbitration happens.

## Backbone

### `FLOW_20` Backbone, Diagnostic, and Service Routing

- SVG: `svg/flows/action/FLOW_20_BACKBONE_DIAGNOSTIC_SERVICE_2026-03-28.svg`
- Related ECU count: `10`
- Related ECU bank: `CGW, DCM, EDR, ETHB, EXT_DIAG, IBOX, SGW, TEST_BAS, TEST_SCN, V2X`
- Summary: Gateway, backbone, diagnostics, and service-facing surfaces route runtime state without becoming hidden feature owners.

## Body and Comfort

### `FLOW_16` Body Ambient Warning Output

- SVG: `svg/flows/action/FLOW_16_BODY_AMBIENT_WARNING_2026-03-28.svg`
- Related ECU count: `12`
- Related ECU bank: `ADM, AFLS, AHLS, BCM, BIO, HLM, MIR, MSC, PTG, SRF, TGM, WIP`
- Summary: Body lighting, ambient, wiper, and exterior cues amplify the selected warning state in the comfort domain.

### `FLOW_17` Access, Security, and Entry

- SVG: `svg/flows/action/FLOW_17_ACCESS_SECURITY_ENTRY_2026-03-28.svg`
- Related ECU count: `11`
- Related ECU bank: `BCM, BSEC, CSM, DKEY, DOOR_FL, DOOR_FR, DOOR_RL, DOOR_RR, PAK, PGS, SMK`
- Summary: Key, access, security, and door controllers are connected into one vehicle-entry behavior chain.

### `FLOW_18` Comfort, Climate, and Seat

- SVG: `svg/flows/action/FLOW_18_COMFORT_CLIMATE_SEAT_2026-03-28.svg`
- Related ECU count: `5`
- Related ECU bank: `BCM, DATC, RATC, SEAT_DRV, SEAT_PASS`
- Summary: Climate and seat controllers are orchestrated as one comfort-domain runtime surface with body and HMI visibility.

## Display and Alert

### `FLOW_11` Navigation Zone Context Ingress

- SVG: `svg/flows/action/FLOW_11_NAV_ZONE_CONTEXT_INGRESS_2026-03-28.svg`
- Related ECU count: `8`
- Related ECU bank: `AMP, CLU, HUD, IVI, NAV, RSE, TMU, VCS`
- Summary: Map and telematics context enters the runtime and becomes zone-aware alert context for downstream selection and HMI.

### `FLOW_12` V2X Emergency Ingress

- SVG: `svg/flows/action/FLOW_12_V2X_EMERGENCY_INGRESS_2026-03-28.svg`
- Related ECU count: `5`
- Related ECU bank: `AMP, CGW, ETHB, HUD, V2X`
- Summary: Emergency-vehicle ingress arrives through the V2X lane and is routed into the warning decision chain.

### `FLOW_13` Alert Arbitration and Gate

- SVG: `svg/flows/action/FLOW_13_ALERT_ARBITRATION_GATE_2026-03-28.svg`
- Related ECU count: `8`
- Related ECU bank: `AMP, CGW, CLU, HUD, IVI, TMU, V2X, VCS`
- Summary: Multiple warning candidates are reduced into one selected alert with explicit gateway and display semantics.

### `FLOW_14` Cluster, HUD, and Audio Output

- SVG: `svg/flows/action/FLOW_14_CLUSTER_HUD_AUDIO_OUTPUT_2026-03-28.svg`
- Related ECU count: `6`
- Related ECU bank: `AMP, CLU, HUD, IVI, TMU, VCS`
- Summary: Selected warning state is rendered into cluster, HUD, and audio output without diverging message semantics.

### `FLOW_15` Service and Access HMI

- SVG: `svg/flows/action/FLOW_15_SERVICE_ACCESS_HMI_2026-03-28.svg`
- Related ECU count: `10`
- Related ECU bank: `CPAY, DKEY, IVI, NAV, OTA, PAK, PGS, RSE, TMU, VCS`
- Summary: Digital-key, payment, OTA, and related service surfaces are orchestrated through one HMI-facing service chain.

## Dynamics

### `FLOW_01` Steering Control Readback

- SVG: `svg/flows/action/FLOW_01_STEERING_CONTROL_READBACK_2026-03-28.svg`
- Related ECU count: `6`
- Related ECU bank: `CGW, CLU, ESC, MDPS, RWS, SAS`
- Summary: Manual steering input is normalized, published as steering state, and rendered back into the steering readback path.

### `FLOW_02` Brake Stability Response

- SVG: `svg/flows/action/FLOW_02_BRAKE_STABILITY_RESPONSE_2026-03-28.svg`
- Related ECU count: `8`
- Related ECU bank: `ABS, AEB, EHB, EPB, ESC, FCA, VCU, VSM`
- Summary: Brake request, AEB pressure intent, and stability outputs are synchronized across chassis brake owners and downstream readers.

### `FLOW_03` Propulsion Energy Status

- SVG: `svg/flows/action/FLOW_03_PROPULSION_ENERGY_STATUS_2026-03-28.svg`
- Related ECU count: `15`
- Related ECU bank: `BAT_BMS, CPC, DCDC, EMS, EOP, EWP, FPCM, INVERTER, ISG, LVR, MCU, OBC, TCU, VCU, _4WD`
- Summary: Powertrain and energy ECUs consolidate drive, torque, battery, and charging state into the central propulsion state lane.

### `FLOW_04` Cruise Speed Support

- SVG: `svg/flows/action/FLOW_04_CRUISE_SPEED_SUPPORT_2026-03-28.svg`
- Related ECU count: `4`
- Related ECU bank: `EMS, SCC, TCU, VCU`
- Summary: Cruise and longitudinal support state moves from support controllers into vehicle speed management and driver-facing outputs.

### `FLOW_05` Chassis Sensor Health

- SVG: `svg/flows/action/FLOW_05_CHASSIS_SENSOR_HEALTH_2026-03-28.svg`
- Related ECU count: `15`
- Related ECU bank: `ABS, ACU, ASM, CDC, ECS, EHB, EPB, ESC, MDPS, ODS, RWS, SAS, TPMS, VCU, VSM`
- Summary: Wheel, angle, suspension, and chassis leaf signals are collected so downstream control and visibility stay health-aware.

## Validation

### `FLOW_19` Validation Scenario Control

- SVG: `svg/flows/action/FLOW_19_VALIDATION_SCENARIO_CONTROL_2026-03-28.svg`
- Related ECU count: `2`
- Related ECU bank: `TEST_BAS, TEST_SCN`
- Summary: Scenario command, injected state, and verdict readback are kept inside a dedicated validation control story.


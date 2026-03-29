# ECU Master Book

This folder keeps the CANoe architecture master-book asset set for the current SIL baseline.

These files do not replace the canonical SoT under `driving-alert-workproducts/0301~0304`.
They are the reviewer-facing reading layer for:
- full ECU coverage
- grouped network views
- per-ECU network flow cards
- feature/action signal-flow companions

## Bundling Rule

- The PDF is built from one fixed story order:
  - overview maps
  - group SVGs
  - canonical action-flow SVGs
  - ECU catalog
- The ECU catalog is always paired by the same ECU:
  - `ECU_CARD_<ECU>_2026-03-28.svg` = page 1 overview card
  - `ECU_CARD_<ECU>_2026-03-28_P2.svg` = page 2 reference card
- Do not mix different ECU names across the pair.
  - Example: `ECU_CARD_ADAS_2026-03-28.svg` must be followed by `ECU_CARD_ADAS_2026-03-28_P2.svg`
  - `ECU_CARD_ADM_2026-03-28_P2.svg` is the pair for `ECU_CARD_ADM_2026-03-28.svg`, not for ADAS
- Flow charts are not attached randomly between ECU cards.
  - canonical flow SVGs are shown first as behavior chapters
  - ECU P1/P2 cards come later as the per-ECU appendix layer

## Official Working Path

- Official tracked build root: `canoe/docs/architecture/master_book/`
- Official commands:
  - `python tools/build_master_book_asset_pack.py`
  - `python tools/render_master_book_pdf.py`
- The former internal mirror under `canoe/AGENT/canoe/docs/architecture/` is retired.
- Use this folder as the single architecture-master-book SoT.

## Read Order

1. `ECU_METADATA_BOOK_2026-03-28.md`
2. `ECU_METADATA_BOOK_2026-03-28.pdf`
3. `ECU_CARD_INDEX_2026-03-28.md`
4. `ECU_NETWORK_MASTER_MATRIX_2026-03-28.md`
5. `ECU_GROUP_NETWORK_VIEW_2026-03-28.md`
6. `svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_2026-03-28.svg`
7. `svg/CORE_COUPLED_ECU_GROUP_MAP_2026-03-28.svg`
8. `svg/GROUP_01_BASE_VEHICLE_DYNAMICS_2026-03-28.svg`
9. `svg/GROUP_02_ADAS_AEB_BRAKE_ASSIST_2026-03-28.svg`
10. `svg/GROUP_03_DISPLAY_WARNING_AUDIO_2026-03-28.svg`
11. `svg/GROUP_04_BODY_COMFORT_AMBIENT_2026-03-28.svg`
12. `svg/GROUP_05_VALIDATION_SCENARIO_2026-03-28.svg`
13. `svg/GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_2026-03-28.svg`
14. `svg/ecu_cards/*.svg`
15. `svg/ecu_cards/ECU_CARD_VCU_2026-03-28.svg`
16. `svg/ecu_cards/ECU_CARD_ESC_2026-03-28.svg`
17. `svg/ecu_cards/ECU_CARD_ADAS_2026-03-28.svg`
18. `svg/ecu_cards/ECU_CARD_AEB_2026-03-28.svg`
19. `svg/ecu_cards/ECU_CARD_BCM_2026-03-28.svg`
20. `svg/ecu_cards/ECU_CARD_CGW_2026-03-28.svg`
21. `svg/ecu_cards/ECU_CARD_IVI_2026-03-28.svg`
22. `svg/ecu_cards/ECU_CARD_TEST_SCN_2026-03-28.svg`
23. `flows/*.puml`
24. `svg/flows/*.svg`
25. `png/flows/*.png`
26. `tools/build_master_book_asset_pack.py`
27. `tools/render_master_book_pdf.py`

## Existing Context Notes

- `project_explained.md`
- `emergency_system_explained.md`

## Source Rules

- Official functional/network/message/sysvar SoT stays in:
  - `driving-alert-workproducts/0301_SysFuncAnalysis.md`
  - `driving-alert-workproducts/0302_NWflowDef.md`
  - `driving-alert-workproducts/0303_Communication_Specification.md`
  - `driving-alert-workproducts/0304_System_Variables.md`
- Runtime truth for owner/writer/consumer remains in:
  - `canoe/src/capl/**`
  - `canoe/cfg/channel_assign/**`
- Test asset linkage is derived from:
  - `canoe/tests/modules/test_units/**`

## Publishing Intent

This package is the official CANoe-side master-book surface for later PDF, appendix, and presentation extraction.
Use it as the visual companion to:
- `driving-alert-workproducts/0301_SysFuncAnalysis.md`
- `driving-alert-workproducts/0302_NWflowDef.md`
- `driving-alert-workproducts/0303_Communication_Specification.md`
- `driving-alert-workproducts/0304_System_Variables.md`

## SVG Set

- `svg/OVERVIEW_RUNTIME_101_ECU_DOMAIN_MAP_2026-03-28.svg`
  - full 101-ECU domain overview
- `svg/CORE_COUPLED_ECU_GROUP_MAP_2026-03-28.svg`
  - high-level coupled runtime risk map
- `svg/GROUP_01_BASE_VEHICLE_DYNAMICS_2026-03-28.svg`
- `svg/GROUP_02_ADAS_AEB_BRAKE_ASSIST_2026-03-28.svg`
- `svg/GROUP_03_DISPLAY_WARNING_AUDIO_2026-03-28.svg`
- `svg/GROUP_04_BODY_COMFORT_AMBIENT_2026-03-28.svg`
- `svg/GROUP_05_VALIDATION_SCENARIO_2026-03-28.svg`
- `svg/GROUP_06_BACKBONE_GATEWAY_DIAGNOSTICS_2026-03-28.svg`

## Metadata Book

- `ECU_METADATA_BOOK_2026-03-28.md`
  - figure-first master markdown asset for later PDF/presentation derivation
- `ECU_METADATA_BOOK_2026-03-28.html`
  - print-ready HTML render target
- `ECU_METADATA_BOOK_2026-03-28.pdf`
  - generated PDF book for shared review
- `ECU_CARD_INDEX_2026-03-28.md`
  - generated index for all per-ECU network flow cards
- `data/ECU_METADATA_DATASET_2026-03-28.json`
  - machine-readable source dataset for regenerated visuals and later appendix promotion
- `data/ECU_FUNCTION_STATEMENTS.json`
  - curated per-ECU functional one-liners used by the HTML and PDF book
- `data/ECU_RISK_NOTES.json`
  - curated per-ECU risk focus notes used by the HTML and PDF book

## Build Tools

- `tools/build_master_book_asset_pack.py`
  - tracked generator for datasets, grouped figures, action-flow pack, and 101 ECU cards
- `tools/render_master_book_pdf.py`
  - tracked HTML/PDF renderer for the figure-first master book

## Prototype Archive

- `prototypes/card_prototypes/*.svg`
  - archived layout studies promoted from the old internal mirror
  - not part of the standard PDF build order
- `references/image-copy.png`
  - retained visual reference from the earlier design-exploration phase

## ECU Flow Cards

- `svg/ecu_cards/ECU_CARD_VCU_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_ESC_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_ADAS_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_AEB_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_BCM_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_CGW_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_IVI_2026-03-28.svg`
- `svg/ecu_cards/ECU_CARD_TEST_SCN_2026-03-28.svg`
- `svg/ecu_cards/*.svg`
  - full generated 101-ECU OEM-style network flow card pack

## Action Signal Flows

- `flows/STEERING_TURN_SIGNAL_FLOW_2026-03-28.puml`
  - master source for the steering-turn feature/message sequence
- `flows/AEB_BRAKE_ASSIST_SIGNAL_FLOW_2026-03-28.puml`
  - master source for AEB decel-profile to brake-assist overlay flow
- `flows/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.puml`
  - master source for manual/automatic ambient lighting ownership flow
- `flows/SCENARIO_START_STOP_SIGNAL_FLOW_2026-03-28.puml`
  - master source for scenario start/stop lifecycle and lamp flow
- `flows/ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.puml`
  - master source for vehicle longitudinal owner/brake downstream flow
- `flows/ROUTE_WARNING_TO_HMI_SIGNAL_FLOW_2026-03-28.puml`
  - master source for route-context warning to IVI / CLU / AMP flow
- `flows/EMERGENCY_INGRESS_TO_OUTPUT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for V2X emergency ingress to rendered warning flow
- `flows/BRAKE_LAMP_AND_ABS_SIGNAL_FLOW_2026-03-28.puml`
  - master source for brake-lamp and ABS downstream state flow
- `flows/OBJECT_RISK_TO_WARNING_SIGNAL_FLOW_2026-03-28.puml`
  - master source for object-risk decision to warning-render flow
- `flows/AUDIO_DUCKING_FROM_ALERT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for effective alert to audio ducking flow
- `flows/FAILSAFE_ESCALATION_TO_OUTPUT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for CGW fail-safe escalation to IVI / CLU output flow
- `flows/CRUISE_SET_TO_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.puml`
  - master source for cruise command to longitudinal owner chain
- `flows/OBJECT_TO_AEB_REQUEST_SIGNAL_FLOW_2026-03-28.puml`
  - master source for object-risk to FCA/AEB brake request flow
- `flows/NAV_CONTEXT_TO_SPEED_LIMIT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for NAV context to speed-limit/runtime consumer flow
- `flows/V2X_PRIORITY_ARBITRATION_SIGNAL_FLOW_2026-03-28.puml`
  - master source for V2X emergency priority arbitration flow
- `flows/CLUSTER_TEXT_RENDER_PATH_SIGNAL_FLOW_2026-03-28.puml`
  - master source for effective alert to cluster warning text render path
- `flows/BODY_LOCK_TO_AMBIENT_CHANGE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for body-access command to BCM ambient/body publication flow
- `flows/WARNING_BEEP_TO_AUDIO_FOCUS_SIGNAL_FLOW_2026-03-28.puml`
  - master source for warning-beep derivation to audio-focus and ducking flow
- `flows/SCENARIO_LOCK_TO_MANUAL_OVERRIDE_RELEASE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for scenario lock dominance and manual-override release flow
- `flows/SEAT_BELT_OVERRIDE_TO_WARNING_SIGNAL_FLOW_2026-03-28.puml`
  - master source for belt toggle override to BCM warning publication flow
- `flows/TURN_SIGNAL_TO_BODY_GATEWAY_SIGNAL_FLOW_2026-03-28.puml`
  - master source for turn-command pulse to BCM body-gateway lamp flow
- `flows/FAILSAFE_BLOCKED_CONTEXT_TO_DIAG_PATH_SIGNAL_FLOW_2026-03-28.puml`
  - master source for blocked fail-safe context to diagnostic/evidence path flow
- `flows/DOOR_OPEN_WARN_TO_COMFORT_PROFILE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for door-open warning to comfort-profile publication flow
- `flows/AMBIENT_PULSE_PHASE_RENDER_PATH_SIGNAL_FLOW_2026-03-28.puml`
  - master source for ambient pulse-phase to cabin animation render flow
- `flows/DIAG_ROUTE_OWNER_TO_GATEWAY_OPEN_SIGNAL_FLOW_2026-03-28.puml`
  - master source for diagnostic route-owner and gateway-open flow
- `flows/PAAK_ACCESS_TO_DOOR_COMMAND_SIGNAL_FLOW_2026-03-28.puml`
  - master source for PAAK access condition to door-command publication flow
- `flows/TMU_REMOTE_CLIMATE_TO_COMFORT_PROFILE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for TMU/HVAC remote climate to comfort-profile flow
- `flows/OBJECT_CONFIDENCE_TO_FAILSAFE_GATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for object-confidence to effective fail-safe gate flow
- `flows/PAAK_AUTH_TO_CHILD_LOCK_SIGNAL_FLOW_2026-03-28.puml`
  - master source for PAAK/drive context to BCM child-lock enforcement flow
- `flows/HVAC_STALE_INPUT_TO_COMFORT_ERROR_SIGNAL_FLOW_2026-03-28.puml`
  - master source for HVAC/TMU stale-input detection to comfort-error publication flow
- `flows/NAV_ROUTE_CLASS_TO_HIGHWAY_READY_SIGNAL_FLOW_2026-03-28.puml`
  - master source for NAV route class to FCAM/HWP readiness flow
- `flows/PAAK_INPUT_STALE_TO_ACCESS_BLOCK_SIGNAL_FLOW_2026-03-28.puml`
  - master source for PAAK freshness loss to blocked door-access command flow
- `flows/SEAT_COMFORT_TO_MASSAGE_INTENSITY_SIGNAL_FLOW_2026-03-28.puml`
  - master source for seat comfort commands to massage-intensity publication flow
- `flows/FAILSAFE_MODE_TO_EDR_STORAGE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for fail-safe and alert severity to EDR storage escalation flow
- `flows/AMBIENT_MODE_TO_IVI_RENDER_SIGNAL_FLOW_2026-03-28.puml`
  - master source for BCM ambient ownership to IVI render seam flow
- `flows/HIGHWAY_READY_TO_CONTROL_ACTIVATION_SIGNAL_FLOW_2026-03-28.puml`
  - master source for highway readiness to long/lat control activation flow
- `flows/FAILSAFE_TO_DIAGNOSTIC_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for core fail-safe context to DCM diagnostic-state flow
- `flows/NAV_ROUTE_CLASS_TO_LANE_MODEL_VALID_SIGNAL_FLOW_2026-03-28.puml`
  - master source for NAV route class to FCAM lane-model-valid publication flow
- `flows/BOUNDARY_FAILSAFE_TO_GATEWAY_SECURITY_SIGNAL_FLOW_2026-03-28.puml`
  - master source for boundary/fail-safe context to SGW security seams flow
- `flows/ROUTE_ACTIVITY_TO_IBOX_LINK_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for route activity to IBOX link-state publication flow
- `flows/OBJECT_RISK_TO_FCA_REQUEST_SIGNAL_FLOW_2026-03-28.puml`
  - master source for object-risk and decel intent to FCA request publication flow
- `flows/PATH_READY_TO_LIDAR_TARGET_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for path readiness to LDR target-state publication flow
- `flows/DIAG_STAGE_TO_ETHB_SERVICE_SECURITY_SIGNAL_FLOW_2026-03-28.puml`
  - master source for diagnostic stage to ETHB route/service/security flow
- `flows/OBJECT_INPUT_TO_FCAM_CAMERA_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for object/nav/path context to FCAM camera-state publication flow
- `flows/DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28.puml`
  - master source for DMS attention context to HWP driver-monitor request flow
- `flows/SERVICE_CONTEXT_TO_SGW_ROUTE_OWNER_SIGNAL_FLOW_2026-03-28.puml`
  - master source for service context to SGW route-owner/security seam flow
- `flows/REMOTE_CLIMATE_TO_DATC_HVAC_OUTPUT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for TMU remote-climate context to DATC HVAC output flow
- `flows/ACCESS_AUTH_TO_REAR_DOOR_UNLOCK_SIGNAL_FLOW_2026-03-28.puml`
  - master source for access authorization to rear-door unlock enforcement flow
- `flows/AUDIO_FOCUS_TO_VCS_TTS_SIGNAL_FLOW_2026-03-28.puml`
  - master source for audio-focus and TMU context to VCS TTS/voice flow
- `flows/TMU_SERVICE_TO_REMOTE_CLIMATE_REQUEST_SIGNAL_FLOW_2026-03-28.puml`
  - master source for connectivity and IVI context to TMU remote-climate request flow
- `flows/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for ambient mode to BCM cabin-light publication flow
- `flows/RISK_LEVEL_TO_SCC_CRUISE_MODULATION_SIGNAL_FLOW_2026-03-28.puml`
  - master source for risk/fail-safe context to SCC cruise modulation flow
- `flows/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.puml`
  - master source for alert/emergency context to IVI warning-beep seam flow
- `flows/AUDIO_FOCUS_TO_AMP_DUCKING_SIGNAL_FLOW_2026-03-28.puml`
  - master source for audio focus and speech context to AMP ducking flow
- `flows/AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for AFLS input and speed to AHLS high-beam-permit flow
- `flows/STEERING_INPUT_TO_MDPS_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for steering input and speed to MDPS state/torque flow
- `flows/AEB_PRESSURE_TO_EHB_COMMAND_SIGNAL_FLOW_2026-03-28.puml`
  - master source for brake and AEB overlay to EHB pressure-command flow
- `flows/STEERING_ANGLE_TO_CLU_FRAME_SIGNAL_FLOW_2026-03-28.puml`
  - master source for steering angle to CLU steering-frame render flow
- `flows/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.puml`
  - master source for ESC/AEB input to VSM intervention publication flow
- `flows/MERGE_CONFLICT_TO_SRR_SIDE_RISK_SIGNAL_FLOW_2026-03-28.puml`
  - master source for merge-conflict context to SRR side-risk publication flow
- `flows/BOUNDARY_STAGE_TO_DCM_SERVICE_RESPONSE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for boundary diagnostic stage to DCM service-response flow
- `flows/TMU_ACCESS_TO_DKEY_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for TMU service and proximity context to DKEY access-state publication flow
- `flows/BATTERY_SOC_TO_BMS_PACK_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for battery SOC/charge input to BAT_BMS pack-state publication flow
- `flows/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.puml`
  - master source for fail-safe and emergency context to VCU routing-policy publication flow
- `flows/DKEY_ACCESS_TO_SMK_IMMOBILIZER_SIGNAL_FLOW_2026-03-28.puml`
  - master source for DKEY access publication to SMK immobilizer/key-auth flow
- `flows/TMU_DKEY_TO_PAAK_STATE_SIGNAL_FLOW_2026-03-28.puml`
  - master source for DKEY and TMU proximity context to PAK state publication flow
- `flows/BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28.puml`
  - master source for BAT_BMS pack-state publication to CPC charge-port flow
- `flows/OBC_INPUT_TO_CPC_CHARGE_ENABLE_SIGNAL_FLOW_2026-03-29.puml`
  - master source for OBC charger state to CPC charge-enable publication flow
- `flows/DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29.puml`
  - master source for DKEY and immobilizer authorization to DOOR_FL unlock/state flow
- `flows/VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29.puml`
  - master source for VCU vehicle-mode publication to ISG state/restart flow
- `flows/DKEY_ACCESS_TO_TGM_TAILGATE_STATE_SIGNAL_FLOW_2026-03-29.puml`
  - master source for DKEY access and tailgate control to TGM tailgate-state flow
- `flows/VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29.puml`
  - master source for VCU vehicle-mode publication to TCU shift-state flow
- `flows/FUEL_BATTERY_TO_ISG_RESTART_READY_SIGNAL_FLOW_2026-03-29.puml`
  - master source for fuel-battery and vehicle context to ISG restart-ready flow
- `flows/STEERING_INPUT_TO_SAS_ANGLE_RAW_SIGNAL_FLOW_2026-03-29.puml`
  - master source for steering input and vehicle speed to SAS raw-angle flow
- `flows/TAILGATE_CONTROL_TO_TGM_POSITION_SIGNAL_FLOW_2026-03-29.puml`
  - master source for tailgate control request to TGM position/power-state flow
- `flows/GEAR_INPUT_TO_TCU_SHIFT_SLIP_SIGNAL_FLOW_2026-03-29.puml`
  - master source for gear input and drive context to TCU shift-slip flow
- `svg/flows/STEERING_TURN_SIGNAL_FLOW_2026-03-28.svg`
  - reviewer-facing styled SVG companion for the same steering-turn runtime path
- `svg/flows/AEB_BRAKE_ASSIST_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/SCENARIO_START_STOP_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/ROUTE_WARNING_TO_HMI_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/EMERGENCY_INGRESS_TO_OUTPUT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/BRAKE_LAMP_AND_ABS_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/OBJECT_RISK_TO_WARNING_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AUDIO_DUCKING_FROM_ALERT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/FAILSAFE_ESCALATION_TO_OUTPUT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/CRUISE_SET_TO_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/OBJECT_TO_AEB_REQUEST_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/NAV_CONTEXT_TO_SPEED_LIMIT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/V2X_PRIORITY_ARBITRATION_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/CLUSTER_TEXT_RENDER_PATH_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/BODY_LOCK_TO_AMBIENT_CHANGE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/WARNING_BEEP_TO_AUDIO_FOCUS_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/SCENARIO_LOCK_TO_MANUAL_OVERRIDE_RELEASE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/SEAT_BELT_OVERRIDE_TO_WARNING_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/TURN_SIGNAL_TO_BODY_GATEWAY_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/FAILSAFE_BLOCKED_CONTEXT_TO_DIAG_PATH_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/DOOR_OPEN_WARN_TO_COMFORT_PROFILE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AMBIENT_PULSE_PHASE_RENDER_PATH_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/DIAG_ROUTE_OWNER_TO_GATEWAY_OPEN_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/PAAK_ACCESS_TO_DOOR_COMMAND_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/TMU_REMOTE_CLIMATE_TO_COMFORT_PROFILE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/OBJECT_CONFIDENCE_TO_FAILSAFE_GATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/PAAK_AUTH_TO_CHILD_LOCK_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/HVAC_STALE_INPUT_TO_COMFORT_ERROR_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/NAV_ROUTE_CLASS_TO_HIGHWAY_READY_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/PAAK_INPUT_STALE_TO_ACCESS_BLOCK_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/SEAT_COMFORT_TO_MASSAGE_INTENSITY_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/FAILSAFE_MODE_TO_EDR_STORAGE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AMBIENT_MODE_TO_IVI_RENDER_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/HIGHWAY_READY_TO_CONTROL_ACTIVATION_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/FAILSAFE_TO_DIAGNOSTIC_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/NAV_ROUTE_CLASS_TO_LANE_MODEL_VALID_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/BOUNDARY_FAILSAFE_TO_GATEWAY_SECURITY_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/ROUTE_ACTIVITY_TO_IBOX_LINK_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/OBJECT_RISK_TO_FCA_REQUEST_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/PATH_READY_TO_LIDAR_TARGET_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/DIAG_STAGE_TO_ETHB_SERVICE_SECURITY_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/OBJECT_INPUT_TO_FCAM_CAMERA_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/SERVICE_CONTEXT_TO_SGW_ROUTE_OWNER_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/REMOTE_CLIMATE_TO_DATC_HVAC_OUTPUT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/ACCESS_AUTH_TO_REAR_DOOR_UNLOCK_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AUDIO_FOCUS_TO_VCS_TTS_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/TMU_SERVICE_TO_REMOTE_CLIMATE_REQUEST_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/RISK_LEVEL_TO_SCC_CRUISE_MODULATION_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AUDIO_FOCUS_TO_AMP_DUCKING_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/STEERING_INPUT_TO_MDPS_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/AEB_PRESSURE_TO_EHB_COMMAND_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/STEERING_ANGLE_TO_CLU_FRAME_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/MERGE_CONFLICT_TO_SRR_SIDE_RISK_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/BOUNDARY_STAGE_TO_DCM_SERVICE_RESPONSE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/TMU_ACCESS_TO_DKEY_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/BATTERY_SOC_TO_BMS_PACK_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/DKEY_ACCESS_TO_SMK_IMMOBILIZER_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/TMU_DKEY_TO_PAAK_STATE_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28.svg`
- `svg/flows/OBC_INPUT_TO_CPC_CHARGE_ENABLE_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/DKEY_ACCESS_TO_TGM_TAILGATE_STATE_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/FUEL_BATTERY_TO_ISG_RESTART_READY_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/STEERING_INPUT_TO_SAS_ANGLE_RAW_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/TAILGATE_CONTROL_TO_TGM_POSITION_SIGNAL_FLOW_2026-03-29.svg`
- `svg/flows/GEAR_INPUT_TO_TCU_SHIFT_SLIP_SIGNAL_FLOW_2026-03-29.svg`
- `png/flows/STEERING_TURN_SIGNAL_FLOW_2026-03-28.png`
  - PlantUML-rendered bitmap preview for direct insertion into PDF/PPT environments
- `png/flows/AEB_BRAKE_ASSIST_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AMBIENT_LIGHTING_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/SCENARIO_START_STOP_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/ACCEL_BRAKE_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/ROUTE_WARNING_TO_HMI_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/EMERGENCY_INGRESS_TO_OUTPUT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/BRAKE_LAMP_AND_ABS_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/OBJECT_RISK_TO_WARNING_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AUDIO_DUCKING_FROM_ALERT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/FAILSAFE_ESCALATION_TO_OUTPUT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/CRUISE_SET_TO_LONGITUDINAL_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/OBJECT_TO_AEB_REQUEST_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/NAV_CONTEXT_TO_SPEED_LIMIT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/V2X_PRIORITY_ARBITRATION_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/CLUSTER_TEXT_RENDER_PATH_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/BODY_LOCK_TO_AMBIENT_CHANGE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/WARNING_BEEP_TO_AUDIO_FOCUS_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/SCENARIO_LOCK_TO_MANUAL_OVERRIDE_RELEASE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/SEAT_BELT_OVERRIDE_TO_WARNING_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/TURN_SIGNAL_TO_BODY_GATEWAY_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/FAILSAFE_BLOCKED_CONTEXT_TO_DIAG_PATH_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/DOOR_OPEN_WARN_TO_COMFORT_PROFILE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AMBIENT_PULSE_PHASE_RENDER_PATH_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/DIAG_ROUTE_OWNER_TO_GATEWAY_OPEN_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/PAAK_ACCESS_TO_DOOR_COMMAND_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/TMU_REMOTE_CLIMATE_TO_COMFORT_PROFILE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/OBJECT_CONFIDENCE_TO_FAILSAFE_GATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/PAAK_AUTH_TO_CHILD_LOCK_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/HVAC_STALE_INPUT_TO_COMFORT_ERROR_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/NAV_ROUTE_CLASS_TO_HIGHWAY_READY_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/PAAK_INPUT_STALE_TO_ACCESS_BLOCK_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/SEAT_COMFORT_TO_MASSAGE_INTENSITY_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/FAILSAFE_MODE_TO_EDR_STORAGE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AMBIENT_MODE_TO_IVI_RENDER_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/HIGHWAY_READY_TO_CONTROL_ACTIVATION_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/FAILSAFE_TO_DIAGNOSTIC_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/NAV_ROUTE_CLASS_TO_LANE_MODEL_VALID_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/BOUNDARY_FAILSAFE_TO_GATEWAY_SECURITY_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/ROUTE_ACTIVITY_TO_IBOX_LINK_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/OBJECT_RISK_TO_FCA_REQUEST_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/PATH_READY_TO_LIDAR_TARGET_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/DIAG_STAGE_TO_ETHB_SERVICE_SECURITY_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/OBJECT_INPUT_TO_FCAM_CAMERA_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/DMS_ATTENTION_TO_HWP_DRIVER_MONITOR_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/SERVICE_CONTEXT_TO_SGW_ROUTE_OWNER_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/REMOTE_CLIMATE_TO_DATC_HVAC_OUTPUT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/ACCESS_AUTH_TO_REAR_DOOR_UNLOCK_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AUDIO_FOCUS_TO_VCS_TTS_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/TMU_SERVICE_TO_REMOTE_CLIMATE_REQUEST_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AMBIENT_MODE_TO_BCM_CABIN_LIGHT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/RISK_LEVEL_TO_SCC_CRUISE_MODULATION_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/ALERT_CONTEXT_TO_IVI_WARNING_BEEP_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AUDIO_FOCUS_TO_AMP_DUCKING_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AFLS_INPUT_TO_AHLS_HIGH_BEAM_PERMIT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/STEERING_INPUT_TO_MDPS_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/AEB_PRESSURE_TO_EHB_COMMAND_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/STEERING_ANGLE_TO_CLU_FRAME_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/ESC_AEB_INPUT_TO_VSM_INTERVENTION_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/MERGE_CONFLICT_TO_SRR_SIDE_RISK_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/BOUNDARY_STAGE_TO_DCM_SERVICE_RESPONSE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/TMU_ACCESS_TO_DKEY_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/BATTERY_SOC_TO_BMS_PACK_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/FAILSAFE_CONTEXT_TO_VCU_ROUTING_POLICY_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/DKEY_ACCESS_TO_SMK_IMMOBILIZER_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/TMU_DKEY_TO_PAAK_STATE_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/BAT_BMS_TO_CPC_CHARGE_PORT_SIGNAL_FLOW_2026-03-28.png`
- `png/flows/OBC_INPUT_TO_CPC_CHARGE_ENABLE_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/DKEY_ACCESS_TO_DOOR_FL_UNLOCK_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/VCU_VEHICLE_MODE_TO_ISG_STATE_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/DKEY_ACCESS_TO_TGM_TAILGATE_STATE_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/VCU_VEHICLE_MODE_TO_TCU_SHIFT_STATE_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/FUEL_BATTERY_TO_ISG_RESTART_READY_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/STEERING_INPUT_TO_SAS_ANGLE_RAW_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/TAILGATE_CONTROL_TO_TGM_POSITION_SIGNAL_FLOW_2026-03-29.png`
- `png/flows/GEAR_INPUT_TO_TCU_SHIFT_SLIP_SIGNAL_FLOW_2026-03-29.png`

## Flow Asset Rule

Each action signal flow should keep this 3-artifact structure:

- `flows/*.puml`
  - editable master sequence source
- `svg/flows/*.svg`
  - curated reviewer-facing vector view
- `png/flows/*.png`
  - immediately previewable bitmap render of the PUML source

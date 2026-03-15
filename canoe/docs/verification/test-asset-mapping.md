# Test Asset Mapping

> [!IMPORTANT]
> This document is the current development baseline for CANoe SIL test construction.
> It may change as native CANoe test assets, oracle seams, and evidence collection are finalized.

## 1. Purpose

This document defines the official mapping from reviewer-facing test IDs in:

- `driving-alert-workproducts/05_Unit_Test.md`
- `driving-alert-workproducts/06_Integration_Test.md`
- `driving-alert-workproducts/07_System_Test.md`

to:

- native CANoe test asset candidates
- primary oracle sources
- primary evidence sources
- current diagnostic need

This is the implementation-side verification bridge between the official `05/06/07` tables and the executable CANoe SIL test surface.

## 2. Mapping rules

1. `05` is mapped as controller, input, and output verification for the product baseline.
2. `06` is mapped as integrated function verification across runtime boundaries.
3. `07` is mapped as end-user and whole-vehicle scenario verification.
4. `Diagnostic Needed?` uses only `Yes` and `No`.
5. `Yes` is reserved for verdicts that remain weak without explicit diagnostic or security state visibility.
6. Repeated simulator preset rows may be grouped where the native asset candidate, oracle type, and evidence type are identical.

## 3. Unit Test mapping

| ID | Candidate native asset | Primary oracle | Primary evidence | Diagnostic Needed? |
|---|---|---|---|---|
| `UT_001` | `TC_CANOE_UT_CORE_001_CGW_CHS_GW` | forwarded vehicle-state seam | native report + trace + `verification_log.csv` | `No` |
| `UT_002` | `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW` | forwarded navigation-context seam | native report + trace + `verification_log.csv` | `No` |
| `UT_003` | `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` | selected warning state | native report + sysvar snapshot + panel capture | `No` |
| `UT_004` | `TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN` | emergency state + timeout clear | native report + trace + sysvar snapshot | `No` |
| `UT_005` | `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST` | arbitration result and decel-assist state | native report + sysvar snapshot + panel capture | `No` |
| `UT_006` | `TC_CANOE_UT_EXT_001_OBJECT_RISK` | object-risk state and downgrade state | native report + trace + event log | `No` |
| `UT_007` | `TC_CANOE_UT_EXT_002_CLU_CONTEXT_ADJUST` | rendered warning context | native report + cluster capture + sysvar snapshot | `No` |
| `UT_008` | `TC_CANOE_UT_EXT_003_DOMAIN_BOUNDARY_FAILSAFE` | fail-safe entry state and boundary-health state | native report + sysvar snapshot + trace + write window | `No` |
| `UT_009` | `TC_CANOE_UT_CORE_004_NAV_CTX_MGR` | zone context state | native report + sysvar snapshot | `No` |
| `UT_010` | `TC_CANOE_UT_CORE_005_EMS_ALERT_TXRX` | emergency tx/rx state and timeout state | native report + CAN/Ethernet trace + write window | `No` |
| `UT_011` | `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` | final selected warning state | native report + sysvar snapshot + panel capture | `No` |
| `UT_012` | `TC_CANOE_UT_CORE_007_BODY_GW_ROUTE` | ambient route state | native report + trace + ambient capture | `No` |
| `UT_013` | `TC_CANOE_UT_CORE_008_IVI_GW_ROUTE` | cluster route state | native report + trace + cluster capture | `No` |
| `UT_014` | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` | ambient color and pattern state | native report + panel capture + screenshot | `No` |
| `UT_015` | `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` | warning text and direction state | native report + cluster capture + screenshot | `No` |
| `UT_016` | `TC_CANOE_UT_EXT_004_CHS_BRAKE_EXT` | brake-related context state | native report + trace + sysvar snapshot | `No` |
| `UT_017` | `TC_CANOE_UT_EXT_005_CHS_DYNAMICS_EXT` | chassis-context state | native report + trace + sysvar snapshot | `No` |
| `UT_018` | `TC_CANOE_UT_EXT_006_BODY_ENTRY_EXIT` | door and tailgate context state | native report + trace + sysvar snapshot | `No` |
| `UT_019` | `TC_CANOE_UT_EXT_007_BODY_OCCUPANT_PROTECTION` | occupant-protection context state | native report + trace + sysvar snapshot | `No` |
| `UT_020` | `TC_CANOE_UT_EXT_008_BODY_COMFORT` | comfort-context state | native report + trace + sysvar snapshot | `No` |
| `UT_021` | `TC_CANOE_UT_EXT_009_IVI_DISPLAY_SERVICE` | display/service context state | native report + sysvar snapshot + panel capture | `No` |
| `UT_022` | `TC_CANOE_UT_EXT_010_IVI_SERVICE_ACCESS` | service-access context state | native report + sysvar snapshot + trace | `No` |
| `UT_023` | `TC_CANOE_UT_EXT_011_ADAS_DRIVE_ASSIST` | drive-assist context state | native report + sysvar snapshot + trace | `No` |
| `UT_024` | `TC_CANOE_UT_EXT_012_ADAS_PARKING_PERCEPTION` | parking/perception context state | native report + sysvar snapshot + trace | `No` |
| `UT_025` | `TC_CANOE_UT_EXT_013_WARNING_DELIVERY_BOUNDARY` | delivery-health and fail-safe state | native report + trace + write window + sysvar snapshot | `No` |
| `UT_026` | `TC_CANOE_UT_EXT_014_DOMAIN_ROUTER_PROPULSION` | propulsion-context state | native report + trace + sysvar snapshot | `No` |
| `UT_027` | `TC_CANOE_UT_EXT_015_DOMAIN_ROUTER_POWER_CHARGE` | power/charge context state | native report + trace + sysvar snapshot | `No` |
| `UT_028`-`UT_030` | `TEST_SCN core input presets` | stimulus-ack and injected input state | write window + trace + preset log | `No` |
| `UT_031`-`UT_035` | `TEST_SCN chassis/body-state presets` | input injection state | write window + trace + preset log | `No` |
| `UT_036`-`UT_048` | `TEST_SCN body/comfort-state presets` | input injection state | write window + trace + preset log | `No` |
| `UT_049`-`UT_051` | `TEST_SCN display/audio/service presets` | input injection state | write window + trace + preset log | `No` |
| `UT_052`-`UT_061` | `TEST_SCN adas/parking/perception presets` | input injection state | write window + trace + preset log | `No` |
| `UT_062` | `TEST_SCN IBOX service preset` | service-state injection | write window + trace + preset log | `No` |
| `UT_063` | `TC_CANOE_UT_EXT_016_SGW_SECURITY_STATE` | security-state injection | write window + trace + sysvar snapshot | `Yes` |
| `UT_064` | `TC_CANOE_UT_EXT_017_DCM_DIAGNOSTIC_STATE` | diagnostic-state injection | write window + trace + sysvar snapshot | `Yes` |
| `UT_065`-`UT_069` | `TEST_SCN backbone/powertrain presets` | input injection state | write window + trace + preset log | `No` |
| `UT_070` | `TC_CANOE_UT_OUT_001_BCM_AMBIENT` | ambient output render state | panel capture + screenshot + native report | `No` |
| `UT_071` | `TC_CANOE_UT_OUT_002_IVI_HMI` | HMI output state | panel capture + screenshot + native report | `No` |
| `UT_072` | `TC_CANOE_UT_OUT_003_CLU_DISPLAY` | cluster display render state | cluster capture + screenshot + native report | `No` |
| `UT_073` | `TC_CANOE_UT_OUT_004_HUD_DISPLAY` | HUD render state | HUD capture + screenshot + native report | `No` |
| `UT_074` | `TC_CANOE_UT_OUT_005_AMP_AUDIO` | audio-guide state | write window + audio state capture + native report | `No` |
| `UT_075` | `TC_CANOE_UT_OUT_006_DECEL_ASSIST_REQ` | decel-assist request state | native report + trace + sysvar snapshot | `No` |
| `UT_076` | `TC_CANOE_UT_OUT_007_POLICE_TX` | external tx frame observation | Ethernet trace + write window + `verification_log.csv` | `No` |
| `UT_077` | `TC_CANOE_UT_OUT_008_AMBULANCE_TX` | external tx frame observation | Ethernet trace + write window + `verification_log.csv` | `No` |

## 4. Integration Test mapping

| ID | Candidate native asset | Primary oracle | Primary evidence | Diagnostic Needed? |
|---|---|---|---|---|
| `IT_001` | `TC_CANOE_IT_CORE_001_BASE_ACTIVATION` | warning activation/inactivation state | native report + sysvar snapshot + panel capture | `No` |
| `IT_002` | `TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH` | zone-warning result state | native report + trace + panel capture | `No` |
| `IT_003` | `TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH` | highway-warning trigger and clear state | native report + sysvar snapshot + panel capture | `No` |
| `IT_004` | `TC_CANOE_IT_V2_001_POLICE_RX` | police-warning result state | native report + trace + panel capture | `No` |
| `IT_005` | `TC_CANOE_IT_V2_002_AMBULANCE_RX` | ambulance-warning result state | native report + trace + panel capture | `No` |
| `IT_006` | `TC_CANOE_IT_V2_003_ARBITRATION` | final selected warning state | native report + sysvar snapshot + panel capture | `No` |
| `IT_007` | `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` | ambient color/pattern result | panel capture + screenshot + `verification_log.csv` | `No` |
| `IT_008` | `TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT` | cluster text/direction result | cluster capture + screenshot + `verification_log.csv` | `No` |
| `IT_009` | `TC_CANOE_IT_V2_004_TIMEOUT_CLEAR` | clear and restore state | native report + trace + sysvar snapshot | `No` |
| `IT_010` | `TC_CANOE_IT_V2_005_DECEL_ASSIST` | decel-assist request and sync state | native report + trace + sysvar snapshot + panel capture | `No` |
| `IT_011` | `TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING` | fail-safe state and minimum-channel state | native report + write window + sysvar snapshot + trace | `No` |
| `IT_012` | `TC_CANOE_IT_EXT_001_OBJECT_RISK_EVENTLOG` | object-risk state and event-log state | native report + trace + event log | `No` |
| `RET_IT_013` | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | retired umbrella row | native report + panel capture + sysvar snapshot | `No` |
| `IT_013` | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | seat-belt emphasis state | native report + panel capture + sysvar snapshot | `No` |
| `IT_014` | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | display-policy reflection state | native report + panel capture + sysvar snapshot | `No` |
| `IT_015` | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | turn-lamp context adjusted warning type | native report + panel capture + sysvar snapshot | `No` |
| `IT_016` | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | drive-mode sensitivity state | native report + panel capture + sysvar snapshot | `No` |
| `IT_017` | `TC_CANOE_IT_BASE_006_AUDIO_VOICE` | audio focus, ducking, and volume policy state | native report + panel capture + sysvar snapshot | `No` |
| `IT_018` | `TC_CANOE_IT_EXT_003_EMERGENCY_PLUS_TTC` | combined warning/decel result state | native report + trace + panel capture | `No` |
| `RET_IT_015` | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | retired umbrella row | native report + trace + sysvar snapshot | `No` |
| `IT_019` | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | parked baseline state | native report + trace + sysvar snapshot | `No` |
| `IT_020` | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | drive baseline state | native report + trace + sysvar snapshot | `No` |
| `RET_IT_016` | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | retired umbrella row | native report + trace + sysvar snapshot | `No` |
| `IT_021` | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | steering-input baseline state | native report + trace + sysvar snapshot | `No` |
| `IT_022` | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | braking-input baseline state | native report + trace + sysvar snapshot | `No` |
| `IT_023` | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | acceleration-driven drive-mode state | native report + trace + sysvar snapshot | `No` |
| `RET_IT_017` | `TC_CANOE_IT_BASE_003_BODY_STATE` | retired umbrella row | native report + trace + sysvar snapshot | `No` |
| `IT_024` | `TC_CANOE_IT_BASE_003_BODY_STATE` | hazard-reflection baseline state | native report + trace + sysvar snapshot | `No` |
| `IT_025` | `TC_CANOE_IT_EXT_010_WINDOW_STATE` | window-state reflection | native report + door-state trace + sysvar snapshot | `No` |
| `IT_026` | `TC_CANOE_IT_BASE_004_BASIC_DISPLAY_UI` | basic display integration state | panel capture + screenshot + native report | `No` |
| `RET_IT_019` | `TC_CANOE_IT_BASE_005_COMFORT_CONTEXT / TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT` | retired umbrella row | native report + trace + sysvar snapshot | `No` |
| `IT_027` | `TC_CANOE_IT_BASE_005_COMFORT_CONTEXT` | comfort-context policy state | native report + trace + sysvar snapshot | `No` |
| `IT_028` | `TC_CANOE_IT_EXT_014_BODY_CONTROL_LOCK` | door lock/open reflection state | native report + door-state trace + sysvar snapshot | `No` |
| `IT_029` | `TC_CANOE_IT_EXT_015_WIPER_RAIN_BASELINE` | wiper/rain baseline reflection state | native report + body-output trace + sysvar snapshot | `No` |
| `IT_030` | `TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT` | security-state service-boundary state | native report + trace + sysvar snapshot | `No` |
| `IT_031` | `TC_CANOE_IT_BASE_006_AUDIO_VOICE` | audio and voice-guide integrated state | panel capture + write window + native report | `No` |
| `RET_IT_021` | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | retired umbrella row | native report + trace + sysvar snapshot | `No` |
| `IT_032` | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | output-channel availability and fallback state | native report + trace + sysvar snapshot | `No` |
| `IT_033` | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | duplicate-popup suppression state | native report + trace + sysvar snapshot | `No` |
| `IT_034` | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | channel-restore consistency state | native report + trace + sysvar snapshot | `No` |
| `IT_035` | `TC_CANOE_IT_EXT_005_DISTANCE_HISTORY` | distance and history-query result | panel capture + native report + `verification_log.csv` | `No` |
| `IT_036` | `TC_CANOE_IT_EXT_006_CHASSIS_EXT_CONTEXT` | EPB/EHB/VSM/ECS/CDC integrated state | native report + trace + sysvar snapshot | `No` |
| `IT_037` | `TC_CANOE_IT_EXT_007_OCCUPANT_COMFORT_CONTEXT` | occupant/comfort integrated state | native report + trace + sysvar snapshot | `No` |
| `IT_038` | `TC_CANOE_IT_EXT_008_DISPLAY_SERVICE_CONTEXT` | display/service integrated state | panel capture + trace + native report | `No` |
| `IT_039` | `TC_CANOE_IT_EXT_009_ADAS_PERCEPTION_CONTEXT` | adas/perception integrated state | native report + trace + sysvar snapshot | `No` |
| `IT_040` | `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG` | service, security, diagnostic integrated state | native report + trace + write window + sysvar snapshot | `Yes` |
| `IT_041` | `TC_CANOE_IT_EXT_011_CHARGE_POWER_CONTEXT` | power and charge integrated state | native report + trace + sysvar snapshot | `No` |
| `IT_042` | `TC_CANOE_IT_EXT_012_DISPLAY_CHANNELS` | cross-channel visual consistency | panel capture + screenshot + `verification_log.csv` | `No` |
| `IT_043` | `TC_CANOE_IT_EXT_013_AUDIO_GUIDE_CHANNEL` | audio-guide consistency | write window + audio state capture + `verification_log.csv` | `No` |
| `IT_044` | `TC_CANOE_IT_ETH_001_POLICE_TX` | police external tx observation | Ethernet trace + write window + `verification_log.csv` | `No` |
| `IT_045` | `TC_CANOE_IT_ETH_002_AMBULANCE_TX` | ambulance external tx observation | Ethernet trace + write window + `verification_log.csv` | `No` |

## 5. System Test mapping

| ID | Candidate native asset | Primary oracle | Primary evidence | Diagnostic Needed? |
|---|---|---|---|---|
| `ST_001` | `TC_CANOE_ST_CORE_001_POWER_ON_BASELINE` | no-warning baseline state | panel capture + screenshot + native report | `No` |
| `ST_002` | `TC_CANOE_ST_CORE_002_NORMAL_DRIVE` | nominal drive state | panel capture + screenshot + native report | `No` |
| `ST_003` | `TC_CANOE_ST_CORE_003_BASIC_WARNING_ACTIVATION` | basic warning activation result | panel capture + trace + `verification_log.csv` | `No` |
| `ST_004` | `TC_CANOE_ST_CORE_004_BASIC_WARNING_CLEAR` | clear-to-normal state | panel capture + trace + `verification_log.csv` | `No` |
| `ST_005` | `TC_CANOE_ST_CORE_005_ENTER_SCHOOL_ZONE` | school-zone warning transition | panel capture + trace + `verification_log.csv` | `No` |
| `ST_006` | `TC_CANOE_ST_CORE_006_EXIT_SCHOOL_ZONE` | school-zone recovery state | panel capture + trace + `verification_log.csv` | `No` |
| `ST_007` | `TC_CANOE_ST_CORE_007_HIGHWAY_POLICY_TRANSITION` | highway-mode transition | panel capture + trace + `verification_log.csv` | `No` |
| `ST_008` | `TC_CANOE_ST_CORE_008_STEERING_INACTIVITY` | warning trigger and clear result | panel capture + trace + `verification_log.csv` | `No` |
| `ST_009` | `TC_CANOE_ST_CORE_009_GUIDE_LEFT` | left-guidance visible result | cluster capture + screenshot + native report | `No` |
| `ST_010` | `TC_CANOE_ST_CORE_010_GUIDE_RIGHT_CLEAR` | right-guidance visible result | cluster capture + screenshot + native report | `No` |
| `ST_011` | `TC_CANOE_ST_V2_001_POLICE_OVERRIDE` | police-over-zone result | panel capture + trace + native report | `No` |
| `ST_012` | `TC_CANOE_ST_V2_002_AMBULANCE_OVERRIDE` | ambulance-over-zone result | panel capture + trace + native report | `No` |
| `ST_013` | `TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT` | police direction render | cluster/HUD capture + native report | `No` |
| `ST_014` | `TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT` | ambulance direction render | cluster/HUD capture + native report | `No` |
| `ST_015` | `TC_CANOE_ST_V2_005_AMBULANCE_PRIORITY` | final selected warning state | panel capture + trace + native report | `No` |
| `ST_016` | `TC_CANOE_ST_V2_006_POLICE_TIEBREAK` | ETA and SourceID arbitration result | native report + sysvar snapshot + trace | `No` |
| `ST_017` | `TC_CANOE_ST_V2_007_AMBULANCE_TIEBREAK` | ETA and SourceID arbitration result | native report + sysvar snapshot + trace | `No` |
| `ST_018` | `TC_CANOE_ST_ETH_001_EXTERNAL_TX_PERIOD` | police tx periodicity observation | Ethernet trace + `verification_log.csv` + write window | `No` |
| `ST_019` | `TC_CANOE_ST_ETH_001_EXTERNAL_TX_PERIOD` | ambulance tx periodicity observation | Ethernet trace + `verification_log.csv` + write window | `No` |
| `ST_020` | `TC_CANOE_ST_V2_008_TIMEOUT_CLEAR` | timeout clear and return state | native report + trace + sysvar snapshot | `No` |
| `ST_021` | `TC_CANOE_ST_CORE_020_EMERGENCY_CLEAR_RESTORE` | restore-to-previous-warning state | panel capture + trace + native report | `No` |
| `ST_022` | `TC_CANOE_ST_EXT_001_INTERSECTION_DECEL` | combined warning/decel result | panel capture + trace + sysvar snapshot | `No` |
| `ST_023` | `TC_CANOE_ST_EXT_002_MERGE_DECEL` | combined warning/decel result | panel capture + trace + sysvar snapshot | `No` |
| `ST_024` | `TC_CANOE_ST_EXT_003_DRIVER_INTERVENTION_CLEAR` | clear-on-driver-intervention result | panel capture + trace + native report | `No` |
| `ST_025` | `TC_CANOE_ST_EXT_004_FAILSAFE_ENTRY` | fail-safe entry and minimum-channel state | native report + write window + trace + sysvar snapshot | `No` |
| `ST_026` | `TC_CANOE_ST_EXT_005_FAILSAFE_RECOVERY` | recovery-from-fail-safe state | native report + trace + sysvar snapshot | `No` |
| `ST_027` | `TC_CANOE_ST_EXT_006_FRONTAL_OBJECT_RISK` | object-warning visible result | panel capture + event log + trace | `No` |
| `ST_028` | `TC_CANOE_ST_EXT_007_LATERAL_OBJECT_RISK` | object-warning visible result | panel capture + event log + trace | `No` |
| `ST_029` | `TC_CANOE_ST_EXT_008_CUTIN_OBJECT_RISK` | object-warning visible result | panel capture + event log + trace | `No` |
| `ST_030` | `TC_CANOE_ST_EXT_009_CONTEXT_ADJUST` | seat-belt and driver-context adjusted warning | panel capture + screenshot + native report | `No` |
| `ST_031` | `TC_CANOE_ST_EXT_009_CONTEXT_ADJUST` | emergency distance display consistency | panel capture + screenshot + native report | `No` |
| `ST_032` | `TC_CANOE_ST_EXT_010_USER_SETTING_CHANGE` | updated output policy state | panel capture + screenshot + native report | `No` |
| `ST_033` | `TC_CANOE_ST_EXT_011_HISTORY_QUERY` | history-view result | panel capture + screenshot + native report | `No` |
| `ST_034` | `TC_CANOE_ST_EXT_012_DELAY_STABILITY` | duplicate-popup guard stability result | native report + trace + `verification_log.csv` | `No` |
| `ST_035` | `TC_CANOE_ST_EXT_012_DELAY_STABILITY` | timeout-clear restore stability result | native report + trace + `verification_log.csv` | `No` |
| `ST_036` | `TC_CANOE_ST_EXT_012_DELAY_STABILITY` | fail-safe recovery stability result | native report + trace + `verification_log.csv` | `No` |
| `ST_037` | `TC_CANOE_ST_EXT_013_CHANNEL_CONTENTION` | audio focus and ducking stability result | panel capture + trace + `verification_log.csv` | `No` |
| `ST_038` | `TC_CANOE_ST_EXT_013_CHANNEL_CONTENTION` | popup priority and cluster sync stability result | panel capture + trace + `verification_log.csv` | `No` |
| `ST_039` | `TC_CANOE_ST_EXT_014_CHASSIS_CONTEXT` | braking/stability context result | native report + trace + sysvar snapshot | `No` |
| `ST_040` | `TC_CANOE_ST_EXT_015_OCCUPANT_COMFORT_CONTEXT` | body/occupant/comfort context result | native report + trace + sysvar snapshot | `No` |
| `ST_041` | `TC_CANOE_ST_EXT_016_DISPLAY_SERVICE_CONTEXT` | display/service context result | panel capture + trace + native report | `No` |
| `ST_042` | `TC_CANOE_ST_EXT_017_ADAS_PERCEPTION_CONTEXT` | adas/perception context result | native report + trace + sysvar snapshot | `No` |
| `ST_043` | `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT` | service/security/diagnostic context result | native report + trace + write window + sysvar snapshot | `Yes` |
| `ST_044` | `TC_CANOE_ST_EXT_019_CHARGE_POWER_CONTEXT` | power/charge context result | native report + trace + sysvar snapshot | `No` |
| `ST_045` | `TC_CANOE_ST_EXT_040_TRIP_SEQUENCE` | end-to-end scenario verdict | native report + panel capture + trace + `verification_log.csv` | `No` |
| `ST_046` | `TC_CANOE_ST_EXT_041_FAILSAFE_RECOVERY` | end-to-end fail-safe scenario verdict | native report + panel capture + trace + `verification_log.csv` | `No` |

## 6. Current implementation priority

Build native assets in this order:

1. `UT_003`, `UT_009`, `UT_011`, `UT_014`, `UT_015`
2. `IT_001` to `IT_008`
3. `ST_001` to `ST_021`
4. diagnostic-linked items:
   - `UT_063`
   - `UT_064`
   - `IT_040`
   - `ST_043`

## 7. Relationship to other verification documents

Use this document together with:

- `oracle.md`
- `execution-guide.md`
- `acceptance-criteria.md`
- `evidence-policy.md`
- `diagnostic-coverage.md`

## Latest diagnostic execution baseline (2026-03-15)

| Official Scope | Native Asset | TEST_SCN Scenario | Primary Producer Wiring | Current Gate |
| --- | --- | --- | --- | --- |
| UT_063 | `TC_CANOE_UT_EXT_016_SGW_SECURITY_STATE` | `203` | `SGW.can -> Diag::SecurityState, Diag::RouteOwner` | Executable unit contract fixed |
| UT_064 | `TC_CANOE_UT_EXT_017_DCM_DIAGNOSTIC_STATE` | `204` | `DCM.can -> Diag::ServiceState, Diag::ResponseKind, Diag::ReasonCode, Diag::LastRequestSid, Diag::LastResponseCode, Diag::LastResponseOk` | Executable unit contract fixed |
| IT_040 | `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG` | `205` | `SGW + DCM integrated diagnostic seam` | Producer wiring done, compile/runtime pending |
| ST_043 | `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT` | `202` | `SGW + DCM integrated diagnostic seam with scenario phase tracking` | Producer wiring done, compile/runtime pending |

## Wave 2 direct-ownership UT baseline

| Official Scope | Native Asset | Reserved TEST_SCN Scenario | Current State |
| --- | --- | --- | --- |
| UT_003 | `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` | `206` | Draft skeleton created, stimulus/oracle binding pending |
| UT_011 | `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` | `207` | Draft skeleton created, stimulus/oracle binding pending |
| UT_014 | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` | `208` | Draft skeleton created, stimulus/oracle binding pending |
| UT_015 | `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` | `209` | Draft skeleton created, stimulus/oracle binding pending |
| UT_076 | `TC_CANOE_UT_OUT_007_POLICE_TX` | `4` | External-TX unit contract created; final frame-period closure remains trace-gated |
| UT_077 | `TC_CANOE_UT_OUT_008_AMBULANCE_TX` | `5` | External-TX unit contract created; final frame-period closure remains trace-gated |

## Wave 2 planned oracle baseline

- `UT_003 / 206`: nominal CGW boundary readiness, nominal routing policy, fail-safe clear.
- `UT_011 / 207`: intended ADAS warning-selection context, nominal warning path, fail-safe clear.
- `UT_014 / 208`: intended BCM ambient policy with nominal body gateway health.
- `UT_015 / 209`: intended IVI text/output mapping without fail-safe override.
- `UT_076 / 4`: police emergency transport activation with TX-facing oracle and trace-gated frame evidence.
- `UT_077 / 5`: ambulance emergency transport activation with TX-facing oracle and trace-gated frame evidence.

## Wave 2 current progress update

- `UT_003 / 206`: executable scenario contract added. Current oracle checks `domainBoundaryStatus=1`, `routingPolicy=1`, `selectedAlertLevel=0`, and `failSafeMode=0`.
- `UT_011 / 207`: executable scenario contract added. Current oracle checks `selectedAlertLevel=3`, `selectedAlertType=3`, `warningPathStatus=0`, and `failSafeMode=0`.
- `UT_014 / 208` and `UT_015 / 209` remain draft skeletons pending concrete stimulus/oracle binding.

## Wave 2 progress update (208/209)

- `UT_014 / 208`: executable scenario contract added. Current oracle checks school-zone ambient policy via `selectedAlertLevel=3`, `selectedAlertType=3`, `ambientColor=3`, `ambientPattern=5`, and `failSafeMode=0`.
- `UT_015 / 209`: executable scenario contract added. Current oracle checks police-emergency text mapping via `selectedAlertLevel=6`, `selectedAlertType=1`, `warningTextCode=101`, and `failSafeMode=0`.
- Dedicated external-TX unit rows are tracked separately with `UT_076 / 4` and `UT_077 / 5`.
- `UT_006`: executable object-risk unit contract added. Current oracle checks frontal/intersection/merge risk and confidence-degrade behavior via scenarios `20`, `21`, `22`, and `24`.
- `UT_007`: executable CLU context-adjust unit contract added. Current oracle checks seat-belt emphasis, display-policy reflection, and distance-context rendering via scenarios `214`, `215`, and `222`.
- `UT_008`: executable boundary/fail-safe unit contract added. Current oracle checks fail-safe retention plus SGW/DCM service seam interpretation via scenarios `18`, `203`, and `204`.
- `UT_010`: executable emergency lifecycle unit contract added. Current oracle checks police/ambulance activation via scenarios `4` and `5`, then timeout-clear via scenario `6`.
- `UT_070`: executable BCM output unit contract added. Current oracle checks school-zone and emergency ambient output via scenarios `208` and `4`.
- `UT_071`: executable IVI HMI output unit contract added. Current oracle checks text/direction, popup/theme, and distance context via scenarios `215`, `220`, and `222`.
- `UT_072`: executable CLU display unit contract added. Current oracle checks police/ambulance direction display plus popup/theme sync via scenarios `30`, `33`, and `220`.
- `UT_073`: executable HUD/front-display unit contract added. Current oracle checks shared front-display direction plus popup/theme seams via scenarios `30` and `220`.
- `UT_074`: executable AMP audio unit contract added. Current oracle checks audio focus, ducking, and volume policy via scenario `215`.
- `UT_075`: executable decel-assist output unit contract added. Current oracle checks active request and fail-safe block via scenarios `16` and `18`.

## External TX unit completion update

- `UT_076 / 4`: executable scenario contract added. Current oracle checks police emergency transport activation via `V2X::alertState=1`, `V2X::emergencyType=1`, `V2X::eta=12`, `V2X::sourceId=11`, `selectedAlertLevel=6`, and `warningTextCode=101`.
- `UT_077 / 5`: executable scenario contract added. Current oracle checks ambulance emergency transport activation via `V2X::alertState=1`, `V2X::emergencyType=2`, `V2X::eta=8`, `V2X::sourceId=22`, `selectedAlertLevel=7`, and `warningTextCode=202`.
- Retired context/display drafts that previously occupied `UT_076/077` have been moved under `retire/`.

## Wave 3 system-test baseline

| Official Scope | Native Asset | TEST_SCN Scenario | Current Contract |
| --- | --- | --- | --- |
| ST_001 | `TC_CANOE_ST_CORE_001_POWER_ON_BASELINE` | `1` | Power-on initialization enters no-warning ready state without fail-safe residue |
| ST_002 | `TC_CANOE_ST_CORE_002_NORMAL_DRIVE` | `14` | Normal-drive baseline keeps routing healthy and no-warning state stable |
| ST_003 | `TC_CANOE_ST_CORE_003_BASIC_WARNING_ACTIVATION` | `1 -> 26` | General-road single-risk activation raises the basic warning state without fail-safe drift |
| ST_004 | `TC_CANOE_ST_CORE_004_BASIC_WARNING_CLEAR` | `26 -> 1` | Basic warning clears back to the no-warning baseline after the condition is removed |
| ST_005 | `TC_CANOE_ST_CORE_005_ENTER_SCHOOL_ZONE` | `1 -> 2` | Transition from normal drive into school-zone overspeed switches to the school-zone warning policy |
| ST_006 | `TC_CANOE_ST_CORE_006_EXIT_SCHOOL_ZONE` | `2 -> 1` | School-zone warning clears cleanly when the system returns to the normal-drive baseline |
| ST_007 | `TC_CANOE_ST_CORE_007_HIGHWAY_POLICY_TRANSITION` | `14 -> 244` | Transition from normal drive into highway context stabilizes on the highway policy without false warning output |
| ST_008 | `TC_CANOE_ST_CORE_008_STEERING_INACTIVITY` | `244 -> 3 -> 244` | Highway no-steer warning triggers after sustained inactivity and clears after steering recovery |
| ST_009 | `TC_CANOE_ST_CORE_009_GUIDE_LEFT` | `7` | Guide-left warning renders left-direction guidance consistently across the visible outputs |
| ST_010 | `TC_CANOE_ST_CORE_010_GUIDE_RIGHT_CLEAR` | `8 -> 1` | Guide-right warning renders correctly and then returns to the no-warning baseline after completion |
| ST_011 | `TC_CANOE_ST_V2_001_POLICE_OVERRIDE` | `11` | Police emergency overrides the active general-warning context without ambiguous dual output |
| ST_012 | `TC_CANOE_ST_V2_002_AMBULANCE_OVERRIDE` | `223` | Ambulance emergency overrides the active general-warning context without ambiguous dual output |
| ST_013 | `TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT` | `30` | Police-right emergency display with `warningTextCode=102` and `renderDirection=2` |
| ST_014 | `TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT` | `33` | Ambulance-left emergency display with `warningTextCode=201` and `renderDirection=1` |
| ST_015 | `TC_CANOE_ST_V2_005_AMBULANCE_PRIORITY` | `212` | Ambulance warning stays selected when police and ambulance dispatch requests are simultaneous |
| ST_016 | `TC_CANOE_ST_V2_006_POLICE_TIEBREAK` | `10` | Equal-priority police warnings resolve consistently by SourceID after ETA tie |
| ST_017 | `TC_CANOE_ST_V2_007_AMBULANCE_TIEBREAK` | `224` | Equal-priority ambulance warnings resolve consistently by SourceID after ETA tie |
| ST_018 | `TC_CANOE_ST_ETH_001_EXTERNAL_TX_PERIOD` | `4` | Police external transport context is stimulated with trace-gated `100ms` periodicity closure |
| ST_019 | `TC_CANOE_ST_ETH_001_EXTERNAL_TX_PERIOD` | `5` | Ambulance external transport context is stimulated with trace-gated `100ms` periodicity closure |
| ST_020 | `TC_CANOE_ST_V2_008_TIMEOUT_CLEAR` | `35` | Timeout-clear removes emergency context and returns the system to a safe restored state |
| ST_021 | `TC_CANOE_ST_CORE_020_EMERGENCY_CLEAR_RESTORE` | `35` | Emergency clear followed by zone-warning restore |
| ST_027 | `TC_CANOE_ST_EXT_006_FRONTAL_OBJECT_RISK` | `20` | Frontal object-risk warning and event-log consistency under forward TTC conflict |
| ST_028 | `TC_CANOE_ST_EXT_007_LATERAL_OBJECT_RISK` | `21` | Lateral object-risk warning and event-log consistency under intersection conflict |
| ST_029 | `TC_CANOE_ST_EXT_008_CUTIN_OBJECT_RISK` | `22` | Cut-in object-risk warning and event-log consistency under merge conflict |
| ST_030 | `TC_CANOE_ST_EXT_009_CONTEXT_ADJUST` | `214` | Seat-belt and driver-context change adjusts warning context without unintended fail-safe or alert-class drift |
| ST_031 | `TC_CANOE_ST_EXT_009_CONTEXT_ADJUST` | `222` | Emergency distance display stays consistent with warning text and rendered police-right context |
| ST_032 | `TC_CANOE_ST_EXT_010_USER_SETTING_CHANGE` | `215` | User display and volume policy change reflected consistently in system-level warning guidance |
| ST_033 | `TC_CANOE_ST_EXT_011_HISTORY_QUERY` | `222 + historyQuery(0)` | Distance display and latest-history query response remain consistent after emergency warning |
| ST_034 | `TC_CANOE_ST_EXT_012_DELAY_STABILITY` | `12` | Duplicate-popup guard suppresses rapid re-trigger oscillation while preserving stable warning guidance |
| ST_035 | `TC_CANOE_ST_EXT_012_DELAY_STABILITY` | `35` | Timeout-clear path restores the prior valid warning context without fail-safe residue |
| ST_036 | `TC_CANOE_ST_EXT_012_DELAY_STABILITY` | `201` | Fail-safe recovery returns the warning path to normal without residual oscillation |
| ST_037 | `TC_CANOE_ST_EXT_013_CHANNEL_CONTENTION` | `215` | Warning-audio policy keeps audio focus, ducking, and volume handling stable under active emergency guidance |
| ST_038 | `TC_CANOE_ST_EXT_013_CHANNEL_CONTENTION` | `220` | Visual-first warning mode keeps popup priority and cluster synchronization stable without fail-safe drift |
| ST_045 | `TC_CANOE_ST_EXT_040_TRIP_SEQUENCE` | `200` | Full trip sequence returns to no-warning stable state |
| ST_046 | `TC_CANOE_ST_EXT_041_FAILSAFE_RECOVERY` | `201` | Fail-safe recovery returns `failSafeMode` to zero |

## Wave 2 completion update (UT_004/UT_005)

- `UT_004`: `TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN` uses scenario `9` and validates ETA/source priority handling in `V2X.can`.
- `UT_005`: `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST` uses scenario `16` and validates proximity-risk plus decel-assist activation in `ADAS.can`.
- With these additions, the current direct-ownership `05` core baseline (`UT_003`, `UT_004`, `UT_005`, `UT_011`, `UT_014`, `UT_015`, `UT_063`, `UT_064`, `UT_076`, `UT_077`) now has executable asset contracts.

## Wave 5 gateway and extension UT baseline

- `UT_001`: `TC_CANOE_UT_CORE_001_CGW_CHS_GW` uses scenarios `216`, `217`, `218`, and `219` to validate normalized chassis-state forwarding for drive, speed, steering, and brake context.
- `UT_002`: `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW` uses scenarios `2`, `7`, and `8` to validate zone, direction, distance, and speed-limit forwarding through the infotainment gateway path.
- `UT_009`: `TC_CANOE_UT_CORE_004_NAV_CTX_MGR` uses scenarios `2`, `3`, `7`, and `8` to validate zone-context classification and navigation-context stabilization.
- `UT_012`: `TC_CANOE_UT_CORE_007_BODY_GW_ROUTE` uses scenarios `208` and `4` to validate ambient-route forwarding from final warning result to body output path.
- `UT_013`: `TC_CANOE_UT_CORE_008_IVI_GW_ROUTE` uses scenarios `209`, `30`, and `33` to validate cluster-route forwarding from final warning result to IVI/cluster output path.
- `UT_016`: `TC_CANOE_UT_EXT_004_CHS_BRAKE_EXT` uses scenarios `216` and `219` to validate brake and parked-state context propagation.
- `UT_017`: `TC_CANOE_UT_EXT_005_CHS_DYNAMICS_EXT` uses scenario `225` to validate suspension/chassis-dynamics context propagation.
- `UT_018`: `TC_CANOE_UT_EXT_006_BODY_ENTRY_EXIT` uses scenarios `226` and `227` to validate door and tailgate entry/exit context propagation.
- `UT_019`: `TC_CANOE_UT_EXT_007_BODY_OCCUPANT_PROTECTION` uses scenario `228` to validate occupant-detection and occupant-protection context propagation.

## Wave 6 service, assist, and router UT baseline

- `UT_020`: `TC_CANOE_UT_EXT_008_BODY_COMFORT` uses scenarios `229` and `230` to validate HVAC remote-climate behavior plus AFLS/AHLS comfort-lighting propagation together with static seat/sunroof comfort outputs.
- `UT_021`: `TC_CANOE_UT_EXT_009_IVI_DISPLAY_SERVICE` uses scenarios `229`, `30`, and `215` to validate TMU service delivery, HUD display rendering, and AMP audio-policy propagation.
- `UT_022`: `TC_CANOE_UT_EXT_010_IVI_SERVICE_ACCESS` uses scenario `229` to validate TMU service state and digital-key service-access propagation.
- `UT_023`: `TC_CANOE_UT_EXT_011_ADAS_DRIVE_ASSIST` uses scenario `233` to validate `LDWS_LKAS` and `RPC` drive-assist / road-preview propagation from FCAM state.
- `UT_024`: `TC_CANOE_UT_EXT_012_ADAS_PARKING_PERCEPTION` uses scenario `234` to validate `PKM` and `SPM` parking-perception propagation from AVM / ultrasonic / SPAS / RSPA state.
- `UT_025`: `TC_CANOE_UT_EXT_013_WARNING_DELIVERY_BOUNDARY` uses scenarios `18`, `203`, and `204` to validate fail-safe entry plus SGW/DCM delivery-boundary and response-state propagation.
- `UT_026`: `TC_CANOE_UT_EXT_014_DOMAIN_ROUTER_PROPULSION` uses scenario `232` to validate propulsion-context propagation through `EOP`, `MCU`, and `INVERTER`.
- `UT_027`: `TC_CANOE_UT_EXT_015_DOMAIN_ROUTER_POWER_CHARGE` uses scenario `231` to validate charging-context propagation through `OBC` and `DCDC`.

## Wave 4 integration baseline

| Official Scope | Native Asset | TEST_SCN Scenario | Current Contract |
| --- | --- | --- | --- |
| IT_002 | `TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH` | `2` | School-zone warning path from nav/chassis input to ambient output |
| IT_003 | `TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH` | `3` | Highway no-steer path from chassis input to ambient output |
| IT_001 | `TC_CANOE_IT_CORE_001_BASE_ACTIVATION` | `1 -> 2 -> 12` | Idle no-warning baseline, activation, and duplicate-guard stability in one integrated flow |
| IT_004 | `TC_CANOE_IT_V2_001_POLICE_RX` | `4` | Police emergency receive path reflected into final warning state |
| IT_005 | `TC_CANOE_IT_V2_002_AMBULANCE_RX` | `5` | Ambulance emergency receive path reflected into final warning state |
| IT_006 | `TC_CANOE_IT_V2_003_ARBITRATION` | `9 -> 10 -> 11 -> 212` | Arbitration baseline covers ETA priority, SourceID tiebreak, emergency-over-nav takeover, and ambulance-over-police dispatch priority |
| IT_007 | `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` | `4` | Emergency ambient output path |
| IT_008 | `TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT` | `30` | Cluster direction output path |
| IT_009 | `TC_CANOE_IT_V2_004_TIMEOUT_CLEAR` | `35` | Emergency clear followed by safe restore to previous valid context |
| IT_010 | `TC_CANOE_IT_V2_005_DECEL_ASSIST` | `19` | Decel-assist request and warning synchronization under emergency proximity |
| IT_011 | `TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING` | `18` | Fail-safe downgrade with minimum warning retention and decel block |
| IT_012 | `TC_CANOE_IT_EXT_001_OBJECT_RISK_EVENTLOG` | `20 -> 21 -> 22 -> 24 -> 25` | Object-risk escalation, validity filtering, confidence downgrade, and event-log continuity |
| RET_IT_013 | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | `214 -> 215 -> 236 -> 239` | Driver-context umbrella row is retired in favor of exact executable rows |
| IT_013 | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | `214` | Seat-belt context raises warning emphasis without unintended alert-class drift |
| IT_014 | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | `215` | Display-policy setting is reflected in output code and rendered direction state |
| IT_015 | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | `239` | Right turn-lamp context adjusts school-zone warning type without fail-safe or level drift |
| IT_016 | `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` | `236` | Sport-mode context raises school-zone warning sensitivity while keeping alert type stable |
| IT_017 | `TC_CANOE_IT_BASE_006_AUDIO_VOICE` | `215` | Alert-volume setting is reflected through audio focus, ducking, and volume policy state |
| IT_018 | `TC_CANOE_IT_EXT_003_EMERGENCY_PLUS_TTC` | `213` | Emergency-priority retention under simultaneous TTC intersection conflict with decel-assist request |
| RET_IT_015 | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | `216 -> 217` | Powertrain umbrella row is retired in favor of exact parked/drive executable rows |
| IT_019 | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | `216` | Parked baseline keeps drive-state and speed-state at a stable no-warning integration baseline |
| IT_020 | `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` | `217` | Drive baseline propagates drive-state and speed-state without unintended warning activation |
| RET_IT_016 | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | `218 -> 219 -> 237` | Chassis umbrella row is retired in favor of exact steering/braking/acceleration executable rows |
| IT_021 | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | `218` | Steering-input propagation baseline keeps steering and speed state aligned for warning judgment |
| IT_022 | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | `219` | Braking-input propagation baseline keeps brake and speed state aligned for warning judgment |
| IT_023 | `TC_CANOE_IT_BASE_002_CHASSIS_STATE` | `237` | High-acceleration baseline drives driveMode and sport-state into a stable chassis integration result |
| RET_IT_017 | `TC_CANOE_IT_BASE_003_BODY_STATE` | `211 -> 216` | Body umbrella row is retired in favor of exact hazard/window executable rows |
| IT_024 | `TC_CANOE_IT_BASE_003_BODY_STATE` | `211` | Hazard reflection baseline keeps turn-lamp state and alert level aligned without unintended drift |
| IT_025 | `TC_CANOE_IT_EXT_010_WINDOW_STATE` | `226` | Front and right door window positions remain consistent with door/window output reflection under entry context |
| IT_026 | `TC_CANOE_IT_BASE_004_BASIC_DISPLAY_UI` | `220` | Visual-first display mode keeps popup, theme, and cluster-sync state consistent on school-zone warning |
| RET_IT_019 | `TC_CANOE_IT_BASE_005_COMFORT_CONTEXT / TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT` | `229 / 203` | Comfort/security umbrella row is retired in favor of exact executable rows |
| IT_027 | `TC_CANOE_IT_BASE_005_COMFORT_CONTEXT` | `229` | Remote-climate, HVAC, rear-climate, and digital-access outputs stay consistent as one comfort context |
| IT_028 | `TC_CANOE_IT_EXT_014_BODY_CONTROL_LOCK` | `226` | Door lock and open-state reflection remain consistent across left/right body control output path |
| IT_029 | `TC_CANOE_IT_EXT_015_WIPER_RAIN_BASELINE` | `229` | Wiper and rain-light baseline remain inactive and consistent across body output path in parked comfort context |
| IT_030 | `TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT` | `203` | Security-state boundary remains consistent without conflicting service downgrade state |
| IT_031 | `TC_CANOE_IT_BASE_006_AUDIO_VOICE` | `215` | Audio focus, ducking, and explicit warning-volume policy under emergency warning |
| RET_IT_021 | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | `18 -> 12 -> 35` | Output-availability umbrella row is retired in favor of exact executable rows |
| IT_032 | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | `18` | Minimum warning channel remains available when fail-safe entry occurs |
| IT_033 | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | `12` | Duplicate-popup suppression prevents over-dense non-emergency popup churn |
| IT_034 | `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` | `35` | Channel state restores to a consistent warning context after clear or mismatch recovery |
| IT_035 | `TC_CANOE_IT_EXT_005_DISTANCE_HISTORY` | `222 + historyQuery(0)` | Emergency distance display and latest-history response consistency |

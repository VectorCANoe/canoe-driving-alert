# Test Oracle / Evidence / Diagnostic Mapping Draft

> [!IMPORTANT]
> This document is a planning draft for the current CANoe SIL baseline.
> It defines how `05`, `06`, and `07` should later connect to native test assets, oracle sources, evidence, and diagnostic need.
> It does not mean every listed native asset or diagnostic seam already exists.

## 1. Diagnostic decision meaning

| Decision | Meaning |
|---|---|
| `No` | current PASS/FAIL can be judged from output, sysvar, trace, report, and evidence without a diagnostic seam |
| `Yes` | current final PASS/FAIL would remain weak or ambiguous without diagnostic visibility |

Optional future expansion candidates are tracked separately and do not affect the current official verdict path.

## 2. Future diagnostic build target

When the project later deepens diagnostic verification, the recommended matrix fields are:

- `ECU`
- `ReqFrame`
- `RespFrame`
- `SID`
- `DID/DTC`
- `PositiveResp`
- `NegativeResp`
- `Timeout`
- `SourceBus`
- `TargetBus`
- `CoverageTier`

Later expansion may include:

- `session control`
- `security access`
- `NRC policy`
- `gateway route ownership`
- `ECU DID catalog`
- `ODX/CDD-based tester interpretation`

## 3. 05 Unit Test mapping draft

Note:
Repeated simulator rows are grouped where the native-asset candidate, oracle type, and evidence type are identical.

| ID | Candidate native asset | Primary oracle | Primary evidence | Diagnostic Needed? | Diagnostic intent |
|---|---|---|---|---|---|
| `UT_001` | `TC_CANOE_UT_CORE_001_CGW_CHS_GW` | forwarded vehicle-state seam | native report + trace + `verification_log.csv` | `No` | - |
| `UT_002` | `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW` | forwarded navigation-context seam | native report + trace + `verification_log.csv` | `No` | - |
| `UT_003` | `TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` | selected warning state | native report + sysvar snapshot + panel capture | `No` | - |
| `UT_004` | `TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN` | emergency state + timeout clear | native report + trace + sysvar snapshot | `No` | - |
| `UT_005` | `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST` | arbitration result and decel-assist state | native report + sysvar snapshot + panel capture | `No` | - |
| `UT_006` | `TC_CANOE_UT_EXT_001_OBJECT_RISK` | object-risk state and downgrade state | native report + trace + event log | `No` | - |
| `UT_007` | `TC_CANOE_UT_EXT_002_CLU_CONTEXT_ADJUST` | rendered warning context | native report + cluster capture + sysvar snapshot | `No` | - |
| `UT_008` | `TC_CANOE_UT_EXT_003_DOMAIN_BOUNDARY_FAILSAFE` | fail-safe entry state and boundary-health state | native report + sysvar snapshot + trace + write window | `No` | - |
| `UT_009` | `TC_CANOE_UT_CORE_004_NAV_CTX_MGR` | zone context state | native report + sysvar snapshot | `No` | - |
| `UT_010` | `TC_CANOE_UT_CORE_005_EMS_ALERT_TXRX` | emergency tx/rx state and timeout state | native report + CAN/Ethernet trace + write window | `No` | - |
| `UT_011` | `TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` | final selected warning state | native report + sysvar snapshot + panel capture | `No` | - |
| `UT_012` | `TC_CANOE_UT_CORE_007_BODY_GW_ROUTE` | ambient route state | native report + trace + ambient capture | `No` | - |
| `UT_013` | `TC_CANOE_UT_CORE_008_IVI_GW_ROUTE` | cluster route state | native report + trace + cluster capture | `No` | - |
| `UT_014` | `TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` | ambient color and pattern state | native report + panel capture + screenshot | `No` | - |
| `UT_015` | `TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` | warning text and direction state | native report + cluster capture + screenshot | `No` | - |
| `UT_016` | `TC_CANOE_UT_EXT_004_CHS_BRAKE_EXT` | brake-related context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_017` | `TC_CANOE_UT_EXT_005_CHS_DYNAMICS_EXT` | chassis-context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_018` | `TC_CANOE_UT_EXT_006_BODY_ENTRY_EXIT` | door and tailgate context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_019` | `TC_CANOE_UT_EXT_007_BODY_OCCUPANT_PROTECTION` | occupant-protection context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_020` | `TC_CANOE_UT_EXT_008_BODY_COMFORT` | comfort-context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_021` | `TC_CANOE_UT_EXT_009_IVI_DISPLAY_SERVICE` | display/service context state | native report + sysvar snapshot + panel capture | `No` | - |
| `UT_022` | `TC_CANOE_UT_EXT_010_IVI_SERVICE_ACCESS` | service-access context state | native report + sysvar snapshot + trace | `No` | - |
| `UT_023` | `TC_CANOE_UT_EXT_011_ADAS_DRIVE_ASSIST` | drive-assist context state | native report + sysvar snapshot + trace | `No` | - |
| `UT_024` | `TC_CANOE_UT_EXT_012_ADAS_PARKING_PERCEPTION` | parking/perception context state | native report + sysvar snapshot + trace | `No` | - |
| `UT_025` | `TC_CANOE_UT_EXT_013_WARNING_DELIVERY_BOUNDARY` | delivery-health and fail-safe state | native report + trace + write window + sysvar snapshot | `No` | - |
| `UT_026` | `TC_CANOE_UT_EXT_014_DOMAIN_ROUTER_PROPULSION` | propulsion-context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_027` | `TC_CANOE_UT_EXT_015_DOMAIN_ROUTER_POWER_CHARGE` | power/charge context state | native report + trace + sysvar snapshot | `No` | - |
| `UT_028`-`UT_030` | `TEST_SCN core input presets` | stimulus-ack and injected input state | write window + trace + preset log | `No` | - |
| `UT_031`-`UT_035` | `TEST_SCN chassis/body-state presets` | input injection state | write window + trace + preset log | `No` | - |
| `UT_036`-`UT_048` | `TEST_SCN body/comfort-state presets` | input injection state | write window + trace + preset log | `No` | - |
| `UT_049`-`UT_051` | `TEST_SCN display/audio/service presets` | input injection state | write window + trace + preset log | `No` | - |
| `UT_052`-`UT_061` | `TEST_SCN adas/parking/perception presets` | input injection state | write window + trace + preset log | `No` | - |
| `UT_062` | `TEST_SCN IBOX service preset` | service-state injection | write window + trace + preset log | `No` | - |
| `UT_063` | `TC_CANOE_UT_EXT_016_SGW_SECURITY_STATE` | security-state injection | write window + trace + sysvar snapshot | `Yes` | security-state and route ownership explanation |
| `UT_064` | `TC_CANOE_UT_EXT_017_DCM_DIAGNOSTIC_STATE` | diagnostic-state injection | write window + trace + sysvar snapshot | `Yes` | diagnostic-state reason and later SID/DID linkage |
| `UT_065`-`UT_069` | `TEST_SCN backbone/powertrain presets` | input injection state | write window + trace + preset log | `No` | - |
| `UT_070` | `TC_CANOE_UT_OUT_001_BCM_AMBIENT` | ambient output render state | panel capture + screenshot + native report | `No` | - |
| `UT_071` | `TC_CANOE_UT_OUT_002_IVI_HMI` | HMI output state | panel capture + screenshot + native report | `No` | - |
| `UT_072` | `TC_CANOE_UT_OUT_003_CLU_DISPLAY` | cluster display render state | cluster capture + screenshot + native report | `No` | - |
| `UT_073` | `TC_CANOE_UT_OUT_004_HUD_DISPLAY` | HUD render state | HUD capture + screenshot + native report | `No` | - |
| `UT_074` | `TC_CANOE_UT_OUT_005_AMP_AUDIO` | audio-guide state | write window + audio state capture + native report | `No` | - |
| `UT_075` | `TC_CANOE_UT_OUT_006_DECEL_ASSIST_REQ` | decel-assist request state | native report + trace + sysvar snapshot | `No` | - |
| `UT_076` | `TC_CANOE_UT_OUT_007_POLICE_TX` | external tx frame observation | Ethernet trace + write window + `verification_log.csv` | `No` | - |
| `UT_077` | `TC_CANOE_UT_OUT_008_AMBULANCE_TX` | external tx frame observation | Ethernet trace + write window + `verification_log.csv` | `No` | - |

## 4. 06 Integration Test mapping draft

| ID | Candidate native asset | Primary oracle | Primary evidence | Diagnostic Needed? | Diagnostic intent |
|---|---|---|---|---|---|
| `IT_001` | `TC_CANOE_IT_CORE_001_BASE_ACTIVATION` | warning activation/inactivation state | native report + sysvar snapshot + panel capture | `No` | - |
| `IT_002` | `TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH` | zone-warning result state | native report + trace + panel capture | `No` | - |
| `IT_003` | `TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH` | highway-warning trigger and clear state | native report + sysvar snapshot + panel capture | `No` | - |
| `IT_004` | `TC_CANOE_IT_V2_001_POLICE_RX` | police-warning result state | native report + trace + panel capture | `No` | - |
| `IT_005` | `TC_CANOE_IT_V2_002_AMBULANCE_RX` | ambulance-warning result state | native report + trace + panel capture | `No` | - |
| `IT_006` | `TC_CANOE_IT_V2_003_ARBITRATION` | final selected warning state | native report + sysvar snapshot + panel capture | `No` | - |
| `IT_007` | `TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` | ambient color/pattern result | panel capture + screenshot + `verification_log.csv` | `No` | - |
| `IT_008` | `TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT` | cluster text/direction result | cluster capture + screenshot + `verification_log.csv` | `No` | - |
| `IT_009` | `TC_CANOE_IT_V2_004_TIMEOUT_CLEAR` | clear and restore state | native report + trace + sysvar snapshot | `No` | - |
| `IT_010` | `TC_CANOE_IT_V2_005_DECEL_ASSIST` | decel-assist request and sync state | native report + trace + sysvar snapshot + panel capture | `No` | - |
| `IT_011` | `TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING` | fail-safe state and minimum-channel state | native report + write window + sysvar snapshot + trace | `No` | - |
| `IT_012` | `TC_CANOE_IT_EXT_001_OBJECT_RISK_EVENTLOG` | object-risk state and event-log state | native report + trace + event log | `No` | - |
| `IT_013` | `TC_CANOE_IT_013_SEATBELT_CONTEXT` | seat-belt emphasis state | native report + panel capture + sysvar snapshot | `No` | - |
| `IT_014` | `TC_CANOE_IT_014_DISPLAY_POLICY` | display-policy reflection state | native report + panel capture + sysvar snapshot | `No` | - |
| `IT_015` | `TC_CANOE_IT_015_TURN_LAMP_CONTEXT` | turn-lamp context adjusted warning type | native report + panel capture + sysvar snapshot | `No` | - |
| `IT_016` | `TC_CANOE_IT_016_DRIVE_MODE_SENSITIVITY` | drive-mode sensitivity state | native report + panel capture + sysvar snapshot | `No` | - |
| `IT_017` | `TC_CANOE_IT_017_AUDIO_VOLUME_POLICY` | audio focus, ducking, and volume policy state | native report + panel capture + sysvar snapshot | `No` | - |
| `IT_018` | `TC_CANOE_IT_EXT_003_EMERGENCY_PLUS_TTC` | combined warning/decel result state | native report + trace + panel capture | `No` | - |
| `IT_019` | `TC_CANOE_IT_019_POWERTRAIN_PARKED_BASELINE` | parked baseline state | native report + trace + sysvar snapshot | `No` | - |
| `IT_020` | `TC_CANOE_IT_020_POWERTRAIN_DRIVE_BASELINE` | drive baseline state | native report + trace + sysvar snapshot | `No` | - |
| `IT_021` | `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE` | steering-input baseline state | native report + trace + sysvar snapshot | `No` | - |
| `IT_022` | `TC_CANOE_IT_022_CHASSIS_BRAKE_BASELINE` | braking-input baseline state | native report + trace + sysvar snapshot | `No` | - |
| `IT_023` | `TC_CANOE_IT_023_CHASSIS_ACCEL_BASELINE` | acceleration-driven drive-mode state | native report + trace + sysvar snapshot | `No` | - |
| `IT_024` | `TC_CANOE_IT_BASE_003_BODY_STATE` | hazard-reflection baseline state | native report + trace + sysvar snapshot | `No` | - |
| `IT_025` | `TC_CANOE_IT_EXT_010_WINDOW_STATE` | window-state reflection | native report + door-state trace + sysvar snapshot | `No` | - |
| `IT_026` | `TC_CANOE_IT_BASE_004_BASIC_DISPLAY_UI` | basic display integration state | panel capture + screenshot + native report | `No` | - |
| `IT_027` | `TC_CANOE_IT_BASE_005_COMFORT_CONTEXT` | comfort-context policy state | native report + trace + sysvar snapshot | `No` | - |
| `IT_028` | `TC_CANOE_IT_EXT_014_BODY_CONTROL_LOCK` | door lock/open reflection state | native report + door-state trace + sysvar snapshot | `No` | - |
| `IT_029` | `TC_CANOE_IT_EXT_015_WIPER_RAIN_BASELINE` | wiper/rain baseline reflection state | native report + body-output trace + sysvar snapshot | `No` | - |
| `IT_030` | `TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT` | security-state service-boundary state | native report + trace + sysvar snapshot | `No` | - |
| `IT_031` | `TC_CANOE_IT_031_AUDIO_GUIDE_RUNTIME` | audio and voice-guide integrated state | panel capture + write window + native report | `No` | - |
| `IT_032` | `TC_CANOE_IT_032_OUTPUT_FALLBACK` | output-channel availability and fallback state | native report + trace + sysvar snapshot | `No` | - |
| `IT_033` | `TC_CANOE_IT_033_DUPLICATE_POPUP_SUPPRESSION` | duplicate-popup suppression state | native report + trace + sysvar snapshot | `No` | - |
| `IT_034` | `TC_CANOE_IT_034_CHANNEL_RESTORE` | channel-restore consistency state | native report + trace + sysvar snapshot | `No` | - |
| `IT_035` | `TC_CANOE_IT_EXT_005_DISTANCE_HISTORY` | distance and history-query result | panel capture + native report + `verification_log.csv` | `No` | - |
| `IT_036` | `TC_CANOE_IT_EXT_006_CHASSIS_EXT_CONTEXT` | EPB/EHB/VSM/ECS/CDC integrated state | native report + trace + sysvar snapshot | `No` | - |
| `IT_037` | `TC_CANOE_IT_EXT_007_OCCUPANT_COMFORT_CONTEXT` | occupant/comfort integrated state | native report + trace + sysvar snapshot | `No` | - |
| `IT_038` | `TC_CANOE_IT_EXT_008_DISPLAY_SERVICE_CONTEXT` | display/service integrated state | panel capture + trace + native report | `No` | - |
| `IT_039` | `TC_CANOE_IT_EXT_009_ADAS_PERCEPTION_CONTEXT` | adas/perception integrated state | native report + trace + sysvar snapshot | `No` | - |
| `IT_040` | `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG` | service, security, diagnostic integrated state | native report + trace + write window + sysvar snapshot | `Yes` | service-state cause, route ownership, diagnostic-state explanation |
| `IT_041` | `TC_CANOE_IT_EXT_011_CHARGE_POWER_CONTEXT` | power and charge integrated state | native report + trace + sysvar snapshot | `No` | - |
| `IT_042` | `TC_CANOE_IT_EXT_012_DISPLAY_CHANNELS` | cross-channel visual consistency | panel capture + screenshot + `verification_log.csv` | `No` | - |
| `IT_043` | `TC_CANOE_IT_EXT_013_AUDIO_GUIDE_CHANNEL` | audio-guide consistency | write window + audio state capture + `verification_log.csv` | `No` | - |
| `IT_044` | `TC_CANOE_IT_ETH_001_POLICE_TX` | police external tx observation | Ethernet trace + write window + `verification_log.csv` | `No` | - |
| `IT_045` | `TC_CANOE_IT_ETH_002_AMBULANCE_TX` | ambulance external tx observation | Ethernet trace + write window + `verification_log.csv` | `No` | - |

## 5. 07 System Test mapping draft

| ID | Candidate native asset | Primary oracle | Primary evidence | Diagnostic Needed? | Diagnostic intent |
|---|---|---|---|---|---|
| `ST_001` | `TC_CANOE_ST_CORE_001_POWER_ON_BASELINE` | no-warning baseline state | panel capture + screenshot + native report | `No` | - |
| `ST_002` | `TC_CANOE_ST_CORE_002_NORMAL_DRIVE` | nominal drive state | panel capture + screenshot + native report | `No` | - |
| `ST_003` | `TC_CANOE_ST_CORE_003_BASIC_WARNING_ACTIVATION` | basic warning activation result | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_004` | `TC_CANOE_ST_CORE_004_BASIC_WARNING_CLEAR` | clear-to-normal state | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_005` | `TC_CANOE_ST_CORE_005_ENTER_SCHOOL_ZONE` | school-zone warning transition | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_006` | `TC_CANOE_ST_CORE_006_EXIT_SCHOOL_ZONE` | school-zone recovery state | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_007` | `TC_CANOE_ST_CORE_007_HIGHWAY_POLICY_TRANSITION` | highway-mode transition | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_008` | `TC_CANOE_ST_CORE_008_STEERING_INACTIVITY` | warning trigger and clear result | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_009` | `TC_CANOE_ST_CORE_009_GUIDE_LEFT` | left-guidance visible result | cluster capture + screenshot + native report | `No` | - |
| `ST_010` | `TC_CANOE_ST_CORE_010_GUIDE_RIGHT_CLEAR` | right-guidance visible result | cluster capture + screenshot + native report | `No` | - |
| `ST_011` | `TC_CANOE_ST_V2_001_POLICE_OVERRIDE` | police-over-zone result | panel capture + trace + native report | `No` | - |
| `ST_012` | `TC_CANOE_ST_V2_002_AMBULANCE_OVERRIDE` | ambulance-over-zone result | panel capture + trace + native report | `No` | - |
| `ST_013` | `TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT` | police direction render | cluster/HUD capture + native report | `No` | - |
| `ST_014` | `TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT` | ambulance direction render | cluster/HUD capture + native report | `No` | - |
| `ST_015` | `TC_CANOE_ST_V2_005_AMBULANCE_PRIORITY` | final selected warning state | panel capture + trace + native report | `No` | - |
| `ST_016` | `TC_CANOE_ST_V2_006_POLICE_TIEBREAK` | ETA and SourceID arbitration result | native report + sysvar snapshot + trace | `No` | - |
| `ST_017` | `TC_CANOE_ST_V2_007_AMBULANCE_TIEBREAK` | ETA and SourceID arbitration result | native report + sysvar snapshot + trace | `No` | - |
| `ST_018` | `TC_CANOE_ST_018_POLICE_TX_PERIOD` | police tx periodicity observation | Ethernet trace + `verification_log.csv` + write window | `No` | - |
| `ST_019` | `TC_CANOE_ST_019_AMBULANCE_TX_PERIOD` | ambulance tx periodicity observation | Ethernet trace + `verification_log.csv` + write window | `No` | - |
| `ST_020` | `TC_CANOE_ST_V2_008_TIMEOUT_CLEAR` | timeout clear and return state | native report + trace + sysvar snapshot | `No` | - |
| `ST_021` | `TC_CANOE_ST_CORE_020_EMERGENCY_CLEAR_RESTORE` | restore-to-previous-warning state | panel capture + trace + native report | `No` | - |
| `ST_022` | `TC_CANOE_ST_EXT_001_INTERSECTION_DECEL` | combined warning/decel result | panel capture + trace + sysvar snapshot | `No` | - |
| `ST_023` | `TC_CANOE_ST_EXT_002_MERGE_DECEL` | combined warning/decel result | panel capture + trace + sysvar snapshot | `No` | - |
| `ST_024` | `TC_CANOE_ST_EXT_003_DRIVER_INTERVENTION_CLEAR` | clear-on-driver-intervention result | panel capture + trace + native report | `No` | - |
| `ST_025` | `TC_CANOE_ST_EXT_004_FAILSAFE_ENTRY` | fail-safe entry and minimum-channel state | native report + write window + trace + sysvar snapshot | `No` | - |
| `ST_026` | `TC_CANOE_ST_EXT_005_FAILSAFE_RECOVERY` | recovery-from-fail-safe state | native report + trace + sysvar snapshot | `No` | - |
| `ST_027` | `TC_CANOE_ST_EXT_006_FRONTAL_OBJECT_RISK` | object-warning visible result | panel capture + event log + trace | `No` | - |
| `ST_028` | `TC_CANOE_ST_EXT_007_LATERAL_OBJECT_RISK` | object-warning visible result | panel capture + event log + trace | `No` | - |
| `ST_029` | `TC_CANOE_ST_EXT_008_CUTIN_OBJECT_RISK` | object-warning visible result | panel capture + event log + trace | `No` | - |
| `ST_030` | `TC_CANOE_ST_030_SEATBELT_CONTEXT_ADJUST` | seat-belt and driver-context adjusted warning | panel capture + screenshot + native report | `No` | - |
| `ST_031` | `TC_CANOE_ST_031_DISTANCE_DISPLAY_CONSISTENCY` | emergency distance display consistency | panel capture + screenshot + native report | `No` | - |
| `ST_032` | `TC_CANOE_ST_EXT_010_USER_SETTING_CHANGE` | updated output policy state | panel capture + screenshot + native report | `No` | - |
| `ST_033` | `TC_CANOE_ST_EXT_011_HISTORY_QUERY` | history-view result | panel capture + screenshot + native report | `No` | - |
| `ST_034` | `TC_CANOE_ST_034_DUPLICATE_POPUP_GUARD` | duplicate-popup guard stability result | native report + trace + `verification_log.csv` | `No` | - |
| `ST_035` | `TC_CANOE_ST_035_TIMEOUT_CLEAR_RESTORE` | timeout-clear restore stability result | native report + trace + `verification_log.csv` | `No` | - |
| `ST_036` | `TC_CANOE_ST_036_FAILSAFE_RECOVERY_STABILITY` | fail-safe recovery stability result | native report + trace + `verification_log.csv` | `No` | - |
| `ST_037` | `TC_CANOE_ST_037_AUDIO_CHANNEL_STABILITY` | audio focus and ducking stability result | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_038` | `TC_CANOE_ST_038_VISUAL_CHANNEL_STABILITY` | popup priority and cluster sync stability result | panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_039` | `TC_CANOE_ST_EXT_014_CHASSIS_CONTEXT` | braking/stability context result | native report + trace + sysvar snapshot | `No` | - |
| `ST_040` | `TC_CANOE_ST_EXT_015_OCCUPANT_COMFORT_CONTEXT` | body/occupant/comfort context result | native report + trace + sysvar snapshot | `No` | - |
| `ST_041` | `TC_CANOE_ST_EXT_016_DISPLAY_SERVICE_CONTEXT` | display/service context result | panel capture + trace + native report | `No` | - |
| `ST_042` | `TC_CANOE_ST_EXT_017_ADAS_PERCEPTION_CONTEXT` | adas/perception context result | native report + trace + sysvar snapshot | `No` | - |
| `ST_043` | `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT` | service/security/diagnostic context result | native report + trace + write window + sysvar snapshot | `Yes` | diagnostic-state cause, route ownership, security/service reason |
| `ST_044` | `TC_CANOE_ST_EXT_019_CHARGE_POWER_CONTEXT` | power/charge context result | native report + trace + sysvar snapshot | `No` | - |
| `ST_045` | `TC_CANOE_ST_EXT_040_TRIP_SEQUENCE` | end-to-end scenario verdict | native report + panel capture + trace + `verification_log.csv` | `No` | - |
| `ST_046` | `TC_CANOE_ST_EXT_041_FAILSAFE_RECOVERY` | end-to-end fail-safe scenario verdict | native report + panel capture + trace + `verification_log.csv` | `No` | - |

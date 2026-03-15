# test_units

Native CANoe Test Unit assets for the current SIL cycle.

## Current Structure
- Shared harness set:
  - `TEST_SCN`
  - `TEST_BAS`
  - `common/ValidationHarnessTestCommon.cin`
- Representative active baseline assets:
- `TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING`
- `TC_CANOE_IT_EXT_001_OBJECT_RISK_EVENTLOG`
- `TC_CANOE_IT_EXT_002_DRIVER_CONTEXT`
- `TC_CANOE_IT_EXT_003_EMERGENCY_PLUS_TTC`
- `TC_CANOE_IT_BASE_001_POWERTRAIN_STATE`
- `TC_CANOE_IT_BASE_002_CHASSIS_STATE`
- `TC_CANOE_IT_BASE_003_BODY_STATE`
- `TC_CANOE_IT_BASE_004_BASIC_DISPLAY_UI`
- `TC_CANOE_IT_BASE_005_COMFORT_CONTEXT`
- `TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT`
- `TC_CANOE_IT_BASE_006_AUDIO_VOICE`
- `TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY`
- `TC_CANOE_IT_EXT_005_DISTANCE_HISTORY`
- `TC_CANOE_IT_ETH_001_POLICE_TX`
- `TC_CANOE_IT_ETH_002_AMBULANCE_TX`
- `TC_CANOE_ST_ETH_001_EXTERNAL_TX_PERIOD`
- Current diagnostic-linked scope skeletons:
  - `TC_CANOE_UT_EXT_016_SGW_SECURITY_STATE`
  - `TC_CANOE_UT_EXT_017_DCM_DIAGNOSTIC_STATE`
  - `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG`
  - `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT`
- Active level suites are kept under sibling path `../test_suites/`.
- Retired draft skeletons:
  - moved under `retire/`

## Ownership Split
- Dev2:
  - testcase portfolio
  - oracle/timing/evidence blueprint
  - skeleton `.can/.vtestunit.yaml/.vtesttree.yaml`
- Dev1:
  - common harness
  - concrete signal/message/assert hookup
  - GUI registration in CANoe
  - native `.vtestreport`

## Execution Status
- The two anchor assets are intended to be runnable.
- The current diagnostic-linked skeleton assets are not official pass targets yet.
- Skeleton assets intentionally stop at `oracle-hook` until Dev1 wires concrete stimulus/oracle paths.

## File Shape
- `*.can`
  - CAPL `export testcase` implementation or draft skeleton
- `*.vtestunit.yaml`
  - CANoe Test Unit descriptor
- `*.vtesttree.yaml`
  - Test tree / fixture mapping

## GUI Registration
Because `canoe/cfg/*.cfg` is GUI-first in this repo, register these assets in CANoe through the GUI.

Recommended path:
1. Open the active CANoe configuration in the GUI.
2. Add a Test Unit reference from the matching `*.vtestunit.yaml`.
3. Register only the two anchor assets first.
4. Enable each draft skeleton only after Dev1 replaces the `oracle-hook` placeholder with concrete assertions.
5. Save the configuration through the GUI only.

## Evidence
- Native CANoe test report (`.vtestreport`)
- Execution screenshot
- Measurement log / run-id binding
- Optional Dev2 packaging through TUI/CLI after native execution

## Wave 2 reserved baseline

The following direct-ownership UT assets define the current active `05` baseline:
`TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` (`206`),
`TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` (`207`),
`TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` (`208`),
`TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` (`209`),
`TC_CANOE_UT_CORE_005_EMS_ALERT_TXRX` (`4 -> 5 -> 6`),
`TC_CANOE_UT_OUT_001_BCM_AMBIENT` (`208 -> 4`),
`TC_CANOE_UT_OUT_002_IVI_HMI` (`215 -> 220 -> 222`),
`TC_CANOE_UT_OUT_003_CLU_DISPLAY` (`30 -> 33 -> 220`),
`TC_CANOE_UT_OUT_004_HUD_DISPLAY` (`30 -> 220`),
`TC_CANOE_UT_OUT_005_AMP_AUDIO` (`215`),
`TC_CANOE_UT_OUT_006_DECEL_ASSIST_REQ` (`16 -> 18`),
`TC_CANOE_UT_OUT_007_POLICE_TX` (`4`), and
`TC_CANOE_UT_OUT_008_AMBULANCE_TX` (`5`).

## Wave 2 execution progress

`TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` (`206`) and
`TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` (`207`) now have executable scenario bindings and concrete assert sets.
The remaining baseline assets (`208`, `209`, `4`, `5`) were then closed one by one with concrete scenario/oracle bindings.

`TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` (`208`) and
`TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` (`209`) now also have executable scenario bindings and concrete assert sets.
`TC_CANOE_UT_CORE_005_EMS_ALERT_TXRX` (`4 -> 5 -> 6`) now closes the emergency lifecycle unit row with activation, receive, and timeout-clear assertions.
`TC_CANOE_UT_OUT_001_BCM_AMBIENT`, `TC_CANOE_UT_OUT_002_IVI_HMI`, `TC_CANOE_UT_OUT_003_CLU_DISPLAY`,
`TC_CANOE_UT_OUT_004_HUD_DISPLAY`, `TC_CANOE_UT_OUT_005_AMP_AUDIO`, and `TC_CANOE_UT_OUT_006_DECEL_ASSIST_REQ`
now close the current direct-output unit rows one by one with exact scenario/oracle bindings.
`TC_CANOE_UT_OUT_007_POLICE_TX` (`4`) and
`TC_CANOE_UT_OUT_008_AMBULANCE_TX` (`5`) provide the dedicated external-TX unit contracts.
`TC_CANOE_UT_EXT_001_OBJECT_RISK`, `TC_CANOE_UT_EXT_002_CLU_CONTEXT_ADJUST`, and
`TC_CANOE_UT_EXT_003_DOMAIN_BOUNDARY_FAILSAFE` provide the exact executable unit contracts for
`UT_006`, `UT_007`, and `UT_008`.
The earlier context/display drafts for `UT_076/UT_077` were retired because they did not match the official external-TX reviewer rows.

## Wave 3 system baseline

Active system-test executable contracts now include:
`TC_CANOE_ST_V2_001_POLICE_OVERRIDE` (`11`),
`TC_CANOE_ST_V2_002_AMBULANCE_OVERRIDE` (`223`),
`TC_CANOE_ST_CORE_013_POLICE_DIRECTION_RIGHT` (`30`),
`TC_CANOE_ST_CORE_014_AMBULANCE_DIRECTION_LEFT` (`33`),
`TC_CANOE_ST_V2_005_AMBULANCE_PRIORITY` (`212`),
`TC_CANOE_ST_V2_006_POLICE_TIEBREAK` (`10`),
`TC_CANOE_ST_V2_007_AMBULANCE_TIEBREAK` (`224`),
`TC_CANOE_ST_ETH_001_EXTERNAL_TX_PERIOD` (`4 -> 5`, trace-gated),
`TC_CANOE_ST_V2_008_TIMEOUT_CLEAR` (`35`),
`TC_CANOE_ST_CORE_020_EMERGENCY_CLEAR_RESTORE` (`35`),
`TC_CANOE_ST_EXT_006_FRONTAL_OBJECT_RISK` (`20`),
`TC_CANOE_ST_EXT_007_LATERAL_OBJECT_RISK` (`21`),
`TC_CANOE_ST_EXT_008_CUTIN_OBJECT_RISK` (`22`),
`TC_CANOE_ST_EXT_009_CONTEXT_ADJUST` (`214 -> 222`),
`TC_CANOE_ST_EXT_010_USER_SETTING_CHANGE` (`215`),
`TC_CANOE_ST_EXT_011_HISTORY_QUERY` (`222 + historyQuery(0)`),
`TC_CANOE_ST_EXT_012_DELAY_STABILITY` (`12 -> 35 -> 201`),
`TC_CANOE_ST_EXT_013_CHANNEL_CONTENTION` (`215 -> 220`),
`TC_CANOE_ST_EXT_040_TRIP_SEQUENCE` (`200`), and
`TC_CANOE_ST_EXT_041_FAILSAFE_RECOVERY` (`201`).

`TC_CANOE_UT_CORE_004_V2X_EVENT_MAINTAIN` and `TC_CANOE_UT_CORE_005_ADAS_DECEL_ASSIST` are now active executable contracts.
This completes the current direct-ownership `05` core baseline at the scenario/assert-contract level.

## Wave 5 gateway and extension UT baseline

Active gateway and extension unit contracts now also include:
`TC_CANOE_UT_CORE_001_CGW_CHS_GW` (`216 -> 217 -> 218 -> 219`),
`TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW` (`2 -> 7 -> 8`),
`TC_CANOE_UT_CORE_004_NAV_CTX_MGR` (`2 -> 3 -> 7 -> 8`),
`TC_CANOE_UT_CORE_007_BODY_GW_ROUTE` (`208 -> 4`),
`TC_CANOE_UT_CORE_008_IVI_GW_ROUTE` (`209 -> 30 -> 33`),
`TC_CANOE_UT_EXT_004_CHS_BRAKE_EXT` (`216 -> 219`),
`TC_CANOE_UT_EXT_005_CHS_DYNAMICS_EXT` (`225`),
`TC_CANOE_UT_EXT_006_BODY_ENTRY_EXIT` (`226 -> 227`), and
`TC_CANOE_UT_EXT_007_BODY_OCCUPANT_PROTECTION` (`228`).

## Wave 6 service, assist, and router UT baseline

Active service, assist, and router unit contracts now also include:
`TC_CANOE_UT_EXT_008_BODY_COMFORT` (`229 -> 230`),
`TC_CANOE_UT_EXT_009_IVI_DISPLAY_SERVICE` (`229 -> 30 -> 215`),
`TC_CANOE_UT_EXT_010_IVI_SERVICE_ACCESS` (`229`),
`TC_CANOE_UT_EXT_011_ADAS_DRIVE_ASSIST` (`233`),
`TC_CANOE_UT_EXT_012_ADAS_PARKING_PERCEPTION` (`234`),
`TC_CANOE_UT_EXT_013_WARNING_DELIVERY_BOUNDARY` (`18 -> 203 -> 204`),
`TC_CANOE_UT_EXT_014_DOMAIN_ROUTER_PROPULSION` (`232`), and
`TC_CANOE_UT_EXT_015_DOMAIN_ROUTER_POWER_CHARGE` (`231`).

## Wave 4 integration baseline

Active integration-test executable contracts now include:
`TC_CANOE_IT_CORE_001_BASE_ACTIVATION` (`1 -> 2 -> 12`),
`TC_CANOE_IT_CORE_002_SCHOOLZONE_PATH` (`2`),
`TC_CANOE_IT_CORE_003_HIGHWAY_NOSTEER_PATH` (`3`),
`TC_CANOE_IT_V2_001_POLICE_RX` (`4`),
`TC_CANOE_IT_V2_002_AMBULANCE_RX` (`5`),
`TC_CANOE_IT_V2_003_ARBITRATION` (`9 -> 10 -> 11 -> 212`),
`TC_CANOE_IT_CORE_007_AMBIENT_OUTPUT` (`4`),
`TC_CANOE_IT_CORE_008_CLUSTER_DIRECTION_OUTPUT` (`30`),
`TC_CANOE_IT_V2_004_TIMEOUT_CLEAR` (`35`),
`TC_CANOE_IT_V2_005_DECEL_ASSIST` (`19`),
`TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING` (`18`), and
`TC_CANOE_IT_EXT_001_OBJECT_RISK_EVENTLOG` (`20 -> 21 -> 22 -> 24 -> 25`),
`TC_CANOE_IT_EXT_002_DRIVER_CONTEXT` (`214 -> 215`),
`TC_CANOE_IT_EXT_003_EMERGENCY_PLUS_TTC` (`213`),
`TC_CANOE_IT_BASE_001_POWERTRAIN_STATE` (`216 -> 217`),
`TC_CANOE_IT_BASE_002_CHASSIS_STATE` (`218 -> 219`),
`TC_CANOE_IT_BASE_003_BODY_STATE` (`211 -> 216`),
`TC_CANOE_IT_BASE_004_BASIC_DISPLAY_UI` (`220`),
`TC_CANOE_IT_BASE_005_BODY_SECURITY_CONTEXT` (`214 -> 203`),
`TC_CANOE_IT_BASE_006_AUDIO_VOICE` (`215`),
`TC_CANOE_IT_EXT_004_OUTPUT_AVAILABILITY` (`18 -> 12 -> 35`), and
`TC_CANOE_IT_EXT_005_DISTANCE_HISTORY` (`222 + historyQuery(0)`),
`TC_CANOE_IT_EXT_010_WINDOW_STATE` (`226`), and
`TC_CANOE_IT_EXT_014_BODY_CONTROL_LOCK` (`226`), and
`TC_CANOE_IT_EXT_015_WIPER_RAIN_BASELINE` (`229`).

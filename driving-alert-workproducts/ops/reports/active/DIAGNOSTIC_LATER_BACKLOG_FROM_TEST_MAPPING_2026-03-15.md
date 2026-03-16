# Optional Diagnostic Expansion Candidates from Test Mapping

> [!IMPORTANT]
> This document is an internal planning note extracted from items that are currently `No` in the official diagnostic decision.
> These items do not block the current CANoe SIL baseline and are not part of the current official diagnostic backlog.

## 1. Purpose

This note keeps optional future candidates from the current test mapping draft.

Use this document only when the project later wants to strengthen:

- failure-cause explanation
- serviceability
- boundary-health interpretation
- transport or timeout root-cause analysis
- advanced context or perception reasoning

## 2. Meaning of optional candidates

These candidates remain `No` in the current official mapping.
They are kept only as a planning note for future robustness, explainability, or serviceability work.

## 3. Unit Test optional candidates

| Source ID | Candidate native asset | Why diagnostic is not required now | Why it may be useful later | Future diagnostic focus |
|---|---|---|---|---|
| `UT_001` | `TC_CANOE_UT_CORE_001_CGW_CHS_GW` | runtime forwarding can be judged by trace and evidence | later boundary-fault explanation may need route detail | route reason, timeout source, boundary health |
| `UT_002` | `TC_CANOE_UT_CORE_002_CGW_INFOTAINMENT_GW` | navigation-context forwarding is observable in normal evidence | later infotainment-path issues may need ownership detail | route ownership, source-bus confirmation |
| `UT_004` | `TC_CANOE_UT_V2_001_EMS_ALERT_RX_TIMEOUT` | timeout clear is currently visible by state change | later timeout disputes may need stale-cause detail | timeout cause, stale-source reason |
| `UT_006` | `TC_CANOE_UT_EXT_001_OBJECT_RISK` | object-risk behavior can be judged by runtime evidence once implemented | later downgrade or confidence disputes may need deeper cause explanation | sensor confidence, downgrade reason |
| `UT_008` | `TC_CANOE_UT_EXT_003_DOMAIN_BOUNDARY_FAILSAFE` | fail-safe entry can be judged on the current oracle/evidence path | later boundary-fault explanation may still benefit from deeper cause visibility | boundary-fault cause, route failure reason, service degradation reason |
| `UT_010` | `TC_CANOE_UT_CORE_005_EMS_ALERT_TXRX` | tx/rx behavior can be observed in trace | later transport failures may need stronger diagnostic interpretation | transport cause, route detail |
| `UT_016` | `TC_CANOE_UT_EXT_004_CHS_BRAKE_EXT` | context reflection is observable now | later brake-assist cause explanation may be needed | brake-state reason |
| `UT_017` | `TC_CANOE_UT_EXT_005_CHS_DYNAMICS_EXT` | chassis-context reflection is observable now | later stability-context interpretation may need source detail | dynamics-state reason |
| `UT_019` | `TC_CANOE_UT_EXT_007_BODY_OCCUPANT_PROTECTION` | context state can be judged by current seams | later safety-context review may require stronger explanation | occupant-protection source reason |
| `UT_022` | `TC_CANOE_UT_EXT_010_IVI_SERVICE_ACCESS` | service-access behavior is observable now | later serviceability reviews may need service-state explanation | service-access reason |
| `UT_023` | `TC_CANOE_UT_EXT_011_ADAS_DRIVE_ASSIST` | availability can be judged by current runtime state | later ADAS availability disputes may need cause detail | function-availability reason |
| `UT_024` | `TC_CANOE_UT_EXT_012_ADAS_PARKING_PERCEPTION` | perception-context behavior is visible now | later confidence or downgrade analysis may need deeper state | perception confidence, downgrade reason |
| `UT_025` | `TC_CANOE_UT_EXT_013_WARNING_DELIVERY_BOUNDARY` | warning delivery failure can be judged on the current oracle/evidence path | later route or service explanation may still benefit from deeper visibility | service-state reason, boundary failure cause, route ownership |
| `UT_026` | `TC_CANOE_UT_EXT_014_DOMAIN_ROUTER_PROPULSION` | routing result is visible in trace | later propulsion-path issues may need source/route detail | route detail, source-bus reason |
| `UT_027` | `TC_CANOE_UT_EXT_015_DOMAIN_ROUTER_POWER_CHARGE` | power and charge context is visible now | later power-path issues may need deeper explanation | power-state reason, route detail |
| `UT_062` | `TEST_SCN IBOX service preset` | current injection logging is enough for baseline work | later service state reviews may want explicit diagnostic interpretation | service-state reason |
| `UT_065`-`UT_069` | `TEST_SCN backbone/powertrain presets` | current preset injection is enough for baseline work | later backbone/powertrain diagnostics may need richer interpretation | backbone service reason, powertrain state reason |
| `UT_076` | `TC_CANOE_UT_OUT_007_POLICE_TX` | tx observation is currently enough through Ethernet trace | later packet-loss or route-cause reviews may need diagnostic depth | transport-failure cause, route detail |
| `UT_077` | `TC_CANOE_UT_OUT_008_AMBULANCE_TX` | tx observation is currently enough through Ethernet trace | later packet-loss or route-cause reviews may need diagnostic depth | transport-failure cause, route detail |

## 4. Integration Test optional candidates

| Source ID | Candidate native asset | Why diagnostic is not required now | Why it may be useful later | Future diagnostic focus |
|---|---|---|---|---|
| `IT_009` | `TC_CANOE_IT_V2_004_TIMEOUT_CLEAR` | timeout clear can be judged by state transition and evidence | later stale-input disputes may need timeout-cause detail | timeout cause, restore-source reason |
| `IT_010` | `TC_CANOE_IT_V2_005_DECEL_ASSIST` | decel-assist result is observable now | later risk-source explanation may need deeper reasoning | risk-source reason |
| `IT_011` | `TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING` | fail-safe entry and minimum-channel behavior can be judged on the current oracle/evidence path | later trigger or delivery-fault explanation may still benefit from deeper visibility | fail-safe trigger reason, delivery-fault cause, boundary ownership |
| `IT_012` | `TC_CANOE_IT_EXT_001_OBJECT_RISK_EVENTLOG` | object-risk and event log can be checked without diagnostics | later confidence and downgrade analysis may need more detail | sensor confidence, downgrade reason |
| `IT_014` | `TC_CANOE_IT_014_DISPLAY_POLICY` | display-policy reflection can be judged by current evidence | later output-policy disputes may need deeper explanation | display-policy reason, rendered-direction cause |
| `IT_019` | `TC_CANOE_IT_019_POWERTRAIN_PARKED_BASELINE` | parked baseline is observable in the current evidence path | later drive-state reviews may need stronger state explanation | parked-state reason, speed-state reason |
| `IT_021` | `TC_CANOE_IT_021_CHASSIS_STEERING_BASELINE` | steering-input baseline is observable in the current seams | later steering-state disputes may need source detail | steering-state reason, speed-state reason |
| `IT_023` | `TC_CANOE_IT_023_CHASSIS_ACCEL_BASELINE` | acceleration-driven drive-mode behavior is currently observable | later drive-mode disputes may need deeper explanation | acceleration-state reason, drive-mode cause |
| `IT_026` | `TC_CANOE_IT_BASE_004_BASIC_DISPLAY_UI` | display integration is currently observable | later display-service disputes may need deeper explanation | display-state reason, service-state cause |
| `IT_028` | `TC_CANOE_IT_EXT_014_BODY_CONTROL_LOCK` | door lock/open reflection is observable in the current seams | later body-control disputes may need stronger cause detail | lock-state reason, open-state cause |
| `IT_031` | `TC_CANOE_IT_031_AUDIO_GUIDE_RUNTIME` | audio-guide runtime can be judged by current panel and write-window evidence | later audio-policy disputes may need deeper explanation | focus cause, ducking reason, volume-policy detail |
| `IT_032` | `TC_CANOE_IT_032_OUTPUT_FALLBACK` | fallback behavior is visible today | later channel-health reviews may need cause detail | fallback reason, channel-health cause |

## 5. System Test optional candidates

| Source ID | Candidate native asset | Why diagnostic is not required now | Why it may be useful later | Future diagnostic focus |
|---|---|---|---|---|
| `ST_018` | `TC_CANOE_ST_018_POLICE_TX_PERIOD` | police tx periodicity observation is currently enough via trace | later packet-loss or transport disputes may need deeper explanation | transport-failure cause, route detail |
| `ST_019` | `TC_CANOE_ST_019_AMBULANCE_TX_PERIOD` | ambulance tx periodicity observation is currently enough via trace | later packet-loss or transport disputes may need deeper explanation | transport-failure cause, route detail |
| `ST_020` | `TC_CANOE_ST_V2_008_TIMEOUT_CLEAR` | timeout clear is visible in the current oracle and evidence path | later failure analysis may need timeout-cause detail | timeout cause |
| `ST_021` | `TC_CANOE_ST_CORE_020_EMERGENCY_CLEAR_RESTORE` | restore behavior is visible in user-facing evidence | later arbitration or restore disputes may need cause detail | restore-source reason |
| `ST_022` | `TC_CANOE_ST_EXT_001_INTERSECTION_DECEL` | combined system result is currently observable | later source-contribution analysis may need deeper explanation | object/emergency contribution reason |
| `ST_023` | `TC_CANOE_ST_EXT_002_MERGE_DECEL` | combined system result is currently observable | later source-contribution analysis may need deeper explanation | object/emergency contribution reason |
| `ST_024` | `TC_CANOE_ST_EXT_003_DRIVER_INTERVENTION_CLEAR` | clear-on-driver-intervention is judged on the current oracle/evidence path | later root-cause review may still benefit from deeper visibility | intervention cause, clear trigger reason |
| `ST_025` | `TC_CANOE_ST_EXT_004_FAILSAFE_ENTRY` | system-level fail-safe entry is judged on the current oracle/evidence path | later root-cause review may still benefit from deeper visibility | fail-safe trigger cause, minimum-warning activation reason, service degradation cause |
| `ST_026` | `TC_CANOE_ST_EXT_005_FAILSAFE_RECOVERY` | recovery can be judged on the current oracle/evidence path | later restored-route or service explanation may still benefit from deeper visibility | recovery reason, restored route cause, restored service cause |
| `ST_027` | `TC_CANOE_ST_EXT_006_FRONTAL_OBJECT_RISK` | visible object-warning result is enough for current stage | later object-confidence or downgrade analysis may need more detail | confidence reason, downgrade cause |
| `ST_028` | `TC_CANOE_ST_EXT_007_LATERAL_OBJECT_RISK` | visible object-warning result is enough for current stage | later object-confidence or downgrade analysis may need more detail | confidence reason, downgrade cause |
| `ST_029` | `TC_CANOE_ST_EXT_008_CUTIN_OBJECT_RISK` | visible object-warning result is enough for current stage | later object-confidence or downgrade analysis may need more detail | confidence reason, downgrade cause |
| `ST_034` | `TC_CANOE_ST_034_DUPLICATE_POPUP_GUARD` | current stability result can be judged by trace and logs | later popup-density disputes may need deeper cause explanation | duplicate-popup cause, stability guard reason |
| `ST_035` | `TC_CANOE_ST_035_TIMEOUT_CLEAR_RESTORE` | current restore stability is observable | later timeout-recovery disputes may need deeper cause explanation | timeout cause, restore reason |
| `ST_036` | `TC_CANOE_ST_036_FAILSAFE_RECOVERY_STABILITY` | fail-safe recovery stability is observable today | later fail-safe oscillation analysis may need stronger cause explanation | recovery stability reason, fail-safe residue cause |
| `ST_037` | `TC_CANOE_ST_037_AUDIO_CHANNEL_STABILITY` | current evidence can show stable audio-channel behavior | later contention analysis may need audio-policy detail | focus cause, ducking reason, audio-policy cause |
| `ST_039` | `TC_CANOE_ST_EXT_014_CHASSIS_CONTEXT` | current result is observable | later vehicle-diagnostics expansion may need source detail | chassis-state reason |
| `ST_040` | `TC_CANOE_ST_EXT_015_OCCUPANT_COMFORT_CONTEXT` | current result is observable | later vehicle-diagnostics expansion may need source detail | occupant/comfort-state reason |
| `ST_045` | `TC_CANOE_ST_EXT_040_TRIP_SEQUENCE` | end-to-end trip verdict can be judged today with current evidence | later trip-level explainability may need richer cause breakdown | trip-level root-cause decomposition |
| `ST_046` | `TC_CANOE_ST_EXT_041_FAILSAFE_RECOVERY` | end-to-end fail-safe scenario verdict can be judged on the current oracle/evidence path | later trip-level root-cause review may still benefit from richer cross-stage explanation | trip-level fail-safe trigger cause, recovery reason, cross-stage diagnostic linkage |

## 6. Recommended promotion rule

Promote an optional candidate into the official `Yes` backlog when any of the following becomes true:

1. reviewer asks for root-cause evidence, not only visible behavior
2. serviceability becomes part of official acceptance
3. security or gateway ownership becomes part of the verdict
4. transport failure or timeout cause must be explained, not only observed
5. object confidence, downgrade cause, or function availability must be justified explicitly

## 7. Recommended implementation order

1. timeout and transport explanation
   - `UT_004`
   - `UT_010`
   - `UT_076`
   - `UT_077`
   - `IT_009`
   - `IT_031`
   - `IT_032`
   - `ST_018`
   - `ST_019`

2. fail-safe and route explanation
   - `UT_008`
   - `UT_025`
   - `IT_011`
   - `ST_024`
   - `ST_025`
   - `ST_041`

3. advanced context and perception reasoning
   - `UT_006`
   - `UT_023`
   - `UT_024`
   - `IT_012`
   - `IT_014`
   - `IT_026`
   - `ST_021`
   - `ST_022`
   - `ST_026`
   - `ST_027`
   - `ST_028`
   - `ST_037`

4. vehicle expansion and serviceability
   - `UT_016`
   - `UT_017`
   - `UT_019`
   - `UT_022`
   - `UT_026`
   - `UT_027`
   - `UT_062`
   - `UT_065`-`UT_069`
   - `IT_019`
   - `IT_021`
   - `IT_023`
   - `IT_028`
   - `ST_032`
   - `ST_033`
   - `ST_034`
   - `ST_035`
   - `ST_036`
   - `ST_039`
   - `ST_040`

## 8. Current decision

At the current project stage:

- keep these items out of the immediate diagnostic build scope
- keep them as `No` in the official mapping
- continue to judge them with oracle, trace, sysvar, report, and evidence
- use this note only when the project later decides to strengthen explanation depth

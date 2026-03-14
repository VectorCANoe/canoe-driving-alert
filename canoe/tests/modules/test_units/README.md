# test_units

Native CANoe Test Unit assets for the current SIL cycle.

## Current Structure
- Shared harness set:
  - `TEST_SCN`
  - `TEST_BAS`
  - `common/ValidationHarnessTestCommon.cin`
- Active anchor assets:
  - `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
  - `TC_CANOE_IT_V2_FAILSAFE_001_CGW`
- Current diagnostic-linked scope skeletons:
  - `TC_CANOE_UT_EXT_016_SGW_SECURITY_STATE`
  - `TC_CANOE_UT_EXT_017_DCM_DIAGNOSTIC_STATE`
  - `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG`
  - `TC_CANOE_ST_EXT_018_SERVICE_SECURITY_DIAG_CONTEXT`
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

The following direct-ownership UT assets are now reserved in the active tree and are intentionally kept as draft skeletons until `TEST_SCN` stimulus and concrete oracle bindings are fixed:
`TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` (`206`),
`TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` (`207`),
`TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` (`208`),
`TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` (`209`),
`TC_CANOE_UT_EXT_076_V2X_EVENT_CONTEXT` (`210`), and
`TC_CANOE_UT_EXT_077_CLU_WARNING_DISPLAY` (`211`).

## Wave 2 execution progress

`TC_CANOE_UT_CORE_003_CGW_BOUNDARY_STATUS` (`206`) and
`TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION` (`207`) now have executable scenario bindings and concrete assert sets.
The remaining wave-2 assets (`208` to `211`) are still maintained as draft skeletons.

`TC_CANOE_UT_CORE_014_BCM_AMBIENT_POLICY` (`208`) and
`TC_CANOE_UT_CORE_015_IVI_TEXT_MAPPING` (`209`) now also have executable scenario bindings and concrete assert sets.
Only `TC_CANOE_UT_EXT_076_V2X_EVENT_CONTEXT` (`210`) and `TC_CANOE_UT_EXT_077_CLU_WARNING_DISPLAY` (`211`) remain as wave-2 draft skeletons.

`TC_CANOE_UT_EXT_076_V2X_EVENT_CONTEXT` (`210`) and
`TC_CANOE_UT_EXT_077_CLU_WARNING_DISPLAY` (`211`) now also have executable scenario bindings and concrete assert sets.
Wave 2 (`206` to `211`) is now complete at the scenario/assert-contract level.

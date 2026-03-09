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
- Draft skeleton assets generated from Dev2 blueprint:
  - `TC_CANOE_UT_V2X_001_EMERGENCY_PRIORITY_ETA`
  - `TC_CANOE_UT_V2X_002_TIMEOUT_CLEAR`
  - `TC_CANOE_IT_V2_SYNC_001_DECEL_AND_WARNING`
  - `TC_CANOE_IT_ADAS_001_OBJECT_FORWARD_CONFLICT`
  - `TC_CANOE_NET_001_CAN_BUS_ARBITRATION_PRIORITY`
  - `TC_CANOE_NET_002_GW_ROUTE_FORWARDING_INTEGRITY`
  - `TC_CANOE_NET_003_TIMEOUT_STALE_CHAIN_CLEAR`
  - `TC_CANOE_NET_004_LOAD_PERIOD_JITTER_STABILITY`
  - `TC_CANOE_NET_005_DIAG_ROUTE_INTEGRITY`

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
- The nine draft skeleton assets are not official pass targets yet.
- Draft skeletons intentionally stop at `oracle-hook` until Dev1 wires concrete stimulus/oracle paths.

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

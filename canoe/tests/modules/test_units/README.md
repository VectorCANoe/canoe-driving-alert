# test_units

Native CANoe Test Unit assets for the current SIL cycle.

## Scope
- Keep the existing validation harness (`VAL_SCENARIO_CTRL`, `VAL_BASELINE_CTRL`)
- Add minimal official CANoe Test Unit PoC assets on top of that harness
- Leave Dev2 TUI/CLI as the external orchestration, packaging, and CI bridge

## Assets
- `TC_CANOE_UT_CORE_001_SCHOOLZONE_OVERSPEED`
  - scenario command: `2`
  - focus: school-zone overspeed warning path
- `TC_CANOE_IT_V2_FAILSAFE_001_DOMAIN_BOUNDARY`
  - scenario command: `18`
  - focus: fail-safe downgrade / domain-boundary path

## File Shape
- `*.can`
  - CAPL `export testcase` implementation
- `*.vtestunit.yaml`
  - CANoe Test Unit descriptor
- `*.vtesttree.yaml`
  - Test tree / fixture mapping

## GUI Registration
Because `canoe/cfg/*.cfg` is GUI-first in this repo, register these assets in CANoe through the GUI.

Recommended path:
1. Open the active CANoe configuration in the GUI.
2. Add a Test Unit reference from the matching `*.vtestunit.yaml`.
3. Save the configuration through the GUI only.
4. Capture the native test report and screenshot as evidence.

## Evidence
- Native CANoe test report
- Execution screenshot
- Measurement log / run-id binding
- Optional Dev2 packaging through TUI/CLI after native execution

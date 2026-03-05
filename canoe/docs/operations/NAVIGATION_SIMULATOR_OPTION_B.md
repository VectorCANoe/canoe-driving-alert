# Navigation Simulator (Option B)

## Purpose
- Drive `Infotainment::roadZone` and `Infotainment::navDirection` with grid-based coordinate movement.
- Inject sysvars through CANoe COM API for repeatable SIL scenarios.
- Keep XVP renderer bound to derived outputs (`UiRender::*`) only.

## Script
- `canoe/scripts/navigation_simulator.py`

## Recommended Panels
- `canoe/project/panel/SDV_Render_Debug.xvp`
- `canoe/project/panel/SDV_Demo_Stage.xvp`
- `canoe/project/panel/SDV_Cluster_View.xvp`

## Prerequisites
1. CANoe running state
2. Load `canoe/cfg/CAN_v2_topology_wip.cfg`
3. `project.sysvars` includes `UiRender` namespace
4. Start measurement (F9)

## Basic Execution
```powershell
python canoe/scripts/navigation_simulator.py --loop --interval-ms 250
```

## 주요 옵션
- `--width`, `--height`: grid size
- `--interval-ms`: step period (ms)
- `--steps`: total steps (`0` for infinite)
- `--loop`: repeat from path end
- `--random-walk`: randomized movement pattern
- `--no-speed-update`: skip `Chassis::*` injection
- `--dry-run`: log only, no COM write

## Injected Variables
- Navigation input:
  - `Infotainment::roadZone`
  - `Infotainment::navDirection`
  - `Infotainment::zoneDistance`
  - `Infotainment::speedLimit`
- Optional chassis input (default on):
  - `Chassis::vehicleSpeed`
  - `Chassis::driveState`
  - `Chassis::steeringInput`

## Operational Notes
- This simulator injects inputs only. Priority/timeout/arbitration logic remains in CAPL.
- Keep `Test::testScenario=0` for pure movement/input mode.
- Use `--seed` with random mode for reproducibility.

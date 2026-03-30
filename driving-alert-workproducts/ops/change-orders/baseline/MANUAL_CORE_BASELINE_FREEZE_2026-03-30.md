# Manual Core Baseline Freeze (2026-03-30)

## Purpose

- `Input_Console` manual vehicle path is now treated as a protected baseline.
- Future cleanup/refactor work must not break the owner-ECU manual car behavior.
- This note is internal execution guidance, not a reviewer-facing publication asset.

## Protected Manual Scope

- selector baseline: `P / N / D / R`
- manual propulsion: throttle / brake
- steering extremes
- manual cruise engage + set
- ambient command reflection
- body manual controls:
  - door unlock/open at standstill
  - window down
  - turn signal
  - front wiper animation

## Execution Rule

Do not change manual vehicle semantics unless the same session re-runs the smoke and confirms `overall_pass=true`.

Required smoke:

- script: `canoe/tools/20_VERIFICATION/20_verify_manual_core_vehicle.py`
- output root: `canoe/tmp/manual_core_vehicle_smoke/`

## Current Passing Snapshot

- latest verified run:
  - `canoe/tmp/manual_core_vehicle_smoke/20260330_220635_manual_core_vehicle`
- result:
  - `overall_pass=true`
  - `step_count=13`

## Current Expected Baseline

- `P` idle:
  - `driveState=0`
  - `vehicleSpeed=0`
- `D + throttle100`:
  - `driveState=3`
  - `throttlePosition=100`
  - `vehicleSpeed >= 100`
- `D + brake100`:
  - `vehicleSpeed=0`
  - `brakePressure=100`
- `N + throttle40`:
  - `vehicleSpeed=0`
- `R + throttle100`:
  - reverse low-speed magnitude band
- steering:
  - `Cmd::steeringAngleCmd=-540 -> Chassis::steeringAngle=0`
  - `Cmd::steeringAngleCmd=+540 -> Chassis::steeringAngle=138`
- cruise:
  - `cruiseSetSpeed=50` latches and speed rises
- ambient:
  - `Cmd::ambientModeCmd=3 -> Body::ambientMode=3`
- body manual controls:
  - door unlock/open at standstill lifts `Body::windowPos` to open threshold
  - window down increases `Body::windowPos`
  - right turn sets `CoreState::turnLampState=2`
  - intermittent wiper advances `Body::frontWiperAnimFrame`

## Known Simplifications

- `driveState` is still the `PRND selector state`, not a pure motion-state signal.
- reverse is still represented as reverse-speed magnitude, not signed negative velocity.
- these are semantics cleanup items, not current blockers.

## Do Not Overdo

- do not reopen broad vehicle dynamics redesign while the baseline is stable
- do not reintroduce `TEST`-dependent ownership into normal manual owner paths
- do not change donor panel contracts to compensate for runtime behavior

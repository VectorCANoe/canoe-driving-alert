# CANoe Documentation

This folder provides the official developer documentation for the CANoe SIL baseline. It explains how the runtime surface is structured, how interfaces are contracted, how verification is executed, and how results are judged.

## Start Here

1. `architecture/ecu-classification.md`
2. `architecture/surface-runtime-verification-map.md`
3. `architecture/skeleton.md`
4. `contracts/communication-matrix.md`
5. `contracts/owner-route.md`
6. `verification/oracle.md`

## Repository Layout

- `architecture/`
  - ECU roles, runtime boundaries, verification placement, and harness structure
- `contracts/`
  - message ownership, route and timeout rules, Ethernet interfaces, diagnostics, and panel or sysvar contracts
- `verification/`
  - execution flow, acceptance criteria, oracle rules, and evidence handling
- `operations/`
  - GUI-first operations, source-to-mirror sync rules, and execution procedure

## Simulation and Test Workflow

1. Read `architecture/` to understand the runtime shape and ECU roles.
2. Read `contracts/` to identify owners, routes, timeout behavior, and interface boundaries.
3. Use `operations/` when applying GUI-first changes or syncing `src/capl` with `cfg/channel_assign`.
4. Run and judge verification with `verification/execution-guide.md`, `verification/acceptance-criteria.md`, `verification/oracle.md`, and `verification/evidence-policy.md`.

## Test Result Handling

- `verification/oracle.md`
  - defines what must be true for a result to be accepted as correct
- `verification/acceptance-criteria.md`
  - defines scenario-level PASS or FAIL conditions
- `verification/evidence-policy.md`
  - defines what evidence must be retained for review
- `verification/execution-guide.md`
  - defines how native CANoe test execution is performed for this baseline

## Related Documents

- `../README.md`
  - external entry point for the CANoe repository surface
- `../cfg/GUI_ONLY_OPERATIONS.md`
  - GUI-first constraints for CANoe configuration handling

# CANoe Runtime Surface

This folder contains the active CANoe runtime for the driving-alert CANoe SIL baseline.

It is the external entrypoint for readers who want to understand:

- how the CANoe project is structured
- where runtime assets live
- how simulation and native test execution are performed
- how verification results are reviewed

## Start Here

1. `cfg/CAN_v2_topology.cfg`
2. `docs/README.md`
3. `FILE_INDEX.md`

## Repository Layout

| Path | Purpose |
| --- | --- |
| `cfg/` | active CANoe configuration and GUI import mirror |
| `databases/` | active CAN DBC set for the current baseline |
| `project/` | panel and system-variable surfaces |
| `src/capl/` | CAPL source of truth for runtime behavior |
| `tests/` | native CANoe test assets and execution packages |
| `docs/` | official development documents for architecture, contracts, verification, and operations |
| `tools/` | helper tools used to maintain or validate the runtime surface |

## Runtime Workflow

### 1. Prepare

- open the active CANoe configuration
- load the required CAN databases
- confirm panel and SysVar surfaces are available
- keep `src/capl/` and `cfg/channel_assign/` aligned

### 2. Build and simulate

- compile the CAPL nodes
- start measurement
- execute the selected scenario or native Test Unit asset

### 3. Review behavior

- inspect panel and SysVar outputs
- review runtime signals and warning outputs
- confirm scenario or baseline verdict state

## Test Result Handling

The current baseline uses a harness-first result model:

- `TEST_SCN` produces the scenario verdict
- `TEST_BAS` aggregates the baseline verdict
- native CANoe Test Unit assets produce executable reports
- evidence is completed through report, screenshot, log, and supporting trace artifacts

Use these documents together:

- `docs/verification/execution-guide.md`
- `docs/verification/acceptance-criteria.md`
- `docs/verification/oracle.md`
- `docs/verification/evidence-policy.md`

## Related Documents

- `docs/architecture/ecu-classification.md`
- `docs/architecture/surface-runtime-verification-map.md`
- `docs/architecture/skeleton.md`
- `docs/contracts/communication-matrix.md`
- `docs/contracts/owner-route.md`

## Scope

This folder owns the CANoe runtime surface only.

It does not act as the canonical owner of:

- customer workproducts
- operator packaging surface
- local research and archive material

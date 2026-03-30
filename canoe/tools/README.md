# tools

Active utility scripts for CANoe maintenance.

## Folder Convention

- `10_RUNTIME/`
  - runtime-side generation helpers
- `20_VERIFICATION/`
  - verification-side gates and checks

## Naming Rule

- `10_*` : runtime helpers
- `20_*` : verification helpers

## Kept Tools

### `10_RUNTIME/10_generate_can_dbc_from_docs.py`
- generate draft DBC baselines from current `0303/0304` docs
- output path: `canoe/databases/`
- always review output manually before integration

### `20_VERIFICATION/20_validate_runtime_priority_gate.py`
- enforce the active CAN/ETH priority gate
- uses active CAN DBCs and `ethernet-backbone.md`
- writes local draft outputs under `canoe/tmp/`
- exit code `0` = pass, `2` = fail

### `20_VERIFICATION/20_build_ecu_flow_appendix.py`
- generate the active ECU-by-ECU appendix from `channel_assign`, split DBCs, runtime ownership matrix, and native test assets
- output path: `canoe/docs/architecture/ecu-flow-appendix.md`
- use this before promoting ECU interaction content into `driving-alert-workproducts` appendix or TeX assets

### `20_VERIFICATION/20_build_ecu_master_book.py`
- generate the official CANoe ECU master-book asset pack
- output path: `canoe/docs/architecture/master_book/`
- includes:
  - ECU metadata dataset
  - master markdown book
  - ECU card index
  - Group 06 SVG
  - full per-ECU SVG card pack
  - PlantUML-based `png/flows/*.png` renders for action signal flows
- rendering prerequisites:
  - global PlantUML: `C:\PlantUML\plantuml-1.2024.8.jar`
  - fallback vendored jar: `canoe/tools/20_VERIFICATION/vendor/plantuml-1.2024.8.jar`
  - Java runtime on PATH, or `C:\Program Files\Java\jdk1.8.0_261\bin\java.exe`

### `20_VERIFICATION/20_probe_runtime_couplings.py`
- capture reproducible runtime coupling evidence from an active CANoe session
- requires:
  - CANoe already open with the intended cfg
  - measurement already running
- supports named probe profiles:
  - `alert`
  - `body`
  - `access`
  - `brake`
  - `all`
- optional scenario trigger:
  - `--scenario-id <id>`
- output path:
  - `canoe/tmp/runtime_probes/<timestamp>_<profile>[_scnN]/`
- writes:
  - `probe.json`
  - `probe.csv`
  - `README.txt`

### `20_VERIFICATION/20_verify_manual_core_vehicle.py`
- verify the owner-ECU manual baseline car from an active CANoe session
- checks:
  - `P/N/D/R` selector behavior
  - throttle / brake
  - steering extremes
  - manual cruise set
  - ambient command reflection
  - door unlock/open standstill path
  - window down path
  - turn signal reflection
  - wiper animation path
- requires:
  - CANoe already open with the intended cfg
  - measurement already running
- output path:
  - `canoe/tmp/manual_core_vehicle_smoke/<timestamp>_manual_core_vehicle/`
- writes:
  - `result.json`
  - `README.txt`

## Policy

- `driving-alert-workproducts` documents remain the source of truth
- generated artifacts are draft support outputs
- cfg patch helpers and reference-side helper scripts are not kept in the active tree

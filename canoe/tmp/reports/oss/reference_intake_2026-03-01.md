# Reference Intake Report (2026-03-01)

## 1) Imported Reference Sets (read-only)
- Vector sample pack copied to: `canoe/reference/vector_samples_19_4_10`
- Approximate source size: `0.82 GB`
- Open-source references cloned (shallow) to: `canoe/reference/oss`
- Git exclusion rules added:
  - `canoe/reference/vector_samples_19_4_10/`
  - `canoe/reference/oss/`

## 2) Sample Inventory Summary (Vector 19.4.10)
- Top-level folders: 31+
- Relevant artifact counts:
  - `*.cfg`: 298
  - `*.stcfg`: 10
  - `*.can`: 749
  - `*.dbc`: 121
  - `*.xml`: 500

### Focused sample candidates for this project
- CAN<->CAN GW CAPL pattern:
  - `canoe/reference/vector_samples_19_4_10/J1939/MoreExamples/Gateway/J1939Gateway.cfg`
  - `canoe/reference/vector_samples_19_4_10/J1939/MoreExamples/Gateway/Nodes/Gateway_CAN1_CAN2.can`
- Ethernet/UDP simulation CAPL pattern:
  - `canoe/reference/vector_samples_19_4_10/Ethernet/Simulation/UDPBasicCAPL/UDPBasicCAPL.cfg`
  - `canoe/reference/vector_samples_19_4_10/Ethernet/Simulation/UDPBasicCAPL/CAPL/Sender.can`
  - `canoe/reference/vector_samples_19_4_10/Ethernet/Simulation/UDPBasicCAPL/CAPL/Receiver.can`
- Ethernet SOME/IP service pattern:
  - `canoe/reference/vector_samples_19_4_10/Ethernet/Simulation/SOMEIPBasicAutosar/SOMEIPBasicAutosar.cfg`
  - `canoe/reference/vector_samples_19_4_10/Ethernet/Simulation/SOMEIPBasicAutosar/CAPL/ADAS.can`
  - `canoe/reference/vector_samples_19_4_10/Ethernet/Simulation/SOMEIPBasicAutosar/CAPL/CAMF.can`
- SIL harness baseline:
  - `canoe/reference/vector_samples_19_4_10/SIL/SilAdapterBasicPython/CANoe/SilAdapterBasicPython.cfg`
  - `canoe/reference/vector_samples_19_4_10/SIL/SilAdapterBasicCpp/CANoe/SilAdapterBasicCpp.cfg`

## 3) Open-source shortlist (cloned)
- `sil-kit` (`vectorgrp/sil-kit`): MIT
- `vsomeip` (`COVESA/vsomeip`): MPL-2.0
- `can-utils` (`linux-can/can-utils`): mixed SPDX (GPL-2.0-only / BSD-3-Clause / LGPL-2.0-only)
- `python-can` (`hardbyte/python-can`): LGPL-3.0
- `python-udsoncan` (`pylessard/python-udsoncan`): MIT
- `uds` (`mdabrowski1990/uds`): MIT

## 4) Immediate applicability to current 4-axis plan
1. cfg/stcfg + IL mapping:
- Reuse structure references from `J1939Gateway.cfg`, `UDPBasicCAPL.cfg`, `SOMEIPBasicAutosar.cfg`.
- Keep current runtime profile as split-domain DBC (`*_can.dbc`) only.

2. Domain DBC + ETH contract:
- Maintain current domain-split DBCs (no merge).
- Use SOME/IP/UDP samples as field-level contract examples only.

3. Domain ECU CAPL + GW nodes:
- Reuse gateway event patterns (`on message` / `on pg` filter-forward logic) from J1939 Gateway sample.
- Reuse UDP socket lifecycle pattern (`on start` open, `on preStop` close) from UDPBasicCAPL.

4. SIL harness + evidence logs:
- Use SIL adapter samples for harness startup scripts and panel trigger flow.
- Keep verification evidence generation in local `canoe/tmp` and project test docs chain.

## 5) Guardrails
- No full overwrite from references.
- Only partial, traceable edits in `canoe/` implementation files.
- Keep domain-separated DBC topology unchanged.

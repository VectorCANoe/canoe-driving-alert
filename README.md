<div align="center">

# canoe-driving-alert

### CAN Communication Project in Hyundai Mobis Bootcamp with Vector Korea

A public repository for designing, verifying, and reviewing a driving-alert system in CANoe SIL.

[English](README.md) | [한국어](README.ko.md)

</div>

<details>
<summary><strong>Project background</strong></summary>

This project was developed as part of the Hyundai Mobis Bootcamp in collaboration with Vector Korea.
It is structured as a public engineering repository that connects communication design, CANoe runtime assets, traceable workproducts, and verification tooling in one place.

</details>

<details>
<summary><strong>Major references</strong></summary>

- Vector CANoe documentation and sample configurations
- Automotive SPICE PAM 3.1
- ISO 26262
- AUTOSAR Classic Platform SWC Modeling Guide
- project-result review samples used to shape workproduct structure and reviewer-facing format

</details>

---

## Overview

Most CAN communication repositories expose only one layer of the work: runtime assets, code, or test outputs.

This repository is built to show the full engineering path:

- communication design
- CANoe runtime implementation
- V-cycle workproducts
- verification execution and review tooling

## Highlights

- CAN + Ethernet communication modeling in CANoe SIL
- end-to-end traceability from requirement to verification
- operator-facing product surface for review workflows
- shared automation for gates, quality checks, and release support

## System flow

```text
Requirements
  -> Functional Definition
  -> Network Flow
  -> Communication Specification
  -> System Variables
  -> CANoe Runtime and CAPL
  -> Unit / Integration / System Verification
```

## Quick start

```powershell
python scripts/run.py
python scripts/run.py gate all
python scripts/run.py scenario run --id 4
python scripts/run.py verify quick --run-id 20260308_0900 --owner DEV2
```

## Repository map

| Path | Purpose |
| --- | --- |
| [`canoe/`](canoe/) | CANoe runtime project, configuration, CAPL source, contracts, and verification docs |
| [`driving-alert-workproducts/`](driving-alert-workproducts/) | canonical workproducts and traceable engineering documents |
| [`product/`](product/) | operator-facing product surface and review assets |
| [`scripts/`](scripts/) | shared launchers, gates, quality tooling, and release helpers |

## Start here

- [`canoe/README.md`](canoe/README.md)
- [`product/sdv_operator/README.md`](product/sdv_operator/README.md)
- [`product/sdv_operator/docs-src/index.md`](product/sdv_operator/docs-src/index.md)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidance.


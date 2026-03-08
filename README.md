# canoe-driving-alert

**CAN Communication Project in Hyundai Mobis Bootcamp with Vector Korea**

## Developer Start

If the repository feels too large, do not scan the whole tree first.
Start here:

1. [DEVELOPMENT_ENTRYPOINTS.md](C:\Users\이준영\CANoe-IVI-OTA\DEVELOPMENT_ENTRYPOINTS.md)
2. [canoe/FILE_INDEX.md](C:\Users\이준영\CANoe-IVI-OTA\canoe\FILE_INDEX.md)
3. [scripts/README.md](C:\Users\이준영\CANoe-IVI-OTA\scripts\README.md)
4. [product/sdv_operator/README.md](C:\Users\이준영\CANoe-IVI-OTA\product\sdv_operator\README.md)

Daily operator/developer commands stay narrow:

- `python scripts/run.py`
- `python scripts/run.py gate all`
- `python scripts/run.py scenario run --id <n>`
- `python scripts/run.py verify quick --run-id <RUN_ID> --owner <OWNER>`

## 🚗 Project Overview

This project focuses on a **real-time driving situation warning system** implemented with **Vector CANoe SIL simulation**.  
The current scope is centered on:
- navigation-context warnings (school zone, highway, guide section),
- emergency vehicle approach alerts (police/ambulance),
- stable warning arbitration and transition control,
- synchronized outputs to ambient lighting and cluster HMI.

### Organization
- **Organization Name**: VectorCANoe
- **Repository**: canoe-driving-alert
- **Partner**: Vector Korea Co., Ltd.
- **Program**: Hyundai Mobis Bootcamp

---

## 🎯 Project Objectives

### Phase 1: Driving Situation Warning Design
1. **Navigation Context Recognition**
   - Detect road-zone context and driving-state conditions
   - Reflect context transitions in warning policy
   - Handle direction guidance scenarios for driver awareness

2. **Emergency Alert Integration**
   - Receive and process emergency approach events (Police/Ambulance)
   - Distinguish vehicle type/direction and expose unified alert context
   - Guarantee safe clear behavior with timeout handling

3. **Warning Arbitration Policy**
   - Resolve concurrent warning conflicts by fixed priority rules
   - Ensure deterministic selection results for identical inputs
   - Minimize transition flicker and maintain driver readability

### Phase 2: SIL Validation and Evidence
1. **CAN + Ethernet Domain Integration in CANoe SIL**
   - Simulate domain gateways and ECU interactions
   - Route context and warning data across CAN and Ethernet boundaries
   - Verify end-to-end warning chain behavior

2. **V-Model Traceability and Test Closure**
   - Maintain full chain: `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST`
   - Execute unit/integration/system tests in SIL scope
   - Record pass/fail evidence and trace logs

---

## 🚀 V-Model Reference Artifacts

A complete V-Model documentation set is maintained under `driving-situation-alert/` and supporting standards under `reference/standards/`.

- **Documentation**: 00~07 lifecycle documents (requirements, architecture, communication, implementation, and tests)
- **CANoe Project**: Simulation assets under `canoe/` (CFG, CAPL, DBC, SysVars, test modules)
- **Traceability**: Audit-ready mapping across requirements, communication design, variables, and verification artifacts

👉 **Primary working set**: `driving-situation-alert/` and `canoe/`

---

## 🛠️ Core Technologies & Skills

### Primary Skills
1. **Driving Situation Warning Architecture**
   - Context-aware warning design
   - Priority arbitration policy
   - Multi-domain warning output coordination

2. **Vector CANoe**
   - CAPL scripting
   - Network simulation
   - SIL-based ECU behavior validation
   - Measurement/trace analysis

3. **CAN + Ethernet Communication**
   - CAN message/database (DBC) design
   - Ethernet alert contract handling (UDP in SIL scope)
   - Gateway-based routing between domains

### Technical Stack
- **Simulation Platform**: Vector CANoe
- **Programming**: CAPL (CAN Access Programming Language)
- **Protocols**: CAN, Ethernet (UDP)
- **Verification Scope**: CANoe SIL
- **Quality Basis**: ASPICE/ISO 26262-aligned documentation discipline

---

## 📁 Project Structure

```
canoe-driving-alert/
├── README.md
├── AGENTS.md
├── canoe/
│   ├── cfg/                  # CANoe configuration files
│   ├── src/capl/             # CAPL node implementations
│   ├── databases/            # Domain CAN DBC files
│   ├── project/sysvars/      # System variable definitions
│   ├── test_modules/         # CANoe test modules
│   └── docs/                 # CANoe operation/architecture notes
├── driving-situation-alert/
│   ├── 00_VModel_Mapping.md
│   ├── 01_Requirements.md
│   ├── 02_Concept_design.md
│   ├── 03_Function_definition.md
│   ├── 0301_SysFuncAnalysis.md
│   ├── 0302_NWflowDef.md
│   ├── 0303_Communication_Specification.md
│   ├── 0304_System_Variables.md
│   ├── 04_SW_Implementation.md
│   ├── 05_Unit_Test.md
│   ├── 06_Integration_Test.md
│   ├── 07_System_Test.md
│   └── tmp/                  # Working notes/reports/templates
├── docs/
│   ├── meeting-notes/        # Meeting records
│   └── mentoring/            # Mentoring feedback logs
├── reference/
│   ├── standards/            # ASPICE / ISO26262 / sample standards
│   └── dbc/                  # Reference DBC collections
└── scripts/
    ├── gates/                # Quality gate scripts (cfg/doc/capl/cli)
    ├── quality/              # Verification/evidence scripts (non-gate)
    ├── canoe/                # CANoe utility scripts
    ├── docs/                 # Document support scripts
    ├── report/               # Report conversion utilities
    └── run.py                # Unified local command entrypoint
```

---

## 🚀 Getting Started

### Prerequisites
- Vector CANoe (SIL environment)
- Basic understanding of CAN/Ethernet communication
- Familiarity with automotive ECU interaction
- CAPL programming knowledge

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/VectorCANoe/canoe-driving-alert.git
   cd canoe-driving-alert
   ```

2. Open CANoe and load configuration files from `canoe/cfg/`

3. Import CAN databases from `canoe/databases/`

### Running Simulations
1. Open the target `.cfg` in CANoe
2. Confirm CAPL node bindings from `canoe/src/capl/`
3. Start measurement and monitor trace/result panels
4. Validate message flow and warning output behavior

### Local Gate Commands (Recommended)
- `python scripts/run.py gate cfg-hygiene`
- `python scripts/run.py gate capl-sync`
- `python scripts/run.py gate doc-sync`
- `python scripts/run.py gate cli-readiness`

---

## 📊 Key Features

### ✅ Implemented Features
- Navigation-zone context handling (school zone / highway / guide section)
- Emergency approach alert handling (police / ambulance)
- Deterministic warning arbitration:
  - `Emergency > Navigation`
  - `Ambulance > Police`
  - `ETA tie -> SourceID ascending`
- Timeout-based clear policy (`1000ms`) and transition stabilization
- Ambient + Cluster synchronized warning output
- V-model traceability document chain (00~07)

### 🔄 Development Workflow
1. **Design**: Define requirements and warning policy
2. **Implementation**: Develop CAPL logic and communication mapping
3. **Simulation**: Verify behavior in CANoe SIL
4. **Validation**: Execute UT/IT/ST and check traceability closure
5. **Documentation**: Update evidence and maintain audit-ready chain

---

## 🧪 Testing & Validation

### Simulation Testing
- Unit tests for node-level functional behavior (`05`)
- Integration tests for inter-node/domain behavior (`06`)
- System scenario tests for end-to-end warning chain (`07`)

### Traceability Verification
- Document chain validation from requirements to test evidence
- Communication consistency checks across `0302/0303/0304` and CANoe assets
- CI quality gates for cfg hygiene, CAPL sync, doc/code sync, and CLI readiness

---

## 📝 Documentation

All project documentation is maintained under:
- `driving-situation-alert/` for V-model documents (00~07)
- `docs/` for meeting/mentoring records
- `canoe/docs/` for implementation/operation guidance

---

## 👥 Contributors

This project is developed as part of the Hyundai Mobis Bootcamp in collaboration with Vector Korea Co., Ltd.

---

## 📄 License

This project is part of the Hyundai Mobis Bootcamp educational program.

License and reference handling:
- Vendor tool dependency (Vector CANoe) is commercial/EULA-based and not redistributed by this repository.
- Vendor sample bundles are treated as reference-only assets unless redistribution permission is explicitly confirmed.
- Operational license reference:
  - `canoe/docs/operations/reference/LICENSE_REFERENCE_REPORT.md`
  - `canoe/docs/operations/reference/OPEN_SOURCE_INTAKE_POLICY.md`

---

## 🔗 Resources

- [Vector CANoe Documentation](https://www.vector.com/int/en/products/products-a-z/software/canoe/)
- [CAN in Automation (CiA)](https://www.can-cia.org/)
- [Hyundai Mobis](https://www.mobis.co.kr/)
- [Vector Korea](https://www.vector.com/kr/ko/)

### OSS Reference Sources

CAN Protocol / Utilities
- [can-utils](https://github.com/linux-can/can-utils) — Linux CAN utilities (candump, cansend, etc.)
- [can-isotp](https://github.com/hartkopp/can-isotp) — ISO 15765-2 (CAN TP) Linux kernel module
- [ICSim](https://github.com/zombieCraig/ICSim) — Instrument Cluster CAN simulator (vcan-based)

DBC / Signal Parsing
- [cantools](https://github.com/eerimoq/cantools) — DBC parser + signal encode/decode (Python)
- [canmatrix](https://github.com/ebroecker/canmatrix) — DBC / ARXML / KCD / SYM format converter
- [opendbc](https://github.com/commaai/opendbc) — Real-world DBC collection (Hyundai/Kia/Toyota, etc.)
- [CANpy](https://github.com/stefanhoelzl/CANpy) — Python CAN node simulator
- [atkv](https://github.com/atkv/atkv) — Lightweight CAN frame parser

Python CAN / Diagnostics
- [python-can](https://github.com/hardbyte/python-can) — Python CAN bus interface library
- [python-can-isotp](https://github.com/pylessard/python-can-isotp) — ISO-TP layer over python-can
- [python-udsoncan](https://github.com/pylessard/python-udsoncan) — UDS (ISO 14229) Python implementation
- [python-uds](https://github.com/StephanHCB/python-uds) — Lightweight UDS Python (ECU simulator pattern)
- [iso14229](https://github.com/driftregion/iso14229) — UDS ISO 14229 implementation in C (embedded ECU)

Vehicle Network Middleware
- [sil-kit](https://github.com/vectorgrp/sil-kit) — Vector SIL Kit source (CANoe SIL integration)
- [sil-kit-docs](https://github.com/vectorgrp/sil-kit-docs) — SIL Kit official documentation
- [vsomeip](https://github.com/COVESA/vsomeip) — AUTOSAR SOME/IP implementation (Ethernet ECU)

---

**Last Updated**: March 2026

# IVI vECU Architecture Documentation

This directory contains the complete system architecture documentation for the IVI vECU project, designed according to ISO 26262, AUTOSAR Classic, and Automotive SPICE standards.

## Main Documents

- **[architecture_overview.md](./architecture_overview.md)** - High-level system architecture with AUTOSAR layered structure, requirements traceability matrix, and V-Model integration
- **[implementation_plan.md](./implementation_plan.md)** - Detailed implementation plan outlining the modular documentation approach and verification strategy
- **[walkthrough.md](./walkthrough.md)** - Comprehensive project walkthrough summarizing all deliverables, requirements coverage, and verification approach

## Detailed Diagrams

All diagrams are created using PlantUML and are located in the `diagrams/` subdirectory:

### [diagrams/lighting_control_architecture.md](./diagrams/lighting_control_architecture.md)
- Component architecture for lighting subsystem
- Speed-linked ambient lighting state machine (REQ_IVI_001)
- Door-linked UX lighting sequences (REQ_IVI_003)
- Reverse rear lighting control (REQ_IVI_017)
- IVI color synchronization flow (REQ_IVI_004)

### [diagrams/safety_system_architecture.md](./diagrams/safety_system_architecture.md)
- ASIL-D critical safety components
- Reverse safety manager state machine (REQ_IVI_002, 007, 008)
- ADAS integration sequences (REQ_IVI_028-031)
- Door open hazard detection (ASIL-D)
- Auto-recovery mechanisms

### [diagrams/ota_diagnostic_sequence.md](./diagrams/ota_diagnostic_sequence.md)
- UDS 0x14 Clear DTC sequence (REQ_IVI_012)
- UDS 0x34 OTA download sequence (REQ_IVI_013)
- OTA failure recovery with automatic rollback (REQ_IVI_015)
- Post-OTA function verification (REQ_IVI_014)
- Complete UDS service implementation

### [diagrams/fault_injection_workflow.md](./diagrams/fault_injection_workflow.md)
- CANoe fault injection test architecture
- BDC communication fault sequences (REQ_IVI_011)
- Door sensor fault injection scenarios (REQ_IVI_022)
- Sensor signal fault types (REQ_IVI_024)
- Comprehensive test matrix with 10+ test cases

### [diagrams/can_communication_stack.md](./diagrams/can_communication_stack.md)
- AUTOSAR ComStack architecture (ASW → RTE → COM → PduR → CanIf → CanDrv)
- CAN signal-to-message mapping for all IDs (0x100-0x30F)
- Message transmission and reception sequences
- Performance metrics and reliability analysis (REQ_IVI_009, 010, 025, 059)

## Requirements Coverage

- **Total Requirements**: 84
- **Coverage**: 100%
- **ASIL-D**: 2 requirements
- **ASIL-C**: 5 requirements
- **ASIL-B**: 18 requirements
- **ASIL-A**: 1 requirement
- **QM**: 16 requirements

## Standards Compliance

- **ISO 26262**: ASIL-D safety architecture with redundant monitoring
- **AUTOSAR Classic**: Complete layered architecture (ASW, RTE, BSW)
- **Automotive SPICE**: V-Model development methodology
- **ISO 14229 (UDS)**: Diagnostic services implementation
- **ISO 11898 (CAN)**: Communication stack architecture

## Usage

These documents are ready for:
- Corporate presentations and design reviews
- Implementation phase (AUTOSAR configuration)
- CANoe test environment setup
- Safety case documentation (ISO 26262)
- ASPICE process compliance

---

**Project Status**: ✅ Complete - Ready for implementation phase

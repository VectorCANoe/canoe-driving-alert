# Implementation Plan - IVI vECU Architecture Design

This plan outlines the steps to create a high-quality, professional architecture design for the IVI vECU project, integrating CANoe, UDS OTA, and ISO 26262 safety standards.

## Proposed Changes

### 📐 Documentation Structure (Modular Approach)

Following industry best practices from Hyundai Mobis, Vector, and global Tier-1 suppliers, the architecture documentation will be organized as follows:

#### 1️⃣ Main Architecture Overview (`architecture_overview.md`)
**Purpose**: High-level system architecture showing the big picture
- **System Context Diagram**: IVI ↔ CANoe ↔ vECU interaction
- **AUTOSAR Layered Architecture**: ASW → RTE → BSW → Virtual Hardware
- **Key Components**: Lighting Control, Safety Manager, OTA Manager, Diagnostic Stack
- **Requirements Traceability Matrix**: Mapping REQ_IDs to architecture blocks

#### 2️⃣ Detailed Sub-Diagrams (Separate Files)

Each critical subsystem will have its own detailed diagram file:

##### [NEW] `diagrams/lighting_control_architecture.md`
- Ambient Lighting Controller (Sport Mode, Speed-linked)
- Dashboard Lighting (Reverse Safety, Door-linked UX)
- PlantUML Component Diagram
- **Traces to**: REQ_IVI_001, REQ_IVI_003, REQ_IVI_004

##### [NEW] `diagrams/safety_system_architecture.md`
- Reverse Safety Manager (ASIL-C/D)
- Door Open Warning Logic
- Safety State Machine
- PlantUML State Diagram
- **Traces to**: REQ_IVI_002, REQ_IVI_007, REQ_IVI_008

##### [NEW] `diagrams/ota_diagnostic_sequence.md`
- UDS 0x34 (Request Download) Sequence
- UDS 0x14 (Clear DTC) Sequence
- OTA Failure Recovery Flow
- PlantUML Sequence Diagram
- **Traces to**: REQ_IVI_011, REQ_IVI_012, REQ_IVI_013, REQ_IVI_015

##### [NEW] `diagrams/fault_injection_workflow.md`
- BDC Fault Injection Scenarios
- DTC Generation & Storage
- CANoe Fault Injection Interface
- PlantUML Activity Diagram
- **Traces to**: REQ_IVI_011

##### [NEW] `diagrams/can_communication_stack.md`
- CAN Signal Mapping (Speed, Gear, Door Status)
- ComStack Architecture (CanIf → PduR → Com → DCM)
- Message Flow Timing Analysis
- PlantUML Deployment Diagram
- **Traces to**: REQ_IVI_009, REQ_IVI_010

---

### 🎨 Diagram Quality Standards

All diagrams will follow these professional standards:

1. **Color Coding**:
   - 🔴 **ASIL-B/C/D**: Red borders (Critical Safety Path)
   - 🔵 **Standard AUTOSAR**: Blue (Standard Components)
   - 🟢 **Custom vECU Logic**: Green/Orange (Project-specific)

2. **PlantUML Themes**: Use `!theme` directives for professional appearance
   - `!theme silver` for component diagrams
   - `!theme materia-outline` for sequence diagrams

3. **Requirement Traceability**: Each block annotated with `REQ_IVI_XXX` references

4. **Corporate Naming Conventions**: Follow Hyundai Mobis/Vector standards
   - `vBDC_ECU` instead of "Body Controller"
   - `IVI_HMI` instead of "Display"
   - `ComStack` instead of "Communication Layer"

## Verification Plan

### Automated Verification
- **PlantUML Syntax Check**: Verify all `.puml` code renders without errors
- **Link Integrity**: Ensure all cross-references between documents are valid

### Manual Verification
- **Requirement Coverage**: Verify all 15+ requirements from Excel are traced to architecture blocks
- **ASIL Compliance**: Confirm safety-critical paths (ASIL-C/D) are clearly marked
- **Professional Quality**: Review against actual Hyundai Mobis/Vector documentation samples

# 🖼️ IVI vECU Architecture: Diagram Gallery

This document provides a unified visual overview of all system architecture diagrams.
All diagrams are rendered from the consolidated [PlantUML (.puml) files](./diagrams/puml/).

---

## 00. Architecture Overview
**System Context & Layered Structure**

![Architecture Overview](./diagrams/rendered/00_architecture_overview.png)
*System Context Diagram*

![AUTOSAR Layers](./diagrams/rendered/00_architecture_overview_001.png)
*AUTOSAR Classic Layered Architecture*

---

## 01. Lighting Control Subsystem
**Ambient UX & Signal-Linked Control**

![Component Architecture](./diagrams/rendered/01_lighting_control.png)
*Lighting Component Architecture*

![Speed-Linked State Machine](./diagrams/rendered/01_lighting_control_001.png)
*REQ_IVI_001: Speed-linked Ambient Lighting*

![Door-Linked Sequence](./diagrams/rendered/01_lighting_control_002.png)
*REQ_IVI_003: Door-linked entry/exit lighting*

![Color Sync Flow](./diagrams/rendered/01_lighting_control_003.png)
*REQ_IVI_004: IVI Color Synchronization*

---

## 02. Safety System Architecture
**ASIL-D Critical Paths & ADAS Integration**

![Safety Components](./diagrams/rendered/02_safety_system.png)
*Safety-Critical Architecture*

![Reverse Gear State Machine](./diagrams/rendered/02_safety_system_001.png)
*REQ_IVI_002: Reverse Gear Safety Management*

![ADAS Integration Sequence](./diagrams/rendered/02_safety_system_002.png)
*Integration with ADAS Subsystems*

![Hazard Detection Flow](./diagrams/rendered/02_safety_system_003.png)
*ASIL-D Hazard Detection Logic*

---

## 03. OTA & Diagnostic Sequence
**Software Update & UDS Services**

![Clear DTC](./diagrams/rendered/03_ota_diagnostic.png)
*UDS 0x14: Clear DTC Flow*

![OTA Download](./diagrams/rendered/03_ota_diagnostic_001.png)
*UDS 0x34: OTA Data Download*

![Failure Recovery](./diagrams/rendered/03_ota_diagnostic_002.png)
*OTA Rollback & Recovery Logic*

![Post-Update Verification](./diagrams/rendered/03_ota_diagnostic_003.png)
*Post-Flash Integrity Checks*

---

## 04. Fault Injection Workflow
**CANoe Testing & Error Simulation**

![Test Architecture](./diagrams/rendered/04_fault_injection.png)
*CANoe Fault Injection Setup*

![BDC Fault Sequence](./diagrams/rendered/04_fault_injection_001.png)
*BDC Communication Failure Scenario*

![Door Signal Fault](./diagrams/rendered/04_fault_injection_002.png)
*Door Open Signal Corruption*

![Fault Injection Matrix](./diagrams/rendered/04_fault_injection_003.png)
*Summary of Injection Scenarios*

![CANoe Config](./diagrams/rendered/04_fault_injection_004.png)
*CANoe Panel & Variable Mapping*

---

## 05. CAN Communication Stack
**ComStack & Signal Mapping**

![AUTOSAR ComStack](./diagrams/rendered/05_can_communication.png)
*Layered Communication Architecture*

![Signal Map](./diagrams/rendered/05_can_communication_001.png)
*Signal-to-PDU Mapping*

![Transmission Sequence](./diagrams/rendered/05_can_communication_002.png)
*Message Transmission Flow*

![Reception Sequence](./diagrams/rendered/05_can_communication_003.png)
*Message Reception Flow*

![Performance Metrics](./diagrams/rendered/05_can_communication_004.png)
*Latency & Throughput Analysis*

![Error Handling](./diagrams/rendered/05_can_communication_005.png)
*Bus-Off & CRC Error Recovery*

---

> [!TIP]
> You can view these images directly in VSCode by opening this document and pressing `Cmd+Shift+V` (Mac) to open the Markdown Preview.

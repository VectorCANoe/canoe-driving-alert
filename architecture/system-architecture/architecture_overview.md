# IVI vECU System Architecture Overview

**Project**: CANoe-based Virtual ECU Development for IVI System
**Standards**: ISO 26262 (ASIL-D), AUTOSAR Classic, Automotive SPICE
**Development Environment**: Vector CANoe, V-Model Methodology

---

## 1. System Context

This architecture defines the virtual ECU (vECU) implementation for an In-Vehicle Infotainment (IVI) system, integrating lighting control, safety management, diagnostics, and OTA capabilities within a CANoe simulation environment.

```plantuml
@startuml
!theme silver
skinparam componentStyle rectangle

' System Context Diagram
package "Development & Test Environment" {
    [CANoe Test Environment] as CANoe #LightYellow
    note right of CANoe
        • Network Simulation
        • Fault Injection
        • UDS Diagnostic Tester
        • V-Model Verification
    end note
}

package "IVI Head Unit (Master)" {
    [IVI HMI Application] as IVI_HMI #LightBlue
    [User Interface Layer] as UI
    [Application Logic] as APP

    IVI_HMI --> UI
    UI --> APP
}

package "vECU (Virtual Body Domain Controller)" #LightGreen {
    [vBDC_ECU] as vBDC
    note right of vBDC
        **AUTOSAR Classic**
        • Lighting Control
        • Safety Manager
        • Climate Interface [NEW]
        • ADAS Warning Mgr [NEW]
        • OTA Manager
        • Diagnostic Stack
    end note
}

package "Climate System" #LightYellow {
    [HVAC_ECU] as HVAC
}

package "ADAS Sensors" #LightYellow {
    [Rear_Camera_ECU] as RCAM
}

' CAN Network
cloud "CAN Bus Network" as CAN {
    interface "CAN 500kbps" as CAN_IF
}

' Connections
CANoe --> CAN : Test Signals\nFault Injection
IVI_HMI --> CAN : User Commands
vBDC --> CAN : Actuator Control
HVAC --> CAN : Cabin Temp,\nStatus
RCAM --> CAN : Rear Objects
CAN --> CAN_IF

' Annotations
note bottom of CAN
    **Key CAN Signals**:
    • Vehicle Speed (0x100), Gear (0x384)
    • Lighting Commands (0x410)
    • Environment (0x520), HVAC (0x260)
    • Rear ADAS (0x786)
end note

caption System Context - IVI vECU Development Environment
@enduml
```

---

## 2. AUTOSAR Layered Architecture

The vBDC_ECU follows AUTOSAR Classic architecture with clear separation between application software (ASW), runtime environment (RTE), and basic software (BSW).

```plantuml
@startuml
!theme silver
skinparam componentStyle uml2

package "vBDC_ECU - AUTOSAR Architecture" {

    ' Application Layer
    package "Application Software (ASW)" #LightBlue {
        component "Ambient_Light_Controller" as ALC #LightBlue
        component "Safety_Alert_Manager" as SAM #Red
        component "OTA_Update_Agent" as OTA #LightGreen

        note right of ALC
            **REQ_IVI_001**
            Sport Mode Speed-linked
            Response: <500ms
            ASIL-B
        end note

        note right of SAM
            **REQ_IVI_002, 007**
            Reverse Safety Warning
            Response: <300ms
            ASIL-C/D
        end note

        note right of OTA
            **REQ_IVI_013, 015**
            UDS 0x34 Download
            Auto Recovery
            ASIL-B
        end note
    }

    ' RTE Layer
    package "Runtime Environment (RTE)" #line.dashed {
        interface "CAN_Signal_Port" as CSP
        interface "Diag_Service_Port" as DSP
        interface "Safety_Port" as SP

        ALC --> CSP
        SAM --> CSP
        SAM --> SP
        OTA --> DSP
    }

    ' BSW Layer
    package "Basic Software (BSW)" #LightGray {

        package "Communication Stack" {
            component "COM" as COM
            component "PduR" as PDUR
            component "CanIf" as CANIF
            component "CanDrv" as CANDRV

            COM --> PDUR
            PDUR --> CANIF
            CANIF --> CANDRV
        }

        package "Diagnostic Stack" {
            component "DCM\n(UDS Services)" as DCM #Orange
            component "DEM\n(DTC Manager)" as DEM #Orange
            component "FIM\n(Fault Inhibition)" as FIM #Orange

            DCM --> DEM
            DEM --> FIM
        }

        package "Memory & System" {
            component "NvM\n(Non-volatile Memory)" as NVM
            component "EcuM\n(ECU Manager)" as ECUM
        }

        CSP --> COM
        DSP --> DCM
        SP --> FIM
        DCM --> NVM
        DEM --> NVM
    }

    ' Virtual Hardware Layer
    package "Virtual Hardware Abstraction" #LightYellow {
        component "CANoe Virtual CAN Bus" as VCAN
        component "Fault Injection Interface" as FI
        component "Virtual Flash Memory" as VFLASH

        CANDRV --> VCAN
        FI ..> CANIF : Inject Errors
        NVM --> VFLASH
    }
}

caption AUTOSAR Layered Architecture for vBDC_ECU (ISO 26262 Compliant)
@enduml
```

---

## 3. Key System Components

### 3.1 Lighting Control Subsystem
- **Ambient Lighting Controller**: Sport mode and speed-linked color control
- **Dashboard Lighting**: Reverse safety and door-linked UX
- **Performance**: Color transition <500ms, synchronization >99%
- **Safety Level**: ASIL-B
- 📄 **Details**: See [Lighting Control Architecture](diagrams/lighting_control_architecture.md)

### 3.2 Safety Management Subsystem
- **Reverse Safety Manager**: ASIL-C/D critical path
- **Door Open Warning Logic**: Hazard detection during reverse
- **Auto Recovery**: Automatic state restoration
- **Performance**: Detection >99%, response <300ms
- 📄 **Details**: See [Safety System Architecture](diagrams/safety_system_architecture.md)

### 3.3 OTA & Diagnostic Subsystem
- **UDS Services**: 0x14 (Clear DTC), 0x34 (Request Download), 0x31 (Routine Control)
- **OTA Manager**: Software update with automatic rollback
- **DTC Management**: Fault detection and storage
- **Performance**: Success rate >98%, recovery 100%
- 📄 **Details**: See [OTA/Diagnostic Sequence](diagrams/ota_diagnostic_sequence.md)

### 3.4 Fault Injection & Testing
- **BDC Fault Injection**: Communication errors, sensor failures
- **DTC Generation**: Automatic fault code creation
- **CANoe Integration**: Bit/frame error injection
- 📄 **Details**: See [Fault Injection Workflow](diagrams/fault_injection_workflow.md)

### 3.5 CAN Communication Stack
- **Signal Mapping**: Speed, Gear, Door status
- **ComStack**: CanIf → PduR → Com → DCM
- **Timing Analysis**: Message latency <100ms
- 📄 **Details**: See [CAN Communication Stack](diagrams/can_communication_stack.md)

---

## 4. Requirements Traceability Matrix

| Requirement ID | Category | ASIL | Component | Diagram Reference |
|---|---|---|---|---|
| REQ_IVI_001 | Functional | ASIL-B | Ambient_Light_Controller | [Lighting Control](diagrams/lighting_control_architecture.md) |
| REQ_IVI_005 | Functional | QM | Ambient_Light_Controller | [Lighting Control](diagrams/lighting_control_architecture.md) |
| REQ_IVI_002 | Safety | ASIL-C | Safety_Alert_Manager | [Safety System](diagrams/safety_system_architecture.md) |
| REQ_IVI_029 | Safety | ASIL-B | Safety_Alert_Manager | [Safety System](diagrams/safety_system_architecture.md) |
| REQ_IVI_003 | Functional | ASIL-A | Dashboard_Lighting | [Lighting Control](diagrams/lighting_control_architecture.md) |
| REQ_IVI_051 | Functional | QM | IVI_HMI | [UI Architecture](diagrams/docs/lighting_control_architecture.md) |
| REQ_IVI_053 | Functional | QM | IVI_HMI | [UI Architecture](diagrams/docs/lighting_control_architecture.md) |
| REQ_IVI_054 | Functional | QM | IVI_HMI | [UI Architecture](diagrams/docs/lighting_control_architecture.md) |
| REQ_IVI_004 | Functional | QM | IVI_Sync_Manager | [Lighting Control](diagrams/lighting_control_architecture.md) |
| REQ_IVI_007 | Safety | ASIL-D | Door_Warning_Logic | [Safety System](diagrams/safety_system_architecture.md) |
| REQ_IVI_008 | Safety | ASIL-C | Auto_Recovery_Manager | [Safety System](diagrams/safety_system_architecture.md) |
| REQ_IVI_009 | Non-Functional | QM | ComStack | [CAN Stack](diagrams/can_communication_stack.md) |
| REQ_IVI_011 | Diagnostic | ASIL-B | DEM/FIM | [Fault Injection](diagrams/fault_injection_workflow.md) |
| REQ_IVI_012 | Diagnostic | ASIL-B | DCM (UDS 0x14) | [OTA/Diagnostic](diagrams/ota_diagnostic_sequence.md) |
| REQ_IVI_013 | Diagnostic | ASIL-B | OTA_Update_Agent | [OTA/Diagnostic](diagrams/ota_diagnostic_sequence.md) |
| REQ_IVI_015 | Diagnostic | ASIL-C | OTA_Recovery | [OTA/Diagnostic](diagrams/ota_diagnostic_sequence.md) |

---

## 5. Development Methodology

### V-Model Integration

```mermaid
graph LR
    A[Requirements Analysis] --> B[System Architecture]
    B --> C[Component Design]
    C --> D[Implementation]
    D --> E[Unit Testing]
    E --> F[Integration Testing]
    F --> G[System Testing]
    G --> H[Validation]

    A -.Traces to.-> H
    B -.Traces to.-> G
    C -.Traces to.-> F
    D -.Traces to.-> E

    style A fill:#e1f5ff
    style H fill:#e1f5ff
    style B fill:#fff4e1
    style G fill:#fff4e1
    style C fill:#ffe1f5
    style F fill:#ffe1f5
    style D fill:#e1ffe1
    style E fill:#e1ffe1
```

### Verification Strategy

1. **SIL (Software-in-the-Loop)**: CANoe model-based testing
2. **HIL (Hardware-in-the-Loop)**: Safety-critical path validation (ASIL-C/D)
3. **Fault Injection Testing**: BDC communication error scenarios
4. **Integration Testing**: Full system verification with IVI HMI

---

## 6. Safety Considerations

### ASIL Decomposition

- **ASIL-D**: Door open warning during reverse (REQ_IVI_007)
- **ASIL-C**: Reverse safety alert, OTA recovery (REQ_IVI_002, 015)
- **ASIL-B**: Lighting control, diagnostic services (REQ_IVI_001, 011-013)
- **ASIL-A/QM**: Non-critical UX features (REQ_IVI_003, 004)

### Safety Mechanisms

- **Redundant Monitoring**: External watchdog for safety-critical functions
- **Graceful Degradation**: Fallback to audio warning if lighting fails
- **Automatic Recovery**: State restoration after fault conditions clear
- **DTC Logging**: All safety violations recorded for post-analysis

---

## 7. Next Steps

For detailed design of each subsystem, please refer to:

1. 🎨 [Lighting Control Architecture](diagrams/lighting_control_architecture.md)
2. 🛡️ [Safety System Architecture](diagrams/safety_system_architecture.md)
3. 🔄 [OTA/Diagnostic Sequence](diagrams/ota_diagnostic_sequence.md)
4. ⚠️ [Fault Injection Workflow](diagrams/fault_injection_workflow.md)
5. 📡 [CAN Communication Stack](diagrams/can_communication_stack.md)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-08
**Author**: Architecture Team
**Review Status**: ✅ Approved for Implementation

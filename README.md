# CANoe-IVI-OTA

**CAN Communication Project in Hyundai Mobis Bootcamp with Vector Korea**

## 🚗 Project Overview

This project focuses on **vECU simulation-based vehicle convenience features and UX-oriented control logic design** using **Vector CANoe**. The project encompasses comprehensive automotive software development including IVI (In-Vehicle Infotainment) system integration, HVAC/window/seat control simulation, UX lighting with ADAS event coordination, and virtual diagnostics with OTA (Over-The-Air) reprogramming capabilities.

### Organization
- **Organization Name**: VectorCANoe
- **Repository**: CANoe-IVI-OTA
- **Partner**: Vector Korea Co., Ltd.
- **Program**: Hyundai Mobis Bootcamp

---

## 🎯 Project Objectives

### Phase 1: IVI-Based Control System Simulation
1. **HVAC/Window/Seat CAPL Simulation**
   - Implement CAPL-based control logic for HVAC systems
   - Develop window control algorithms
   - Create seat adjustment simulation models

2. **UX Lighting & ADAS Event Integration**
   - Design UX lighting control logic
   - Integrate ADAS (Advanced Driver Assistance Systems) event triggers
   - Coordinate lighting responses with vehicle events

3. **Reverse Parking & Lighting Control Algorithm**
   - Implement reverse parking detection logic
   - Develop automated lighting control for parking scenarios
   - Create safety-oriented illumination patterns

### Phase 2: Virtual Diagnostics & Reprogramming
1. **Fault Injection & UDS-based Diagnostics**
   - Inject faults into BDC (Body Domain Controller) logic
   - Verify proper DTC (Diagnostic Trouble Code) generation using UDS protocol
   - Validate diagnostic communication flows

2. **Virtual OTA Process via vVIRTUALtarget**
   - Implement virtual software update procedures
   - Test OTA reprogramming workflows
   - Validate firmware update mechanisms in simulation environment

---

## 🚀 V-Model Sample Artifacts (New!)

A complete **V-Model reference implementation** has been added to `docs/sample/`. This serves as a gold standard for project documentation and CANoe implementation.

- **Documentation**: 13 files covering the full V-Model lifecycle (Requirements → Architecture → Implementation → Test).
- **CANoe Project**: Fully functional simulation in `docs/sample/canoe/` including:
  - **5 Simulated ECUs**: BCM, Gateway, Cluster, Tester, OTA Server (CAPL implemented).
  - **E2E Scenario**: Fault Injection → Diagnostics (UDS) → DoIP/OTA Update.
  - **Automated Testing**: `Master_Scenario.can` for one-click verification.

👉 **[See Sample Project Guide](docs/sample/canoe/README.md)**

---

## 🛠️ Core Technologies & Skills

### Primary Skills
1. **IVI (In-Vehicle Infotainment) Systems**
   - Infotainment system architecture
   - User interface integration
   - Multi-domain communication

2. **Vector CANoe**
   - CAPL scripting
   - Network simulation
   - vECU configuration
   - vVIRTUALtarget integration

3. **CAN Communication**
   - CAN protocol implementation
   - Message database (DBC) management
   - Network diagnostics
   - UDS (Unified Diagnostic Services)

### Technical Stack
- **Simulation Platform**: Vector CANoe
- **Programming**: CAPL (CAN Access Programming Language)
- **Protocols**: CAN, UDS, OTA
- **Diagnostics**: DTC management, Fault injection
- **Virtual ECU**: vVIRTUALtarget

---

## 📁 Project Structure

```
CANoe-IVI-OTA/
├── README.md
├── docs/
│   ├── meeting-notes/          # Project meeting records
│   ├── specifications/         # Technical specifications
│   └── diagrams/              # Architecture and flow diagrams
├── src/
│   ├── IVI/                   # IVI system implementations
│   │   ├── HVAC/             # HVAC control logic
│   │   ├── Window/           # Window control algorithms
│   │   └── Seat/             # Seat adjustment logic
│   ├── UX-Lighting/          # UX lighting control
│   │   ├── ADAS-Integration/ # ADAS event coordination
│   │   └── Parking/          # Parking lighting control
│   └── Diagnostics/          # Diagnostic and OTA modules
│       ├── BDC/              # Body Domain Controller logic
│       ├── UDS/              # UDS protocol implementation
│       └── OTA/              # OTA reprogramming logic
├── simulation/
│   ├── configurations/        # CANoe configuration files
│   ├── databases/            # CAN database files (DBC)
│   └── test-cases/           # Simulation test scenarios
└── tests/
    ├── unit/                 # Unit tests
    └── integration/          # Integration tests
```

---

## 🚀 Getting Started

### Prerequisites
- Vector CANoe (with vVIRTUALtarget support)
- Basic understanding of CAN protocol
- Familiarity with automotive ECU systems
- CAPL programming knowledge

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/VectorCANoe/CANoe-IVI-OTA.git
   cd CANoe-IVI-OTA
   ```

2. Open CANoe and load the project configuration files from `simulation/configurations/`

3. Import CAN database files from `simulation/databases/`

### Running Simulations
1. Open the desired simulation configuration in CANoe
2. Load the appropriate CAPL scripts from `src/`
3. Start the simulation and monitor the trace window
4. Verify control logic behavior and communication flows

---

## 📊 Key Features

### ✅ Implemented Features
- IVI-based HVAC control simulation
- Window and seat control algorithms
- UX lighting with ADAS event coordination
- Reverse parking detection and lighting control
- BDC fault injection mechanisms
- UDS-based DTC generation and verification
- Virtual OTA software update process

### 🔄 Development Workflow
1. **Design**: Define control logic and communication requirements
2. **Implementation**: Develop CAPL scripts and vECU configurations
3. **Simulation**: Test in CANoe environment
4. **Validation**: Verify functionality and diagnose issues
5. **Documentation**: Record results and update specifications

---

## 🧪 Testing & Validation

### Simulation Testing
- CAPL-based unit tests for individual control modules
- Integration tests for multi-ECU communication
- Fault injection scenarios for diagnostic validation

### Diagnostic Verification
- DTC generation validation using UDS protocol
- Fault recovery mechanism testing
- OTA update process verification in vVIRTUALtarget

---

## 📝 Documentation

All project documentation is maintained in the `docs/` directory:
- **Meeting Notes**: Regular project meeting records
- **Specifications**: Technical requirements and design documents
- **Diagrams**: System architecture and communication flow diagrams

---

## 👥 Contributors

This project is developed as part of the Hyundai Mobis Bootcamp in collaboration with Vector Korea Co., Ltd.

---

## 📄 License

This project is part of the Hyundai Mobis Bootcamp educational program.

---

## 🔗 Resources

- [Vector CANoe Documentation](https://www.vector.com/int/en/products/products-a-z/software/canoe/)
- [CAN Protocol Specification](https://www.can-cia.org/)
- [UDS Protocol (ISO 14229)](https://www.iso.org/standard/72439.html)
- [Hyundai Mobis](https://www.mobis.co.kr/)
- [Vector Korea](https://www.vector.com/kr/ko/)

---

**Last Updated**: February 2026

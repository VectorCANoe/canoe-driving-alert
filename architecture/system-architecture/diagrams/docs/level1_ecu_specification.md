# Level 1: Vehicle System ECU Specification

## 📋 Overview

**Document Purpose**: Detailed specification of all ECUs in the vehicle system architecture
**Total ECU Count**: 11
**Architecture Type**: Domain-Based with Central Gateway
**Date**: 2026-02-11

---

## 🚗 ECU Inventory by Domain

### 1. Powertrain Domain (2 ECUs)

#### 1.1 Engine Control Unit (EMS)
- **Full Name**: Engine Management System
- **Manufacturer Example**: Bosch, Continental, Denso
- **CAN ID Range**: 0x100-0x17F
- **Network**: CAN High-Speed 1 (500 kbps)
- **ASIL Level**: ASIL-D
- **Cycle Time**: 10ms (critical signals)

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| Engine_RPM | 0x100 | 16 bit | rpm | 0-8000 | 10ms |
| Vehicle_Speed | 0x101 | 16 bit | km/h | 0-300 | 10ms |
| Engine_Torque | 0x102 | 16 bit | Nm | -500 to 1000 | 20ms |
| Coolant_Temp | 0x103 | 8 bit | °C | -40 to 150 | 100ms |
| Throttle_Position | 0x104 | 8 bit | % | 0-100 | 20ms |

**Functions**:
- Fuel injection control
- Ignition timing
- Emission control
- Engine diagnostics

---

#### 1.2 Transmission Control Unit (TCU)
- **Full Name**: Transmission Control Unit
- **CAN ID Range**: 0x180-0x1FF
- **Network**: CAN High-Speed 1 (500 kbps)
- **ASIL Level**: ASIL-C
- **Cycle Time**: 20ms

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| Gear_Position | 0x180 | 4 bit | enum | P/R/N/D/S | 20ms |
| Shift_Status | 0x181 | 2 bit | enum | 0-3 | 20ms |
| Oil_Temperature | 0x182 | 8 bit | °C | -40 to 150 | 100ms |
| Torque_Converter_Lock | 0x183 | 1 bit | bool | 0/1 | 50ms |

**Functions**:
- Gear shift control
- Torque converter management
- Transmission diagnostics

---

### 2. Chassis Domain (2 ECUs)

#### 2.1 ESP ECU (Electronic Stability Program)
- **Full Name**: Electronic Stability Program
- **Manufacturer Example**: Bosch ESP 9.3, Continental MK100
- **CAN ID Range**: 0x200-0x27F
- **Network**: CAN High-Speed 1 (500 kbps)
- **ASIL Level**: ASIL-D
- **Cycle Time**: 10ms (critical signals)

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| Wheel_Speed_FL | 0x200 | 16 bit | km/h | 0-300 | 10ms |
| Wheel_Speed_FR | 0x201 | 16 bit | km/h | 0-300 | 10ms |
| Wheel_Speed_RL | 0x202 | 16 bit | km/h | 0-300 | 10ms |
| Wheel_Speed_RR | 0x203 | 16 bit | km/h | 0-300 | 10ms |
| Yaw_Rate | 0x210 | 16 bit | deg/s | -100 to 100 | 10ms |
| Lateral_Accel | 0x211 | 16 bit | m/s² | -15 to 15 | 10ms |
| Brake_Pressure | 0x212 | 16 bit | bar | 0-200 | 10ms |
| ESP_Active | 0x213 | 1 bit | bool | 0/1 | 10ms |

**Functions**:
- Anti-lock braking (ABS)
- Traction control (TCS)
- Electronic stability control
- Hill start assist

---

#### 2.2 MDPS ECU (Motor Driven Power Steering)
- **Full Name**: Motor Driven Power Steering
- **CAN ID Range**: 0x280-0x2FF
- **Network**: CAN High-Speed 1 (500 kbps)
- **ASIL Level**: ASIL-C
- **Cycle Time**: 20ms

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| Steering_Angle | 0x280 | 16 bit | deg | -720 to 720 | 20ms |
| Steering_Torque | 0x281 | 16 bit | Nm | -10 to 10 | 20ms |
| Steering_Rate | 0x282 | 16 bit | deg/s | -500 to 500 | 20ms |
| MDPS_Status | 0x283 | 8 bit | enum | 0-7 | 50ms |

**Functions**:
- Electric power steering assist
- Lane keeping assist (LKA) actuation
- Parking assist actuation

---

### 3. Body Domain (1 ECU)

#### 3.1 Body Control Module (BCM)
- **Full Name**: Body Control Module
- **CAN ID Range**: 0x500-0x57F
- **Network**: CAN Low-Speed (125 kbps)
- **ASIL Level**: ASIL-B (door safety), QM (comfort)
- **Cycle Time**: 100ms

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| Door_Status_FL | 0x500 | 2 bit | enum | 0-3 | 100ms |
| Door_Status_FR | 0x501 | 2 bit | enum | 0-3 | 100ms |
| Door_Status_RL | 0x502 | 2 bit | enum | 0-3 | 100ms |
| Door_Status_RR | 0x503 | 2 bit | enum | 0-3 | 100ms |
| Window_Position_FL | 0x520 | 8 bit | % | 0-100 | 200ms |
| Central_Lock_Status | 0x521 | 1 bit | bool | 0/1 | 100ms |

**Key Signals (Rx)**:
| Signal Name | CAN ID | Source | Function |
|------------|--------|--------|----------|
| Ambient_Light_RGB | 0x410 | IVI | Ambient lighting control |
| Light_Command | 0x411 | IVI | Exterior light control |

**Functions**:
- Exterior lighting control (headlamps, tail lamps)
- Interior lighting (ambient, dome)
- Door lock/unlock
- Window control
- Wiper control

---

### 4. Infotainment & ADAS Domain (5 ECUs)

#### 4.1 IVI Head Unit ⭐ (Project Focus)
- **Full Name**: In-Vehicle Infotainment
- **CAN ID Range**: 0x400-0x47F
- **Network**: CAN High-Speed 2 (500 kbps)
- **ASIL Level**: QM (display), ASIL-B (ADAS warning path)
- **Cycle Time**: 100ms

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| Ambient_Light_RGB | 0x410 | 24 bit | RGB | 0-255 each | 100ms |
| Theme_Package | 0x411 | 8 bit | enum | 0-10 | 500ms |
| Profile_Data | 0x412 | 64 bit | struct | - | 1000ms |
| Scenario_Params | 0x413 | 32 bit | struct | - | 500ms |

**Key Signals (Rx)**:
| Signal Name | CAN ID | Source | Purpose |
|------------|--------|--------|---------|
| Vehicle_Speed | 0x101 | EMS | Speed display, lighting |
| Gear_Position | 0x180 | TCU | Reverse warning |
| LDW_Status | 0x300 | Camera | ADAS warning display |
| AEB_Event | 0x302 | Camera | Emergency warning |
| BSD_Object_Left | 0x340 | Radar | Blind spot warning |

**Functions**:
- Multimedia & navigation
- Ambient lighting control
- ADAS warning display
- Theme/profile management
- User scenario editing

**Requirements Coverage**:
- REQ_IVI_001-005: Lighting control
- REQ_IVI_028-038: ADAS integration
- REQ_IVI_042-050: UI features

---

#### 4.2 Instrument Cluster
- **CAN ID Range**: 0x480-0x4FF
- **Network**: CAN High-Speed 2 (500 kbps)
- **ASIL Level**: ASIL-B
- **Cycle Time**: 50ms

**Key Signals (Rx)**:
| Signal Name | CAN ID | Source | Display |
|------------|--------|--------|---------|
| Engine_RPM | 0x100 | EMS | Tachometer |
| Vehicle_Speed | 0x101 | EMS | Speedometer |
| Gear_Position | 0x180 | TCU | Gear indicator |
| LDW_Status | 0x300 | Camera | Warning light |
| AEB_Event | 0x302 | Camera | Warning light |

**Functions**:
- Speedometer, tachometer
- Warning lights
- ADAS status display
- Fuel gauge, temperature gauge

---

#### 4.3 Front Camera ECU
- **Full Name**: Forward-Facing Camera (ADAS)
- **CAN ID Range**: 0x300-0x33F
- **Network**: CAN High-Speed 2 (500 kbps)
- **ASIL Level**: ASIL-D (AEB), ASIL-C (LDW)
- **Cycle Time**: 10ms (critical events), 50ms (status)

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| LDW_Status | 0x300 | 2 bit | enum | 0-3 | 50ms |
| Lane_Position | 0x301 | 16 bit | cm | -200 to 200 | 50ms |
| AEB_Event | 0x302 | 2 bit | enum | 0-3 | 10ms |
| Collision_Risk | 0x303 | 8 bit | % | 0-100 | 20ms |
| Object_Detection | 0x310 | 32 bit | struct | - | 50ms |

**Functions**:
- Lane Departure Warning (LDW)
- Automatic Emergency Braking (AEB)
- Forward Collision Warning (FCW)
- Traffic sign recognition

**Requirements**:
- REQ_IVI_028: LDW response <80ms
- REQ_IVI_030: AEB response <50ms

---

#### 4.4 Radar ECU (Blind Spot Detection)
- **CAN ID Range**: 0x340-0x37F
- **Network**: CAN High-Speed 2 (500 kbps)
- **ASIL Level**: ASIL-B
- **Cycle Time**: 50ms

**Key Signals (Tx)**:
| Signal Name | CAN ID | Length | Unit | Range | Cycle |
|------------|--------|--------|------|-------|-------|
| BSD_Object_Left | 0x340 | 1 bit | bool | 0/1 | 50ms |
| BSD_Object_Right | 0x341 | 1 bit | bool | 0/1 | 50ms |
| Object_Distance | 0x342 | 8 bit | m | 0-50 | 50ms |
| Object_Velocity | 0x343 | 16 bit | km/h | -100 to 100 | 50ms |

**Functions**:
- Blind Spot Detection (BSD)
- Rear Cross Traffic Alert (RCTA)

**Requirements**:
- REQ_IVI_031: BSD response <70ms

---

#### 4.5 Smart Cruise Control (SCC)
- **CAN ID Range**: 0x380-0x3BF
- **Network**: CAN High-Speed 2 (500 kbps)
- **ASIL Level**: ASIL-C
- **Cycle Time**: 50ms

**Key Signals (Tx/Rx)**:
| Signal Name | CAN ID | Direction | Purpose |
|------------|--------|-----------|---------|
| SCC_Active | 0x380 | Tx | Cruise status |
| Set_Speed | 0x381 | Tx | Target speed |
| Following_Distance | 0x382 | Tx | Distance to lead vehicle |

**Functions**:
- Adaptive Cruise Control (ACC)
- Speed limit assist

---

### 5. Gateway (1 ECU)

#### 5.1 Central Gateway ECU
- **CAN ID Range**: 0x700-0x7FF (diagnostic)
- **Networks**:
  - CAN-HS1 (500 kbps)
  - CAN-HS2 (500 kbps)
  - CAN-LS (125 kbps)
  - Ethernet (100 Mbps)
  - Telematics (4G/5G)
- **ASIL Level**: ASIL-D (safety routing), QM (general routing)
- **Cycle Time**: Variable

**Functions**:
- CAN-CAN routing
- CAN-Ethernet gateway
- Firewall & intrusion detection
- Diagnostic routing (UDS)
- OTA update coordination

**Routing Table**:
| Source Network | Destination Network | Filtered Messages |
|---------------|---------------------|-------------------|
| CAN-HS1 | CAN-HS2 | 0x100-0x1FF (Powertrain) |
| CAN-HS2 | CAN-HS1 | 0x300-0x3FF (ADAS) |
| CAN-HS2 | CAN-LS | 0x410-0x413 (IVI commands) |
| Ethernet | All CAN | Diagnostic (0x7DF-0x7FF) |

---

## 🌐 Network Architecture

### CAN Network Segmentation

#### CAN High-Speed 1 (500 kbps)
**Purpose**: Powertrain & Chassis (safety-critical, high-frequency)
**ECUs**: EMS, TCU, ESP, MDPS
**Message Load**: ~40% utilization
**Termination**: 120Ω at both ends

#### CAN High-Speed 2 (500 kbps)
**Purpose**: ADAS & Infotainment (sensor data, user interface)
**ECUs**: IVI, Cluster, Camera, Radar, SCC
**Message Load**: ~35% utilization
**Termination**: 120Ω at both ends

#### CAN Low-Speed (125 kbps)
**Purpose**: Body & Comfort (non-critical, low-frequency)
**ECUs**: BCM
**Message Load**: ~15% utilization
**Termination**: Built-in

---

## 📊 Communication Matrix Summary

### IVI Communication Dependencies

**IVI Receives From**:
| Source ECU | CAN ID Range | Purpose | Cycle |
|-----------|-------------|---------|-------|
| EMS | 0x100-0x104 | Speed, RPM display | 10-100ms |
| TCU | 0x180-0x183 | Gear position, reverse warning | 20-100ms |
| Camera | 0x300-0x310 | ADAS warnings (LDW, AEB) | 10-50ms |
| Radar | 0x340-0x343 | BSD warnings | 50ms |

**IVI Sends To**:
| Destination ECU | CAN ID Range | Purpose | Cycle |
|----------------|-------------|---------|-------|
| BCM | 0x410-0x413 | Ambient lighting, theme | 100-500ms |

---

## 🔧 Design Rationale

### Why 11 ECUs?
1. **Domain Separation**: Fault isolation between critical systems
2. **Supplier Diversity**: Different Tier-1 suppliers per domain
3. **Scalability**: Easy to add new functions within domains
4. **Safety**: ASIL-D functions isolated from QM functions

### Why Dual CAN-HS?
1. **Bandwidth**: Prevent bus overload (500 kbps each)
2. **Redundancy**: Critical signals on separate buses
3. **Latency**: Reduce message collisions
4. **Security**: Gateway filters cross-domain traffic

### Why Central Gateway?
1. **Security**: Single point for firewall & intrusion detection
2. **Diagnostics**: Unified diagnostic access
3. **OTA**: Centralized update management
4. **Cost**: Reduce wiring complexity

---

## 📝 References

**Industry Standards**:
- ISO 11898 (CAN Protocol)
- ISO 26262 (Functional Safety)
- ISO 14229 (UDS Diagnostics)
- AUTOSAR Classic Platform R20-11
- AUTOSAR Adaptive Platform R21-11

**Real Vehicle Examples**:
- Tesla Model 3 (commaai/opendbc: tesla_can.dbc)
- Hyundai/Kia (commaai/opendbc: hyundai_kia_generic.dbc)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-11
**Next Review**: After Level 2 architecture completion

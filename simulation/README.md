# CANoe Simulation Environment

**Project**: IVI-OTA Ambient Lighting & UDS Diagnostics
**Created**: 2026-02-12
**CANoe Version**: 19.4 (SP19)

---

## 📁 Directory Structure

```
simulation/
├── configurations/          # CANoe configuration files
│   └── IVI_OTA_Project.cfg # Main project configuration ⭐
├── databases/              # CAN database files
│   └── vehicle_system.dbc  # Complete vehicle CAN database (20 messages)
├── nodes/                  # CAPL node implementations
│   ├── IVI.can            # (To be created) IVI ambient lighting control
│   ├── BCM.can            # (To be created) Body control & lighting
│   ├── CGW.can            # (To be created) Gateway routing
│   ├── EMS.can            # (To be created) Engine management
│   ├── ESP.can            # (To be created) Vehicle dynamics
│   └── ...                # Other ECU nodes
├── capl/                   # Shared CAPL libraries
├── panels/                 # Control panels (GUI)
├── tests/                  # Test sequences
└── logs/                   # Measurement logs (BLF files)
```

---

## 🚀 Quick Start

### 1. Open Configuration in CANoe
```
1. Launch CANoe 19.4 (SP19)
2. File → Open Configuration
3. Select: simulation/configurations/IVI_OTA_Project.cfg
4. CANoe will load all networks, nodes, and database
```

### 2. Network Setup

| Network | Baudrate | Channel | Description |
|---------|----------|---------|-------------|
| **CAN1** (CAN-HS #1) | 500 kbps | 1 | Powertrain, Chassis, Safety (ASIL-D) |
| **CAN2** (CAN-HS #2) | 500 kbps | 2 | ADAS, Infotainment (IVI, Cluster) |
| **CAN3** (CAN-LS) | 125 kbps | 3 | Body Control (BCM, HVAC) |

### 3. ECU Nodes (13 Total)

#### 🎯 **Project Main Nodes** (Priority)
1. **IVI** (CAN2) - Ambient lighting control, user profiles ⭐
2. **BCM** (CAN3) - Lighting feedback, door/seat sensors ⭐
3. **CGW** (CAN1/2/3) - Network routing, diagnostics, OTA ⭐

#### 🚗 **Vehicle Domain Nodes**
4. **EMS** (CAN1) - Engine management, vehicle speed
5. **TCU** (CAN1) - Transmission control
6. **ESP** (CAN1) - Vehicle dynamics, wheel speeds
7. **MDPS** (CAN1) - Steering control

#### 📷 **ADAS Nodes**
8. **Camera** (CAN2) - LDW, AEB, object detection
9. **Rear_Camera** (CAN2) - Rear parking assistance
10. **Radar** (CAN2) - Blind spot detection
11. **SCC** (CAN2) - Smart cruise control

#### 🌡️ **Comfort Nodes**
12. **Cluster** (CAN2) - Instrument display
13. **HVAC** (CAN3) - Climate control

---

## 📊 CAN Messages (20 Total)

### Project-Specific Messages ⭐

| ID | Name | Sender | Network | Description |
|----|------|--------|---------|-------------|
| **0x400** | IVI_AmbientLight | IVI | CAN2 | RGB lighting control (11 themes) |
| **0x410** | IVI_Profile | IVI | CAN2 | User profile management (6 profiles) |
| **0x510** | BCM_LightControl | BCM | CAN3 | Lighting feedback (RGB actual values) |
| **0x520** | BCM_SensorStatus | BCM | CAN3 | Ambient light, rain, wiper sensors |
| **0x522** | BCM_SeatStatus | BCM | CAN3 | Seat occupancy & belt status |

### Vehicle System Messages

| ID | Name | Sender | Network | ASIL | Cycle |
|----|------|--------|---------|------|-------|
| 0x100 | EMS_EngineStatus | EMS | CAN1 | D | 10ms |
| 0x101 | EMS_Temperature | EMS | CAN1 | D | 100ms |
| 0x104 | HVAC_Status | HVAC | CAN3 | QM | 200ms |
| 0x180 | TCU_GearStatus | TCU | CAN1 | C | 20ms |
| 0x200 | ESP_VehicleDynamics | ESP | CAN1 | D | 10ms |
| 0x210 | ESP_Sensors | ESP | CAN1 | D | 10ms |
| 0x280 | MDPS_SteeringStatus | MDPS | CAN1 | C | 20ms |
| 0x300 | Camera_LDW | Camera | CAN2 | D | 50ms |
| 0x310 | Camera_Objects | Camera | CAN2 | C | 50ms |
| 0x312 | Rear_Camera_Objects | Rear_Camera | CAN2 | B | 50ms |
| 0x340 | Radar_BSD | Radar | CAN2 | B | 50ms |
| 0x380 | SCC_Status | SCC | CAN2 | C | 50ms |
| 0x480 | Cluster_Display | Cluster | CAN2 | B | 50ms |
| 0x500 | BCM_DoorStatus | BCM | CAN3 | B | 100ms |
| 0x700 | CGW_Status | CGW | CAN1 | D | 1000ms |

---

## 🎨 IVI Ambient Lighting Feature

### Theme Packages (11 Total)
0. **SPORT** - Dynamic red/orange
1. **COMFORT** - Soft blue/white
2. **ECO** - Green/teal
3. **CUSTOM1-3** - User-defined RGB
4. **NIGHT** - Low brightness mode
5. **PARTY** - Multi-color cycling
6. **RELAX** - Warm tones
7. **DYNAMIC** - Speed-linked intensity
8. **USER_DEFINED** - Full RGB control

### Control Flow
```
IVI (CAN2)
  ↓ IVI_AmbientLight (0x400): RGB, Brightness, Theme
Gateway (Routing)
  ↓
BCM (CAN3)
  ↓ Process & Control LED Drivers
  ↓ BCM_LightControl (0x510): RGB_Actual, Status
Gateway (Routing)
  ↓
IVI, Cluster (CAN2)
  ↓ Display actual values & status
```

---

## 🧪 Environment Variables

### IVI Control
- `IVI_Theme_Selected` (0-10): Current theme
- `IVI_Brightness` (0-100): Brightness %
- `IVI_RGB_R/G/B` (0-255): RGB values

### Vehicle State
- `Vehicle_Speed`: km/h
- `Engine_RPM`: rpm
- `Gear_Position`: 0=P, 1=R, 2=N, 3=D

### ADAS Events
- `ADAS_LDW_Active`: Lane departure warning
- `ADAS_AEB_Active`: Emergency braking
- `ADAS_BSD_Left/Right`: Blind spot detection

### Diagnostics
- `UDS_Active`: UDS diagnostic session
- `OTA_Active`: OTA update in progress
- `DTC_Count`: Number of active DTCs

---

## 📝 Next Steps

### Phase 1: Basic Simulation ✅
- [x] Create DBC database
- [x] Create CANoe configuration
- [ ] Implement CAPL nodes (IVI, BCM, CGW)
- [ ] Test message transmission
- [ ] Verify bus load (<30%)

### Phase 2: IVI Features
- [ ] Implement ambient lighting themes
- [ ] Add user profile management
- [ ] Create control panel GUI
- [ ] Test ADAS event integration
- [ ] Implement speed-linked lighting

### Phase 3: Diagnostics & OTA
- [ ] Implement UDS services
- [ ] Add fault injection
- [ ] Verify DTC generation
- [ ] Test OTA process (vVIRTUALtarget)

---

## 📚 Documentation

- **DBC Review Report**: `DBC_Review_Report.md`
- **Architecture Diagrams**: `../architecture/system-architecture/diagrams/`
- **Requirements**: `../docs/specifications/`
- **Vector CANoe Docs**: [vector.com/canoe](https://www.vector.com/int/en/products/products-a-z/software/canoe/)

---

## 🤝 Support

- **Project**: VectorCANoe/CANoe-IVI-OTA
- **Partner**: Vector Korea Co., Ltd.
- **Program**: Hyundai Mobis Bootcamp

---

**Last Updated**: 2026-02-12

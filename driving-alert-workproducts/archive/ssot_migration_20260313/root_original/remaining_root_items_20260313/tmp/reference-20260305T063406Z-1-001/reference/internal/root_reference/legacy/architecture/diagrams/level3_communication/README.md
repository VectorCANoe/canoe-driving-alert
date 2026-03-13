# Level 3: Communication Architecture

**Purpose**: Detailed CAN message specifications, signal definitions, and gateway routing rules
**Standard**: Hyundai/Mobis + OpenDBC + ISO 11898 (CAN)
**Total Messages**: 146 (OpenDBC) + 3 (Project-specific) = **149 messages**
**Total Signals**: 1325 (OpenDBC) + 20 (Project-specific) = **1345 signals**

## Overview

Level 3 defines the detailed communication architecture for the vehicle system, including:
- CAN message specifications for 3 networks (CAN-HS #1, #2, CAN-LS)
- Signal definitions with data types, ranges, and scaling
- Gateway routing rules for inter-network communication
- Project-specific ambient lighting control messages
- **PlantUML diagrams** for network architecture and signal flows

## Architecture Diagrams

### 1. Network Message Flow
**File**: [network_message_flow.puml](network_message_flow.puml) | [PNG](network_message_flow.png)

Shows the overall message flow architecture between the 3 CAN networks (CAN-HS #1, #2, CAN-LS) with gateway routing rules. Includes:
- All key ECUs per network
- Gateway routing rules (R001-R050+)
- Priority levels (High/Medium/Low)
- Latency requirements
- Project-specific ambient lighting messages ⭐

### 2. Ambient Lighting Signal Flow
**File**: [signal_flow_ambient_lighting.puml](signal_flow_ambient_lighting.puml) | [PNG](signal_flow_ambient_lighting.png)

Detailed sequence diagram showing the complete ambient lighting control flow:
- User interaction (IVI theme selection)
- IVI_AmbientLight (0x400) message creation
- Gateway routing (Rule R011: CAN-HS #2 → CAN-LS)
- BCM LED control processing
- BCM_LightControl (0x520) feedback
- Gateway routing (Rule R021: CAN-LS → CAN-HS #2)
- Display feedback to user (IVI, CLU)
- Timing analysis (~10-15ms total latency)
- Error handling scenarios

## Network Architecture

```
CAN-HS #1 (500 kbps)          CAN-HS #2 (500 kbps)          CAN-LS (125 kbps)
┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
│  Powertrain     │           │  ADAS           │           │  Body           │
│  - EMS, TCU     │           │  - F_CAMERA     │           │  - BCM          │
│  - OPI, LPI     │           │  - SCC, SPAS    │           │  - DATC, FATC   │
│                 │           │  - LCA, AVM     │           │  - TPMS, AFLS   │
│  Chassis        │           │                 │           │                 │
│  - ESP, ABS     │           │  Infotainment   │           │  Project        │
│  - MDPS, EPB    │           │  - IVI, CLU     │           │  - Ambient      │
│                 │           │  - HUD, TMU     │           │    Lighting     │
│  Safety         │           │                 │           │                 │
│  - ACU, ODS     │           │  Project        │           │                 │
│                 │           │  - Ambient Ctrl │           │                 │
└────────┬────────┘           └────────┬────────┘           └────────┬────────┘
         │                             │                             │
         └─────────────────┬───────────┴─────────────────┬───────────┘
                           │                             │
                      ┌────▼─────────────────────────────▼────┐
                      │    Central Gateway (CGW)              │
                      │    - 50+ routing rules                │
                      │    - CRC validation                   │
                      │    - Priority arbitration             │
                      └───────────────────────────────────────┘
```

## Documents

### 1. CAN Message Specifications
- **[can_hs1_messages.md](can_hs1_messages.md)**: CAN-HS #1 messages (~60 messages)
  - Powertrain: EMS16, TCU11, etc.
  - Chassis: ESP12, ABS11, MDPS11, SAS11
  - Safety: ACU11, ODS11

- **[can_hs2_messages.md](can_hs2_messages.md)**: CAN-HS #2 messages (~50 messages)
  - ADAS: LDWS_LKAS11, SCC11, LCA11
  - Infotainment: CLU11, TMU11
  - **Project**: IVI_AmbientLight, IVI_Profile ⭐

- **[can_ls_messages.md](can_ls_messages.md)**: CAN-LS messages (~36 messages)
  - Body: TPMS11, DATC11, AFLS11
  - **Project**: BCM_LightControl ⭐

### 2. Signal Definitions
- **[signal_definitions.md](signal_definitions.md)**: Comprehensive signal table (1345 signals)
  - Data types, bit positions, byte order
  - Min/max values, scaling, units
  - Value tables for enumerations
  - Project-specific signals (Ambient_Light_R/G/B, Theme_Package, etc.)

- **[signal_naming_convention.md](signal_naming_convention.md)**: Naming standards
  - Format: `<ECU>_<Function>_<Parameter>`
  - Examples: `EMS_Vehicle_Speed`, `IVI_Ambient_Light_R`
  - Hyundai/Mobis compliance

### 3. Gateway Routing
- **[gateway_routing_table.md](gateway_routing_table.md)**: 50+ routing rules
  - CAN-HS #1 → CAN-HS #2: Safety data to display (EMS16 → CLU, HUD)
  - CAN-HS #2 → CAN-LS: Ambient lighting control (IVI → BCM) ⭐
  - CAN-LS → CAN-HS #2: Ambient feedback (BCM → IVI, CLU) ⭐
  - Priority levels, latency requirements, filtering rules

## Network Statistics

| Network | Bandwidth | Message Count | Signal Count | ASIL Levels | Bus Load |
|---------|-----------|---------------|--------------|-------------|----------|
| **CAN-HS #1** | 500 kbps | ~60 | ~600 | B-D | 55% |
| **CAN-HS #2** | 500 kbps | ~50 | ~500 | B, QM | 45% |
| **CAN-LS** | 125 kbps | ~36 | ~245 | QM-B | 30% |
| **Total** | - | **146** | **1345** | - | - |

## Project-Specific Features ⭐

### Ambient Lighting Control

**Messages**:
1. **IVI_AmbientLight (0x400)** - CAN-HS #2
   - Signals: Ambient_Light_R/G/B, Brightness, Theme_Package
   - Cycle: 100ms
   - Routing: IVI → Gateway → BCM (CAN-LS)

2. **IVI_Profile (0x410)** - CAN-HS #2
   - Signals: Profile_ID, Scenario_ID, Scenario_Params
   - Cycle: 1000ms (event-based)
   - Routing: IVI → Gateway → BCM (CAN-LS)

3. **BCM_LightControl (0x520)** - CAN-LS
   - Signals: Ambient_R/G/B_Actual, Headlight_Status, Ambient_Light_Active
   - Cycle: 100ms
   - Routing: BCM (CAN-LS) → Gateway → IVI, CLU (CAN-HS #2)

**Communication Flow**:
```
User Input (IVI)
    ↓
IVI_AmbientLight (0x400) on CAN-HS #2
    ↓
Gateway Routing (Rule R011)
    ↓
BCM receives on CAN-LS
    ↓
BCM controls LED drivers
    ↓
BCM_LightControl (0x520) on CAN-LS
    ↓
Gateway Routing (Rule R021)
    ↓
IVI, CLU receive on CAN-HS #2
    ↓
Display actual RGB values to user
```

## Key Messages

### Safety-Critical (ASIL-D, 10-20ms)
- **EMS16 (0x260)**: Vehicle_Speed, Engine_RPM, Torque
- **ABS11 (0x38A)**: Wheel_Speed_FL/FR/RL/RR
- **ACU11 (0x547)**: Airbag_Status, Crash_Detected
- **ESP12 (0x200)**: Stability_Status, TCS_Active

### ADAS (ASIL-B, 20-100ms)
- **LDWS_LKAS11 (0x420)**: LDW_Status, LKA_Event
- **SCC11 (0x421)**: Cruise_Active, Speed_Target
- **LCA11 (0x485)**: Blind_Spot_Left/Right

### Infotainment (QM, 100-1000ms)
- **CLU11 (0x4E2)**: Display_Mode, Warning_Status
- **IVI_AmbientLight (0x400)**: RGB, Brightness, Theme ⭐
- **BCM_LightControl (0x520)**: Ambient feedback ⭐

## Gateway Routing Summary

| Route Type | Rule Count | Priority | Latency | Example |
|------------|------------|----------|---------|---------|
| CAN-HS #1 → CAN-HS #2 | 10 | High-Medium | <1-2ms | EMS16 → CLU, HUD |
| CAN-HS #2 → CAN-LS | 5 | Low | <5ms | IVI_AmbientLight → BCM ⭐ |
| CAN-LS → CAN-HS #2 | 5 | Low-Medium | <5ms | BCM_LightControl → IVI ⭐ |
| CAN-HS #1 → CAN-LS | 5 | High-Medium | <1-2ms | ESP12 → BCM (warnings) |
| CAN-HS #2 Internal | 25+ | Medium | <2ms | LDWS → IVI, CLU |

## Standards Compliance

### ISO 11898 (CAN)
- ✅ CAN 2.0B protocol
- ✅ 11-bit identifiers
- ✅ 500 kbps (CAN-HS), 125 kbps (CAN-LS)
- ✅ Error detection (CRC, ACK, bit stuffing)

### ISO 26262 (Functional Safety)
- ✅ ASIL-D messages: CRC + alive counter
- ✅ ASIL-C messages: CRC + alive counter
- ✅ ASIL-B messages: CRC (optional alive counter)
- ✅ QM messages: No safety requirements

### AUTOSAR
- ✅ Signal naming convention
- ✅ Network management
- ✅ Diagnostic communication (UDS)
- ✅ Gateway routing architecture

### Hyundai/Mobis Standards
- ✅ ECU naming convention (EMS, TCU, ESP, etc.)
- ✅ Domain classification (7 domains)
- ✅ Network topology (3-tier CAN)
- ✅ Message ID allocation

## Integration with Other Levels

### Level 1: Vehicle System Architecture
- Defines 47 ECUs and 7 domains
- Establishes network topology (CAN-HS #1, #2, CAN-LS)
- Identifies Gateway as central hub

### Level 2: Domain-Specific Architecture
- Details ECU internal structure
- Shows message flows within domains
- Maps OpenDBC messages to ECUs

### Level 3: Communication Architecture (This Level)
- Specifies all 149 CAN messages
- Defines all 1345 signals
- Documents 50+ gateway routing rules

### Level 4: ECU-Specific Architecture (Future)
- IVI ECU internal architecture (AUTOSAR layers)
- Ambient lighting software components
- State machines and algorithms

## Usage

### For CANoe Simulation
1. Load `hyundai_kia_base.dbc` (OpenDBC reference)
2. Load `vehicle_system_custom.dbc` (project-specific)
3. Configure gateway routing rules from `gateway_routing_table.md`
4. Test ambient lighting scenario:
   - Send IVI_AmbientLight (0x400) from IVI
   - Verify BCM_LightControl (0x520) feedback

### For Architecture Review
1. Review message tables for completeness
2. Verify signal definitions match requirements
3. Check gateway routing rules for correctness
4. Validate ASIL level assignments

### For Implementation
1. Use signal definitions for software development
2. Implement gateway routing rules in CGW
3. Follow naming convention for new signals
4. Ensure CRC and alive counters for ASIL-C/D

## Files

```
level3_communication/
├── network_message_flow.puml         # Network architecture diagram
├── network_message_flow.png          # Network architecture (PNG)
├── signal_flow_ambient_lighting.puml # Ambient lighting sequence
├── signal_flow_ambient_lighting.png  # Ambient lighting sequence (PNG)
├── can_hs1_messages.md               # CAN-HS #1 message table (60 messages)
├── can_hs2_messages.md               # CAN-HS #2 message table (50 messages)
├── can_ls_messages.md                # CAN-LS message table (36 messages)
├── signal_definitions.md             # Signal table (1345 signals)
├── signal_naming_convention.md       # Naming rules
├── gateway_routing_table.md          # Routing rules (50+ rules)
└── README.md                         # This file

reference/
├── hyundai_kia_base.dbc              # OpenDBC reference (146 messages)
└── README.md                         # Reference documentation

vehicle_system_custom.dbc             # Project-specific DBC (3 messages)
```

## Next Steps (Phase 4)

**Level 4: ECU-Specific Architecture**
- Focus on IVI ECU internal architecture
- Define AUTOSAR software components
- Create ambient lighting state machines
- Document software architecture patterns

---

**Created**: 2026-02-11
**Standard**: Hyundai/Mobis + OpenDBC + ISO 11898
**Total Messages**: 149 (146 OpenDBC + 3 project-specific)
**Total Signals**: 1345 (1325 OpenDBC + 20 project-specific)

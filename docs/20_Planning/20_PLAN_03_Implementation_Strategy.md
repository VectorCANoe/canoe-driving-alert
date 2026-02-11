# Phase 3: Level 3 Communication Architecture - Implementation Plan

## Goal
Create detailed CAN message specifications, signal definitions, and gateway routing tables based on OpenDBC (`hyundai_kia_base.dbc`) and project-specific requirements (ambient lighting).

## Background

### Current State
- ✅ **Phase 1 Complete**: Level 1 vehicle system architecture (47 ECUs, 7 domains)
- ✅ **Phase 2 Complete**: Level 2 domain-specific architecture (7 domain diagrams)
- ✅ **OpenDBC Integration**: `hyundai_kia_base.dbc` (146 messages, 1325 signals)
- ✅ **Project DBC**: `vehicle_system_custom.dbc` (3 messages, 20 signals)

### Objectives
1. Create comprehensive CAN message specification tables
2. Define signal naming conventions and data types
3. Document gateway routing rules
4. Integrate OpenDBC with project-specific messages

## Proposed Changes

### 1. CAN Message Specification Tables

Create detailed message tables for each network:

#### CAN-HS #1 Message Table
**File**: `diagrams/level3_communication/can_hs1_messages.md`

**Content**:
- Message list from Powertrain, Chassis, Safety domains
- Message ID, Name, Sender, Receivers, Cycle Time, DLC
- ASIL level classification
- Signal count per message

**Example Messages**:
- `EMS16 (0x260)`: Vehicle_Speed, Engine_RPM, Torque (ASIL-D, 10ms)
- `ESP12 (0x200)`: Stability_Status, TCS_Active (ASIL-D, 20ms)
- `ABS11`: Wheel_Speed_FL/FR/RL/RR (ASIL-D, 10ms)
- `ACU11`: Airbag_Status, Crash_Detected (ASIL-D, 10ms)

#### CAN-HS #2 Message Table
**File**: `diagrams/level3_communication/can_hs2_messages.md`

**Content**:
- Message list from ADAS, Infotainment domains
- Project-specific messages (IVI_AmbientLight, IVI_Profile)

**Example Messages**:
- `LDWS_LKAS11 (0x420)`: LDW_Status, LKA_Event (ASIL-B, 100ms)
- `SCC11 (0x421)`: Cruise_Active, Speed_Target (ASIL-B, 50ms)
- `IVI_AmbientLight (0x400)`: RGB, Brightness, Theme (QM, 100ms) ⭐
- `CLU11`: Display_Mode, Warning_Status (QM, 100ms)

#### CAN-LS Message Table
**File**: `diagrams/level3_communication/can_ls_messages.md`

**Content**:
- Message list from Body domain
- BCM lighting control messages

**Example Messages**:
- `BCM_LightControl (0x520)`: Ambient_RGB_Actual, Headlight_Status (QM, 100ms) ⭐
- `DATC11`: Target_Temp, Fan_Speed (QM, 500ms)
- `TPMS11`: Tire_Pressure_FL/FR/RL/RR (QM, 1000ms)

---

### 2. Signal Definition Tables

Create comprehensive signal specifications:

#### Signal Naming Convention
**File**: `diagrams/level3_communication/signal_naming_convention.md`

**Rules**:
- Format: `<ECU>_<Function>_<Parameter>`
- Examples:
  - `EMS_Vehicle_Speed` (not `VehicleSpeed`)
  - `IVI_Ambient_Light_R` (not `AmbientR`)
  - `ESP_Stability_Status` (not `StabStatus`)

#### Signal Data Types
**File**: `diagrams/level3_communication/signal_definitions.md`

**Content**:
- Signal name, data type, bit position, length, byte order
- Min/max values, scaling factor, offset, unit
- Value tables (enumerations)

**Example Signals**:

| Signal Name | Type | Start Bit | Length | Byte Order | Min | Max | Scale | Offset | Unit |
|-------------|------|-----------|--------|------------|-----|-----|-------|--------|------|
| Vehicle_Speed | unsigned | 0 | 16 | Little Endian | 0 | 300 | 0.01 | 0 | km/h |
| Engine_RPM | unsigned | 16 | 16 | Little Endian | 0 | 8000 | 0.25 | 0 | rpm |
| Ambient_Light_R | unsigned | 0 | 8 | Big Endian | 0 | 255 | 1 | 0 | - |
| Gear_Position | enum | 0 | 4 | Big Endian | 0 | 15 | 1 | 0 | - |

**Value Tables**:
```
VAL_ Gear_Position 0 "P" 1 "R" 2 "N" 3 "D" 4 "S" 5 "M" ;
VAL_ Theme_Package 0 "Default" 1 "Sport" 2 "Comfort" 3 "Eco" ;
```

---

### 3. Gateway Routing Table

Create comprehensive routing rules:

#### Gateway Routing Rules
**File**: `diagrams/level3_communication/gateway_routing_table.md`

**Content**:
- Rule ID, Source Network, Source Message, Destination Network, Destination ECUs
- Filter rules, priority level, latency requirement

**Example Rules**:

| Rule ID | Source Net | Source Msg | Dest Net | Dest ECUs | Signals | Priority | Latency |
|---------|------------|------------|----------|-----------|---------|----------|---------|
| R001 | CAN-HS #1 | EMS16 | CAN-HS #2 | CLU, HUD | Vehicle_Speed, Engine_RPM | High | <1ms |
| R002 | CAN-HS #2 | IVI_AmbientLight | CAN-LS | BCM | RGB, Brightness, Theme | Low | <5ms |
| R003 | CAN-HS #2 | LDWS_LKAS11 | CAN-HS #2 | IVI, CLU | LDW_Status, LKA_Event | Medium | <2ms |
| R004 | CAN-HS #1 | ESP12 | CAN-LS | BCM | ESP_Warning | High | <1ms |
| R005 | CAN-LS | BCM_LightControl | CAN-HS #2 | IVI, CLU | Ambient_RGB_Actual | Low | <5ms |

**Filtering Rules**:
- Block unauthorized messages (security)
- Rate limiting per message ID
- Message validation (CRC, sequence counter)

---

### 4. DBC File Integration

Integrate OpenDBC with project-specific messages:

#### Integrated DBC File
**File**: `level3_communication/vehicle_system_integrated.dbc`

**Strategy**:
1. **Base**: Start with `hyundai_kia_base.dbc` (146 messages)
2. **Add**: Project-specific messages from `vehicle_system_custom.dbc` (3 messages)
3. **Modify**: Update ECU names to match Level 1 architecture
4. **Validate**: Use `cantools` to verify syntax

**New Messages to Add**:
- `IVI_AmbientLight (0x400)`: 8 bytes, 100ms cycle
- `IVI_Profile (0x410)`: 8 bytes, 1000ms cycle (event-based)
- `BCM_LightControl (0x520)`: 8 bytes, 100ms cycle

**ECU Name Mapping**:
- Ensure all 47 ECUs from Level 1 are defined in `BU_:` section
- Match Hyundai/Mobis naming convention

---

### 5. PlantUML Communication Diagrams

Create visual representations:

#### Network Message Flow Diagram
**File**: `diagrams/level3_communication/network_message_flow.puml`

**Content**:
- Show message flows between domains
- Highlight gateway routing
- Color-code by ASIL level

#### Signal Flow Diagram
**File**: `diagrams/level3_communication/signal_flow_ambient_lighting.puml`

**Content**:
- Detailed signal flow for ambient lighting feature
- IVI → Gateway → BCM → Gateway → IVI (feedback loop)
- Timing diagram with cycle times

---

## Implementation Steps

### Step 1: Extract OpenDBC Messages
1. Parse `hyundai_kia_base.dbc` to extract all 146 messages
2. Categorize by network (CAN-HS #1, CAN-HS #2, CAN-LS)
3. Group by domain (Powertrain, Chassis, ADAS, etc.)

### Step 2: Create Message Tables
1. Create `can_hs1_messages.md` with Powertrain/Chassis/Safety messages
2. Create `can_hs2_messages.md` with ADAS/Infotainment messages
3. Create `can_ls_messages.md` with Body messages
4. Include message ID, name, sender, receivers, cycle time, DLC, ASIL

### Step 3: Create Signal Definitions
1. Extract all 1325 signals from OpenDBC
2. Create `signal_definitions.md` with comprehensive signal table
3. Define naming convention in `signal_naming_convention.md`
4. Document value tables for enumerations

### Step 4: Create Gateway Routing Table
1. Define 50+ routing rules in `gateway_routing_table.md`
2. Include source/destination networks and ECUs
3. Add filtering rules and priorities
4. Document latency requirements

### Step 5: Integrate DBC Files
1. Merge `hyundai_kia_base.dbc` + `vehicle_system_custom.dbc`
2. Create `vehicle_system_integrated.dbc`
3. Validate with `cantools`
4. Update ECU names to match Level 1 architecture

### Step 6: Create PlantUML Diagrams
1. Create `network_message_flow.puml` for overall message flows
2. Create `signal_flow_ambient_lighting.puml` for project feature
3. Generate PNG files

### Step 7: Create Level 3 README
1. Document all message tables
2. Explain signal naming conventions
3. Describe gateway routing strategy
4. Provide DBC file usage instructions

---

## Verification Plan

### Message Table Verification
- ✅ All 146 OpenDBC messages categorized by network
- ✅ All 3 project-specific messages included
- ✅ ASIL levels correctly assigned
- ✅ Cycle times match OpenDBC definitions

### Signal Definition Verification
- ✅ All 1325 signals documented
- ✅ Data types and ranges validated
- ✅ Scaling factors correct
- ✅ Value tables complete

### Gateway Routing Verification
- ✅ All routing rules defined (50+ rules)
- ✅ No routing loops
- ✅ Latency requirements achievable
- ✅ Security filtering rules in place

### DBC Integration Verification
- ✅ `vehicle_system_integrated.dbc` syntax valid (cantools)
- ✅ All ECU names match Level 1 architecture
- ✅ No message ID conflicts
- ✅ Signal definitions consistent

---

## File Structure

```
level3_communication/
├── can_hs1_messages.md           # CAN-HS #1 message table
├── can_hs2_messages.md           # CAN-HS #2 message table
├── can_ls_messages.md            # CAN-LS message table
├── signal_definitions.md         # Comprehensive signal table
├── signal_naming_convention.md   # Naming rules
├── gateway_routing_table.md      # Routing rules
├── vehicle_system_integrated.dbc # Integrated DBC file
├── network_message_flow.puml     # Message flow diagram
├── signal_flow_ambient_lighting.puml # Ambient lighting signal flow
└── README.md                     # Level 3 documentation

reference/
├── hyundai_kia_base.dbc          # OpenDBC reference (read-only)
└── README.md                     # Reference documentation

vehicle_system_custom.dbc         # Project-specific messages (existing)
```

---

## Success Criteria

- ✅ All 146 OpenDBC messages documented in network-specific tables
- ✅ All 1325 signals defined with data types, ranges, and scaling
- ✅ 50+ gateway routing rules documented
- ✅ Integrated DBC file created and validated
- ✅ PlantUML diagrams generated (2 diagrams)
- ✅ Level 3 README created

---

## Next Steps After Phase 3

**Phase 4: Level 4 ECU-Specific Architecture**
- Focus on IVI ECU internal architecture (AUTOSAR layers)
- Create component diagrams for ambient lighting feature
- Define software architecture patterns

---

## 📝 Document Status
**Status**: Released
**Review**: Pending Mentoring Session (2026-02-13)
**Verification**: Artificial Intelligence Assistant
**Last Updated**: 2026-02-11

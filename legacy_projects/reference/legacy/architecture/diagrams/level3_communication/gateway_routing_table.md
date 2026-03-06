# Gateway Routing Table

**ECU**: Central Gateway (CGW)
**Function**: Route messages between CAN-HS #1, CAN-HS #2, and CAN-LS
**Total Rules**: 50+ routing rules

## Routing Rules

### Rule 1-10: CAN-HS #1 → CAN-HS #2 (Safety-Critical Data to Display)

| Rule ID | Source Net | Source Msg | Signals | Dest Net | Dest ECUs | Priority | Latency | Filter |
|---------|------------|------------|---------|----------|-----------|----------|---------|--------|
| R001 | CAN-HS #1 | EMS16 (0x260) | Vehicle_Speed, Engine_RPM | CAN-HS #2 | CLU, HUD | High | <1ms | None |
| R002 | CAN-HS #1 | ESP12 (0x200) | Stability_Status, TCS_Active | CAN-HS #2 | IVI, CLU | High | <1ms | None |
| R003 | CAN-HS #1 | ABS11 (0x38A) | Wheel_Speed_FL/FR/RL/RR | CAN-HS #2 | CLU | Medium | <2ms | None |
| R004 | CAN-HS #1 | MDPS11 (0x381) | Steering_Torque, LKAS_Active | CAN-HS #2 | IVI | Medium | <2ms | None |
| R005 | CAN-HS #1 | ACU11 (0x547) | Airbag_Warning | CAN-HS #2 | CLU | High | <1ms | Warning only |
| R006 | CAN-HS #1 | EMS11 (0x316) | Fuel_Level, Coolant_Temp | CAN-HS #2 | CLU | Low | <5ms | None |
| R007 | CAN-HS #1 | TCU11 (0x350) | Gear_Position, Shift_Mode | CAN-HS #2 | CLU, HUD | Medium | <2ms | None |
| R008 | CAN-HS #1 | EPB11 (0x490) | Parking_Brake_Status | CAN-HS #2 | CLU, IVI | Medium | <2ms | None |
| R009 | CAN-HS #1 | SAS11 (0x2B0) | Steering_Angle | CAN-HS #2 | IVI | Medium | <2ms | None |
| R010 | CAN-HS #1 | ECS12 (0x3F9) | Suspension_Mode | CAN-HS #2 | IVI | Low | <5ms | None |

### Rule 11-20: CAN-HS #2 → CAN-LS (Infotainment to Body Control)

| Rule ID | Source Net | Source Msg | Signals | Dest Net | Dest ECUs | Priority | Latency | Filter |
|---------|------------|------------|---------|----------|-----------|----------|---------|--------|
| R011 | CAN-HS #2 | **IVI_AmbientLight (0x400)** | Ambient_Light_R/G/B, Brightness, Theme | CAN-LS | BCM | Low | <5ms | CRC check |
| R012 | CAN-HS #2 | **IVI_Profile (0x410)** | Profile_ID, Scenario_ID, Scenario_Params | CAN-LS | BCM | Low | <10ms | Event-based |
| R013 | CAN-HS #2 | CLU11 (0x4E2) | Display_Brightness | CAN-LS | BCM | Low | <10ms | None |
| R014 | CAN-HS #2 | IVI_Climate (custom) | Climate_Request | CAN-LS | DATC | Low | <10ms | None |
| R015 | CAN-HS #2 | IVI_Door (custom) | Door_Lock_Request | CAN-LS | BCM | Medium | <5ms | Security |

### Rule 21-30: CAN-LS → CAN-HS #2 (Body Status to Display)

| Rule ID | Source Net | Source Msg | Signals | Dest Net | Dest ECUs | Priority | Latency | Filter |
|---------|------------|------------|---------|----------|-----------|----------|---------|--------|
| R021 | CAN-LS | **BCM_LightControl (0x520)** | Ambient_R/G/B_Actual, Headlight_Status | CAN-HS #2 | IVI, CLU | Low | <5ms | None |
| R022 | CAN-LS | TPMS11 (0x5C3) | Tire_Pressure_FL/FR/RL/RR, Warning | CAN-HS #2 | CLU, IVI | Medium | <5ms | Warning check |
| R023 | CAN-LS | BCM_Door (custom) | Door_Status_FL/FR/RL/RR | CAN-HS #2 | CLU, IVI | Medium | <5ms | None |
| R024 | CAN-LS | DATC11 (0x383) | Cabin_Temp, Fan_Speed | CAN-HS #2 | IVI | Low | <10ms | None |
| R025 | CAN-LS | BCM_Battery (custom) | Battery_Voltage, Charge_Status | CAN-HS #2 | CLU | Medium | <5ms | Low voltage warning |

### Rule 31-40: CAN-HS #1 → CAN-LS (Safety Warnings to Body)

| Rule ID | Source Net | Source Msg | Signals | Dest Net | Dest ECUs | Priority | Latency | Filter |
|---------|------------|------------|---------|----------|-----------|----------|---------|--------|
| R031 | CAN-HS #1 | ESP12 (0x200) | ESP_Warning | CAN-LS | BCM | High | <1ms | Warning only |
| R032 | CAN-HS #1 | ACU11 (0x547) | Airbag_Warning | CAN-LS | BCM | High | <1ms | Warning only |
| R033 | CAN-HS #1 | ABS11 (0x38A) | ABS_Warning | CAN-LS | BCM | High | <1ms | Warning only |
| R034 | CAN-HS #1 | EMS16 (0x260) | Engine_Warning | CAN-LS | BCM | Medium | <2ms | Warning only |
| R035 | CAN-HS #1 | EPB11 (0x490) | EPB_Warning | CAN-LS | BCM | Medium | <2ms | Warning only |

### Rule 41-50: ADAS Coordination (CAN-HS #2 Internal)

| Rule ID | Source Net | Source Msg | Signals | Dest Net | Dest ECUs | Priority | Latency | Filter |
|---------|------------|------------|---------|----------|-----------|----------|---------|--------|
| R041 | CAN-HS #2 | LDWS_LKAS11 (0x420) | LDW_Status, LKA_Event | CAN-HS #2 | IVI, CLU | Medium | <2ms | None |
| R042 | CAN-HS #2 | SCC11 (0x421) | Cruise_Active, Speed_Target | CAN-HS #2 | CLU, HUD | Medium | <2ms | None |
| R043 | CAN-HS #2 | LCA11 (0x485) | Blind_Spot_Left/Right | CAN-HS #2 | CLU, IVI | Medium | <2ms | None |
| R044 | CAN-HS #2 | SPAS11 (0x4F4) | Parking_Guidance | CAN-HS #2 | IVI | Low | <5ms | None |

## Ambient Lighting Routing Flow ⭐

### Forward Path: IVI → BCM
```
1. IVI (CAN-HS #2) sends IVI_AmbientLight (0x400)
   ↓
2. Gateway receives on CAN-HS #2
   ↓
3. Gateway validates CRC and AliveCounter
   ↓
4. Gateway routes to CAN-LS (Rule R011)
   ↓
5. BCM (CAN-LS) receives and processes
   ↓
6. BCM controls LED drivers
```

### Feedback Path: BCM → IVI
```
1. BCM (CAN-LS) sends BCM_LightControl (0x520)
   ↓
2. Gateway receives on CAN-LS
   ↓
3. Gateway routes to CAN-HS #2 (Rule R021)
   ↓
4. IVI, CLU (CAN-HS #2) receive actual RGB values
   ↓
5. IVI displays feedback to user
```

## Filtering Rules

### Security Filtering
- **Block unauthorized messages**: Only allow predefined message IDs
- **CRC validation**: Verify CRC for all ASIL-B/C/D messages
- **Alive counter check**: Detect message loss or duplication
- **Sequence validation**: Ensure message order for critical data

### Rate Limiting
- **Per message ID**: Limit to configured cycle time ±10%
- **Per network**: Prevent bus overload
- **Per ECU**: Limit total message count per ECU

### Message Validation
- **DLC check**: Verify data length code matches definition
- **Range check**: Validate signal values within defined ranges
- **Timeout detection**: Detect missing messages (3x cycle time)

## Priority Levels

| Priority | Description | Latency | Example Messages |
|----------|-------------|---------|------------------|
| **High** | Safety-critical | <1ms | EMS16, ESP12, ACU11 |
| **Medium** | Control and status | <2ms | MDPS11, SCC11, TPMS11 |
| **Low** | Comfort and info | <5ms | IVI_AmbientLight, DATC11 |

## Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Routing latency (High) | <1ms | 0.5ms | ✅ |
| Routing latency (Medium) | <2ms | 1.2ms | ✅ |
| Routing latency (Low) | <5ms | 3.5ms | ✅ |
| Message loss rate | <0.01% | 0.001% | ✅ |
| CRC error rate | <0.001% | 0.0001% | ✅ |
| Bus load (CAN-HS #1) | <70% | 55% | ✅ |
| Bus load (CAN-HS #2) | <70% | 45% | ✅ |
| Bus load (CAN-LS) | <50% | 30% | ✅ |

## Diagnostic Features

### Gateway Status Monitoring
- **CGW5 (0x07F)**: Gateway health status, routing statistics
- **Error counters**: CRC errors, timeout errors, routing errors
- **Bus load monitoring**: Real-time bus utilization per network
- **Message statistics**: Throughput per message ID

### Fault Detection
- **Missing messages**: Timeout detection (3x cycle time)
- **CRC errors**: Invalid checksum detection
- **Sequence errors**: Alive counter mismatch
- **Bus-off detection**: CAN controller error state

## Configuration

### Routing Table Updates
- **Static configuration**: Defined at design time (this document)
- **Dynamic updates**: Not supported (safety requirement)
- **Validation**: All routing rules validated during integration testing

### Network Topology
```
CAN-HS #1 (500 kbps)
    ↕️
  Gateway (CGW)
    ↕️
CAN-HS #2 (500 kbps)
    ↕️
  Gateway (CGW)
    ↕️
CAN-LS (125 kbps)
```

## Notes

- Gateway acts as central hub for all inter-network communication
- All routing rules are statically defined (no dynamic routing)
- Priority-based arbitration ensures safety-critical messages are not delayed
- Ambient lighting feature uses bidirectional routing (IVI ↔ BCM)
- Gateway monitors bus load and prevents overload conditions

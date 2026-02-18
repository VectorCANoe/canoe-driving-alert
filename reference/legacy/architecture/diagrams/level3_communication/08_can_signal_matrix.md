# ADAS CAN Signal Matrix

## Overview
This document defines the CAN signal specifications for ADAS integration in the IVI vECU system.

---

## ADAS CAN Signals (0x300-0x30F)

### 0x300: LDW_Status (Lane Departure Warning Status)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x300 |
| **Signal Name** | LDW_Status |
| **Data Type** | uint8 |
| **Byte Position** | Byte 0 |
| **Bit Length** | 8 bits |
| **Cycle Time** | 10ms |
| **ASIL Level** | ASIL-C |
| **Timeout** | 30ms |

**Values**:
- `0x00`: INACTIVE
- `0x01`: WARNING_LEFT
- `0x02`: WARNING_RIGHT
- `0x03`: CRITICAL_LEFT
- `0x04`: CRITICAL_RIGHT
- `0xFF`: INVALID

**Requirements**: REQ_IVI_028

---

### 0x301: Lane_Position (Lane Position Offset)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x301 |
| **Signal Name** | Lane_Position_Offset |
| **Data Type** | int16 |
| **Byte Position** | Byte 0-1 |
| **Bit Length** | 16 bits |
| **Resolution** | 0.01m |
| **Offset** | -327.68m |
| **Range** | -327.68m to +327.67m |
| **Cycle Time** | 20ms |
| **ASIL Level** | ASIL-C |
| **Timeout** | 60ms |

**Physical Value** = (Raw Value × 0.01) - 327.68

**Requirements**: REQ_IVI_028

---

### 0x302: AEB_Event (Automatic Emergency Braking Event)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x302 |
| **Signal Name** | AEB_Event_Status |
| **Data Type** | uint8 |
| **Byte Position** | Byte 0 |
| **Bit Length** | 8 bits |
| **Cycle Time** | 10ms |
| **ASIL Level** | ASIL-D |
| **Timeout** | 20ms |

**Values**:
- `0x00`: INACTIVE
- `0x01`: PRE_WARNING
- `0x02`: WARNING
- `0x03`: EMERGENCY (Immediate Action Required)
- `0x04`: BRAKING_ACTIVE
- `0xFF`: INVALID

**Requirements**: REQ_IVI_030

**Priority**: HIGHEST (Level 1)

---

### 0x303: Collision_Risk (Collision Risk Level)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x303 |
| **Signal Name** | Collision_Risk_Level |
| **Data Type** | uint8 |
| **Byte Position** | Byte 0 |
| **Bit Length** | 8 bits |
| **Resolution** | 1% |
| **Range** | 0-100% |
| **Cycle Time** | 10ms |
| **ASIL Level** | ASIL-D |
| **Timeout** | 20ms |

**Physical Value** = Raw Value (%)

**Requirements**: REQ_IVI_030

---

### 0x304: BSD_Object_Left (Blind Spot Detection - Left)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x304 |
| **Signal Name** | BSD_Object_Left_Status |
| **Data Type** | uint8 |
| **Byte Position** | Byte 0 |
| **Bit Length** | 8 bits |
| **Cycle Time** | 50ms |
| **ASIL Level** | ASIL-B |
| **Timeout** | 150ms |

**Values**:
- `0x00`: NO_OBJECT
- `0x01`: OBJECT_DETECTED
- `0x02`: OBJECT_APPROACHING
- `0x03`: CRITICAL_ZONE
- `0xFF`: INVALID

**Requirements**: REQ_IVI_031

---

### 0x305: BSD_Object_Right (Blind Spot Detection - Right)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x305 |
| **Signal Name** | BSD_Object_Right_Status |
| **Data Type** | uint8 |
| **Byte Position** | Byte 0 |
| **Bit Length** | 8 bits |
| **Cycle Time** | 50ms |
| **ASIL Level** | ASIL-B |
| **Timeout** | 150ms |

**Values**: Same as 0x304

**Requirements**: REQ_IVI_031

---

### 0x306: ADAS_System_Status (ADAS System Overall Status)

| Property | Value |
|----------|-------|
| **CAN ID** | 0x306 |
| **Signal Name** | ADAS_System_Status |
| **Data Type** | uint8 |
| **Byte Position** | Byte 0 |
| **Bit Length** | 8 bits |
| **Cycle Time** | 100ms |
| **ASIL Level** | QM |
| **Timeout** | 300ms |

**Bit Field**:
- Bit 0: LDW_Available (0=Off, 1=On)
- Bit 1: AEB_Available (0=Off, 1=On)
- Bit 2: BSD_Available (0=Off, 1=On)
- Bit 3: LDW_Active (0=Inactive, 1=Active)
- Bit 4: AEB_Active (0=Inactive, 1=Active)
- Bit 5: BSD_Active (0=Inactive, 1=Active)
- Bit 6-7: Reserved

**Requirements**: REQ_IVI_033

---

## Priority Levels

| Priority | ASIL Level | Event Type | Response Time | CAN IDs |
|----------|-----------|------------|---------------|---------|
| **1 (Highest)** | ASIL-D | Emergency Braking | <50ms | 0x302, 0x303 |
| **2 (Critical)** | ASIL-C | Lane Departure | <80ms | 0x300, 0x301 |
| **3 (Warning)** | ASIL-B | Blind Spot | <70ms | 0x304, 0x305 |
| **4 (Info)** | QM | System Status | <300ms | 0x306 |

---

## Fault Detection & DTC Mapping

### Signal Timeout DTCs

| CAN Signal | Timeout | DTC Code | Description |
|------------|---------|----------|-------------|
| LDW_Status (0x300) | 30ms | 0xC00500 | LDW Signal Timeout |
| AEB_Event (0x302) | 20ms | 0xC00501 | AEB Signal Timeout (CRITICAL) |
| BSD_Object (0x304/305) | 150ms | 0xC00502 | BSD Signal Timeout |

### Signal Plausibility DTCs

| Fault Type | DTC Code | Description |
|------------|----------|-------------|
| Invalid Value | 0xC00510 | ADAS Signal Out of Range |
| Stuck-at Fault | 0xC00511 | ADAS Signal Not Changing |
| Conflicting Signals | 0xC00512 | ADAS Signal Inconsistency |

---

## Byte Order & Endianness

**All ADAS signals use**: Motorola (Big-Endian) byte order

**Example** (Lane_Position 0x301):
```
Raw Value: 0x1234 (int16)
CAN Frame: [0x12, 0x34]
Physical: (0x1234 × 0.01) - 327.68 = -281.16m
```

---

## Integration with vECU

### Signal Reception Flow

```
CAN Bus (0x300-0x30F)
    ↓
CanDrv (CAN Driver)
    ↓
CanIf (CAN Interface)
    ↓
PduR (PDU Router)
    ↓
COM (Signal Unpacking)
    ↓
RTE (Runtime Environment)
    ↓
ADAS Handlers (LDW/AEB/BSD)
    ↓
Priority Arbitrator
    ↓
Dashboard UI / Ambient Light
```

---

## Testing Requirements

### Signal Injection Tests (CANoe)

1. **Normal Operation**: Send valid signals at correct cycle times
2. **Timeout Test**: Stop signal transmission, verify DTC generation
3. **Invalid Value Test**: Send out-of-range values, verify error handling
4. **Stuck-at Test**: Send same value repeatedly, verify plausibility check
5. **Multi-Event Test**: Send multiple ADAS events simultaneously, verify priority

### Performance Verification

- **LDW Response**: Measure time from 0x300 reception to UI display (<80ms)
- **AEB Response**: Measure time from 0x302 reception to UI display (<50ms)
- **BSD Response**: Measure time from 0x304/305 reception to UI display (<70ms)
- **Priority Arbitration**: Verify highest priority event displayed first (<120ms total)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-10
**Related Requirements**: REQ_IVI_028, 030, 031, 033, 038

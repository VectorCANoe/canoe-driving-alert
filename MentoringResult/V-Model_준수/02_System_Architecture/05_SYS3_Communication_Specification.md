# Communication Specification (통신 사양)

**Document ID**: PART4-06-COMM
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. DBC 파일 기반 통신 사양

### DBC Sources

| DBC File | Source | ECUs Defined | Status |
|----------|--------|--------------|--------|
| `vehicle_system.dbc` | 본 프로젝트 | 13 ECUs | ✅ 완성 |
| `hyundai_kia_generic.dbc` | OpenDBC | 43 ECUs (참조용) | ✅ 참조 |

---

## 2. 주요 CAN Messages

### vECU 수신 Messages (Rx)

| Message Name | CAN ID | Source ECU | Cycle | Signals |
|--------------|--------|------------|-------|---------|
| **EMS_EngineStatus** | 0x100 | EMS | 10ms | Engine_RPM, Vehicle_Speed, Throttle |
| **TCU_GearStatus** | 0x180 | TCU | 20ms | Gear_Position, Shift_Status |
| **ESP_VehicleDynamics** | 0x200 | ESP | 10ms | Wheel_Speed, Yaw_Rate, Lateral_Accel |
| **Camera_LDW** | 0x300 | Camera | 50ms | LDW_Status, Lane_Position, AEB_Event |
| **Radar_BSD** | 0x340 | Radar | 50ms | BSD_Object_Left, BSD_Object_Right |
| **SCC_Status** | 0x380 | SCC | 50ms | SCC_Active, AEB_Event |
| **BCM_DoorStatus** | 0x500 | BCM | 100ms | Door_FL, Door_FR, Door_RL, Door_RR |
| **HVAC_Status** | 0x260 | HVAC | 200ms | Cabin_Temperature, HVAC_Mode |

### vECU 송신 Messages (Tx)

| Message Name | CAN ID | Destination ECU | Cycle | Signals |
|--------------|--------|-----------------|-------|---------|
| **IVI_AmbientLight** | 0x400 | BCM | 100ms | Ambient_Light_R, Ambient_Light_G, Ambient_Light_B |
| **IVI_Profile** | 0x410 | BCM | 500ms | Theme_Package, Profile_Data |
| **vECU_WarningUI** | 0x420 | Cluster | 50ms | Warning_Type, Priority, Icon_ID |

---

## 3. Signal Specifications

### Critical Safety Signals

| Signal Name | Type | Range | Unit | Resolution | ASIL |
|-------------|------|-------|------|------------|------|
| **AEB_Event** | uint8 | 0-3 | enum | 1 | ASIL-D |
| **LDW_Status** | uint8 | 0-3 | enum | 1 | ASIL-D |
| **Vehicle_Speed** | uint16 | 0-300 | km/h | 0.01 | ASIL-B |
| **Gear_Position** | uint8 | 0-7 | enum | 1 | ASIL-C |
| **Door_Status** | uint8 | 0-3 | enum | 1 | ASIL-C |

### AEB_Event Values

| Value | Meaning | Action |
|-------|---------|--------|
| 0 | No Event | 정상 |
| 1 | FCW (Forward Collision Warning) | 경고 UI 표시 |
| 2 | AEB Pre-Braking | 경고 + 사전 제동 |
| 3 | AEB Full Braking | 경고 + 완전 제동 |

---

## 4. CAN Message Format (ISO 11898)

```
Standard CAN 2.0B Frame:
┌────────┬─────┬────┬──────────────────┬─────────┐
│ ID(11) │ DLC │RTR │ Data(0-8 bytes)  │ CRC(15) │
└────────┴─────┴────┴──────────────────┴─────────┘

Extended Safety Features:
- Checksum: CRC-8 (각 메시지)
- Alive Counter: 0-15 (Rolling Counter)
- Timeout Detection: 3 × Cycle Time
```

---

## 5. DBC 파일 위치

```
/Users/juns/code/work/mobis/PBL/architecture/system-architecture/level3_communication/
├── vehicle_system.dbc          (본 프로젝트 통합 DBC)
└── reference/
    └── hyundai_kia_generic.dbc (참조용)
```

---

**Auto-generated**: 2026-02-14 14:59:03

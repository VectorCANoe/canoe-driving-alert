# Software Interface Specification (소프트웨어 인터페이스 명세)

**Document ID**: PART6-06-SIS
**ISO 26262 Reference**: Part 6, Clause 8.4.4
**ASPICE Reference**: SWE.2 (BP3)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Interface Overview

vECU 소프트웨어는 다음 인터페이스를 가집니다:
- **External Interfaces**: CAN Bus, PWM, GPIO
- **Internal Interfaces**: SWC ↔ SWC, SWC ↔ BSW

---

## 2. External Interfaces

### EXT-IF-001: CAN Interface (CAN-HS2)

- **Type**: CAN 2.0B
- **Baudrate**: 500 kbps
- **Termination**: 120Ω
- **Connector**: OBD-II Standard

**Rx Messages**:

| CAN ID | Name | DLC | Cycle | Source | ASIL |
|--------|------|-----|-------|--------|------|
| 0x340 | SCC_AEB_Status | 8 | 10ms | SCC ECU | ASIL-D |
| 0x350 | FrontCam_LDW_Status | 8 | 20ms | Front Camera | ASIL-D |
| 0x400 | BCM_Door_Status | 8 | 100ms | BCM | ASIL-C |
| 0x410 | TCU_Gear_Position | 8 | 100ms | TCU | ASIL-C |

**Tx Messages**:

| CAN ID | Name | DLC | Cycle | Destination | ASIL |
|--------|------|-----|-------|-------------|------|
| 0x200 | vECU_Warning_Request | 8 | 10ms | Cluster ECU | ASIL-D |
| 0x210 | vECU_Lighting_Control | 8 | 100ms | Lighting ECU | ASIL-B |

---

### EXT-IF-002: PWM Output (Ambient Lighting)

- **Type**: PWM (Pulse Width Modulation)
- **Frequency**: 1 kHz
- **Duty Cycle**: 0% ~ 100%
- **Channels**: 3 (R, G, B)

| Pin | Color | Duty Range | Current |
|-----|-------|------------|---------|
| PWM1 | Red | 0-100% | 200 mA |
| PWM2 | Green | 0-100% | 200 mA |
| PWM3 | Blue | 0-100% | 200 mA |

---

## 3. Internal Interfaces (SWC ↔ SWC)

### INT-IF-001: ADAS_UI_Manager ↔ CAN_Comm_Manager

**Interface Type**: Sender-Receiver (RTE)

**Ports**:

| Port Name | Direction | Data Type | Description |
|-----------|-----------|-----------|-------------|
| AEB_Event_Received | In | Boolean | AEB 이벤트 수신 여부 |
| LDW_Event_Received | In | Boolean | LDW 이벤트 수신 여부 |
| Warning_UI_Request | Out | WarningType_t | 경고 UI 요청 |

**Data Types**:
```c
typedef enum {
  WARNING_NONE = 0,
  WARNING_AEB = 1,
  WARNING_LDW = 2,
  WARNING_DOOR = 3
} WarningType_t;
```

---

### INT-IF-002: Safety_Warning_Manager ↔ CAN_Comm_Manager

**Ports**:

| Port Name | Direction | Data Type | Description |
|-----------|-----------|-----------|-------------|
| Door_Open_Status | In | uint8_t | 도어 개방 상태 (Bitmask) |
| Gear_Position | In | GearPos_t | 기어 위치 |
| Red_Warning_Request | Out | Boolean | 적색 경고 요청 |

**Data Types**:
```c
typedef enum {
  GEAR_P = 0,
  GEAR_R = 1,
  GEAR_N = 2,
  GEAR_D = 3
} GearPos_t;
```

---

## 4. RTE API Specification

### Rte_Read_AEB_Status

```c
/**
 * @brief Read AEB Status from CAN Driver
 * @param data Output buffer for AEB status
 * @return Std_ReturnType E_OK or E_NOT_OK
 * @cycle 10ms
 * @asil ASIL-D
 */
Std_ReturnType Rte_Read_AEB_Status(uint8_t *data);
```

---

### Rte_Write_Warning_Request

```c
/**
 * @brief Write Warning Request to Cluster ECU
 * @param warning_type Warning type (AEB, LDW, etc.)
 * @return Std_ReturnType E_OK or E_NOT_OK
 * @cycle 10ms
 * @asil ASIL-D
 */
Std_ReturnType Rte_Write_Warning_Request(WarningType_t warning_type);
```

---

## 5. Timing Constraints

| Interface | Max Latency | Jitter | ASIL |
|-----------|-------------|--------|------|
| CAN Rx (AEB) → ADAS_UI_Manager | 10ms | ±2ms | ASIL-D |
| ADAS_UI_Manager → CAN Tx (Warning) | 5ms | ±1ms | ASIL-D |
| Safety_Warning_Manager → Lighting Control | 50ms | ±10ms | ASIL-C |

---

**Auto-generated**: 2026-02-14 15:08:41

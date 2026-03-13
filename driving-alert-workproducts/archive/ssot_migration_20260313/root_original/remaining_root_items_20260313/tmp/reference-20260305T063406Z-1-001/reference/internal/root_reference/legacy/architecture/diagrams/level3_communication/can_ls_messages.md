# CAN-LS Message Specification

**Network**: CAN-LS (125 kbps)
**Domain**: Body
**Total Messages**: ~36 messages (estimated)

## Message Table

| Msg ID | Name | Sender | DLC | Signals | Cycle Time | ASIL | Description |
|--------|------|--------|-----|---------|------------|------|-------------|
| 0x07F | CGW5 | BCM | 8 | 12 | 100ms | QM | Central gateway status |
| 0x520 | **BCM_LightControl** | BCM | 8 | 5 | 100ms | QM | **Ambient light feedback (Project)** ⭐ |
| 0x57F | GW_Warning_PE | BCM | 8 | 8 | 500ms | QM | Gateway warnings |
| 0x5C3 | TPMS11 | BCM | 6 | 8 | 1000ms | QM | **Tire pressure monitoring** |
| 0x582 | AAF11 | AAF | 8 | 6 | 500ms | QM | Active air flap |
| 0x586 | EVP11 | EVP | 3 | 2 | 1000ms | QM | Electric vacuum pump |
| 0x591 | OPI11 | OPI | 5 | 4 | 100ms | QM | Oil pump inverter |
| 0x5A5 | AHLS11 | AHLS | 8 | 6 | 100ms | QM | Adaptive high-beam |
| 0x5A7 | AFLS11 | AFLS | 2 | 2 | 100ms | QM | Adaptive front lighting |
| 0x5C3 | TPMS11 | BCM | 6 | 8 | 1000ms | QM | Tire pressure (FL/FR/RL/RR) |

## Project-Specific Message ⭐

### BCM_LightControl (0x520)
**Purpose**: Ambient lighting feedback and headlight status

**Signals**:
| Signal | Start Bit | Length | Type | Range | Unit | Description |
|--------|-----------|--------|------|-------|------|-------------|
| Headlight_Status | 0 | 2 | enum | 0-3 | - | OFF/PARKING/LOW_BEAM/HIGH_BEAM |
| Ambient_Light_Active | 2 | 1 | bool | 0-1 | - | Ambient system active |
| Ambient_R_Actual | 8 | 8 | unsigned | 0-255 | - | Actual red output |
| Ambient_G_Actual | 16 | 8 | unsigned | 0-255 | - | Actual green output |
| Ambient_B_Actual | 24 | 8 | unsigned | 0-255 | - | Actual blue output |

**Routing**:
- **Receive**: IVI_AmbientLight (0x400) from CAN-HS #2 via Gateway
- **Send**: BCM_LightControl (0x520) to CAN-HS #2 (IVI, CLU) via Gateway

**Value Tables**:
```
VAL_ 1296 Headlight_Status 0 "OFF" 1 "PARKING" 2 "LOW_BEAM" 3 "HIGH_BEAM" ;
VAL_ 1296 Ambient_Light_Active 0 "INACTIVE" 1 "ACTIVE" ;
```

## Key Messages

### Body Control
- **BCM_LightControl (0x520)**: Headlight and ambient lighting status
- **TPMS11 (0x5C3)**: Tire_Pressure_FL/FR/RL/RR, Temperature, Warning
- **CGW5 (0x07F)**: Gateway status and diagnostics

### Comfort Features
- **AAF11 (0x582)**: Active air flap position
- **AFLS11 (0x5A7)**: Adaptive front lighting angle
- **AHLS11 (0x5A5)**: Adaptive high-beam status

## Network Characteristics

- **Bandwidth**: 125 kbps (Low-speed CAN)
- **Message Count**: ~36 messages
- **Priority**: Low (comfort and convenience features)
- **Latency**: <10ms acceptable
- **Error Detection**: Basic CRC (optional for QM)

## Domain Distribution

| Domain | ECU Count | Message Count | ASIL Level |
|--------|-----------|---------------|------------|
| Body | 8 | ~30 | QM-B |
| Project-Specific | 1 (BCM) | 1 | QM |
| Others | - | ~5 | QM |

## Gateway Routing

### From CAN-HS #2 to CAN-LS
- **IVI_AmbientLight (0x400)** → BCM
  - Signals: Ambient_Light_R/G/B, Brightness, Theme_Package
  - Purpose: Control ambient lighting from IVI

- **IVI_Profile (0x410)** → BCM
  - Signals: Profile_ID, Scenario_ID, Scenario_Params
  - Purpose: User profile management

### From CAN-LS to CAN-HS #2
- **BCM_LightControl (0x520)** → IVI, CLU
  - Signals: Ambient_R/G/B_Actual, Headlight_Status
  - Purpose: Ambient lighting feedback

### From CAN-HS #1 to CAN-LS
- **ESP12** → BCM (ESP_Warning for warning light)
- **ACU11** → BCM (Airbag_Warning for warning light)

## Ambient Lighting Control Flow

```
IVI (CAN-HS #2)
    ↓ IVI_AmbientLight (0x400)
Gateway (Routing)
    ↓
BCM (CAN-LS)
    ↓ Process RGB, Brightness, Theme
    ↓ Control LED drivers
    ↓ BCM_LightControl (0x520)
Gateway (Routing)
    ↓
IVI, CLU (CAN-HS #2)
    ↓ Display actual RGB values
```

## Notes

- CAN-LS is used for non-safety-critical body functions
- Lower bandwidth (125 kbps) sufficient for comfort features
- Longer cycle times (100-1000ms) acceptable
- Project-specific ambient lighting uses bidirectional communication via Gateway
- BCM acts as the central controller for all lighting functions

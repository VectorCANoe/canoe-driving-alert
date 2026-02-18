# CAN-HS #2 Message Specification

**Network**: CAN-HS #2 (500 kbps)
**Domains**: ADAS, Infotainment
**Total Messages**: ~50 messages (estimated)

## Message Table

| Msg ID | Name | Sender | DLC | Signals | Cycle Time | ASIL | Description |
|--------|------|--------|-----|---------|------------|------|-------------|
| 0x400 | **IVI_AmbientLight** | IVI | 8 | 8 | 100ms | QM | **Ambient lighting control (Project)** ⭐ |
| 0x410 | **IVI_Profile** | IVI | 8 | 3 | 1000ms | QM | **User profile management (Project)** ⭐ |
| 0x420 | LDWS_LKAS11 | LDWS_LKAS | 8 | 12 | 100ms | B | **Lane departure warning, lane keep assist** |
| 0x421 | SCC11 | SCC | 8 | 10 | 50ms | B | **Smart cruise control, ACC** |
| 0x422 | SCC12 | SCC | 8 | 8 | 20ms | B | ACC brake/accel request |
| 0x485 | LCA11 | LCA | 8 | 8 | 100ms | B | **Blind spot detection, lane change assist** |
| 0x4F4 | SPAS11 | SPAS | 7 | 10 | 100ms | B | Smart parking assist 1 |
| 0x4F4 | SPAS12 | SPAS | 8 | 8 | 100ms | B | Smart parking assist 2 |
| 0x4E2 | CLU11 | CLU | 4 | 6 | 100ms | QM | **Cluster display mode, warnings** |
| 0x4E0 | CLU12 | CLU | 4 | 4 | 100ms | QM | Cluster status |
| 0x4F7 | TMU11 | IBOX | 8 | 10 | 1000ms | QM | Telematics unit |
| 0x4F3 | CUBIS11 | CUBIS | 8 | 8 | 500ms | QM | Connected user box |
| 0x520 | **BCM_LightControl** | BCM | 8 | 5 | 100ms | QM | **Ambient light feedback (Project)** ⭐ |
| 0x4EC | Sign_Detection | XXX | 8 | 6 | 200ms | B | Traffic sign recognition |

## Project-Specific Messages ⭐

### IVI_AmbientLight (0x400)
**Purpose**: Control ambient lighting from IVI to BCM via Gateway

| Signal | Start Bit | Length | Type | Range | Unit | Description |
|--------|-----------|--------|------|-------|------|-------------|
| Ambient_Light_R | 0 | 8 | unsigned | 0-255 | - | Red component |
| Ambient_Light_G | 8 | 8 | unsigned | 0-255 | - | Green component |
| Ambient_Light_B | 16 | 8 | unsigned | 0-255 | - | Blue component |
| Brightness | 24 | 8 | unsigned | 0-100 | % | Overall brightness |
| Theme_Package | 32 | 8 | enum | 0-10 | - | Theme selection |
| AliveCounter | 56 | 4 | unsigned | 0-15 | - | Message counter |
| Checksum | 60 | 4 | unsigned | 0-15 | - | CRC checksum |

**Routing**: IVI → Gateway → BCM (CAN-LS)

### IVI_Profile (0x410)
**Purpose**: User profile and scenario management

| Signal | Start Bit | Length | Type | Range | Unit | Description |
|--------|-----------|--------|------|-------|------|-------------|
| Profile_ID | 0 | 8 | enum | 0-5 | - | User profile (DRIVER1-3, GUEST, VALET, CUSTOM) |
| Scenario_ID | 8 | 8 | unsigned | 0-20 | - | Scenario selection |
| Scenario_Params | 16 | 32 | unsigned | 0-4294967295 | - | Scenario parameters |

**Routing**: IVI → Gateway → BCM (CAN-LS)

### BCM_LightControl (0x520)
**Purpose**: Ambient lighting feedback from BCM to IVI

| Signal | Start Bit | Length | Type | Range | Unit | Description |
|--------|-----------|--------|------|-------|------|-------------|
| Headlight_Status | 0 | 2 | enum | 0-3 | - | OFF/PARKING/LOW/HIGH |
| Ambient_Light_Active | 2 | 1 | bool | 0-1 | - | Ambient system active |
| Ambient_R_Actual | 8 | 8 | unsigned | 0-255 | - | Actual red output |
| Ambient_G_Actual | 16 | 8 | unsigned | 0-255 | - | Actual green output |
| Ambient_B_Actual | 24 | 8 | unsigned | 0-255 | - | Actual blue output |

**Routing**: BCM (CAN-LS) → Gateway → IVI, CLU (CAN-HS #2)

## Key Messages (ADAS)

### ASIL-B Messages (20-100ms cycle)
- **LDWS_LKAS11 (0x420)**: LDW_Status_Left/Right, LKA_Event, Lane_Detection_Quality
- **SCC11 (0x421)**: Cruise_Active, Speed_Target, Distance_Target
- **SCC12 (0x422)**: ACC_Status, Brake_Request, Accel_Request
- **LCA11 (0x485)**: Blind_Spot_Left/Right, LCA_Warning

## Network Characteristics

- **Bandwidth**: 500 kbps
- **Message Count**: ~50 messages
- **Priority**: Medium (ADAS) to Low (Infotainment)
- **Latency**: <2ms for ADAS, <5ms for Infotainment
- **Error Detection**: CRC for ASIL-B messages

## Domain Distribution

| Domain | ECU Count | Message Count | ASIL Level |
|--------|-----------|---------------|------------|
| ADAS | 7 | ~25 | B |
| Infotainment | 5 | ~20 | QM |
| Project-Specific | 2 (IVI, BCM) | 3 | QM |

## Gateway Routing

### From CAN-HS #1 to CAN-HS #2
- EMS16 → CLU, HUD (Vehicle_Speed, Engine_RPM)
- ESP12 → IVI (Stability_Status)

### From CAN-HS #2 to CAN-LS
- IVI_AmbientLight → BCM
- IVI_Profile → BCM

### From CAN-LS to CAN-HS #2
- BCM_LightControl → IVI, CLU

## Notes

- Project-specific messages (IVI_AmbientLight, IVI_Profile, BCM_LightControl) enable ambient lighting feature
- ADAS messages (ASIL-B) require CRC and alive counters
- Infotainment messages (QM) have lower priority and longer cycle times

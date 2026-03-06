# Level 2 Domain Architecture - README

## Overview
This directory contains detailed domain-specific architecture diagrams for the vehicle system. Each domain diagram shows ECU internal structure, message flows, and OpenDBC message definitions.

## Domain Diagrams

### 1. Powertrain Domain (`level2_powertrain.puml`)
**ECUs**: 7 ECUs
- EMS (Engine Management System)
- TCU (Transmission Control Unit)
- OPI (Oil Pump Inverter)
- LPI (LPG Injection)
- FPCM (Fuel Pump Control)
- REA (Rear Engine Actuator)
- AAF (Active Air Flap)

**Network**: CAN-HS #1 (500 kbps)
**Key Messages**: EMS16 (Vehicle Speed, RPM, Torque), TCU11 (Gear Position)
**ASIL Level**: B-D

### 2. Chassis Domain (`level2_chassis.puml`)
**ECUs**: 6 ECUs
- ESP (Electronic Stability Program)
- ABS (Anti-lock Braking System)
- MDPS (Motor Driven Power Steering)
- SAS (Steering Angle Sensor)
- EPB (Electronic Parking Brake)
- ECS (Electronic Control Suspension)

**Network**: CAN-HS #1 (500 kbps)
**Key Messages**: ESP12 (Stability Status), ABS11 (Wheel Speed), MDPS12 (Steering Angle)
**ASIL Level**: C-D (Safety-Critical)

### 3. ADAS Domain (`level2_adas.puml`)
**ECUs**: 7 ECUs
- F_CAMERA (Front Camera)
- BSD_RADAR (Blind Spot Detection)
- SCC (Smart Cruise Control)
- SPAS (Smart Parking Assist)
- AVM (Around View Monitor)
- PGS (Parking Guidance System)
- SNV (Surround Night Vision)

**Network**: CAN-HS #2 (500 kbps)
**Key Messages**: LDWS_LKAS11 (Lane Warnings), SCC11 (Cruise Control), LCA11 (Blind Spot)
**ASIL Level**: B

### 4. Infotainment Domain (`level2_infotainment.puml`)
**ECUs**: 5 ECUs
- IVI (In-Vehicle Infotainment)
- CLU (Cluster Unit)
- HUD (Head-Up Display)
- TMU (Telematics Unit)
- CUBIS (Connected User Box)

**Network**: CAN-HS #2 (500 kbps)
**Key Messages**:
- **IVI_AmbientLight (0x400)**: Project-specific ambient lighting control
- **IVI_Profile (0x410)**: User profile management
- CLU11, HUD11, TMU11

**ASIL Level**: QM
**Special Feature**: Ambient lighting integration with BCM via Gateway

### 5. Body Domain (`level2_body.puml`)
**ECUs**: 8 ECUs
- BCM (Body Control Module)
- DATC (Dual Auto Temperature Control)
- FATC (Full Auto Temperature Control)
- AFLS (Adaptive Front Lighting)
- AHLS (Adaptive High-beam Light)
- PSB (Pre-Safe Belt)
- TPMS (Tire Pressure Monitoring)
- SMK (Smart Key)

**Network**: CAN-LS (125 kbps)
**Key Messages**:
- **BCM_LightControl (0x520)**: Ambient lighting feedback
- DATC11, FATC11, TPMS11

**ASIL Level**: QM-B
**Special Feature**: Receives IVI_AmbientLight from Gateway

### 6. Safety Domain (`level2_safety.puml`)
**ECUs**: 2 ECUs
- ACU (Airbag Control Unit)
- ODS (Occupant Detection System)

**Network**: CAN-HS #1 (500 kbps)
**Key Messages**: ACU11 (Airbag Status, Crash Detection), ODS13 (Occupant Classification)
**ASIL Level**: C-D (Highest)
**Crash Detection Timeline**: 0ms (Impact) → 10ms (Severity) → 15ms (Decision) → 20-30ms (Deployment)

### 7. Gateway Architecture (`level2_gateway.puml`)
**ECU**: 1 ECU
- CGW (Central Gateway)

**Networks**: Connects CAN-HS #1, CAN-HS #2, CAN-LS
**Key Functions**:
- Message routing between 3 networks
- Message filtering and validation
- Security gateway (SecOC, firewall)
- Diagnostic gateway (UDS, DoIP)
- Network management

**ASIL Level**: ASIL-C
**Performance**: <1ms routing latency, 1000+ msg/sec throughput

## Routing Examples

### Speed Data Routing
- **Source**: EMS16 (CAN-HS #1)
- **Destination**: CLU, HUD (CAN-HS #2)
- **Signals**: Vehicle_Speed, Engine_RPM

### Ambient Lighting Routing
- **Source**: IVI_AmbientLight (CAN-HS #2)
- **Destination**: BCM (CAN-LS)
- **Signals**: Ambient_Light_RGB, Brightness, Theme_Package

### ADAS Warning Routing
- **Source**: LDWS_LKAS11 (CAN-HS #2)
- **Destination**: IVI, CLU (CAN-HS #2)
- **Signals**: LDW_Status, LKA_Event

## Network Topology

```
CAN-HS #1 (500 kbps)          CAN-HS #2 (500 kbps)          CAN-LS (125 kbps)
├─ Powertrain (7 ECU)         ├─ ADAS (7 ECU)               ├─ Body (8 ECU)
├─ Chassis (6 ECU)            └─ Infotainment (5 ECU)
└─ Safety (2 ECU)
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                    CGW (Gateway)
```

## Message Statistics

| Domain | ECU Count | Message Count | Cycle Time | ASIL Level |
|--------|-----------|---------------|------------|------------|
| Powertrain | 7 | ~15 | 10-500ms | B-D |
| Chassis | 6 | ~12 | 10-100ms | C-D |
| ADAS | 7 | ~20 | 20-100ms | B |
| Infotainment | 5 | ~15 | 100-1000ms | QM |
| Body | 8 | ~15 | 100-1000ms | QM-B |
| Safety | 2 | ~5 | 10-100ms | C-D |
| Gateway | 1 | ~50 routing rules | <1ms | C |

## Files

- `level2_powertrain.puml` / `.png` - Powertrain domain architecture
- `level2_chassis.puml` / `.png` - Chassis domain architecture
- `level2_adas.puml` / `.png` - ADAS domain architecture
- `level2_infotainment.puml` / `.png` - Infotainment domain architecture
- `level2_body.puml` / `.png` - Body domain architecture
- `level2_safety.puml` / `.png` - Safety domain architecture
- `level2_gateway.puml` / `.png` - Gateway architecture
- `README.md` - This file

## Standards Compliance

- **ISO 26262**: ASIL level classification for safety-critical ECUs
- **AUTOSAR**: Domain-based architecture pattern
- **Hyundai/Mobis**: Standard ECU naming convention
- **OpenDBC**: Message and signal definitions from `hyundai_kia_base.dbc`

## Next Steps

Proceed to **Level 3: Communication Architecture** for detailed CAN message specifications and signal definitions.

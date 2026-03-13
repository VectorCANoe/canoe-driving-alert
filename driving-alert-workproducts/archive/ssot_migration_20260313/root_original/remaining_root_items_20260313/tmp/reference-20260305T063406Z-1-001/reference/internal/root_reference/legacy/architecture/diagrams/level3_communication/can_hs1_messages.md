# CAN-HS #1 Message Specification

**Network**: CAN-HS #1 (500 kbps)
**Domains**: Powertrain, Chassis, Safety
**Total Messages**: ~60 messages (estimated)

## Message Table

| Msg ID | Name | Sender | DLC | Signals | Cycle Time | ASIL | Description |
|--------|------|--------|-----|---------|------------|------|-------------|
| 0x030 | EMS18 | EMS | 6 | 8 | 100ms | B-D | Engine status |
| 0x080 | EMS_DCT11 | EMS | 8 | 12 | 20ms | B-D | DCT transmission control |
| 0x081 | EMS_DCT12 | EMS | 8 | 10 | 20ms | B-D | DCT transmission status |
| 0x183 | REA11 | REA | 8 | 6 | 100ms | B | Rear engine actuator |
| 0x18F | EMS_H12 | EMS | 8 | 14 | 50ms | B-D | Engine hybrid control |
| 0x260 | EMS16 | EMS | 8 | 15 | 10ms | D | **Vehicle speed, RPM, torque** |
| 0x280 | EMS13 | EMS | 8 | 12 | 20ms | B-D | Engine control |
| 0x329 | EMS12 | EMS | 8 | 14 | 50ms | B-D | Engine diagnostics |
| 0x316 | EMS11 | EMS | 8 | 16 | 20ms | B-D | Engine management |
| 0x320 | EMS20 | EMS | 6 | 8 | 100ms | B | Engine auxiliary |
| 0x366 | EMS_366 | EMS | 8 | 10 | 100ms | B | Engine extended |
| 0x384 | EMS17 | EMS | 8 | 12 | 50ms | B-D | Engine control 2 |
| 0x38A | WHL_SPD11 | ABS | 8 | 4 | 10ms | D | **Wheel speed (4 wheels)** |
| 0x387 | WHL_PUL11 | ABS | 6 | 4 | 20ms | D | Wheel pulse |
| 0x38A | ABS11 | ABS | 8 | 8 | 10ms | D | **ABS status, brake pressure** |
| 0x2B0 | SAS11 | MDPS | 5 | 2 | 10ms | C | **Steering angle sensor** |
| 0x381 | MDPS11 | MDPS | 8 | 14 | 10ms | C | **Motor driven power steering** |
| 0x383 | FATC11 | DATC | 8 | 16 | 500ms | QM | Climate control |
| 0x393 | TCS12 | ESC | 4 | 6 | 20ms | D | Traction control 2 |
| 0x394 | TCS13 | ESC | 8 | 12 | 20ms | D | Traction control 3 |
| 0x47F | ESP11 | ESC | 6 | 8 | 20ms | D | **ESP status** |
| 0x490 | EPB11 | EPB | 7 | 10 | 100ms | C | Electronic parking brake |
| 0x547 | ACU11 | ACU | 8 | 12 | 10ms | D | **Airbag control, crash detection** |
| 0x548 | ACU12 | ACU | 8 | 10 | 100ms | D | Airbag status |
| 0x549 | PSB11 | PSB | 2 | 2 | 100ms | B | Pre-safe belt |
| 0x557 | EMS15 | EMS | 8 | 14 | 100ms | B | Engine management 15 |
| 0x559 | EMS14 | EMS | 8 | 12 | 100ms | B | Engine management 14 |
| 0x559 | BAT11 | EMS | 8 | 8 | 1000ms | QM | Battery status |
| 0x5A5 | AHLS11 | AHLS | 8 | 6 | 100ms | QM | Adaptive high-beam |
| 0x5A7 | AFLS11 | AFLS | 2 | 2 | 100ms | QM | Adaptive front lighting |
| 0x5C3 | TPMS11 | BCM | 6 | 8 | 1000ms | QM | Tire pressure monitoring |
| 0x5FC | ODS11 | ODS | 8 | 12 | 100ms | C | **Occupant detection 1** |
| 0x5FB | ODS12 | ODS | 8 | 10 | 100ms | C | **Occupant detection 2** |
| 0x5FC | ODS13 | ODS | 5 | 6 | 100ms | C | **Occupant classification** |
| 0x3F9 | ECS12 | ECS | 4 | 6 | 100ms | QM | Electronic control suspension |

## Key Messages (Safety-Critical)

### ASIL-D Messages (10-20ms cycle)
- **EMS16 (0x260)**: Vehicle_Speed, Engine_RPM, Torque
- **ABS11 (0x38A)**: Wheel_Speed_FL/FR/RL/RR, Brake_Pressure
- **ACU11 (0x547)**: Airbag_Status, Crash_Detected, Pretensioner_Status
- **ESP11 (0x47F)**: Stability_Status, TCS_Active, ABS_Active

### ASIL-C Messages (10-20ms cycle)
- **MDPS11 (0x381)**: Steering_Torque, LKAS_Active
- **SAS11 (0x2B0)**: Steering_Angle, Angular_Velocity
- **ODS13 (0x5FC)**: Occupant_Classification, Seat_Occupied
- **EPB11 (0x490)**: Parking_Brake_Status, Auto_Hold_Active

## Network Characteristics

- **Bandwidth**: 500 kbps
- **Message Count**: ~60 messages
- **Priority**: Highest (safety-critical)
- **Latency**: <1ms for ASIL-D messages
- **Error Detection**: CRC, sequence counter

## Domain Distribution

| Domain | ECU Count | Message Count | ASIL Level |
|--------|-----------|---------------|------------|
| Powertrain | 7 | ~20 | B-D |
| Chassis | 6 | ~15 | C-D |
| Safety | 2 | ~8 | C-D |
| Others | - | ~17 | QM-B |

## Notes

- All safety-critical messages (ASIL-D) have 10-20ms cycle times
- Gateway routes selected messages to CAN-HS #2 (CLU, HUD)
- CRC and alive counters required for ASIL-C/D messages

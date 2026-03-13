# Signal Definitions

**Total Signals**: 1325+ signals (from OpenDBC) + 20 project-specific signals
**Standard**: Hyundai/Mobis Signal Naming Convention
**Reference**: `signal_naming_convention.md`

## Key Signal Definitions

### Powertrain Domain

#### EMS16 (0x260) - Engine Management System
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| CR_Vcu_AccPedDep_Pc | 0 | 8 | Little Endian | unsigned | 0 | 100 | 0.4 | 0 | % | Accelerator pedal position |
| CF_Ems_AclAct | 8 | 12 | Little Endian | unsigned | 0 | 3000 | 0.125 | -1600 | Nm | Engine torque actual |
| CF_Ems_EngStat | 20 | 3 | Little Endian | enum | 0 | 7 | 1 | 0 | - | Engine status |
| CR_Vcu_AccPedDep_Pc | 24 | 16 | Little Endian | unsigned | 0 | 300 | 0.01 | 0 | km/h | **Vehicle speed** |
| CR_Ems_EngSpeed | 40 | 16 | Little Endian | unsigned | 0 | 8000 | 0.25 | 0 | rpm | **Engine RPM** |

**Value Tables**:
```
VAL_ 608 CF_Ems_EngStat 0 "OFF" 1 "ACC" 2 "ON" 3 "START" 4 "RUNNING" ;
```

#### TCU11 (0x350) - Transmission Control Unit
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| CF_Tcu_CurGr | 0 | 4 | Little Endian | enum | 0 | 15 | 1 | 0 | - | **Current gear position** |
| CF_Tcu_ShfMode | 4 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | Shift mode (D/S/M) |
| CF_Tcu_OilTemp | 16 | 8 | Little Endian | unsigned | -40 | 215 | 1 | -40 | °C | Transmission oil temp |

**Value Tables**:
```
VAL_ 848 CF_Tcu_CurGr 0 "P" 1 "R" 2 "N" 3 "D" 4 "S" 5 "M1" 6 "M2" 7 "M3" 8 "M4" 9 "M5" 10 "M6" ;
VAL_ 848 CF_Tcu_ShfMode 0 "D" 1 "S" 2 "M" 3 "ECO" ;
```

### Chassis Domain

#### ABS11 (0x38A) - Anti-lock Braking System
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| WHL_SPD_FL | 0 | 14 | Little Endian | unsigned | 0 | 300 | 0.03125 | 0 | km/h | **Wheel speed front left** |
| WHL_SPD_FR | 14 | 14 | Little Endian | unsigned | 0 | 300 | 0.03125 | 0 | km/h | **Wheel speed front right** |
| WHL_SPD_RL | 28 | 14 | Little Endian | unsigned | 0 | 300 | 0.03125 | 0 | km/h | **Wheel speed rear left** |
| WHL_SPD_RR | 42 | 14 | Little Endian | unsigned | 0 | 300 | 0.03125 | 0 | km/h | **Wheel speed rear right** |
| CF_Abs_Stat | 56 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | ABS status |

**Value Tables**:
```
VAL_ 906 CF_Abs_Stat 0 "INACTIVE" 1 "ACTIVE" 2 "FAULT" 3 "RESERVED" ;
```

#### MDPS11 (0x381) - Motor Driven Power Steering
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| CR_Mdps_StrTq | 0 | 12 | Little Endian | signed | -2048 | 2047 | 0.01 | 0 | Nm | **Steering torque** |
| CF_Mdps_Stat | 12 | 4 | Little Endian | enum | 0 | 15 | 1 | 0 | - | MDPS status |
| CF_Lkas_Stat | 16 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | LKAS active status |

#### SAS11 (0x2B0) - Steering Angle Sensor
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| SAS_Angle | 0 | 16 | Little Endian | signed | -2048 | 2047 | 0.1 | 0 | deg | **Steering wheel angle** |
| SAS_Speed | 16 | 8 | Little Endian | unsigned | 0 | 255 | 4 | 0 | deg/s | Steering angular velocity |

### ADAS Domain

#### LDWS_LKAS11 (0x420) - Lane Departure Warning / Lane Keep Assist
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| CF_Lkas_LdwsOpt_USM | 0 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | LDW option setting |
| CF_Lkas_LdwsSysState | 2 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | **LDW system state** |
| CF_Lkas_LdwsLHWarning | 4 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | **LDW left warning** |
| CF_Lkas_LdwsRHWarning | 6 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | **LDW right warning** |
| CF_Lkas_HbaCmd | 8 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | High beam assist command |
| CF_Lkas_FcwOpt_USM | 10 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | FCW option setting |
| CF_Lkas_FcwCollisionWarning | 12 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | **FCW collision warning** |
| CF_Lkas_FusionState | 14 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | Sensor fusion state |

**Value Tables**:
```
VAL_ 1056 CF_Lkas_LdwsSysState 0 "OFF" 1 "STANDBY" 2 "ACTIVE" 3 "FAULT" ;
VAL_ 1056 CF_Lkas_LdwsLHWarning 0 "NONE" 1 "WARNING" 2 "CRITICAL" 3 "RESERVED" ;
VAL_ 1056 CF_Lkas_FcwCollisionWarning 0 "NONE" 1 "WARNING" 2 "CRITICAL" 3 "RESERVED" ;
```

#### SCC11 (0x421) - Smart Cruise Control
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| CF_Scc_Stat | 0 | 3 | Little Endian | enum | 0 | 7 | 1 | 0 | - | **SCC status** |
| CF_Scc_VSetDis | 8 | 8 | Little Endian | unsigned | 0 | 255 | 1 | 0 | km/h | **Target speed** |
| CF_Scc_ObjDist | 16 | 8 | Little Endian | unsigned | 0 | 255 | 1 | 0 | m | **Object distance** |
| CF_Scc_TakeOverReq | 24 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | Takeover request |

**Value Tables**:
```
VAL_ 1057 CF_Scc_Stat 0 "OFF" 1 "STANDBY" 2 "ACTIVE" 3 "OVERRIDE" 4 "FAULT" ;
VAL_ 1057 CF_Scc_TakeOverReq 0 "NONE" 1 "WARNING" 2 "CRITICAL" 3 "EMERGENCY" ;
```

### Safety Domain

#### ACU11 (0x547) - Airbag Control Unit
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| CF_Acu_AirBagStat | 0 | 2 | Little Endian | enum | 0 | 3 | 1 | 0 | - | **Airbag status** |
| CF_Acu_CrashDetected | 2 | 1 | Little Endian | bool | 0 | 1 | 1 | 0 | - | **Crash detected** |
| CF_Acu_PretensionerFL | 3 | 1 | Little Endian | bool | 0 | 1 | 1 | 0 | - | Pretensioner FL deployed |
| CF_Acu_PretensionerFR | 4 | 1 | Little Endian | bool | 0 | 1 | 1 | 0 | - | Pretensioner FR deployed |
| CF_Acu_AirBagFL | 5 | 1 | Little Endian | bool | 0 | 1 | 1 | 0 | - | Airbag FL deployed |
| CF_Acu_AirBagFR | 6 | 1 | Little Endian | bool | 0 | 1 | 1 | 0 | - | Airbag FR deployed |

**Value Tables**:
```
VAL_ 1351 CF_Acu_AirBagStat 0 "NORMAL" 1 "WARNING" 2 "FAULT" 3 "DEPLOYED" ;
```

### Project-Specific Signals ⭐

#### IVI_AmbientLight (0x400)
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| **Ambient_Light_R** | 0 | 8 | Big Endian | unsigned | 0 | 255 | 1 | 0 | - | **Red component (0-255)** |
| **Ambient_Light_G** | 8 | 8 | Big Endian | unsigned | 0 | 255 | 1 | 0 | - | **Green component (0-255)** |
| **Ambient_Light_B** | 16 | 8 | Big Endian | unsigned | 0 | 255 | 1 | 0 | - | **Blue component (0-255)** |
| **Brightness** | 24 | 8 | Big Endian | unsigned | 0 | 100 | 0.4 | 0 | % | **Overall brightness (0-100%)** |
| **Theme_Package** | 32 | 8 | Big Endian | enum | 0 | 10 | 1 | 0 | - | **Theme selection** |
| Reserved | 40 | 16 | Big Endian | unsigned | 0 | 65535 | 1 | 0 | - | Reserved for future use |
| AliveCounter | 56 | 4 | Big Endian | unsigned | 0 | 15 | 1 | 0 | - | Message alive counter |
| Checksum | 60 | 4 | Big Endian | unsigned | 0 | 15 | 1 | 0 | - | CRC checksum |

**Value Tables**:
```
VAL_ 1024 Theme_Package 0 "SPORT" 1 "COMFORT" 2 "ECO" 3 "CUSTOM1" 4 "CUSTOM2" 5 "CUSTOM3" 6 "NIGHT" 7 "PARTY" 8 "RELAX" 9 "DYNAMIC" 10 "USER_DEFINED" ;
```

#### IVI_Profile (0x410)
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| **Profile_ID** | 0 | 8 | Big Endian | enum | 0 | 5 | 1 | 0 | - | **User profile ID** |
| **Scenario_ID** | 8 | 8 | Big Endian | unsigned | 0 | 20 | 1 | 0 | - | **Scenario selection** |
| **Scenario_Params** | 16 | 32 | Big Endian | unsigned | 0 | 4294967295 | 1 | 0 | - | **Scenario parameters** |
| Reserved | 48 | 16 | Big Endian | unsigned | 0 | 65535 | 1 | 0 | - | Reserved for future use |

**Value Tables**:
```
VAL_ 1040 Profile_ID 0 "DRIVER1" 1 "DRIVER2" 2 "DRIVER3" 3 "GUEST" 4 "VALET" 5 "CUSTOM" ;
```

#### BCM_LightControl (0x520)
| Signal Name | Start Bit | Length | Byte Order | Type | Min | Max | Scale | Offset | Unit | Description |
|-------------|-----------|--------|------------|------|-----|-----|-------|--------|------|-------------|
| **Headlight_Status** | 0 | 2 | Big Endian | enum | 0 | 3 | 1 | 0 | - | **Headlight status** |
| **Ambient_Light_Active** | 2 | 1 | Big Endian | bool | 0 | 1 | 1 | 0 | - | **Ambient system active** |
| Reserved1 | 3 | 5 | Big Endian | unsigned | 0 | 31 | 1 | 0 | - | Reserved |
| **Ambient_R_Actual** | 8 | 8 | Big Endian | unsigned | 0 | 255 | 1 | 0 | - | **Actual red output** |
| **Ambient_G_Actual** | 16 | 8 | Big Endian | unsigned | 0 | 255 | 1 | 0 | - | **Actual green output** |
| **Ambient_B_Actual** | 24 | 8 | Big Endian | unsigned | 0 | 255 | 1 | 0 | - | **Actual blue output** |
| Reserved2 | 32 | 32 | Big Endian | unsigned | 0 | 4294967295 | 1 | 0 | - | Reserved |

**Value Tables**:
```
VAL_ 1296 Headlight_Status 0 "OFF" 1 "PARKING" 2 "LOW_BEAM" 3 "HIGH_BEAM" ;
VAL_ 1296 Ambient_Light_Active 0 "INACTIVE" 1 "ACTIVE" ;
```

## Data Type Summary

| Type | Description | Example |
|------|-------------|---------|
| **unsigned** | Unsigned integer | Vehicle_Speed, Engine_RPM |
| **signed** | Signed integer | Steering_Torque, Accel_Request |
| **enum** | Enumeration with value table | Gear_Position, Theme_Package |
| **bool** | Boolean (0/1) | Crash_Detected, Ambient_Light_Active |

## Byte Order

| Byte Order | Description | Usage |
|------------|-------------|-------|
| **Little Endian** | LSB first (Intel format) | Most OpenDBC signals |
| **Big Endian** | MSB first (Motorola format) | Project-specific signals |

## Scaling Formula

```
Physical_Value = (Raw_Value × Scale) + Offset
```

**Example**:
- Signal: Vehicle_Speed
- Raw Value: 12500
- Scale: 0.01
- Offset: 0
- Physical Value: 12500 × 0.01 + 0 = **125 km/h**

## Notes

- All signal names follow Hyundai/Mobis naming convention (see `signal_naming_convention.md`)
- OpenDBC signals use Little Endian byte order
- Project-specific signals use Big Endian byte order
- Total signal count: 1325 (OpenDBC) + 20 (project-specific) = **1345 signals**
- All ASIL-C/D messages require CRC and alive counters

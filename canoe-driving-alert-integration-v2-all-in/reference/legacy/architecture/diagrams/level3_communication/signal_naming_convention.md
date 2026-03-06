# Signal Naming Convention

**Version**: 1.0
**Standard**: Hyundai/Mobis Naming Convention
**Reference**: ISO 11898 (CAN), AUTOSAR Signal Naming

## Naming Rules

### Format
```
<ECU>_<Function>_<Parameter>[_<Index>]
```

### Components
1. **ECU**: 3-5 letter ECU abbreviation (uppercase)
2. **Function**: Functional group (PascalCase or snake_case)
3. **Parameter**: Specific parameter name (PascalCase or snake_case)
4. **Index** (optional): Array index for multiple instances (FL/FR/RL/RR, 1/2/3)

## Examples

### Powertrain Domain
```
EMS_Vehicle_Speed          ✅ (Clear, follows convention)
VehicleSpeed               ❌ (Missing ECU prefix)
EMS_Speed                  ⚠️ (Ambiguous - which speed?)

EMS_Engine_RPM             ✅
EMS_Torque_Actual          ✅
EMS_Gear_Position          ✅
TCU_Shift_Request          ✅
```

### Chassis Domain
```
ABS_Wheel_Speed_FL         ✅ (With index)
ABS_Wheel_Speed_FR         ✅
ABS_Brake_Pressure         ✅
ESP_Stability_Status       ✅
MDPS_Steering_Torque       ✅
MDPS_Steering_Angle        ✅
SAS_Angle_Sensor           ✅
EPB_Parking_Brake_Status   ✅
```

### ADAS Domain
```
LDWS_LDW_Status_Left       ✅
LDWS_LKA_Event             ✅
SCC_Cruise_Active          ✅
SCC_Speed_Target           ✅
LCA_Blind_Spot_Left        ✅
LCA_Blind_Spot_Right       ✅
```

### Infotainment Domain
```
IVI_Ambient_Light_R        ✅ (Project-specific)
IVI_Ambient_Light_G        ✅
IVI_Ambient_Light_B        ✅
IVI_Brightness             ✅
IVI_Theme_Package          ✅
CLU_Display_Mode           ✅
HUD_Speed_Display          ✅
```

### Body Domain
```
BCM_Headlight_Status       ✅
BCM_Ambient_R_Actual       ✅ (Feedback signal)
BCM_Door_Lock_FL           ✅
DATC_Target_Temp           ✅
TPMS_Tire_Pressure_FL      ✅
```

### Safety Domain
```
ACU_Airbag_Status          ✅
ACU_Crash_Detected         ✅
ODS_Occupant_Classification ✅
ODS_Seat_Occupied_FL       ✅
```

## Special Cases

### Array Signals (Multiple Instances)
Use standard automotive suffixes:
- **FL**: Front Left
- **FR**: Front Right
- **RL**: Rear Left
- **RR**: Rear Right
- **1, 2, 3**: Numbered instances

```
ABS_Wheel_Speed_FL         ✅
ABS_Wheel_Speed_FR         ✅
ABS_Wheel_Speed_RL         ✅
ABS_Wheel_Speed_RR         ✅

TPMS_Tire_Pressure_FL      ✅
ODS_Seat_Occupied_1        ✅
```

### Status vs. Actual vs. Request
- **Status**: Current state (read-only)
- **Actual**: Actual measured value (feedback)
- **Request**: Command or setpoint (control)
- **Target**: Desired value (setpoint)

```
EMS_Torque_Status          ✅ (Current state)
EMS_Torque_Actual          ✅ (Measured value)
EMS_Torque_Request         ✅ (Command)
SCC_Speed_Target           ✅ (Desired speed)
```

### Boolean Signals
Use `_Active`, `_Enable`, `_Status` suffixes:

```
SCC_Cruise_Active          ✅ (0=Inactive, 1=Active)
LDWS_LKA_Enable            ✅ (0=Disabled, 1=Enabled)
BCM_Ambient_Light_Active   ✅
ESP_TCS_Active             ✅
```

### Enumeration Signals
Use descriptive names with value tables:

```
EMS_Gear_Position          ✅
  0 = P (Park)
  1 = R (Reverse)
  2 = N (Neutral)
  3 = D (Drive)
  4 = S (Sport)
  5 = M (Manual)

IVI_Theme_Package          ✅
  0 = SPORT
  1 = COMFORT
  2 = ECO
  3 = CUSTOM1
  ...
```

## Reserved Keywords

Avoid using these as signal names (use as suffixes instead):
- `Status`, `Active`, `Enable`, `Request`, `Actual`, `Target`
- `Left`, `Right`, `Front`, `Rear`, `FL`, `FR`, `RL`, `RR`
- `Warning`, `Error`, `Fault`, `Diagnostic`

## Anti-Patterns ❌

```
Speed                      ❌ (No ECU prefix)
EMS_Spd                    ❌ (Abbreviation not standard)
VehicleSpeed               ❌ (No ECU prefix)
EMS16_Speed                ❌ (Message name in signal)
Ambient_R                  ❌ (No ECU prefix)
AmbientLightRed            ❌ (No ECU prefix, inconsistent naming)
```

## Compliance

### ISO 11898 (CAN)
- Signal names must be unique within a message
- Maximum 32 characters recommended
- Use ASCII characters only

### AUTOSAR
- Follow AUTOSAR signal naming convention
- Use PascalCase or snake_case consistently
- Avoid special characters except underscore

### Hyundai/Mobis Standard
- ECU prefix mandatory
- Use standard automotive abbreviations
- Follow domain-specific conventions

## Summary

| Rule | Example | Status |
|------|---------|--------|
| ECU prefix mandatory | `EMS_Vehicle_Speed` | ✅ |
| Function group included | `MDPS_Steering_Torque` | ✅ |
| Array index for multiple | `ABS_Wheel_Speed_FL` | ✅ |
| Descriptive parameter name | `SCC_Cruise_Active` | ✅ |
| Consistent case (PascalCase) | `IVI_Ambient_Light_R` | ✅ |
| No abbreviations | `EMS_Spd` | ❌ |
| No message name in signal | `EMS16_Speed` | ❌ |

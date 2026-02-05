# Ambient Lighting Control Module

## Overview

The Ambient Lighting module provides interior atmosphere lighting control for enhanced user experience. This module manages RGB LED strips and zones throughout the vehicle cabin.

## Features

### Color Control
- **RGB Color Selection**: Full spectrum color control (16.7 million colors)
- **Predefined Themes**: Comfort, Sport, Eco, Romantic, Dynamic
- **Custom Colors**: User-defined color preferences
- **Zone Control**: Independent control of multiple lighting zones

### Lighting Zones
1. **Front Footwell** (Driver & Passenger)
2. **Rear Footwell** (Left & Right)
3. **Door Panels** (All 4 doors)
4. **Dashboard Accent**
5. **Center Console**
6. **Cup Holders**
7. **Door Handles** (Interior)

### Brightness Control
- **10 Brightness Levels**: 10% to 100% in 10% increments
- **Automatic Dimming**: Based on external light sensor
- **Smooth Transitions**: Fade in/out effects (configurable duration)

### Scene Modes

#### Comfort Mode
- Warm white tones (2700K-3000K equivalent)
- Soft amber/orange hues
- Low to medium brightness
- Slow breathing effect

#### Sport Mode
- Dynamic red tones
- High brightness
- Pulsing effect on acceleration
- Synchronized with driving dynamics

#### Eco Mode
- Cool green/blue tones
- Medium brightness
- Static illumination
- Energy-efficient operation

### Vehicle State Integration
- **Welcome Sequence**: Lights activate on door unlock
- **Goodbye Sequence**: Lights fade out on door lock
- **Driving Mode Sync**: Color adapts to selected driving mode
- **Door Open Alert**: Specific zone highlights when door opens
- **Seatbelt Reminder**: Pulsing effect for unbuckled seatbelts

## CAN Interface

### Input Messages
```
AmbientLightControl (0x2A0)
- ColorR [0-255]: Red component
- ColorG [0-255]: Green component
- ColorB [0-255]: Blue component
- Brightness [0-10]: Brightness level
- Mode [0-5]: Scene mode selection
- ZoneMask [8 bits]: Active zones bitmap

VehicleState (0x100)
- DoorStatus [4 bits]: Door open/close status
- IgnitionState [2 bits]: Off/Acc/On/Start
- DrivingMode [3 bits]: Comfort/Sport/Eco/etc
- AmbientLightSensor [0-255]: External light level
```

### Output Messages
```
AmbientLightStatus (0x2A1)
- CurrentMode [0-5]: Active scene mode
- ActualBrightness [0-10]: Current brightness
- FaultStatus [8 bits]: Zone fault indicators
- PowerConsumption [0-100]: Power usage percentage
```

## Implementation Files

### CAPL Scripts
- `ambient_control.can`: Main control logic
- `color_manager.can`: Color calculation and transitions
- `zone_controller.can`: Individual zone management
- `scene_modes.can`: Predefined scene implementations

### Header Files
- `ambient_interface.cin`: CAN message definitions
- `color_definitions.cin`: Color constants and macros
- `zone_mapping.cin`: Zone configuration

## Testing

### Unit Tests
- Color value validation
- Brightness level transitions
- Zone activation/deactivation
- Fault detection

### Integration Tests
- CAN message handling
- Vehicle state synchronization
- Multi-zone coordination
- Power management

## Safety Considerations

- **ASIL QM**: No safety impact (comfort feature)
- **Fault Handling**: Graceful degradation on zone failure
- **Power Limits**: Maximum current draw monitoring
- **Thermal Protection**: Overheat detection and shutdown

## Development Guidelines

1. Use smooth transitions (minimum 500ms fade time)
2. Validate all color values before applying
3. Implement zone independence (one zone failure doesn't affect others)
4. Log all mode changes for diagnostics
5. Respect user preferences (save to EEPROM)

## Future Enhancements

- Music synchronization
- Navigation turn indicators
- Phone call notification
- Ambient sound integration

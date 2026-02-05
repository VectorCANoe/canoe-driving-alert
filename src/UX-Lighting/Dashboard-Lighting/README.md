# Dashboard Lighting Control Module

## Overview

The Dashboard Lighting module controls instrument cluster and center fascia illumination, ensuring optimal visibility and aesthetic appeal. This is a critical UX component affecting driver information readability.

## Features

### Instrument Cluster Lighting
- **Speedometer Illumination**: Adaptive brightness control
- **Tachometer Illumination**: RPM-based dynamic lighting
- **Fuel Gauge Lighting**: Status-based color coding
- **Warning Indicators**: High-visibility alert lighting
- **LCD Backlight**: Adaptive contrast control

### Center Fascia Lighting
- **HVAC Controls**: Button and dial illumination
- **Infotainment Bezel**: Screen surround lighting
- **Storage Compartment**: Interior lighting
- **USB/Power Ports**: Locator lighting
- **Gear Selector**: Position indicator lighting

### Adaptive Brightness
- **10 Manual Levels**: User-adjustable brightness (10%-100%)
- **Auto Mode**: Light sensor-based automatic adjustment
- **Day Mode**: High brightness for sunlight visibility
- **Night Mode**: Reduced brightness to prevent glare
- **Tunnel Detection**: Temporary brightness boost

### Color Themes
- **Classic White**: Traditional warm white (3000K)
- **Cool Blue**: Modern blue-white (5000K)
- **Amber**: Retro amber tone (2200K)
- **Adaptive**: Changes with ambient lighting mode
- **Sport Red**: Performance-oriented red accents

## CAN Interface

### Input Messages
```
DashboardLightControl (0x2B0)
- BrightnessLevel [0-10]: Manual brightness setting
- AutoMode [0-1]: Auto brightness enable
- ColorTheme [0-4]: Theme selection
- DayNightMode [0-1]: Day(0) or Night(1)
- DimmerOverride [0-1]: Temporary dimming

LightSensor (0x150)
- AmbientLight [0-255]: External light level (lux)
- TunnelDetection [0-1]: Tunnel entry/exit

VehicleSpeed (0x110)
- Speed [0-255]: Vehicle speed (km/h)
- EngineRPM [0-8000]: Engine RPM
```

### Output Messages
```
DashboardLightStatus (0x2B1)
- ActualBrightness [0-100]: Current brightness %
- ActiveTheme [0-4]: Current color theme
- FaultCode [0-15]: Fault status
  - 0: No fault
  - 1: Cluster backlight failure
  - 2: Fascia LED failure
  - 3: Light sensor fault
  - 4: Overtemperature
- PowerState [0-1]: On/Off status
```

## Lighting Zones

### Zone 1: Instrument Cluster
- Speedometer ring
- Tachometer ring
- Gauge needles
- LCD backlight
- Warning symbols

### Zone 2: Center Fascia Upper
- HVAC control panel
- Infotainment bezel
- Hazard button
- Climate vents

### Zone 3: Center Fascia Lower
- Gear selector
- Drive mode buttons
- USB ports
- Cup holder lighting

### Zone 4: Steering Wheel
- Button backlighting
- Paddle shifter indicators
- Airbag cover accent

## Adaptive Brightness Algorithm

```
if (AutoMode == 1) {
    if (AmbientLight > 200) {
        // Bright daylight
        TargetBrightness = 100%;
        ColorTemp = 5000K;
    } else if (AmbientLight > 100) {
        // Overcast/Indoor
        TargetBrightness = 70%;
        ColorTemp = 4000K;
    } else if (AmbientLight > 20) {
        // Dusk/Dawn
        TargetBrightness = 40%;
        ColorTemp = 3000K;
    } else {
        // Night
        TargetBrightness = 20%;
        ColorTemp = 2700K;
    }

    // Tunnel boost
    if (TunnelDetection == 1) {
        TargetBrightness += 30%;
    }

    // Smooth transition
    FadeToTarget(TargetBrightness, 1000ms);
}
```

## Implementation Files

### CAPL Scripts
- `dashboard_control.can`: Main control logic
- `brightness_manager.can`: Adaptive brightness algorithm
- `zone_manager.can`: Multi-zone coordination
- `fault_handler.can`: Fault detection and reporting

### Header Files
- `dashboard_interface.cin`: CAN message definitions
- `brightness_tables.cin`: Lookup tables for auto mode
- `zone_config.cin`: Zone configuration and mapping

## Safety Considerations

- **ASIL A**: Driver information visibility is safety-relevant
- **Fault Detection**: Continuous monitoring of all zones
- **Fail-Safe**: Default to medium brightness on sensor fault
- **Warning Priority**: Critical warnings always maximum brightness
- **Glare Prevention**: Maximum brightness limits for night driving

## Testing

### Unit Tests
- Brightness calculation accuracy
- Color theme switching
- Fault detection logic
- Auto mode sensor response

### Integration Tests
- CAN message timing
- Multi-zone synchronization
- Day/night mode transitions
- Tunnel detection response

### Validation Tests
- Visibility testing in various light conditions
- Glare assessment (night driving)
- User preference validation
- Long-term reliability testing

## Development Guidelines

1. **Smooth Transitions**: All brightness changes must fade (minimum 500ms)
2. **Glare Prevention**: Night mode brightness never exceeds 30%
3. **Warning Priority**: Safety warnings override all dimming
4. **Sensor Validation**: Filter sensor noise (moving average, 5 samples)
5. **User Override**: Manual settings always take precedence over auto mode

## Performance Requirements

- **Response Time**: < 100ms from CAN message to brightness change
- **Fade Smoothness**: 60 FPS equivalent (16.6ms update rate)
- **Power Consumption**: < 5W total for all zones
- **Lifespan**: 50,000 hours minimum LED lifetime
- **Temperature Range**: -40°C to +85°C operation

## Future Enhancements

- **Gesture Control**: Brightness adjustment via hand gestures
- **Driver Recognition**: Personalized brightness preferences
- **Attention Monitoring**: Brightness boost when drowsiness detected
- **Navigation Integration**: Turn-by-turn direction indicators

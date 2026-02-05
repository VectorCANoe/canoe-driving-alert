# IVI (In-Vehicle Infotainment) Module

This directory contains the implementation of IVI-based control systems.

## Components

### HVAC (Heating, Ventilation, and Air Conditioning)
- CAPL scripts for HVAC control logic
- Temperature management algorithms
- Climate control simulation

### Window Control
- Power window control algorithms
- Safety mechanisms (anti-pinch)
- Synchronization logic

### Seat Control
- Seat position adjustment logic
- Memory seat functionality
- Heating/ventilation control

## Development Guidelines

1. All CAPL scripts should follow Vector CANoe naming conventions
2. Include comprehensive comments for control logic
3. Test each module independently before integration
4. Document CAN message dependencies

## Testing

Run simulation tests using the configurations in `simulation/test-cases/IVI/`

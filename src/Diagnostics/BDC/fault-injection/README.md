# BDC Fault Injection Module

## Overview

The Fault Injection module systematically introduces faults into the Body Domain Controller (BDC) logic to validate diagnostic capabilities, DTC generation, and fault handling mechanisms. This is critical for ISO 26262 compliance and ASPICE verification activities.

## Purpose

1. **Diagnostic Validation**: Verify UDS diagnostic services correctly detect faults
2. **DTC Generation**: Confirm proper Diagnostic Trouble Code creation
3. **Fault Handling**: Test error recovery and fail-safe mechanisms
4. **Safety Validation**: Ensure safety-critical faults are properly handled
5. **OTA Testing**: Validate fault detection before and after software updates

## Fault Injection Categories

### 1. Communication Faults
- **CAN Bus Errors**
  - Message timeout (missing messages)
  - Message corruption (CRC errors)
  - Bus-off condition
  - Babbling node simulation

- **Network Faults**
  - Partial network failure
  - ECU isolation
  - Message flooding
  - Arbitration errors

### 2. Sensor Faults
- **Light Sensor Failures**
  - Stuck-at-high (always bright)
  - Stuck-at-low (always dark)
  - Intermittent failures
  - Out-of-range values
  - Noise injection

- **Temperature Sensor Faults**
  - Short circuit
  - Open circuit
  - Drift errors
  - Calibration errors

### 3. Actuator Faults
- **LED Driver Failures**
  - Open circuit (LED not illuminating)
  - Short circuit (overcurrent)
  - Partial failure (reduced brightness)
  - Thermal shutdown

- **Motor Control Faults** (Window, Seat)
  - Stall detection
  - Overcurrent
  - Position sensor failure
  - Anti-pinch malfunction

### 4. Software Faults
- **Memory Errors**
  - Stack overflow
  - Heap corruption
  - EEPROM write failure
  - Flash corruption

- **Logic Errors**
  - Watchdog timeout
  - Task overrun
  - Deadlock simulation
  - Race condition injection

### 5. Power Supply Faults
- **Voltage Faults**
  - Undervoltage (< 9V)
  - Overvoltage (> 16V)
  - Voltage ripple
  - Brownout conditions

## Fault Injection Methods

### Method 1: CAN Message Manipulation
```capl
on message AmbientLightControl {
    if (gFaultInjectionActive) {
        switch (gFaultType) {
            case FAULT_MSG_TIMEOUT:
                // Drop message to simulate timeout
                return;

            case FAULT_MSG_CORRUPT:
                // Corrupt data bytes
                this.ColorR = 0xFF;
                this.ColorG = 0xFF;
                this.ColorB = 0xFF;
                break;

            case FAULT_CRC_ERROR:
                // Invalidate CRC
                this.CRC = ~this.CRC;
                break;
        }
    }
    // Normal processing
}
```

### Method 2: Sensor Value Injection
```capl
on timer SensorFaultInjection {
    if (gFaultInjectionActive) {
        message LightSensor msg;

        switch (gFaultType) {
            case FAULT_SENSOR_STUCK_HIGH:
                msg.AmbientLight = 255;
                break;

            case FAULT_SENSOR_STUCK_LOW:
                msg.AmbientLight = 0;
                break;

            case FAULT_SENSOR_NOISE:
                msg.AmbientLight = random(256);
                break;

            case FAULT_SENSOR_OUT_OF_RANGE:
                msg.AmbientLight = 300; // Invalid value
                break;
        }

        output(msg);
    }
}
```

### Method 3: State Machine Corruption
```capl
on key 'f' {
    // Force invalid state transition
    gLightingState = INVALID_STATE;
    write("Fault Injected: Invalid state = %d", gLightingState);
}
```

## Fault Injection Scenarios

### Scenario 1: Ambient Light Sensor Failure
**Objective**: Validate DTC generation for light sensor fault

**Steps**:
1. Start normal operation
2. Inject sensor stuck-at-high fault
3. Wait for fault detection timeout (2 seconds)
4. Verify DTC P0C00 (Ambient Light Sensor Circuit) is set
5. Read DTC via UDS service 0x19
6. Confirm fault lamp illumination
7. Clear fault and verify recovery

**Expected DTCs**:
- `P0C00`: Ambient Light Sensor Circuit
- Status: Confirmed, Test Failed, Warning Indicator Requested

### Scenario 2: Dashboard LED Driver Failure
**Objective**: Validate open circuit detection

**Steps**:
1. Command dashboard lighting to 100% brightness
2. Inject LED open circuit fault (Zone 1)
3. Monitor current feedback
4. Verify DTC B1234 (Dashboard Lighting Circuit Open) is set
5. Verify other zones continue operating (graceful degradation)
6. Test fail-safe mode activation

**Expected DTCs**:
- `B1234`: Dashboard Lighting Circuit Open - Zone 1
- Status: Confirmed, Test Failed

### Scenario 3: CAN Communication Loss
**Objective**: Validate network timeout handling

**Steps**:
1. Establish normal CAN communication
2. Stop sending critical messages (e.g., VehicleState)
3. Wait for timeout (500ms)
4. Verify DTC U0100 (Lost Communication with ECU) is set
5. Verify system enters safe state
6. Restore communication and verify recovery

**Expected DTCs**:
- `U0100`: Lost Communication with ECU
- Status: Confirmed, Test Failed

### Scenario 4: OTA Update Integrity Fault
**Objective**: Validate software update verification

**Steps**:
1. Initiate OTA update process
2. Inject checksum error in update package
3. Verify update is rejected
4. Confirm DTC P0600 (Software Verification Failure) is set
5. Verify system remains on previous software version
6. Test rollback mechanism

**Expected DTCs**:
- `P0600`: Software Verification Failure
- Status: Confirmed, Test Failed

## DTC Mapping

| Fault Type | DTC Code | Description | ASIL |
|------------|----------|-------------|------|
| Ambient Light Sensor | P0C00 | Sensor Circuit Fault | QM |
| Dashboard LED Open | B1234 | LED Circuit Open | A |
| Dashboard LED Short | B1235 | LED Circuit Short | A |
| Light Sensor Range | P0C01 | Sensor Out of Range | QM |
| CAN Timeout | U0100 | Lost Communication | B |
| CAN Bus-Off | U0101 | Bus-Off Condition | B |
| Window Anti-Pinch | B2345 | Anti-Pinch Malfunction | A |
| OTA Checksum | P0600 | Software Verification | B |
| OTA Timeout | P0601 | Update Timeout | B |
| Memory Corruption | P0602 | Memory Fault | B |

## Fault Injection Control

### CAN Control Message
```
FaultInjectionControl (0x7E0)
- FaultEnable [0-1]: Enable/disable fault injection
- FaultType [0-255]: Fault type selector
- FaultParameter [0-65535]: Fault-specific parameter
- Duration [0-65535]: Fault duration (ms), 0 = permanent
- TargetECU [0-15]: Target ECU for fault
```

### CAPL Test Interface
```capl
// Enable fault injection
void EnableFaultInjection(byte faultType, word duration) {
    message FaultInjectionControl msg;
    msg.FaultEnable = 1;
    msg.FaultType = faultType;
    msg.Duration = duration;
    output(msg);
}

// Disable fault injection
void DisableFaultInjection() {
    message FaultInjectionControl msg;
    msg.FaultEnable = 0;
    output(msg);
}
```

## Test Automation

### Automated Test Sequence
```capl
testcase TC_FaultInjection_AmbientSensor() {
    // Setup
    TestWaitForSystemReady();
    ClearAllDTCs();

    // Execute
    write("Injecting ambient light sensor fault...");
    EnableFaultInjection(FAULT_SENSOR_STUCK_HIGH, 5000);

    // Verify
    TestWaitForTime(2500); // Wait for detection

    if (ReadDTC(0xP0C00) == DTC_CONFIRMED) {
        TestStepPass("DTC P0C00 correctly set");
    } else {
        TestStepFail("DTC P0C00 not set");
    }

    // Cleanup
    DisableFaultInjection();
    TestWaitForTime(1000);
    ClearAllDTCs();
}
```

## Safety Considerations

- **ASIL B**: Fault injection testing is safety-relevant
- **Isolation**: Faults must not propagate to other systems
- **Recovery**: All faults must be recoverable
- **Documentation**: All injected faults must be logged
- **Validation**: Fault injection results must be reviewed

## Development Guidelines

1. **Controlled Environment**: Only inject faults in test environment
2. **Logging**: Log all fault injection events with timestamps
3. **Reproducibility**: Ensure faults are reproducible
4. **Safety**: Never inject faults that could cause physical damage
5. **Documentation**: Document expected vs. actual behavior

## Fault Injection Tools

- **CANoe CAPL**: Primary fault injection mechanism
- **vVIRTUALtarget**: Software-level fault injection
- **Fault Injection Panel**: GUI for manual fault control
- **Automated Test Scripts**: Systematic fault injection sequences

## References

- ISO 26262-6: Software level fault injection
- ISO 26262-8: Supporting processes for fault injection
- ASPICE SWE.6: Software qualification test
- Vector CANoe Fault Injection Guide

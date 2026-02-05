# OTA (Over-The-Air) Update Module

## Overview

The OTA Update module implements virtual software reprogramming using Vector's vVIRTUALtarget platform. This module handles secure software updates, integrity verification, and rollback mechanisms for the BDC and lighting control systems.

## Purpose

1. **Remote Updates**: Enable software updates without physical access
2. **Security**: Ensure update authenticity and integrity
3. **Reliability**: Guarantee safe update process with rollback capability
4. **Validation**: Verify updated software functionality
5. **Compliance**: Meet ISO 26262 and cybersecurity requirements

## OTA Update Process

### Phase 1: Update Notification
```
1. Backend Server → Vehicle: Update available notification
2. Vehicle → User: Display update prompt (IVI screen)
3. User: Accept or schedule update
4. Vehicle → Server: Acknowledge update request
```

### Phase 2: Download
```
1. Server → Vehicle: Send update package metadata
2. Vehicle: Validate metadata (signature, version, compatibility)
3. Server → Vehicle: Stream update package chunks
4. Vehicle: Verify each chunk (checksum)
5. Vehicle: Assemble complete package
6. Vehicle: Verify complete package (SHA-256 hash)
```

### Phase 3: Installation
```
1. Vehicle: Check preconditions (battery, parking, etc.)
2. Vehicle: Create backup of current software
3. Vehicle: Enter update mode (disable non-critical functions)
4. Vehicle: Flash new software to vECU
5. Vehicle: Verify flash operation
6. Vehicle: Update configuration data
```

### Phase 4: Validation
```
1. Vehicle: Reboot with new software
2. Vehicle: Run self-tests (POST - Power-On Self-Test)
3. Vehicle: Verify critical functions
4. Vehicle: Compare version numbers
5. Vehicle: Report update status to server
```

### Phase 5: Rollback (if needed)
```
1. Vehicle: Detect update failure
2. Vehicle: Restore backup software
3. Vehicle: Reboot with previous version
4. Vehicle: Report rollback to server
5. Vehicle: Set DTC for failed update
```

## Update Package Structure

```
OTA_Package_v2.1.0.bin
├── Header (256 bytes)
│   ├── Magic Number (4 bytes): 0x4F544155 ("OTAU")
│   ├── Version (16 bytes): "2.1.0"
│   ├── Target ECU (16 bytes): "BDC_IVI_LIGHTING"
│   ├── Package Size (4 bytes): Total size in bytes
│   ├── Checksum (32 bytes): SHA-256 hash
│   ├── Signature (128 bytes): RSA-2048 signature
│   └── Timestamp (8 bytes): Unix timestamp
├── Metadata (variable)
│   ├── Release Notes
│   ├── Compatibility Matrix
│   ├── Preconditions
│   └── Post-Update Actions
├── Software Binary (variable)
│   ├── Application Code
│   ├── Configuration Data
│   └── Calibration Parameters
└── Footer (64 bytes)
    ├── CRC-32 (4 bytes)
    └── End Marker (4 bytes): 0x454E4421 ("END!")
```

## CAN Interface

### Update Control Messages

```
OTA_UpdateControl (0x7E5)
- Command [0-255]: Update command
  - 0x01: Check for updates
  - 0x02: Download update
  - 0x03: Install update
  - 0x04: Abort update
  - 0x05: Rollback
- Parameter [0-65535]: Command-specific parameter
- Sequence [0-255]: Message sequence number

OTA_UpdateStatus (0x7E6)
- State [0-15]: Current update state
  - 0: Idle
  - 1: Checking for updates
  - 2: Downloading
  - 3: Download complete
  - 4: Installing
  - 5: Validating
  - 6: Complete
  - 7: Failed
  - 8: Rolling back
- Progress [0-100]: Update progress percentage
- ErrorCode [0-255]: Error code if failed
- CurrentVersion [32 bytes]: Current software version
- TargetVersion [32 bytes]: Target software version
```

### Download Progress Messages

```
OTA_DownloadProgress (0x7E7)
- ChunkNumber [0-65535]: Current chunk number
- TotalChunks [0-65535]: Total number of chunks
- ChunkSize [0-65535]: Size of current chunk
- ChunkChecksum [0-4294967295]: CRC-32 of chunk
- BytesReceived [0-4294967295]: Total bytes received
- BytesTotal [0-4294967295]: Total package size
```

## Security Features

### 1. Authentication
- **RSA-2048 Signature**: Verify update package authenticity
- **Certificate Chain**: Validate signing authority
- **Timestamp Validation**: Prevent replay attacks

### 2. Integrity
- **SHA-256 Hash**: Verify complete package integrity
- **CRC-32 Chunks**: Verify individual chunk integrity
- **Flash Verification**: Read-back verification after programming

### 3. Authorization
- **ECU Compatibility**: Verify update is for correct ECU
- **Version Check**: Prevent downgrade attacks
- **Feature Flags**: Enable/disable OTA based on vehicle configuration

### 4. Secure Boot
- **Boot Loader Verification**: Verify boot loader integrity
- **Application Verification**: Verify application before execution
- **Rollback Protection**: Prevent rollback to vulnerable versions

## Preconditions for Update

### Vehicle State Requirements
```capl
bool CheckUpdatePreconditions() {
    // Battery voltage
    if (GetBatteryVoltage() < 12.0) {
        SetErrorCode(ERR_LOW_BATTERY);
        return false;
    }

    // Vehicle must be parked
    if (GetVehicleSpeed() > 0) {
        SetErrorCode(ERR_VEHICLE_MOVING);
        return false;
    }

    // Ignition must be ON
    if (GetIgnitionState() != IGN_ON) {
        SetErrorCode(ERR_IGNITION_OFF);
        return false;
    }

    // No critical DTCs
    if (HasCriticalDTCs()) {
        SetErrorCode(ERR_CRITICAL_FAULT);
        return false;
    }

    // Sufficient storage space
    if (GetFreeFlashSpace() < GetUpdateSize()) {
        SetErrorCode(ERR_INSUFFICIENT_SPACE);
        return false;
    }

    return true;
}
```

## Update State Machine

```
[IDLE]
  ↓ (Update Available)
[CHECKING]
  ↓ (Update Confirmed)
[DOWNLOADING]
  ↓ (Download Complete)
[VERIFYING]
  ↓ (Verification OK)
[READY_TO_INSTALL]
  ↓ (User Confirms)
[INSTALLING]
  ↓ (Installation Complete)
[VALIDATING]
  ↓ (Validation OK)
[COMPLETE]

Error Paths:
[DOWNLOADING] → [FAILED] → [IDLE]
[INSTALLING] → [FAILED] → [ROLLING_BACK] → [IDLE]
[VALIDATING] → [FAILED] → [ROLLING_BACK] → [IDLE]
```

## Implementation Files

### CAPL Scripts
- `ota_manager.can`: Main OTA control logic
- `download_handler.can`: Package download management
- `flash_programmer.can`: vVIRTUALtarget flash interface
- `security_validator.can`: Signature and hash verification
- `rollback_manager.can`: Backup and rollback logic

### Header Files
- `ota_interface.cin`: CAN message definitions
- `security_defs.cin`: Cryptographic constants
- `version_info.cin`: Version management

### Update Packages
- `update-packages/`: Directory for OTA update binaries
  - `BDC_v2.0.0_to_v2.1.0.bin`
  - `Lighting_v1.5.0_to_v1.6.0.bin`
  - `IVI_v3.2.0_to_v3.3.0.bin`

## Testing Scenarios

### Test Case 1: Successful Update
**Objective**: Validate complete OTA update process

**Steps**:
1. Prepare update package with valid signature
2. Initiate update download
3. Verify download progress (0% → 100%)
4. Verify package integrity (SHA-256)
5. Install update to vVIRTUALtarget
6. Reboot and validate new version
7. Verify all functions operational
8. Confirm update status reported to server

**Expected Result**: Update completes successfully, version updated

### Test Case 2: Corrupted Package
**Objective**: Validate integrity checking

**Steps**:
1. Prepare update package with invalid checksum
2. Initiate update download
3. Download completes
4. Integrity verification fails
5. Verify DTC P0600 (Software Verification Failure) is set
6. Verify system remains on current version
7. Verify error reported to server

**Expected Result**: Update rejected, DTC set, no version change

### Test Case 3: Installation Failure with Rollback
**Objective**: Validate rollback mechanism

**Steps**:
1. Prepare valid update package
2. Download and verify package
3. Begin installation
4. Inject flash programming error
5. Installation fails
6. Automatic rollback initiated
7. Previous version restored
8. System reboots with original software
9. Verify DTC P0601 (Update Timeout) is set

**Expected Result**: Rollback successful, original version restored

### Test Case 4: Precondition Violation
**Objective**: Validate precondition checking

**Steps**:
1. Prepare valid update package
2. Set vehicle speed > 0 km/h
3. Attempt to initiate update
4. Verify update is rejected
5. Verify error code ERR_VEHICLE_MOVING
6. Stop vehicle (speed = 0)
7. Retry update initiation
8. Verify update proceeds

**Expected Result**: Update blocked when moving, allowed when stopped

## Fault Injection for OTA

### Fault Scenarios
1. **Network Interruption**: Simulate connection loss during download
2. **Checksum Mismatch**: Corrupt package during download
3. **Flash Error**: Simulate flash programming failure
4. **Power Loss**: Simulate battery disconnect during update
5. **Signature Invalid**: Inject invalid RSA signature

### Expected Behavior
- Network interruption → Resume download from last chunk
- Checksum mismatch → Reject package, set DTC
- Flash error → Rollback to previous version
- Power loss → Resume or rollback on next power-up
- Invalid signature → Reject package immediately

## Performance Requirements

- **Download Speed**: Minimum 100 kB/s over CAN
- **Installation Time**: < 5 minutes for typical update
- **Rollback Time**: < 2 minutes
- **Verification Time**: < 30 seconds
- **Total Update Time**: < 10 minutes (download + install + validate)

## Safety Considerations

- **ASIL B**: OTA updates affect safety-critical functions
- **Fail-Safe**: Always maintain ability to rollback
- **Validation**: Comprehensive POST after update
- **Monitoring**: Continuous health monitoring post-update
- **Logging**: Complete audit trail of all update activities

## Development Guidelines

1. **Always Verify**: Check signature and hash before installation
2. **Always Backup**: Create backup before any flash operation
3. **Atomic Updates**: Update completes fully or rolls back fully
4. **User Notification**: Keep user informed of update progress
5. **Error Handling**: Graceful handling of all error conditions
6. **Logging**: Log all update events for diagnostics

## vVIRTUALtarget Integration

### Flash Programming Interface
```capl
// Program flash memory
int ProgramFlash(byte[] data, dword address, dword size) {
    // vVIRTUALtarget flash programming API
    return vVT_FlashProgram(address, data, size);
}

// Verify flash memory
int VerifyFlash(byte[] expected, dword address, dword size) {
    byte[] actual;
    vVT_FlashRead(address, actual, size);
    return memcmp(expected, actual, size);
}

// Erase flash sector
int EraseFlashSector(dword address) {
    return vVT_FlashErase(address);
}
```

## Future Enhancements

- **Delta Updates**: Only download changed portions
- **Compression**: Reduce package size with compression
- **Multi-ECU Updates**: Coordinate updates across multiple ECUs
- **A/B Partitioning**: Dual-bank flash for seamless updates
- **Predictive Updates**: AI-based update scheduling

## References

- ISO 26262-6: Software updates and modifications
- ISO/SAE 21434: Cybersecurity for road vehicles
- UDS ISO 14229: Diagnostic services for reprogramming
- Vector vVIRTUALtarget Documentation
- AUTOSAR Secure Onboard Communication (SecOC)

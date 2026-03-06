# Contributing to canoe-driving-alert

Thank you for your interest in contributing to the canoe-driving-alert project! This document provides guidelines for contributing to this Hyundai Mobis Bootcamp project in collaboration with Vector Korea.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Documentation](#documentation)
7. [Commit Guidelines](#commit-guidelines)
8. [Pull Request Process](#pull-request-process)
9. [Review Process](#review-process)

---

## Code of Conduct

This project adheres to professional automotive industry standards. All contributors are expected to:

- Respect ISO 26262 and ASPICE processes
- Follow Vector CANoe best practices
- Maintain professional communication
- Prioritize safety and quality
- Collaborate constructively

---

## Getting Started

### Prerequisites

- **Vector CANoe** (Version 17+ recommended)
- **Git** for version control
- Understanding of **CAN / CAN-FD / DoIP** protocols
- Familiarity with **CAPL** programming
- Knowledge of automotive diagnostics (**UDS ISO 14229**)

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/VectorCANoe/canoe-driving-alert.git
   cd canoe-driving-alert
   ```

2. Open the CANoe configuration:
   - `canoe/cfg/IVI_OTA_Project.cfg`

3. Load the DBC database:
   - `canoe/databases/vehicle_system.dbc`

---

## Development Process

### Workflow

1. **Planning**: Review SRS (REQ-F/G/D/O/A/N) and HARA documents.
2. **Implementation**: Develop CAPL nodes in `canoe/nodes/`.
3. **Verification**: Run CANoe simulation and verify DTC generation.
4. **Validation**: Execute E2E scenario (Fault -> Diagnostics -> OTA).

### Branch Strategy

```
main (Stable — Production/Mentor Submission)
├── develop (Integration branch)
│   ├── feature/bcm-fault-sim      (Window Motor Fault logic)
│   ├── feature/cgw-routing         (CAN-LS to HS2/HS1 routing)
│   ├── feature/uds-diagnostic     (Tester node development)
│   └── feature/ota-rollback       (OTA safety mechanism)
└── hotfix/critical-signal-fix
```

### Branch Naming Convention

- `feature/xxx`: New signal/node implementation
- `bugfix/xxx`: Fix for existing CAPL/DBC errors
- `docs/xxx`: Documentation updates (V-Model, Guides)
- `test/xxx`: Test script/module improvements

---

## Coding Standards

### CAPL (Communication Access Programming Language)

#### Naming Conventions

```capl
// Global variables: g prefix + CamelCase
int gIsDiagnosticActive = 0;
float gMotorCurrentValue = 0.0;

// Constants: ALL_CAPS with underscores
const int MOTOR_THRESHOLD_AMPS = 50;
const int DTC_WINDOW_OVERCURRENT = 0xB1234;

// Message variables: message + Name (from DBC)
message BCM_FaultStatus mFaultMsg;

// Functions: CamelCase, start with Verb
void SendDiagnosticResponse(byte sid) { ... }
```

#### Documentation Standard

Every CAPL node must have a header:

```capl
/*
 * Node: BCM_Sim.can
 * Requirement: REQ-F01, REQ-N01
 * ASIL: B
 * Description: Simulates window motor overcurrent and generates DTC B1234.
 */
```

---

## Testing Requirements

We use the V-Model approach for testing:

1. **Unit Test (SWE.4)**: Individual CAPL node logic verification.
2. **Integration Test (SWE.5)**: Routing latency between nodes (≤ 5ms).
3. **System Test (SYS.5)**: Complete E2E Scenario verify (Fault to OTA).

---

## Commit Guidelines

Follow the Conventional Commits format:

`type(scope): subject`

- **feat**: New feature (e.g., `feat(cgw): add DoIP bridge`)
- **fix**: Bug fix (e.g., `fix(dbc): correct 0x500 cycle time`)
- **docs**: Documentation only
- **test**: Adding or correcting tests

---

## Pull Request Process

1. Create a branch from `develop`.
2. Ensure CAPL code compiles without errors/warnings.
3. Update relevant documentation (e.g., `CHANGELOG.md`).
4. Submit PR to `develop` for review.
5. Once approved, merge using Squash and Merge.

---

## Review Process

All code and documentation must undergo peer review focusing on:
- **ASIL Compliance**: Safety mechanisms correctly implemented.
- **Protocol Adherence**: UDS/CAN timing within requirements.
- **Traceability**: All changes linked to a Requirement ID.

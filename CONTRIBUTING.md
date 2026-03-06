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
- Understanding of **CAN / Ethernet(UDP)** communication
- Familiarity with **CAPL** programming
- **Python 3.11+** for local gate scripts

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/VectorCANoe/canoe-driving-alert.git
   cd canoe-driving-alert
   ```

2. Open the CANoe configuration:
   - `canoe/cfg/CAN_v2_topology_wip.cfg` (active working profile)

3. Load split DBC set:
   - `canoe/databases/chassis_can.dbc`
   - `canoe/databases/powertrain_can.dbc`
   - `canoe/databases/body_can.dbc`
   - `canoe/databases/infotainment_can.dbc`
   - `canoe/databases/adas_can.dbc`
   - `canoe/databases/eth_backbone_can_stub.dbc`

---

## Development Process

### Workflow

1. **Planning**: Review `AGENTS.md` and `driving-situation-alert/TMP_HANDOFF.md` (`FRESH/STALE` policy).
2. **Implementation**: Update CAPL in `canoe/src/capl/` and keep `canoe/cfg/channel_assign/` synchronized.
3. **Verification**: Run local gates (`cfg-hygiene`, `capl-sync`, and relevant `doc-sync`/`cli-readiness`).
4. **Validation**: Execute CANoe SIL UT/IT/ST chain and update evidence/docs as needed.

### Branch Strategy

```
main (protected baseline)
├── feature/<topic>
├── bugfix/<topic>
├── docs/<topic>
└── hotfix/<topic>
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

Minimum local gate checks before PR:

- `python scripts/run.py gate cfg-hygiene`
- `python scripts/run.py gate capl-sync`
- `python scripts/run.py gate doc-sync` (when doc/trace chain changes)
- `python scripts/run.py gate cli-readiness` (when CLI/scripts packaging changes)

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

1. Create a branch from `main`.
2. Ensure CAPL code compiles without errors/warnings.
3. Run required local gates and confirm PASS.
4. Keep `canoe/src/capl` and `canoe/cfg/channel_assign` synchronized.
5. Update relevant documentation (e.g., trace chain docs, operation notes) when scope requires.
6. Submit PR to `main` for review.
7. Once approved, merge using Squash and Merge.

---

## Review Process

All code and documentation must undergo peer review focusing on:
- **ASIL Compliance**: Safety mechanisms correctly implemented.
- **Protocol Adherence**: UDS/CAN timing within requirements.
- **Traceability**: All changes linked to a Requirement ID.

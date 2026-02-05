# Contributing to CANoe-IVI-OTA

Thank you for your interest in contributing to the CANoe-IVI-OTA project! This document provides guidelines for contributing to this Hyundai Mobis Bootcamp project in collaboration with Vector Korea.

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

## Code of Conduct

This project adheres to professional automotive industry standards. All contributors are expected to:

- Respect ISO 26262 and ASPICE processes
- Follow Vector CANoe best practices
- Maintain professional communication
- Prioritize safety and quality
- Collaborate constructively

## Getting Started

### Prerequisites

- Vector CANoe (with vVIRTUALtarget license)
- Git for version control
- Understanding of CAN protocol
- Familiarity with CAPL programming
- Knowledge of automotive diagnostics (UDS)

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/VectorCANoe/CANoe-IVI-OTA.git
   cd CANoe-IVI-OTA
   ```

2. Review project structure and documentation

3. Set up CANoe with project configurations

4. Review safety and requirements documentation

## Development Process

### Workflow

1. **Planning**: Review requirements and create design documents
2. **Implementation**: Develop CAPL scripts and configurations
3. **Testing**: Execute unit and integration tests
4. **Review**: Peer review of code and documentation
5. **Integration**: Merge approved changes
6. **Validation**: System-level validation

### Branch Strategy

```
main (production-ready code)
├── develop (integration branch)
│   ├── feature/ambient-lighting-zones
│   ├── feature/dashboard-adaptive-brightness
│   ├── feature/fault-injection-scenarios
│   └── feature/ota-security-enhancement
└── hotfix/critical-bug-fix
```

### Branch Naming Convention

- `feature/short-description`: New features
- `bugfix/issue-number-description`: Bug fixes
- `hotfix/critical-issue`: Critical production fixes
- `docs/documentation-update`: Documentation only
- `test/test-improvement`: Test enhancements

## Coding Standards

### CAPL Coding Standards

#### Naming Conventions

```capl
// Global variables: g prefix, CamelCase
int gAmbientLightBrightness;
float gDashboardBrightnessLevel;

// Constants: ALL_CAPS with underscores
const int MAX_BRIGHTNESS = 100;
const int MIN_BRIGHTNESS = 0;

// Functions: CamelCase, descriptive names
void SetAmbientLightColor(byte red, byte green, byte blue) {
    // Implementation
}

// Message handlers: on message MessageName
on message AmbientLightControl {
    // Handler implementation
}
```

#### Code Structure

```capl
// File header with description
/*
 * Module: Ambient Lighting Control
 * Description: RGB ambient lighting zone management
 * Author: [Name]
 * Date: 2026-02-05
 * Version: 1.0.0
 * ASIL: QM
 */

// Includes
#include "ambient_interface.cin"
#include "color_definitions.cin"

// Constants
const int ZONE_COUNT = 8;
const int FADE_DURATION_MS = 500;

// Global variables
int gCurrentBrightness = 50;
byte gColorR = 255, gColorG = 255, gColorB = 255;

// Function declarations
void InitializeAmbientLighting();
void SetZoneColor(int zone, byte r, byte g, byte b);
void FadeToColor(byte targetR, byte targetG, byte targetB, int duration);

// Event handlers
on start {
    InitializeAmbientLighting();
}

// Function implementations
void InitializeAmbientLighting() {
    write("Initializing ambient lighting system...");
    // Implementation
}
```

#### Comments

```capl
// Single-line comments for brief explanations

/*
 * Multi-line comments for:
 * - Function descriptions
 * - Complex algorithm explanations
 * - Safety-critical notes
 */

// TODO: Implement color temperature adjustment
// FIXME: Brightness transition not smooth
// SAFETY: This function affects ASIL B component
// NOTE: Requires CAN message 0x2A0 to be active
```

### Code Quality Requirements

- **No Magic Numbers**: Use named constants
- **Error Handling**: Check all return values
- **Logging**: Log important events and errors
- **Modularity**: Keep functions focused and small (< 50 lines)
- **Testability**: Write testable code with clear interfaces

## Testing Requirements

### Unit Testing

Every CAPL module must have corresponding unit tests:

```capl
testcase TC_AmbientLight_SetColor() {
    // Arrange
    byte testR = 255, testG = 128, testB = 64;

    // Act
    SetAmbientLightColor(testR, testG, testB);

    // Assert
    if (gColorR == testR && gColorG == testG && gColorB == testB) {
        TestStepPass("Color set correctly");
    } else {
        TestStepFail("Color mismatch");
    }
}
```

### Integration Testing

Test CAN communication and multi-module interaction:

```capl
testcase TC_Integration_DashboardLighting() {
    // Test dashboard lighting responds to light sensor
    message LightSensor msg;
    msg.AmbientLight = 255; // Bright daylight
    output(msg);

    TestWaitForTime(200); // Wait for processing

    // Verify dashboard brightness increased
    // ...
}
```

### Test Coverage Requirements

- **Unit Tests**: Minimum 80% code coverage
- **Integration Tests**: All CAN message interactions
- **System Tests**: All use cases and scenarios
- **Safety Tests**: 100% coverage of ASIL A/B functions

## Documentation

### Required Documentation

For every new feature or module:

1. **README.md**: Module overview and usage
2. **Requirements**: Link to requirements document
3. **Design**: Architecture and detailed design
4. **Test Plan**: Test strategy and cases
5. **User Guide**: How to use the feature

### Documentation Standards

- Use Markdown for all documentation
- Include diagrams for complex concepts
- Provide code examples
- Link to related documents
- Keep documentation up-to-date with code

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(ambient): Add 8-zone RGB control

Implemented independent control for 8 ambient lighting zones
with smooth color transitions and scene modes.

Closes #123
```

```
fix(dashboard): Correct brightness calculation in auto mode

Fixed adaptive brightness algorithm to properly handle
tunnel detection and prevent sudden brightness jumps.

Fixes #456
ASIL: A
```

### Commit Best Practices

- One logical change per commit
- Write clear, descriptive messages
- Reference issue numbers
- Include ASIL level for safety-related changes

## Pull Request Process

### Before Creating a PR

1. ✅ All tests pass
2. ✅ Code follows coding standards
3. ✅ Documentation is updated
4. ✅ Commit messages are clear
5. ✅ No merge conflicts with target branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Safety Impact
- ASIL Level: [QM/A/B/C/D]
- Safety Impact: [None/Low/Medium/High]

## Checklist
- [ ] Code follows project standards
- [ ] Documentation updated
- [ ] Reviewed by peer
- [ ] Ready for merge
```

## Review Process

### Code Review Checklist

Reviewers should verify:

- ✅ **Functionality**: Code works as intended
- ✅ **Standards**: Follows coding standards
- ✅ **Safety**: Safety requirements met
- ✅ **Testing**: Adequate test coverage
- ✅ **Documentation**: Complete and accurate
- ✅ **Performance**: No performance regressions
- ✅ **Security**: No security vulnerabilities

### Review Timeline

- **Initial Review**: Within 2 business days
- **Follow-up**: Within 1 business day
- **Approval**: Requires 2 approvals for safety-critical code

### Addressing Review Comments

- Respond to all comments
- Make requested changes or provide rationale
- Re-request review after changes
- Be professional and constructive

## Questions or Issues?

- Create an issue on GitHub
- Contact project maintainers
- Refer to Vector CANoe documentation
- Review ISO 26262 and ASPICE guidelines

---

**Thank you for contributing to CANoe-IVI-OTA!**

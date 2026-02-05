# Safety Management

This directory contains all ISO 26262 functional safety management artifacts for the CANoe-IVI-OTA project.

## Overview

ISO 26262 is the international standard for functional safety of electrical and electronic systems in road vehicles. This directory structure supports the complete safety lifecycle from concept through production.

## Directory Structure

### safety-plan/
Contains the overall safety management documentation:
- **project-safety-plan.md**: Master safety plan defining safety activities, responsibilities, and schedules
- **safety-case.md**: Argumentation that safety goals are achieved
- **functional-safety-concept.md**: High-level safety requirements and architecture

### hazard-analysis/
HARA (Hazard Analysis and Risk Assessment) artifacts:
- **hazard-identification.xlsx**: Identified hazards and operational situations
- **risk-assessment.xlsx**: Severity, exposure, and controllability analysis
- **ASIL-determination.xlsx**: ASIL (A, B, C, D, or QM) assignment for each hazard

### safety-requirements/
Safety requirements derived from HARA:
- **functional-safety-requirements.xlsx**: High-level safety goals
- **technical-safety-requirements.xlsx**: Detailed technical safety requirements
- **safety-goals.md**: Documented safety goals for the system

### fmea/
Failure Mode and Effects Analysis:
- **system-fmea.xlsx**: System-level FMEA
- **hardware-fmea.xlsx**: Hardware component FMEA
- **software-fmea.xlsx**: Software FMEA for critical functions

### fta/
Fault Tree Analysis for systematic failure analysis:
- **fault-trees/**: FTA diagrams and analysis

### safety-validation/
Safety validation activities and reports:
- **validation-plan.md**: Plan for safety validation
- **validation-reports/**: Safety validation test results

### safety-reviews/
Safety review records:
- **safety-review-plan.md**: Schedule and scope of safety reviews
- **review-records/**: Minutes and outcomes of safety reviews

## ASIL Levels

Our project focuses on the following ASIL classifications:

| Component | ASIL Level | Rationale |
|-----------|------------|-----------|
| IVI HVAC Control | QM | Comfort function, no safety impact |
| Window Control | ASIL A | Minor injury risk (anti-pinch) |
| Ambient Lighting | QM | UX feature, no safety impact |
| Dashboard Lighting | ASIL A | Driver information visibility |
| ADAS Lighting Integration | ASIL B | Safety-related driver alerts |
| BDC Diagnostics | ASIL B | Safety monitoring function |
| OTA Update | ASIL B | Software integrity critical |

## Key Safety Goals

1. **SG-01**: The system shall prevent unintended window closure causing injury (ASIL A)
2. **SG-02**: Dashboard lighting shall ensure critical information visibility (ASIL A)
3. **SG-03**: ADAS lighting alerts shall be timely and distinguishable (ASIL B)
4. **SG-04**: Diagnostic system shall detect and report safety-critical faults (ASIL B)
5. **SG-05**: OTA updates shall not compromise vehicle safety functions (ASIL B)

## Safety Lifecycle Process

```
1. Concept Phase → HARA → Safety Goals
2. System Development → Safety Requirements → Architecture
3. Software Development → Detailed Design → Implementation
4. Verification → Unit/Integration/System Testing
5. Validation → Safety Validation → Release
```

## Compliance

This structure supports ISO 26262:2018 compliance:
- Part 2: Management of functional safety
- Part 3: Concept phase
- Part 4: Product development at the system level
- Part 6: Product development at the software level
- Part 8: Supporting processes

## References

- ISO 26262:2018 - Road vehicles — Functional safety
- Vector CANoe Safety Manual
- Hyundai Mobis Safety Standards

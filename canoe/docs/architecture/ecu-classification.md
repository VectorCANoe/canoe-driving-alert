# ECU Classification

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the practical ECU role classification for the active CANoe SIL baseline.

The classification is used to make four things explicit:

- who owns a runtime decision
- who owns cross-domain boundary behavior
- which surfaces exist only for local feature behavior or presentation
- which surfaces are validation-only and must stay outside product ownership

This is a runtime architecture document.
It is not a vehicle-program inventory document and it is not a GUI regrouping guide.

## Why this classification is used

The project needs a stable way to answer questions such as:

- Is this node a product owner or a validation harness?
- Should this node own a contract or only consume it?
- Should timeout and route authority stay local or move to a boundary surface?
- Is this node part of the product runtime or only part of the verification system?

Without a role-based classification, owner, route, timeout, and oracle decisions drift into file-by-file exceptions.

## Role classes

The current baseline uses four role classes.

| Role class | Meaning | Typical examples |
| --- | --- | --- |
| Gateway / Backbone | cross-domain boundary, routing, backbone health, service edge | `CGW`, `SGW`, `DCM`, `IBOX`, `ETHB` |
| Domain Runtime Owner | primary owner of domain state and major runtime decisions | `VCU`, `MDPS`, `BCM`, `IVI`, `CLU`, `ADAS`, `V2X`, `SCC` |
| Local Feature / Output Surface | local controller, feature surface, or output-facing surface under a larger runtime boundary | `ABS`, `EPB`, `AFLS`, `WIP`, `HUD`, `PGS`, `FCAM`, `SPAS` |
| Validation Harness | scenario injection, verdict aggregation, and evidence support only | `TEST_SCN`, `TEST_BAS` |

## Interpretation rules

### 1. Gateway / Backbone

Use this class when a surface exists mainly to:

- bridge domains
- enforce boundary health
- apply cross-domain route authority
- expose backbone or service-edge behavior

These surfaces should not absorb product meaning that belongs to domain runtime owners.

### 2. Domain Runtime Owner

Use this class when a surface owns one or more of the following:

- normalized domain state
- alert or feature decision inputs
- major output meaning
- domain-level timeout or fail-safe behavior

These surfaces are the default candidates for owner decisions in contracts.

### 3. Local Feature / Output Surface

Use this class when a surface:

- performs local control
- reflects a selected runtime result
- publishes narrow feature outputs
- depends on a higher-level owner for final business meaning

These surfaces may publish outputs, but they should not silently become arbitration owners.

### 4. Validation Harness

Use this class only for surfaces that:

- inject scenarios
- aggregate verdicts
- mirror evidence-oriented state
- support test execution rather than product behavior

Validation harness surfaces must stay separate from product ECU ownership.

## Supporting labels

For reviewer clarity, the following labels may be used when needed:

| Label | Meaning |
| --- | --- |
| `DOMAIN ECU` | product ECU with clear domain responsibility |
| `FEATURE SURFACE` | reviewer-visible feature surface |
| `INFRA SERVICE` | backbone, governance, or service-edge support surface |
| `VALIDATION` | test-only surface |

These labels are optional.
The role classes above remain the primary classification system.

## Current project reading

Read the active baseline like this:

- `CGW` and related backbone surfaces: gateway / backbone
- `VCU`, `IVI`, `ADAS`, `V2X`, `BCM`, `CLU`, `SCC`: domain runtime owners
- comfort, body, chassis, parking, HMI, and sensor-facing leaf surfaces: local feature or output surfaces
- `TEST_SCN`, `TEST_BAS`: validation harness

This project is a driving-alert CANoe SIL baseline.
Only classify surfaces that are meaningful to the current contracts, runtime behavior, or verification path.

## Working rules

1. Keep product ownership separate from validation ownership.
2. Keep route and timeout authority explicit when a gateway surface is involved.
3. Assign contract ownership to the smallest surface that truly owns the business meaning.
4. Do not use transport placement alone to define ECU role.
5. When a surface is only used for observation, evidence, or test stimulus, classify it as validation rather than product runtime.

## Development note

If the runtime architecture changes, update this document before changing contract ownership, route authority, or verification boundaries in downstream documents.

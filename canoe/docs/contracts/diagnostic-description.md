# Diagnostic Description

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document explains the current diagnostic model used by the CANoe SIL baseline.

## Scope

- diagnostic request and response observation
- diagnostic summary seams exposed to runtime, panel, and tools
- evidence-oriented diagnostic fields
- expected future extension points

## Current Diagnostic Model

The active baseline uses a lightweight diagnostic surface centered on observation and evidence rather than a full standalone diagnostic stack description.

The current model is built around:

- request-side capture for what was asked of the system
- response-side capture for what the runtime returned
- summary fields for verdict and evidence workflows
- counters and timestamps for repeatability and debug support

## Diagnostic Layers

| Layer | Role | Main output |
| --- | --- | --- |
| Request observation | capture service intent and request metadata | request identifier, service type, bus/context |
| Response observation | capture status, payload summary, and timing result | response code, response summary, timing fields |
| Runtime summary | expose diagnostic state to panel, tools, and verification | `Diag::*` SysVars |
| Evidence support | support screenshots, logs, and verification records | summary fields, counters, timestamps |

## Current Source Chain

- `contracts/diagnostic-sysvar-contract.md`
- `verification/execution-guide.md`
- `verification/evidence-policy.md`

## Design Rules

- keep diagnostic observation explicit and readable
- do not overload panel-facing variables with raw transport payload detail
- keep evidence-friendly summary fields stable even if implementation detail changes
- add protocol-specific depth only when the active baseline really requires it

## Development Note

This document is a development description, not a frozen final protocol specification.
If the project expands its native diagnostic coverage, transport detail and ownership depth may be extended later.
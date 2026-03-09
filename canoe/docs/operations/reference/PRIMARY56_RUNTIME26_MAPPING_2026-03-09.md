# Primary Surface to Runtime Mapping (2026-03-09)

## Purpose

This document maps the current wide reviewer-facing surface ECU inventory (`100`) to the current active runtime set (`13`).

## Current counts
- visible surface ECUs: `100`
- active runtime anchors: `13`
- product runtime anchors: `11`
- validation-only nodes: `2`
- placeholder surface nodes: `87`

## Active runtime anchor assignment

| Runtime anchor | Assigned surface ECU | Category | Status |
| --- | --- | --- | --- |
| `EMS` | `EMS` | Powertrain | Active |
| `TCU` | `TCU` | Powertrain | Active |
| `VCU` | `VCU` | Powertrain | Active |
| `ESC` | `ESC` | Chassis/Safety | Active |
| `MDPS` | `MDPS` | Chassis/Safety | Active |
| `CGW` | `CGW` | Infrastructure | Active |
| `BCM` | `BCM` | Body/Comfort | Active |
| `IVI` | `IVI` | IVI/HMI | Active |
| `CLU` | `CLU` | IVI/HMI | Active |
| `ADAS` | `ADAS` | ADAS/V2X | Active |
| `V2X` | `V2X` | ADAS/V2X | Active |
| `TST_SCN` | `VALIDATION_HARNESS` | Validation | Validation-only |
| `TST_BAS` | `VALIDATION_HARNESS` | Validation | Validation-only |

## Placeholder policy
Remaining visible surface ECUs stay as placeholder nodes and do not receive runtime logic, message ownership, or ID allocation until explicitly promoted.

## Historical note

`CHGW`, `PTGW`, `ETHM` were intermediate naming candidates in pre-merge audit notes and are not part of the current active runtime mapping baseline.

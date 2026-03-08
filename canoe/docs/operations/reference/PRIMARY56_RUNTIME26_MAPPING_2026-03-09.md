# Primary-56 to Runtime Mapping (2026-03-09)

## Purpose

This document maps the wide reviewer-facing surface ECU inventory to the reduced active runtime anchor set after absorption.

## Current counts
- primary reviewer-facing surface ECUs: `56`
- active runtime anchors: `14`
- validation-only nodes: `2`
- absorbed wrapper-only nodes removed from active tree: `10`

## Active runtime anchor assignment

| Runtime anchor | Assigned surface ECU | Category | Status |
| --- | --- | --- | --- |
| `EMS` | `EMS` | Powertrain | Active |
| `TCU` | `TCU` | Powertrain | Active |
| `VCU` | `VCU` | Powertrain | Active |
| `ESC` | `ESC` | Chassis/Safety | Active |
| `MDPS` | `MDPS` | Chassis/Safety | Active |
| `CHGW` | `CHGW` | Chassis/Safety | Active |
| `PTGW` | `PTGW` | Powertrain | Active |
| `CGW` | `CGW` | Infrastructure | Active |
| `ETHM` | `ETH_BACKBONE` | Infrastructure | Active |
| `BCM` | `BCM` | Body/Comfort | Active |
| `IVI` | `IVI` | IVI/HMI | Active |
| `CLU` | `CLU` | IVI/HMI | Active |
| `ADAS` | `ADAS` | ADAS/V2X | Active |
| `V2X` | `V2X` | ADAS/V2X | Active |
| `VAL_SCENARIO_CTRL` | `VALIDATION_HARNESS` | Validation | Validation-only |
| `VAL_BASELINE_CTRL` | `VALIDATION_HARNESS` | Validation | Validation-only |

## Placeholder policy
The remaining primary surface ECUs stay visible at architecture level, but they do not receive CAPL runtime nodes until explicitly promoted.

# Test Suite Composition

> Warning
> This suite composition is the current CANoe SIL executable baseline.
> When CAPL assets are added, renamed, retired, or moved between active and retire scope,
> the corresponding level suite must be updated in the same baseline.

## Purpose

This document defines the active level suites used to execute the current native CANoe test baseline.
The suite boundary follows executable assets, not historical umbrella reviewer rows.

## Active level suites

- `TS_CANOE_UT_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_UT_ACTIVE_BASELINE/TS_CANOE_UT_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: all active non-retired `TC_CANOE_UT_*` assets
- `TS_CANOE_IT_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_IT_ACTIVE_BASELINE/TS_CANOE_IT_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: all active non-retired `TC_CANOE_IT_*` assets
- `TS_CANOE_ST_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_ST_ACTIVE_BASELINE/TS_CANOE_ST_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: all active non-retired `TC_CANOE_ST_*` assets

## Active campaign suite

- `TS_CANOE_FULL_ACTIVE_BASELINE`
  - path: `canoe/tests/modules/test_suites/TS_CANOE_FULL_ACTIVE_BASELINE/TS_CANOE_FULL_ACTIVE_BASELINE.vtestunit.yaml`
  - scope: ordered wrapper over the current `UT`, `IT`, and `ST` active suites

## Inclusion rule

- include only assets that exist under `canoe/tests/modules/test_units/`
- exclude everything under `canoe/tests/modules/test_units/retire/`
- do not include umbrella reviewer IDs directly
- use exact executable assets as suite members

## Composition rule

- `UT` suite groups unit-level executable assets
- `IT` suite groups integration-level executable assets
- `ST` suite groups system-level executable assets
- `FULL` suite groups the three active level suites into one campaign entry point
- suite membership is asset-based and may cover multiple exact reviewer rows when one executable asset intentionally closes multiple exact cases

## Update rule

- if a row is split into exact rows, update suite membership only when the executable asset set changes
- if an asset is retired, remove it from the corresponding suite in the same change set
- if a new executable asset becomes active, add it to the corresponding suite before changing reviewer-facing status to `Ready`

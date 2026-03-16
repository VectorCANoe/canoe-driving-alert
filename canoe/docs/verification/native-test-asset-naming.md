# Native Test Asset Naming

> [!IMPORTANT]
> This document is the current development baseline for native CANoe SIL test asset naming.
> It may change as the final test tree, harness layout, and execution packaging are fixed.

## 1. Purpose

This document defines the naming convention for executable native test assets that implement the official reviewer-facing test IDs in:

- `driving-alert-workproducts/05_Unit_Test.md`
- `driving-alert-workproducts/06_Integration_Test.md`
- `driving-alert-workproducts/07_System_Test.md`

The goal is to keep:

- `05/06/07` reviewer-facing
- native assets implementation-facing
- the mapping between them stable and readable

## 2. Naming pattern

Use this format for native test assets:

`TC_CANOE_<LEVEL>_<GROUP>_<SEQ>_<SLUG>`

Where:

- `<LEVEL>` = `UT` | `IT` | `ST`
- `<GROUP>` = `CORE` | `V2` | `EXT` | `BASE` | `ETH` | `FULL`
- `<SEQ>` = three digits such as `001`
- `<SLUG>` = short business-readable identifier

Examples:

- `TC_CANOE_UT_CORE_003_ADAS_WARN_CTRL`
- `TC_CANOE_IT_EXT_010_SERVICE_SECURITY_DIAG`
- `TC_CANOE_ST_FULL_002_CONTINUOUS_TRIP_WITH_FAILSAFE`

## 3. Preset and stimulus assets

Use this format for scenario preset or stimulus-only helpers:

`TEST_SCN_<GROUP>_<SLUG>`

Examples:

- `TEST_SCN_CORE_INPUT_PRESET`
- `TEST_SCN_SGW_SECURITY_PRESET`
- `TEST_SCN_DCM_DIAGNOSTIC_PRESET`

Use `TEST_SCN_*` only for:

- input presets
- stimulus profiles
- reusable scenario setup blocks

Do not use `TEST_SCN_*` as the final executable verdict asset name for `UT/IT/ST`.

## 4. Group meaning

| Group | Meaning |
|---|---|
| `CORE` | core driving-alert baseline behavior |
| `V2` | current feature deepening and emergency/arbitration behavior |
| `EXT` | extension behavior beyond the minimal core concept |
| `BASE` | vehicle baseline context integration |
| `ETH` | Ethernet-facing observation or transport verification |
| `FULL` | whole-trip or full-system composed scenario |

## 5. Slug rule

1. Use business-readable names first.
2. Prefer ECU/service/function wording over internal variable names.
3. Keep slugs stable even if internal implementation changes.
4. Do not encode temporary requirement ranges or flow IDs into the slug.
5. Use uppercase snake case only.

Good:

- `ZONE_WARNING`
- `FAILSAFE_MIN_WARNING`
- `DISPLAY_SERVICE_CONTEXT`

Avoid:

- `FLOW_0302_CASE_4`
- `SYSVAR_WARNSTATE_TEST`
- `TMP_NEW_CHAIN`

## 6. Recommended logical tree

The future native test tree should follow this logical grouping:

```text
verification/
├─ unit/
│  ├─ core/
│  ├─ v2/
│  ├─ ext/
│  ├─ out/
│  └─ presets/
├─ integration/
│  ├─ core/
│  ├─ v2/
│  ├─ base/
│  ├─ ext/
│  └─ eth/
└─ system/
   ├─ core/
   ├─ v2/
   ├─ ext/
   ├─ eth/
   └─ full/
```

This is a logical organization rule, not a forced physical folder rule.

## 7. Current build order

Build native assets in this order:

1. `UT` core verdict assets
   - `UT_003`
   - `UT_009`
   - `UT_011`
   - `UT_014`
   - `UT_015`
2. `IT` core composed assets
   - `IT_001` to `IT_008`
3. `ST` core scenario assets
   - `ST_001` to `ST_021`
4. diagnostic-linked assets
   - `UT_063`
   - `UT_064`
   - `IT_040`
   - `ST_043`

## 8. Relationship to other verification documents

Use this document together with:

- `test-asset-mapping.md`
- `diagnostic-coverage.md`
- `execution-guide.md`

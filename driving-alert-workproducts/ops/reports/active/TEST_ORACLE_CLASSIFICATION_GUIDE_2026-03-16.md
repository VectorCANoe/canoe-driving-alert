# Test Oracle Classification Guide

> [!IMPORTANT]
> This document is a working execution guide for DEV1/DEV2/Docs coordination.
> It does not replace the official tables in `05_Unit_Test.md`, `06_Integration_Test.md`, or `07_System_Test.md`.
> Use this guide to decide which oracle should drive PASS/FAIL when native CANoe test assets are implemented or updated.

## 1. Purpose

This guide defines the primary oracle class for the current CANoe SIL baseline.

It complements:

- `driving-alert-workproducts/05_Unit_Test.md`
- `driving-alert-workproducts/06_Integration_Test.md`
- `driving-alert-workproducts/07_System_Test.md`
- `driving-alert-workproducts/ops/reports/active/TEST_ORACLE_EVIDENCE_DIAGNOSTIC_MAPPING_DRAFT_2026-03-15.md`

The goal is to keep TC authoring consistent when the same feature can be observed from:

- owner state
- transport delivery
- ECU output state

## 2. Oracle Classes

| Oracle Class | Meaning | Typical Source |
|---|---|---|
| `Owner Oracle` | Central owner logic or arbitration result is the main verdict basis | `@Core::*`, `@CoreState::*`, owner-local state |
| `Transport Oracle` | CAN/Ethernet delivery result is the main verdict basis | `@Test::obs*`, Ethernet trace, CAN trace |
| `ECU State Oracle` | Product ECU output or consumed/reflected state is the main verdict basis | `frm*` CAN state, panel/HMI state, ECU-level state |

## 3. Closure Rule

1. Use one `Primary Oracle` to decide PASS/FAIL.
2. Use `Secondary Oracle` only to diagnose mismatches or support evidence.
3. Do not let `Transport Oracle` replace `Owner Oracle` for owner-algorithm unit rows.
4. Do not let `Owner Oracle` replace `Transport Oracle` for Ethernet/CAN delivery rows.
5. For system scenarios, prefer visible or product-state outcome first unless the row explicitly targets transport periodicity or fail-safe delivery.

## 4. 05 Unit Test Oracle Mapping

| Row ID | Primary Oracle | Secondary Oracle | Notes |
|---|---|---|---|
| `UT_001`, `UT_002`, `UT_003` | `Owner Oracle` | `ECU State Oracle` | CGW/ADAS local responsibility rows |
| `UT_004`, `UT_005`, `UT_006` | `Owner Oracle` | `Transport Oracle` | V2/arbitration/object-risk unit decisions |
| `UT_007`, `UT_008`, `UT_009` | `Owner Oracle` | `ECU State Oracle` | CLU/CGW/IVI local policy rows |
| `UT_010` | `Transport Oracle` | `Owner Oracle` | V2 tx/rx and timeout behavior |
| `UT_011`, `UT_012`, `UT_013`, `UT_014`, `UT_015` | `Owner Oracle` | `ECU State Oracle` | arbitration/gateway/output policy rows |
| `UT_016`, `UT_017` | `ECU State Oracle` | `Owner Oracle` | chassis extension reflection rows |
| `UT_018`, `UT_019`, `UT_020` | `ECU State Oracle` | `Owner Oracle` | body/occupant/comfort reflection rows |
| `UT_021`, `UT_022` | `ECU State Oracle` | `Owner Oracle` | display/service access reflection rows |
| `UT_023`, `UT_024` | `ECU State Oracle` | `Owner Oracle` | adas/parking/perception extension reflection rows |
| `UT_025` | `Transport Oracle` | `Owner Oracle` | delivery boundary and fail-safe transport row |
| `UT_026`, `UT_027` | `ECU State Oracle` | `Owner Oracle` | propulsion/power-charge extension reflection rows |
| `UT_028`~`UT_069` | `ECU State Oracle` | `Transport Oracle` | support/input preset rows, not priority closeout targets |
| `UT_070`, `UT_071`, `UT_072`, `UT_073`, `UT_074`, `UT_075` | `ECU State Oracle` | `Owner Oracle` | visible output / decel request output rows |
| `UT_076`, `UT_077` | `Transport Oracle` | `Owner Oracle` | external Ethernet tx periodic observation |

## 5. 06 Integration Test Oracle Mapping

| Row ID | Primary Oracle | Secondary Oracle | Notes |
|---|---|---|---|
| `IT_001`, `IT_002`, `IT_003` | `Owner Oracle` | `ECU State Oracle` | baseline activation and zone/highway logic integration |
| `IT_004`, `IT_005`, `IT_006` | `Transport Oracle` | `Owner Oracle` | emergency receive and arbitration delivery rows |
| `IT_007`, `IT_008` | `ECU State Oracle` | `Owner Oracle` | ambient / cluster integration output |
| `IT_009`, `IT_010`, `IT_011` | `Transport Oracle` | `Owner Oracle` | timeout clear, decel assist, fail-safe delivery |
| `IT_012` | `Transport Oracle` | `Owner Oracle` | object-risk transport plus event record support |
| `IT_013`, `IT_014`, `IT_015`, `IT_016`, `IT_017` | `Owner Oracle` | `ECU State Oracle` | context and policy adjustment rows |
| `IT_018` | `Transport Oracle` | `Owner Oracle` | emergency + TTC combined transport row |
| `IT_019`, `IT_020`, `IT_021`, `IT_022`, `IT_023` | `ECU State Oracle` | `Owner Oracle` | chassis/powertrain baseline integration |
| `IT_024`, `IT_025`, `IT_026`, `IT_027`, `IT_028`, `IT_029`, `IT_030`, `IT_031` | `ECU State Oracle` | `Owner Oracle` | body/display/service integration rows |
| `IT_032`, `IT_033`, `IT_034`, `IT_035` | `Owner Oracle` | `ECU State Oracle` | availability, duplicate guard, restore, history policy rows |
| `IT_036`, `IT_037`, `IT_038`, `IT_039`, `IT_041` | `ECU State Oracle` | `Owner Oracle` | extension ECU state integration rows |
| `IT_040` | `ECU State Oracle` | `Owner Oracle` | service/security/diagnostic state reflection, diagnostic explanation optional |
| `IT_042`, `IT_043` | `ECU State Oracle` | `Owner Oracle` | display/audio service consistency |
| `IT_044`, `IT_045` | `Transport Oracle` | `Owner Oracle` | police/ambulance tx path rows |

## 6. 07 System Test Oracle Mapping

| Row ID | Primary Oracle | Secondary Oracle | Notes |
|---|---|---|---|
| `ST_001`, `ST_002` | `ECU State Oracle` | `Owner Oracle` | power-on and normal-drive visible baseline |
| `ST_003`, `ST_004`, `ST_005`, `ST_006`, `ST_007`, `ST_008`, `ST_009`, `ST_010` | `ECU State Oracle` | `Owner Oracle` | customer-visible warning transition rows |
| `ST_011`, `ST_012`, `ST_015`, `ST_016`, `ST_017` | `Transport Oracle` | `Owner Oracle` | emergency arbitration and priority system rows |
| `ST_013`, `ST_014` | `ECU State Oracle` | `Transport Oracle` | direction render correctness on cluster/HUD |
| `ST_018`, `ST_019` | `Transport Oracle` | `Owner Oracle` | tx periodicity rows |
| `ST_020`, `ST_021` | `Transport Oracle` | `Owner Oracle` | timeout clear and restore path |
| `ST_022`, `ST_023`, `ST_024`, `ST_025`, `ST_026` | `Transport Oracle` | `Owner Oracle` | decel assist, fail-safe entry/recovery rows |
| `ST_027`, `ST_028`, `ST_029` | `Transport Oracle` | `ECU State Oracle` | object-risk, object-scenario, event visibility rows |
| `ST_030`, `ST_031`, `ST_032`, `ST_033`, `ST_034` | `ECU State Oracle` | `Owner Oracle` | user-visible context/display/history rows |
| `ST_035`, `ST_036` | `Transport Oracle` | `Owner Oracle` | timeout-clear restore and fail-safe recovery stability |
| `ST_037`, `ST_038` | `ECU State Oracle` | `Owner Oracle` | audio/visual channel stability |
| `ST_039`, `ST_040`, `ST_041`, `ST_042`, `ST_043`, `ST_044` | `ECU State Oracle` | `Owner Oracle` | extension system-context rows |
| `ST_045`, `ST_046` | `ECU State Oracle` | `Transport Oracle` | end-to-end scenario rows; transport used as supporting evidence |

## 7. DEV2 Authoring Rule

When DEV2 creates or updates native test assets:

1. Pick `Primary Oracle` from this guide first.
2. Add only the minimum `Secondary Oracle` needed for diagnosis.
3. Do not add direct transport observer logic to each testcase.
4. Use `TEST_BAS` shared observer for all Ethernet delivery checks.
5. Keep `Owner Oracle` rows focused on product logic, not on packet existence.
6. Keep `ECU State Oracle` rows focused on product-visible state, not on internal owner variables only.

## 8. Next Sync Rule

If `05/06/07` official rows are split, merged, or renumbered, this guide and the diagnostic/evidence mapping draft must be updated in the same batch.

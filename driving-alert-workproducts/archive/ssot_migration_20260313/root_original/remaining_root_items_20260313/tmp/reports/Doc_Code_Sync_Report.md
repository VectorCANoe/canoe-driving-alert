# Doc-Code Sync Report

- Generated At: 2026-03-09 03:35:50 UTC
- Branch: main
- Commit: e7f3bfa
- Gate Result: FAIL

## Req Coverage
| Doc | Covered | Total | Status |
| --- | --- | --- | --- |
| 03 | 98 | 98 | PASS |
| 0301 | 98 | 98 | PASS |
| 0302 | 98 | 98 | PASS |
| 0303 | 98 | 98 | PASS |
| 0304 | 98 | 98 | PASS |
| 05 | 98 | 98 | PASS |
| 07 | 98 | 98 | PASS |
| 06 | 98 | 98 | PASS |

## Func Coverage
| Doc | Covered | Total | Status |
| --- | --- | --- | --- |
| 0301 | 96 | 96 | PASS |
| 0302 | 96 | 96 | PASS |
| 0303 | 96 | 96 | PASS |
| 0304 | 96 | 96 | PASS |

## Implementation Summary
| Item | Coverage | Status |
| --- | --- | --- |
| CAPL node files | 2/26 | FAIL |
| CFG node links | 26/26 | PASS |
| Split DBC files | 6/6 | PASS |
| CFG absolute path hygiene | 0 forbidden path | PASS |

## Issues
### FAIL
- CAPL missing: ACCEL_CTRL, ADAS_WARN_CTRL, AMBIENT_CTRL, BODY_GW, BRK_CTRL, CHS_GW, CLU_BASE_CTRL, CLU_HMI_CTRL, DOMAIN_BOUNDARY_MGR, DOMAIN_ROUTER, DRV_STATE_MGR, EMS_ALERT_RX, EMS_AMB_TX, EMS_POLICE_TX, ENG_CTRL, ETH_SW, HAZARD_CTRL, INFOTAINMENT_GW, IVI_GW, NAV_CTX_MGR, STEER_CTRL, TCM, WARN_ARB_MGR, WINDOW_CTRL
### WARN
- DOMAIN_BOUNDARY_MGR not in DBC BU_: keep as rx-only internal policy or add Rx participant explicitly.

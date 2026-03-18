# Doc-Code Sync Report

- Generated At: 2026-03-17 18:07:54 UTC
- Branch: develop
- Commit: 759b3c2c
- Gate Result: FAIL

## Req Coverage
| Doc | Covered | Total | Status |
| --- | --- | --- | --- |
| 03 | 0 | 97 | FAIL |
| 0301 | 0 | 97 | FAIL |
| 0302 | 0 | 97 | FAIL |
| 0303 | 0 | 97 | FAIL |
| 0304 | 0 | 97 | FAIL |
| 05 | 0 | 97 | FAIL |
| 07 | 0 | 97 | FAIL |
| 06 | 97 | 97 | PASS |

## Func Coverage
| Doc | Covered | Total | Status |
| --- | --- | --- | --- |
| 0301 | 0 | 0 | PASS |
| 0302 | 0 | 0 | PASS |
| 0303 | 0 | 0 | PASS |
| 0304 | 0 | 0 | PASS |

## Implementation Summary
| Item | Coverage | Status |
| --- | --- | --- |
| CAPL node files | 101/101 | PASS |
| channel_assign links | 101/101 | PASS |
| CFG runtime links | 0/101 | WARN |
| Split DBC files | 5/6 | FAIL |
| CFG absolute path hygiene | 0 forbidden path | PASS |

## Issues
### FAIL
- 03: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- 0301: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- 0302: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- 0303: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- 0304: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- 05: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- 07: missing Req Req_001, Req_002, Req_003, Req_004, Req_005, Req_006
- Missing CFG file for gate: expected one of CAN_500kBaud_1ch_split.cfg, CAN_v2_topology_wip.cfg, CAN_500kBaud_1ch.cfg, CAN_500kBaud_1ch.cfg
- Missing DBC files: eth_backbone_can_stub.dbc
### WARN
- CFG runtime links are partial vs channel_assign/source (0/101): ABS, ACU, ADAS, ADM, AEB, AFLS, AHLS, AMP, ASM, AVM, BAT_BMS, BCM
- DOMAIN_BOUNDARY_MGR not in DBC BU_: keep as rx-only internal policy or add Rx participant explicitly.

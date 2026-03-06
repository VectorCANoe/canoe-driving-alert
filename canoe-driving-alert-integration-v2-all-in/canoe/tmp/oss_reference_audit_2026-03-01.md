# OSS Reference Audit (2026-03-01)

## Scope
- Path: `canoe/reference/oss`
- Method: local repository contents (license/readme/SPDX) review
- Note: some repos are marked as different owner in sandbox context; license/readme review is still completed from local files.

## Audit Summary

| Repo | Purpose Fit (CANoe SIL + CAN/Ethernet) | License | Risk Level | Decision |
|---|---|---|---|---|
| `vectorgrp/sil-kit` | High (SIL co-simulation baseline) | MIT | Low | Keep, reference patterns allowed |
| `COVESA/vsomeip` | High (Ethernet SOME/IP contract patterns) | MPL-2.0 | Medium | Keep, reference/integration level |
| `linux-can/can-utils` | Medium (SocketCAN tooling, Linux focused) | Mixed SPDX (GPL/LGPL/BSD variants) | High | Keep as tooling reference only, no direct code copy |
| `hardbyte/python-can` | Medium (CAN tooling in Python) | LGPL-3.0 | Medium | Keep for test tooling reference, avoid direct runtime copy |
| `pylessard/python-udsoncan` | Medium (UDS patterns) | MIT | Low | Keep, optional diagnostics test harness reference |
| `mdabrowski1990/uds` | Medium (UDS client/server patterns) | MIT | Low | Keep, optional diagnostics reference |

## Verified Local Evidence
- `canoe/reference/oss/sil-kit/LICENSE` -> MIT
- `canoe/reference/oss/vsomeip/LICENSE` -> MPL-2.0
- `canoe/reference/oss/python-can/LICENSE.txt` -> LGPL-3.0
- `canoe/reference/oss/python-udsoncan/LICENSE.txt` -> MIT
- `canoe/reference/oss/uds/LICENSE` -> MIT
- `canoe/reference/oss/can-utils/*` -> mixed SPDX headers (GPL/LGPL/BSD)

## Practical Usage Rules for This Project
1. Prioritize MIT/BSD/Apache references for direct adaptation candidates.
2. Use MPL/LGPL/GPL family as design pattern references unless legal review explicitly approves copy scope.
3. Never import OSS code directly into `canoe/src/capl` without trace note + license check record.
4. Keep all third-party source trees outside runtime path (`canoe/reference/oss` only).
5. For every adopted pattern, create a short note in commit message: `source repo + path + adaptation reason`.

## Next Action
- Continue implementation with policy above.
- Complete `split.cfg` CAPL link closure and ETH/GW path hardening with double-check gate.

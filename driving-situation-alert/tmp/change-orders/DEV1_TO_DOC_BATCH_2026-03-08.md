# Dev1 -> Docs Batch Handoff (2026-03-08)

## Purpose
- Batch handoff for docs-team updates discovered during Dev1 runtime audit.
- No new requirement expansion is requested in this batch.
- Scope is doc sync, ownership wording, and SIL shortcut disclosure only.

## Recommended Order
1. DSR-001 `Comm_106` wording fix
2. DSR-002 `Test::*` rows in `0304`
3. DSR-004 HMI/cluster mirror ownership in `0304` and `04`
4. DSR-005 SIL shortcut disclosure in `04`
5. DSR-003 `ETH_SW` role wording in `0302/0303`

## Request Table
| ID | Priority | Target | Request | Evidence |
|---|---|---|---|---|
| DSR-001 | High | `0303_Communication_Specification.md` | Align `Comm_106` wording to the active chain: `VAL_SCENARIO_CTRL -> frmTestResultMsg(0x2A5) -> VAL_BASELINE_CTRL -> frmBaseTestResultMsg(0x2A6)` | `canoe/docs/operations/DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-002 | High | `0304_System_Variables.md` | Add active runtime `Test::*` rows: `displayModeSetting`, `alertVolumeSetting`, `seatBeltOverride`, `historyQueryOffset`, `historyQueryCode` | `canoe/docs/operations/DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-003 | Medium | `0302_NWflowDef.md`, `0303_Communication_Specification.md` | Clarify that `ETH_SW` is an active-profile health/freshness monitor, not a forwarding Ethernet switch | `canoe/docs/operations/DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-004 | Medium | `0304_System_Variables.md`, `04_SW_Implementation.md` | Reflect runtime ownership split: `IVI_GW` is the cluster/HMI frame producer, `CLU_HMI_CTRL` is the mirror/display-state owner for `warningTextCode`, `themeMode`, `popup*`, `audio*`, `volumeLevel`, `ttsState`, `clusterNotif*`, `clusterSync*` | `canoe/docs/operations/DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-005 | Low | `04_SW_Implementation.md` | Add an implementation note that current SIL runtime still uses downstream `selectedAlert` shortcut consumption in `BODY_GW`/`IVI_GW`, and keeps the `EMS_ALERT_RX` `@V2X::*` fallback for compatibility. Mark both as Ethernet cutover backlog, not current-cycle defects. | `canoe/docs/operations/DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |

## Notes
- Keep `01` unchanged in this batch.
- Keep `0302/0303` as contract-oriented docs; place SIL shortcut disclosure in `04` unless a chain-level note is strictly needed.
- This batch does not request architecture redesign or new functionality.

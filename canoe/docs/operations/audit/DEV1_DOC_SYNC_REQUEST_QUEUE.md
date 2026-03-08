# Dev1 Doc Sync Request Queue

**Document ID**: CANOE-OPS-DEV1-DOCSYNC-QUEUE  
**Version**: 1.0  
**Date**: 2026-03-08  
**Status**: Working  
**Owner**: Dev1

---

## 1. Purpose

This queue stores docs-team handoff items discovered during Dev1 audit work.

- Record first
- batch handoff later
- do not treat this file as product SoT

---

## 2. Current Queue

| ID | Priority | Target Doc | Topic | Request | Source |
|---|---|---|---|---|---|
| DSR-001 | High | `0303_Communication_Specification.md` | `Comm_106` | Fix residual `frmBaseTestResultMsg` wording to match active chain: `VAL_SCENARIO_CTRL -> frmTestResultMsg(0x2A5) -> VAL_BASELINE_CTRL -> frmBaseTestResultMsg(0x2A6)` | `DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-002 | High | `0304_System_Variables.md` | `Test::*` coverage | Add active `Test::*` rows used by runtime: `displayModeSetting`, `alertVolumeSetting`, `seatBeltOverride`, `historyQueryOffset`, `historyQueryCode` | `DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-003 | Medium | `0302_NWflowDef.md`, `0303_Communication_Specification.md` | `ETHM` role wording | Clarify that `ETHM` is a SIL health/freshness monitor in the active profile, not a forwarding Ethernet switch | `DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-004 | Medium | `0304_System_Variables.md`, `04_SW_Implementation.md` | HMI/cluster mirror ownership | Update owner/mapping wording so `IVI` is the producer of cluster/HMI bus frames, while `CLU` is the active mirror/display-state owner for `warningTextCode`, `themeMode`, `popup*`, `audio*`, `volumeLevel`, `ttsState`, `clusterNotif*`, and `clusterSync*` | `DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |
| DSR-005 | Low | `04_SW_Implementation.md` | SIL shortcut disclosure | Add an implementation note that the active SIL runtime still consumes downstream `selectedAlert` state through `Core::*` in `BCM`/`IVI`, and keeps the `V2X` `@V2X::*` fallback for compatibility. Mark both as Ethernet cutover backlog, not current-cycle defects. | `DEV1_INTERFACE_AUDIT_REPORT_2026-03-08.md` |

---

## 3. Working Rule

- Add new items only when evidence exists.
- Close items only after:
  - docs are updated, or
  - Dev1 explicitly decides no docs action is needed.


# Dev1 Interface Audit Checklist

**Document ID**: CANOE-OPS-DEV1-INT-CHECK  
**Version**: 1.0  
**Date**: 2026-03-08  
**Status**: Active  
**Owner**: Dev1

---

## 1. Purpose

This checklist fixes Dev1 execution priority for the current phase.

- Goal: close interface quality before adding new runtime logic.
- Scope: active CANoe SIL runtime only.
- Exclusions: GUI redesign, new requirement expansion, Dev2 CLI feature work.

---

## 2. Priority Order

1. P1: Message Contract Audit
2. P2: SysVar Boundary Audit
3. P3: Single Owner / Single Writer Audit
4. P4: Timeout / Reset / Fail-safe Audit
5. P5: Observability Support Audit

Detailed procedure:
- `canoe/docs/operations/audit/DEV1_INTERFACE_AUDIT_PLAYBOOK.md`

### Ethernet Transition Guardrail

- [ ] Keep domain CAN paths unchanged unless a real defect exists.
- [ ] Treat `ETH_INTERFACE_CONTRACT.md` as the logical Ethernet SoT.
- [ ] Treat `eth_backbone_can_stub.dbc` as a replaceable SIL transport stub, not the final architecture.
- [ ] Do not introduce wide architecture expansion only for future Ethernet.
- [ ] Prefer decisions that reduce future transport swap cost:
  - clear owner
  - clear adapter boundary
  - no hidden dependency on stub-only IDs

---

## 3. P1. Message Contract Audit

- [ ] Every active message has one clear owner.
- [ ] `0302`, `0303`, DBC, and CAPL Tx/Rx match for:
  - message name
  - ID
  - DLC
  - period or event
  - timeout
  - owner
- [ ] Validation-only messages are explicitly marked and isolated from product messages.
- [ ] ETH logical names and CAN-stub names have one stable mapping path.
- [ ] No product path depends on undocumented alias names.

Primary evidence:
- `canoe/databases/*.dbc`
- `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`
- `driving-situation-alert/0302_NWflowDef.md`
- `driving-situation-alert/0303_Communication_Specification.md`
- `canoe/src/capl/*`

Close criteria:
- zero unresolved owner conflicts
- zero unresolved DBC/doc/code mismatches in active profile
- zero active-path decisions that would force unnecessary full refactor at Ethernet cutover

---

## 4. P2. SysVar Boundary Audit

- [ ] Every SysVar is classified as one of:
  - runtime owner state
  - runtime mirror
  - validation-only control
  - UI/debug support
- [ ] SysVar usage is judged by boundary and role, not by raw count alone.
- [ ] Every inter-node shortcut through SysVar is marked as one of:
  - acceptable SIL shortcut
  - cleanup target before Ethernet cutover
  - invalid hidden dependency
- [ ] `Test::*` usage is justified and documented as validation-only.
- [ ] Product runtime does not depend on `Test::*` as a hidden functional source.
- [ ] `Core::*` and `CoreState::*` do not replace a missing message contract.
- [ ] `0304` naming, range, and unit match current code.

Primary evidence:
- `driving-situation-alert/0304_System_Variables.md`
- `canoe/project/sysvars/project.sysvars`
- `canoe/src/capl/*`

Close criteria:
- all active SysVars classified
- all active shortcut paths classified
- no unresolved hidden functional dependency through SysVars only

---

## 5. P3. Single Owner / Single Writer Audit

- [ ] Each result/status/event signal has one runtime writer.
- [ ] Each result frame has one sender owner.
- [ ] No duplicated write path remains after recent `0x2A6` cleanup.
- [ ] Event codes and health states have deterministic ownership.

Hotspot examples:
- `frmTestResultMsg (0x2A5)`
- `frmBaseTestResultMsg (0x2A6)`
- `Core::objectEventCode`
- `Core::failSafeMode`
- `CoreState::*` snapshots and counters

Close criteria:
- one writer per active state/output item

---

## 6. P4. Timeout / Reset / Fail-safe Audit

- [ ] Startup state is deterministic.
- [ ] Reset clears injected state and transient status.
- [ ] Timeout clear works without stale residue.
- [ ] Fail-safe enter and recovery conditions are explicit.
- [ ] Long-run tick/timer handling is wrap-safe.

Close criteria:
- no known stale or stuck-state path in active runtime

---

## 7. P5. Observability Support Audit

- [ ] Arbitration decision reason is visible in logs or mirrors.
- [ ] Object-risk decision path is visible.
- [ ] Boundary/fail-safe reason is visible.
- [ ] Validation output can explain PASS/FAIL without manual code tracing.

Close criteria:
- Dev2 can identify failure cause from runtime evidence without opening CAPL first

---

## 8. Working Rule

Dev1 closes work in this order:

1. Contract correctness
2. State ownership
3. Runtime robustness
4. Observability

Do not invert this order by adding new features first.

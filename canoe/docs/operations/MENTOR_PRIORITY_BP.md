# Mentor Priority BP (Execution Baseline)

**Document ID**: CANOE-BP-MENTOR-PRIORITY  
**Version**: 1.1  
**Date**: 2026-03-05  
**Status**: Active  
**Scope**: CANoe SIL, CAN + Ethernet (UDP)

---

## 1. Purpose

This baseline applies mentor feedback first and keeps implementation decisions practical:

- Historical note: v1 was a single-bus flat architecture used for fast parallel development.
- Split CAN by network/domain DBC.
- Keep Ethernet contract outside DBC.
- Fix message ownership before deep logic refinement.
- Deliver runnable end-to-end chain first, then iterate.

---

## 2. Non-Negotiable Rules

1. CAN SoT is split DBC only:
- `canoe/databases/chassis_can.dbc`
- `canoe/databases/powertrain_can.dbc`
- `canoe/databases/body_can.dbc`
- `canoe/databases/infotainment_can.dbc`
- `canoe/databases/chassis_can.dbc`
- `canoe/databases/eth_backbone_can_stub.dbc`

2. Ethernet SoT is contract document only:
- `canoe/docs/operations/ETH_INTERFACE_CONTRACT.md`

3. Backup policy:
- `canoe/databases/v1_legacy/v1_split_345bdb4/emergency_system.dbc` is backup compatibility artifact.
- It must not replace split DBC SoT in design documents.

4. Ownership policy:
- One CAN message has one sender owner.
- For one message, choose only one runtime owner:
  - CAPL output owner, or
  - CANoeIL periodic/event owner
- Dual ownership is prohibited.

5. Naming policy:
- Do not split one ECU into pseudo-nodes solely by Rx/Tx role.
- Gateway can appear across multiple networks by role, but ECU identity is singular.

---

## 3. Runtime Profiles

### Runtime-Core (must pass first)
- Comm_001~Comm_009
- Comm_101~Comm_106
- Target: stable start/stop, no IL resource conflict, deterministic CAN trace.

### Extended-Design (staged activation)
- Comm_201~Comm_205
- Keep as design-complete but activation-controlled until ownership/logic is ready.

---

## 4. Gate Criteria

The following gates are mandatory before calling a build mentor-priority compliant:

1. Split DBC presence pass.
2. Ethernet contract presence pass.
3. Duplicate message ID/name across active DBCs = 0.
4. Active CAN message volume >= 40.
5. Core/baseline message set coverage pass.
6. CANoe measurement startup:
  - No `TxFrameUpdateRequest` resource errors.
  - No message ownership conflict in active profile.

---

## 5. Operational Workflow

1. Update 0302/0303/0304 (source side).
2. Reflect to split DBCs.
3. Run mentor-priority validator:
   - `python canoe/tools/validate_mentor_priority.py`
4. Resolve ownership conflicts (CAPL vs IL) for active runtime profile.
5. Re-run measurement and capture evidence.

---

## 6. Expected Artifacts

- Ownership matrix:
  - `canoe/docs/operations/CAN_MESSAGE_OWNERSHIP_MATRIX.md`
- Gate report:
  - `canoe/tmp/mentor_priority_gate_report.md`
- Optional compatibility backup:
  - `canoe/databases/v1_legacy/v1_split_345bdb4/emergency_system.dbc`

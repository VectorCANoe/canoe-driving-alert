# Software Unit Design Traceability (소프트웨어 유닛 설계 추적성)

**Document ID**: PART6-09-SUDT
**ISO 26262 Reference**: Part 6, Clause 9
**ASPICE Reference**: SWE.3 (BP5)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Software Requirements → Software Units

### SWR-001: CAN Message Reception (AEB)

| Software Unit | Function | ASIL |
|---------------|----------|------|
| SU-D-001 | CAN_Receive_AEB() | ASIL-D |
| SU-D-010 | CRC_Check() | ASIL-D |
| SU-D-011 | Alive_Counter_Check() | ASIL-D |

---

### SWR-002: AEB Event Processing

| Software Unit | Function | ASIL |
|---------------|----------|------|
| SU-D-002 | AEB_Event_Handler() | ASIL-D |
| SU-D-012 | Priority_Queue_Insert() | ASIL-D |
| SU-D-013 | Event_Scheduler() | ASIL-D |

---

### SWR-003: Cluster Warning UI Request

| Software Unit | Function | ASIL |
|---------------|----------|------|
| SU-D-003 | CAN_Transmit_Warning() | ASIL-D |
| SU-D-014 | CRC_Calculate() | ASIL-D |

---

## 2. Traceability Matrix

| SWR ID | Software Units | Total Units | Coverage |
|--------|----------------|-------------|----------|
| SWR-001 | SU-D-001, SU-D-010, SU-D-011 | 3 | 100% |
| SWR-002 | SU-D-002, SU-D-012, SU-D-013 | 3 | 100% |
| SWR-003 | SU-D-003, SU-D-014 | 2 | 100% |
| SWR-009 | SU-B-003 | 1 | 100% |
| SWR-010 | SU-B-001 | 1 | 100% |

**Total**: 120 SWRs → 45 Software Units

---

**Auto-generated**: 2026-02-14 15:10:48

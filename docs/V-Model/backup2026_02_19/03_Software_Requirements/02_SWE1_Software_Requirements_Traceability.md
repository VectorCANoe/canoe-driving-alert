# Software Requirements Traceability (소프트웨어 요구사항 추적성)

**Document ID**: PART6-02-SRT
**ISO 26262 Reference**: Part 6, Clause 7
**ASPICE Reference**: SWE.1 (BP6)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Bidirectional Traceability

```
System Requirements (55개)
        ↕
Software Requirements (120개)
        ↕
Software Architecture (Modules)
        ↕
Software Units (Functions)
        ↕
Software Unit Tests
```

---

## 2. System Req → Software Req Mapping

### REQ-A02: AEB 긴급 제동 경고

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-001 | CAN Message Reception (AEB) | ASIL-D |
| SWR-002 | AEB Event Processing | ASIL-D |
| SWR-003 | Cluster Warning UI Request | ASIL-D |

---

### REQ-A01: LDW 차선 이탈 경고

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-004 | LDW CAN Message Reception | ASIL-D |
| SWR-005 | LDW Dual-Channel Warning | ASIL-D |
| SWR-006 | LDW Timing Guarantee | ASIL-D |

---

### REQ-A03: 후진 중 도어 개방 경고

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-007 | Door Open Signal Reception | ASIL-D |
| SWR-008 | Reverse Gear Signal Reception | ASIL-D |
| SWR-009 | Door Open + Reverse Logic | ASIL-D |

---

### REQ-A01: Sports Mode Ambient Lighting

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-010 | Ambient Lighting Control | ASIL-B |

---

## 3. Coverage Statistics

- **System Requirements**: 55개
- **Software Requirements**: 120개
- **Traceability Coverage**: 100% (55/55)
- **Average Decomposition Ratio**: 2.2 (120/55)

---

**Auto-generated**: 2026-02-14 15:08:41

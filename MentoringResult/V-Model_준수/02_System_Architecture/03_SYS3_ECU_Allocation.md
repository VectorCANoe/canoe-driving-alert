# ECU Allocation (ECU 할당)

**Document ID**: PART4-04-ECU
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. ECU Allocation Summary

### System Requirements → ECU Mapping

| ECU | Allocated Requirements | ASIL | DBC Source |
|-----|------------------------|------|------------|
| **vECU (IVI vECU)** | REQ-001, 004, 008~014, 027~047 | ASIL-D | 본 프로젝트 신규 |
| **Cluster ECU** | REQ-002, 006, 018, 027, 029, 031 | ASIL-D | hyundai_kia_generic.dbc |
| **BCM** | REQ-003, 006, 021, 030, 051 | ASIL-C | vehicle_system.dbc |
| **TCU** | REQ-002, 006, 015, 016, 020 | ASIL-C | vehicle_system.dbc |
| **Front Camera** | REQ-027, 032, 033, 037 | ASIL-D | vehicle_system.dbc |
| **Rear Camera** | REQ-028, 030 | ASIL-C | vehicle_system.dbc |
| **SCC (AEB)** | REQ-029, 034, 035 | ASIL-D | vehicle_system.dbc |

---

## 2. Domain별 ECU List


### Infotainment Domain

| # | ECU | ASIL | Primary Function |
|---|-----|------|------------------|
| 1 | IVI Control ECU | ASIL-B | ... |
| 2 | vECU (IVI vECU) | ASIL-B | ... |
| 3 | Cluster ECU | ASIL-B | ... |
| 4 | HUD ECU | ASIL-B | ... |

### Body Domain

| # | ECU | ASIL | Primary Function |
|---|-----|------|------------------|
| 1 | BCM | ASIL-B | ... |
| 2 | Lighting Control ECU | ASIL-B | ... |
| 3 | HVAC Control ECU | ASIL-B | ... |
| 4 | BDC | ASIL-B | ... |
| 5 | Door Sensors | ASIL-B | ... |
| 6 | Seat Control ECU | ASIL-B | ... |

### ADAS Domain

| # | ECU | ASIL | Primary Function |
|---|-----|------|------------------|
| 1 | ADAS Control ECU | ASIL-D | ... |
| 2 | Front Camera (LDW) | ASIL-D | ... |
| 3 | Rear Camera (RVC) | ASIL-D | ... |
| 4 | Radar (BSD) | ASIL-D | ... |
| 5 | SCC (AEB) | ASIL-D | ... |
| 6 | AVM ECU | ASIL-D | ... |

### Powertrain Domain

| # | ECU | ASIL | Primary Function |
|---|-----|------|------------------|
| 1 | EMS | ASIL-C | ... |
| 2 | TCU | ASIL-C | ... |
| 3 | Vehicle Speed Sensor | ASIL-C | ... |

### Chassis Domain

| # | ECU | ASIL | Primary Function |
|---|-----|------|------------------|
| 1 | ESP/ESC | ASIL-D | ... |
| 2 | MDPS | ASIL-D | ... |
| 3 | ABS | ASIL-D | ... |
| 4 | EPB | ASIL-D | ... |


---

## 3. Safety Requirements Allocation

| Safety Goal | ASIL | Allocated ECU(s) | Rationale |
|-------------|------|------------------|-----------|
| SG-01 (AEB 경고) | ASIL-D | vECU, Cluster | Dual Channel |
| SG-02 (LDW 경고) | ASIL-D | vECU, Cluster, MDPS | Dual Channel |
| SG-03 (후진 경고) | ASIL-B | vECU, TCU, Cluster | Single Channel 충분 |
| SG-04 (도어 경고) | ASIL-C | vECU, BCM, Cluster | 주행 중 안전 |
| SG-07 (Fail-Safe) | ASIL-C | vECU (CAN Driver) | 통신 오류 감지 |

---

**Auto-generated**: 2026-02-14 14:59:03

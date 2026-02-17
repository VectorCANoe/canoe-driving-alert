# ECU Allocation (ECU 할당)

**Document ID**: PART4-04-ECU
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 2.0
**Date**: 2026-02-17
**Status**: Released (v2.0 — ASIL 모순 해소, HSI 추가)

---

## 1. ECU Allocation Summary

### System Requirements → ECU Mapping

| ECU | Allocated Requirements | ASIL | DBC Source |
|-----|------------------------|------|------------|
| **vECU (IVI vECU)** | REQ-A01, 004, 008~014, 027~047 | ASIL-D (최고) / ASIL-B (도메인 평균) | 본 프로젝트 신규 |
| **Cluster ECU** | REQ-F01, 006, 018, 027, 029, 031 | ASIL-D | hyundai_kia_generic.dbc |
| **BCM** | REQ-F01, 006, 021, 030, 051 | ASIL-C | vehicle_system.dbc |
| **TCU** | REQ-F01, 006, 015, 016, 020 | ASIL-C | vehicle_system.dbc |
| **Front Camera** | REQ-A01, 032, 033, 037 | ASIL-D | vehicle_system.dbc |
| **Rear Camera** | REQ-A03, 030 | ASIL-D | vehicle_system.dbc |
| **SCC (AEB)** | REQ-A02, 034, 035 | ASIL-D | vehicle_system.dbc |

---

## 2. Domain별 ECU List


### Infotainment Domain

| # | ECU | ASIL | Primary Function |
|---|-----|------|------------------|
| 1 | IVI Control ECU | ASIL-B | ... |
| 2 | vECU (IVI vECU) | ASIL-D (ADAS UI 파티션) / ASIL-B (Infotainment 파티션) | ASIL 분리 파티셔닝 적용 |
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
| 3 | Rear Camera (RVC) | ASIL-D | 후방 장애물 감지, 후진 지원 |
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
| SG-04 (도어 경고) | ASIL-B (수정) | vECU, BCM, Cluster | 주행 중 안전 |
| SG-06 (Fail-Safe) | ASIL-B (수정, 구 SG-07) | vECU (CAN Driver) | CAN 통신 오류 감지 |

---

## 4. vECU ASIL 파티셔닝 설명 (ASIL Clarification)

> **ISSUE-26 해소**: vECU는 하나의 물리 ECU이지만 ASIL-D와 ASIL-B 소프트웨어 파티션을 동시에 포함합니다.

| 파티션 | 포함 소프트웨어 모듈 | ASIL | Freedom from Interference |
|--------|-------------------|------|--------------------------|
| ASIL-D 파티션 | ADAS_UI_Manager, CAN_Driver (ASIL-D CAN) | ASIL-D | MPU 분리, 별도 메모리 영역 |
| ASIL-B 파티션 | Safety_Warning_Manager, Reverse_Warning_Manager, Fail-Safe_Manager | ASIL-B | MPU 분리 |
| ASIL-A 파티션 | Lighting_Control_Manager | ASIL-A | 별도 태스크 |
| QM 파티션 | OTA_Manager, User_Profile_Manager, Priority_Manager | QM | 비보호 |

> **ISO 26262-6:2018 §7.4.6 (Freedom from Interference)**: ASIL-D 파티션은 QM/ASIL-B 파티션의 고장으로부터 보호됩니다.
> ECU Allocation Summary에서 vECU의 ASIL-D는 "해당 ECU에서 구현되는 최고 ASIL"을 나타냅니다.

---

## 5. Hardware-Software Interface (HSI) 참조

> **ISO 26262-4:2018 Clause 7.4.1**: 시스템 아키텍처 설계는 Hardware-Software Interface를 기술해야 합니다.

| 인터페이스 | 하드웨어 | 소프트웨어 모듈 | ASIL | 제약사항 |
|-----------|---------|--------------|------|---------|
| CAN-HS1 (ADAS) | CAN 컨트롤러 2 (500kbps) | CAN_Driver → ADAS_UI_Manager | ASIL-D | 인터럽트 지연 ≤ 1ms |
| CAN-HS2 (Body) | CAN 컨트롤러 1 (500kbps) | CAN_Driver → Safety_Warning | ASIL-B | 메시지 큐 깊이 ≥ 32 |
| CAN-LS (진단) | CAN 컨트롤러 3 (125kbps) | Diagnostic_Manager | ASIL-B | UDS Timeout 5s |
| Watchdog IC | External WD (TPS3823 계열) | Task_ADAS Kick (Window 80~120ms) | ASIL-D | 전원 공급 독립 |
| MPU | Cortex-M4 MPU (8 Region) | RTOS 스케줄러 | ASIL-D | Region 설정 오류 시 Hard Fault |
| Ambient LED PWM | PWM 타이머 채널 | Lighting_Control_Manager | ASIL-A | 주파수 범위: 200Hz~10kHz |

> 상세 HSI 명세는 **02_System_Architecture/06_SYS3_Interface_Definition.md** Section 2 참조.


---

**Document Version**: 2.0 | **Last Updated**: 2026-02-17

---

## 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release |
| 2.0 | 2026-02-17 | Technical Review | ASIL 모순 해소 (vECU D/B 파티셔닝, Rear Camera D); SG-04→ASIL-B; SG-07→SG-06; HSI 섹션 추가 |

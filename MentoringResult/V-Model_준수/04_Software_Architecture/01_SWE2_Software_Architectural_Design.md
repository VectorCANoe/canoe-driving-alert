# Software Architectural Design (소프트웨어 아키텍처 설계)

**Document ID**: PART6-05-SAD
**ISO 26262 Reference**: Part 6, Clause 8
**ASPICE Reference**: SWE.2
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Software Architecture Overview

**Architecture Pattern**: Layered Architecture with AUTOSAR Classic 기반

```
┌─────────────────────────────────────────┐
│      Application Layer (ASIL-D)         │
│  ┌───────────┬──────────────┬─────────┐ │
│  │ ADAS UI   │ Warning Mgr  │ Lighting│ │
│  │ Manager   │ (ASIL-C)     │ Control │ │
│  │ (ASIL-D)  │              │(ASIL-B) │ │
│  └───────────┴──────────────┴─────────┘ │
├─────────────────────────────────────────┤
│      RTE (Runtime Environment)          │
├─────────────────────────────────────────┤
│      Basic Software (BSW)               │
│  ┌───────────┬──────────────┬─────────┐ │
│  │ CAN Driver│ Diagnostic   │ Memory  │ │
│  │ (ASIL-D)  │ (UDS)        │ Manager │ │
│  └───────────┴──────────────┴─────────┘ │
├─────────────────────────────────────────┤
│      MCAL (Microcontroller Abstraction) │
└─────────────────────────────────────────┘
```

---

## 2. Software Components (SWCs)

### SWC-01: ADAS_UI_Manager

- **ASIL**: ASIL-D
- **Responsibility**: ADAS 이벤트 처리 (AEB, LDW, BSD)
- **Inputs**:
  - CAN Rx: SCC_AEB_Status, FrontCam_LDW_Status
- **Outputs**:
  - CAN Tx: Cluster_Warning_Request
- **Internal State**: Event Queue (Priority-based)
- **Cycle Time**: 10ms
- **Memory**: 8 KB RAM

**Sub-Modules**:
- AEB_Handler (SWR-001, SWR-002, SWR-003)
- LDW_Handler (SWR-004, SWR-005, SWR-006)
- Event_Scheduler (Priority Queue)

---

### SWC-02: Safety_Warning_Manager

- **ASIL**: ASIL-C
- **Responsibility**: 안전 경고 로직 (후진 + 도어)
- **Inputs**:
  - CAN Rx: BCM_Door_Status, TCU_Gear_Position
- **Outputs**:
  - CAN Tx: Cluster_Warning_Request, Lighting_Control_Request
- **Internal State**: Safety Logic State Machine
- **Cycle Time**: 10ms
- **Memory**: 4 KB RAM

**Sub-Modules**:
- Door_Monitor (SWR-007)
- Gear_Monitor (SWR-008)
- Safety_Logic_Evaluator (SWR-009)

---

### SWC-03: Lighting_Control_Manager

- **ASIL**: ASIL-B
- **Responsibility**: Ambient 조명 제어
- **Inputs**:
  - CAN Rx: Vehicle_Speed, Sports_Mode_Status
- **Outputs**:
  - PWM Output: LED_R, LED_G, LED_B
- **Internal State**: Color Lookup Table
- **Cycle Time**: 100ms
- **Memory**: 2 KB RAM

**Sub-Modules**:
- Speed_Monitor (SWR-010)
- Color_Controller (Lookup Table)

---

### SWC-04: CAN_Communication_Manager

- **ASIL**: ASIL-D
- **Responsibility**: CAN 송수신, E2E 보호
- **Inputs**: Application Layer Messages
- **Outputs**: CAN Bus (CAN-HS2)
- **Safety Mechanisms**:
  - CRC-8 Validation
  - Alive Counter Check
  - Timeout Monitoring (30ms)
- **Cycle Time**: 1ms (Interrupt-driven)

---

## 3. Software Architecture Layers

### Layer 1: Application Layer

| Component | ASIL | Cycle | RAM | Flash |
|-----------|------|-------|-----|-------|
| ADAS_UI_Manager | ASIL-D | 10ms | 8 KB | 32 KB |
| Safety_Warning_Manager | ASIL-C | 10ms | 4 KB | 16 KB |
| Lighting_Control_Manager | ASIL-B | 100ms | 2 KB | 8 KB |

---

### Layer 2: Service Layer (RTE)

- **Purpose**: SWC 간 통신 추상화
- **Functions**:
  - Rte_Read_XXX(): Input Port 읽기
  - Rte_Write_XXX(): Output Port 쓰기
  - Rte_Call_XXX(): Server-Client 통신

---

### Layer 3: Basic Software (BSW)

| Module | ASIL | Responsibility |
|--------|------|----------------|
| CAN Driver | ASIL-D | CAN 송수신, 오류 감지 |
| Diagnostic Manager | ASIL-B | UDS 서비스, DTC 관리 |
| Memory Manager | QM | NVM 읽기/쓰기 |
| OS (OSEK/VDX) | ASIL-D | Task Scheduling, Resource Management |

---

## 4. Safety Architecture

### ASIL Decomposition

| Component | Original ASIL | Decomposed | Independence |
|-----------|---------------|------------|--------------|
| LDW_Handler | ASIL-D | ASIL-C (시각) + ASIL-C (촉각) | HW 채널 분리 |

### Freedom from Interference (FFI)

- **Memory Protection**: MPU (Memory Protection Unit) 사용
  - ASIL-D SWC: 0x1000_0000 ~ 0x1000_1FFF (Protected)
  - ASIL-C SWC: 0x1000_2000 ~ 0x1000_2FFF (Protected)
  - QM SWC: 0x1000_3000 ~ 0x1000_3FFF (Non-protected)
- **Timing Protection**: Execution Time Monitoring (Watchdog per Task)
- **Control Flow Monitoring**: Program Flow Monitoring (PFM)

---

## 5. Interface Specification

### SWC-01 ↔ SWC-04 Interface

**Interface Name**: ADAS_to_CAN

| Port Name | Direction | Data Type | Cycle |
|-----------|-----------|-----------|-------|
| AEB_Warning_Request | Out | Boolean | 10ms |
| LDW_Warning_Request | Out | Boolean | 10ms |
| SCC_AEB_Status | In | uint8_t | 10ms |
| FrontCam_LDW_Status | In | uint8_t | 10ms |

---

### SWC-02 ↔ SWC-04 Interface

**Interface Name**: Safety_to_CAN

| Port Name | Direction | Data Type | Cycle |
|-----------|-----------|-----------|-------|
| Door_Status | In | uint8_t (Bitmask) | 10ms |
| Gear_Position | In | uint8_t | 10ms |
| Red_Warning_Active | Out | Boolean | 10ms |

---

## 6. Data Flow Diagram

```
[SCC ECU] --CAN--> [CAN_Driver] --[AEB_Status]--> [ADAS_UI_Manager] --[Warning_Request]--> [Cluster ECU]
                                                          |
                                                          v
                                                  [Event_Scheduler]
                                                          |
                                                          v
                                                  [Priority Queue]
```

---

## 7. Task Architecture (OSEK OS)

| Task Name | Priority | Cycle | WCET | ASIL |
|-----------|----------|-------|------|------|
| Task_ADAS | 10 (Highest) | 10ms | 8ms | ASIL-D |
| Task_Safety | 9 | 10ms | 5ms | ASIL-C |
| Task_Lighting | 5 | 100ms | 10ms | ASIL-B |
| Task_Diag | 3 | 100ms | 15ms | ASIL-B |

**Scheduling Policy**: Preemptive Priority-based

---

## 8. Memory Map

| Region | Address Range | Size | ASIL | Content |
|--------|---------------|------|------|---------|
| Flash | 0x0000_0000 ~ 0x0007_FFFF | 512 KB | ASIL-D | Code + Const |
| RAM | 0x2000_0000 ~ 0x2000_FFFF | 64 KB | ASIL-D | Global Variables |
| Stack (Task_ADAS) | 0x2000_F000 ~ 0x2000_FFFF | 4 KB | ASIL-D | Task Stack |

---

## 9. ASPICE SWE.2 Compliance

**Base Practices**:
- ✅ BP1: Software architectural design developed
- ✅ BP2: Software requirements allocated to components
- ✅ BP3: Software interfaces defined
- ✅ BP4: Dynamic behavior described
- ✅ BP5: Consistency ensured (Req ↔ Arch)
- ✅ BP6: Traceability established

---

**Auto-generated**: 2026-02-14 15:08:41

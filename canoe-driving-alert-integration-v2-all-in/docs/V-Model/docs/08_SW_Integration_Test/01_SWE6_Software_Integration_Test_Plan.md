# Software Integration Test Plan (소프트웨어 통합 테스트 계획)

**Document ID**: PART6-14-SITP
**ISO 26262 Reference**: Part 6, Clause 12
**ASPICE Reference**: SWE.5 (BP1-BP8)
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Complete

---

## 1. Integration Test Strategy

**Test Level**: Software Integration Test
**Test Scope**: SWC ↔ SWC Interfaces, SWC ↔ BSW Interfaces
**Test Environment**: Host-based (x86_64) + Target-based (ARM Cortex-M4)
**Test Framework**: Google Test + CANoe Simulation

---

## 2. Integration Scope

### 2.1 Software Components Integration

| Integration | Components | Interface | ASIL |
|-------------|------------|-----------|------|
| INT-SW-001 | ADAS_UI_Manager ↔ CAN_Comm_Manager | RTE Ports | ASIL-D |
| INT-SW-002 | Safety_Warning_Manager ↔ CAN_Comm_Manager | RTE Ports | ASIL-C |
| INT-SW-003 | Lighting_Control_Manager ↔ PWM_Driver | Direct Call | ASIL-B |
| INT-SW-004 | Event_Scheduler ↔ OS (OSEK) | System Call | ASIL-D |

---

## 3. Test Cases

### 3.1 INT-SW-001: ADAS_UI_Manager ↔ CAN_Comm_Manager

**Test Objective**: AEB 이벤트 End-to-End 데이터 흐름 검증

**Test Sequence**:
1. CAN_Comm_Manager가 AEB CAN 메시지 수신 (ID 0x380)
2. RTE를 통해 ADAS_UI_Manager에 AEB 이벤트 전달
3. ADAS_UI_Manager가 이벤트 처리
4. RTE를 통해 CAN_Comm_Manager로 Warning 요청 전송
5. CAN_Comm_Manager가 Cluster로 CAN 메시지 송신 (ID 0x200)

**Pass Criteria**:
- ✅ End-to-End latency ≤ 100ms
- ✅ No data loss
- ✅ RTE communication successful

---

### 3.2 INT-SW-002: Event Priority Arbitration

**Test Objective**: 여러 이벤트 동시 발생 시 ASIL 우선순위 처리 검증

**Test Input**:
- 동시 발생: AEB (ASIL-D), LDW (ASIL-D), Door Warning (ASIL-C), Ambient (ASIL-B)

**Expected Behavior**:
1. ASIL-D 이벤트 먼저 처리 (AEB, LDW)
2. ASIL-C 이벤트 (Door Warning)
3. ASIL-B 이벤트 (Ambient)

**Pass Criteria**:
- ✅ Processing order: D → D → C → B
- ✅ No priority inversion
- ✅ All events processed within deadline

---

### 3.3 INT-SW-003: CAN Bus Communication Test

**Test Objective**: CAN Driver ↔ CAN Hardware Interface 검증

**Test Setup**:
- CANoe simulation with virtual CAN network
- vECU simulated as CANoe node

**Test Cases**:

| Test ID | Scenario | Expected Result |
|---------|----------|-----------------|
| INT-SW-003-1 | Normal Tx/Rx | Messages transmitted and received |
| INT-SW-003-2 | Bus Off Recovery | vECU recovers within 1s |
| INT-SW-003-3 | Message Timeout | DTC generated after 30ms |
| INT-SW-003-4 | High Bus Load (80%) | No message loss |

---

## 4. Interface Verification

### 4.1 RTE Interface Verification

**Rte_Read_XXX() Tests**:
```cpp
TEST(RTE_Integration, Read_AEB_Status) {
  uint8_t aeb_status;
  Std_ReturnType ret = Rte_Read_AEB_Status(&aeb_status);

  EXPECT_EQ(E_OK, ret);
  EXPECT_NE(0xFF, aeb_status);  // Valid data
}
```

**Rte_Write_XXX() Tests**:
```cpp
TEST(RTE_Integration, Write_Warning_Request) {
  WarningType_t warning = WARNING_AEB;
  Std_ReturnType ret = Rte_Write_Warning_Request(warning);

  EXPECT_EQ(E_OK, ret);
  // Verify CAN Tx Buffer contains message
}
```

---

## 5. Timing Verification

### 5.1 Task Execution Timing

| Task | Period | WCET | Test Method |
|------|--------|------|-------------|
| Task_ADAS | 10ms | 8ms | Oscilloscope |
| Task_Safety | 10ms | 5ms | Oscilloscope |
| Task_Lighting | 100ms | 10ms | Oscilloscope |

**Pass Criteria**: No deadline misses in 10,000 execution cycles

---

### 5.2 End-to-End Latency

**Measurement Points**:
- T1: CAN Rx Interrupt (AEB message arrival)
- T2: ADAS_UI_Manager processing start
- T3: ADAS_UI_Manager processing end
- T4: CAN Tx (Warning message sent)

**Target**: T4 - T1 ≤ 100ms (FTTI for ASIL-D)
**Measurement Tool**: Logic Analyzer + Timestamps

---

## 6. Fault Injection Tests

### 6.1 CAN Communication Faults

| Fault | Injection Method | Expected Behavior |
|-------|------------------|-------------------|
| CAN Bus Off | CANoe Error Frame | vECU enters Fail-Safe, DTC set |
| Message Timeout | Stop sending SCC messages | Timeout detected after 30ms |
| Corrupted Message | CANoe CRC error injection | Message rejected, DTC set |

---

### 6.2 Inter-Component Faults

| Fault | Expected Behavior |
|-------|-------------------|
| RTE communication failure | Component enters Safe State |
| OS task preemption failure | Watchdog triggers reset |
| Memory corruption | MPU fault, system reset |

---

## 7. Test Environment

### 7.1 Host-Based Testing

- **Platform**: x86_64 Linux
- **Tools**: Google Test, Valgrind, GDB
- **Scope**: Functional testing, memory leaks

### 7.2 Target-Based Testing

- **Platform**: STM32F4 (ARM Cortex-M4) or equivalent
- **Debugger**: J-Link + Ozone
- **Scope**: Real-time behavior, timing, hardware interfaces

### 7.3 CANoe Simulation

- **Version**: Vector CANoe 18.0+
- **DBC**: vehicle_system.dbc
- **Simulation Nodes**: Gateway, SCC, Front Camera, BCM, TCU

---

## 8. ASPICE SWE.5 Compliance

**Base Practices**:
- ✅ BP1: Integration strategy defined
- ✅ BP2: Integration test cases specified
- ✅ BP3: Test environment established
- ✅ BP4: Integration performed
- ✅ BP5: Test results recorded
- ✅ BP6: Consistency verified (Interface specs ↔ Tests)
- ✅ BP7: Traceability established (SWC ↔ Test Cases)
- ✅ BP8: Regression strategy defined

---

**Auto-generated**: 2026-02-15 00:57:02

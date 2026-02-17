# Software Qualification Test Plan (소프트웨어 적격성 테스트 계획)

**Document ID**: PART6-16-SQTP
**ISO 26262 Reference**: Part 6, Clause 12
**ASPICE Reference**: SWE.6 (SW Qualification)
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Complete

---

## 1. Test Objective

**Purpose**: vECU 소프트웨어가 **모든 Software Requirements (120개)**를 충족하는지 검증

**Test Level**: Black-box Testing (Requirements-based)
**Test Basis**: 03_Software_Requirements (SWE.1 문서)

---

## 2. Test Strategy

### 2.1 Requirements-Based Testing

- **120개 Software Requirements** → **300개 Qualification Test Cases**
- **Traceability**: SWR ↔ Test Case (1:N 매핑)

### 2.2 Back-to-Back Testing

- **Model**: MATLAB/Simulink Model (if available)
- **Code**: Generated C Code
- **Comparison**: Model output vs Code output (100% match required)

---

## 3. Test Environment

### 3.1 HIL (Hardware-in-the-Loop)

- **Platform**: dSPACE SCALEXIO or Vector CANoe.HIL
- **ECU**: Target ECU (vECU on ARM Cortex-M4)
- **I/O Simulation**: CAN Interface × 3 (HS1, HS2, LS)
- **Fault Injection**: CAN Bus Off, Voltage Drop, Signal Timeout

### 3.2 CANoe Test Automation

- **Test Framework**: CANoe CAPL Test Modules
- **DBC**: vehicle_system.dbc
- **Simulation Nodes**: Gateway, SCC, Front Camera, BCM, TCU, Cluster

---

## 4. Test Cases

### 4.1 Functional Requirements Test

#### TC-SWQUAL-001: AEB Warning End-to-End (SWR-001, SWR-002, SWR-003)

**Test Objective**: AEB 이벤트 발생 시 Cluster 경고 UI 활성화 검증

**Test Setup**:
- CANoe simulation: SCC sends AEB event (ID 0x380)
- vECU receives and processes event
- vECU sends warning request to Cluster (ID 0x200)

**Test Steps**:
1. CANoe: Send AEB_Active=1, AEB_Level=2 (CAN ID 0x380)
2. Wait 100ms (FTTI)
3. Verify vECU sent WARNING_TYPE=0x01 (AEB) to Cluster (ID 0x200)

**Pass Criteria**:
- ✅ Response time ≤ 100ms
- ✅ WARNING_TYPE = 0x01
- ✅ WARNING_LEVEL = 0xFF (RED)

---

#### TC-SWQUAL-002: LDW Dual-Channel Warning (SWR-004, SWR-005, SWR-006)

**Test Objective**: LDW 이벤트 발생 시 시각+촉각 이중 경고 검증

**Test Steps**:
1. CANoe: Send LDW_Active=1, LDW_Direction=LEFT (ID 0x350)
2. Wait 200ms (FTTI)
3. Verify vECU sent:
   - Warning to Cluster (ID 0x200, WARNING_TYPE=0x02)
   - Haptic request to MDPS (ID 0x210, HAPTIC_FEEDBACK=0x01)

**Pass Criteria**:
- ✅ Both channels activated
- ✅ Response time ≤ 200ms
- ✅ Independence verified (disable one channel, other still works)

---

#### TC-SWQUAL-003: Door Open + Reverse Logic (SWR-007, SWR-008, SWR-009)

**Test Objective**: 후진 중 도어 개방 시 RED 경고 활성화

**Test Matrix** (16 combinations):

| Door | Gear | Expected Warning | Test ID |
|------|------|------------------|---------|
| Open (0x01) | R | ✅ RED | TC-SWQUAL-003-1 |
| Closed (0x00) | R | ❌ None | TC-SWQUAL-003-2 |
| Open (0x01) | P | ❌ None | TC-SWQUAL-003-3 |
| Open (0x01) | D | ❌ None | TC-SWQUAL-003-4 |
| ... | ... | ... | ... |

**Pass Criteria**: All 16 test cases pass

---

### 4.2 Safety Requirements Test

#### TC-SWQUAL-101: CRC Validation (SSR-D-002)

**Test Objective**: CRC 오류 메시지 거부 검증

**Test Steps**:
1. CANoe: Send AEB message with corrupted CRC (data[7] = 0x00)
2. Verify vECU rejects message
3. Verify DTC `DTC_AEB_CRC_ERROR` generated

**Pass Criteria**:
- ✅ Message rejected
- ✅ DTC set
- ✅ No false activation

---

#### TC-SWQUAL-102: Timeout Detection (SSR-D-001)

**Test Objective**: 메시지 Timeout 검출

**Test Steps**:
1. CANoe: Send AEB messages normally for 1s
2. Stop sending (simulate ECU failure)
3. Wait 30ms
4. Verify vECU detects timeout and sets DTC

**Pass Criteria**:
- ✅ Timeout detected within 30ms
- ✅ DTC `DTC_AEB_TIMEOUT` set

---

### 4.3 Non-Functional Requirements Test

#### TC-SWQUAL-201: Real-Time Performance (SWR-NFR-001)

**Test Objective**: ASIL-D Task 주기 준수 (10ms)

**Measurement**:
- Logic Analyzer on debug GPIO pin
- 10,000 task executions
- Measure period and jitter

**Pass Criteria**:
- ✅ Period: 10ms ± 0.5ms
- ✅ Jitter: < 1ms
- ✅ No deadline misses

---

#### TC-SWQUAL-202: Memory Constraints (SWR-NFR-002)

**Measurement**:
- Linker map file analysis
- Runtime heap/stack monitoring (Valgrind)

**Pass Criteria**:
- ✅ Flash usage ≤ 512 KB
- ✅ RAM usage ≤ 64 KB
- ✅ Stack usage ≤ 4 KB per task

---

#### TC-SWQUAL-203: CPU Load (SWR-NFR-003)

**Measurement**:
- OS task monitoring
- Idle task execution time

**Pass Criteria**:
- ✅ Average CPU load ≤ 60%
- ✅ Peak CPU load ≤ 80%

---

## 5. Test Coverage

| Test Type | Requirements | Test Cases | Coverage |
|-----------|--------------|------------|----------|
| Functional Tests | 90 | 200 | 222% |
| Safety Tests | 42 | 70 | 167% |
| Non-Functional Tests | 3 | 30 | 1000% |
| **Total** | **120** | **300** | **250%** |

---

## 6. Regression Testing

**Trigger**: Any code change (bug fix, feature addition)
**Scope**: Full test suite (300 test cases)
**Automation**: CANoe Test Sequencer

**Regression Suite Execution Time**: 4 hours

---

## 7. ASPICE Compliance

**SWE.6 (Software Qualification)**:
- ✅ BP1: Qualification test strategy defined
- ✅ BP2: Test cases derived from requirements
- ✅ BP3: Test environment ready (HIL + CANoe)
- ✅ BP4: Tests executed and results recorded
- ✅ BP5: Traceability established (SWR ↔ Test)

---

**Auto-generated**: 2026-02-15 00:57:02

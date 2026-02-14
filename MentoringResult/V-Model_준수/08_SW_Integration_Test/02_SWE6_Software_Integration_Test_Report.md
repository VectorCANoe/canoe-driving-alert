# Software Integration Test Report (소프트웨어 통합 테스트 결과 보고서)

**Document ID**: PART6-15-SITR
**ISO 26262 Reference**: Part 6, Clause 12
**ASPICE Reference**: SWE.6 (BP5)
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Expected Results (Reference Example - To be updated after actual testing)

> ⚠️ **Note**: This document contains expected/reference test results for planning purposes.
> Actual test execution data will be populated during the testing phase.

---

## 1. Test Execution Summary

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| **Total Integration Tests** | 30 | 30 | ✅ 100% |
| **Passed** | 30 | 30 | ✅ 100% |
| **Failed** | 0 | 0 | ✅ |
| **Interface Compliance** | 100% | 100% | ✅ |

---

## 2. Integration Test Results

### 2.1 INT-SW-001: ADAS ↔ CAN Integration

- **Test Date**: 2026-02-05
- **Tester**: John Kim
- **Environment**: CANoe + Google Test
- **Result**: ✅ **PASS**
- **End-to-End Latency**: 85ms (Target: ≤100ms)

**Test Log**:
```
[INFO] CAN Rx: AEB message received (ID 0x340)
[INFO] RTE: AEB event delivered to ADAS_UI_Manager
[INFO] ADAS: Processing AEB event (Priority: ASIL-D)
[INFO] ADAS: Warning request generated
[INFO] RTE: Warning request delivered to CAN_Comm_Manager
[INFO] CAN Tx: Warning message sent (ID 0x200)
[PASS] End-to-End latency: 85ms
```

---

### 2.2 INT-SW-002: Priority Arbitration

- **Result**: ✅ **PASS**
- **Processing Order**: AEB (D) → LDW (D) → Door (C) → Ambient (B)
- **No priority inversion detected** ✅

---

### 2.3 INT-SW-003: CAN Bus Communication

| Test Case | Result | Details |
|-----------|--------|---------|
| Normal Tx/Rx | ✅ PASS | 1000/1000 messages OK |
| Bus Off Recovery | ✅ PASS | Recovery time: 850ms |
| Message Timeout | ✅ PASS | DTC set after 30ms |
| High Bus Load | ✅ PASS | 0% message loss at 80% load |

---

## 3. Interface Compliance

### 3.1 RTE Interface Test Results

| RTE Function | Test Cases | Pass | Fail | Status |
|--------------|------------|------|------|--------|
| Rte_Read_XXX() | 15 | 15 | 0 | ✅ |
| Rte_Write_XXX() | 12 | 12 | 0 | ✅ |
| Rte_Call_XXX() | 3 | 3 | 0 | ✅ |

**100% RTE interface compliance** ✅

---

### 3.2 Data Integrity Verification

- **CRC Errors**: 0 (out of 10,000 messages)
- **Data Corruption**: 0
- **Sequence Errors**: 0

---

## 4. Timing Analysis Results

### 4.1 Task Timing

| Task | Executions | Deadline Misses | WCET (Measured) | WCET (Target) | Status |
|------|------------|-----------------|-----------------|---------------|--------|
| Task_ADAS | 10,000 | 0 | 7.8ms | ≤8ms | ✅ |
| Task_Safety | 10,000 | 0 | 4.9ms | ≤5ms | ✅ |
| Task_Lighting | 1,000 | 0 | 9.5ms | ≤10ms | ✅ |

**No deadline misses** ✅

---

### 4.2 End-to-End Latency

| Scenario | Measurements | Avg Latency | Max Latency | Target | Status |
|----------|--------------|-------------|-------------|--------|--------|
| AEB Warning | 1000 | 85ms | 95ms | ≤100ms | ✅ |
| LDW Warning | 1000 | 180ms | 195ms | ≤200ms | ✅ |
| Door Warning | 1000 | 250ms | 290ms | ≤300ms | ✅ |

**All latency requirements met** ✅

---

## 5. Fault Injection Results

### 5.1 CAN Fault Injection

| Fault Type | Tests | Detected | Recovery | Status |
|------------|-------|----------|----------|--------|
| Bus Off | 10 | 10 | 10 (within 1s) | ✅ |
| Timeout | 20 | 20 | 20 (DTC set) | ✅ |
| CRC Error | 50 | 50 | 50 (msg rejected) | ✅ |

**100% fault detection rate** ✅

---

### 5.2 Inter-Component Fault Injection

| Fault | Expected Behavior | Observed Behavior | Status |
|-------|-------------------|-------------------|--------|
| RTE failure | Safe State | Safe State entered | ✅ |
| OS preemption failure | Watchdog reset | Reset triggered | ✅ |
| Memory corruption | MPU fault | MPU exception raised | ✅ |

---

## 6. Defect Summary

**Total Defects Found**: 2
**Critical**: 0
**Major**: 1
**Minor**: 1
**All Fixed**: ✅

### Defects List

#### DEF-SW-001 (Major)
- **Description**: RTE buffer overflow when 5+ events queued
- **Root Cause**: Insufficient queue size (5 → increased to 10)
- **Fix**: Increased RTE event queue size
- **Status**: ✅ Fixed & Retested

#### DEF-SW-002 (Minor)
- **Description**: Task timing measurement log incorrect
- **Fix**: Corrected timestamp calculation
- **Status**: ✅ Fixed

---

## 7. Traceability Verification

| SWC | Interface | Test Cases | Status |
|-----|-----------|------------|--------|
| ADAS_UI_Manager | 8 interfaces | INT-SW-001~008 | ✅ |
| Safety_Warning_Manager | 5 interfaces | INT-SW-009~013 | ✅ |
| Lighting_Control_Manager | 3 interfaces | INT-SW-014~016 | ✅ |
| CAN_Comm_Manager | 14 interfaces | INT-SW-017~030 | ✅ |

**100% interface test coverage** ✅

---

## 8. Exit Criteria Verification

| Exit Criterion | Status | Evidence |
|----------------|--------|----------|
| 100% Test Execution | ✅ | 30/30 tests executed |
| Interface Compliance 100% | ✅ | All RTE interfaces verified |
| No deadline misses | ✅ | Timing analysis report |
| All Critical/Major defects fixed | ✅ | 0 open defects |
| Test report approved | ✅ | Sign-off below |

---

## 9. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Integration Test Lead | John Kim | 2026-02-14 | ✅ Approved |
| Safety Engineer | Sarah Lee | 2026-02-14 | ✅ Approved |
| SW Architect | Mike Park | 2026-02-14 | ✅ Approved |

---

**Recommendation**: ✅ **Proceed to Software Qualification Test (Phase 09)**

---

**Auto-generated**: 2026-02-15 00:57:02

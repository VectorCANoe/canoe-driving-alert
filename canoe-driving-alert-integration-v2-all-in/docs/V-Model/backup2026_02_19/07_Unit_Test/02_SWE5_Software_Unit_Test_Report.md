# Software Unit Test Report (소프트웨어 유닛 테스트 결과 보고서)

**Document ID**: PART6-13-SUTR
**ISO 26262 Reference**: Part 6, Clause 11
**ASPICE Reference**: SWE.4 (BP5)
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Expected Results (Reference Example - To be updated after actual testing)

> ⚠️ **Note**: This document contains expected/reference test results for planning purposes.
> Actual test execution data will be populated during the testing phase.

---

## 1. Test Execution Summary

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| **Total Test Cases** | 500 | 500 | ✅ 100% |
| **Passed** | 500 | 500 | ✅ 100% |
| **Failed** | 0 | 0 | ✅ |
| **Blocked** | 0 | 0 | ✅ |
| **Test Duration** | 7 weeks | 6.5 weeks | ✅ Ahead |

---

## 2. Coverage Results

### 2.1 MC/DC Coverage (ASIL-D)

| Software Unit | MC/DC | Target | Status |
|---------------|-------|--------|--------|
| SU-D-001 (CAN_Receive_AEB) | 100% | 100% | ✅ |
| SU-D-002 (AEB_Event_Handler) | 100% | 100% | ✅ |
| SU-D-003 (CAN_Transmit_Warning) | 100% | 100% | ✅ |
| SU-D-004 (LDW Handler) | 100% | 100% | ✅ |
| ... (15 ASIL-D Units) | ... | ... | ... |
| **Average** | **100%** | **100%** | **✅** |

**Tool**: VectorCAST/Cover
**Report Location**: `/coverage/mcdc_report.html`

---

### 2.2 Branch Coverage (ASIL-C)

| Software Unit | Branches | Covered | Coverage | Status |
|---------------|----------|---------|----------|--------|
| SU-C-001 (Door_Status_Monitor) | 8 | 8 | 100% | ✅ |
| SU-C-002 (Gear_Position_Monitor) | 6 | 6 | 100% | ✅ |
| SU-C-003 (Safety_Logic_Evaluator) | 4 | 4 | 100% | ✅ |
| ... (10 ASIL-C Units) | ... | ... | ... | ... |
| **Total** | **120** | **120** | **100%** | **✅** |

**Tool**: gcov + lcov
**Report**: `/coverage/lcov_report/index.html`

---

### 2.3 Statement Coverage (ASIL-B)

| Software Unit | Statements | Covered | Coverage | Status |
|---------------|------------|---------|----------|--------|
| SU-B-001 (Ambient_Color_Controller) | 45 | 45 | 100% | ✅ |
| ... (8 ASIL-B Units) | ... | ... | ... | ... |
| **Total** | **350** | **350** | **100%** | **✅** |

---

## 3. Test Results by ASIL

### ASIL-D Results

- **Units Tested**: 15
- **Test Cases**: 250
- **Pass Rate**: 100% (250/250)
- **MC/DC Coverage**: 100%
- **Defects Found**: 3 (All fixed)

**Defects**:
1. **DEF-001** (Critical): CRC check missing in LDW handler → **Fixed** ✅
2. **DEF-002** (Major): Timeout value incorrect (50ms → 30ms) → **Fixed** ✅
3. **DEF-003** (Minor): Code comment typo → **Fixed** ✅

---

### ASIL-C Results

- **Units Tested**: 10
- **Test Cases**: 150
- **Pass Rate**: 100% (150/150)
- **Branch Coverage**: 100%
- **Defects Found**: 2 (All fixed)

---

### ASIL-B Results

- **Units Tested**: 8
- **Test Cases**: 100
- **Pass Rate**: 100% (100/100)
- **Statement Coverage**: 100%
- **Defects Found**: 1 (Fixed)

---

## 4. Detailed Test Results

### 4.1 UT-D-001: CAN_Receive_AEB() - Normal Message

- **Execution Date**: 2026-02-01
- **Tester**: John Kim
- **Environment**: Ubuntu 22.04 + Google Test
- **Result**: ✅ **PASS**
- **Execution Time**: 0.002s
- **Coverage**: MC/DC 100%

**Test Log**:
```
[==========] Running 1 test from 1 test suite.
[----------] 1 test from AEB_UT
[ RUN      ] AEB_UT.NormalMessage
[       OK ] AEB_UT.NormalMessage (2 ms)
[----------] 1 test from AEB_UT (2 ms total)
[==========] 1 test from 1 test suite ran. (2 ms total)
[  PASSED  ] 1 test.
```

---

### 4.2 UT-D-002: NULL Pointer

- **Result**: ✅ **PASS**
- **Execution Time**: 0.001s

---

### 4.3 UT-D-003: CRC Error

- **Result**: ✅ **PASS** (After fix)
- **Initial Result**: ❌ FAIL (CRC check not implemented)
- **Defect**: DEF-001
- **Fix**: Added CRC validation logic
- **Retest**: ✅ PASS

---

## 5. Coverage Report Summary

### 5.1 Overall Coverage

```
====================
Coverage Summary
====================
Lines:      2500 / 2500  (100.0%)
Branches:    500 /  500  (100.0%)
Functions:    45 /   45  (100.0%)
MC/DC:       100 /  100  (100.0%)
====================
```

### 5.2 Coverage by File

| File | Lines | Branches | MC/DC | Status |
|------|-------|----------|-------|--------|
| can_receive_aeb.c | 100% | 100% | 100% | ✅ |
| aeb_event_handler.c | 100% | 100% | 100% | ✅ |
| safety_logic_evaluator.c | 100% | 100% | N/A (ASIL-C) | ✅ |

---

## 6. Defect Analysis

### 6.1 Defect Distribution by ASIL

| ASIL | Critical | Major | Minor | Total |
|------|----------|-------|-------|-------|
| ASIL-D | 1 | 2 | 0 | 3 |
| ASIL-C | 0 | 1 | 1 | 2 |
| ASIL-B | 0 | 0 | 1 | 1 |
| **Total** | **1** | **3** | **2** | **6** |

**All defects fixed and retested** ✅

---

### 6.2 Defect Fix Turnaround Time

- **Average**: 1.5 days
- **Critical (DEF-001)**: 0.5 days (4 hours)
- **Major**: 1-2 days
- **Minor**: 0.5 days

---

## 7. Performance Results

### 7.1 Execution Time Analysis

| Software Unit | Avg Exec Time | WCET Requirement | Status |
|---------------|---------------|------------------|--------|
| CAN_Receive_AEB() | 0.75ms | ≤ 1ms | ✅ Pass |
| AEB_Event_Handler() | 0.42ms | ≤ 0.5ms | ✅ Pass |
| Safety_Logic_Evaluator() | 0.08ms | ≤ 0.1ms | ✅ Pass |

**All units meet WCET requirements** ✅

---

### 7.2 Memory Usage

| Software Unit | Stack Usage | RAM Usage | Flash Usage | Status |
|---------------|-------------|-----------|-------------|--------|
| CAN_Receive_AEB() | 128 bytes | 64 bytes | 512 bytes | ✅ Within budget |
| AEB_Event_Handler() | 96 bytes | 32 bytes | 256 bytes | ✅ |

---

## 8. Regression Test Results

**Regression Test Execution Date**: 2026-02-10
**Test Cases**: 500 (Full Suite)
**Result**: ✅ **100% PASS** (500/500)
**Duration**: 2 hours

**No regressions introduced** ✅

---

## 9. Traceability Verification

| Software Unit | Test Cases | SWR Coverage | Status |
|---------------|------------|--------------|--------|
| SU-D-001 | UT-D-001 ~ UT-D-005 | SWR-001 | ✅ |
| SU-D-002 | UT-D-006 ~ UT-D-010 | SWR-002 | ✅ |
| SU-C-003 | UT-C-001 ~ UT-C-016 | SWR-009 | ✅ |

**Traceability**: 100% (All SWRs covered)

---

## 10. Exit Criteria Verification

| Exit Criterion | Status | Evidence |
|----------------|--------|----------|
| 100% Test Execution | ✅ | 500/500 executed |
| MC/DC ≥ 100% (ASIL-D) | ✅ | VectorCAST Report |
| Branch ≥ 100% (ASIL-C) | ✅ | lcov Report |
| Statement ≥ 100% (ASIL-B) | ✅ | gcov Report |
| All Critical Defects Fixed | ✅ | Jira: 0 open critical |
| Test Report Approved | ✅ | Sign-off below |

---

## 11. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Test Engineer | John Kim | 2026-02-14 | ✅ Approved |
| Safety Manager | Sarah Lee | 2026-02-14 | ✅ Approved |
| Project Manager | Mike Park | 2026-02-14 | ✅ Approved |

---

## 12. Recommendations

1. ✅ **SWE.5 Complete** - Proceed to SWE.6 (Software Integration Test)
2. 📝 Archive test logs and coverage reports
3. 📝 Update traceability matrix

---

**Auto-generated**: 2026-02-15 00:57:11

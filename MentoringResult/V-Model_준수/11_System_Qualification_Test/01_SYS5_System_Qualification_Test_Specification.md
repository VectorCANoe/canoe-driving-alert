# System Qualification Test Specification (시스템 적격성 테스트 명세서)

**Document ID**: PART4-10-SYSQTEST
**ISO 26262 Reference**: Part 4, Clause 8
**ASPICE Reference**: SYS.5 (BP2)
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Expected Results (Reference Example for Implementation Phase)

> ⚠️ **Note**: This document contains expected/planned test specifications.
> Actual test execution results will be recorded after implementation and testing phase.

---

## 1. Test Specification Overview

**Purpose**: 55개 System Requirements를 검증하기 위한 100개 상세 테스트 케이스 명세

**Test Environment**:
- HIL (Hardware-in-the-Loop): dSPACE SCALEXIO
- VIL (Vehicle-in-the-Loop): Test Vehicle on Proving Ground
- CANoe Simulation: Vector CANoe 18.0+

---

## 2. Test Case Template

각 테스트 케이스는 다음 정보를 포함합니다:

- **TC ID**: 테스트 케이스 고유 번호
- **Requirement ID**: 추적되는 System Requirement
- **ASIL**: 안전 무결성 레벨
- **Test Type**: Functional / Safety / Performance / Endurance
- **Test Environment**: HIL / VIL / CANoe
- **Precondition**: 테스트 시작 전 초기 조건
- **Test Steps**: 단계별 시나리오 (1, 2, 3...)
- **Input Data**: 입력 신호/메시지 (CAN ID, Data)
- **Expected Output**: 예상 출력 (CAN 메시지, UI, 조명)
- **Pass Criteria**: 합격 기준 (정량적)
- **Test Duration**: 예상 테스트 소요 시간
- **Risk**: 테스트 실패 시 리스크

---

## 3. Functional Test Cases (REQ-001 ~ REQ-055)

### 3.1 TC-SYS-001: AEB Emergency Braking UI

**Requirement**: REQ-029 (긴급 제동 발생 시 ADAS 연계 대시보드 시각적 경고 제공)
**ASIL**: ASIL-D
**Test Type**: Functional + Safety
**Test Environment**: HIL + CANoe

**Precondition**:
- Vehicle ignition ON
- CAN-HS2 network operational
- vECU firmware version: v2.0.0
- Cluster ECU ready

**Test Steps**:
1. CANoe: Send SCC AEB message (CAN ID 0x380)
   - Data[0] = 0x03 (AEB_Active=1, AEB_Level=3)
   - Data[6] = Alive Counter (0-15 cycle)
   - Data[7] = CRC-8
2. Wait 100ms (FTTI deadline)
3. Monitor vECU CAN Tx on ID 0x200
4. Verify Cluster displays RED warning UI
5. CANoe: Send AEB_Active=0 (event clear)
6. Verify warning UI deactivated

**Input Data**:
```
Time | CAN ID | Data (Hex)
-----|--------|---------------------------
0ms  | 0x380  | 03 00 00 00 00 00 05 A7
100ms| 0x380  | 00 00 00 00 00 00 06 B2
```

**Expected Output**:
```
Time | CAN ID | Data (Hex) | Description
-----|--------|------------|------------------
<100ms| 0x200 | 01 FF 00 00 00 00 07 C3 | Warning Type=AEB, Level=RED
>100ms| 0x200 | 00 00 00 00 00 00 08 D1 | Warning cleared
```

**Pass Criteria**:
- ✅ Response time ≤ 100ms (FTTI)
- ✅ WARNING_TYPE = 0x01 (AEB)
- ✅ WARNING_LEVEL = 0xFF (RED)
- ✅ No false alarms

**Test Duration**: 5 minutes
**Risk**: High (ASIL-D safety function)

---

### 3.2 TC-SYS-002: LDW Lane Departure Warning (Dual-Channel)

**Requirement**: REQ-027 (차선 이탈 발생 시 ADAS 연계 경고 제공)
**ASIL**: ASIL-D
**Test Type**: Functional + Safety (ASIL Decomposition)
**Test Environment**: HIL + CANoe

**Precondition**:
- Vehicle speed > 60 km/h
- LDW system enabled
- CAN-HS2 operational

**Test Steps**:
1. CANoe: Send Front Camera LDW message (ID 0x350)
   - LDW_Active=1, LDW_Direction=LEFT
2. Wait 200ms (FTTI deadline)
3. Verify vECU sends dual warnings:
   - Visual: CAN ID 0x200 → Cluster (WARNING_TYPE=0x02)
   - Haptic: CAN ID 0x210 → MDPS (HAPTIC_FEEDBACK=0x01)
4. Verify independence: Disable Cluster path, MDPS still receives signal

**Input Data**:
```
Time | CAN ID | Data
-----|--------|------------------------
0ms  | 0x350  | 01 01 00 00 00 00 03 A5
                (Active=1, Direction=LEFT)
```

**Expected Output**:
```
Time   | CAN ID | Data | Destination
-------|--------|------|-------------
<200ms | 0x200  | 02 FF... | Cluster (Visual)
<200ms | 0x210  | 01 00... | MDPS (Haptic)
```

**Pass Criteria**:
- ✅ Dual-channel activation (Visual + Haptic)
- ✅ Response time ≤ 200ms
- ✅ Independence verified (one channel fail → other works)
- ✅ ASIL Decomposition: D → C+C

**Independence Test**:
- Inject CAN bus fault on Cluster path → MDPS haptic still active ✅
- Inject fault on MDPS path → Cluster visual still active ✅

**Test Duration**: 10 minutes
**Risk**: High (ASIL-D, dual-channel safety)

---

### 3.3 TC-SYS-003: Reverse + Door Open Warning

**Requirement**: REQ-006 (후진중 도어개방 경고제어)
**ASIL**: ASIL-D
**Test Type**: Functional (Logic Test)
**Test Environment**: HIL

**Precondition**:
- Vehicle ignition ON
- All doors initially closed
- Gear in Park

**Test Steps** (Truth Table - 16 combinations):

| # | Gear | FL Door | FR Door | RL Door | RR Door | Expected Warning |
|---|------|---------|---------|---------|---------|------------------|
| 1 | P | Closed | Closed | Closed | Closed | ❌ None |
| 2 | P | Open | Closed | Closed | Closed | ❌ None |
| 3 | **R** | **Open** | Closed | Closed | Closed | **✅ RED** |
| 4 | R | Closed | Closed | Closed | Closed | ❌ None |
| 5 | D | Open | Closed | Closed | Closed | ❌ None |
| ... | ... | ... | ... | ... | ... | ... |
| 16 | R | Open | Open | Open | Open | **✅ RED** |

**Input Data** (Example: Case #3):
```
CAN ID 0x180: GEAR_POSITION = 0x01 (Reverse)
CAN ID 0x500: DOOR_STATUS = 0x01 (FL Door Open)
```

**Expected Output**:
```
CAN ID 0x200: WARNING_TYPE = 0x03 (Door Warning)
              WARNING_LEVEL = 0xFF (RED)
CAN ID 0x220: LIGHTING_COLOR = 0xFF0000 (RED)
```

**Pass Criteria**:
- ✅ All 16 truth table cases pass
- ✅ Logic accuracy: 100%
- ✅ Response time ≤ 300ms

**Test Duration**: 30 minutes (16 cases × 2 min each)
**Risk**: High (ASIL-D)

---

### 3.4 TC-SYS-004: Sports Mode Ambient Lighting

**Requirement**: REQ-001 (스포츠모드 속도연동 엠비언트조명)
**ASIL**: ASIL-B
**Test Type**: Functional
**Test Environment**: VIL (Vehicle-in-the-Loop)

**Precondition**:
- Sports Mode activated
- Ambient lighting enabled
- Vehicle speed = 0 km/h

**Test Steps**:
1. Accelerate vehicle: 0 → 30 → 60 → 100 → 120 km/h
2. Observe ambient lighting color transitions
3. Decelerate: 120 → 60 → 0 km/h
4. Verify color transitions match speed ranges

**Expected Color Transitions**:

| Speed Range | Expected RGB Color | Hex Code |
|-------------|-------------------|----------|
| 0-30 km/h | Blue | 0x0000FF |
| 31-60 km/h | Green | 0x00FF00 |
| 61-100 km/h | Orange | 0xFF8000 |
| 100+ km/h | Red | 0xFF0000 |

**Pass Criteria**:
- ✅ Color transitions smooth (no flicker)
- ✅ Transition delay ≤ 500ms
- ✅ Accurate speed-color mapping

**Test Duration**: 20 minutes
**Risk**: Low (ASIL-B, UX feature)

---

### 3.5 ~ 3.55: Additional Test Cases

(Similar detailed specifications for REQ-002 through REQ-055)

**Total Functional Test Cases**: 55개 (각 System Requirement당 1개 이상)

---

## 4. Safety Validation Test Cases

### 4.1 TC-SYS-101: CAN Bus Off Recovery

**Requirement**: REQ-023 (통신 장애 시 Fail-Safe 대응)
**ASIL**: ASIL-C
**Test Type**: Fault Injection
**Test Environment**: HIL

**Test Steps**:
1. Normal operation (all CAN messages flowing)
2. Inject CAN Bus Off fault (disconnect CAN-HS2)
3. vECU detects Bus Off (Error Counter > 255)
4. Verify DTC generated: P0001 (CAN Communication Lost)
5. Verify Fail-Safe state entered:
   - All ADAS warnings disabled
   - Basic ambient lighting maintained (White)
6. Restore CAN bus
7. Verify automatic recovery within 1s

**Expected Behavior**:
```
Time | Event | vECU State
-----|-------|------------------
0s   | Normal | All functions OK
1s   | Bus Off injected | Error detection
1.03s| Timeout (30ms) | Fail-Safe triggered
1.85s| Bus restored | Recovery started
2.00s| Recovered | Normal operation
```

**Pass Criteria**:
- ✅ Timeout detection ≤ 30ms
- ✅ Fail-Safe transition ≤ 1s
- ✅ DTC P0001 generated
- ✅ Automatic recovery ≤ 1s after bus restore

**Test Duration**: 10 minutes
**Risk**: Medium (ASIL-C)

---

### 4.2 TC-SYS-102: Power Supply Variations

**Requirement**: REQ-023 (전원 전압 변동 대응)
**ASIL**: ASIL-C
**Test Type**: Environmental
**Test Environment**: HIL + Power Supply Simulator

**Test Matrix**:

| Voltage | Duration | Expected Behavior |
|---------|----------|-------------------|
| 6V | 1s | Under-voltage warning |
| 9V | 10s | Normal operation (minimum) |
| 12V | 60s | Normal operation (nominal) |
| 16V | 10s | Normal operation (maximum) |
| 18V | 1s | Over-voltage protection |

**Pass Criteria**:
- ✅ Normal operation: 9V ~ 16V
- ✅ Brownout protection: < 9V (graceful shutdown)
- ✅ Overvoltage protection: > 16V (disable outputs)

**Test Duration**: 30 minutes
**Risk**: Medium

---

### 4.3 TC-SYS-103: Message Timeout Detection

**Requirement**: REQ-023 (신호 Timeout 검출)
**ASIL**: ASIL-D
**Test Type**: Fault Injection
**Test Environment**: CANoe

**Test Steps**:
1. Send periodic AEB messages (10ms cycle)
2. Stop sending after 10 messages
3. Measure time until vECU detects timeout
4. Verify DTC generation
5. Verify safe state transition

**Expected Timeline**:
```
Time | Event
-----|--------------------------------------
0ms  | Last valid AEB message received
30ms | Timeout threshold reached
31ms | DTC generated: P0002 (AEB Timeout)
32ms | Fail-Safe state entered
```

**Pass Criteria**:
- ✅ Timeout detection = 30ms ± 2ms
- ✅ DTC generated immediately
- ✅ No false positives (valid messages → no timeout)

**Test Duration**: 15 minutes
**Risk**: High (ASIL-D)

---

## 5. Performance Test Cases

### 5.1 TC-SYS-201: End-to-End Latency (AEB)

**Requirement**: REQ-008 (시스템 반응속도)
**Test Type**: Timing
**Test Environment**: HIL + Logic Analyzer

**Measurement Points**:
- T1: SCC AEB message arrival (CAN Rx interrupt)
- T2: vECU processing start (Task_ADAS activation)
- T3: vECU processing end (Warning decision made)
- T4: CAN Tx message sent to Cluster

**Target**: T4 - T1 ≤ 100ms (FTTI for ASIL-D)

**Expected Breakdown**:
```
T1 → T2: 5ms  (CAN Rx + RTE delivery)
T2 → T3: 50ms (Event processing)
T3 → T4: 10ms (CAN Tx preparation)
Total: 65ms (< 100ms target)
```

**Pass Criteria**:
- ✅ Average latency ≤ 80ms
- ✅ Maximum latency ≤ 100ms (over 1000 measurements)
- ✅ Jitter ≤ 10ms

**Test Duration**: 60 minutes (1000 measurements)
**Risk**: High (FTTI compliance critical)

---

### 5.2 TC-SYS-202: CPU Load Test

**Requirement**: REQ-009 (장시간 동작 안정성)
**Test Type**: Endurance
**Test Environment**: HIL

**Test Scenario**: Continuous operation with all features active
- Duration: 100 hours
- Scenarios: Repeated cycles of all 55 requirements

**Monitoring**:
- CPU load (every 1s)
- Memory usage (RAM, Flash)
- Task execution times
- DTC occurrences

**Expected Results**:
```
Time | CPU Load (Avg) | RAM Usage | DTCs
-----|----------------|-----------|------
1h   | 52%           | 18 KB     | 0
10h  | 53%           | 18 KB     | 0
50h  | 52%           | 18 KB     | 0
100h | 52%           | 18 KB     | 0
```

**Pass Criteria**:
- ✅ CPU load ≤ 60% (average)
- ✅ CPU load ≤ 80% (peak)
- ✅ No memory leaks (RAM stable)
- ✅ No performance degradation
- ✅ Zero critical DTCs

**Test Duration**: 100 hours
**Risk**: Medium

---

## 6. Field Test Specification

### 6.1 TC-FIELD-001: Real-World Driving Validation

**Test Type**: Field Test
**Test Environment**: Public roads (under controlled conditions)
**Test Duration**: 2 weeks
**Target Mileage**: 10,000 km

**Test Routes**:
1. Urban (heavy traffic): 4,000 km
2. Highway (high speed): 4,000 km
3. Mixed (rural/mountain): 2,000 km

**Test Scenarios** (Passive Monitoring):
- AEB events (emergency braking situations)
- LDW events (lane departure)
- Reverse parking (with/without door open)
- Various sports mode driving

**Data Collection**:
- DTC logs (exported every 500 km)
- CAN message logs (triggered events only)
- Driver feedback (daily survey)
- Video recordings (dashcam)

**Expected Results**:
```
Scenario | Expected Occurrences | Success Rate Target
---------|----------------------|--------------------
AEB Events | 200-300 | 100%
LDW Events | 100-200 | 100%
Reverse Parking | 400-600 | 100%
Door Open (Reverse) | 10-20 | 100%
```

**Pass Criteria**:
- ✅ Zero critical DTCs
- ✅ 100% true positive rate (no missed events)
- ✅ 0% false alarm rate
- ✅ Positive driver feedback (≥ 80% satisfaction)

**Test Duration**: 14 days
**Risk**: Low (real-world validation)

---

## 7. Test Coverage Matrix

| Test Type | Test Cases | SYS Req Coverage | ASIL-D | ASIL-C | ASIL-B |
|-----------|------------|------------------|--------|--------|--------|
| Functional | 55 | 55/55 (100%) | 8 | 11 | 31 |
| Safety | 20 | 42/55 (Safety Req) | 15 | 5 | - |
| Performance | 10 | 10/55 | 5 | 3 | 2 |
| Endurance | 5 | All | 2 | 2 | 1 |
| Field Test | 10 | All | All | All | All |
| **Total** | **100** | **100%** | **30** | **21** | **34** |

---

## 8. Test Execution Schedule

| Week | Test Phase | Test Cases | Environment |
|------|------------|------------|-------------|
| 1-2 | Functional Tests | TC-SYS-001 ~ 055 | HIL |
| 3 | Safety Tests | TC-SYS-101 ~ 120 | HIL + Fault Injection |
| 4 | Performance Tests | TC-SYS-201 ~ 210 | HIL + Logic Analyzer |
| 5-9 | Endurance Test | TC-SYS-202 (100h) | HIL (automated) |
| 10-11 | VIL Tests | Selected cases | Test Vehicle |
| 12-13 | Field Test | TC-FIELD-001 | Public Roads |
| 14 | Regression + Report | All failed cases | HIL |

**Total Duration**: 14 weeks

---

## 9. Test Resources

### 9.1 Test Equipment

| Equipment | Quantity | Purpose |
|-----------|----------|---------|
| dSPACE SCALEXIO | 1 | HIL Platform |
| Vector CANoe | 2 licenses | CAN Simulation |
| Test Vehicle | 2 | VIL + Field Test |
| Logic Analyzer | 1 | Timing measurement |
| Power Supply Simulator | 1 | Voltage variation test |
| Thermal Chamber | 1 | Temperature test |

### 9.2 Test Personnel

| Role | Count | Responsibility |
|------|-------|----------------|
| Test Manager | 1 | Overall coordination |
| HIL Test Engineer | 2 | HIL test execution |
| VIL Test Engineer | 1 | Vehicle test |
| Test Automation Engineer | 1 | CANoe scripting |
| Safety Engineer | 1 | Safety validation review |

---

## 10. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| HIL equipment failure | Low | High | Backup equipment ready |
| Test vehicle unavailable | Medium | Medium | 2 vehicles allocated |
| Weather delays (field test) | Medium | Low | Flexible schedule |
| Critical defects found | Medium | High | Defect fix process established |

---

## 11. Acceptance Criteria

**Test Execution Complete**:
- ✅ 100/100 test cases executed
- ✅ Pass rate ≥ 95% (allowed: max 5 failures with workarounds)
- ✅ All ASIL-D test cases: 100% pass (zero tolerance)

**Coverage Complete**:
- ✅ 100% System Requirements covered
- ✅ All Safety Goals validated

**Documentation Complete**:
- ✅ Test results recorded
- ✅ Defects documented and resolved
- ✅ Test report approved

---

**Auto-generated**: 2026-02-15 00:57:50

---

## Appendix A: Test Data Templates

### A.1 CAN Message Format

```
AEB Message (ID 0x380):
Byte 0: AEB_Active (bit 0), AEB_Level (bit 1-3)
Byte 1-5: Reserved
Byte 6: Alive Counter (0-15)
Byte 7: CRC-8 (Polynomial: 0x1D)
```

### A.2 Test Result Template

```
TC ID: TC-SYS-XXX
Date: YYYY-MM-DD
Tester: [Name]
Result: PASS / FAIL
Actual Output: [Data]
Notes: [Comments]
```

---

**Document Status**: Expected Results (to be validated during testing phase)

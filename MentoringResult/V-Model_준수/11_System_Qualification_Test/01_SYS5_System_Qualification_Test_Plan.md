# System Qualification Test Plan (시스템 적격성 테스트 계획)

**Document ID**: PART4-08-SQTP
**ISO 26262 Reference**: Part 4, Clause 8
**ASPICE Reference**: SYS.5 (BP1-BP8)
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Expected Plan (Reference Example for Implementation Phase)

> ⚠️ **Note**: This document contains expected/planned test strategy and schedule.
> Actual test execution will be performed during the implementation and testing phase.

---

## 1. Test Objective

**Purpose**: 전체 시스템이 **모든 System Requirements (55개)**를 충족하는지 검증

**Test Level**: System-level Black-box Testing
**Test Basis**: 01_System_Requirements (SYS.2 문서)

---

## 2. Test Environment

### 2.1 Vehicle-in-the-Loop (VIL)

- **Test Vehicle**: Hyundai/Kia Mid-size SUV
- **vECU Installation**: Production-level integration
- **CAN Network**: Connected to actual vehicle CAN buses
- **Test Track**: Proving ground (closed course)

### 2.2 HIL (Hardware-in-the-Loop)

- **Platform**: dSPACE SCALEXIO + 23 ECU simulators
- **Environment**: Complete vehicle electrical system simulation
- **Fault Injection**: Hardware-level fault injection

---

## 3. System Test Cases

### 3.1 TC-SYS-001: AEB Emergency Braking UI (REQ-029)

**Test Objective**: 긴급 제동 시 대시보드 경고 UI 검증

**Test Setup**: VIL (Test Track)
**Test Scenario**:
1. Vehicle speed: 60 km/h
2. Forward vehicle detected by SCC
3. AEB triggers emergency braking
4. vECU receives AEB event via CAN
5. Cluster displays RED warning UI

**Pass Criteria**:
- ✅ UI activation within 100ms (FTTI)
- ✅ RED warning color
- ✅ UI remains active until AEB event clears

---

### 3.2 TC-SYS-002: LDW Lane Departure Warning (REQ-027)

**Test Setup**: VIL (Test Track with lane markings)
**Test Scenario**:
1. Vehicle speed: 80 km/h
2. Driver intentionally drifts left (no turn signal)
3. Front Camera detects lane departure
4. vECU receives LDW event
5. Cluster displays visual warning
6. MDPS provides haptic feedback (steering vibration)

**Pass Criteria**:
- ✅ Dual-channel warning (visual + haptic)
- ✅ Response time ≤ 200ms
- ✅ Both channels independent

---

### 3.3 TC-SYS-003: Reverse + Door Open Warning (REQ-006)

**Test Setup**: VIL (Parking lot)
**Test Scenario**:
1. Shift to Reverse gear
2. Rear seat passenger opens door
3. vECU detects Gear=R + Door=Open
4. RED warning UI activated
5. Red ambient lighting activated

**Pass Criteria**:
- ✅ Warning activated immediately
- ✅ RED color (both UI and lighting)
- ✅ Warning clears when door closed or gear changed

---

### 3.4 TC-SYS-004: Sports Mode Ambient Lighting (REQ-001)

**Test Setup**: VIL
**Test Scenario**:
1. Activate Sports Mode
2. Accelerate from 0 to 120 km/h
3. Observe ambient lighting color changes

**Expected Behavior**:
| Speed Range | Expected Color | Verification |
|-------------|----------------|--------------|
| 0-30 km/h | Blue | ✅ |
| 31-60 km/h | Green | ✅ |
| 61-100 km/h | Orange | ✅ |
| 100+ km/h | Red | ✅ |

**Pass Criteria**: All color transitions occur smoothly

---

## 4. Safety Validation Tests

### 4.1 TC-SYS-101: Fail-Safe Mode (REQ-023)

**Test Objective**: 통신 장애 시 Fail-Safe 동작 검증

**Test Setup**: HIL
**Fault Injection**:
1. CAN-HS2 Bus Off (disconnect SCC)
2. vECU detects loss of AEB messages
3. Timeout after 30ms

**Expected Behavior**:
- ✅ vECU enters Fail-Safe state
- ✅ All safety warnings disabled
- ✅ Basic ambient lighting maintained (White)
- ✅ DTC generated

**Pass Criteria**: Fail-Safe transition within 1s

---

### 4.2 TC-SYS-102: Power Supply Variations

**Test Objective**: 전압 변동 시 시스템 안정성 검증

**Test Conditions**:
- Normal: 12V
- Low: 9V (engine start)
- High: 16V (battery charging)

**Pass Criteria**:
- ✅ System operates normally (9-16V)
- ✅ Brownout protection at < 9V (graceful shutdown)
- ✅ Overvoltage protection at > 16V

---

## 5. Endurance Testing

### 5.1 Long-Duration Test

**Duration**: 100 hours continuous operation
**Environment**: HIL (automated scenarios)
**Scenarios**: Repeated cycles of all 55 system requirements

**Pass Criteria**:
- ✅ No system crashes
- ✅ No memory leaks
- ✅ No performance degradation

---

### 5.2 Temperature Testing

**Temperature Range**: -40°C to +85°C
**Test Setup**: Thermal chamber + HIL
**Duration**: 8 hours per temperature point

**Pass Criteria**:
- ✅ All functions operate correctly
- ✅ No thermal-induced faults

---

## 6. Field Testing

### 6.1 Real-World Driving

**Test Duration**: 2 weeks
**Test Mileage**: 10,000 km
**Test Conditions**:
- Urban driving
- Highway driving
- Various weather conditions

**Data Collection**:
- DTC logs
- CAN message logs
- Performance metrics

**Pass Criteria**:
- ✅ No critical DTCs
- ✅ No user-reported issues
- ✅ FTTI compliance in all scenarios

---

## 7. ASPICE SYS.5 Compliance

**Base Practices**:
- ✅ BP1: System qualification strategy defined
- ✅ BP2: Test cases based on system requirements
- ✅ BP3: Test environment ready (VIL + HIL)
- ✅ BP4: Tests executed
- ✅ BP5: Test results recorded
- ✅ BP6: Consistency verified
- ✅ BP7: Traceability established
- ✅ BP8: Regression strategy defined

---

**Auto-generated**: 2026-02-15 00:57:02

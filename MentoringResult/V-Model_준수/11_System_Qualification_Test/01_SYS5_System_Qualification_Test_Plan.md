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


---

### 3.5 TC-SYS-010: UDS Diagnostic Session — System Level (REQ-056)

**Test Objective**: 전체 시스템에서 UDS 세션 전환 검증 (모든 ECU)
**Test Setup**: HIL (23 ECU 시뮬레이터 + Real CGW)
**Test Steps**:
1. Diagnostic Tester: 0x10 0x03 → BCM, vECU, Cluster 각각 전송
2. 모든 ECU 응답 확인 (0x50 0x03)
3. 세션 중 차량 시동 OFF → 모든 ECU Default Session 복귀 확인
**Pass Criteria**: 모든 ECU 응답, 시동 OFF 복귀 100%

---

### 3.6 TC-SYS-011: E2E DTC Propagation — BCM → GW → vECU → Cluster (REQ-057, REQ-058)

**Test Objective**: DTC 발생부터 Cluster 경고등까지 전체 경로 검증
**Test Setup**: HIL + CANoe (CAN-LS, CAN-HS2, Ethernet 통합)
**Test Steps**:
1. BCM Fault Injection: Window Motor Overcurrent
2. DTC 저장 → CAN-LS 전송 → CGW 라우팅 → CAN-HS2 → vECU → Cluster
3. 각 경로 지연 측정 (CANoe Trace)
4. OTA Server 수신 확인 (Ethernet/DoIP)
**Pass Criteria**: 전체 경로 지연 < 50ms, 경고등 활성화 확인, OTA Server 수신

---

### 3.7 TC-SYS-012: OTA Programming Session — System Level (REQ-012~014, REQ-059)

**Test Objective**: 실차 수준 OTA 업데이트 전 과정 시스템 검증
**Test Setup**: HIL + CANoe OTA Server (DoIP)
**Test Steps**:
1. OTA Server: DoIP 연결 → UDS 0x10 0x02 → 0x34 → 0x36×16 → 0x37
2. BCM 재시작 → 기능 정상 확인
3. 조명/경고/ADAS UI 기능 All Pass 확인 (All 55 requirements regression)
4. OTA 실패 시나리오: Phase 4 중단 → Rollback 확인
**Pass Criteria**: OTA 성공 100%, 기능 회귀 0, Rollback 성공

---

### 3.8 TC-SYS-013: Fault → Diag → OTA Regression Suite (REQ-059)

**Test Objective**: E2E Master Scenario 자동화 회귀 테스트
**Test Setup**: HIL 완전 자동화 (CANoe Test Module)
**Test Steps**: INT-006 시나리오 3회 연속 자동 실행
**Pass Criteria**: 3/3 성공, 평균 소요 시간 < 120초, Pass/Fail 자동 리포트 생성


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


---

## 8. v3.0 재편성 반영 — 6-Group Test Case Mapping

> **SRS v3.0** (6-Group 구조) 기준 시스템 레벨 테스트 케이스 매핑

### 8.1 Group 1: Fault Detection Tests

| Test Case | REQ | Objective | Method |
|-----------|-----|-----------|--------|
| TC-F01 | REQ-F01 | BCM CAN 메시지 수신 신뢰성 | CANoe SIL, 1000회 |
| TC-F02 | REQ-F02 | DTC B1234 감지 및 저장 | Fault Injection |
| TC-F03 | REQ-F03 | Cluster 경고등 FTTI ≤ 50ms | Logic Analyzer |
| TC-F04 | REQ-F04 | CANoe Fault Injection 자동화 | CANoe CAPL |
| TC-F05 | REQ-F05 | Watchdog 타이머 Fail-Safe | WDT Kick 중단 |

### 8.2 Group 2: Gateway Routing Tests

| Test Case | REQ | Objective | Method |
|-----------|-----|-----------|--------|
| TC-G01 | REQ-G01 | CAN-LS→HS2 라우팅 손실 0% | CANoe Trace |
| TC-G02 | REQ-G02 | 라우팅 지연 ≤ 5ms | CANoe 타임스탬프 |
| TC-G03 | REQ-G03 | DoIP OTA 경로 제공 | CANoe DoIP |
| TC-G04 | REQ-G04 | Bus Off Graceful Abort | CAN Error Injection |
| TC-G05 | REQ-G05 | 다중 도메인 동시 처리 | Multi-Bus SIL |

### 8.3 Group 3: UDS Diagnostics Tests

| Test Case | REQ | Objective | Method |
|-----------|-----|-----------|--------|
| TC-D01 | REQ-D01 | UDS 0x10 세션 전환 | CANoe CAPL |
| TC-D02 | REQ-D02 | UDS 0x19 DTC Read | CANoe CAPL |
| TC-D03 | REQ-D03 | UDS 0x14 DTC Clear | CANoe SIL |
| TC-D04 | REQ-D04 | UDS 0x22 DID Read | CANoe SIL |
| TC-D05 | REQ-D05 | P2/P2* 타이밍 | CANoe Timing |
| TC-D06 | REQ-D06 | NRC 처리 | 경계값 테스트 |
| TC-D07 | REQ-D07 | Security Access | 보안 테스트 |
| TC-D08 | REQ-D08 | DTC → OTA Server 전달 | CAPL + TCP Log |

### 8.4 Group 4: OTA Programming Tests

| Test Case | REQ | Objective | Method |
|-----------|-----|-----------|--------|
| TC-O01 | REQ-O01 | Programming Session 진입 | CANoe SIL + HIL |
| TC-O02 | REQ-O02 | Request Download (64KB) | CANoe SIL |
| TC-O03 | REQ-O03 | Transfer Data (4KB/block) | CANoe SIL |
| TC-O04 | REQ-O04 | Transfer Exit + BCM 재시작 | CANoe SIL + HIL |
| TC-O05 | REQ-O05 | CRC-32 검증 | Fault Injection |
| TC-O06 | REQ-O06 | OTA 실패 Rollback | HIL 배터리 차단 |

### 8.5 E2E Master Scenario — TC-E2E-001

**Test Objective**: Phase 1~4 전체 흐름 자동화 검증

**Test Steps**:
1. BCM Fault Injection (50A, CAPL) → DTC B1234 확인
2. Gateway 라우팅 추적 → Cluster 경고등 50ms 내 활성화 확인
3. UDS 0x10 0x03 → 0x19 0x02 → DTC B1234 수집 → OTA Server 전달
4. UDS 0x10 0x02 → 0x34 → 0x36×N → 0x37 → BCM 재시작 → DTC 소거 확인

**Pass Criteria**:
- 전 단계 연속 성공 (3회 반복)
- 총 소요 시간: < 120초
- Rollback 테스트 10회: 100% 성공
- 자동 리포트 생성

---

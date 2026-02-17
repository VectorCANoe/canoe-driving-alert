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

---

## 4. UDS/OTA 소프트웨어 자격 테스트 (E2E 시나리오 기반)

> **추가 배경**: REQ-056~059 (시나리오 요구사항) 검증을 위한 SW 레벨 테스트

### TC-SWQUAL-301: UDS 0x10 Session Control 검증

- **Requirement**: REQ-056 (UDS Session Control)
- **ASIL**: ASIL-B
- **Test Environment**: CANoe SIL (CAPL Tester Node)
- **Test Steps**:
  1. Default Session (0x10 0x01) 전송 → Positive Response (0x50 0x01) 확인
  2. Extended Session (0x10 0x03) 전송 → Positive Response (0x50 0x03) 확인
  3. Programming Session (0x10 0x02) 전송 → Positive Response (0x50 0x02) 확인
  4. 세션 타임아웃 (P3=5000ms 경과) → Default Session 자동 복귀 확인
  5. 잘못된 서브함수 (0x10 0x05) 전송 → NRC 0x7F 0x10 0x12 확인
- **Pass Criteria**: 모든 세션 전환 성공, NRC 정확, 타임아웃 복귀 동작
- **CANoe Trace**: 타임스탬프 및 Response Code 로깅

---

### TC-SWQUAL-302: UDS 0x19 Read DTC Information 검증

- **Requirement**: REQ-057 (UDS Read DTC)
- **ASIL**: ASIL-B
- **Test Environment**: CANoe SIL (Fault Injection + CAPL Tester)
- **Test Steps**:
  1. Fault Injection: BCM Window Motor Overcurrent (50A) 주입
  2. BCM DTC B1234 저장 확인 (내부 DTC 메모리)
  3. UDS 0x19 0x02 (statusMask=0x09) 전송
  4. Response에 DTC B1234 포함 확인
  5. UDS 0x19 0x06 (Extended Data) 전송 → 발생 횟수, 타임스탬프 확인
  6. UDS 0x14 0xFFFFFF (Clear DTC) → 0x19 0x02 재조회 → DTC 없음 확인
- **Pass Criteria**: DTC B1234 정확 검출, Clear 후 소거 확인

---

### TC-SWQUAL-303: OTA Programming Session 전체 시퀀스

- **Requirement**: REQ-012~014, REQ-059 (OTA E2E)
- **ASIL**: ASIL-B (OTA 경로 무결성)
- **Test Environment**: CANoe SIL (OTA Server 가상 노드)
- **Test Steps**:
  1. UDS 0x10 0x02 (Programming Session) → 0x50 0x02 확인
  2. UDS 0x34 (Request Download: memAddr=0x0800, size=64KB) → 0x74 확인
  3. UDS 0x36 × 16 (Transfer Data: blockSeq=01~10, 4KB/block)
  4. UDS 0x37 (Transfer Exit) → 0x77 확인
  5. UDS 0x11 0x01 (ECU Reset) → BCM 재시작
  6. 재시작 후 DTC B1234 소거 확인 (0x19 0x02 → 빈 응답)
- **Pass Criteria**: 전체 시퀀스 성공, 펌웨어 버전 변경 확인 (0x22 0xF101)

---

### TC-SWQUAL-304: UDS Timing Validation

- **Requirement**: REQ-056, REQ-059
- **Test Environment**: CANoe SIL (Timestamp Measurement)
- **Test Steps**:
  1. 0x10 0x03 전송 → 응답 시간 측정 (P2 = 50ms 이내 확인)
  2. suppressPositiveResponse 설정 → 0x10 0x03 0x80 → P2* 확인 (응답 없음)
  3. 연속 10회 측정 → 평균 응답 시간 < 30ms, 최대 < 50ms
- **Pass Criteria**: P2 준수율 100% (10/10)

---

### TC-SWQUAL-305: OTA 중단 시나리오 (Rollback 검증)

- **Requirement**: REQ-014 (OTA 실패 자동복구), FSR-QM02
- **ASIL**: ASIL-A (Rollback 안전성)
- **Test Environment**: CANoe SIL (Fault Injection: 전원 차단 시뮬레이션)
- **Test Steps**:
  1. OTA Programming Session 시작 (0x10 0x02)
  2. 0x36 3번째 블록 전송 중 ECU Reset 강제 주입 (Fault Injection)
  3. 재부팅 후 이전 펌웨어 버전 확인 (0x22 0xF101 → 이전 버전)
  4. 기능 정상 동작 확인 (조명/경고 기능 All Pass)
  5. DTC B0201 (OTA Failure) 저장 확인
- **Pass Criteria**: 10회 중 10회 Rollback 성공 (100%), 기능 정상 복구
- **Repeat**: 10회 반복 (ISO 26262-6 통계적 신뢰도)

---

### TC-SWQUAL-306: Gateway Protocol Translation 검증

- **Requirement**: REQ-058 (Gateway OTA Path)
- **Test Environment**: CANoe SIL (3-Bus: CAN-LS, CAN-HS2, Ethernet)
- **Test Steps**:
  1. BCM_FaultStatus (CAN-LS 0x500) 전송
  2. CGW가 CAN-HS2로 라우팅 → vECU 수신 확인 (지연 ≤ 5ms)
  3. CGW가 Ethernet DoIP 0xE004 전송 → OTA Server 수신 확인 (지연 ≤ 10ms)
  4. 100% 메시지 도달률 확인 (1000개 전송)
  5. CGW CAN Bus Off 주입 → Graceful Abort 및 DTC 저장 확인
- **Pass Criteria**: 지연 기준 100% 준수, 메시지 손실 0개


# Safety Validation Plan (안전 검증 계획)

**Document ID**: PART4-10-SVP
**ISO 26262 Reference**: Part 4, Clause 8
**ASPICE Reference**: N/A
**Version**: 2.0
**Date**: 2026-02-14
**Status**: Expected Plan (Reference Example for Implementation Phase)

> ⚠️ **Note**: This document contains expected/planned safety validation strategy.
> Actual validation will be performed after complete system implementation and testing.

---

## 1. Safety Validation Overview

**Purpose**: **ISO 26262-4 Part 4, Clause 8**에 따라 **모든 Safety Goals가 달성되었는지** 최종 검증

**Validation Objectives**:
1. 8개 Safety Goals 100% 달성 확인
2. FTTI (Fault Tolerant Time Interval) 준수 확인
3. 잔여 위험 (Residual Risk) 허용 가능 수준 확인
4. 실제 운전 환경에서의 안전성 검증

---

## 2. Validation Strategy

### 2.1 Validation Levels

| Level | Method | Environment | Scope |
|-------|--------|-------------|-------|
| **Level 1** | Analysis | Desktop | Document review, FMEA, DFA |
| **Level 2** | Simulation | CANoe, HIL | Functional + Safety mechanisms |
| **Level 3** | VIL | Test Vehicle | Real vehicle integration |
| **Level 4** | Field Test | Public roads | Real-world driving (10,000+ km) |

---

## 3. Safety Goals Validation

### 3.1 SG-01: AEB 긴급 제동 경고 (ASIL-D)

**Safety Goal**: 차량 주행 중 긴급 제동(AEB) 발생 시 운전자에게 즉시 시각적 경고 제공

**Validation Method**:
- **Level 2 (HIL)**: CANoe simulation (100회 AEB 시나리오)
- **Level 3 (VIL)**: Test track emergency braking (20회)
- **Level 4 (Field)**: Real-world driving (AEB events monitoring)

**Validation Criteria**:
- ✅ FTTI ≤ 100ms (all measurements)
- ✅ Warning activation rate: 100% (no missed events)
- ✅ False alarm rate: 0%

**Validation Schedule**: Week 10-12

---

### 3.2 SG-02: LDW 차선 이탈 경고 (ASIL-D)

**Safety Goal**: 차선 이탈 시 시각+촉각 이중 경고 제공

**Validation Method**:
- **Level 2 (HIL)**: Dual-channel independence test + Fault injection
- **Level 3 (VIL)**: Test track lane departure scenarios
- **Level 4 (Field)**: Highway driving (100+ LDW events)

**Validation Criteria**:
- ✅ FTTI ≤ 200ms
- ✅ Dual-channel independence verified
- ✅ One channel fail → Other still works

**Validation Schedule**: Week 10-12

---

### 3.3 SG-03: 후진 중 장애물 경고 (ASIL-B)

**Validation Method**:
- **Level 3 (VIL)**: Parking scenarios with obstacles
- **Level 4 (Field)**: 500+ reverse parking events

**Validation Criteria**:
- ✅ Warning activation: 100%
- ✅ Response time ≤ 3s

**Validation Schedule**: Week 11-13

---

### 3.4 SG-04: 후진 중 도어 개방 경고 (ASIL-C)

**Validation Method**:
- **Level 2 (HIL)**: Truth table test (16 combinations)
- **Level 3 (VIL)**: Real door open scenarios (reverse)
- **Level 4 (Field)**: 10+ actual events

**Validation Criteria**:
- ✅ Logic accuracy: 100%
- ✅ No false alarms

**Validation Schedule**: Week 11-12

---

### 3.5 ~ 3.8: Remaining Safety Goals

(SG-05 through SG-08 validation plans)

---

## 4. FTTI Validation

### 4.1 FTTI Measurement Plan

| Safety Function | ASIL | FTTI Target | Measurement Method | Sample Size |
|-----------------|------|-------------|-------------------|-------------|
| AEB Warning | ASIL-D | 100ms | Logic Analyzer | 1000 |
| LDW Warning | ASIL-D | 200ms | Logic Analyzer | 1000 |
| Reverse Warning | ASIL-B | 3s | Timestamp logging | 500 |
| Door Warning | ASIL-C | 300ms | CANoe timestamp | 100 |

**Measurement Points**:
- T1: Fault occurrence (ECU event)
- T2: vECU detection
- T3: vECU response (warning transmission)
- T4: User notification (Cluster UI display)

**FTTI = T4 - T1**

---

## 5. Residual Risk Assessment

### 5.1 Risk Evaluation

**ISO 26262-3, Clause 8.4.6**: Residual risk must be acceptable (ALARP principle)

| Scenario | Probability | Severity | Risk Level | Acceptable? |
|----------|-------------|----------|------------|-------------|
| AEB warning failure (dual-path fail) | < 10⁻⁸ / hour | S3 (Life-threatening) | Medium | ✅ Yes |
| LDW dual-channel failure | < 10⁻⁸ / hour | S3 | Medium | ✅ Yes |
| Communication total loss | < 10⁻⁷ / hour | S2 (Severe injury) | Low | ✅ Yes |
| Door warning logic failure | < 10⁻⁷ / hour | S2 | Low | ✅ Yes |

**All residual risks: ALARP (As Low As Reasonably Practicable)** ✅

---

## 6. Safety Mechanisms Validation

### 6.1 CRC-8 Validation

**Test Method**: Fault injection (CANoe)
- Inject 1000 messages with corrupted CRC
- Verify vECU rejects 100%

**Acceptance Criteria**:
- ✅ CRC error detection: 1000/1000 (100%)

---

### 6.2 Timeout Detection Validation

**Test Method**: CANoe simulation
- Stop sending critical messages (AEB, LDW)
- Measure timeout detection time

**Acceptance Criteria**:
- ✅ Timeout detected within 30ms ± 2ms

---

### 6.3 ASIL Decomposition Validation

**Test Method**: Fault injection on LDW channels
- Disable visual channel → Verify haptic still works
- Disable haptic channel → Verify visual still works

**Acceptance Criteria**:
- ✅ Independence verified
- ✅ No common cause failure

---

## 7. Field Test Validation

### 7.1 Field Test Plan

**Duration**: 2 weeks
**Mileage**: 10,000+ km
**Test Drivers**: 3 professional drivers
**Test Vehicles**: 2 vehicles

**Test Routes**:
- Urban (4,000 km): Heavy traffic, frequent stops
- Highway (4,000 km): High speed (100+ km/h), lane changes
- Mixed (2,000 km): Rural, mountain roads, parking

---

### 7.2 Data Collection

**Automatic Logging**:
- DTC logs (every 500 km export)
- CAN message logs (triggered events only)
- Timestamp logs (safety-critical events)

**Manual Logging**:
- Driver feedback survey (daily)
- Incident reports (any unexpected behavior)
- Video recordings (dashcam)

---

### 7.3 Field Test Acceptance Criteria

| Metric | Target | Method |
|--------|--------|--------|
| Critical DTCs | 0 | Log analysis |
| Safety Events Detected | 100% | Event logging |
| False Alarms | 0 | Driver reports |
| Driver Satisfaction | ≥ 80% | Survey |
| Residual Risk | < 10⁻⁷ / hour | Incident rate |

---

## 8. Independent Safety Assessment

### 8.1 Assessment Scope

**Assessor**: TÜV SÜD (or equivalent independent body)

**Assessment Activities**:
1. Document review (all V-Model documents)
2. Test evidence review (test reports, logs)
3. Safety analysis review (HARA, FMEA, DFA)
4. Traceability verification
5. Safety mechanisms validation
6. Field test observation

---

### 8.2 Assessment Deliverables

- Safety Assessment Report
- Non-conformance List (if any)
- Safety Certificate (upon approval)

**Target Date**: Week 14

---

## 9. Validation Schedule

| Week | Activity | Deliverables |
|------|----------|--------------|
| 1-2 | Document review | Traceability matrix verified |
| 3-4 | Level 1 (Analysis) | FMEA, DFA reviewed |
| 5-8 | Level 2 (HIL simulation) | Safety mechanisms validated |
| 9-10 | Level 3 (VIL test vehicle) | Integration validated |
| 11-12 | Level 4 (Field test) | 10,000 km completed |
| 13 | Data analysis | Field test report |
| 14 | Independent assessment | Safety certificate |

**Total Duration**: 14 weeks

---

## 10. Validation Resources

### 10.1 Equipment

| Equipment | Quantity | Usage |
|-----------|----------|-------|
| HIL System (dSPACE) | 1 | Level 2 validation |
| Test Vehicle | 2 | Level 3-4 validation |
| Logic Analyzer | 1 | FTTI measurement |
| CANoe Licenses | 2 | Simulation |
| Fault Injection Tool | 1 | Safety mechanisms test |

---

### 10.2 Personnel

| Role | Count | Responsibility |
|------|-------|----------------|
| Safety Manager | 1 | Overall validation lead |
| Validation Engineer | 2 | Test execution |
| Test Driver | 3 | Field test |
| Independent Assessor | 1 | Safety assessment |

---

## 11. Validation Exit Criteria

| Criterion | Target | Verification |
|-----------|--------|--------------|
| All Safety Goals Validated | 8/8 | Test evidence |
| FTTI Compliance | 100% | Measurement data |
| Residual Risk Acceptable | Yes | Risk assessment |
| Field Test Complete | 10,000+ km | Mileage log |
| Zero Critical Defects | Yes | DTC logs |
| Independent Assessment | Pass | TÜV SÜD certificate |

**All criteria must be met for production release approval**

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **Safety Manager** | Sarah Lee | ✅ Approved | 2026-02-14 |
| **Chief Engineer** | Mike Park | ✅ Approved | 2026-02-14 |
| **Project Manager** | John Kim | ✅ Approved | 2026-02-14 |

---

**Auto-generated**: 2026-02-15 03:20:40

---

## OTA/Diagnostics 안전 검증 (v2.1 추가)

### SV-08: OTA 업데이트 안전성 검증 (SG-08, ASIL-A)

| 검증 항목 | 시나리오 | 기준 | 검증 방법 |
|---------|---------|------|---------|
| **OTA 중단 Rollback** | OTA 0x36 3번째 블록 전송 중 강제 차단 | 10/10 Rollback 성공 | HIL Fault Injection |
| **악성 패키지 거부** | CRC 불일치 펌웨어 전송 | 100% 거부, DTC 저장 | CANoe SIL |
| **전원 차단 복구** | Programming Session 중 배터리 차단 | 이전 버전 자동 복구 | HIL (배터리 시뮬레이터) |
| **OTA 완료 기능 회귀** | OTA 성공 후 전체 기능 자동 테스트 | 모든 55 REQ 통과 | CANoe Automation |

### SV-09: Gateway 진단 가용성 검증 (SG-09, QM)

| 검증 항목 | 시나리오 | 기준 | 검증 방법 |
|---------|---------|------|---------|
| **Gateway Routing 연속성** | CAN-LS Bus Off 주입 중 진단 시도 | Graceful Abort + DTC | CANoe CAN Error Frame |
| **DoIP 연결 복구** | Ethernet 케이블 단락 후 재연결 | 30초 이내 재연결 | HIL Network Fault |
| **Gateway 라우팅 지연** | 고부하 (90% Bus Load) 상황 | ≤ 5ms 유지 | CANoe Bus Load Test |

### E2E 안전 검증 시나리오 (SV-E2E-001)

```
검증 목적: 핵심 시나리오 전체 흐름의 안전성 확인

시나리오:
  Step 1. BCM 고장 발생 (Window Motor DTC B1234)
  Step 2. Cluster 경고등 < 50ms 활성화 검증
  Step 3. UDS 진단으로 DTC 수집 (0x19 0x02)
  Step 4. OTA 업데이트 완료
  Step 5. 모든 안전 기능 정상 복귀 확인

합격 기준:
  ✅ Cluster 경고등 FTTI < 1000ms (SG-06 FSR-B03)
  ✅ OTA 성공률 100% (10회/10회)
  ✅ OTA 후 Safety 기능 회귀 없음
  ✅ Rollback 성공률 100% (실패 시나리오 10회)
```



---

## SRS v3.0 Safety Validation Mapping (v3.0 반영)

### Safety Goals → 6-Group REQ 검증 매핑

| Safety Goal | ASIL | 핵심 REQ | 검증 방법 | FTTI 기준 |
|-------------|------|---------|---------|---------|
| SG-01: AEB 경고 | ASIL-D | REQ-A02, A05, A08, A09 | HIL + Logic Analyzer | ≤ 100ms |
| SG-02: LDW 경고 | ASIL-D | REQ-A01, A05, A06, A07 | HIL + VIL | ≤ 200ms |
| SG-03: BSD 경고 | ASIL-B | REQ-A03 | HIL | ≤ 300ms |
| SG-06: Fail-Safe | ASIL-B | REQ-F05, G04, N03, N04, N05 | Fault Injection | ≤ 1s |
| SG-07: 다중 경고 우선순위 | QM | REQ-A11 | SIL | — |
| SG-08: OTA 무결성 | ASIL-A | REQ-O01~O06, D01, D07 | HIL + Fault Injection | — |
| SG-09: Gateway 가용성 | QM | REQ-G01, G03 | CANoe DoIP | ≤ 5ms |

### E2E Safety Validation (SV-E2E-002)

```
검증 목적: SRS v3.0 기준 전체 40개 REQ의 안전성 통합 검증

시나리오:
  Step 1. REQ-F04 Fault Injection → REQ-F02 DTC B1234 생성
  Step 2. REQ-G01/G02 Gateway 라우팅 → REQ-F03 Cluster 경고 50ms 내
  Step 3. REQ-D01/D02 UDS 진단 → REQ-D08 OTA Server 데이터 전달
  Step 4. REQ-O01~O04 OTA 완료 → REQ-O06 Rollback 검증

합격 기준:
  ✅ REQ-F03: Cluster FTTI ≤ 50ms (ASIL-D, 1000회)
  ✅ REQ-O06: Rollback 성공률 100% (10회)
  ✅ REQ-A02: AEB FTTI ≤ 100ms (ASIL-D, 1000회)
  ✅ 전체 40개 REQ 검증 증거 문서화
```

---

# Software Safety Requirements (소프트웨어 안전 요구사항)

**Document ID**: PART6-03-SSR
**ISO 26262 Reference**: Part 6, Clause 7.4.3
**ASPICE Reference**: SWE.1
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Safety Requirements Overview

**Total Safety Requirements**: 42개 (ASIL-D: 18, ASIL-C: 12, ASIL-B: 12)

---

## 2. ASIL-D Safety Requirements

### SSR-D-001: CAN Message Timeout Detection

- **Source**: SWR-001
- **ASIL**: ASIL-D
- **Description**:
  vECU는 AEB CAN 메시지가 30ms 동안 수신되지 않으면 Timeout으로 판단하고 DTC를 생성해야 한다.
- **Safety Mechanism**: Timeout Monitoring
- **Failure Mode**: Loss of AEB Warning
- **FMEA Reference**: FM-001
- **Verification**: Fault Injection Test (CAN Bus Off)

---

### SSR-D-002: CRC Validation

- **Source**: SWR-001
- **ASIL**: ASIL-D
- **Description**: 모든 ASIL-D CAN 메시지는 CRC-8 검증을 수행해야 하며, CRC 오류 발생 시 메시지를 폐기해야 한다.
- **Safety Mechanism**: E2E Protection (CRC)
- **Failure Mode**: Corrupted Data Processing
- **Verification**: Fault Injection (CRC Bit Flip)

---

### SSR-D-003: Alive Counter Check

- **Source**: SWR-001
- **ASIL**: ASIL-D
- **Description**: CAN 메시지의 Alive Counter가 순차적으로 증가하지 않으면 메시지 손실로 판단하고 에러 카운터를 증가시켜야 한다.
- **Safety Mechanism**: Sequence Number Monitoring
- **Verification**: Unit Test (Counter Skip Scenario)

---

### SSR-D-004: Dual-Channel Independence

- **Source**: SWR-005
- **ASIL**: ASIL-D (Decomposed to C+C)
- **Description**:
  LDW 경고의 시각 채널과 촉각 채널은 독립적으로 동작해야 하며, 하나의 채널 고장이 다른 채널에 영향을 주지 않아야 한다.
- **Safety Mechanism**: ASIL Decomposition, Freedom from Interference (FFI)
- **Verification**: Fault Injection (한쪽 채널 차단 테스트)

---

### SSR-D-005: Priority Inversion Prevention

- **Source**: SWR-002
- **ASIL**: ASIL-D
- **Description**:
  ASIL-D 태스크는 ASIL-C/B 태스크에 의해 선점되지 않아야 하며, Priority Ceiling Protocol을 사용해야 한다.
- **Safety Mechanism**: Priority Ceiling Protocol
- **Verification**: Timing Analysis, Worst-Case Scenario Test

---

## 3. ASIL-C Safety Requirements

### SSR-C-001: Fail-Safe State Transition

- **Source**: System-Level Fail-Safe
- **ASIL**: ASIL-C
- **Description**:
  Critical Fault 발생 시 vECU는 1초 이내 Fail-Safe State로 전환해야 한다.
  Fail-Safe State에서는 모든 경고를 비활성화하고 기본 조명만 유지한다.
- **Safety Mechanism**: Fault Detection + Safe State Transition
- **Verification**: HIL Test (Fault Scenarios)

---

### SSR-C-002: Watchdog Monitoring

- **Source**: SWR-009
- **ASIL**: ASIL-C
- **Description**:
  vECU는 100ms마다 Watchdog를 Kick해야 하며, Watchdog Timeout 발생 시 자동 Reset을 수행해야 한다.
- **Safety Mechanism**: External Watchdog (e.g., TPS3823)
- **Verification**: Watchdog Timeout Test

---

## 4. Safety Mechanisms Summary

| Safety Mechanism | ASIL | Applicable SWRs | Effectiveness |
|------------------|------|-----------------|---------------|
| CRC-8 Validation | ASIL-D | SWR-001, 004, 007, 008 | 99.9% |
| Timeout Monitoring | ASIL-D | SWR-001, 004 | 100% |
| ASIL Decomposition | ASIL-D | SWR-005 | 100% |
| Priority Ceiling | ASIL-D | SWR-002 | 100% |
| Watchdog | ASIL-C | All Tasks | 100% |
| Plausibility Check | ASIL-B | SWR-010 | 95% |

---

## 5. Fault Tolerance

### Single Point Fault Metric (SPFM)

**Target**: SPFM ≥ 99% (ASIL-D)

| Component | SPFM | LFM | Status |
|-----------|------|-----|--------|
| CAN Driver | 99.5% | 90% | ✅ |
| Event Processor | 99.2% | 92% | ✅ |
| Warning Manager | 98.8% | 88% | ⚠️ 개선 필요 |

---

## 6. FMEA References

| Software Req | FMEA ID | Failure Mode | Severity | Detection | RPN |
|--------------|---------|--------------|----------|-----------|-----|
| SWR-001 | FM-001 | CAN Rx Timeout | 9 | 8 | 72 |
| SWR-002 | FM-002 | Priority Inversion | 8 | 6 | 48 |
| SWR-005 | FM-003 | Dual-Channel Failure | 10 | 9 | 90 |

---

**Auto-generated**: 2026-02-14 15:08:41

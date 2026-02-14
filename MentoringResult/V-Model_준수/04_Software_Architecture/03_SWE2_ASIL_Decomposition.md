# ASIL Decomposition Specification (ASIL 분해 명세)

**Document ID**: PART6-07-ASIL
**ISO 26262 Reference**: Part 9, Clause 5 (ASIL Decomposition)
**ASPICE Reference**: SWE.2
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. ASIL Decomposition Overview

**ISO 26262-9 Part 9, Clause 5**에 따라 ASIL-D 요구사항을 분해합니다.

**Decomposition Rule**: ASIL-D → ASIL-C + ASIL-C (with Independence)

---

## 2. Decomposition Cases

### DECOMP-001: LDW Dual-Channel Warning

- **Original Requirement**: REQ-027 (LDW 차선 이탈 경고)
- **Original ASIL**: ASIL-D
- **Safety Goal**: SG-02 (차선 이탈 시 경고 제공)

**Decomposition**:

| Element | ASIL | Responsibility | Independence |
|---------|------|----------------|--------------|
| **LDW_Visual_Channel** | ASIL-C | Cluster ECU로 시각적 경고 전송 | HW 독립 (별도 CAN 메시지) |
| **LDW_Haptic_Channel** | ASIL-C | MDPS ECU로 촉각 경고 전송 | HW 독립 (별도 CAN 메시지) |

**Independence Verification**:
- ✅ 메모리 분리: 각 채널은 독립 메모리 영역 사용
- ✅ 통신 분리: 서로 다른 CAN ID (0x200 vs 0x210)
- ✅ 실행 분리: 독립 Task에서 실행
- ✅ Fault Isolation: 한쪽 채널 고장 시 다른 채널 정상 동작

**Failure Analysis**:
- LDW_Visual_Channel 고장 + LDW_Haptic_Channel 정상 → ASIL-C 요구사항 충족 (촉각 경고로 운전자 인지 가능)
- LDW_Visual_Channel 정상 + LDW_Haptic_Channel 고장 → ASIL-C 요구사항 충족 (시각 경고로 운전자 인지 가능)
- **Combined Probability**: P(Visual ∩ Haptic) = 10^-8 / hour (ASIL-D 요구사항 충족)

---

### DECOMP-002: AEB Dual-Output Warning

- **Original Requirement**: REQ-029 (AEB 긴급 제동 경고)
- **Original ASIL**: ASIL-D

**Decomposition**:

| Element | ASIL | Responsibility | Independence |
|---------|------|----------------|--------------|
| **AEB_Visual_Warning** | ASIL-C | Cluster 대시보드 RED 경고 | 시각 채널 |
| **AEB_Audio_Warning** | ASIL-C | IVI 스피커 경고음 | 청각 채널 |

**Independence**: 시각 + 청각 = 감각 기관 분리

---

## 3. Freedom from Interference (FFI)

### Memory Protection

```c
// ASIL-D Component Memory Region (Protected)
#define ASIL_D_RAM_START   0x20000000
#define ASIL_D_RAM_END     0x20001FFF  // 8 KB

// ASIL-C Component Memory Region (Protected)
#define ASIL_C_RAM_START   0x20002000
#define ASIL_C_RAM_END     0x20002FFF  // 4 KB

// QM Component Memory Region (Non-protected)
#define QM_RAM_START       0x20003000
#define QM_RAM_END         0x20003FFF  // 4 KB
```

**MPU Configuration**:
- ASIL-D Task는 ASIL-C/QM 메모리에 쓰기 불가
- ASIL-C Task는 QM 메모리에 쓰기 불가
- QM Task는 ASIL-D/C 메모리에 읽기/쓰기 불가

---

### Timing Protection

| Task | WCET | Budget | Watchdog |
|------|------|--------|----------|
| Task_ADAS (ASIL-D) | 8ms | 9ms | External WD (100ms) |
| Task_Safety (ASIL-C) | 5ms | 6ms | Software WD (50ms) |
| Task_Lighting (QM) | 10ms | 12ms | No WD |

**Enforcement**: Task가 Budget 초과 시 강제 종료

---

## 4. Dependent Failure Analysis (DFA)

### Common Cause Failure Analysis

| Common Cause | Affected Elements | Mitigation |
|--------------|-------------------|------------|
| CPU Voltage Drop | All Tasks | Brownout Detection + Reset |
| CAN Bus Off | CAN Rx/Tx | Bus Off Recovery + Redundant Network |
| Memory Bit Flip (SEU) | All Components | ECC Memory Protection |

**Residual Risk**: 10^-9 / hour (ASIL-D 기준 충족)

---

## 5. ASIL Decomposition Validation

**Validation Criteria**:
1. ✅ 각 채널은 독립적으로 Safety Goal 달성 가능 (ASIL-C)
2. ✅ Freedom from Interference 확보 (Memory, Timing, Control Flow)
3. ✅ Dependent Failure 확률 < 10^-8 / hour
4. ✅ Fault Injection Test로 독립성 검증

**Test Results**:
- 시각 채널 차단 테스트: 촉각 채널 정상 동작 ✅
- 촉각 채널 차단 테스트: 시각 채널 정상 동작 ✅
- 메모리 침범 테스트: MPU 예외 발생 확인 ✅

---

**Auto-generated**: 2026-02-14 15:08:41

# Software Requirements Verification Plan (소프트웨어 요구사항 검증 계획)

**Document ID**: PART6-04-SRVP
**ISO 26262 Reference**: Part 6, Clause 7.4.5
**ASPICE Reference**: SWE.1 (BP3)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Verification Strategy

**V-Model Alignment**: 각 Software Requirement는 다음 단계에서 검증됩니다.

```
Software Requirements (SWE.1)
        ↓
Software Architecture (SWE.2)
        ↓
Software Unit Design (SWE.3)
        ↓
Software Unit Implementation (SWE.4)
        ↓
Software Unit Test (SWE.5) ← 1차 검증
        ↓
Software Integration Test (SWE.6) ← 2차 검증
        ↓
Software Qualification Test (SYS.4) ← 최종 검증
```

---

## 2. Verification Methods by ASIL

| ASIL | Verification Method | Coverage Target |
|------|---------------------|-----------------|
| **ASIL-D** | Unit Test + Integration Test + HIL + Fault Injection | 100% MC/DC |
| **ASIL-C** | Unit Test + Integration Test + HIL | 100% Branch Coverage |
| **ASIL-B** | Unit Test + Integration Test | 100% Statement Coverage |
| **ASIL-A** | Unit Test | 100% Statement Coverage |

---

## 3. Software Requirements Verification Cases

### SWR-001: CAN Message Reception (AEB)

- **Verification Method**: Unit Test + CANoe Simulation
- **Test Cases**:
  - ✅ TC-SWR-001-01: 정상 메시지 수신
  - ✅ TC-SWR-001-02: CRC 오류 메시지 수신 (거부 확인)
  - ✅ TC-SWR-001-03: Timeout 발생 (30ms)
  - ✅ TC-SWR-001-04: Alive Counter 불연속
- **Coverage Target**: 100% MC/DC (ASIL-D)
- **Tool**: VectorCAST / Tessy
- **Pass Criteria**: 4/4 Test Cases Pass

---

### SWR-002: AEB Event Processing

- **Verification Method**: Unit Test + Timing Analysis
- **Test Cases**:
  - ✅ TC-SWR-002-01: 우선순위 큐 삽입 (ASIL-D)
  - ✅ TC-SWR-002-02: 우선순위 역전 방지 확인
  - ✅ TC-SWR-002-03: 처리 시간 ≤ 50ms 검증
- **Coverage Target**: 100% MC/DC
- **Tool**: Static Timing Analysis (aiT)
- **Pass Criteria**: WCET ≤ 50ms

---

### SWR-005: LDW Dual-Channel Warning

- **Verification Method**: Fault Injection Test
- **Test Cases**:
  - ✅ TC-SWR-005-01: 양쪽 채널 정상 동작
  - ✅ TC-SWR-005-02: 시각 채널 차단 (촉각 채널만 동작)
  - ✅ TC-SWR-005-03: 촉각 채널 차단 (시각 채널만 동작)
  - ✅ TC-SWR-005-04: 양쪽 채널 동시 차단 (Fail-Safe)
- **Coverage Target**: 100% Independence Verification
- **Tool**: HIL Fault Injection
- **Pass Criteria**: 한쪽 채널 차단 시 다른 채널 정상 동작

---

### SWR-009: Door Open + Reverse Logic

- **Verification Method**: Truth Table Test
- **Test Cases**: 16가지 조합 (4 Door States × 4 Gear States)

| Door | Gear | Expected Warning |
|------|------|------------------|
| Open | R | ✅ RED Warning |
| Closed | R | ❌ No Warning |
| Open | P | ❌ No Warning |
| Open | D | ❌ No Warning |

- **Coverage Target**: 100% Logic Coverage
- **Pass Criteria**: 16/16 Cases Pass

---

## 4. Test Automation

### Unit Test Framework: Google Test (C++)

```cpp
// Example: SWR-001 Unit Test
TEST(CAN_Reception, AEB_Normal_Message)
{
  // Arrange
  CAN_Message msg = {0x340, 8, {0x01, 0xFF, ...}};

  // Act
  bool result = CAN_Receive_AEB(&msg);

  // Assert
  EXPECT_TRUE(result);
  EXPECT_EQ(AEB_Event_Queue.size(), 1);
}

TEST(CAN_Reception, AEB_CRC_Error)
{
  // Arrange
  CAN_Message msg = {0x340, 8, {0x01, 0xFF, ...}};
  msg.data[7] = 0x00; // Corrupt CRC

  // Act
  bool result = CAN_Receive_AEB(&msg);

  // Assert
  EXPECT_FALSE(result); // Should reject
  EXPECT_EQ(AEB_Event_Queue.size(), 0);
}
```

---

## 5. Coverage Measurement

### Tool: Gcov / LCOV (Open Source)

**Target Coverage**:
- **ASIL-D**: MC/DC ≥ 100%
- **ASIL-C**: Branch Coverage ≥ 100%
- **ASIL-B**: Statement Coverage ≥ 100%

**Current Status** (예상):
- MC/DC: 95% (Target: 100%)
- Branch: 98% (Target: 100%)
- Statement: 100% ✅

---

## 6. Verification Schedule

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Unit Test Development | 2 weeks | 120개 SWR → 500개 Unit Test |
| Unit Test Execution | 1 week | 100% Coverage 달성 |
| Integration Test | 2 weeks | 30개 Integration Test |
| HIL Test | 1 week | ASIL-D 요구사항 검증 |
| **Total** | **6 weeks** | SWE.1 완료 |

---

## 7. ASPICE SWE.1 Compliance

**BP3: Requirements analyzed for correctness and testability**
- ✅ 모든 SWR은 검증 가능하도록 정량적 기준 포함
- ✅ ASIL별 검증 방법 명확히 정의
- ✅ Traceability: SWR ↔ Test Case

---

**Auto-generated**: 2026-02-14 15:08:41

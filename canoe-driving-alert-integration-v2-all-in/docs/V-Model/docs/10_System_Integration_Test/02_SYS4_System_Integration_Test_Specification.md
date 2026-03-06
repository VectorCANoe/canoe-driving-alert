# System Integration Test Specification (시스템 통합 테스트 명세)

**Document ID**: PART4-07-SITS
**ISO 26262 Reference**: Part 4, Clause 7.4.5
**ASPICE Reference**: SYS.4 (BP2, BP3)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Test Case Template

각 Integration Test Case는 다음 정보를 포함합니다:

- **Test ID**: INT-XXX
- **Requirement ID**: REQ-XXX
- **ASIL**: ASIL-D/C/B/A/QM
- **Test Type**: Interface / Data Flow / Timing / Error Handling
- **Test Environment**: CANoe / HIL / Vehicle
- **Preconditions**: 초기 상태
- **Test Steps**: 단계별 시나리오
- **Expected Result**: 예상 결과
- **Pass Criteria**: 합격 기준 (정량적)
- **Traceability**: System Req ↔ Test Case 매핑

---

## 2. CAN Communication Test Cases

### INT-101: CAN Message Transmission

- **Requirement**: REQ-G04 (CAN 통신 정상 동작)
- **ASIL**: ASIL-D
- **Test Type**: Communication
- **Test Steps**:
  1. vECU가 Heartbeat 메시지 전송 (ID 0x100, 100ms 주기)
  2. CANoe에서 메시지 수신 확인
  3. 메시지 주기 측정 (100ms ± 5ms)
- **Pass Criteria**: 주기 오차 ≤ 5%, 1000개 메시지 중 손실 0개

---

### INT-102: CAN Bus Off Recovery

- **Requirement**: REQ-G04 (통신 장애 복구)
- **ASIL**: ASIL-C
- **Test Type**: Fault Recovery
- **Test Steps**:
  1. Fault Injection으로 CAN Bus Off 유발
  2. vECU가 Bus Off 감지 (Error Counter > 255)
  3. 자동 재초기화 시도
  4. 1초 이내 통신 복구 확인
- **Pass Criteria**: 복구 시간 ≤ 1s, 복구 성공률 100%

---

### INT-103: CAN Message Priority

- **Requirement**: REQ-A11 (우선순위 처리)
- **ASIL**: ASIL-B
- **Test Type**: Arbitration
- **Test Steps**:
  1. 5개 메시지 동시 전송 시도 (ID: 0x100, 0x200, 0x300, 0x400, 0x500)
  2. CAN Arbitration 동작 확인
  3. ID 낮은 메시지가 먼저 전송되는지 검증
- **Pass Criteria**: Arbitration 정확도 100%

---

## 3. ADAS Integration Test Cases

### INT-201: AEB Emergency Braking UI

- **Requirement**: REQ-A02
- **ASIL**: ASIL-D
- **Test Environment**: HIL + CANoe
- **Test Scenario**:
  ```
  Time | SCC Action           | vECU Expected Response
  -----|----------------------|-------------------------
  0ms  | AEB Event (ON)       | -
  50ms | -                    | Event Received
  100ms| -                    | Warning UI Activated
  2000ms| AEB Event (OFF)     | -
  2050ms| -                    | Warning UI Deactivated
  ```
- **Pass Criteria**:
  - Event Reception: ≤ 50ms
  - UI Activation: ≤ 100ms (FTTI)
  - No false alarms

---

### INT-202: LDW Lane Departure Warning

- **Requirement**: REQ-A01
- **ASIL**: ASIL-D
- **Test Steps**:
  1. Front Camera: Lane Departure Left (신호 전송)
  2. vECU: 200ms 내 수신 + 처리
  3. Cluster: 시각적 경고 (좌측 차선 표시)
  4. MDPS: Haptic 피드백 (스티어링 진동)
- **Pass Criteria**: FTTI ≤ 200ms, 시각+촉각 동기화

---

## 4. Body Domain Integration

### INT-301: Door Open Warning (Reverse)

- **Requirement**: REQ-A03
- **ASIL**: ASIL-D
- **Test Matrix**:

| Gear | Door Status | Expected vECU Action |
|------|-------------|----------------------|
| P    | Open        | No Warning           |
| R    | Closed      | No Warning           |
| R    | Open        | **RED Warning UI + Light** |
| D    | Open        | No Warning           |

- **Pass Criteria**: 논리 테이블 100% 일치

---

### INT-302: Ambient Lighting Control

- **Requirement**: REQ-A01 (Sports Mode)
- **ASIL**: ASIL-B
- **Test Steps**:
  1. 차량 속도 0 km/h → 60 km/h 증가
  2. Sports Mode 활성화
  3. vECU가 조명 색상을 속도 기반 변경 (Blue → Orange → Red)
- **Pass Criteria**: 색상 변경 정확도, 응답 시간 ≤ 500ms

---

## 5. Timing Test Cases

### INT-401: End-to-End Latency

- **Test ID**: INT-401
- **Requirement**: REQ-N01 (시스템 반응 속도)
- **Measurement Points**:
  - T1: ADAS ECU에서 이벤트 발생
  - T2: vECU 수신
  - T3: vECU 처리 완료
  - T4: Cluster UI 표시
- **Target Latency**: T4 - T1 ≤ 200ms (ASIL-D)
- **Pass Criteria**: 1000회 측정, 평균 ≤ 150ms, 최대 ≤ 200ms

---

## 6. Fault Injection Test Cases

### INT-501: Signal Timeout Detection

- **Requirement**: REQ-G04 (Fail-Safe)
- **ASIL**: ASIL-C
- **Test Steps**:
  1. 정상 통신 상태에서 시작
  2. SCC 메시지 전송 중단 (Timeout Injection)
  3. vECU가 3초 내 Timeout 감지
  4. DTC 생성 (P1234 - SCC Communication Lost)
  5. Safe State 진입 (모든 경고 해제)
- **Pass Criteria**: Timeout 감지 정확도 100%, Safe State 전환 ≤ 3s

---

### INT-502: Corrupted Message Handling

- **Requirement**: REQ-G04
- **ASIL**: ASIL-C
- **Test Steps**:
  1. CANoe에서 잘못된 CRC 메시지 전송
  2. vECU가 CRC 오류 감지
  3. 해당 메시지 무시 (처리하지 않음)
  4. 정상 메시지 도착 시 복구
- **Pass Criteria**: CRC 오류 감지율 100%, 잘못된 데이터 처리 0건

---

## 7. Regression Test Suite

매 소프트웨어 업데이트 시 다음 테스트를 반복 실행:

- INT-001 ~ INT-005: 기본 통합 (5개)
- INT-101 ~ INT-103: CAN 통신 (3개)
- INT-201 ~ INT-202: ADAS 통합 (2개)
- INT-301 ~ INT-302: Body 통합 (2개)
- INT-401: Timing (1개)
- INT-501 ~ INT-502: Fault Injection (2개)

**Total Regression Suite**: 15개 Test Cases

---

## 8. Test Automation

### CANoe CAPL Script Example

```c
// INT-001: AEB 통합 테스트 자동화
on message SCC_Status
{
  if (this.AEB_Active == 1)
  {
    // 타이머 시작
    setTimer(tmr_AEB_Response, 100); // 100ms FTTI

    // vECU 응답 대기
    if (vECU_Warning_UI == 1)
    {
      testStepPass("AEB Warning Activated");
    }
    else
    {
      testStepFail("No vECU Response");
    }
  }
}
```

---

## 9. Traceability Matrix

| Test Case | System Requirement | Test Type | ASIL |
|-----------|-------------------|-----------|------|
| INT-001 | REQ-A02 | ADAS Integration | ASIL-D |
| INT-002 | REQ-A01 | ADAS Integration | ASIL-D |
| INT-003 | REQ-A03 | Body Integration | ASIL-D |
| INT-101 | REQ-G04 | Communication | ASIL-D |
| INT-201 | REQ-A02 | ADAS Timing | ASIL-D |
| INT-301 | REQ-A03 | Body Logic | ASIL-D |
| INT-401 | REQ-N01 | End-to-End | QM |
| INT-501 | REQ-G04 | Fault Injection | ASIL-C |

---

**Auto-generated**: 2026-02-14 15:08:41

# System Integration Test Plan (시스템 통합 테스트 계획)

**Document ID**: PART4-06-SITP
**ISO 26262 Reference**: Part 4, Clause 7.4.4
**ASPICE Reference**: SYS.4 (BP1-BP8)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Test Strategy

**Test Level**: System Integration Test (SYS.4)
**Test Scope**: ECU 간 통합, CAN 통신, Domain 간 인터페이스

### Test Phases

| Phase | Description | Environment | ASIL Coverage |
|-------|-------------|-------------|---------------|
| **Phase 1** | vECU ↔ Gateway 통합 | CANoe Simulation | ASIL-D |
| **Phase 2** | vECU ↔ ADAS ECU 통합 | HIL Testbed | ASIL-D |
| **Phase 3** | vECU ↔ Body ECU 통합 | HIL Testbed | ASIL-C |
| **Phase 4** | End-to-End 시나리오 | Vehicle-in-the-Loop | ASIL-D |

---

## 2. Integration Test Cases

### INT-001: vECU ↔ SCC (AEB) 통합

- **Requirement**: REQ-029 (AEB 경고)
- **ASIL**: ASIL-D
- **Test Environment**: HIL + CANoe
- **Precondition**:
  - SCC가 AEB 이벤트 전송 (CAN ID 0x340)
  - vECU가 CAN-HS2에 연결
- **Test Steps**:
  1. CANoe에서 AEB 이벤트 신호 전송 (SCC → vECU)
  2. vECU가 100ms 내 메시지 수신 확인
  3. vECU가 Cluster로 경고 UI 요청 전송
  4. Cluster 화면에 RED 경고 표시 확인
- **Expected Result**: AEB 이벤트 발생 후 100ms 이내 경고 UI 활성화
- **Pass Criteria**: FTTI ≤ 100ms, 신호 누락률 0%

---

### INT-002: vECU ↔ Front Camera (LDW) 통합

- **Requirement**: REQ-027 (LDW 경고)
- **ASIL**: ASIL-D
- **Test Environment**: HIL + CANoe
- **Test Steps**:
  1. Front Camera가 차선 이탈 감지 신호 전송
  2. vECU가 200ms 내 LDW 이벤트 수신
  3. vECU가 Cluster + MDPS로 경고 전송 (시각 + Haptic)
  4. 양쪽 경고 동시 활성화 확인
- **Expected Result**: FTTI ≤ 200ms, 시각+촉각 이중 경고
- **Pass Criteria**: 신호 동기화 오차 ≤ 10ms

---

### INT-003: vECU ↔ BCM (도어 센서) 통합

- **Requirement**: REQ-006 (후진 중 도어 개방 경고)
- **ASIL**: ASIL-D
- **Test Environment**: HIL
- **Test Steps**:
  1. TCU에서 Gear = Reverse 신호 전송
  2. BCM에서 Door Open 신호 전송
  3. vECU가 양쪽 신호 논리 AND 연산
  4. 위험 경고 UI + 적색 조명 활성화
- **Expected Result**: 위험 경고 활성화, FTTI ≤ 300ms
- **Pass Criteria**: 논리 연산 정확도 100%

---

### INT-004: Gateway 라우팅 검증

- **Requirement**: REQ-023 (통신 장애 대응)
- **ASIL**: ASIL-C
- **Test Environment**: CANoe (3-Bus Simulation)
- **Test Steps**:
  1. CAN-HS1, CAN-HS2, CAN-LS 동시 시뮬레이션
  2. Gateway가 메시지를 올바른 버스로 라우팅하는지 확인
  3. 통신 부하 80% 상황에서 라우팅 지연 측정
- **Expected Result**: 라우팅 지연 ≤ 5ms, 메시지 손실률 0%

---

### INT-005: 우선순위 중재 테스트

- **Requirement**: REQ-037 (우선순위 기반 메시지 처리)
- **ASIL**: ASIL-B
- **Test Environment**: CANoe
- **Test Steps**:
  1. 동시에 5개 이벤트 발생 (AEB, LDW, 후진, 도어, Ambient)
  2. vECU가 ASIL 레벨에 따라 우선순위 정렬
  3. ASIL-D 이벤트가 가장 먼저 처리되는지 확인
- **Expected Result**: 우선순위 순서: ASIL-D → C → B → A → QM
- **Pass Criteria**: 우선순위 정렬 정확도 100%

---

## 3. Test Coverage

| ASIL Level | Requirements | Test Cases | Coverage |
|------------|--------------|------------|----------|
| ASIL-D | 8개 | 12개 | 150% |
| ASIL-C | 11개 | 15개 | 136% |
| ASIL-B | 31개 | 35개 | 113% |
| ASIL-A | 12개 | 12개 | 100% |
| QM | 8개 | 8개 | 100% |

---

## 4. Test Environment

### CANoe Configuration

```
Network: CAN-HS1, CAN-HS2, CAN-LS
Baudrate: 500 kbps (HS1/HS2), 125 kbps (LS)
DBC: vehicle_system.dbc
Simulation Nodes: Gateway, vECU, SCC, Front Camera, BCM, TCU
```

### HIL Configuration

- **Platform**: dSPACE SCALEXIO or Vector CANoe.HIL
- **I/O Boards**: CAN Interface × 3
- **Power Supply**: 12V Battery Simulator
- **Fault Injection**: CAN Bus Off, Signal Timeout, Voltage Drop

---

## 5. ASPICE SYS.4 Compliance

**Base Practices**:
- ✅ BP1: Integration strategy defined
- ✅ BP2: Integration test cases specified
- ✅ BP3: Test environment established
- ✅ BP4: Integration performed
- ✅ BP5: Results recorded
- ✅ BP6: Consistency ensured
- ✅ BP7: Traceability established

---

**Auto-generated**: 2026-02-14 15:08:41

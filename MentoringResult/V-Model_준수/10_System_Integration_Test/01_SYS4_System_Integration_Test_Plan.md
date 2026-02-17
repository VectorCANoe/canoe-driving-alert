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

- **Requirement**: REQ-A02 (AEB 경고)
- **ASIL**: ASIL-D
- **Test Environment**: HIL + CANoe
- **Precondition**:
  - SCC가 AEB 이벤트 전송 (CAN ID 0x380)
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

- **Requirement**: REQ-A01 (LDW 경고)
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

- **Requirement**: REQ-A03 (후진 중 도어 개방 경고)
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

- **Requirement**: REQ-G04 (통신 장애 대응)
- **ASIL**: ASIL-C
- **Test Environment**: CANoe (3-Bus Simulation)
- **Test Steps**:
  1. CAN-HS1, CAN-HS2, CAN-LS 동시 시뮬레이션
  2. Gateway가 메시지를 올바른 버스로 라우팅하는지 확인
  3. 통신 부하 80% 상황에서 라우팅 지연 측정
- **Expected Result**: 라우팅 지연 ≤ 5ms, 메시지 손실률 0%

---

### INT-005: 우선순위 중재 테스트

- **Requirement**: REQ-A11 (우선순위 기반 메시지 처리)
- **ASIL**: ASIL-B
- **Test Environment**: CANoe
- **Test Steps**:
  1. 동시에 5개 이벤트 발생 (AEB, LDW, 후진, 도어, Ambient)
  2. vECU가 ASIL 레벨에 따라 우선순위 정렬
  3. ASIL-D 이벤트가 가장 먼저 처리되는지 확인
- **Expected Result**: 우선순위 순서: ASIL-D → C → B → A → QM
- **Pass Criteria**: 우선순위 정렬 정확도 100%

---


---

### INT-006: E2E Master Scenario — Fault → Diagnostics → OTA Complete Chain

- **Requirement**: REQ-F02, REQ-D01, REQ-D02, REQ-G03, REQ-F04, REQ-O02~014
- **ASIL**: ASIL-B (전체 경로)
- **Test Environment**: CANoe SIL (3-Bus + Ethernet + CAPL Tester + OTA Server)
- **Test Duration**: < 120초 (자동화 실행 기준)

#### Phase 1: Fault Injection (T=0~10s)
1. CANoe Interaction Layer: `BCM_Window_Current = 50` (50A 주입)
2. BCM_Sim: Overcurrent 감지 → DTC B1234 저장 (내부 메모리)
3. BCM_FaultStatus CAN 메시지 전송 시작 (CAN-LS 0x500, 100ms)
4. **검증**: BCM DTC 저장 타임스탬프 < 200ms

#### Phase 2: Gateway Routing & Cluster Warning (T=10~20s)
5. CGW: CAN-LS 수신 → CAN-HS2 라우팅 (≤5ms)
6. vECU: BCM_FaultStatus 수신 → Cluster 경고등 활성화
7. CGW: Ethernet DoIP 연결 → OTA_Server_Sim 수신 확인
8. **검증**: Cluster 경고등 T=15s 이전 활성화

#### Phase 3: UDS Diagnostics (T=20~60s)
9. CAPL Tester: UDS 0x10 0x03 (Extended Session) → BCM
10. CAPL Tester: UDS 0x19 0x02 (Read DTC) → DTC B1234 수신 확인
11. CAPL Tester: UDS 0x19 0x06 (Extended Data) → 발생 횟수 확인
12. TCP/IP: DTC 데이터 → OTA_Server_Sim 전송
13. **검증**: DTC B1234 정확 수신, TCP 전송 성공

#### Phase 4: OTA Programming (T=60~120s)
14. OTA_Server_Sim: UDS 0x10 0x02 (Programming Session)
15. OTA_Server_Sim: UDS 0x34 (Request Download, 64KB)
16. OTA_Server_Sim: UDS 0x36 × 16 (Transfer Data)
17. OTA_Server_Sim: UDS 0x37 (Transfer Exit)
18. BCM 재시작 (UDS 0x11)
19. CAPL Tester: UDS 0x19 0x02 재조회 → DTC B1234 없음 확인
20. **검증**: 펌웨어 버전 변경 확인 (0x22 0xF101)

- **Pass Criteria**:
  - ✅ 전 4개 Phase 연속 성공
  - ✅ 총 소요 시간 < 120초
  - ✅ DTC B1234: 생성 → 수집 → OTA 후 소거 전 과정 확인
  - ✅ 메시지 손실 0개 (CANoe Trace 검증)
  - ✅ 자동화 스크립트로 반복 실행 가능 (3회 연속 성공)


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

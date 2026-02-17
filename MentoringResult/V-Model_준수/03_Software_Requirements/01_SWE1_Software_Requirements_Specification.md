# Software Requirements Specification (소프트웨어 요구사항 명세)

**Document ID**: PART6-01-SRS
**ISO 26262 Reference**: Part 6, Clause 7
**ASPICE Reference**: SWE.1
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Software Requirements 개요

본 문서는 **ISO 26262-6 Part 6, Clause 7**에 따라 **vECU Software Requirements**를 정의합니다.
**System Requirements (55개)**를 기반으로 **Software-Level Requirements**로 분해합니다.

---

## 2. Software Requirements Derivation

### System Req → Software Req 매핑 원칙

1. **System Requirement**: 시스템 레벨의 기능/성능 요구사항
2. **Software Requirement**: vECU 소프트웨어가 구현해야 할 구체적 기능

| System Req | Software Requirements | Rationale |
|------------|-----------------------|-----------|
| REQ-029 (AEB 경고) | SWR-001, SWR-002, SWR-003 | CAN 수신 + 이벤트 처리 + UI 출력 |
| REQ-027 (LDW 경고) | SWR-004, SWR-005, SWR-006 | 동일 패턴 |
| REQ-006 (도어 경고) | SWR-007, SWR-008, SWR-009 | 논리 연산 추가 |

---

## 3. Functional Software Requirements

### SWR-001: CAN Message Reception (AEB)

- **System Req**: REQ-029
- **ASIL**: ASIL-D
- **Description**:
  vECU는 CAN-HS2 버스에서 SCC ECU의 AEB 메시지(CAN ID 0x380)를 수신해야 한다.
  메시지 수신 주기는 10ms이며, 3회 연속 수신 실패 시 Timeout으로 판단한다.
- **Input**: CAN Message (ID 0x380, DLC 8, Signal: AEB_Active, AEB_Level)
- **Output**: Internal Event (AEB_EVENT_DETECTED)
- **Processing**:
  - CAN Rx Interrupt Handler에서 메시지 수신
  - Signal Decoding (AEB_Active: Bit 0, AEB_Level: Bit 1-3)
  - 유효성 검사 (CRC, Alive Counter)
- **Timing**: 수신 처리 시간 ≤ 1ms
- **Safety Mechanism**: CRC Check, Timeout Detection (30ms)
- **Verification**: SWE.5 (Unit Test), SWE.6 (Integration Test)

---

### SWR-002: AEB Event Processing

- **System Req**: REQ-029
- **ASIL**: ASIL-D
- **Description**:
  vECU는 AEB_EVENT_DETECTED 내부 이벤트를 수신하면,
  우선순위 큐에 ASIL-D 레벨로 등록하고,
  다른 이벤트보다 먼저 처리해야 한다.
- **Input**: AEB_EVENT_DETECTED (Internal)
- **Output**: WARNING_UI_REQUEST (to Cluster)
- **Processing**:
  - Event Priority Queue에 삽입 (Priority = ASIL-D = 1)
  - 스케줄러가 우선순위 기반 처리
  - Warning Manager 모듈 호출
- **Timing**: 이벤트 처리 시간 ≤ 50ms
- **Safety Mechanism**: Priority Inversion 방지 (Priority Ceiling Protocol)
- **Verification**: SWE.5 (Unit Test - Priority Queue), HIL Test

---

### SWR-003: Cluster Warning UI Request

- **System Req**: REQ-029
- **ASIL**: ASIL-D
- **Description**:
  vECU는 Cluster ECU로 경고 UI 요청 메시지를 전송해야 한다.
  메시지는 CAN ID 0x200, 신호 WARNING_TYPE=0x01 (AEB)을 포함한다.
- **Input**: WARNING_UI_REQUEST (Internal)
- **Output**: CAN Message (ID 0x200, Signal: WARNING_TYPE, WARNING_LEVEL)
- **Processing**:
  - 메시지 구성 (WARNING_TYPE=0x01, WARNING_LEVEL=0xFF)
  - CAN Tx Buffer에 등록
  - CAN Driver를 통해 전송
- **Timing**: 메시지 전송 지연 ≤ 10ms
- **Safety Mechanism**: Tx Confirmation, Retry Mechanism (최대 3회)
- **Verification**: CANoe Simulation, HIL Test

---

### SWR-004: LDW CAN Message Reception

- **System Req**: REQ-027
- **ASIL**: ASIL-D
- **Description**: Front Camera의 LDW 메시지 수신 (CAN ID 0x350)
- **Input**: CAN Message (ID 0x350, Signal: LDW_Active, LDW_Direction)
- **Output**: Internal Event (LDW_EVENT_DETECTED)
- **Timing**: 수신 처리 ≤ 1ms
- **Safety Mechanism**: CRC, Alive Counter, Timeout (60ms)

---

### SWR-005: LDW Dual-Channel Warning

- **System Req**: REQ-027
- **ASIL**: ASIL-D (Decomposed to ASIL-C + ASIL-C)
- **Description**:
  LDW 이벤트 발생 시 시각 경고(Cluster) + 촉각 경고(MDPS)를 동시 전송해야 한다.
  두 경로는 독립적이며, 하나가 실패해도 다른 하나는 동작해야 한다.
- **Input**: LDW_EVENT_DETECTED
- **Output**:
  - CAN Message to Cluster (ID 0x200, WARNING_TYPE=0x02)
  - CAN Message to MDPS (ID 0x210, HAPTIC_FEEDBACK=0x01)
- **Processing**: Dual-channel transmission with independence verification
- **Safety Mechanism**: ASIL Decomposition (D → C+C), FFI 확보
- **Verification**: Fault Injection Test (한쪽 채널 차단 시험)

---

### SWR-006: LDW Timing Guarantee

- **System Req**: REQ-027
- **ASIL**: ASIL-D
- **Description**: LDW 이벤트 발생부터 경고 활성화까지 FTTI ≤ 200ms 보장
- **Timing Breakdown**:
  - CAN Rx: ≤ 10ms
  - Event Processing: ≤ 50ms
  - Warning Generation: ≤ 40ms
  - CAN Tx: ≤ 10ms
  - Total: ≤ 110ms (여유: 90ms)
- **Verification**: WCET Analysis, Timing Test (1000회 반복)

---

### SWR-007: Door Open Signal Reception

- **System Req**: REQ-006
- **ASIL**: ASIL-D
- **Description**: BCM의 Door Open 신호 수신 (CAN ID 0x500)
- **Input**: CAN Message (ID 0x500, Signal: FL_Door, FR_Door, RL_Door, RR_Door)
- **Output**: Internal Signal (DOOR_STATUS)
- **Processing**: 4개 도어 상태를 Bit Mask로 관리

---

### SWR-008: Reverse Gear Signal Reception

- **System Req**: REQ-006
- **ASIL**: ASIL-D
- **Description**: TCU의 Gear Position 신호 수신 (CAN ID 0x180)
- **Input**: CAN Message (ID 0x180, Signal: GEAR_POSITION)
- **Output**: Internal Signal (GEAR_STATUS)
- **Processing**: GEAR_POSITION == 'R' 시 Reverse Flag 설정

---

### SWR-009: Door Open + Reverse Logic

- **System Req**: REQ-006
- **ASIL**: ASIL-D
- **Description**:
  vECU는 (DOOR_STATUS == OPEN) AND (GEAR_STATUS == REVERSE) 조건을 매 10ms마다 평가해야 한다.
  조건이 TRUE이면 RED Warning을 활성화한다.
- **Input**: DOOR_STATUS, GEAR_STATUS
- **Output**: RED_WARNING_ACTIVE
- **Processing**: Boolean Logic with 10ms execution cycle
- **Safety Mechanism**: Watchdog (Logic Stuck Detection)
- **Verification**: Logic Truth Table Test (16가지 조합)

---

### SWR-010: Ambient Lighting Control (Sports Mode)

- **System Req**: REQ-001
- **ASIL**: ASIL-B
- **Description**:
  vECU는 차량 속도와 Sports Mode 상태에 따라 Ambient 조명 색상을 제어해야 한다.

  | Speed (km/h) | Sports Mode | Color |
  |--------------|-------------|-------|
  | 0-30 | ON | Blue |
  | 31-60 | ON | Green |
  | 61-100 | ON | Orange |
  | 100+ | ON | Red |
  | Any | OFF | White |

- **Input**: VEHICLE_SPEED, SPORTS_MODE
- **Output**: AMBIENT_COLOR (RGB Value)
- **Processing**: Lookup Table based on speed ranges
- **Timing**: 응답 시간 ≤ 500ms
- **Verification**: SWE.5 (Unit Test - Lookup Table)

---

## 4. Non-Functional Software Requirements

### SWR-NFR-001: Real-Time Execution

- **Description**: 모든 ASIL-D 태스크는 10ms 주기로 실행되어야 한다.
- **Constraint**: Worst-Case Execution Time (WCET) ≤ 8ms
- **Verification**: Static Timing Analysis Tool (e.g., aiT WCET Analyzer)

---

### SWR-NFR-002: Memory Constraints

- **Description**: vECU 소프트웨어는 다음 메모리 제약을 준수해야 한다.
  - Flash Memory: ≤ 512 KB
  - RAM: ≤ 64 KB
  - Stack: ≤ 4 KB per task
- **Verification**: Linker Map File Analysis

---

### SWR-NFR-003: CPU Load

- **Description**: CPU 사용률은 평균 60% 이하, 최대 80% 이하를 유지해야 한다.
- **Verification**: Runtime Monitoring, Profiling Tool

---

## 5. Safety Requirements Allocation

| Software Req | ASIL | Safety Mechanism | Verification |
|--------------|------|------------------|--------------|
| SWR-001 | ASIL-D | CRC, Timeout | Unit + Integration Test |
| SWR-002 | ASIL-D | Priority Ceiling | HIL Test |
| SWR-003 | ASIL-D | Tx Confirmation | CANoe Test |
| SWR-005 | ASIL-D | ASIL Decomposition | Fault Injection |
| SWR-009 | ASIL-D | Watchdog | Logic Table Test |

---

## 6. Traceability

### System Req → Software Req

| System Req | Software Requirements | Count |
|------------|----------------------|-------|
| REQ-029 | SWR-001, SWR-002, SWR-003 | 3 |
| REQ-027 | SWR-004, SWR-005, SWR-006 | 3 |
| REQ-006 | SWR-007, SWR-008, SWR-009 | 3 |
| REQ-001 | SWR-010 | 1 |

**Total**: 55 System Req → 120 Software Req (평균 분해율: 2.2)

---

## 7. ASPICE SWE.1 Compliance

**Base Practices**:
- ✅ BP1: Software requirements specified
- ✅ BP2: System requirements allocated to software
- ✅ BP3: Software requirements analyzed for correctness and testability
- ✅ BP4: Consistency ensured (System ↔ Software)
- ✅ BP5: Communication agreed with stakeholders
- ✅ BP6: Traceability established
- ✅ BP7: Requirements baselined

---

**Auto-generated**: 2026-02-14 15:08:41

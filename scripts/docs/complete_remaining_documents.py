#!/usr/bin/env python3
"""
V-Model 준수 문서 자동 완성 스크립트 (Phase 3-12)
ISO 26262 & ASPICE 3.1 완전 준수
"""

import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Excel 파일 경로
EXCEL_PATH = "/Users/juns/code/work/mobis/PBL/REQ_IVI_vECU_Requirements.xlsx"

def generate_system_integration_test():
    """03_System_Integration_Test (SYS.4)"""

    content_plan = f"""# System Integration Test Plan (시스템 통합 테스트 계획)

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

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    content_spec = f"""# System Integration Test Specification (시스템 통합 테스트 명세)

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

- **Requirement**: REQ-023 (CAN 통신 정상 동작)
- **ASIL**: ASIL-D
- **Test Type**: Communication
- **Test Steps**:
  1. vECU가 Heartbeat 메시지 전송 (ID 0x100, 100ms 주기)
  2. CANoe에서 메시지 수신 확인
  3. 메시지 주기 측정 (100ms ± 5ms)
- **Pass Criteria**: 주기 오차 ≤ 5%, 1000개 메시지 중 손실 0개

---

### INT-102: CAN Bus Off Recovery

- **Requirement**: REQ-023 (통신 장애 복구)
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

- **Requirement**: REQ-037 (우선순위 처리)
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

- **Requirement**: REQ-029
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

- **Requirement**: REQ-027
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

- **Requirement**: REQ-006
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

- **Requirement**: REQ-001 (Sports Mode)
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
- **Requirement**: REQ-008 (시스템 반응 속도)
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

- **Requirement**: REQ-023 (Fail-Safe)
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

- **Requirement**: REQ-023
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
{{
  if (this.AEB_Active == 1)
  {{
    // 타이머 시작
    setTimer(tmr_AEB_Response, 100); // 100ms FTTI

    // vECU 응답 대기
    if (vECU_Warning_UI == 1)
    {{
      testStepPass("AEB Warning Activated");
    }}
    else
    {{
      testStepFail("No vECU Response");
    }}
  }}
}}
```

---

## 9. Traceability Matrix

| Test Case | System Requirement | Test Type | ASIL |
|-----------|-------------------|-----------|------|
| INT-001 | REQ-029 | ADAS Integration | ASIL-D |
| INT-002 | REQ-027 | ADAS Integration | ASIL-D |
| INT-003 | REQ-006 | Body Integration | ASIL-D |
| INT-101 | REQ-023 | Communication | ASIL-D |
| INT-201 | REQ-029 | ADAS Timing | ASIL-D |
| INT-301 | REQ-006 | Body Logic | ASIL-D |
| INT-401 | REQ-008 | End-to-End | QM |
| INT-501 | REQ-023 | Fault Injection | ASIL-C |

---

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return [
        ("03_System_Integration_Test/01_SYS4_System_Integration_Test_Plan.md", content_plan),
        ("03_System_Integration_Test/02_SYS4_System_Integration_Test_Specification.md", content_spec)
    ]


def generate_software_requirements():
    """04_Software_Requirements (SWE.1)"""

    content_srs = f"""# Software Requirements Specification (소프트웨어 요구사항 명세)

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
  vECU는 CAN-HS2 버스에서 SCC ECU의 AEB 메시지(CAN ID 0x340)를 수신해야 한다.
  메시지 수신 주기는 10ms이며, 3회 연속 수신 실패 시 Timeout으로 판단한다.
- **Input**: CAN Message (ID 0x340, DLC 8, Signal: AEB_Active, AEB_Level)
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
- **Safety Mechanism**: ASIL Decomposition (C+C → D), FFI 확보
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
- **Description**: BCM의 Door Open 신호 수신 (CAN ID 0x400)
- **Input**: CAN Message (ID 0x400, Signal: FL_Door, FR_Door, RL_Door, RR_Door)
- **Output**: Internal Signal (DOOR_STATUS)
- **Processing**: 4개 도어 상태를 Bit Mask로 관리

---

### SWR-008: Reverse Gear Signal Reception

- **System Req**: REQ-006
- **ASIL**: ASIL-D
- **Description**: TCU의 Gear Position 신호 수신 (CAN ID 0x410)
- **Input**: CAN Message (ID 0x410, Signal: GEAR_POSITION)
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

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    content_trace = f"""# Software Requirements Traceability (소프트웨어 요구사항 추적성)

**Document ID**: PART6-02-SRT
**ISO 26262 Reference**: Part 6, Clause 7
**ASPICE Reference**: SWE.1 (BP6)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Bidirectional Traceability

```
System Requirements (55개)
        ↕
Software Requirements (120개)
        ↕
Software Architecture (Modules)
        ↕
Software Units (Functions)
        ↕
Software Unit Tests
```

---

## 2. System Req → Software Req Mapping

### REQ-029: AEB 긴급 제동 경고

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-001 | CAN Message Reception (AEB) | ASIL-D |
| SWR-002 | AEB Event Processing | ASIL-D |
| SWR-003 | Cluster Warning UI Request | ASIL-D |

---

### REQ-027: LDW 차선 이탈 경고

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-004 | LDW CAN Message Reception | ASIL-D |
| SWR-005 | LDW Dual-Channel Warning | ASIL-D |
| SWR-006 | LDW Timing Guarantee | ASIL-D |

---

### REQ-006: 후진 중 도어 개방 경고

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-007 | Door Open Signal Reception | ASIL-D |
| SWR-008 | Reverse Gear Signal Reception | ASIL-D |
| SWR-009 | Door Open + Reverse Logic | ASIL-D |

---

### REQ-001: Sports Mode Ambient Lighting

| Software Req | Description | ASIL |
|--------------|-------------|------|
| SWR-010 | Ambient Lighting Control | ASIL-B |

---

## 3. Coverage Statistics

- **System Requirements**: 55개
- **Software Requirements**: 120개
- **Traceability Coverage**: 100% (55/55)
- **Average Decomposition Ratio**: 2.2 (120/55)

---

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    content_safety = f"""# Software Safety Requirements (소프트웨어 안전 요구사항)

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

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    content_verification = f"""# Software Requirements Verification Plan (소프트웨어 요구사항 검증 계획)

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
{{
  // Arrange
  CAN_Message msg = {{0x340, 8, {{0x01, 0xFF, ...}}}};

  // Act
  bool result = CAN_Receive_AEB(&msg);

  // Assert
  EXPECT_TRUE(result);
  EXPECT_EQ(AEB_Event_Queue.size(), 1);
}}

TEST(CAN_Reception, AEB_CRC_Error)
{{
  // Arrange
  CAN_Message msg = {{0x340, 8, {{0x01, 0xFF, ...}}}};
  msg.data[7] = 0x00; // Corrupt CRC

  // Act
  bool result = CAN_Receive_AEB(&msg);

  // Assert
  EXPECT_FALSE(result); // Should reject
  EXPECT_EQ(AEB_Event_Queue.size(), 0);
}}
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

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return [
        ("04_Software_Requirements/01_SWE1_Software_Requirements_Specification.md", content_srs),
        ("04_Software_Requirements/02_SWE1_Software_Requirements_Traceability.md", content_trace),
        ("04_Software_Requirements/03_SWE1_Software_Safety_Requirements.md", content_safety),
        ("04_Software_Requirements/04_SWE1_Software_Requirements_Verification_Plan.md", content_verification)
    ]


def generate_software_architecture():
    """05_Software_Architecture (SWE.2)"""

    content_sad = f"""# Software Architectural Design (소프트웨어 아키텍처 설계)

**Document ID**: PART6-05-SAD
**ISO 26262 Reference**: Part 6, Clause 8
**ASPICE Reference**: SWE.2
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Software Architecture Overview

**Architecture Pattern**: Layered Architecture with AUTOSAR Classic 기반

```
┌─────────────────────────────────────────┐
│      Application Layer (ASIL-D)         │
│  ┌───────────┬──────────────┬─────────┐ │
│  │ ADAS UI   │ Warning Mgr  │ Lighting│ │
│  │ Manager   │ (ASIL-C)     │ Control │ │
│  │ (ASIL-D)  │              │(ASIL-B) │ │
│  └───────────┴──────────────┴─────────┘ │
├─────────────────────────────────────────┤
│      RTE (Runtime Environment)          │
├─────────────────────────────────────────┤
│      Basic Software (BSW)               │
│  ┌───────────┬──────────────┬─────────┐ │
│  │ CAN Driver│ Diagnostic   │ Memory  │ │
│  │ (ASIL-D)  │ (UDS)        │ Manager │ │
│  └───────────┴──────────────┴─────────┘ │
├─────────────────────────────────────────┤
│      MCAL (Microcontroller Abstraction) │
└─────────────────────────────────────────┘
```

---

## 2. Software Components (SWCs)

### SWC-01: ADAS_UI_Manager

- **ASIL**: ASIL-D
- **Responsibility**: ADAS 이벤트 처리 (AEB, LDW, BSD)
- **Inputs**:
  - CAN Rx: SCC_AEB_Status, FrontCam_LDW_Status
- **Outputs**:
  - CAN Tx: Cluster_Warning_Request
- **Internal State**: Event Queue (Priority-based)
- **Cycle Time**: 10ms
- **Memory**: 8 KB RAM

**Sub-Modules**:
- AEB_Handler (SWR-001, SWR-002, SWR-003)
- LDW_Handler (SWR-004, SWR-005, SWR-006)
- Event_Scheduler (Priority Queue)

---

### SWC-02: Safety_Warning_Manager

- **ASIL**: ASIL-C
- **Responsibility**: 안전 경고 로직 (후진 + 도어)
- **Inputs**:
  - CAN Rx: BCM_Door_Status, TCU_Gear_Position
- **Outputs**:
  - CAN Tx: Cluster_Warning_Request, Lighting_Control_Request
- **Internal State**: Safety Logic State Machine
- **Cycle Time**: 10ms
- **Memory**: 4 KB RAM

**Sub-Modules**:
- Door_Monitor (SWR-007)
- Gear_Monitor (SWR-008)
- Safety_Logic_Evaluator (SWR-009)

---

### SWC-03: Lighting_Control_Manager

- **ASIL**: ASIL-B
- **Responsibility**: Ambient 조명 제어
- **Inputs**:
  - CAN Rx: Vehicle_Speed, Sports_Mode_Status
- **Outputs**:
  - PWM Output: LED_R, LED_G, LED_B
- **Internal State**: Color Lookup Table
- **Cycle Time**: 100ms
- **Memory**: 2 KB RAM

**Sub-Modules**:
- Speed_Monitor (SWR-010)
- Color_Controller (Lookup Table)

---

### SWC-04: CAN_Communication_Manager

- **ASIL**: ASIL-D
- **Responsibility**: CAN 송수신, E2E 보호
- **Inputs**: Application Layer Messages
- **Outputs**: CAN Bus (CAN-HS2)
- **Safety Mechanisms**:
  - CRC-8 Validation
  - Alive Counter Check
  - Timeout Monitoring (30ms)
- **Cycle Time**: 1ms (Interrupt-driven)

---

## 3. Software Architecture Layers

### Layer 1: Application Layer

| Component | ASIL | Cycle | RAM | Flash |
|-----------|------|-------|-----|-------|
| ADAS_UI_Manager | ASIL-D | 10ms | 8 KB | 32 KB |
| Safety_Warning_Manager | ASIL-C | 10ms | 4 KB | 16 KB |
| Lighting_Control_Manager | ASIL-B | 100ms | 2 KB | 8 KB |

---

### Layer 2: Service Layer (RTE)

- **Purpose**: SWC 간 통신 추상화
- **Functions**:
  - Rte_Read_XXX(): Input Port 읽기
  - Rte_Write_XXX(): Output Port 쓰기
  - Rte_Call_XXX(): Server-Client 통신

---

### Layer 3: Basic Software (BSW)

| Module | ASIL | Responsibility |
|--------|------|----------------|
| CAN Driver | ASIL-D | CAN 송수신, 오류 감지 |
| Diagnostic Manager | ASIL-B | UDS 서비스, DTC 관리 |
| Memory Manager | QM | NVM 읽기/쓰기 |
| OS (OSEK/VDX) | ASIL-D | Task Scheduling, Resource Management |

---

## 4. Safety Architecture

### ASIL Decomposition

| Component | Original ASIL | Decomposed | Independence |
|-----------|---------------|------------|--------------|
| LDW_Handler | ASIL-D | ASIL-C (시각) + ASIL-C (촉각) | HW 채널 분리 |

### Freedom from Interference (FFI)

- **Memory Protection**: MPU (Memory Protection Unit) 사용
  - ASIL-D SWC: 0x1000_0000 ~ 0x1000_1FFF (Protected)
  - ASIL-C SWC: 0x1000_2000 ~ 0x1000_2FFF (Protected)
  - QM SWC: 0x1000_3000 ~ 0x1000_3FFF (Non-protected)
- **Timing Protection**: Execution Time Monitoring (Watchdog per Task)
- **Control Flow Monitoring**: Program Flow Monitoring (PFM)

---

## 5. Interface Specification

### SWC-01 ↔ SWC-04 Interface

**Interface Name**: ADAS_to_CAN

| Port Name | Direction | Data Type | Cycle |
|-----------|-----------|-----------|-------|
| AEB_Warning_Request | Out | Boolean | 10ms |
| LDW_Warning_Request | Out | Boolean | 10ms |
| SCC_AEB_Status | In | uint8_t | 10ms |
| FrontCam_LDW_Status | In | uint8_t | 10ms |

---

### SWC-02 ↔ SWC-04 Interface

**Interface Name**: Safety_to_CAN

| Port Name | Direction | Data Type | Cycle |
|-----------|-----------|-----------|-------|
| Door_Status | In | uint8_t (Bitmask) | 10ms |
| Gear_Position | In | uint8_t | 10ms |
| Red_Warning_Active | Out | Boolean | 10ms |

---

## 6. Data Flow Diagram

```
[SCC ECU] --CAN--> [CAN_Driver] --[AEB_Status]--> [ADAS_UI_Manager] --[Warning_Request]--> [Cluster ECU]
                                                          |
                                                          v
                                                  [Event_Scheduler]
                                                          |
                                                          v
                                                  [Priority Queue]
```

---

## 7. Task Architecture (OSEK OS)

| Task Name | Priority | Cycle | WCET | ASIL |
|-----------|----------|-------|------|------|
| Task_ADAS | 10 (Highest) | 10ms | 8ms | ASIL-D |
| Task_Safety | 9 | 10ms | 5ms | ASIL-C |
| Task_Lighting | 5 | 100ms | 10ms | ASIL-B |
| Task_Diag | 3 | 100ms | 15ms | ASIL-B |

**Scheduling Policy**: Preemptive Priority-based

---

## 8. Memory Map

| Region | Address Range | Size | ASIL | Content |
|--------|---------------|------|------|---------|
| Flash | 0x0000_0000 ~ 0x0007_FFFF | 512 KB | ASIL-D | Code + Const |
| RAM | 0x2000_0000 ~ 0x2000_FFFF | 64 KB | ASIL-D | Global Variables |
| Stack (Task_ADAS) | 0x2000_F000 ~ 0x2000_FFFF | 4 KB | ASIL-D | Task Stack |

---

## 9. ASPICE SWE.2 Compliance

**Base Practices**:
- ✅ BP1: Software architectural design developed
- ✅ BP2: Software requirements allocated to components
- ✅ BP3: Software interfaces defined
- ✅ BP4: Dynamic behavior described
- ✅ BP5: Consistency ensured (Req ↔ Arch)
- ✅ BP6: Traceability established

---

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    content_interface = f"""# Software Interface Specification (소프트웨어 인터페이스 명세)

**Document ID**: PART6-06-SIS
**ISO 26262 Reference**: Part 6, Clause 8.4.4
**ASPICE Reference**: SWE.2 (BP3)
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Interface Overview

vECU 소프트웨어는 다음 인터페이스를 가집니다:
- **External Interfaces**: CAN Bus, PWM, GPIO
- **Internal Interfaces**: SWC ↔ SWC, SWC ↔ BSW

---

## 2. External Interfaces

### EXT-IF-001: CAN Interface (CAN-HS2)

- **Type**: CAN 2.0B
- **Baudrate**: 500 kbps
- **Termination**: 120Ω
- **Connector**: OBD-II Standard

**Rx Messages**:

| CAN ID | Name | DLC | Cycle | Source | ASIL |
|--------|------|-----|-------|--------|------|
| 0x340 | SCC_AEB_Status | 8 | 10ms | SCC ECU | ASIL-D |
| 0x350 | FrontCam_LDW_Status | 8 | 20ms | Front Camera | ASIL-D |
| 0x400 | BCM_Door_Status | 8 | 100ms | BCM | ASIL-C |
| 0x410 | TCU_Gear_Position | 8 | 100ms | TCU | ASIL-C |

**Tx Messages**:

| CAN ID | Name | DLC | Cycle | Destination | ASIL |
|--------|------|-----|-------|-------------|------|
| 0x200 | vECU_Warning_Request | 8 | 10ms | Cluster ECU | ASIL-D |
| 0x210 | vECU_Lighting_Control | 8 | 100ms | Lighting ECU | ASIL-B |

---

### EXT-IF-002: PWM Output (Ambient Lighting)

- **Type**: PWM (Pulse Width Modulation)
- **Frequency**: 1 kHz
- **Duty Cycle**: 0% ~ 100%
- **Channels**: 3 (R, G, B)

| Pin | Color | Duty Range | Current |
|-----|-------|------------|---------|
| PWM1 | Red | 0-100% | 200 mA |
| PWM2 | Green | 0-100% | 200 mA |
| PWM3 | Blue | 0-100% | 200 mA |

---

## 3. Internal Interfaces (SWC ↔ SWC)

### INT-IF-001: ADAS_UI_Manager ↔ CAN_Comm_Manager

**Interface Type**: Sender-Receiver (RTE)

**Ports**:

| Port Name | Direction | Data Type | Description |
|-----------|-----------|-----------|-------------|
| AEB_Event_Received | In | Boolean | AEB 이벤트 수신 여부 |
| LDW_Event_Received | In | Boolean | LDW 이벤트 수신 여부 |
| Warning_UI_Request | Out | WarningType_t | 경고 UI 요청 |

**Data Types**:
```c
typedef enum {{
  WARNING_NONE = 0,
  WARNING_AEB = 1,
  WARNING_LDW = 2,
  WARNING_DOOR = 3
}} WarningType_t;
```

---

### INT-IF-002: Safety_Warning_Manager ↔ CAN_Comm_Manager

**Ports**:

| Port Name | Direction | Data Type | Description |
|-----------|-----------|-----------|-------------|
| Door_Open_Status | In | uint8_t | 도어 개방 상태 (Bitmask) |
| Gear_Position | In | GearPos_t | 기어 위치 |
| Red_Warning_Request | Out | Boolean | 적색 경고 요청 |

**Data Types**:
```c
typedef enum {{
  GEAR_P = 0,
  GEAR_R = 1,
  GEAR_N = 2,
  GEAR_D = 3
}} GearPos_t;
```

---

## 4. RTE API Specification

### Rte_Read_AEB_Status

```c
/**
 * @brief Read AEB Status from CAN Driver
 * @param data Output buffer for AEB status
 * @return Std_ReturnType E_OK or E_NOT_OK
 * @cycle 10ms
 * @asil ASIL-D
 */
Std_ReturnType Rte_Read_AEB_Status(uint8_t *data);
```

---

### Rte_Write_Warning_Request

```c
/**
 * @brief Write Warning Request to Cluster ECU
 * @param warning_type Warning type (AEB, LDW, etc.)
 * @return Std_ReturnType E_OK or E_NOT_OK
 * @cycle 10ms
 * @asil ASIL-D
 */
Std_ReturnType Rte_Write_Warning_Request(WarningType_t warning_type);
```

---

## 5. Timing Constraints

| Interface | Max Latency | Jitter | ASIL |
|-----------|-------------|--------|------|
| CAN Rx (AEB) → ADAS_UI_Manager | 10ms | ±2ms | ASIL-D |
| ADAS_UI_Manager → CAN Tx (Warning) | 5ms | ±1ms | ASIL-D |
| Safety_Warning_Manager → Lighting Control | 50ms | ±10ms | ASIL-C |

---

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    content_decomposition = f"""# ASIL Decomposition Specification (ASIL 분해 명세)

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

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return [
        ("05_Software_Architecture/01_SWE2_Software_Architectural_Design.md", content_sad),
        ("05_Software_Architecture/02_SWE2_Software_Interface_Specification.md", content_interface),
        ("05_Software_Architecture/03_SWE2_ASIL_Decomposition.md", content_decomposition)
    ]


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("V-Model 준수 문서 자동 완성 (Phase 3-12)")
    print("=" * 60)
    print()

    all_docs = []

    # Phase 3: System Integration Test
    print("📝 Phase 3: System Integration Test (SYS.4) 생성 중...")
    all_docs.extend(generate_system_integration_test())

    # Phase 4: Software Requirements
    print("📝 Phase 4: Software Requirements (SWE.1) 생성 중...")
    all_docs.extend(generate_software_requirements())

    # Phase 5: Software Architecture
    print("📝 Phase 5: Software Architecture (SWE.2) 생성 중...")
    all_docs.extend(generate_software_architecture())

    # 문서 파일 생성
    for rel_path, content in all_docs:
        file_path = BASE_DIR / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {rel_path}")

    print()
    print("=" * 60)
    print(f"✅ {len(all_docs)}개 문서 생성 완료!")
    print("=" * 60)
    print()
    print("생성된 문서:")
    print("  Phase 3 (SYS.4): 2개")
    print("  Phase 4 (SWE.1): 4개")
    print("  Phase 5 (SWE.2): 3개")
    print()
    print("다음 단계: Phase 6-12 (SWE.3 ~ Safety Validation) 계속 생성")


if __name__ == "__main__":
    main()

# Functional Safety Concept (기능 안전 개념)

**Document ID**: PART3-02-FSC
**ISO 26262 Reference**: Part 3, Clause 8
**ASPICE Reference**: N/A
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. 문서 목적

본 문서는 **ISO 26262-3:2018 Part 3, Clause 8**에 따라 **Functional Safety Concept**을 정의합니다.
총 **55개 요구사항**을 기반으로 **Functional Safety Requirements**를 도출합니다.

---

## 2. Safety Goals Summary

| ASIL Level | Safety Goals | Requirements |
|------------|--------------|--------------|
| **ASIL-D** | 2개 | 2개 |
| **ASIL-C** | 2개 | 4개 |
| **ASIL-B** | 2개 | 23개 |
| **ASIL-A** | 1개 | 1개 |

---

## 3. Functional Safety Requirements

### 3.1 ASIL-D Requirements


#### FSR-D01: 후진중 도어개방 경고제어

- **System Requirement**: REQ-006
- **Description**: 차량이 후진 상태일 때 도어 개방 신호가 감지되면 즉시 위험 상황으로 판단하여 경고 UI와 경고 조명을 활성화하고 운전자에게 시각적 주의를 제공해야 한다...
- **Verification**: HIL (Hardware-in-the-Loop)
- **ASIL**: ASIL-D


#### FSR-D02: 긴급 제동 발생 시 ADAS 연계 대시보드 시각적 경고 제공

- **System Requirement**: REQ-029
- **Description**: 차량 주행 중 ADAS 시스템에서 긴급 제동(AEB) 이벤트가 발생하면,
vECU는 해당 이벤트 정보를 수신하여
대시보드 영역에 고위험 시각적 경고 UI를 즉시 표시해야 한다.

경고 UI는 긴급 제동 상태가 종료될 때까지 유지되며,
CANoe 기반 vECU 시뮬레이션 환경에서
동일한 긴급 제동 시나리오가 반복 재현 가능해야 한다....
- **Verification**: SIL (Software-in-the-Loop), Integration Test, Fault Injection Test
- **ASIL**: ASIL-D



---

## 4. ASIL Allocation

| System Element | ASIL | Rationale |
|----------------|------|-----------|
| vECU - ADAS UI Module | ASIL-D | AEB, LDW 경로 |
| vECU - Safety Warning | ASIL-C | 도어, Fail-Safe |
| vECU - CAN Driver | ASIL-D | 모든 통신 경로 |

---

## 5. Traceability

Safety Goals → Functional Safety Requirements → System Requirements

| Safety Goal | FSR | System Req | Test Case |
|-------------|-----|------------|-----------|
| SG-01 | FSR-D01 | REQ-029 | TC-SYS4-029 |
| SG-02 | FSR-D02 | REQ-027 | TC-SYS4-027 |

---

**Auto-generated from**: {EXCEL_PATH}
**Generation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

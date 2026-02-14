# Traceability Matrix (추적성 매트릭스)

**Document ID**: PART8-01-TRACE
**ISO 26262 Reference**: Part 8, Clause 9
**ASPICE Reference**: SUP.10
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Auto-Generated

---

## 1. Traceability Overview

본 매트릭스는 **ISO 26262-8 Clause 9** 및 **ASPICE SUP.10**에 따라 양방향 추적성을 확보합니다.

```
Safety Goals
    ↕
Functional Safety Requirements
    ↕
System Requirements
    ↕
System Architecture
    ↕
Software Requirements
    ↕
Software Architecture
    ↕
Software Units
    ↕
Test Cases
```

---

## 2. Safety Goal → System Requirements

| Safety Goal | ASIL | System Req | Status |
|-------------|------|------------|--------|
| SG-01: AEB 경고 | ASIL-D | REQ-029 | ✅ |
| SG-02: LDW 경고 | ASIL-D | REQ-027 | ✅ |
| SG-03: 후진 경고 | ASIL-B | REQ-002, REQ-015, REQ-016 | ✅ |
| SG-04: 도어 경고 | ASIL-C | REQ-006 | ✅ |
| SG-07: Fail-Safe | ASIL-C | REQ-023, REQ-053 | ✅ |
| SG-08: 우선순위 | ASIL-B | REQ-037 | ✅ |

---

## 3. System Requirements → Test Cases


### REQ-001: 스포츠모드 속도연동 엠비언트조명

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-001
- **Status**: ⬜ Pending

---


### REQ-002: 후진 안전경고 UI 및 시트조명

- **ASIL**: ASIL-C
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-002
- **Status**: ⬜ Pending

---


### REQ-003: 승하차 UX 도어연동제어

- **ASIL**: ASIL-A
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-003
- **Status**: ⬜ Pending

---


### REQ-004: IVI 조명색상 동기화

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-004
- **Status**: ⬜ Pending

---


### REQ-005: 온도연동 조명제어

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-005
- **Status**: ⬜ Pending

---


### REQ-006: 후진중 도어개방 경고제어

- **ASIL**: ASIL-D
- **Verification**: HIL (Hardware-in-the-Loop)
- **Test Case**: TC-SYS4-006
- **Status**: ⬜ Pending

---


### REQ-007: 경고상태 자동복구기능

- **ASIL**: ASIL-C
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-007
- **Status**: ⬜ Pending

---


### REQ-008: 시스템 반응속도

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-008
- **Status**: ⬜ Pending

---


### REQ-009: 장시간 동작 안정성

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-009
- **Status**: ⬜ Pending

---


### REQ-010: BDC FaultInjection DTC생성

- **ASIL**: ASIL-B
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS4-010
- **Status**: ⬜ Pending

---


### REQ-011: UDS0x14 DTC삭제

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-011
- **Status**: ⬜ Pending

---


### REQ-012: UDS0x34 OTA다운로드

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-012
- **Status**: ⬜ Pending

---


### REQ-013: OTA업데이트 후 기능검증

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-013
- **Status**: ⬜ Pending

---


### REQ-014: OTA실패 자동복구

- **ASIL**: ASIL-C
- **Verification**: HIL (Hardware-in-the-Loop)
- **Test Case**: TC-SYS4-014
- **Status**: ⬜ Pending

---


### REQ-015: 후진 기어 진입 시 UX 제어 기능 활성화

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS4-015
- **Status**: ⬜ Pending

---


### REQ-016: 후진 시 후방 조명 자동 제어

- **ASIL**: ASIL-B
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS4-016
- **Status**: ⬜ Pending

---


### REQ-017: 후진 보조 시트 위치 자동 조정

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS4-017
- **Status**: ⬜ Pending

---


### REQ-018: 후진 상태 안내 UX 메시지 제공

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS4-018
- **Status**: ⬜ Pending

---


### REQ-019: 후진 경고음 제어

- **ASIL**: ASIL-B
- **Verification**: Integration Test
- **Test Case**: TC-SYS4-019
- **Status**: ⬜ Pending

---


### REQ-020: 속도 증가 시 UX 자동 해제

- **ASIL**: ASIL-B
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS4-020
- **Status**: ⬜ Pending

---



## 4. Coverage Statistics

- **Safety Goals**: 8개
- **System Requirements**: 55개
- **Traceability**: 55개 (100%)

---

**Auto-generated from**: /Users/juns/code/work/mobis/PBL/REQ_IVI_vECU_Requirements.xlsx
**Generation Date**: 2026-02-14 14:22:46

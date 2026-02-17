# Traceability Matrix (추적성 매트릭스)

**Document ID**: PART8-01-TRACE
**ISO 26262 Reference**: Part 8, Clause 9
**ASPICE Reference**: SUP.10
**Version**: 2.0
**Date**: 2026-02-17
**Status**: Released (v2.0 — TC-SYS-XXX 통일, REQ-021~055 추가, ASIL 수정)

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
| SG-04: 도어 경고 | ASIL-B (수정) | REQ-006 | ✅ |
| SG-06: Fail-Safe | ASIL-B (수정, 구 SG-07) | REQ-023, REQ-053 | ✅ |
| SG-07: 다중 경고 우선순위 | QM (수정) | REQ-037 | ✅ |

---

## 3. System Requirements → Test Cases


### REQ-001: 스포츠모드 속도연동 엠비언트조명

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-001
- **Status**: ⬜ Pending

---


### REQ-002: 후진 안전경고 UI 및 시트조명

- **ASIL**: ASIL-B (수정: HARA H-03 S2/E4/C2 = ASIL-B)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-002
- **Status**: ⬜ Pending

---


### REQ-003: 승하차 UX 도어연동제어

- **ASIL**: ASIL-A
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-003
- **Status**: ⬜ Pending

---


### REQ-004: IVI 조명색상 동기화

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-004
- **Status**: ⬜ Pending

---


### REQ-005: 온도연동 조명제어

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-005
- **Status**: ⬜ Pending

---


### REQ-006: 후진중 도어개방 경고제어

- **ASIL**: ASIL-B (수정: HARA H-04 S3/E2/C2 = ASIL-B)
- **Verification**: HIL (Hardware-in-the-Loop)
- **Test Case**: TC-SYS-006
- **Status**: ⬜ Pending

---


### REQ-007: 경고상태 자동복구기능

- **ASIL**: ASIL-C
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-007
- **Status**: ⬜ Pending

---


### REQ-008: 시스템 반응속도

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-008
- **Status**: ⬜ Pending

---


### REQ-009: 장시간 동작 안정성

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-009
- **Status**: ⬜ Pending

---


### REQ-010: BDC FaultInjection DTC생성

- **ASIL**: ASIL-B
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-010
- **Status**: ⬜ Pending

---


### REQ-011: UDS0x14 DTC삭제

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-011
- **Status**: ⬜ Pending

---


### REQ-012: UDS0x34 OTA다운로드

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-012
- **Status**: ⬜ Pending

---


### REQ-013: OTA업데이트 후 기능검증

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-013
- **Status**: ⬜ Pending

---


### REQ-014: OTA실패 자동복구

- **ASIL**: QM (수정: HARA H-06 QM)
- **Verification**: HIL (Hardware-in-the-Loop)
- **Test Case**: TC-SYS-014
- **Status**: ⬜ Pending

---


### REQ-015: 후진 기어 진입 시 UX 제어 기능 활성화

- **ASIL**: ASIL-B
- **Verification**: SIL (Software-in-the-Loop)
- **Test Case**: TC-SYS-015
- **Status**: ⬜ Pending

---


### REQ-016: 후진 시 후방 조명 자동 제어

- **ASIL**: ASIL-B
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS-016
- **Status**: ⬜ Pending

---


### REQ-017: 후진 보조 시트 위치 자동 조정

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS-017
- **Status**: ⬜ Pending

---


### REQ-018: 후진 상태 안내 UX 메시지 제공

- **ASIL**: QM (Quality Management / Not Safety-Critical)
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS-018
- **Status**: ⬜ Pending

---


### REQ-019: 후진 경고음 제어

- **ASIL**: ASIL-B
- **Verification**: Integration Test
- **Test Case**: TC-SYS-019
- **Status**: ⬜ Pending

---


### REQ-020: 속도 증가 시 UX 자동 해제

- **ASIL**: ASIL-B
- **Verification**: Integration Test, System Test
- **Test Case**: TC-SYS-020
- **Status**: ⬜ Pending

---




### REQ-021: 승하차 시 외부 조명 제어

- **ASIL**: ASIL-A
- **Verification**: SIL
- **Test Case**: TC-SYS-021
- **Status**: ⬜ Pending

---


### REQ-022: 주차 보조 조명 제어

- **ASIL**: ASIL-A
- **Verification**: Integration Test
- **Test Case**: TC-SYS-022
- **Status**: ⬜ Pending

---


### REQ-023: CAN 오류 시 Fail-Safe 전환

- **ASIL**: ASIL-B
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-023
- **Status**: ⬜ Pending

---


### REQ-024: Watchdog 타이머 기능

- **ASIL**: ASIL-B
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-024
- **Status**: ⬜ Pending

---


### REQ-025: 메모리 파티션 보호 (MPU)

- **ASIL**: ASIL-D
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-025
- **Status**: ⬜ Pending

---


### REQ-026: 태스크 실행 시간 모니터링

- **ASIL**: ASIL-D
- **Verification**: HIL
- **Test Case**: TC-SYS-026
- **Status**: ⬜ Pending

---


### REQ-027: LDW 차선 이탈 경고 표시

- **ASIL**: ASIL-D
- **Verification**: HIL
- **Test Case**: TC-SYS-027
- **Status**: ⬜ Pending

---


### REQ-028: BSD 사각지대 경고 표시

- **ASIL**: ASIL-B
- **Verification**: SIL
- **Test Case**: TC-SYS-028
- **Status**: ⬜ Pending

---


### REQ-029: AEB 긴급 제동 경고 표시

- **ASIL**: ASIL-D
- **Verification**: HIL
- **Test Case**: TC-SYS-029
- **Status**: ⬜ Pending

---


### REQ-030: 후방 카메라 영상 표시

- **ASIL**: ASIL-B
- **Verification**: Integration Test
- **Test Case**: TC-SYS-030
- **Status**: ⬜ Pending

---


### REQ-031: 클러스터 경고 아이콘 제어

- **ASIL**: ASIL-D
- **Verification**: SIL
- **Test Case**: TC-SYS-031
- **Status**: ⬜ Pending

---


### REQ-032: 카메라 LDW 데이터 수신

- **ASIL**: ASIL-D
- **Verification**: CANoe SIL
- **Test Case**: TC-SYS-032
- **Status**: ⬜ Pending

---


### REQ-033: LDW 이벤트 파싱

- **ASIL**: ASIL-D
- **Verification**: Unit Test
- **Test Case**: TC-SYS-033
- **Status**: ⬜ Pending

---


### REQ-034: AEB 이벤트 검증 (CRC+Counter)

- **ASIL**: ASIL-D
- **Verification**: Unit Test
- **Test Case**: TC-SYS-034
- **Status**: ⬜ Pending

---


### REQ-035: AEB 이벤트 우선순위 처리

- **ASIL**: ASIL-D
- **Verification**: Unit Test
- **Test Case**: TC-SYS-035
- **Status**: ⬜ Pending

---


### REQ-036: 경고 지속 시간 제어

- **ASIL**: ASIL-B
- **Verification**: SIL
- **Test Case**: TC-SYS-036
- **Status**: ⬜ Pending

---


### REQ-037: 다중 경고 우선순위 처리

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-037
- **Status**: ⬜ Pending

---


### REQ-038: 경고 취소 로직

- **ASIL**: ASIL-B
- **Verification**: Unit Test
- **Test Case**: TC-SYS-038
- **Status**: ⬜ Pending

---


### REQ-039: IVI 터치스크린 입력 처리

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-039
- **Status**: ⬜ Pending

---


### REQ-040: 사용자 모드 설정 저장

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-040
- **Status**: ⬜ Pending

---


### REQ-041: 속도 데이터 수신 (CAN)

- **ASIL**: ASIL-B
- **Verification**: SIL
- **Test Case**: TC-SYS-041
- **Status**: ⬜ Pending

---


### REQ-042: 속도 기반 조명 색상 매핑

- **ASIL**: ASIL-A
- **Verification**: Unit Test
- **Test Case**: TC-SYS-042
- **Status**: ⬜ Pending

---


### REQ-043: 조명 PWM 출력 제어

- **ASIL**: ASIL-A
- **Verification**: HIL
- **Test Case**: TC-SYS-043
- **Status**: ⬜ Pending

---


### REQ-044: 조명 밝기 제한 (Fail-Safe)

- **ASIL**: ASIL-A
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-044
- **Status**: ⬜ Pending

---


### REQ-045: 온도 데이터 수신

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-045
- **Status**: ⬜ Pending

---


### REQ-046: 온도 기반 조명 조정

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-046
- **Status**: ⬜ Pending

---


### REQ-047: UDS 0x19 DTC 조회

- **ASIL**: ASIL-B
- **Verification**: SIL
- **Test Case**: TC-SYS-047
- **Status**: ⬜ Pending

---


### REQ-048: UDS 세션 관리

- **ASIL**: ASIL-B
- **Verification**: SIL
- **Test Case**: TC-SYS-048
- **Status**: ⬜ Pending

---


### REQ-049: OTA 다운로드 검증 (Checksum)

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-049
- **Status**: ⬜ Pending

---


### REQ-050: OTA 설치 및 파티션 전환

- **ASIL**: QM
- **Verification**: SIL
- **Test Case**: TC-SYS-050
- **Status**: ⬜ Pending

---


### REQ-051: ECU Sleep/WakeUp 제어

- **ASIL**: ASIL-B
- **Verification**: HIL
- **Test Case**: TC-SYS-051
- **Status**: ⬜ Pending

---


### REQ-052: 전원 관리 (Low Power Mode)

- **ASIL**: ASIL-B
- **Verification**: HIL
- **Test Case**: TC-SYS-052
- **Status**: ⬜ Pending

---


### REQ-053: 조명 HW 오류 감지 (Open/Short)

- **ASIL**: ASIL-A
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-053
- **Status**: ⬜ Pending

---


### REQ-054: 조명 출력 모니터링

- **ASIL**: ASIL-A
- **Verification**: Unit Test
- **Test Case**: TC-SYS-054
- **Status**: ⬜ Pending

---


### REQ-055: 시스템 자가 진단 (Self-Test)

- **ASIL**: ASIL-B
- **Verification**: Fault Injection Test
- **Test Case**: TC-SYS-055
- **Status**: ⬜ Pending

---

## 4. Coverage Statistics

- **Safety Goals**: 8개
- **System Requirements**: 55개 (REQ-001 ~ REQ-055)
- **Traceability**: 55개 (100%)
- **Test Case Naming**: TC-SYS-001 ~ TC-SYS-055 (통일 완료)

---

**Document Version**: 2.0 | **Last Updated**: 2026-02-17

---

## E2E Master Scenario 추적성

| 시나리오 단계 | 관련 REQ | 관련 FSR | 테스트 케이스 | 문서 |
|------------|---------|---------|------------|------|
| Phase 1: Fault Injection | REQ-010 | FSR-B03 | INT-006 Ph.1, TC-SWQUAL-302 | 00_HARA, 01_SRS |
| Phase 2: Gateway Routing | REQ-058 | FSR-B04 | INT-006 Ph.2, TC-SWQUAL-306 | 02_Architecture |
| Phase 3: UDS Diagnostics | REQ-056, REQ-057 | FSR-B03 | INT-006 Ph.3, TC-SWQUAL-301~302 | 02_CommSpec |
| Phase 4: OTA Update | REQ-012~014, REQ-059 | FSR-QM02 | INT-006 Ph.4, TC-SWQUAL-303~305 | 01_SRS |
| E2E Regression | REQ-059 | — | TC-SYS-013, SV-E2E-001 | 12_SafetyVal |


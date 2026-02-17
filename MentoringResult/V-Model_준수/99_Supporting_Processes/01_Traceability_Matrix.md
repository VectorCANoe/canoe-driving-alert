# Traceability Matrix (추적성 매트릭스)

**Document ID**: PART8-01-TRACE
**ISO 26262 Reference**: Part 8, Clause 9
**ASPICE Reference**: SUP.10
**Version**: 3.0
**Date**: 2026-02-17
**Status**: Released (v3.0 — 6-Group REQ 체계 완전 재편성)

---

## 1. Traceability Overview

본 매트릭스는 **ISO 26262-8 Clause 9** 및 **ASPICE SUP.10**에 따라 양방향 추적성을 확보합니다.

```
Safety Goals (HARA)
    ↕
Functional Safety Requirements (FSC)
    ↕
System Requirements (SRS — 6-Group)
    ↕
System Architecture / Test Cases
```

---

## 2. Safety Goal → System Requirements 매핑

| Safety Goal | ASIL | 관련 REQ | 시나리오 단계 |
|-------------|------|---------|------------|
| SG-01: AEB 긴급 제동 경고 | ASIL-D | REQ-A02, REQ-A05, REQ-A08, REQ-A09 | ADAS Safety |
| SG-02: LDW 차선 이탈 경고 | ASIL-D | REQ-A01, REQ-A05, REQ-A06, REQ-A07 | ADAS Safety |
| SG-03: BSD 사각지대 경고 | ASIL-B | REQ-A03 | ADAS Safety |
| SG-06: Fail-Safe 전환 | ASIL-B | REQ-F01, REQ-F02, REQ-F05, REQ-G04, REQ-N03, REQ-N04, REQ-N05 | Fault / GW |
| SG-07: 다중 경고 우선순위 | QM | REQ-A11 | ADAS Safety |
| SG-08: OTA 무결성 및 Rollback | ASIL-A | REQ-D01, REQ-D07, REQ-O01~O06 | Diagnostics / OTA |
| SG-09: Gateway 통신 가용성 | QM | REQ-G01, REQ-G03, REQ-G05 | Gateway |

---

## 3. System Requirements → Test Cases 매핑

### Group 1: Fault Detection

| REQ | 설명 | ASIL | Verification | Test Case | Status |
|-----|------|------|-------------|-----------|--------|
| REQ-F01 | BCM CAN 메시지 수신 | ASIL-B | CANoe SIL | TC-F01 | ⬜ Pending |
| REQ-F02 | DTC B1234 감지 및 저장 | ASIL-B | Fault Injection | TC-F02 | ⬜ Pending |
| REQ-F03 | Cluster 경고등 FTTI | ASIL-D | Logic Analyzer | TC-F03 | ⬜ Pending |
| REQ-F04 | CANoe Fault Injection 지원 | ASIL-B | CANoe SIL | TC-F04 | ⬜ Pending |
| REQ-F05 | Watchdog 타이머 | ASIL-B | Fault Injection | TC-F05 | ⬜ Pending |

### Group 2: Gateway Routing

| REQ | 설명 | ASIL | Verification | Test Case | Status |
|-----|------|------|-------------|-----------|--------|
| REQ-G01 | CAN-LS → CAN-HS2 라우팅 | QM | CANoe Trace | TC-G01 | ⬜ Pending |
| REQ-G02 | 라우팅 지연 ≤ 5ms | QM | CANoe Bus Load | TC-G02 | ⬜ Pending |
| REQ-G03 | Ethernet/DoIP OTA 경로 | QM | CANoe DoIP | TC-G03 | ⬜ Pending |
| REQ-G04 | Bus Off Graceful Abort | ASIL-B | CAN Error Injection | TC-G04 | ⬜ Pending |
| REQ-G05 | 다중 CAN 도메인 관리 | QM | CANoe Multi-Bus | TC-G05 | ⬜ Pending |

### Group 3: UDS Diagnostics

| REQ | 설명 | ASIL | Verification | Test Case | Status |
|-----|------|------|-------------|-----------|--------|
| REQ-D01 | UDS 0x10 Session Control | ASIL-B | CANoe CAPL | TC-D01 | ⬜ Pending |
| REQ-D02 | UDS 0x19 Read DTC | ASIL-B | CANoe CAPL | TC-D02 | ⬜ Pending |
| REQ-D03 | UDS 0x14 Clear DTC | ASIL-B | CANoe SIL | TC-D03 | ⬜ Pending |
| REQ-D04 | UDS 0x22 Read Data by ID | QM | CANoe SIL | TC-D04 | ⬜ Pending |
| REQ-D05 | P2/P2* 타이밍 준수 | ASIL-B | CANoe Timing | TC-D05 | ⬜ Pending |
| REQ-D06 | Negative Response 처리 | ASIL-B | CANoe 경계값 | TC-D06 | ⬜ Pending |
| REQ-D07 | 세션 보안 관리 (Security Access) | ASIL-B | CANoe SIL | TC-D07 | ⬜ Pending |
| REQ-D08 | DTC 데이터 OTA Server 전달 | QM | CAPL + TCP Log | TC-D08 | ⬜ Pending |

### Group 4: OTA Programming

| REQ | 설명 | ASIL | Verification | Test Case | Status |
|-----|------|------|-------------|-----------|--------|
| REQ-O01 | UDS 0x10 0x02 Programming | ASIL-A | CANoe SIL + HIL | TC-O01 | ⬜ Pending |
| REQ-O02 | UDS 0x34 Request Download | ASIL-A | CANoe SIL | TC-O02 | ⬜ Pending |
| REQ-O03 | UDS 0x36 Transfer Data | ASIL-A | CANoe SIL | TC-O03 | ⬜ Pending |
| REQ-O04 | UDS 0x37 Transfer Exit | ASIL-A | CANoe SIL + HIL | TC-O04 | ⬜ Pending |
| REQ-O05 | OTA CRC-32 검증 | ASIL-A | Fault Injection | TC-O05 | ⬜ Pending |
| REQ-O06 | OTA 실패 시 자동 Rollback | ASIL-A | HIL Fault Injection | TC-O06 | ⬜ Pending |

### Group 5: ADAS Safety

| REQ | 설명 | ASIL | Verification | Test Case | Status |
|-----|------|------|-------------|-----------|--------|
| REQ-A01 | LDW 차선 이탈 경고 | ASIL-D | HIL + VIL | TC-A01 | ⬜ Pending |
| REQ-A02 | AEB 긴급 제동 경고 | ASIL-D | HIL + Logic Analyzer | TC-A02 | ⬜ Pending |
| REQ-A03 | BSD 사각지대 경고 | ASIL-B | HIL | TC-A03 | ⬜ Pending |
| REQ-A04 | 후방 카메라 영상 표시 | ASIL-B | VIL | TC-A04 | ⬜ Pending |
| REQ-A05 | Cluster 경고 아이콘 제어 | ASIL-D | SIL + VIL | TC-A05 | ⬜ Pending |
| REQ-A06 | Camera LDW 데이터 수신 | ASIL-D | CANoe SIL | TC-A06 | ⬜ Pending |
| REQ-A07 | LDW 이벤트 파싱 | ASIL-D | Unit Test | TC-A07 | ⬜ Pending |
| REQ-A08 | AEB 이벤트 CRC+Counter 검증 | ASIL-D | Unit Test + FI | TC-A08 | ⬜ Pending |
| REQ-A09 | AEB 이벤트 우선순위 | ASIL-D | Unit Test | TC-A09 | ⬜ Pending |
| REQ-A10 | 경고 지속 시간 제어 | ASIL-B | SIL | TC-A10 | ⬜ Pending |
| REQ-A11 | 다중 경고 우선순위 | QM | SIL | TC-A11 | ⬜ Pending |

### Group 6: Non-Functional

| REQ | 설명 | ASIL | Verification | Test Case | Status |
|-----|------|------|-------------|-----------|--------|
| REQ-N01 | 시스템 반응 속도 | QM | SIL 타이밍 | TC-N01 | ⬜ Pending |
| REQ-N02 | 장시간 동작 안정성 | QM | HIL 100h | TC-N02 | ⬜ Pending |
| REQ-N03 | MPU 메모리 파티션 보호 | ASIL-D | Fault Injection | TC-N03 | ⬜ Pending |
| REQ-N04 | 태스크 실행 시간 모니터링 | ASIL-D | HIL 런타임 | TC-N04 | ⬜ Pending |
| REQ-N05 | 시스템 자가 진단 (POST) | ASIL-B | Fault Injection | TC-N05 | ⬜ Pending |

---

## 4. E2E Master Scenario 추적성

| 시나리오 단계 | 관련 REQ | 관련 FSR | 테스트 케이스 |
|------------|---------|---------|------------|
| Phase 1: Fault Injection (BCM DTC) | REQ-F01, REQ-F02, REQ-F03, REQ-F04 | FSR-B03 | TC-F01~04, INT-006 Ph.1 |
| Phase 2: Gateway Routing | REQ-G01, REQ-G02, REQ-G03 | FSR-QM01 | TC-G01~03, INT-006 Ph.2 |
| Phase 3: UDS Diagnostics | REQ-D01, REQ-D02, REQ-D07, REQ-D08 | FSR-B04 | TC-D01~08, INT-006 Ph.3 |
| Phase 4: OTA Programming | REQ-O01~O06 | FSR-QM02 | TC-O01~06, INT-006 Ph.4 |
| E2E Regression | 전체 40개 | — | INT-006 전체, SV-E2E-001 |

---

## 5. Coverage Statistics

| 항목 | 수량 |
|-----|------|
| Safety Goals | 7개 (SG-01, 02, 03, 06, 07, 08, 09) |
| System Requirements | 40개 (REQ-F/G/D/O/A/N) |
| Test Cases | 40개 (TC-F/G/D/O/A/N 01~11) |
| Traceability | 40/40 (100%) |
| E2E Scenario Coverage | Phase 1~4 + Regression |

---

## 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-14 | 초기 생성 (REQ-A01~020) |
| 2.0 | 2026-02-17 | REQ-A03~059 추가 |
| **3.0** | **2026-02-17** | **완전 재편성 — 6-Group 구조 (REQ-F/G/D/O/A/N)** |

---

**Document Version**: 3.0 | **Last Updated**: 2026-02-17

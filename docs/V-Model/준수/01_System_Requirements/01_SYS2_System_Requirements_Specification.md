# System Requirements Specification (시스템 요구사항 명세서)

**Document ID**: PART4-01-SRS
**ISO 26262 Reference**: Part 4, Clause 6
**ASPICE Reference**: SYS.2 (BP1-BP9)
**Version**: 3.0
**Date**: 2026-02-17
**Status**: Released (v3.0 — 6-Group 구조 완전 재편성)

---

## 🔴 핵심 검증 시나리오 — Master E2E Scenario (Red Thread)

> 본 프로젝트의 모든 요구사항은 아래 **4단계 시나리오**에서 도출됩니다.
> ASPICE SYS.2는 시나리오 기반 요구사항 도출을 명시합니다 (BP2: Define system requirements).

```
[Phase 1] Fault Detection    →  Group 1: REQ-F01 ~ REQ-F05
[Phase 2] Gateway Routing    →  Group 2: REQ-G01 ~ REQ-G05
[Phase 3] UDS Diagnostics    →  Group 3: REQ-D01 ~ REQ-D08
[Phase 4] OTA Update         →  Group 4: REQ-O01 ~ REQ-O06
[지속]    ADAS Safety         →  Group 5: REQ-A01 ~ REQ-A11
[지속]    Non-Functional      →  Group 6: REQ-N01 ~ REQ-N05
```

**적용 표준**: ISO 14229-1 UDS | ISO 13400-2 DoIP | ISO 26262-4 | ASPICE PAM 3.1

---

## 1. 요구사항 개요

**총 요구사항**: 40개 (v3.0 재편성)

| Group | ID 범위 | Count | 핵심 기능 | ASIL |
|-------|---------|-------|---------|------|
| **Group 1**: Fault Detection | REQ-F01~F05 | 5 | BCM DTC 감지, Cluster 경고 | ASIL-B/D |
| **Group 2**: Gateway Routing | REQ-G01~G05 | 5 | CAN 라우팅, DoIP 경로 | QM/ASIL-B |
| **Group 3**: UDS Diagnostics | REQ-D01~D08 | 8 | UDS 세션, DTC Read | ASIL-B |
| **Group 4**: OTA Programming | REQ-O01~O06 | 6 | 펌웨어 다운/전송/검증 | ASIL-A/QM |
| **Group 5**: ADAS Safety | REQ-A01~A11 | 11 | AEB/LDW/BSD 경고 | ASIL-D/B |
| **Group 6**: Non-Functional | REQ-N01~N05 | 5 | 성능, 안전 메커니즘 | ASIL-D/B |
| **합계** | | **40** | | |

---

## 2. Group 1: Fault Detection (고장 감지)

> **시나리오 Phase 1**: BCM에서 고장(DTC B1234)을 감지하고 CAN-LS로 전파

---

### REQ-F01: BCM CAN 메시지 수신

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-B (SG-06: Fail-Safe — S2/E3/C2)
- **Description**: 시스템은 BCM이 전송하는 `BCM_FaultStatus` CAN 메시지 (CAN-LS, ID: 0x500, 주기: 10ms)를 누락 없이 수신하고 파싱해야 한다. 수신 타임아웃은 30ms로 설정하며, 타임아웃 발생 시 DTC를 생성해야 한다.
- **Rationale**: BCM 고장 감지가 전체 시나리오의 시작점이므로 신뢰성 있는 수신이 필수
- **Acceptance Criteria**:
  - CAN 메시지 수신율 ≥ 99.9% (1000회 중 최소 999회)
  - 타임아웃 감지 시간 ≤ 30ms ± 2ms
- **Verification Method**: CANoe SIL (CAPL 자동화 테스트)
- **Trace**: SG-06 → FSR-B03 → REQ-F01 → TC-F01

---

### REQ-F02: DTC B1234 감지 및 저장

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-B (SG-06: Fail-Safe)
- **Description**: 시스템은 `BCM_FaultStatus.WindowMotorOvercurrent = 1` (50A 초과) 조건을 감지하면 ISO 14229 DTC 포맷으로 DTC B1234를 내부 메모리에 저장해야 한다. DTC 저장은 이벤트 발생 후 10ms 이내에 완료되어야 한다.
- **Acceptance Criteria**:
  - DTC B1234 저장 성공률: 100%
  - 저장 지연: ≤ 10ms
  - ISO 14229 DTC Status Byte 준수
- **Verification Method**: Fault Injection Test (CANoe CAPL)
- **Trace**: SG-06 → FSR-B03 → REQ-F02 → TC-F02

---

### REQ-F03: Cluster 경고등 활성화 (FTTI)

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D (SG-01: AEB, SG-02: LDW — S3/E4/C3)
- **Description**: BCM DTC 발생 이후 Cluster 경고등(Dashboard Warning Indicator)은 **FTTI(Fault Tolerant Time Interval) 50ms 이내**에 활성화되어야 한다. 경고등 색상은 RED이며, DTC가 클리어될 때까지 지속 표시한다.
- **Rationale**: ISO 26262 ASIL-D 요구사항 — FTTI 초과 시 운전자가 위험을 인지하지 못할 수 있음
- **Acceptance Criteria**:
  - FTTI (T_fault → T_cluster_on) ≤ 50ms (1000회 측정, 100% 준수)
  - 경고등 색상: RED (RGB 255,0,0 ± 허용오차)
  - 경고 유지: DTC Clear 전까지 상시 표시
- **Verification Method**: Logic Analyzer + CANoe Timestamp
- **Trace**: SG-01 → FSR-D01 → REQ-F03 → TC-F03

---

### REQ-F04: CANoe Fault Injection 지원

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: 검증 환경에서 CANoe CAPL을 통해 `BCM_FaultStatus` 신호를 소프트웨어적으로 주입(Fault Injection)할 수 있어야 한다. 주입 파라미터: 전류값(A), 지속시간(ms), 반복횟수(회).
- **Acceptance Criteria**:
  - CAPL 스크립트로 10회 연속 Fault Injection 가능
  - 각 Injection 후 DTC B1234 생성 확인
- **Verification Method**: CANoe SIL (자동화)
- **Trace**: REQ-F04 → TC-F04

---

### REQ-F05: Watchdog 타이머 (SW Fault Detection)

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-B (SG-06)
- **Description**: vECU 소프트웨어는 Watchdog 타이머(WDT)를 구현해야 한다. WDT 타임아웃은 50ms이며, 소프트웨어가 주기적으로 WDT를 리셋(Kick)하지 않으면 시스템은 Fail-Safe 상태로 전환한다.
- **Acceptance Criteria**:
  - WDT 타임아웃 설정: 50ms
  - Kick 주기: ≤ 30ms (정상 동작 시)
  - Fail-Safe 전환 시간: 50ms ± 5ms
- **Verification Method**: Fault Injection Test (WDT Kick 중단)
- **Trace**: SG-06 → FSR-B03 → REQ-F05 → TC-F05

---

## 3. Group 2: Gateway Routing (게이트웨이 라우팅)

> **시나리오 Phase 2**: Central Gateway가 CAN 도메인 간 DTC를 라우팅하고 OTA Server에 DoIP 경로를 제공

---

### REQ-G01: CAN-LS → CAN-HS2 DTC 라우팅

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: QM (SG-09: Gateway 가용성)
- **Description**: Central Gateway는 CAN-LS(125kbps)에서 수신한 `BCM_FaultStatus` 메시지(0x500)를 CAN-HS2(500kbps)로 라우팅해야 한다. 라우팅 테이블은 정적으로 설정되며, 메시지 손실 없이 전달해야 한다.
- **Acceptance Criteria**:
  - 메시지 라우팅 성공률: 100% (손실 0)
  - 라우팅 지연: ≤ 5ms (REQ-G02 연계)
- **Verification Method**: CANoe 추적 (CAN-LS Trace → CAN-HS2 Trace 타임스탬프 비교)
- **Trace**: SG-09 → FSR-QM01 → REQ-G01 → TC-G01

---

### REQ-G02: Gateway 라우팅 지연 ≤ 5ms

- **Category**: 성능 요구사항 (Performance)
- **Priority**: High (P1)
- **ASIL**: QM
- **Description**: Central Gateway의 CAN-LS → CAN-HS2 메시지 변환 및 전달 지연은 **최대 5ms 이내**여야 한다. 90% Bus Load 고부하 상황에서도 이 기준을 유지해야 한다.
- **Acceptance Criteria**:
  - 정상 부하: ≤ 3ms (평균)
  - 고부하 (90% Bus Load): ≤ 5ms
  - 측정 횟수: 1000회
- **Verification Method**: CANoe Bus Load Test
- **Trace**: TSR-B04 → REQ-G02 → TC-G02

---

### REQ-G03: Ethernet/DoIP OTA 경로 제공

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: QM
- **Description**: Central Gateway는 OTA Server와 BCM 사이의 DoIP(Diagnostic over IP, ISO 13400-2) 통신 경로를 제공해야 한다. DoIP Routing Activation(0xE001)을 처리하고, UDS 메시지를 CAN-LS로 포워딩해야 한다.
- **Acceptance Criteria**:
  - DoIP Routing Activation 처리 시간: ≤ 100ms
  - UDS 메시지 포워딩 성공률: 100%
  - Ethernet Link Loss 시 DTC 생성 (REQ-G04 연계)
- **Verification Method**: CANoe DoIP 시뮬레이션
- **Trace**: SG-09 → FSR-QM01 → REQ-G03 → TC-G03

---

### REQ-G04: Bus Off 시 Graceful Abort

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: CAN Bus Off 상태 감지 시 Gateway는 진행 중인 UDS/OTA 세션을 안전하게 중단(Graceful Abort)하고, DTC를 저장하며, Fail-Safe 상태로 전환해야 한다.
- **Acceptance Criteria**:
  - Bus Off 감지 시간: ≤ 30ms
  - DTC 생성: 100%
  - OTA 중 Bus Off → Rollback 성공 (REQ-O06 연계)
- **Verification Method**: CANoe CAN Error Frame 주입
- **Trace**: SG-06 → FSR-B03 → REQ-G04 → TC-G04

---

### REQ-G05: 다중 CAN 도메인 메시지 관리

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2)
- **ASIL**: QM
- **Description**: Central Gateway는 CAN-LS, CAN-HS1, CAN-HS2 3개 도메인의 메시지를 동시에 처리해야 한다. 우선순위: 안전 관련 메시지 (AEB/LDW) > DTC 메시지 > 일반 메시지.
- **Acceptance Criteria**:
  - 3개 도메인 동시 처리 가능
  - 안전 메시지 우선 처리 보장
- **Verification Method**: CANoe Multi-Bus SIL
- **Trace**: REQ-G05 → TC-G05

---

## 4. Group 3: UDS Diagnostics (진단 통신)

> **시나리오 Phase 3**: CANoe Tester가 UDS 프로토콜로 BCM의 DTC를 수집하고 OTA Server로 전달

---

### REQ-D01: UDS 0x10 Session Control

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-B (SG-08: OTA 무결성 — S2/E2/C2)
- **Description**: 시스템은 UDS 서비스 0x10 (Session Control)을 지원해야 한다. 세션 유형: Default(0x01), Extended Diagnostic(0x03), Programming(0x02). 잘못된 세션 전환 요청 시 Negative Response (0x7F 0x10 0x22)를 반환해야 한다.
- **Acceptance Criteria**:
  - Default → Extended 전환: PositiveResponse 0x50 0x03
  - Extended → Programming 전환: PositiveResponse 0x50 0x02
  - 잘못된 전환: NegativeResponse 0x7F 0x10 0x22
  - 세션 타임아웃(S3) 후 자동 Default 복귀: 5000ms
- **Verification Method**: CANoe CAPL 자동화 (TC-D01)
- **Trace**: SG-08 → FSR-B04 → REQ-D01 → TC-D01

---

### REQ-D02: UDS 0x19 Read DTC Information

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-B
- **Description**: 시스템은 UDS 서비스 0x19 (Read DTC Information)을 지원해야 한다. 서브 함수: 0x02 (reportDTCByStatusMask). DTC B1234의 상태 바이트, 스냅샷 데이터를 포함하여 응답해야 한다.
- **Acceptance Criteria**:
  - 0x19 0x02 요청 → DTC B1234 포함 응답
  - DTC Status Byte 정확도: 100%
  - 응답 시간 ≤ P2 timeout (50ms)
- **Verification Method**: CANoe CAPL 자동화 (TC-D02)
- **Trace**: SG-08 → REQ-D02 → TC-D02

---

### REQ-D03: UDS 0x14 Clear DTC

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: 시스템은 UDS 서비스 0x14 (Clear Diagnostic Information)를 지원해야 한다. DTC 그룹 전체 클리어(0xFFFFFF) 및 특정 DTC 클리어를 지원해야 한다. DTC 클리어 후 Cluster 경고등이 소등되어야 한다.
- **Acceptance Criteria**:
  - 0x14 0xFF 0xFF 0xFF → 전체 DTC 클리어, PositiveResponse
  - DTC 클리어 후 Cluster 경고등 소등 시간: ≤ 1s
- **Verification Method**: CANoe SIL (TC-D03)
- **Trace**: REQ-D03 → TC-D03

---

### REQ-D04: UDS 0x22 Read Data by Identifier

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Medium (P2)
- **ASIL**: QM
- **Description**: 시스템은 UDS 서비스 0x22 (Read Data by Identifier)를 지원해야 한다. 지원 DID: 0xF100 (SW 버전), 0xF101 (HW 버전), 0xF186 (Active Diagnostic Session).
- **Acceptance Criteria**:
  - 0x22 0xF100 → SW 버전 문자열 응답
  - 지원하지 않는 DID → NegativeResponse 0x7F 0x22 0x31
- **Verification Method**: CANoe SIL (TC-D04)
- **Trace**: REQ-D04 → TC-D04

---

### REQ-D05: UDS P2/P2* 타이밍 준수

- **Category**: 성능 요구사항 (Performance)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: UDS 응답 타이밍은 ISO 14229-1 규격을 준수해야 한다. P2 Server Max: 50ms (Enhanced), P2* Server Max: 5000ms (Extended). P2 초과 시 Pending Response (0x78) 전송.
- **Acceptance Criteria**:
  - P2 타임아웃 내 응답 또는 Pending Response
  - Pending Response 사용 시 P2* 이내 최종 응답
- **Verification Method**: CANoe Timing Analyzer (TC-D05)
- **Trace**: REQ-D05 → TC-D05

---

### REQ-D06: UDS Negative Response 처리

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: 시스템은 지원하지 않거나 조건이 맞지 않는 UDS 요청에 대해 적절한 Negative Response Code(NRC)를 반환해야 한다. 주요 NRC: 0x11 (서비스 미지원), 0x22 (조건 불충족), 0x31 (DID 미지원), 0x35 (Security 미인가).
- **Acceptance Criteria**:
  - 모든 오류 조건에서 NRC 정확히 반환
  - NRC 응답 시간 ≤ P2 timeout
- **Verification Method**: CANoe SIL 경계값 테스트 (TC-D06)
- **Trace**: REQ-D06 → TC-D06

---

### REQ-D07: 진단 세션 보안 관리

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: Programming Session(0x02) 진입을 위해서는 Security Access (UDS 0x27) 인증을 완료해야 한다. Seed-Key 알고리즘을 사용하며, 3회 연속 인증 실패 시 10분간 잠금.
- **Acceptance Criteria**:
  - 인증 없이 Programming Session 진입 불가 (NRC 0x33)
  - Seed-Key 알고리즘 정확도: 100%
  - 3회 실패 후 잠금: 600s
- **Verification Method**: CANoe SIL 보안 테스트 (TC-D07)
- **Trace**: SG-08 → FSR-B04 → REQ-D07 → TC-D07

---

### REQ-D08: DTC 데이터 OTA Server 전달

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: QM
- **Description**: CANoe Tester는 UDS 0x19로 수집한 DTC B1234 데이터를 TCP/IP 소켓을 통해 가상 OTA 서버에 전달해야 한다. 전달 포맷: JSON {"dtc": "B1234", "status": 0x08, "timestamp": epoch}.
- **Acceptance Criteria**:
  - DTC 데이터 전달 성공률: 100%
  - 전달 지연: ≤ 100ms
  - JSON 포맷 정확도: 스키마 검증 통과
- **Verification Method**: CANoe CAPL + TCP Socket 로그 분석 (TC-D08)
- **Trace**: REQ-D08 → TC-D08 → INT-006 Phase 3

---

## 5. Group 4: OTA Programming (OTA 소프트웨어 갱신)

> **시나리오 Phase 4**: OTA Server가 UDS 프로그래밍 세션으로 BCM 펌웨어를 갱신

---

### REQ-O01: UDS 0x10 0x02 Programming Session

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-A (SG-08: OTA Rollback — S2/E2/C2 = ASIL-A)
- **Description**: OTA Server는 BCM에 UDS 0x10 0x02 (Programming Session) 전환을 요청할 수 있어야 한다. Programming Session 진입 전 Security Access(0x27)가 완료되어야 한다. 세션 진입 후 타임아웃(P3): 5000ms.
- **Acceptance Criteria**:
  - Security Access 완료 후 Programming Session 진입 성공: 100%
  - PositiveResponse 0x50 0x02 수신
  - P3 타임아웃 내 0x34 수신 안 되면 Default Session 복귀
- **Verification Method**: CANoe SIL + HIL (TC-O01)
- **Trace**: SG-08 → FSR-QM02 → REQ-O01 → TC-O01

---

### REQ-O02: UDS 0x34 Request Download

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-A
- **Description**: OTA Server는 UDS 0x34 (Request Download)로 펌웨어 다운로드를 요청할 수 있어야 한다. 요청 파라미터: Memory Address, Memory Size (64KB max), Data Format Identifier (압축 없음: 0x00).
- **Acceptance Criteria**:
  - 유효한 0x34 요청에 PositiveResponse 0x74 (maxBlockLength 포함)
  - 64KB 초과 요청 → NegativeResponse 0x31
  - Programming Session 외 요청 → NegativeResponse 0x22
- **Verification Method**: CANoe SIL (TC-O02)
- **Trace**: SG-08 → FSR-QM02 → REQ-O02 → TC-O02

---

### REQ-O03: UDS 0x36 Transfer Data

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-A
- **Description**: OTA Server는 UDS 0x36 (Transfer Data)으로 펌웨어 데이터를 4KB 단위 블록으로 전송할 수 있어야 한다. Block Sequence Counter는 1씩 증가하며, 순서 오류 시 NegativeResponse(0x73)를 반환해야 한다.
- **Acceptance Criteria**:
  - 블록 크기: 최대 4096 bytes
  - 순서 오류 → NegativeResponse 0x73
  - 전체 전송 성공률: 100%
- **Verification Method**: CANoe SIL (TC-O03)
- **Trace**: SG-08 → FSR-QM02 → REQ-O03 → TC-O03

---

### REQ-O04: UDS 0x37 Transfer Exit

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-A
- **Description**: 모든 데이터 전송 완료 후 OTA Server는 UDS 0x37 (Transfer Exit)을 전송해야 한다. 시스템은 전체 데이터 CRC 검증 후 PositiveResponse를 반환하고 BCM을 재시작해야 한다.
- **Acceptance Criteria**:
  - CRC 검증 통과 → PositiveResponse 0x77, BCM 재시작
  - CRC 불일치 → NegativeResponse 0x70, 자동 Rollback
  - BCM 재시작 후 DTC B1234 자동 소거
- **Verification Method**: CANoe SIL + HIL (TC-O04)
- **Trace**: SG-08 → FSR-QM02 → REQ-O04 → TC-O04

---

### REQ-O05: OTA Checksum 검증 (CRC-32)

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-A
- **Description**: 펌웨어 전송 완료 후 CRC-32 체크섬을 검증해야 한다. 예상 CRC(OTA Server 제공)와 수신 데이터 CRC가 불일치하면 설치를 거부하고 이전 버전을 유지해야 한다.
- **Acceptance Criteria**:
  - CRC 불일치 감지율: 100% (1000회 테스트)
  - 불일치 시 설치 거부 및 이전 버전 유지: 100%
  - 악성 패키지(변조 CRC) 거부: 100%
- **Verification Method**: Fault Injection Test (TC-O05)
- **Trace**: SG-08 → FSR-QM02 → REQ-O05 → TC-O05

---

### REQ-O06: OTA 실패 시 자동 Rollback

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-A
- **Description**: OTA 업데이트 중 전원 차단, 통신 단절, CRC 오류 등의 실패 발생 시 시스템은 자동으로 이전 펌웨어 버전으로 복구(Rollback)해야 한다. Rollback 완료 후 DTC를 생성하고 Cluster에 경고를 표시해야 한다.
- **Acceptance Criteria**:
  - Rollback 성공률: 10/10회 (100%)
  - Rollback 완료 시간: ≤ 30s
  - Rollback 후 DTC 생성: 100%
- **Verification Method**: HIL Fault Injection (배터리 차단 시뮬레이터) (TC-O06)
- **Trace**: SG-08 → FSR-QM02 → REQ-O06 → TC-O06

---

## 6. Group 5: ADAS Safety (ADAS 안전 기능)

> **지속 기능**: 실차 구현을 전제로 AEB/LDW/BSD 경고 UI를 ISO 26262 ASIL-D 수준으로 구현

---

### REQ-A01: LDW 차선 이탈 경고 표시

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D (SG-02: LDW — S3/E4/C3)
- **Description**: 차선 이탈 감지 시 Cluster에 시각 경고와 MDPS를 통한 촉각 경고(스티어링 진동)를 동시에 표시해야 한다. 이중 채널(시각+촉각) 독립 구현으로 ASIL Decomposition (D = B+B).
- **Acceptance Criteria**:
  - FTTI ≤ 200ms
  - 이중 채널 독립성 검증
  - 한 채널 고장 시 다른 채널 정상 동작
- **Verification Method**: HIL (ASIL Decomposition 검증) + VIL
- **Trace**: SG-02 → FSR-D02 → REQ-A01 → TC-A01

---

### REQ-A02: AEB 긴급 제동 경고 표시

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D (SG-01: AEB — S3/E4/C3)
- **Description**: AEB 시스템에서 긴급 제동 신호 수신 시 Cluster에 RED 경고 UI를 100ms 이내에 표시해야 한다. 경고는 AEB 이벤트가 해제될 때까지 지속.
- **Acceptance Criteria**:
  - FTTI ≤ 100ms (1000회 측정, 100% 준수)
  - 오경보율(False Alarm): 0%
  - AEB 이벤트 감지율: 100%
- **Verification Method**: HIL + Logic Analyzer (TC-A02)
- **Trace**: SG-01 → FSR-D01 → REQ-A02 → TC-A02

---

### REQ-A03: BSD 사각지대 경고 표시

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-B (SG-03: BSD — S2/E4/C2)
- **Description**: 사각지대에 차량 감지 시 Cluster 사이드 미러 경고 아이콘을 활성화해야 한다. 방향 지시등 조작 시 경고 강도 증가 (점등 → 점멸).
- **Acceptance Criteria**:
  - 경고 활성화 시간 ≤ 300ms
  - 방향지시등 조작 시 경고 강도 변경
- **Verification Method**: HIL (TC-A03)
- **Trace**: SG-03 → FSR-B02 → REQ-A03 → TC-A03

---

### REQ-A04: 후방 카메라 영상 표시

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: 후진 기어 진입 시 IVI 화면에 후방 카메라 영상을 1s 이내에 표시해야 한다. 영상 해상도: 1280×720 이상, 프레임레이트: 30fps 이상.
- **Acceptance Criteria**:
  - R 기어 진입 후 영상 표시까지 ≤ 1s
  - 해상도 및 프레임레이트 준수
- **Verification Method**: VIL (Integration Test) (TC-A04)
- **Trace**: REQ-A04 → TC-A04

---

### REQ-A05: Cluster 경고 아이콘 제어

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D
- **Description**: AEB/LDW/BSD 이벤트에 따라 Cluster 내 해당 경고 아이콘을 정확하게 활성화/비활성화해야 한다. 아이콘 색상 코드: AEB=RED, LDW=YELLOW, BSD=YELLOW.
- **Acceptance Criteria**:
  - 이벤트 → 아이콘 활성화 오류율: 0%
  - 아이콘 색상 정확도: 100%
- **Verification Method**: SIL + VIL (TC-A05)
- **Trace**: SG-01 → SG-02 → FSR-D01 → REQ-A05 → TC-A05

---

### REQ-A06: Camera LDW 데이터 수신

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D
- **Description**: 전방 카메라 LDW 이벤트 데이터를 CAN-HS2를 통해 수신해야 한다. 메시지 주기: 10ms, 타임아웃: 30ms. 수신 누락 시 Fail-Safe.
- **Acceptance Criteria**:
  - 메시지 수신율: ≥ 99.9%
  - 타임아웃 감지: ≤ 30ms
- **Verification Method**: CANoe SIL (TC-A06)
- **Trace**: SG-02 → FSR-D02 → REQ-A06 → TC-A06

---

### REQ-A07: LDW 이벤트 파싱

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D
- **Description**: 수신된 LDW CAN 메시지의 신호를 파싱하여 이탈 방향(좌/우), 이탈 강도(경/중/강)를 정확하게 추출해야 한다. 파싱 오류율: 0%.
- **Acceptance Criteria**:
  - 파싱 정확도: 100% (1000회 테스트)
  - 잘못된 메시지 포맷 → 거부 및 DTC 생성
- **Verification Method**: Unit Test (TC-A07)
- **Trace**: SG-02 → REQ-A07 → TC-A07

---

### REQ-A08: AEB 이벤트 검증 (CRC + Counter)

- **Category**: 안전 요구사항 (Safety)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D
- **Description**: AEB CAN 메시지의 CRC-8 및 Alive Counter를 검증해야 한다. CRC 불일치 또는 Counter 불연속 시 해당 메시지를 무효화하고 DTC를 생성해야 한다.
- **Acceptance Criteria**:
  - CRC 오류 감지율: 100%
  - Counter 불연속 감지율: 100%
  - 무효 메시지 → DTC 생성: 100%
- **Verification Method**: Unit Test + Fault Injection (TC-A08)
- **Trace**: SG-01 → FSR-D01 → REQ-A08 → TC-A08

---

### REQ-A09: AEB 이벤트 우선순위 처리

- **Category**: 기능 요구사항 (Functional)
- **Priority**: Critical (P0)
- **ASIL**: ASIL-D
- **Description**: AEB 이벤트는 모든 다른 경고보다 최우선 처리(Priority 0)되어야 한다. AEB 활성화 중 다른 경고(LDW, BSD) 수신 시 AEB 경고를 유지하고 나머지는 큐에 대기.
- **Acceptance Criteria**:
  - AEB 경고 최우선 처리 검증 (모든 조합)
  - 우선순위 역전(Priority Inversion) 없음
- **Verification Method**: Unit Test (우선순위 테이블 전수 검사) (TC-A09)
- **Trace**: SG-01 → REQ-A09 → TC-A09

---

### REQ-A10: 경고 지속 시간 제어

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: 경고 이벤트 해제 후 경고 표시의 최소 지속 시간을 보장해야 한다. AEB: 이벤트 해제 후 3s 유지, LDW: 2s 유지, BSD: 1s 유지.
- **Acceptance Criteria**:
  - 각 경고 유형별 최소 지속 시간 준수 (오차 ±100ms)
- **Verification Method**: SIL (TC-A10)
- **Trace**: REQ-A10 → TC-A10

---

### REQ-A11: 다중 경고 우선순위 처리

- **Category**: 기능 요구사항 (Functional)
- **Priority**: High (P1)
- **ASIL**: QM (다중 경고 처리 로직)
- **Description**: 여러 경고가 동시에 발생할 때 우선순위 테이블에 따라 처리해야 한다. 우선순위: AEB (P0) > LDW (P1) > BSD (P2) > DTC Warning (P3).
- **Acceptance Criteria**:
  - 우선순위 테이블 모든 조합 검증 (4! = 24 케이스)
  - 상위 우선순위 경고 항상 우선 표시
- **Verification Method**: SIL (TC-A11)
- **Trace**: SG-07 → REQ-A11 → TC-A11

---

## 7. Group 6: Non-Functional Requirements (비기능 요구사항)

> **지속 기준**: 시스템 전체에 적용되는 성능·안전·신뢰성 기준

---

### REQ-N01: 시스템 반응 속도

- **Category**: 성능 요구사항 (Performance)
- **Priority**: High (P1)
- **ASIL**: QM (성능 기준)
- **Description**: ASIL-D 안전 기능의 이벤트-경고 응답 지연은 100ms 이내여야 한다. ASIL-B 기능은 500ms, QM 기능은 1000ms.
- **Acceptance Criteria**:
  - ASIL-D 이벤트 → 경고: ≤ 100ms
  - ASIL-B 이벤트 → 경고: ≤ 500ms
  - QM 기능: ≤ 1000ms
- **Verification Method**: SIL 타이밍 측정 (TC-N01)
- **Trace**: REQ-N01 → TC-N01

---

### REQ-N02: 장시간 동작 안정성

- **Category**: 신뢰성 요구사항 (Reliability)
- **Priority**: High (P1)
- **ASIL**: QM
- **Description**: 시스템은 100시간 연속 동작 중 크래시, 메모리 누수, 성능 저하 없이 안정적으로 동작해야 한다.
- **Acceptance Criteria**:
  - 100시간 동작 중 크래시 0회
  - 메모리 사용량 증가: ≤ 1% per 10 hours
  - 응답 속도 저하: ≤ 5%
- **Verification Method**: HIL 장시간 테스트 (TC-N02)
- **Trace**: REQ-N02 → TC-N02

---

### REQ-N03: 메모리 파티션 보호 (MPU)

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-D (ISO 26262 ASIL-D 소프트웨어 요구사항)
- **Description**: vECU 소프트웨어는 Memory Protection Unit (MPU)을 사용하여 ASIL-D 파티션과 QM 파티션을 분리해야 한다. 파티션 침범 시 즉시 Fail-Safe 전환.
- **Acceptance Criteria**:
  - MPU 파티션 경계 침범 → Fail-Safe 전환 100%
  - ASIL 파티션과 QM 파티션 간 데이터 간섭 없음
- **Verification Method**: Fault Injection Test (TC-N03)
- **Trace**: SG-06 → FSR-D03 → REQ-N03 → TC-N03

---

### REQ-N04: 태스크 실행 시간 모니터링

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-D
- **Description**: 각 RTOS 태스크의 WCET(Worst Case Execution Time)를 런타임에 모니터링해야 한다. WCET 초과 시 해당 태스크를 강제 종료하고 Fail-Safe 상태로 전환.
- **Acceptance Criteria**:
  - WCET 초과 감지율: 100%
  - Fail-Safe 전환 시간: ≤ 10ms
- **Verification Method**: HIL 런타임 모니터링 (TC-N04)
- **Trace**: SG-06 → FSR-D03 → REQ-N04 → TC-N04

---

### REQ-N05: 시스템 자가 진단 (Self-Test)

- **Category**: 안전 요구사항 (Safety)
- **Priority**: High (P1)
- **ASIL**: ASIL-B
- **Description**: 시스템 시동 시 자가 진단(Power-On Self-Test, POST)을 수행해야 한다. 점검 항목: RAM 무결성, Flash CRC, 통신 인터페이스 상태. POST 실패 시 시스템 시작을 거부하고 DTC를 생성해야 한다.
- **Acceptance Criteria**:
  - POST 완료 시간: ≤ 500ms
  - RAM 오류 감지율: 100%
  - Flash CRC 오류 감지율: 100%
- **Verification Method**: Fault Injection Test (TC-N05)
- **Trace**: SG-06 → FSR-B03 → REQ-N05 → TC-N05

---

## 8. 요구사항 추적성 요약

| Group | REQ ID | Safety Goal | ASIL | FSR |
|-------|--------|-------------|------|-----|
| G1 Fault Detection | REQ-F01 | SG-06 | ASIL-B | FSR-B03 |
| G1 Fault Detection | REQ-F02 | SG-06 | ASIL-B | FSR-B03 |
| G1 Fault Detection | REQ-F03 | SG-01/02 | ASIL-D | FSR-D01 |
| G1 Fault Detection | REQ-F04 | — | ASIL-B | — |
| G1 Fault Detection | REQ-F05 | SG-06 | ASIL-B | FSR-B03 |
| G2 Gateway | REQ-G01 | SG-09 | QM | FSR-QM01 |
| G2 Gateway | REQ-G02 | — | QM | TSR-B04 |
| G2 Gateway | REQ-G03 | SG-09 | QM | FSR-QM01 |
| G2 Gateway | REQ-G04 | SG-06 | ASIL-B | FSR-B03 |
| G2 Gateway | REQ-G05 | — | QM | — |
| G3 UDS Diagnostics | REQ-D01 | SG-08 | ASIL-B | FSR-B04 |
| G3 UDS Diagnostics | REQ-D02 | SG-08 | ASIL-B | FSR-B04 |
| G3 UDS Diagnostics | REQ-D03 | — | ASIL-B | — |
| G3 UDS Diagnostics | REQ-D04 | — | QM | — |
| G3 UDS Diagnostics | REQ-D05 | — | ASIL-B | — |
| G3 UDS Diagnostics | REQ-D06 | — | ASIL-B | — |
| G3 UDS Diagnostics | REQ-D07 | SG-08 | ASIL-B | FSR-B04 |
| G3 UDS Diagnostics | REQ-D08 | — | QM | — |
| G4 OTA | REQ-O01 | SG-08 | ASIL-A | FSR-QM02 |
| G4 OTA | REQ-O02 | SG-08 | ASIL-A | FSR-QM02 |
| G4 OTA | REQ-O03 | SG-08 | ASIL-A | FSR-QM02 |
| G4 OTA | REQ-O04 | SG-08 | ASIL-A | FSR-QM02 |
| G4 OTA | REQ-O05 | SG-08 | ASIL-A | FSR-QM02 |
| G4 OTA | REQ-O06 | SG-08 | ASIL-A | FSR-QM02 |
| G5 ADAS | REQ-A01 | SG-02 | ASIL-D | FSR-D02 |
| G5 ADAS | REQ-A02 | SG-01 | ASIL-D | FSR-D01 |
| G5 ADAS | REQ-A03 | SG-03 | ASIL-B | FSR-B02 |
| G5 ADAS | REQ-A04 | — | ASIL-B | — |
| G5 ADAS | REQ-A05 | SG-01/02 | ASIL-D | FSR-D01 |
| G5 ADAS | REQ-A06 | SG-02 | ASIL-D | FSR-D02 |
| G5 ADAS | REQ-A07 | SG-02 | ASIL-D | FSR-D02 |
| G5 ADAS | REQ-A08 | SG-01 | ASIL-D | FSR-D01 |
| G5 ADAS | REQ-A09 | SG-01 | ASIL-D | FSR-D01 |
| G5 ADAS | REQ-A10 | — | ASIL-B | — |
| G5 ADAS | REQ-A11 | SG-07 | QM | — |
| G6 Non-Func | REQ-N01 | — | QM | — |
| G6 Non-Func | REQ-N02 | — | QM | — |
| G6 Non-Func | REQ-N03 | SG-06 | ASIL-D | FSR-D03 |
| G6 Non-Func | REQ-N04 | SG-06 | ASIL-D | FSR-D03 |
| G6 Non-Func | REQ-N05 | SG-06 | ASIL-B | FSR-B03 |

---

## 9. ASPICE SYS.2 준수 현황

| Base Practice | 준수 사항 | 상태 |
|--------------|---------|------|
| BP1: 고객 요구사항 정의 | 시나리오 기반 요구사항 도출 | ✅ |
| BP2: 시스템 요구사항 정의 | 40개 REQ (6-Group 구조) | ✅ |
| BP3: 인터페이스 요구사항 정의 | CAN/DoIP/UDS 인터페이스 명시 | ✅ |
| BP4: 안전 요구사항 | ASIL-D/B/A/QM 분류 완료 | ✅ |
| BP5: 검증 기준 정의 | 모든 REQ에 Acceptance Criteria | ✅ |
| BP6: 일관성 검증 | 상위-하위 추적성 확인 | ✅ |
| BP7: 변경 영향 분석 | 기준선 관리 (Git) | ✅ |
| BP8: 재사용 메커니즘 | 공통 ASIL 분류 체계 | ✅ |
| BP9: 양방향 추적성 | Traceability Matrix (SUP.10) | ✅ |

---

## 10. 개정 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|---------|
| 1.0 | 2026-02-14 | 초기 생성 (REQ-001~055) |
| 2.0 | 2026-02-17 | REQ-056~059 추가 (비파괴 추가) |
| **3.0** | **2026-02-17** | **완전 재편성 — 6-Group 구조 (REQ-F/G/D/O/A/N)** |

---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **Safety Manager** | Sarah Lee | ✅ Approved | 2026-02-17 |
| **Chief Engineer** | Mike Park | ✅ Approved | 2026-02-17 |
| **Project Manager** | John Kim | ✅ Approved | 2026-02-17 |

---

**Document Version**: 3.0 | **Last Updated**: 2026-02-17

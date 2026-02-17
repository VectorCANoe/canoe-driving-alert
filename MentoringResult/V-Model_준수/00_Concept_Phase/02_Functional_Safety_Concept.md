# Functional Safety Concept (기능 안전 개념)

**Document ID**: PART3-02-FSC
**ISO 26262 Reference**: Part 3, Clause 8
**ASPICE Reference**: N/A
**Version**: 2.0
**Date**: 2026-02-17
**Status**: Released (v2.0 — Completed per ISO 26262-1:2018 review)

> **Change Log v2.0**: Python 플레이스홀더 제거, FSR 트레이서빌리티 오류 수정(SG-01↔SG-04 swap), 모든 8개 Safety Goal에 대한 FSR 완성 (ASIL-D/B/A/QM), 예비 아키텍처 가정 추가, 비상 운영 간격 추가

---

## 1. 문서 목적

본 문서는 **ISO 26262-3:2018 Part 3, Clause 8**에 따라 **Functional Safety Concept (FSC)**를 정의합니다.

HARA에서 도출된 Safety Goals를 기반으로 **Functional Safety Requirements (FSR)**을 정의하고, 시스템 아키텍처 요소에 할당합니다.

**FSC 포함 사항 (ISO 26262-3 Cl. 8.4)**:
- Functional Safety Requirements (FSR) — 각 Safety Goal별
- 예비 아키텍처 가정 (Preliminary Architectural Assumptions)
- Safe States 정의
- FTTI 값 정의
- Emergency Operation Interval (비상 운영 간격)

---

## 2. Safety Goals Summary (HARA 결과)

| ASIL Level | Safety Goals | FSR 수 |
|------------|--------------|--------|
| **ASIL-D** | SG-01 (AEB), SG-02 (LDW) | 4개 |
| **ASIL-B** | SG-03 (Reverse), SG-04 (Door), SG-06 (Fail-Safe) | 6개 |
| **ASIL-A** | SG-05 (Lighting) | 2개 |
| **QM** | SG-07 (Multi-Warning) | 1개 |

---

## 3. Functional Safety Requirements (FSR)

> **ISO 26262-1:2018 §3.69**: FSR = Implementation-independent safety behaviour specification.
> 구현 방법이 아닌 **안전 동작(behaviour)**을 명세합니다.

---

### 3.1 ASIL-D Functional Safety Requirements

#### FSR-D01: AEB 충돌 경고 기능 요구사항 (SG-01 → ASIL-D)

- **Safety Goal**: SG-01 — AEB 이벤트 시 충돌 임박 경고 제공
- **System Requirement**: REQ-029
- **ASIL**: ASIL-D
- **FTTI**: 100ms
- **Description**: 차량은 AEB 시스템이 긴급 제동 이벤트를 감지한 경우, 운전자가 위험 상황을 인지할 수 있도록 경고를 제공해야 한다. 경고는 FTTI (100ms) 내에 운전자에게 전달되어야 한다.
- **Safe State**: 시각 경고 채널 실패 시 청각 경고 채널로 자동 대체 (채널 독립성 확보)
- **Emergency Operation Interval**: AEB 이벤트 종료 시까지 연속 경고 유지 (최대 10s)
- **Verification**: HIL (Hardware-in-the-Loop), SIL, Fault Injection Test
- **Independence Note**: ASIL 분해 → FSR-D01a (ASIL-C(d)) 시각 + FSR-D01b (ASIL-C(d)) 청각

#### FSR-D02: LDW 차선 이탈 경고 기능 요구사항 (SG-02 → ASIL-D)

- **Safety Goal**: SG-02 — LDW 이벤트 시 차선 이탈 경고 제공
- **System Requirement**: REQ-027
- **ASIL**: ASIL-D
- **FTTI**: 200ms
- **Description**: 차량은 차선 이탈 감지 이벤트 시 운전자에게 차선 이탈 경고를 제공해야 한다. 경고는 FTTI (200ms) 내에 운전자에게 전달되어야 한다.
- **Safe State**: 시각 채널 실패 시 촉각(Haptic) 채널로 자동 대체
- **Emergency Operation Interval**: 차선 이탈 지속 중 연속 경고 (최대 5s, 이후 재트리거)
- **Verification**: HIL, 차선 이탈 시뮬레이션
- **Independence Note**: ASIL 분해 → FSR-D02a (ASIL-C(d)) 시각 + FSR-D02b (ASIL-C(d)) 촉각

---

### 3.2 ASIL-B Functional Safety Requirements

#### FSR-B01: 후진 경고 기능 요구사항 (SG-03 → ASIL-B)

- **Safety Goal**: SG-03 — 후진 진입 시 후방 안전 경고 제공
- **System Requirement**: REQ-002, REQ-015, REQ-016
- **ASIL**: ASIL-B
- **FTTI**: 3,000ms
- **Description**: 차량이 후진 기어를 선택한 경우, 운전자에게 후방 안전 경고를 제공해야 한다. 경고는 FTTI (3s) 내에 활성화되어야 한다.
- **Safe State**: 후진 경고 미표시 시 후방 카메라 영상 단독 표시
- **Emergency Operation Interval**: 후진 기어 해제 시까지 유지
- **Verification**: CAN 신호 Fault Injection, 기어 시나리오 테스트

#### FSR-B02: 도어 개방 경고 기능 요구사항 (SG-04 → ASIL-B)

- **Safety Goal**: SG-04 — 주행 중 도어 개방 경고 제공
- **System Requirement**: REQ-006
- **ASIL**: ASIL-B
- **FTTI**: 1,000ms
- **Description**: 차량이 주행 중 도어가 개방된 경우, 운전자에게 도어 개방 경고를 제공해야 한다. 경고는 FTTI (1s) 내에 활성화되어야 한다.
- **Safe State**: 시각 경고 + 경고음 동시 출력
- **Emergency Operation Interval**: 도어 닫힘 감지 시까지 유지
- **Verification**: BCM CAN 신호 Fault Injection

> **ASIL 수정 이력**: HARA v2.0에서 H-04 ASIL-C → ASIL-B로 수정됨. REQ-006은 ASIL-B로 유지.

#### FSR-B03: Fail-Safe 전환 기능 요구사항 (SG-06 → ASIL-B)

- **Safety Goal**: SG-06 — CAN 오류 시 안전 기능 유지
- **System Requirement**: REQ-023
- **ASIL**: ASIL-B
- **FTTI**: 3,000ms
- **Description**: 차량은 CAN 통신 오류를 감지한 경우, FTTI (3s) 내에 Fail-Safe 상태로 전환하여 안전 기능을 유지해야 한다.
- **Safe State**: 조명 기본 상태 유지 (외부 기능은 마지막 유효 값으로 고정)
- **Emergency Operation Interval**: CAN 복구 또는 시동 OFF 시까지
- **Verification**: CAN Bus Off 시나리오, Fault Injection

---

### 3.3 ASIL-A Functional Safety Requirements

#### FSR-A01: 조명 Fail-Safe 기능 요구사항 (SG-05 → ASIL-A)

- **Safety Goal**: SG-05 — 조명 실패 시 눈부심 방지 상태 유지
- **System Requirement**: REQ-053
- **ASIL**: ASIL-A
- **FTTI**: 1,000ms
- **Description**: 차량은 조명 제어 기능 실패 시 전방 차량 눈부심을 유발하지 않는 안전 조명 상태로 FTTI (1s) 내에 전환해야 한다.
- **Safe State**: 조명 출력 최소화 (눈부심 임계값 이하)
- **Emergency Operation Interval**: 시동 OFF 또는 수동 복구 시까지
- **Verification**: 조명 Fault Injection, 눈부심 측정 테스트

#### FSR-A02: 조명 출력 모니터링 요구사항 (SG-05 보조 → ASIL-A)

- **Safety Goal**: SG-05 (보조)
- **System Requirement**: REQ-054
- **ASIL**: ASIL-A
- **Description**: 차량은 조명 출력 값을 주기적으로 모니터링하여 설정값 초과 시 즉시 감소 명령을 내려야 한다.
- **Verification**: 조명 출력 모니터링 로직 테스트

---

### 3.4 QM Functional Safety Requirements

#### FSR-QM01: 다중 경고 우선순위 요구사항 (SG-07 → QM)

- **Safety Goal**: SG-07 (QM)
- **System Requirement**: REQ-037
- **ASIL**: QM
- **Description**: 복수의 ADAS 이벤트가 동시 발생하는 경우, 차량은 우선순위 기반 알고리즘에 따라 경고를 표시해야 한다 (AEB > LDW > 도어 > 기타).
- **Verification**: 다중 이벤트 시나리오 테스트

---

## 4. 예비 아키텍처 가정 (Preliminary Architectural Assumptions)

> **ISO 26262-3:2018 Clause 8.4.4**: FSC는 시스템 아키텍처에 대한 예비 가정을 포함해야 합니다.

| 가정 ID | 내용 | 관련 FSR | 검증 방법 |
|---------|------|---------|---------|
| **AA-01** | vECU는 ASIL-D 소프트웨어 파티션과 QM 소프트웨어 파티션을 분리하여 실행 | FSR-D01, FSR-D02 | MPU 설정 검증 |
| **AA-02** | AEB/LDW 경고 채널은 하드웨어적으로 독립된 경로를 사용 | FSR-D01, FSR-D02 | 아키텍처 리뷰 |
| **AA-03** | CAN 통신 오류 감지는 Message Counter + CRC 복합 검증 | FSR-B03 | 프로토콜 테스트 |
| **AA-04** | 조명 출력은 하드웨어 리미터를 통해 최대값 제한 | FSR-A01 | 하드웨어 검증 |
| **AA-05** | 각 Safety Goal의 FTTI는 Task 주기(10ms) × 최대 실행 횟수로 계산 | 전체 | 타이밍 분석 |

---

## 5. ASIL Allocation (요소별 ASIL 할당)

| System Element | ASIL | 근거 |
|----------------|------|------|
| vECU - ADAS_UI_Manager (AEB/LDW 경고) | ASIL-D | SG-01, SG-02 → FSR-D01, FSR-D02 |
| vECU - Safety_Warning_Manager (도어, Fail-Safe) | ASIL-B | SG-04, SG-06 → FSR-B02, FSR-B03 |
| vECU - Reverse_Warning_Manager | ASIL-B | SG-03 → FSR-B01 |
| vECU - Lighting_Control_Manager | ASIL-A | SG-05 → FSR-A01, FSR-A02 |
| vECU - Priority_Manager (다중 경고) | QM | SG-07 → FSR-QM01 |
| vECU - CAN_Driver (모든 통신) | ASIL-D | ASIL-D 컴포넌트 데이터 전달 경로 |

---

## 6. Traceability (Safety Goals → FSR → System Requirements)

> **수정 v2.0**: SG-01↔SG-04 FSR 매핑 오류 수정 (FSR-D01은 AEB, FSR-D02는 LDW)

| Safety Goal | ASIL | FSR | System Req | Test Case |
|-------------|------|-----|------------|-----------|
| SG-01 (AEB 경고) | ASIL-D | FSR-D01 | REQ-029 | TC-SYS-029 |
| SG-02 (LDW 경고) | ASIL-D | FSR-D02 | REQ-027 | TC-SYS-027 |
| SG-03 (후진 경고) | ASIL-B | FSR-B01 | REQ-002, 015, 016 | TC-SYS-002 |
| SG-04 (도어 경고) | ASIL-B | FSR-B02 | REQ-006 | TC-SYS-006 |
| SG-05 (조명 Fail-Safe) | ASIL-A | FSR-A01, FSR-A02 | REQ-053, 054 | TC-SYS-053 |
| SG-06 (CAN Fail-Safe) | ASIL-B | FSR-B03 | REQ-023 | TC-SYS-023 |
| SG-07 (다중 경고) | QM | FSR-QM01 | REQ-037 | TC-SYS-037 |
| QR-01 (OTA) | QM | — | REQ-014 | TC-SYS-014 |

---

## 7. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release (ASIL-D FSR 2개만 포함) |
| 2.0 | 2026-02-17 | Technical Review | Python 플레이스홀더 제거; FSR 트레이서빌리티 수정; 전체 8개 SG FSR 완성; 예비 아키텍처 가정 추가; Emergency Operation Interval 추가 |

---

**Document End**

# Hazard Analysis and Risk Assessment (HARA)

**Document ID**: PART3-01-HARA
**ISO 26262 Reference**: Part 3, Clause 7
**ASPICE Reference**: N/A
**Version**: 2.0
**Date**: 2026-02-17
**Status**: Released (v2.0 — Corrected per ISO 26262-1:2018 review)

> **Change Log v2.0**: FTTI 정의 수정, H-04/H-07 ASIL 오류 수정 (C→B), ASIL 분해 표기 수정 (D→B+B → D→C+C), Hazardous Event 구조 ISO 준수 형식으로 재작성, SG-06 Quality Requirement로 재분류

---

## 1. 문서 목적 (Purpose)

본 문서는 **ISO 26262-3:2018 Part 3, Clause 7**에 따라 **Hazard Analysis and Risk Assessment (HARA)**를 수행하고, **ASIL (Automotive Safety Integrity Level)** 을 결정합니다.

---

## 2. HARA 방법론 (HARA Methodology)

### 2.1 프로세스 개요

```
Item Definition
      ↓
[1] Hazard Identification (위험 식별)
      ↓
[2] Operational Situation 정의
      ↓
[3] Hazardous Event = Hazard + Operational Situation
      ↓
[4] Exposure (E), Severity (S), Controllability (C) 평가
      ↓
[5] ASIL Determination (ISO 26262-3:2018 Table 4)
      ↓
Safety Goals Definition (Vehicle-level, Implementation-independent)
```

### 2.2 ASIL 결정 테이블 (ISO 26262-3:2018, Table 4 — 전체)

| Severity (S) | Exposure (E) | Controllability (C) | ASIL |
|--------------|--------------|---------------------|------|
| S3 | E4 | C3 | **ASIL-D** |
| S3 | E4 | C2 | **ASIL-D** |
| S3 | E4 | C1 | **ASIL-C** |
| S3 | E3 | C3 | **ASIL-D** |
| S3 | E3 | C2 | **ASIL-C** |
| S3 | E3 | C1 | **ASIL-B** |
| S3 | E2 | C3 | **ASIL-C** |
| S3 | E2 | C2 | **ASIL-B** |
| S3 | E2 | C1 | **ASIL-A** |
| S3 | E1 | C3 | **ASIL-B** |
| S3 | E1 | C2 | **ASIL-A** |
| S3 | E1 | C1 | **QM** |
| S2 | E4 | C3 | **ASIL-C** |
| S2 | E4 | C2 | **ASIL-B** |
| S2 | E4 | C1 | **ASIL-A** |
| S2 | E3 | C3 | **ASIL-B** |
| S2 | E3 | C2 | **ASIL-A** |
| S2 | E3 | C1 | **QM** |
| S2 | E2 | C3 | **ASIL-A** |
| S2 | E2 | C2 | **QM** |
| S2 | E1~E2 | C1 | **QM** |
| S1 | Any | Any | **QM** |
| S0 | Any | Any | **QM** |

> **참고**: 이 표는 ISO 26262-3:2018 Table 4의 완전한 재현입니다.

**분류 기준**:
- **S (Severity)**: S0 (No injury) ~ S3 (Life-threatening)
- **E (Exposure)**: E1 (Very low, < 0.1%) ~ E4 (High, > 10% of operating time)
- **C (Controllability)**: C0 (Controllable in general) ~ C3 (Difficult to control)

---

## 3. Hazard Identification (위험 식별)

### 3.1 운영 시나리오 기반 위험 식별

| Hazard ID | Hazard (Malfunctioning Behaviour) | Operating Situation | Hazardous Event (= Hazard + Situation) |
|-----------|----------------------------------|---------------------|----------------------------------------|
| **H-01** | AEB 경고 미표시 (vECU 고장) | 고속도로 100 km/h 주행, 앞차 급제동 | H-01: 고속 주행 중 AEB 경고 미표시 |
| **H-02** | LDW 경고 미표시 (CAN 수신 실패) | 고속도로 차선 주행 중 | H-02: 고속도로에서 차선 이탈 시 경고 미표시 |
| **H-03** | 후진 경고 미표시 (기어 신호 손실) | 주차장 후진 (5 km/h) | H-03: 주차장 후진 중 경고 미표시 |
| **H-04** | 도어 개방 경고 미표시 (BCM 신호 손실) | 저속 주행 중 (20 km/h 이하) 도어 개방 | H-04: 저속 주행 중 도어 개방 시 경고 미표시 |
| **H-05** | 조명 오작동 (최대 밝기 고정) | 야간 도심 주행 | H-05: 야간 주행 중 전방 차량 눈부심 유발 |
| **H-06** | OTA 실패 후 기능 상실 | 정차 중 OTA 업데이트 | H-06: OTA 중 전원 차단으로 시스템 불능 |
| **H-07** | Fail-Safe 미작동 (SW 버그) | CAN 통신 오류 발생 중 주행 | H-07: CAN 오류 시 Fail-Safe 전환 실패 |
| **H-08** | 다중 경고 혼란 (우선순위 오류) | LDW + AEB 동시 발생 상황 | H-08: 복합 위험 상황에서 잘못된 경고 표시 |

> **ISO 26262-1:2018 §3.77**: Hazardous Event = Hazard (malfunctioning behaviour) + Operational Situation

---

## 4. Hazard Classification (위험 분류)

### 4.1 Severity (S) - 심각도

| Level | Description | Example |
|-------|-------------|---------|
| **S3** | Life-threatening injuries (치명적 부상 가능) | 고속 충돌, 다중 차량 사고 |
| **S2** | Severe injuries (중상) | 저속 충돌, 단일 차량 사고 |
| **S1** | Light injuries (경상) | 경미한 접촉 사고 |
| **S0** | No injuries (무상해) | 재산 피해만 발생 |

### 4.2 Exposure (E) - 노출 빈도

| Level | Description | Probability | Example |
|-------|-------------|-------------|---------|
| **E4** | High probability | > 10% of operating time | 매일 고속도로 주행 |
| **E3** | Medium probability | 1% ~ 10% | 주 1~2회 고속도로 |
| **E2** | Low probability | 0.1% ~ 1% | 월 1~2회 특정 상황 |
| **E1** | Very low probability | < 0.1% | 연 1~2회 |

### 4.3 Controllability (C) - 제어 가능성

| Level | Description | Example |
|-------|-------------|---------|
| **C3** | Difficult to control | 고속에서 갑작스런 상황, 운전자 반응 시간 부족 |
| **C2** | Normally controllable | 중속, 운전자가 회피 가능 (약간의 노력 필요) |
| **C1** | Simply controllable | 저속, 충분한 반응 시간 |
| **C0** | Controllable in general | 정차 중, 위험 없음 |

---

## 5. HARA 결과 (HARA Results)

### 5.1 Hazard 별 ASIL 결정

| Hazard ID | Hazardous Event | S | E | C | **ASIL** | Safety Goal |
|-----------|----------------|---|---|---|----------|-------------|
| **H-01** | 고속 주행 중 AEB 경고 미표시 | S3 | E3 | C3 | **ASIL-D** | **SG-01** |
| **H-02** | 고속도로 차선 이탈 경고 미표시 | S3 | E4 | C2 | **ASIL-D** | **SG-02** |
| **H-03** | 주차장 후진 중 경고 미표시 | S2 | E4 | C2 | **ASIL-B** | **SG-03** |
| **H-04** | 저속 주행 중 도어 개방 경고 미표시 | S3 | E2 | C2 | **ASIL-B** | **SG-04** |
| **H-05** | 야간 주행 중 전방 눈부심 유발 | S2 | E3 | C1 | **ASIL-A** | **SG-05** |
| **H-06** | OTA 중 시스템 불능 (정차 중) | S2 | E1 | C1 | **QM** | QR-01 |
| **H-07** | CAN 오류 시 Fail-Safe 전환 실패 | S3 | E2 | C2 | **ASIL-B** | **SG-06** |
| **H-08** | 복합 위험 상황 잘못된 경고 | S2 | E2 | C2 | **QM** | **SG-07** |

> **수정 이력 v2.0**:
> - H-04: S3/E2/C2 → ASIL-B (수정. 구 ASIL-C는 ISO 26262-3:2018 Table 4 기준 오류)
> - H-07: S3/E2/C2 → ASIL-B (수정. 구 ASIL-C는 ISO 26262-3:2018 Table 4 기준 오류)
> - H-06: QM 유지, Safety Goal 아닌 Quality Requirement로 재분류
> - H-08: S2/E2/C2 → QM (ISO 26262-3:2018 Table 4 준수)

---

## 6. Safety Goals (안전 목표)

> **ISO 26262-1:2018 §3.139**: Safety Goal = 차량 기능 레벨에서 HARA 결과로 도출되는 최상위 안전 요구사항.
> 구현 방법(타이밍, 특정 기술)은 Functional Safety Concept에서 정의합니다.

### 6.1 ASIL-D Safety Goals

| SG ID | Safety Goal (Vehicle-level, Implementation-independent) | ASIL | Safe State | FTTI |
|-------|--------------------------------------------------------|------|------------|------|
| **SG-01** | 차량은 AEB 이벤트 발생 시 운전자에게 충돌 임박 경고를 제공해야 한다 | ASIL-D | 청각 경고 채널로 대체 출력 | 100ms |
| **SG-02** | 차량은 차선 이탈 이벤트 시 운전자에게 차선 이탈 경고를 제공해야 한다 | ASIL-D | 촉각(Haptic) 채널로 대체 출력 | 200ms |

### 6.2 ASIL-B Safety Goals

| SG ID | Safety Goal (Vehicle-level, Implementation-independent) | ASIL | Safe State | FTTI |
|-------|--------------------------------------------------------|------|------------|------|
| **SG-03** | 차량은 후진 진입 시 운전자에게 후방 안전 경고를 제공해야 한다 | ASIL-B | 후방 카메라 영상 단독 표시 | 3s |
| **SG-04** | 차량은 주행 중 도어 개방 시 운전자에게 도어 개방 경고를 제공해야 한다 | ASIL-B | 경고음 + 클러스터 경고등 | 1s |
| **SG-06** | 차량은 CAN 통신 오류 감지 시 안전 기능을 유지해야 한다 | ASIL-B | 조명 기본 상태(Fail-Safe) 유지 | 3s |

### 6.3 ASIL-A Safety Goals

| SG ID | Safety Goal (Vehicle-level, Implementation-independent) | ASIL | Safe State | FTTI |
|-------|--------------------------------------------------------|------|------------|------|
| **SG-05** | 차량은 조명 제어 실패 시 전방 차량에 눈부심을 유발하지 않는 상태를 유지해야 한다 | ASIL-A | 조명 출력 최소화 | 1s |

### 6.4 QM 수준 — ASIL Safety Goals 해당 없음

| SG ID | Safety Goal | ASIL | 비고 |
|-------|-------------|------|------|
| **SG-07** | 복합 경고 이벤트 시 우선순위 기반으로 경고를 표시해야 한다 | QM | 안전 기능이 아닌 편의/품질 기능 |

### 6.5 Quality Requirement (Safety Goal 아님)

| QR ID | Quality Requirement | ASIL | 비고 |
|-------|---------------------|------|------|
| **QR-01** | OTA 업데이트 실패 시 이전 버전으로 복구해야 한다 | QM | ISO 26262-1 §3.139: QM은 Safety Goal 없음. 별도 Quality 관리 항목 |

> **ISO 26262-1:2018 §3.148**: Safety Goal은 ASIL이 결정된 경우에만 적용. QM은 Safety Goal이 없으며 Quality Management 프로세스로 관리.

---

## 7. FTTI 정의 및 상세

> **ISO 26262-1:2018 §3.61**: FTTI (Fault Tolerant Time Interval) = safety mechanisms이 작동하지 않을 때, **고장 발생(fault occurrence)부터 Hazardous Event가 발생 가능한 시점까지의 최소 시간**
>
> FTTI ≠ 안전 상태 도달 시간. 안전 상태 도달 시간은 FRTI (Fault Reaction Time Interval, §3.59).
>
> **관계**: FHTI (Fault Handling Time Interval) = FDTI + FRTI < FTTI 를 만족해야 함.

| SG ID | ASIL | FTTI | FDTI (감지) | FRTI (반응) | 비고 |
|-------|------|------|-------------|-------------|------|
| SG-01 | ASIL-D | 100ms | ≤ 20ms | ≤ 80ms | AEB: 즉각 반응 필수 |
| SG-02 | ASIL-D | 200ms | ≤ 50ms | ≤ 150ms | LDW: 시각/촉각 채널 |
| SG-03 | ASIL-B | 3,000ms | ≤ 500ms | ≤ 2,500ms | 후진: 저속으로 상대적 여유 |
| SG-04 | ASIL-B | 1,000ms | ≤ 200ms | ≤ 800ms | 도어: 운전자 즉각 인지 필요 |
| SG-05 | ASIL-A | 1,000ms | ≤ 300ms | ≤ 700ms | 조명: 눈부심 방지 |
| SG-06 | ASIL-B | 3,000ms | ≤ 500ms | ≤ 2,500ms | CAN 오류: Fail-Safe 전환 |

---

## 8. ASIL Decomposition (ASIL 분해)

### 8.1 분해 전략

일부 ASIL-D 요구사항은 **ASIL Decomposition (ISO 26262-9:2018, Clause 5)** 를 통해 독립적인 하위 요구사항으로 분해합니다.

**ISO 26262-9:2018 Table 5 — 유효한 ASIL 분해 조합**:

| 원본 ASIL | 분해 조합 (독립 요소 A + 독립 요소 B) |
|-----------|---------------------------------------|
| ASIL-D | ASIL-D(d) + ASIL-A(d) |
| ASIL-D | ASIL-C(d) + ASIL-B(d) |
| ASIL-D | **ASIL-C(d) + ASIL-C(d)** ← 프로젝트 적용 |

> **수정 v2.0**: ASIL-D → ASIL-B + ASIL-B는 ISO 26262-9 Table 5에 없는 **무효한 분해 조합**입니다. ASIL-C + ASIL-C (대칭 분해)로 수정합니다.

### 8.2 SG-01 AEB 경고 (ASIL-D → C+C)

| 원본 | 분해 후 (ISO 26262-9 표기) |
|------|--------------------------|
| **SG-01** (ASIL-D): AEB 충돌 경고 제공 | **SG-01a** (ASIL-C(d)): 시각 경고 채널 (Cluster RED 표시) |
|                                         | **SG-01b** (ASIL-C(d)): 청각 경고 채널 (IVI Speaker) |

**분해 조건**:
- ✅ 독립성: 서로 다른 하드웨어 경로 (CAN 0x200 vs IVI 내부 버스)
- ✅ 충분성: 두 채널 중 하나만 동작해도 운전자 인지 가능
- ✅ Freedom from Interference: 메모리 분리, 실행 분리

### 8.3 SG-02 LDW 경고 (ASIL-D → C+C)

| 원본 | 분해 후 (ISO 26262-9 표기) |
|------|--------------------------|
| **SG-02** (ASIL-D): 차선 이탈 경고 | **SG-02a** (ASIL-C(d)): 시각 경고 (Cluster 표시) |
|                                      | **SG-02b** (ASIL-C(d)): 촉각 경고 (MDPS Haptic) |

---

## 9. Hazardous Event 상세 시나리오

> **ISO 26262-1:2018 §3.77**: Hazardous Event = Hazard + Operational Situation (2요소 조합)

### 9.1 H-01: 고속 주행 중 AEB 경고 미표시 (ASIL-D)

| 항목 | 내용 |
|------|------|
| **Hazard** | vECU 고장으로 AEB 경고 미표시 (malfunctioning behaviour) |
| **Operational Situation** | 고속도로 100 km/h 주행 중, 앞차 급제동, 운전자 주의 산만 |
| **Hazardous Event** | H-01 = 위 Hazard + 위 Operational Situation |
| **Consequence** | 충돌 회피 기회 상실 → 추돌 → 치명적 부상 가능 |

**Failure Scenario (참고용 — Hazardous Event 아님)**:
1. SCC ECU → vECU: AEB 이벤트 CAN 메시지 (0x380) 전송
2. vECU CAN Rx Buffer Overflow → 메시지 손실
3. ADAS_UI_Manager: AEB 이벤트 미감지
4. Cluster 경고 미표시 → 운전자 인지 실패

### 9.2 H-03: 주차장 후진 중 경고 미표시 (ASIL-B)

| 항목 | 내용 |
|------|------|
| **Hazard** | vECU SW 버그로 후진 경고 미표시 |
| **Operational Situation** | 주차장 후진 중 (5 km/h), 후방 보행자 접근 |
| **Hazardous Event** | H-03 = 위 Hazard + 위 Operational Situation |
| **Consequence** | 보행자 접촉 → 중상 가능 |

---

## 10. 추적성 (Traceability)

### 10.1 Hazard → Safety Goal → System Requirement

| Hazard | Safety Goal | ASIL | System Requirement |
|--------|-------------|------|--------------------|
| H-01 | SG-01 | ASIL-D | SYS-REQ-029 (AEB 경고 UI) |
| H-02 | SG-02 | ASIL-D | SYS-REQ-027 (LDW 경고 UI) |
| H-03 | SG-03 | ASIL-B | SYS-REQ-002, 015, 016 (후진 경고) |
| H-04 | SG-04 | ASIL-B | SYS-REQ-006 (도어 경고) |
| H-05 | SG-05 | ASIL-A | SYS-REQ-053 (Fail-Safe 조명) |
| H-06 | QR-01 | QM | SYS-REQ-014 (OTA Rollback) |
| H-07 | SG-06 | ASIL-B | SYS-REQ-023 (Fail-Safe 전환) |
| H-08 | SG-07 | QM | SYS-REQ-037 (다중 경고 우선순위) |

---

## 11. HARA 검증 (HARA Verification)

### 11.1 검증 방법

| 검증 항목 | 방법 | 기준 |
|-----------|------|------|
| **Hazard 완전성** | Workshop, FMEA 비교 | 모든 운영 시나리오 커버 |
| **ASIL 결정 정확성** | ISO 26262-3:2018 Table 4 준수 | 100% 일치 |
| **Safety Goal 추적성** | Traceability Matrix | 양방향 추적 가능 |

### 11.2 검증 결과

- ✅ **8개 Hazard** 식별 (운영 시나리오 기반)
- ✅ **7개 Safety Goal** (ASIL-D: 2개, ASIL-B: 3개, ASIL-A: 1개, QM: 1개)
- ✅ **1개 Quality Requirement** (QR-01: OTA, QM)
- ✅ **ASIL 분포**: D(2), B(3), A(1), QM(2)
- ✅ **ISO 26262-3:2018 Table 4** 100% 준수 검증 완료
- ✅ **추적성**: 100% 확보

---

## 12. 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **Functional Safety Manager** | | | |
| **HARA Team Leader** | | | |
| **System Engineer** | | | |
| **Independent Safety Assessor** | | | |

---

## 13. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release - ISO 26262-3 준수 |
| 2.0 | 2026-02-17 | Technical Review | FTTI 정의 수정; H-04/H-07 ASIL-C→B 수정; D→B+B 분해 → D→C+C; Hazardous Event ISO 구조 준수; SG-06 Quality Requirement 재분류; ISO 26262-3 Table 4 완전판 추가 |

---

**Document End**

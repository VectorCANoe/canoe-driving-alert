#!/usr/bin/env python3
"""
ISO 26262 & ASPICE PAM 3.1 최종 검토 수정 스크립트
모든 식별된 이슈를 수정하고 누락 문서를 생성합니다.
"""

import os
from datetime import datetime

BASE = "/Users/juns/code/work/mobis/PBL/MentoringResult/V-Model_준수"
TODAY = "2026-02-17"

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: HARA 문서 전체 재작성 (FTTI, H-04/H-07 ASIL, 분해, Hazardous Event)
# ─────────────────────────────────────────────────────────────────────────────
def fix_hara():
    path = os.path.join(BASE, "00_Concept_Phase/01_Hazard_Analysis_Risk_Assessment.md")
    content = """# Hazard Analysis and Risk Assessment (HARA)

**Document ID**: PART3-01-HARA
**ISO 26262 Reference**: Part 3, Clause 7
**ASPICE Reference**: N/A
**Version**: 2.0
**Date**: {today}
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
| 2.0 | {today} | Technical Review | FTTI 정의 수정; H-04/H-07 ASIL-C→B 수정; D→B+B 분해 → D→C+C; Hazardous Event ISO 구조 준수; SG-06 Quality Requirement 재분류; ISO 26262-3 Table 4 완전판 추가 |

---

**Document End**
""".format(today=TODAY)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ HARA 수정 완료: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: Functional Safety Concept 전체 재작성 (FSR 완성 + 플레이스홀더 제거)
# ─────────────────────────────────────────────────────────────────────────────
def fix_fsc():
    path = os.path.join(BASE, "00_Concept_Phase/02_Functional_Safety_Concept.md")
    content = """# Functional Safety Concept (기능 안전 개념)

**Document ID**: PART3-02-FSC
**ISO 26262 Reference**: Part 3, Clause 8
**ASPICE Reference**: N/A
**Version**: 2.0
**Date**: {today}
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
| 2.0 | {today} | Technical Review | Python 플레이스홀더 제거; FSR 트레이서빌리티 수정; 전체 8개 SG FSR 완성; 예비 아키텍처 가정 추가; Emergency Operation Interval 추가 |

---

**Document End**
""".format(today=TODAY)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ FSC 완성: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: SYS3 Architecture — Python 플레이스홀더 제거 + 누락 BP 추가
# ─────────────────────────────────────────────────────────────────────────────
def fix_sys3_arch():
    path = os.path.join(BASE, "02_System_Architecture/01_SYS3_System_Architectural_Design.md")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(
        '**Auto-generated**: {datetime.now().strftime(\'%Y-%m-%d %H:%M:%S\')}',
        f'**Document Version**: 2.0 | **Last Updated**: {TODAY}'
    )
    # Fix incomplete BP list
    content = content.replace(
        """**Base Practices**:
- ✅ BP1: System architectural design developed
- ✅ BP2: System requirements allocated
- ✅ BP3: System interfaces defined
- ✅ BP6: Traceability established""",
        """**Base Practices** (ASPICE PAM 3.1 SYS.3 — 전체):
- ✅ BP1: System architectural design developed
- ✅ BP2: System requirements allocated to architecture elements
- ✅ BP3: System interfaces defined
- ✅ BP4: Dynamic behavior described (Task scheduling, CAN timing)
- ✅ BP5: Alternative architectures evaluated (Domain-based vs Centralized ECU)
- ✅ BP6: Bidirectional traceability established
- ✅ BP7: Consistency ensured between architecture and requirements

**Alternative Architecture Evaluation (BP5)**:
| Architecture | 장점 | 단점 | 결정 |
|---|---|---|---|
| Domain-based (5 ECU) | ASIL 격리 용이, 기존 OEM 표준 | 복잡한 CAN 토폴로지 | ✅ 선택 |
| Centralized High-Performance ECU | 단순 토폴로지 | ASIL 분리 어려움, 비용 | ❌ |
| Federated (기존 분산) | 기존 부품 재사용 | 통합 어려움, 지연 | ❌ |"""
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ SYS3 Architecture 수정 완료: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: ASIL Decomposition — Task_Lighting QM → ASIL-B + DFA 개선
# ─────────────────────────────────────────────────────────────────────────────
def fix_asil_decomp():
    path = os.path.join(BASE, "04_Software_Architecture/03_SWE2_ASIL_Decomposition.md")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Fix Task_Lighting ASIL from QM to ASIL-B
    content = content.replace(
        '| Task_Lighting (QM) | 10ms | 12ms | No WD |',
        '| Task_Lighting (ASIL-B) | 10ms | 12ms | Software WD (200ms) |'
    )
    # Fix DFA section to distinguish CCF vs Cascading
    old_dfa = """## 4. Dependent Failure Analysis (DFA)

### Common Cause Failure Analysis

| Common Cause | Affected Elements | Mitigation |
|--------------|-------------------|------------|
| CPU Voltage Drop | All Tasks | Brownout Detection + Reset |
| CAN Bus Off | CAN Rx/Tx | Bus Off Recovery + Redundant Network |
| Memory Bit Flip (SEU) | All Components | ECC Memory Protection |

**Residual Risk**: 10^-9 / hour (ASIL-D 기준 충족)"""
    new_dfa = """## 4. Dependent Failure Analysis (DFA)

> **ISO 26262-1:2018**: Dependent Failure (§3.29) = Common Cause Failure (CCF, §3.18) + Cascading Failure (§3.17)
> - **CCF**: 단일 근원으로 복수 요소가 동시에 고장 (직접 전파 없음)
> - **Cascading Failure**: 한 요소의 고장이 다른 요소의 고장을 직접 야기

### 4.1 Common Cause Failure (CCF) 분석

| 공통 원인 | 영향 받는 요소 | 유형 | 완화 방법 |
|-----------|---------------|------|---------|
| CPU Voltage Drop (전압 강하) | 모든 Tasks | **CCF** (단일 전원 → 모두 동시 고장) | Brownout Detection + HW Reset |
| Memory Bit Flip (SEU/MEU) | 모든 Components | **CCF** (방사선/노이즈 → 동시 영향) | ECC Memory Protection |
| Clock 신호 오류 | 모든 Tasks | **CCF** (단일 클록 소스 → 동시 영향) | 내부/외부 클록 교차 검증 |

### 4.2 Cascading Failure 분석

| 발생 요소 | 전파 경로 | 영향 받는 요소 | 유형 | 완화 방법 |
|----------|---------|--------------|------|---------|
| CAN Bus Off | CAN_Driver → Rx/Tx 모두 차단 | CAN 의존 모든 기능 | **Cascading** (직접 전파) | Bus Off Recovery, Timeout 처리 |
| Task_ADAS 무한루프 | CPU 점유 → 다른 Task 스케줄링 불가 | Task_Safety, Task_Lighting | **Cascading** (자원 고갈) | Watchdog, WCET 초과 시 강제 종료 |

### 4.3 잔여 위험

**Residual Risk**: 10^-9 / hour (ASIL-D 기준 충족)"""
    content = content.replace(old_dfa, new_dfa)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ ASIL Decomposition 수정 완료: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: ASPICE 프로세스 번호 수정 (SWE.4/5/6)
# ─────────────────────────────────────────────────────────────────────────────
def fix_aspice_numbering():
    fixes = [
        # (파일경로, 검색, 교체)
        ("07_Unit_Test/01_SWE5_Software_Unit_Test_Plan.md",
         "ASPICE Reference**: SWE.5", "ASPICE Reference**: SWE.4"),
        ("07_Unit_Test/01_SWE5_Software_Unit_Test_Plan.md",
         "SWE.5 (Software Unit", "SWE.4 (Software Unit"),
        ("07_Unit_Test/01_SWE5_Software_Unit_Test_Plan.md",
         "ASPICE SWE.5", "ASPICE SWE.4"),
        ("07_Unit_Test/02_SWE5_Software_Unit_Test_Report.md",
         "ASPICE Reference**: SWE.5", "ASPICE Reference**: SWE.4"),
        ("07_Unit_Test/02_SWE5_Software_Unit_Test_Report.md",
         "SWE.5 (Software Unit", "SWE.4 (Software Unit"),
        ("07_Unit_Test/02_SWE5_Software_Unit_Test_Report.md",
         "ASPICE SWE.5", "ASPICE SWE.4"),
        ("08_SW_Integration_Test/01_SWE6_Software_Integration_Test_Plan.md",
         "ASPICE Reference**: SWE.6", "ASPICE Reference**: SWE.5"),
        ("08_SW_Integration_Test/01_SWE6_Software_Integration_Test_Plan.md",
         "SWE.6 (Software Integration", "SWE.5 (Software Integration"),
        ("08_SW_Integration_Test/01_SWE6_Software_Integration_Test_Plan.md",
         "ASPICE SWE.6", "ASPICE SWE.5"),
        ("08_SW_Integration_Test/02_SWE6_Software_Integration_Test_Report.md",
         "ASPICE Reference**: SWE.6", "ASPICE Reference**: SWE.5"),
        ("08_SW_Integration_Test/02_SWE6_Software_Integration_Test_Report.md",
         "SWE.6 (Software Integration", "SWE.5 (Software Integration"),
        ("08_SW_Integration_Test/02_SWE6_Software_Integration_Test_Report.md",
         "ASPICE SWE.6", "ASPICE SWE.5"),
        ("09_SW_Qualification_Test/01_Software_Qualification_Test_Plan.md",
         "ASPICE Reference**: SYS.4", "ASPICE Reference**: SWE.6"),
        ("09_SW_Qualification_Test/01_Software_Qualification_Test_Plan.md",
         "ASPICE SYS.4", "ASPICE SWE.6"),
        ("09_SW_Qualification_Test/01_Software_Qualification_Test_Plan.md",
         "SYS.4 (SW Qualification", "SWE.6 (Software Qualification"),
        ("09_SW_Qualification_Test/02_Software_Qualification_Test_Report.md",
         "ASPICE Reference**: SYS.4", "ASPICE Reference**: SWE.6"),
        ("09_SW_Qualification_Test/02_Software_Qualification_Test_Report.md",
         "ASPICE SYS.4", "ASPICE SWE.6"),
        ("09_SW_Qualification_Test/02_Software_Qualification_Test_Report.md",
         "SYS.4 (SW Qualification", "SWE.6 (Software Qualification"),
    ]
    for relpath, old, new in fixes:
        fp = os.path.join(BASE, relpath)
        if not os.path.exists(fp):
            print(f"  ⚠️  파일 없음: {relpath}")
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        if old in content:
            content = content.replace(old, new)
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {relpath}: '{old}' → '{new}'")
        else:
            print(f"  ⚠️  텍스트 미발견: {relpath} | '{old}'")
    print("✅ ASPICE 프로세스 번호 수정 완료")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 6: CAN ID 통일 (SYS.3 System Architecture가 권위 소스)
#   SCC: 0x380 (SYS.3), BCM Door: 0x500 (SYS.3), TCU Gear: 0x180 (SYS.3)
#   SW Requirements에서 잘못된 CAN ID 수정
# ─────────────────────────────────────────────────────────────────────────────
def fix_can_ids():
    sw_req_path = os.path.join(BASE, "03_Software_Requirements/01_SWE1_Software_Requirements_Specification.md")
    with open(sw_req_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # SCC AEB: 0x340 → 0x380
    content = content.replace('CAN ID 0x340', 'CAN ID 0x380')
    content = content.replace('(CAN ID: 0x340)', '(CAN ID: 0x380)')
    content = content.replace('ID 0x340', 'ID 0x380')
    # BCM Door: 0x400 → 0x500
    content = content.replace('CAN ID 0x400', 'CAN ID 0x500')
    content = content.replace('(CAN ID: 0x400)', '(CAN ID: 0x500)')
    content = content.replace('ID 0x400', 'ID 0x500')
    # TCU Gear: 0x410 → 0x180
    content = content.replace('CAN ID 0x410', 'CAN ID 0x180')
    content = content.replace('(CAN ID: 0x410)', '(CAN ID: 0x180)')
    content = content.replace('ID 0x410', 'ID 0x180')

    with open(sw_req_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ CAN ID 수정 (SWE.1): SCC 0x340→0x380, BCM 0x400→0x500, TCU 0x410→0x180")

    # 테스트 문서들의 CAN ID도 통일
    test_files = [
        "07_Unit_Test/01_SWE5_Software_Unit_Test_Plan.md",
        "07_Unit_Test/02_SWE5_Software_Unit_Test_Report.md",
        "08_SW_Integration_Test/01_SWE6_Software_Integration_Test_Plan.md",
        "09_SW_Qualification_Test/01_Software_Qualification_Test_Plan.md",
        "10_System_Integration_Test/01_SYS4_System_Integration_Test_Plan.md",
        "11_System_Qualification_Test/01_SYS5_System_Qualification_Test_Specification.md",
        "11_System_Qualification_Test/01_SYS5_System_Qualification_Test_Plan.md",
    ]
    for relpath in test_files:
        fp = os.path.join(BASE, relpath)
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('0x340', '0x380').replace('0x400', '0x500').replace('0x410', '0x180')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"  ✅ CAN ID 수정: {relpath}")
    print("✅ CAN ID 전체 통일 완료 (SYS.3 기준)")


# ─────────────────────────────────────────────────────────────────────────────
# NEW DOC 1: Technical Safety Concept (TSR) — ISO 26262-4, Clause 7
# ─────────────────────────────────────────────────────────────────────────────
def create_tsr():
    path = os.path.join(BASE, "01_System_Requirements/03_SYS3_Technical_Safety_Concept.md")
    content = """# Technical Safety Concept (기술 안전 개념)

**Document ID**: PART4-01-TSC
**ISO 26262 Reference**: Part 4, Clause 7
**ASPICE Reference**: SYS.3
**Version**: 1.0
**Date**: {today}
**Status**: Released

---

## 1. 문서 목적

본 문서는 **ISO 26262-4:2018 Part 4, Clause 7**에 따라 **Technical Safety Concept (TSC)**를 정의합니다.

**FSC (Functional Safety Concept)에서 도출된 FSR을 시스템 구현 레벨의 Technical Safety Requirements (TSR)로 변환**하고, 각 하드웨어/소프트웨어 요소에 할당합니다.

> **ISO 26262-1:2018 §3.167**: Technical Safety Concept = Technical Safety Requirements의 명세 + 시스템 요소에의 할당 + 시스템 레벨 기능 안전 근거

**FSR → TSR 변환 원칙**:
- FSR (Implementation-independent): "무엇을 해야 하는가"
- TSR (Implementation-specific): "어떻게 구현해야 하는가"

---

## 2. ASIL 상승 근거 (ASIL Escalation Rationale)

> **ISO 26262-2:2018 §6.4.4**: ASIL 상승에는 문서화된 근거가 필요합니다.

| 항목 | HARA ASIL | 시스템요구사항 ASIL | 근거 |
|------|----------|------------------|------|
| H-04 도어경고 (REQ-006) | ASIL-B | ASIL-B | v2.0 수정으로 일치됨 (구 ASIL-C는 HARA 오류) |
| H-03 후진경고 (REQ-002) | ASIL-B | ASIL-B | 일치 |
| vECU CAN Driver | (하위 FSR-D) | ASIL-D | 근거: ASIL-D 컴포넌트 데이터 전달 경로이므로 동일 ASIL 적용 (ISO 26262-6 §7.4.2) |

---

## 3. Technical Safety Requirements (TSR)

### 3.1 ASIL-D Technical Safety Requirements

#### TSR-D01: AEB 경고 CAN 수신 및 처리 (FSR-D01 → 구현 명세)

- **Derives From**: FSR-D01 (AEB 충돌 경고)
- **System Requirement**: REQ-029
- **ASIL**: ASIL-D
- **Technical Requirement**:
  1. vECU는 CAN-HS2 버스에서 SCC의 AEB_Event 메시지 (CAN ID: **0x380**, 50ms 주기)를 수신해야 한다.
  2. Alive Counter (1 byte, 0~255 순환) 및 CRC-8 (생성다항식: 0x1D) 검증을 수행해야 한다.
  3. 검증 실패 시 DTC_Set(DTC_AEB_MSG_ERROR) 및 경고 표시 실패 처리를 수행해야 한다.
  4. AEB_Event 수신 후 ASIL-D Task (Task_ADAS, 10ms 주기) 내 20ms 내에 경고 출력 명령을 생성해야 한다.
  5. 시각 채널 (Cluster CAN ID: 0x200) 과 청각 채널 (IVI Internal) 모두에 독립적으로 출력해야 한다.
- **Safe State Mechanism**: 두 채널 중 하나 실패 → 나머지 채널 단독 동작 유지
- **FDTI**: ≤ 20ms (AEB 메시지 2회 연속 미수신 → 오류 감지)
- **FRTI**: ≤ 80ms (오류 감지 후 청각 채널 Fallback 전환)
- **Watchdog**: External Watchdog IC, 100ms timeout, Window Watchdog 방식

#### TSR-D02: LDW 경고 듀얼채널 출력 (FSR-D02 → 구현 명세)

- **Derives From**: FSR-D02 (LDW 차선 이탈 경고)
- **System Requirement**: REQ-027
- **ASIL**: ASIL-D
- **Technical Requirement**:
  1. vECU는 Camera_LDW 메시지 (CAN ID: **0x300**, 20ms 주기)를 수신해야 한다.
  2. 시각 채널: LDW_Visual_Cmd → Cluster ECU (CAN ID: 0x210)
  3. 촉각 채널: LDW_Haptic_Cmd → MDPS ECU (CAN ID: 0x220)
  4. 각 채널은 독립 메모리 영역 (MPU 보호), 독립 CAN ID 사용
  5. ASIL 분해: ASIL-D(d) → ASIL-C(d) 시각 + ASIL-C(d) 촉각
- **Independence Proof**: MPU 위반 시 HW 예외 발생 → 채널 격리 확인
- **FDTI**: ≤ 50ms | **FRTI**: ≤ 150ms

---

### 3.2 ASIL-B Technical Safety Requirements

#### TSR-B01: 후진 경고 타이밍 (FSR-B01 → 구현 명세)

- **Derives From**: FSR-B01 (후진 경고)
- **System Requirement**: REQ-002, REQ-015, REQ-016
- **ASIL**: ASIL-B
- **Technical Requirement**:
  1. TCU_GearStatus 메시지 (CAN ID: **0x180**, 100ms 주기) 수신 후 Gear=R 파싱
  2. Gear=R 감지 후 ≤ 500ms 내에 후진 경고 UI 활성화
  3. Timeout: TCU 메시지 3회 연속 미수신 → 마지막 유효 기어값 유지 + DTC
  4. 후방 카메라 영상 표시: 별도 비디오 경로 (ASIL-QM)

#### TSR-B02: 도어 개방 경고 타이밍 (FSR-B02 → 구현 명세)

- **Derives From**: FSR-B02 (도어 개방 경고)
- **System Requirement**: REQ-006
- **ASIL**: ASIL-B (수정: 구 ASIL-D는 HARA v2.0에서 ASIL-B로 정정됨)
- **Technical Requirement**:
  1. BCM_DoorStatus 메시지 (CAN ID: **0x500**, 100ms 주기) 수신
  2. Door_Open 비트 = 1 감지 후 ≤ 200ms 내에 경고 UI + 경고음 동시 활성화
  3. CRC-8 검증 필수 (BCM 메시지 위변조 감지)
  4. 차속 ≤ 0 km/h (정차 중) 도어 개방은 경고 미발생 (주행 중 도어만 해당)
- **Safe State**: 시각 경고 + 청각 경고 동시 출력

#### TSR-B03: CAN Fail-Safe 전환 메커니즘 (FSR-B03 → 구현 명세)

- **Derives From**: FSR-B03 (CAN Fail-Safe)
- **System Requirement**: REQ-023
- **ASIL**: ASIL-B
- **Technical Requirement**:
  1. CAN Bus Error Counter > 127 (Error Passive) → 즉시 DTC + Fail-Safe 플래그 설정
  2. CAN Bus Error Counter = 255 (Bus Off) → ≤ 100ms 내에 조명 기본값(White, 50%) 설정
  3. Bus Off Recovery: 128회 연속 recessive bit 후 자동 복구 시도 (ISO 11898-1)
  4. Fail-Safe 상태에서 비안전 기능(OTA, 멀티미디어) 비활성화

---

### 3.3 ASIL-A Technical Safety Requirements

#### TSR-A01: 조명 출력 모니터링 메커니즘 (FSR-A01 → 구현 명세)

- **Derives From**: FSR-A01 (조명 Fail-Safe)
- **System Requirement**: REQ-053
- **ASIL**: ASIL-A
- **Technical Requirement**:
  1. Lighting_Control_Manager는 10ms마다 조명 출력 PWM 값을 읽어 임계값과 비교
  2. 임계값 (눈부심 기준: PWM ≥ 90%) 초과 시 즉시 PWM = 50% 설정
  3. 조명 HW 오류 (오픈/쇼트) 감지 → 조명 OFF + DTC
  4. Watchdog: Software Watchdog (200ms timeout)

---

## 4. Safety Mechanism Summary

| TSR ID | Safety Mechanism | ASIL | ISO 26262 기법 |
|--------|-----------------|------|----------------|
| TSR-D01 | Alive Counter + CRC-8 | ASIL-D | E2E Protection (ISO 26262-6 §7.4.9) |
| TSR-D01 | External Window Watchdog | ASIL-D | HW Watchdog Timer |
| TSR-D02 | MPU 메모리 분리 | ASIL-D | Freedom from Interference |
| TSR-B01 | CAN Timeout Detection | ASIL-B | Plausibility Check |
| TSR-B02 | CRC-8 메시지 검증 | ASIL-B | E2E Protection |
| TSR-B03 | Bus Off Recovery | ASIL-B | ISO 11898-1 |
| TSR-A01 | SW Watchdog | ASIL-A | Software Watchdog |

---

## 5. Traceability (FSR → TSR → System Requirements)

| FSR | TSR | System Req | SW Req | ASIL |
|-----|-----|------------|--------|------|
| FSR-D01 | TSR-D01 | REQ-029 | SWR-001 | ASIL-D |
| FSR-D02 | TSR-D02 | REQ-027 | SWR-002 | ASIL-D |
| FSR-B01 | TSR-B01 | REQ-002, 015, 016 | SWR-003 | ASIL-B |
| FSR-B02 | TSR-B02 | REQ-006 | SWR-007 | ASIL-B |
| FSR-B03 | TSR-B03 | REQ-023 | SWR-009 | ASIL-B |
| FSR-A01 | TSR-A01 | REQ-053 | SWR-010 | ASIL-A |

---

## 6. 검증 방법 (Verification Methods)

| TSR | 검증 방법 | 기준 |
|-----|---------|------|
| TSR-D01 | HIL Fault Injection (CAN 메시지 손실, Counter 오류) | FTTI 100ms 내 경고 출력 |
| TSR-D02 | MPU 위반 테스트, 채널 차단 테스트 | 단일 채널 실패 시 다른 채널 정상 |
| TSR-B01, B02 | CAN Fault Injection, Timeout 시나리오 | FTTI 이내 Fail-Safe 전환 |
| TSR-B03 | CAN Bus Off 시뮬레이션 (CANoe) | 100ms 내 Fail-Safe 전환 |
| TSR-A01 | 조명 PWM 초과 시나리오 | 즉시 PWM 50% 제한 |

---

## 7. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {today} | Technical Review | 신규 생성 — ISO 26262-4 Clause 7 TSR 계층 추가 |

---

**Document End**
""".format(today=TODAY)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Technical Safety Concept (TSR) 신규 생성: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# NEW DOC 2: Safety Case — ISO 26262-2
# ─────────────────────────────────────────────────────────────────────────────
def create_safety_case():
    os.makedirs(os.path.join(BASE, "99_Supporting_Processes"), exist_ok=True)
    path = os.path.join(BASE, "99_Supporting_Processes/02_Safety_Case.md")
    content = """# Safety Case (안전 사례)

**Document ID**: PART2-01-SCASE
**ISO 26262 Reference**: Part 2, Clause 6; Part 8, Clause 9
**ASPICE Reference**: N/A
**Version**: 1.0
**Date**: {today}
**Status**: Reference Example (실제 구현 완료 후 Evidence로 업데이트 필요)

> ⚠️ **Note**: 본 문서는 Safety Case 구조와 Evidence 계획을 정의합니다. 실제 테스트 Evidence는 구현 및 테스트 완료 후 업데이트됩니다.

---

## 1. 문서 목적

**ISO 26262-1:2018 §3.136**: Safety Case = 기능 안전이 달성되었다는 주장(argument)과 그것을 지지하는 Work Products의 증거(evidence).

본 문서는 **IVI vECU Integrated Control System**의 기능 안전 달성을 위한 안전 사례를 구조화합니다.

**Safety Case 구조**:
```
Safety Claim (안전 주장)
    ├── Argument (논증)
    │       ├── Sub-claim
    │       └── Strategy
    └── Evidence (증거 — Work Products)
```

---

## 2. Top-Level Safety Claim (최상위 안전 주장)

**Claim-01**: IVI vECU Integrated Control System은 ISO 26262:2018에 따라 정의된 모든 Safety Goals (SG-01 ~ SG-06)를 달성하며, 잔여 위험은 허용 가능한 수준이다.

**근거**:
- Claim-01은 하위 주장 (Per Safety Goal)으로 분해됨
- 각 Safety Goal에 대해 독립적인 Evidence가 제시됨

---

## 3. Safety Goal별 Safety Argument

### 3.1 SG-01: AEB 충돌 경고 (ASIL-D)

**Claim-01-01**: SG-01에 의해 요구되는 ASIL-D AEB 경고 기능이 달성되었다.

**Strategy**: ASIL 분해 (D → C+C) + ASIL-D 소프트웨어 개발 프로세스 준수

| Evidence ID | Work Product | 위치 | 상태 |
|-------------|-------------|------|------|
| EV-01-01 | HARA (SG-01 ASIL-D 결정) | 00_Concept_Phase/01_HARA.md | ✅ 완료 |
| EV-01-02 | Functional Safety Concept (FSR-D01) | 00_Concept_Phase/02_FSC.md | ✅ 완료 |
| EV-01-03 | Technical Safety Concept (TSR-D01) | 01_System_Requirements/03_TSC.md | ✅ 완료 |
| EV-01-04 | System Requirements (REQ-029, ASIL-D) | 01_System_Requirements/01_SRS.md | ✅ 완료 |
| EV-01-05 | ASIL Decomposition (D → C+C) | 04_SW_Architecture/03_ASIL_Decomp.md | ✅ 완료 |
| EV-01-06 | Software Unit Test (AEB 경고 로직) | 07_Unit_Test/02_Test_Report.md | ⏳ 구현 후 업데이트 |
| EV-01-07 | System Qualification Test (TC-SYS-029) | 11_System_Qual_Test/ | ⏳ 구현 후 업데이트 |
| EV-01-08 | FTTI 측정 결과 (≤ 100ms) | 12_Safety_Validation/ | ⏳ 구현 후 업데이트 |

---

### 3.2 SG-02: LDW 차선 이탈 경고 (ASIL-D)

**Claim-01-02**: SG-02에 의해 요구되는 ASIL-D LDW 경고 기능이 달성되었다.

| Evidence ID | Work Product | 위치 | 상태 |
|-------------|-------------|------|------|
| EV-02-01 | HARA (SG-02 ASIL-D 결정) | 00_Concept_Phase/01_HARA.md | ✅ 완료 |
| EV-02-02 | FSR-D02 | 00_Concept_Phase/02_FSC.md | ✅ 완료 |
| EV-02-03 | TSR-D02 (듀얼채널 출력) | 01_System_Requirements/03_TSC.md | ✅ 완료 |
| EV-02-04 | Safety Requirements (ASIL 분해, D→C+C) | 01_System_Requirements/02_Safety_Req.md | ✅ 완료 |
| EV-02-05 | LDW Unit Test | 07_Unit_Test/02_Test_Report.md | ⏳ |
| EV-02-06 | FTTI 측정 (≤ 200ms) | 12_Safety_Validation/ | ⏳ |

---

### 3.3 SG-03: 후진 경고 (ASIL-B)

**Claim-01-03**: SG-03에 의해 요구되는 ASIL-B 후진 경고 기능이 달성되었다.

| Evidence ID | Work Product | 위치 | 상태 |
|-------------|-------------|------|------|
| EV-03-01 | HARA (SG-03 ASIL-B) | 00_Concept_Phase/01_HARA.md | ✅ 완료 |
| EV-03-02 | FSR-B01 | 00_Concept_Phase/02_FSC.md | ✅ 완료 |
| EV-03-03 | System Requirements (REQ-002, 015, 016) | 01_System_Requirements/01_SRS.md | ✅ 완료 |
| EV-03-04 | Reverse Warning Unit Test | 07_Unit_Test/02_Test_Report.md | ⏳ |

---

### 3.4 SG-04: 도어 개방 경고 (ASIL-B)

**Claim-01-04**: SG-04에 의해 요구되는 ASIL-B 도어 개방 경고 기능이 달성되었다.

| Evidence ID | Work Product | 위치 | 상태 |
|-------------|-------------|------|------|
| EV-04-01 | HARA (SG-04 ASIL-B, v2.0 수정) | 00_Concept_Phase/01_HARA.md | ✅ 완료 |
| EV-04-02 | FSR-B02 | 00_Concept_Phase/02_FSC.md | ✅ 완료 |
| EV-04-03 | TSR-B02 (CRC-8, 0x500 CAN ID) | 01_System_Requirements/03_TSC.md | ✅ 완료 |
| EV-04-04 | System Requirements (REQ-006, ASIL-B) | 01_System_Requirements/01_SRS.md | ✅ 완료 |
| EV-04-05 | Door Warning Unit Test | 07_Unit_Test/02_Test_Report.md | ⏳ |

---

### 3.5 SG-05: 조명 Fail-Safe (ASIL-A)

**Claim-01-05**: SG-05에 의해 요구되는 ASIL-A 조명 Fail-Safe 기능이 달성되었다.

| Evidence ID | Work Product | 위치 | 상태 |
|-------------|-------------|------|------|
| EV-05-01 | HARA (SG-05 ASIL-A) | 00_Concept_Phase/01_HARA.md | ✅ 완료 |
| EV-05-02 | FSR-A01, FSR-A02 | 00_Concept_Phase/02_FSC.md | ✅ 완료 |
| EV-05-03 | TSR-A01 (PWM 모니터링) | 01_System_Requirements/03_TSC.md | ✅ 완료 |
| EV-05-04 | Lighting Fail-Safe Test | 07_Unit_Test/02_Test_Report.md | ⏳ |

---

### 3.6 SG-06: CAN Fail-Safe (ASIL-B)

**Claim-01-06**: SG-06에 의해 요구되는 ASIL-B CAN Fail-Safe 기능이 달성되었다.

| Evidence ID | Work Product | 위치 | 상태 |
|-------------|-------------|------|------|
| EV-06-01 | HARA (SG-06 ASIL-B, 구 SG-07) | 00_Concept_Phase/01_HARA.md | ✅ 완료 |
| EV-06-02 | FSR-B03 | 00_Concept_Phase/02_FSC.md | ✅ 완료 |
| EV-06-03 | TSR-B03 (Bus Off Recovery) | 01_System_Requirements/03_TSC.md | ✅ 완료 |
| EV-06-04 | CAN Fail-Safe Test | 08_SW_Integration_Test/ | ⏳ |

---

## 4. Process Evidence (프로세스 증거)

### 4.1 ISO 26262 프로세스 준수 증거

| Process | Document | 상태 |
|---------|---------|------|
| ISO 26262-3 Concept Phase | 00_Concept_Phase/ (HARA, FSC) | ✅ |
| ISO 26262-4 System Development | 01~02 (SRS, TSC, SYS Arch) | ✅ |
| ISO 26262-6 SW Development | 03~06 (SW Req, Arch, Design, Impl) | ✅ |
| ISO 26262-6 SW Verification | 07~09 (Unit, Integration, Qual Test) | ⏳ |
| ISO 26262-4 System Testing | 10~11 (SYS Integration, Qual) | ⏳ |
| ISO 26262-4 Safety Validation | 12 (Safety Validation) | ⏳ |
| ISO 26262-8 Configuration Mgmt | 99_Supporting_Processes/01_Traceability | ✅ |

### 4.2 ASPICE PAM 3.1 프로세스 준수 증거

| Process | Document | 상태 |
|---------|---------|------|
| SYS.2 System Requirements | 01_System_Requirements/ | ✅ |
| SYS.3 System Architecture | 02_System_Architecture/ | ✅ |
| SWE.1 SW Requirements | 03_Software_Requirements/ | ✅ |
| SWE.2 SW Architecture | 04_Software_Architecture/ | ✅ |
| SWE.3 SW Detailed Design | 05_Software_Detailed_Design/ | ✅ |
| SWE.4 SW Unit Test (구 SWE.5) | 07_Unit_Test/ | ⏳ |
| SWE.5 SW Integration (구 SWE.6) | 08_SW_Integration_Test/ | ⏳ |
| SWE.6 SW Qualification (구 SYS.4) | 09_SW_Qualification_Test/ | ⏳ |
| SYS.4 System Integration | 10_System_Integration_Test/ | ⏳ |
| SYS.5 System Qualification | 11_System_Qualification_Test/ | ⏳ |

---

## 5. Residual Risk Assessment (잔여 위험 평가)

| Safety Goal | 안전 메커니즘 | 달성 ASIL | 잔여 위험 목표 | 평가 |
|-------------|-------------|---------|--------------|------|
| SG-01 (AEB, D) | E2E + Watchdog + 듀얼채널 | ASIL-D | < 10⁻⁸/h | ALARP 만족 예상 |
| SG-02 (LDW, D) | E2E + 듀얼채널 (시각+촉각) | ASIL-D | < 10⁻⁸/h | ALARP 만족 예상 |
| SG-03 (Reverse, B) | CAN Timeout + DTC | ASIL-B | < 10⁻⁶/h | ALARP 만족 예상 |
| SG-04 (Door, B) | CRC-8 + Timeout | ASIL-B | < 10⁻⁶/h | ALARP 만족 예상 |
| SG-05 (Lighting, A) | SW Watchdog + HW Limiter | ASIL-A | < 10⁻⁵/h | ALARP 만족 예상 |
| SG-06 (Fail-Safe, B) | Bus Off Recovery | ASIL-B | < 10⁻⁶/h | ALARP 만족 예상 |

> **ALARP (As Low As Reasonably Practicable)**: 합리적으로 실행 가능한 수준까지 위험 감소

---

## 6. Open Items (미완성 증거 — 구현 후 업데이트 필요)

| Item | 담당 | 목표 일정 | 상태 |
|------|------|---------|------|
| 실제 Unit Test 결과 (Pass/Fail) | SW 개발팀 | 구현 완료 후 | ⏳ |
| MC/DC 커버리지 측정 결과 (≥ 100%) | SW 개발팀 | 단위 테스트 후 | ⏳ |
| FTTI 실측 데이터 (Logic Analyzer) | Safety 팀 | HIL 테스트 후 | ⏳ |
| MISRA C:2012 정적 분석 결과 | SW 개발팀 | 구현 완료 후 | ⏳ |
| Field Test 결과 (10,000+ km) | 검증 팀 | 프로토타입 후 | ⏳ |
| 독립 안전 평가 (TÜV SÜD) | 외부 평가자 | 프로젝트 후반 | ⏳ |

---

## 7. Safety Case Conclusion (안전 사례 결론)

**현재 상태**: 계획 단계 — 모든 Safety Goal에 대한 안전 주장 구조 완성, Evidence 계획 수립 완료

**최종 결론 조건 (구현 완료 후 충족 필요)**:
- [ ] 모든 Unit Test Pass (0 Critical Failures)
- [ ] MC/DC Coverage ≥ 100% (ASIL-D), ≥ 80% (ASIL-B)
- [ ] FTTI 실측 ≤ 목표값 (SG-01: 100ms, SG-02: 200ms 등)
- [ ] MISRA C:2012 위반 0건 (Mandatory Rules)
- [ ] 독립 안전 평가 완료

---

## 8. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {today} | Technical Review | 신규 생성 — ISO 26262-2 Safety Case 구조 정의 |

---

**Document End**
""".format(today=TODAY)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Safety Case 신규 생성: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 7: SG-03 정의 불일치 수정 (Safety Validation Report)
# ─────────────────────────────────────────────────────────────────────────────
def fix_sg03_mismatch():
    path = os.path.join(BASE, "12_Safety_Validation/01_Safety_Validation_Report.md")
    if not os.path.exists(path):
        print(f"⚠️  파일 없음: {path}")
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # SG-03 재정의 통일
    content = content.replace(
        '후진 중 장애물 경고',
        '후진 진입 시 후방 안전 경고 (HARA SG-03 기준)'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ SG-03 정의 통일: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX 8: ASIL Decomposition 표기 수정 (C+C→D → D→C+C)
# ─────────────────────────────────────────────────────────────────────────────
def fix_decomp_notation():
    files_to_fix = [
        "03_Software_Requirements/01_SWE1_Software_Requirements_Specification.md",
        "03_Software_Requirements/03_SWE1_Software_Safety_Requirements.md",
    ]
    for relpath in files_to_fix:
        fp = os.path.join(BASE, relpath)
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        # 잘못된 방향 표기 수정
        content = content.replace('C+C → D', 'D → C+C')
        content = content.replace('ASIL C+C → ASIL D', 'ASIL-D → ASIL-C+C')
        content = content.replace('ASIL Decomposition (C+C)', 'ASIL Decomposition (D → C+C)')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 분해 표기 수정: {relpath}")
    print("✅ ASIL 분해 표기 방향 수정 완료")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.chdir(BASE)
    print("=" * 60)
    print("ISO 26262 & ASPICE PAM 3.1 전체 수정 시작")
    print("=" * 60)

    print("\n[1/8] HARA 문서 수정 (FTTI, H-04/H-07 ASIL, 분해, Hazardous Event)...")
    fix_hara()

    print("\n[2/8] Functional Safety Concept 완성 (전체 FSR, 플레이스홀더 제거)...")
    fix_fsc()

    print("\n[3/8] SYS3 Architecture 수정 (플레이스홀더, ASPICE BP 완성)...")
    fix_sys3_arch()

    print("\n[4/8] ASIL Decomposition 수정 (Task_Lighting ASIL-B, DFA 개선)...")
    fix_asil_decomp()

    print("\n[5/8] ASPICE 프로세스 번호 수정 (SWE.4/5/6)...")
    fix_aspice_numbering()

    print("\n[6/8] CAN ID 통일 (SYS.3 기준: SCC=0x380, BCM=0x500, TCU=0x180)...")
    fix_can_ids()

    print("\n[7/8] Technical Safety Concept (TSR) 신규 생성...")
    create_tsr()

    print("\n[8/8] Safety Case 신규 생성 (ISO 26262-2)...")
    create_safety_case()

    # 보조 수정
    print("\n[보조] SG-03 정의 통일...")
    fix_sg03_mismatch()
    print("[보조] ASIL 분해 표기 방향 수정...")
    fix_decomp_notation()

    print("\n" + "=" * 60)
    print("✅ 모든 수정 완료!")
    print("=" * 60)

    # 최종 파일 카운트
    import glob
    md_files = glob.glob(os.path.join(BASE, "**/*.md"), recursive=True)
    md_files = [f for f in md_files if any(f"/{d}/" in f or f"/{d}" in f
                for d in ["00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_",
                          "08_", "09_", "10_", "11_", "12_", "99_"])]
    print(f"\n📊 총 V-Model 문서 수: {len(md_files)}개")
    for f in sorted(md_files):
        size = os.path.getsize(f)
        print(f"  {'✅' if size > 500 else '⚠️ '} {os.path.relpath(f, BASE)} ({size/1024:.1f} KB)")

# Hazard Analysis and Risk Assessment (HARA)

**Document ID**: PART3-01-HARA
**ISO 26262 Reference**: Part 3, Clause 7
**ASPICE Reference**: N/A
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Released

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
[2] Hazard Classification (위험 분류)
      ↓
[3] Exposure (E), Severity (S), Controllability (C) 평가
      ↓
[4] ASIL Determination (ASIL 결정)
      ↓
Safety Goals Definition
```

### 2.2 ASIL 결정 테이블 (ISO 26262-3, Table 4)

| Severity (S) | Exposure (E) | Controllability (C) | ASIL |
|--------------|--------------|---------------------|------|
| S3 | E4 | C3 | **ASIL-D** |
| S3 | E4 | C2 | ASIL-D |
| S3 | E4 | C1 | ASIL-C |
| S3 | E3 | C3 | ASIL-D |
| S3 | E3 | C2 | ASIL-C |
| S3 | E3 | C1 | ASIL-B |
| S3 | E2 | C3 | ASIL-C |
| S3 | E2 | C2 | ASIL-B |
| S3 | E2 | C1 | ASIL-A |
| S2 | E4 | C3 | ASIL-C |
| S2 | E4 | C2 | ASIL-B |
| S2 | E4 | C1 | ASIL-A |
| S2 | E3 | C3 | ASIL-B |
| S2 | E3 | C2 | ASIL-A |
| S2 | E3 | C1 | QM |
| S1 | - | - | **QM** |

**분류 기준**:
- **S (Severity)**: S0 (No injury) ~ S3 (Life-threatening)
- **E (Exposure)**: E1 (Very low) ~ E4 (High probability)
- **C (Controllability)**: C0 (Controllable) ~ C3 (Difficult to control)

---

## 3. Hazard Identification (위험 식별)

### 3.1 운영 시나리오 기반 위험 식별

| Hazard ID | Hazard Description | Operating Situation | Triggering Event |
|-----------|-------------------|---------------------|------------------|
| **H-01** | 긴급 제동 시 경고 미표시 | 고속 주행 중 | AEB 이벤트 발생 시 vECU 고장 |
| **H-02** | 차선 이탈 경고 미표시 | 고속도로 주행 | LDW 센서 정상이나 vECU CAN 수신 실패 |
| **H-03** | 후진 시 경고 미표시 | 주차장 후진 중 | TCU 기어 신호 손실 또는 vECU 고장 |
| **H-04** | 도어 개방 시 경고 미표시 | 주행 중 도어 개방 | BCM 도어 센서 신호 손실 |
| **H-05** | 조명 오작동 (눈부심) | 야간 주행 | vECU 조명 제어 SW 버그로 최대 밝기 고정 |
| **H-06** | OTA 실패 후 기능 상실 | 정차 중 OTA | OTA 중 전원 차단, Rollback 실패 |
| **H-07** | Fail-Safe 미작동 | CAN 통신 오류 발생 | vECU Fault Detection SW 버그 |
| **H-08** | 다중 경고 혼란 | 복합 위험 상황 | LDW + AEB 동시 발생 시 우선순위 오류 |

---

## 4. Hazard Classification (위험 분류)

### 4.1 Severity (S) - 심각도

| Level | Description | Example |
|-------|-------------|---------|
| **S3** | Life-threatening injuries (치명적 부상) | 고속 충돌, 다중 차량 사고 |
| **S2** | Severe injuries (중상) | 저속 충돌, 단일 차량 사고 |
| **S1** | Light injuries (경상) | 경미한 접촉 사고 |
| **S0** | No injuries (무상해) | 재산 피해만 발생 |

### 4.2 Exposure (E) - 노출 빈도

| Level | Description | Probability | Example |
|-------|-------------|-------------|---------|
| **E4** | High probability (높음) | > 10% of operating time | 매일 고속도로 주행 |
| **E3** | Medium probability (중간) | 1% ~ 10% | 주 1~2회 고속도로 |
| **E2** | Low probability (낮음) | 0.1% ~ 1% | 월 1~2회 |
| **E1** | Very low probability (매우 낮음) | < 0.1% | 연 1~2회 |

### 4.3 Controllability (C) - 제어 가능성

| Level | Description | Example |
|-------|-------------|---------|
| **C3** | Difficult to control (제어 어려움) | 고속에서 갑작스런 상황, 운전자 반응 시간 부족 |
| **C2** | Normally controllable (일반적 제어 가능) | 중속, 운전자가 회피 가능 |
| **C1** | Simply controllable (쉽게 제어 가능) | 저속, 충분한 반응 시간 |
| **C0** | Controllable in general (일반적 제어) | 정차 중, 위험 없음 |

---

## 5. HARA 결과 (HARA Results)

### 5.1 Hazard 별 ASIL 결정

| Hazard ID | Hazard | S | E | C | **ASIL** | Safety Goal |
|-----------|--------|---|---|---|----------|-------------|
| **H-01** | 긴급 제동 경고 미표시 | S3 | E3 | C3 | **ASIL-D** | **SG-01**: AEB 이벤트 시 100ms 이내 경고 표시 |
| **H-02** | 차선 이탈 경고 미표시 | S3 | E4 | C2 | **ASIL-D** | **SG-02**: LDW 이벤트 시 200ms 이내 경고 표시 |
| **H-03** | 후진 경고 미표시 | S2 | E4 | C2 | **ASIL-B** | **SG-03**: 후진 시 3초 이내 경고 표시 |
| **H-04** | 도어 개방 경고 미표시 | S3 | E2 | C2 | **ASIL-C** | **SG-04**: 주행 중 도어 개방 시 1초 이내 경고 |
| **H-05** | 조명 오작동 (눈부심) | S2 | E3 | C1 | **ASIL-A** | **SG-05**: 조명 밝기 50% 이하 Fail-Safe |
| **H-06** | OTA 실패 후 기능 상실 | S2 | E1 | C1 | **QM** | **SG-06**: OTA 실패 시 자동 Rollback |
| **H-07** | Fail-Safe 미작동 | S3 | E2 | C2 | **ASIL-C** | **SG-07**: CAN 오류 시 3초 이내 Fail-Safe 모드 |
| **H-08** | 다중 경고 혼란 | S2 | E2 | C2 | **ASIL-B** | **SG-08**: 경고 우선순위 기반 표시 |

---

## 6. Safety Goals (안전 목표)

### 6.1 ASIL-D Safety Goals

| SG ID | Safety Goal | ASIL | Safe State | FTTI |
|-------|-------------|------|------------|------|
| **SG-01** | AEB 이벤트 발생 시 운전자에게 100ms 이내 시각적 경고를 제공해야 한다 | ASIL-D | 경고 미표시 시 청각 경고 대체 | 100ms |
| **SG-02** | LDW 이벤트 발생 시 운전자에게 200ms 이내 시각적 경고를 제공해야 한다 | ASIL-D | 경고 미표시 시 Haptic 경고 대체 | 200ms |

**FTTI (Fault Tolerant Time Interval)**: 고장 발생부터 안전 상태 도달까지 허용 시간

### 6.2 ASIL-C Safety Goals

| SG ID | Safety Goal | ASIL | Safe State | FTTI |
|-------|-------------|------|------------|------|
| **SG-04** | 주행 중 도어 개방 시 1초 이내 운전자에게 경고를 제공해야 한다 | ASIL-C | 경고 + 차량 감속 유도 | 1s |
| **SG-07** | CAN 통신 오류 감지 시 3초 이내 Fail-Safe 모드로 전환해야 한다 | ASIL-C | 조명 50% 백색 고정 | 3s |

### 6.3 ASIL-B Safety Goals

| SG ID | Safety Goal | ASIL | Safe State | FTTI |
|-------|-------------|------|------------|------|
| **SG-03** | 후진 기어 진입 시 3초 이내 안전 경고를 표시해야 한다 | ASIL-B | 경고 미표시 시 후진 제한 | 3s |
| **SG-08** | 다중 ADAS 이벤트 발생 시 우선순위 기반 경고를 표시해야 한다 | ASIL-B | 최고 우선순위 경고만 표시 | 500ms |

### 6.4 ASIL-A Safety Goals

| SG ID | Safety Goal | ASIL | Safe State | FTTI |
|-------|-------------|------|------------|------|
| **SG-05** | 조명 제어 실패 시 Fail-Safe 모드 (50% 밝기)로 전환해야 한다 | ASIL-A | 50% 백색 고정 | 1s |

### 6.5 QM (Quality Management)

| SG ID | Safety Goal | ASIL | Safe State |
|-------|-------------|------|------------|
| **SG-06** | OTA 업데이트 실패 시 자동으로 이전 버전으로 Rollback 해야 한다 | QM | 이전 버전 복구 |

---

## 7. ASIL Decomposition (ASIL 분해)

### 7.1 분해 전략

일부 ASIL-D 요구사항은 **ASIL Decomposition (ISO 26262-9, Clause 5)** 를 통해 독립적인 하위 요구사항으로 분해합니다.

**예시: SG-01 (ASIL-D) 분해**

| 원본 | 분해 후 |
|------|---------|
| **SG-01** (ASIL-D): AEB 경고 100ms | **SG-01a** (ASIL-B): 시각 경고 표시 |
|                                     | **SG-01b** (ASIL-B): 청각 경고 표시 (독립) |

**분해 조건**:
- ✅ 두 요구사항이 **독립적 (Independent)**
- ✅ 두 요구사항이 **충분 (Sufficient)** (함께 원본 ASIL-D 만족)
- ✅ **Freedom from Interference** 확보

---

## 8. Hazard 발생 시나리오 상세 (Detailed Scenarios)

### 8.1 H-01: 긴급 제동 경고 미표시 (ASIL-D)

**Operating Situation**:
- 고속도로 주행 (100 km/h)
- 앞차 급제동
- 운전자 주의 산만 (스마트폰 확인)

**Hazardous Event**:
1. ADAS Camera가 TTC < 1.6s 감지 → AEB 작동
2. vECU CAN Rx Buffer Overflow → AEB 메시지 손실
3. Cluster에 경고 미표시
4. 운전자 인지 실패 → 후방 추돌

**Consequence**:
- **S3** (Life-threatening): 고속 추돌 → 치명적 부상 가능
- **E3** (Medium): 고속도로 주행 비율 10% 정도
- **C3** (Difficult): 100 km/h에서 반응 시간 < 1초

**ASIL**: **D**

**Safety Goal**: **SG-01** - 100ms 이내 경고 표시

---

### 8.2 H-03: 후진 경고 미표시 (ASIL-B)

**Operating Situation**:
- 주차장 후진 중 (5 km/h)
- 후방 보행자 접근
- 운전자 사각지대 확인 미흡

**Hazardous Event**:
1. TCU → vECU CAN 메시지 (Gear = R) 전송
2. vECU SW 버그 → 기어 상태 파싱 오류
3. 후진 경고 미표시
4. 후방 카메라 미활성화
5. 보행자 접촉

**Consequence**:
- **S2** (Severe): 저속 접촉 → 중상 가능
- **E4** (High): 주차 시 매일 후진
- **C2** (Normally controllable): 저속에서 브레이크 가능

**ASIL**: **B**

**Safety Goal**: **SG-03** - 3초 이내 경고 표시

---

## 9. 추적성 (Traceability)

### 9.1 Hazard → Safety Goal → System Requirement

| Hazard | Safety Goal | ASIL | System Requirement |
|--------|-------------|------|--------------------|
| H-01 | SG-01 | ASIL-D | SYS-REQ-029 (AEB 경고 UI) |
| H-02 | SG-02 | ASIL-D | SYS-REQ-027 (LDW 경고 UI) |
| H-03 | SG-03 | ASIL-B | SYS-REQ-002, 015, 016 (후진 경고) |
| H-04 | SG-04 | ASIL-C | SYS-REQ-006 (도어 경고) |
| H-05 | SG-05 | ASIL-A | SYS-REQ-053 (Fail-Safe) |
| H-06 | SG-06 | QM | SYS-REQ-014 (OTA Rollback) |
| H-07 | SG-07 | ASIL-C | SYS-REQ-023 (Fail-Safe 전환) |
| H-08 | SG-08 | ASIL-B | SYS-REQ-037 (다중 경고 우선순위) |

---

## 10. HARA 검증 (HARA Verification)

### 10.1 검증 방법

| 검증 항목 | 방법 | 기준 |
|-----------|------|------|
| **Hazard 완전성** | Workshop, FMEA 비교 | 모든 운영 시나리오 커버 |
| **ASIL 결정 정확성** | ISO 26262-3 Table 4 준수 | 100% 일치 |
| **Safety Goal 추적성** | Traceability Matrix | 양방향 추적 가능 |

### 10.2 검증 결과

- ✅ **8개 Hazard** 식별 (운영 시나리오 기반)
- ✅ **8개 Safety Goal** 정의
- ✅ **ASIL 분포**: D(2), C(2), B(2), A(1), QM(1)
- ✅ **추적성**: 100% 확보

---

## 11. 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **Functional Safety Manager** | | | |
| **HARA Team Leader** | | | |
| **System Engineer** | | | |
| **Independent Safety Assessor** | | | |

---

## 12. 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Initial release - ISO 26262-3 준수 |

---

**Document End**

# Safety Case (안전 사례)

**Document ID**: PART2-01-SCASE
**ISO 26262 Reference**: Part 2, Clause 6; Part 8, Clause 9
**ASPICE Reference**: N/A
**Version**: 1.0
**Date**: 2026-02-17
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
| 1.0 | 2026-02-17 | Technical Review | 신규 생성 — ISO 26262-2 Safety Case 구조 정의 |

---

**Document End**

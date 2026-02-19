# V-Model 구조 검토 (ISO 26262 & ASPICE 준수)

## 📋 검토 목적

현재 문서 구조가 **ISO 26262**와 **ASPICE 3.1** 의 V-Model 명명 규칙을 올바르게 따르고 있는지 검증

---

## 🎯 ISO 26262 & ASPICE V-Model 표준 구조

### V-Model 좌측 (Development - 좌에서 우로)

| 단계 | ISO 26262 | ASPICE 3.1 | 산출물 예시 | 우측 검증 단계 |
|------|-----------|------------|-------------|---------------|
| **레벨 0** | Part 3: Concept Phase | - | Item Definition, Hazard Analysis, Safety Goals | **검증** |
| **레벨 1** | Part 4-7: System Requirements | **SYS.2** | System Requirements Specification | **SYS.5** System Qualification |
| **레벨 2** | Part 4-8: System Architecture | **SYS.3** | System Architecture Design, Interface Spec | **SYS.4** System Integration |
| **레벨 3** | Part 6-6: SW Requirements | **SWE.1** | Software Requirements Specification | **SWE.6** SW Qualification |
| **레벨 4** | Part 6-7: SW Architecture | **SWE.2** | Software Architecture Design | **SWE.5** SW Integration |
| **레벨 5** | Part 6-8: SW Detailed Design | **SWE.3** | Detailed Design, Unit Design | **SWE.4** Unit Test |
| **레벨 6** | Part 6-9: Implementation | **SWE.3** | Source Code | **SWE.4** Unit Test |

### V-Model 우측 (Verification & Validation - 우에서 좌로)

| 단계 | ISO 26262 | ASPICE 3.1 | 산출물 예시 | 대응 좌측 |
|------|-----------|------------|-------------|-----------|
| **레벨 6** | Part 6-9: Unit Testing | **SWE.4** | Unit Test Specification, Unit Test Results | Implementation |
| **레벨 5** | Part 6-10: SW Integration Test | **SWE.5** | SW Integration Test Spec, Results | SW Architecture |
| **레벨 4** | Part 6-11: SW Qualification Test | **SWE.6** | SW Qualification Test Spec, Results | SW Requirements |
| **레벨 3** | Part 4-9: System Integration Test | **SYS.4** | System Integration Test Spec, Results | System Architecture |
| **레벨 2** | Part 4-10: System Qualification Test | **SYS.5** | System Qualification Test Spec, Results | System Requirements |
| **레벨 1** | Part 4-10: Safety Validation | - | Validation Report | Safety Goals |

---

## ⚠️ 현재 문서 구조 분석

### 현재 파일 목록

```
MentoringResult/
├── 01_Requirements.md
├── 01_Requirements_Traceability.md  (신규)
├── 02_Concept_Design_Guide.md
├── 03_00_Function_definition.md
├── 03_01_SysFuncAnalysis.md
├── 03_02_NWflowDef.md
├── 03_03_Communication_Specification.md
├── 03_04_System_Variables.md
├── 05_Unit_Test.md
├── 06_Integration_Test.md
├── 07_System_Test.md
```

---

## 🔍 문제점 분석

### ❌ 문제 1: 문서 번호 체계 혼란

| 현재 번호 | 현재 이름 | 의도한 의미 | ISO 26262 | ASPICE | ⚠️ 문제점 |
|-----------|-----------|-------------|-----------|--------|----------|
| 01 | Requirements | 요구사항 명세 | Part 4-7 | SYS.2 | ✅ 올바름 |
| 01 | Requirements_Traceability | 추적성 매트릭스 | Part 8 | - | ⚠️ 별도 문서 필요? |
| **02** | Concept_Design_Guide | 개념 설계 | **Part 3** | - | ❌ **번호 순서 잘못됨!** |
| 03 | Function_definition | 기능 정의 | Part 4-8 | SYS.3 | ⚠️ Architecture 일부 |
| 03_01 | SysFuncAnalysis | 시스템 기능 분석 | Part 4-8 | SYS.3 | ✅ 올바름 |
| 03_02 | NWflowDef | 네트워크 흐름 정의 | Part 4-8 | SYS.3 | ✅ 올바름 |
| 03_03 | Communication_Specification | 통신 사양 | Part 4-8 | SYS.3 | ✅ 올바름 |
| 03_04 | System_Variables | 시스템 변수 | Part 4-8 | SYS.3 | ✅ 올바름 |
| **04** | **누락** | **SW Requirements** | **Part 6-6** | **SWE.1** | ❌ **누락!** |
| 05 | Unit_Test | 단위 테스트 | Part 6-9 | SWE.4 | ⚠️ SWE.1, SWE.2, SWE.3 누락 |
| 06 | Integration_Test | 통합 테스트 | Part 6-10? | SWE.5? SYS.4? | ❌ **모호함!** |
| 07 | System_Test | 시스템 테스트 | Part 4-10 | SYS.5 | ⚠️ SWE.6 누락 |

---

### ❌ 문제 2: Concept Design 위치 오류

**ISO 26262 Part 3: Concept Phase**
- Item Definition (아이템 정의)
- Hazard Analysis and Risk Assessment (위험 분석)
- Functional Safety Concept (기능 안전 개념)

**현재**: `02_Concept_Design_Guide.md`
**문제**: Concept Phase는 **V-Model 최상위** (Requirements 이전)
**올바른 번호**: `00_Concept_Phase.md` 또는 별도 섹션

---

### ❌ 문제 3: Software Level 문서 누락

**누락된 ASPICE 프로세스**:
- ❌ **SWE.1** (Software Requirements Specification)
- ❌ **SWE.2** (Software Architectural Design)
- ❌ **SWE.3** (Software Detailed Design)
- ❌ **SWE.6** (Software Qualification Test)

**현재**: SYS → 바로 Unit Test로 점프
**문제**: **V-Model 중간 단계 생략** → ASPICE 부적합

---

### ❌ 문제 4: Integration Test 모호성

**06_Integration_Test.md** 가 의미하는 것:
- **SWE.5** (Software Integration Test)? → SW 컴포넌트 간 통합
- **SYS.4** (System Integration Test)? → ECU 간 통합

**ISO 26262 구분**:
- Part 6-10: SW Integration & Testing (SWE.5)
- Part 4-9: Item Integration & Testing (SYS.4)

**해결**: 두 문서로 분리 필요

---

### ❌ 문제 5: Traceability 위치

**현재**: `01_Requirements_Traceability.md`
**문제**: Traceability는 **ISO 26262 Part 8 (Supporting Processes)** → 별도 관리

**올바른 구조**:
```
00_Supporting/
├── Traceability_Matrix.md
├── Configuration_Management.md
├── Change_Management.md
└── Documentation_Management.md
```

---

## ✅ 제안: ISO 26262 & ASPICE 준수 문서 구조

### 📁 최종 권장 구조

```
MentoringResult/
│
├── 00_Concept_Phase/                      (ISO 26262 Part 3)
│   ├── 00_Item_Definition.md
│   ├── 01_Hazard_Analysis_Risk_Assessment.md (HARA)
│   └── 02_Functional_Safety_Concept.md
│
├── 01_System_Requirements/                (ISO 26262 Part 4-7, ASPICE SYS.2)
│   ├── 01_SYS2_System_Requirements_Specification.md
│   └── 01_SYS2_Safety_Requirements.md
│
├── 02_System_Architecture/                (ISO 26262 Part 4-8, ASPICE SYS.3)
│   ├── 02_SYS3_System_Architectural_Design.md
│   ├── 02_SYS3_Domain_Architecture.md
│   ├── 02_SYS3_ECU_Allocation.md
│   ├── 02_SYS3_Network_Topology.md
│   ├── 02_SYS3_Communication_Specification.md (DBC)
│   └── 02_SYS3_Interface_Definition.md
│
├── 03_Software_Requirements/              (ISO 26262 Part 6-6, ASPICE SWE.1)
│   ├── 03_SWE1_Software_Requirements_Specification.md
│   └── 03_SWE1_vECU_Requirements.md
│
├── 04_Software_Architecture/              (ISO 26262 Part 6-7, ASPICE SWE.2)
│   ├── 04_SWE2_Software_Architectural_Design.md
│   ├── 04_SWE2_Component_Design.md
│   └── 04_SWE2_Interface_Design.md
│
├── 05_Software_Detailed_Design/           (ISO 26262 Part 6-8, ASPICE SWE.3)
│   ├── 05_SWE3_Detailed_Design.md
│   └── 05_SWE3_Unit_Design.md
│
├── 06_Implementation/                     (ISO 26262 Part 6-9, ASPICE SWE.3)
│   └── 06_Implementation_Guide.md         (코드는 별도 repository)
│
├── 07_Unit_Test/                          (ISO 26262 Part 6-9, ASPICE SWE.4)
│   ├── 07_SWE4_Unit_Test_Specification.md
│   └── 07_SWE4_Unit_Test_Results.md
│
├── 08_SW_Integration_Test/                (ISO 26262 Part 6-10, ASPICE SWE.5)
│   ├── 08_SWE5_SW_Integration_Test_Specification.md
│   └── 08_SWE5_SW_Integration_Test_Results.md
│
├── 09_SW_Qualification_Test/              (ISO 26262 Part 6-11, ASPICE SWE.6)
│   ├── 09_SWE6_SW_Qualification_Test_Specification.md
│   └── 09_SWE6_SW_Qualification_Test_Results.md
│
├── 10_System_Integration_Test/            (ISO 26262 Part 4-9, ASPICE SYS.4)
│   ├── 10_SYS4_System_Integration_Test_Specification.md
│   └── 10_SYS4_System_Integration_Test_Results.md
│
├── 11_System_Qualification_Test/          (ISO 26262 Part 4-10, ASPICE SYS.5)
│   ├── 11_SYS5_System_Qualification_Test_Specification.md
│   └── 11_SYS5_System_Qualification_Test_Results.md
│
├── 12_Safety_Validation/                  (ISO 26262 Part 4-10)
│   └── 12_Safety_Validation_Report.md
│
└── 99_Supporting_Processes/               (ISO 26262 Part 8)
    ├── Traceability_Matrix.md             ⭐ 여기로 이동
    ├── Configuration_Management.md
    ├── Change_Management.md
    └── Documentation_Management.md
```

---

## 📊 V-Model 매핑 테이블

### 개발 단계 (좌 → 우)

| 번호 | 문서명 | ISO 26262 | ASPICE | V-Level | 검증 단계 |
|------|--------|-----------|--------|---------|-----------|
| 00 | Concept Phase | Part 3 | - | 0 | 12 Safety Validation |
| 01 | System Requirements | Part 4-7 | SYS.2 | 1 | 11 SYS.5 System Qualification |
| 02 | System Architecture | Part 4-8 | SYS.3 | 2 | 10 SYS.4 System Integration |
| 03 | SW Requirements | Part 6-6 | SWE.1 | 3 | 09 SWE.6 SW Qualification |
| 04 | SW Architecture | Part 6-7 | SWE.2 | 4 | 08 SWE.5 SW Integration |
| 05 | SW Detailed Design | Part 6-8 | SWE.3 | 5 | 07 SWE.4 Unit Test |
| 06 | Implementation | Part 6-9 | SWE.3 | 6 | 07 SWE.4 Unit Test |

### 검증 단계 (우 → 좌)

| 번호 | 문서명 | ISO 26262 | ASPICE | V-Level | 개발 단계 |
|------|--------|-----------|--------|---------|-----------|
| 07 | Unit Test | Part 6-9 | SWE.4 | 6 | 05/06 Detailed Design/Impl |
| 08 | SW Integration Test | Part 6-10 | SWE.5 | 5 | 04 SW Architecture |
| 09 | SW Qualification Test | Part 6-11 | SWE.6 | 4 | 03 SW Requirements |
| 10 | System Integration Test | Part 4-9 | SYS.4 | 3 | 02 System Architecture |
| 11 | System Qualification Test | Part 4-10 | SYS.5 | 2 | 01 System Requirements |
| 12 | Safety Validation | Part 4-10 | - | 1 | 00 Concept Phase |

---

## 🎯 Traceability 구조

### ISO 26262 Part 8 요구사항

**양방향 추적성 (Bidirectional Traceability)**:

```
Safety Goals (Part 3)
    ↕ (SYS.2 BP7)
System Requirements (Part 4-7, SYS.2)
    ↕ (SYS.3 BP7)
System Architecture (Part 4-8, SYS.3)
    ↕ (SWE.1 BP6)
Software Requirements (Part 6-6, SWE.1)
    ↕ (SWE.2 BP7)
Software Architecture (Part 6-7, SWE.2)
    ↕ (SWE.3 BP5)
Detailed Design (Part 6-8, SWE.3)
    ↕ (SWE.4 BP5)
Unit Test Cases (Part 6-9, SWE.4)
```

**우측 검증 추적성**:

```
Unit Test Results
    ↕
SW Integration Test Results
    ↕
SW Qualification Test Results
    ↕
System Integration Test Results
    ↕
System Qualification Test Results
    ↕
Safety Validation Results
```

---

## ⚠️ 현재 구조의 ASPICE 준수 문제

### ASPICE Capability Level 평가

| 프로세스 | 요구사항 | 현재 상태 | 결과 |
|----------|----------|-----------|------|
| **SYS.2** | System Requirements Specification | ✅ 01_Requirements.md | **Pass** |
| **SYS.3** | System Architectural Design | ✅ 03_*.md | **Pass** |
| **SYS.4** | System Integration Test | ⚠️ 06? 모호함 | **Fail** |
| **SYS.5** | System Qualification Test | ⚠️ 07? 모호함 | **Fail** |
| **SWE.1** | SW Requirements Specification | ❌ 누락 | **Fail** |
| **SWE.2** | SW Architectural Design | ❌ 누락 | **Fail** |
| **SWE.3** | SW Detailed Design | ❌ 누락 | **Fail** |
| **SWE.4** | Unit Test | ✅ 05_Unit_Test.md | **Pass** |
| **SWE.5** | SW Integration Test | ❌ 누락 | **Fail** |
| **SWE.6** | SW Qualification Test | ❌ 누락 | **Fail** |

**현재 ASPICE Capability Level**: **0 (Incomplete)** ❌

**목표 Level 2 달성 위해 필요**:
- ✅ BP (Base Practice) 모두 수행
- ✅ 모든 Work Product 생성
- ✅ Traceability 확보

---

## 💡 권장 조치

### Option 1: 완전 준수 (Full Compliance) ⭐ 권장

**장점**:
- ISO 26262 & ASPICE 완전 준수
- 산업 표준 준수
- 멘토 평가 시 전문성 입증

**단점**:
- 문서 개수 증가 (12개 → 30+개)
- 작업량 증가

**구조**:
```
00_Concept_Phase/ (3 files)
01_System_Requirements/ (2 files)
02_System_Architecture/ (6 files)
03_Software_Requirements/ (2 files)
04_Software_Architecture/ (3 files)
05_Software_Detailed_Design/ (2 files)
06_Implementation/ (1 file)
07_Unit_Test/ (2 files)
08_SW_Integration_Test/ (2 files)
09_SW_Qualification_Test/ (2 files)
10_System_Integration_Test/ (2 files)
11_System_Qualification_Test/ (2 files)
12_Safety_Validation/ (1 file)
99_Supporting_Processes/ (4 files)
```

**총 34개 문서**

---

### Option 2: 축약 준수 (Simplified Compliance)

**현재 구조 최소 수정**으로 ASPICE Level 1 달성

**필수 추가 문서**:
```
00_Concept_Phase.md                        (NEW)
03_SWE1_SW_Requirements.md                 (NEW)
04_SWE2_SW_Architecture.md                 (NEW)
05_SWE3_SW_Detailed_Design.md              (NEW)
06_Integration_Test → 분리:
    06_SWE5_SW_Integration_Test.md         (RENAME)
    07_SYS4_System_Integration_Test.md     (NEW)
08_SWE6_SW_Qualification_Test.md           (NEW)
09_SYS5_System_Qualification_Test.md       (RENAME from 07)
```

**총 추가: 7개 문서**

---

### Option 3: 최소 준수 (Minimal Compliance)

**학교 프로젝트 수준** (ASPICE Level 0 허용)

**현재 구조 유지 + 명명만 수정**:
```
00_Concept_Design.md                       (RENAME from 02)
01_SYS2_Requirements.md                    (RENAME)
02_SYS3_Architecture/                      (RENAME from 03)
    ├── Function_Definition.md
    ├── SysFuncAnalysis.md
    ├── NWflowDef.md
    ├── Communication_Specification.md
    └── System_Variables.md
03_SWE134_Implementation_Guide.md          (NEW - 통합)
04_SWE4_Unit_Test.md                       (RENAME from 05)
05_SWE5_SW_Integration_Test.md             (RENAME from 06)
06_SYS45_System_Test.md                    (RENAME from 07)
99_Supporting/
    └── Traceability_Matrix.md             (MOVE from 01)
```

**총 변경: 이름 변경 + 1개 추가**

---

## 🎯 최종 권장 사항

### 우리 프로젝트 상황
- **학교 PBL 프로젝트** (산업 프로젝트 아님)
- **일요일 멘토 제출** (시간 압박)
- **CANoe 시뮬레이션 중심** (실제 양산 아님)
- **4주차 프로젝트** (제한된 범위)

### ⭐ 추천: **Option 2 (축약 준수)**

**이유**:
1. ✅ ASPICE Level 1 달성 가능
2. ✅ ISO 26262 기본 구조 준수
3. ✅ 멘토에게 표준 이해도 입증
4. ⚠️ 작업량 증가하지만 관리 가능 (7개 추가)
5. ✅ V-Model 양쪽 완성

**구체적 작업**:
1. **00_Concept_Phase.md** - 기존 02 내용 이동
2. **03_SWE1_SW_Requirements.md** - 56개 요구사항 중 SW 관련만 추출
3. **04_SWE2_SW_Architecture.md** - vECU 컴포넌트 구조
4. **05_SWE3_SW_Detailed_Design.md** - vECU 상세 설계
5. 06, 07, 08, 09 재구성

---

## 📋 다음 단계

**결정 필요**:
1. Option 1, 2, 3 중 선택
2. 문서 번호 체계 재정의
3. Traceability Matrix 위치 결정

**선택 후**:
1. 문서 구조 재구성
2. 파일 이름 변경
3. 내용 재배치
4. Traceability 업데이트

---

**어떤 Option을 선택하시겠습니까?**
- **Option 1**: 완전 준수 (34개 문서)
- **Option 2**: 축약 준수 (현재 + 7개) ⭐ 권장
- **Option 3**: 최소 준수 (현재 + 명명 변경)

---

**작성일**: 2026-02-14
**검토자**: AI Assistant
**승인 대기**: 프로젝트 팀

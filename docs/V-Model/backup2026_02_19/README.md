# V-Model 완전 준수 문서 구조

**프로젝트**: IVI vECU Integrated Control System
**기준**: ISO 26262-6:2018 & ASPICE 3.1
**생성일**: 2026-02-14
**문서 개수**: 34개
**상태**: 진행 중

---

## 📋 문서 구조 개요

본 폴더는 **ISO 26262**와 **ASPICE 3.1**을 완전 준수하는 V-Model 기반 문서 구조입니다.

```
V-Model 좌측 (Development)          V-Model 우측 (Verification)
┌────────────────────┐              ┌────────────────────┐
│ 00 Concept Phase   │◄────────────►│ 12 Safety Valid.   │
├────────────────────┤              ├────────────────────┤
│ 01 SYS.2 (SYS Req) │◄────────────►│ 11 SYS.5 (SYS Qual)│
├────────────────────┤              ├────────────────────┤
│ 02 SYS.3 (SYS Arc) │◄────────────►│ 10 SYS.4 (SYS Int) │
├────────────────────┤              ├────────────────────┤
│ 03 SWE.1 (SW Req)  │◄────────────►│ 09 SWE.6 (SW Qual) │
├────────────────────┤              ├────────────────────┤
│ 04 SWE.2 (SW Arc)  │◄────────────►│ 08 SWE.5 (SW Int)  │
├────────────────────┤              ├────────────────────┤
│ 05 SWE.3 (Detail)  │◄────────────►│ 07 SWE.4 (Unit)    │
├────────────────────┤              └────────────────────┘
│ 06 Implementation  │
└────────────────────┘

99 Supporting Processes (Traceability, Config, Change, Doc Management)
```

---

## 📂 폴더 구조

### 00_Concept_Phase (ISO 26262 Part 3)
- ✅ `00_Item_Definition.md` - Item 정의, 범위, 인터페이스
- ✅ `01_Hazard_Analysis_Risk_Assessment.md` - HARA, ASIL 결정
- ⬜ `02_Functional_Safety_Concept.md` - Safety Goals, Safety Requirements

### 01_System_Requirements (ISO 26262 Part 4-7, ASPICE SYS.2)
- ⬜ `01_SYS2_System_Requirements_Specification.md` - 시스템 요구사항 (56개)
- ⬜ `02_SYS2_Safety_Requirements.md` - 안전 요구사항 (ASIL 기반)

### 02_System_Architecture (ISO 26262 Part 4-8, ASPICE SYS.3)
- ⬜ `01_SYS3_System_Architectural_Design.md` - 시스템 아키텍처 개요
- ⬜ `02_SYS3_Domain_Architecture.md` - 5개 Domain 구조
- ⬜ `03_SYS3_ECU_Allocation.md` - 23개 ECU 할당
- ⬜ `04_SYS3_Network_Topology.md` - CAN 네트워크 토폴로지
- ⬜ `05_SYS3_Communication_Specification.md` - DBC 기반 통신 규격
- ⬜ `06_SYS3_Interface_Definition.md` - ECU 간 인터페이스

### 03_Software_Requirements (ISO 26262 Part 6-6, ASPICE SWE.1)
- ⬜ `01_SWE1_Software_Requirements_Specification.md` - SW 요구사항
- ⬜ `02_SWE1_vECU_Requirements.md` - vECU 특화 요구사항

### 04_Software_Architecture (ISO 26262 Part 6-7, ASPICE SWE.2)
- ⬜ `01_SWE2_Software_Architectural_Design.md` - SW 아키텍처
- ⬜ `02_SWE2_Component_Design.md` - 컴포넌트 설계
- ⬜ `03_SWE2_Interface_Design.md` - 컴포넌트 간 인터페이스

### 05_Software_Detailed_Design (ISO 26262 Part 6-8, ASPICE SWE.3)
- ⬜ `01_SWE3_Detailed_Design.md` - 상세 설계
- ⬜ `02_SWE3_Unit_Design.md` - 유닛 설계

### 06_Implementation (ISO 26262 Part 6-9, ASPICE SWE.3)
- ⬜ `01_Implementation_Guide.md` - 구현 가이드 (코드는 별도 repo)

### 07_Unit_Test (ISO 26262 Part 6-9, ASPICE SWE.4)
- ⬜ `01_SWE4_Unit_Test_Specification.md` - 단위 테스트 사양
- ⬜ `02_SWE4_Unit_Test_Results.md` - 단위 테스트 결과

### 08_SW_Integration_Test (ISO 26262 Part 6-10, ASPICE SWE.5)
- ⬜ `01_SWE5_SW_Integration_Test_Specification.md` - SW 통합 테스트 사양
- ⬜ `02_SWE5_SW_Integration_Test_Results.md` - SW 통합 테스트 결과

### 09_SW_Qualification_Test (ISO 26262 Part 6-11, ASPICE SWE.6)
- ⬜ `01_SWE6_SW_Qualification_Test_Specification.md` - SW 적격성 테스트 사양
- ⬜ `02_SWE6_SW_Qualification_Test_Results.md` - SW 적격성 테스트 결과

### 10_System_Integration_Test (ISO 26262 Part 4-9, ASPICE SYS.4)
- ⬜ `01_SYS4_System_Integration_Test_Specification.md` - 시스템 통합 테스트 사양
- ⬜ `02_SYS4_System_Integration_Test_Results.md` - 시스템 통합 테스트 결과

### 11_System_Qualification_Test (ISO 26262 Part 4-10, ASPICE SYS.5)
- ⬜ `01_SYS5_System_Qualification_Test_Specification.md` - 시스템 적격성 테스트 사양
- ⬜ `02_SYS5_System_Qualification_Test_Results.md` - 시스템 적격성 테스트 결과

### 12_Safety_Validation (ISO 26262 Part 4-10)
- ⬜ `01_Safety_Validation_Report.md` - 안전 검증 보고서

### 99_Supporting_Processes (ISO 26262 Part 8)
- ⬜ `01_Traceability_Matrix.md` - 양방향 추적성 매트릭스
- ⬜ `02_Configuration_Management.md` - 형상 관리
- ⬜ `03_Change_Management.md` - 변경 관리
- ⬜ `04_Documentation_Management.md` - 문서 관리

---

## 📊 진행 상황

| 단계 | 문서 개수 | 완료 | 진행률 |
|------|-----------|------|--------|
| 00 Concept Phase | 3 | 2 | 67% |
| 01 System Requirements | 2 | 0 | 0% |
| 02 System Architecture | 6 | 0 | 0% |
| 03 Software Requirements | 2 | 0 | 0% |
| 04 Software Architecture | 3 | 0 | 0% |
| 05 Software Detailed Design | 2 | 0 | 0% |
| 06 Implementation | 1 | 0 | 0% |
| 07 Unit Test | 2 | 0 | 0% |
| 08 SW Integration Test | 2 | 0 | 0% |
| 09 SW Qualification Test | 2 | 0 | 0% |
| 10 System Integration Test | 2 | 0 | 0% |
| 11 System Qualification Test | 2 | 0 | 0% |
| 12 Safety Validation | 1 | 0 | 0% |
| 99 Supporting Processes | 4 | 0 | 0% |
| **총계** | **34** | **2** | **6%** |

---

## 🎯 작업 우선순위

### Phase 1: 좌측 개발 단계 (우선)
1. ✅ 00 Concept Phase (2/3 완료)
2. ⬜ 01 System Requirements
3. ⬜ 02 System Architecture
4. ⬜ 03 Software Requirements
5. ⬜ 04 Software Architecture
6. ⬜ 05 Software Detailed Design
7. ⬜ 06 Implementation

### Phase 2: 우측 검증 단계
8. ⬜ 07 Unit Test
9. ⬜ 08 SW Integration Test
10. ⬜ 09 SW Qualification Test
11. ⬜ 10 System Integration Test
12. ⬜ 11 System Qualification Test
13. ⬜ 12 Safety Validation

### Phase 3: Supporting Processes
14. ⬜ 99 Traceability Matrix
15. ⬜ 99 Configuration Management
16. ⬜ 99 Change Management
17. ⬜ 99 Documentation Management

---

## 🔧 템플릿 자동 생성

나머지 32개 문서의 템플릿을 자동 생성하려면:

```bash
cd /Users/juns/code/work/mobis/PBL/MentoringResult/V-Model_준수
python3 generate_templates.py
```

템플릿에는 다음이 포함됩니다:
- 문서 헤더 (Document ID, ISO 26262 Reference, ASPICE Reference)
- 섹션 구조 (ISO 26262/ASPICE 요구사항 기반)
- 추적성 테이블
- 승인 테이블
- 개정 이력

---

## 📖 ISO 26262 & ASPICE 준수 체크리스트

### ISO 26262-3 (Concept Phase)
- ✅ Item Definition (Clause 5)
- ✅ Hazard Analysis and Risk Assessment (Clause 7)
- ⬜ Functional Safety Concept (Clause 8)

### ISO 26262-4 (System Level)
- ⬜ System Requirements (Clause 6)
- ⬜ System Architectural Design (Clause 7)
- ⬜ System Integration and Testing (Clause 8)
- ⬜ System Qualification Testing (Clause 9)

### ISO 26262-6 (Software Level)
- ⬜ Software Requirements (Clause 5)
- ⬜ Software Architectural Design (Clause 6)
- ⬜ Software Detailed Design (Clause 7)
- ⬜ Software Unit Design and Implementation (Clause 8)
- ⬜ Software Unit Testing (Clause 9)
- ⬜ Software Integration and Testing (Clause 10)
- ⬜ Software Qualification Testing (Clause 11)

### ISO 26262-8 (Supporting Processes)
- ⬜ Configuration Management (Clause 5)
- ⬜ Change Management (Clause 6)
- ⬜ Verification (Clause 9)
- ⬜ Documentation (Clause 10)

### ASPICE 3.1
- ⬜ SYS.2 (System Requirements Analysis) - BP1~BP7
- ⬜ SYS.3 (System Architectural Design) - BP1~BP8
- ⬜ SYS.4 (System Integration and Integration Test) - BP1~BP8
- ⬜ SYS.5 (System Qualification Test) - BP1~BP6
- ⬜ SWE.1 (Software Requirements Analysis) - BP1~BP6
- ⬜ SWE.2 (Software Architectural Design) - BP1~BP8
- ⬜ SWE.3 (Software Detailed Design) - BP1~BP6
- ⬜ SWE.4 (Software Unit Verification) - BP1~BP5
- ⬜ SWE.5 (Software Integration and Integration Test) - BP1~BP7
- ⬜ SWE.6 (Software Qualification Test) - BP1~BP5

---

## 📚 참고 문서

- ISO 26262-3:2018 - Concept phase
- ISO 26262-4:2018 - Product development at the system level
- ISO 26262-6:2018 - Product development at the software level
- ISO 26262-8:2018 - Supporting processes
- ASPICE 3.1 - Automotive SPICE Process Assessment Model

---

## ✅ 다음 단계

1. **나머지 템플릿 생성**: `python3 generate_templates.py` 실행
2. **System Requirements 작성**: 56개 요구사항을 SYS.2 포맷으로 변환
3. **Traceability Matrix 완성**: Safety Goals → System Req → SW Req → Test Cases
4. **System Architecture 설계**: Domain/ECU 할당 문서화
5. **DBC 파일 통합**: Communication Specification에 포함

---

**작성일**: 2026-02-14
**작성자**: AI Assistant
**검토자**: 프로젝트 팀
**승인**: 대기 중

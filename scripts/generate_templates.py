#!/usr/bin/env python3
"""
V-Model 문서 템플릿 자동 생성기
ISO 26262 & ASPICE 준수 템플릿 생성
"""

import os
from pathlib import Path

# 문서 템플릿 정의
DOCUMENT_TEMPLATES = {
    "00_Concept_Phase/02_Functional_Safety_Concept.md": {
        "doc_id": "PART3-02-FSC",
        "iso_ref": "Part 3, Clause 8",
        "aspice_ref": "N/A",
        "title": "Functional Safety Concept (기능 안전 개념)",
        "sections": [
            "1. 문서 목적",
            "2. Safety Goals",
            "3. Functional Safety Requirements",
            "4. Safe States 정의",
            "5. Fault Tolerant Time Interval (FTTI)",
            "6. Safety Mechanisms",
            "7. ASIL Allocation",
            "8. Verification 계획",
            "9. Traceability"
        ]
    },

    "01_System_Requirements/01_SYS2_System_Requirements_Specification.md": {
        "doc_id": "PART4-01-SRS",
        "iso_ref": "Part 4, Clause 6",
        "aspice_ref": "SYS.2",
        "title": "System Requirements Specification (시스템 요구사항 명세서)",
        "sections": [
            "1. 문서 목적 (Purpose)",
            "2. 요구사항 개요 (Requirements Overview)",
            "3. 기능 요구사항 (Functional Requirements)",
            "4. 안전 요구사항 (Safety Requirements)",
            "5. 비기능 요구사항 (Non-Functional Requirements)",
            "6. 진단/OTA 요구사항 (Diagnostic/OTA Requirements)",
            "7. 우선순위 및 ASIL 분류",
            "8. Traceability (Safety Goals → System Requirements)",
            "9. Verification Methods",
            "10. ASPICE SYS.2 Work Products"
        ]
    },

    "02_System_Architecture/01_SYS3_System_Architectural_Design.md": {
        "doc_id": "PART4-02-SAD",
        "iso_ref": "Part 4, Clause 7",
        "aspice_ref": "SYS.3",
        "title": "System Architectural Design (시스템 아키텍처 설계)",
        "sections": [
            "1. 문서 목적",
            "2. 시스템 아키텍처 개요",
            "3. Domain 구조 (5 Domains)",
            "4. ECU Allocation (23 ECUs)",
            "5. System Elements",
            "6. Safety Mechanisms",
            "7. Freedom from Interference",
            "8. Hardware-Software Interface (HSI)",
            "9. Traceability (System Req → System Elements)",
            "10. ASPICE SYS.3 Work Products"
        ]
    }
}

# 공통 템플릿 헤더
def generate_header(doc_id, iso_ref, aspice_ref, title):
    return f"""# {title}

**Document ID**: {doc_id}
**ISO 26262 Reference**: {iso_ref}
**ASPICE Reference**: {aspice_ref}
**Version**: 1.0
**Date**: 2026-02-14
**Status**: Template

---

## ⚠️ 템플릿 사용 안내

본 문서는 **ISO 26262** 및 **ASPICE 3.1** 준수를 위한 **템플릿**입니다.

**작성 방법**:
1. 각 섹션의 [TODO] 항목을 실제 내용으로 채웁니다
2. 표준 요구사항 (BP, Work Product)을 확인하여 누락 없이 작성합니다
3. Traceability 테이블을 완성합니다
4. 승인 테이블에 서명을 받습니다

---

"""

# 공통 템플릿 푸터
def generate_footer():
    return """
---

## 승인 (Approval)

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| **작성자** | | | |
| **검토자** | | | |
| **승인자** | | | |

---

## 개정 이력 (Revision History)

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-14 | AI Assistant | Template created |

---

**Document End**
"""

# 섹션 템플릿 생성
def generate_sections(sections):
    content = ""
    for section in sections:
        content += f"""## {section}

**[TODO]** 이 섹션을 작성하세요.

**ISO 26262 요구사항**:
- [ ] 해당 Clause의 모든 요구사항 충족
- [ ] Work Product 생성
- [ ] Traceability 확보

**ASPICE Base Practice**:
- [ ] BP1: ...
- [ ] BP2: ...

---

"""
    return content

# 전체 템플릿 생성
def generate_template(doc_id, iso_ref, aspice_ref, title, sections):
    template = generate_header(doc_id, iso_ref, aspice_ref, title)
    template += generate_sections(sections)
    template += generate_footer()
    return template

# 메인 함수
def main():
    base_path = Path("/Users/juns/code/work/mobis/PBL/MentoringResult/V-Model_준수")

    # 이미 생성된 파일 건너뛰기
    skip_files = [
        "00_Concept_Phase/00_Item_Definition.md",
        "00_Concept_Phase/01_Hazard_Analysis_Risk_Assessment.md"
    ]

    created_count = 0
    skipped_count = 0

    # 정의된 템플릿 생성
    for filepath, config in DOCUMENT_TEMPLATES.items():
        full_path = base_path / filepath

        if str(filepath) in skip_files or full_path.exists():
            print(f"⏭️  Skipped (already exists): {filepath}")
            skipped_count += 1
            continue

        template_content = generate_template(
            config["doc_id"],
            config["iso_ref"],
            config["aspice_ref"],
            config["title"],
            config["sections"]
        )

        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(template_content)

        print(f"✅ Created: {filepath}")
        created_count += 1

    # 간단한 템플릿 (나머지 문서)
    simple_templates = [
        ("01_System_Requirements/02_SYS2_Safety_Requirements.md", "PART4-02-SAFETYREQ", "Part 4, Clause 6", "SYS.2", "Safety Requirements"),
        ("02_System_Architecture/02_SYS3_Domain_Architecture.md", "PART4-03-DOM", "Part 4, Clause 7", "SYS.3", "Domain Architecture"),
        ("02_System_Architecture/03_SYS3_ECU_Allocation.md", "PART4-04-ECU", "Part 4, Clause 7", "SYS.3", "ECU Allocation"),
        ("02_System_Architecture/04_SYS3_Network_Topology.md", "PART4-05-NET", "Part 4, Clause 7", "SYS.3", "Network Topology"),
        ("02_System_Architecture/05_SYS3_Communication_Specification.md", "PART4-06-COMM", "Part 4, Clause 7", "SYS.3", "Communication Specification"),
        ("02_System_Architecture/06_SYS3_Interface_Definition.md", "PART4-07-IF", "Part 4, Clause 7", "SYS.3", "Interface Definition"),
        ("03_Software_Requirements/01_SWE1_Software_Requirements_Specification.md", "PART6-01-SWREQ", "Part 6, Clause 5", "SWE.1", "Software Requirements Specification"),
        ("03_Software_Requirements/02_SWE1_vECU_Requirements.md", "PART6-02-VECUREQ", "Part 6, Clause 5", "SWE.1", "vECU Requirements"),
        ("04_Software_Architecture/01_SWE2_Software_Architectural_Design.md", "PART6-03-SWARC", "Part 6, Clause 6", "SWE.2", "Software Architectural Design"),
        ("04_Software_Architecture/02_SWE2_Component_Design.md", "PART6-04-COMP", "Part 6, Clause 6", "SWE.2", "Component Design"),
        ("04_Software_Architecture/03_SWE2_Interface_Design.md", "PART6-05-SWIF", "Part 6, Clause 6", "SWE.2", "Software Interface Design"),
        ("05_Software_Detailed_Design/01_SWE3_Detailed_Design.md", "PART6-06-DET", "Part 6, Clause 7", "SWE.3", "Detailed Design"),
        ("05_Software_Detailed_Design/02_SWE3_Unit_Design.md", "PART6-07-UNIT", "Part 6, Clause 7", "SWE.3", "Unit Design"),
        ("06_Implementation/01_Implementation_Guide.md", "PART6-08-IMPL", "Part 6, Clause 8", "SWE.3", "Implementation Guide"),
        ("07_Unit_Test/01_SWE4_Unit_Test_Specification.md", "PART6-09-UTEST", "Part 6, Clause 9", "SWE.4", "Unit Test Specification"),
        ("07_Unit_Test/02_SWE4_Unit_Test_Results.md", "PART6-10-UTRES", "Part 6, Clause 9", "SWE.4", "Unit Test Results"),
        ("08_SW_Integration_Test/01_SWE5_SW_Integration_Test_Specification.md", "PART6-11-SITEST", "Part 6, Clause 10", "SWE.5", "SW Integration Test Specification"),
        ("08_SW_Integration_Test/02_SWE5_SW_Integration_Test_Results.md", "PART6-12-SITRES", "Part 6, Clause 10", "SWE.5", "SW Integration Test Results"),
        ("09_SW_Qualification_Test/01_SWE6_SW_Qualification_Test_Specification.md", "PART6-13-SQTEST", "Part 6, Clause 11", "SWE.6", "SW Qualification Test Specification"),
        ("09_SW_Qualification_Test/02_SWE6_SW_Qualification_Test_Results.md", "PART6-14-SQTRES", "Part 6, Clause 11", "SWE.6", "SW Qualification Test Results"),
        ("10_System_Integration_Test/01_SYS4_System_Integration_Test_Specification.md", "PART4-08-SYSTEST", "Part 4, Clause 8", "SYS.4", "System Integration Test Specification"),
        ("10_System_Integration_Test/02_SYS4_System_Integration_Test_Results.md", "PART4-09-SYSTRES", "Part 4, Clause 8", "SYS.4", "System Integration Test Results"),
        ("11_System_Qualification_Test/01_SYS5_System_Qualification_Test_Specification.md", "PART4-10-SYSQTEST", "Part 4, Clause 9", "SYS.5", "System Qualification Test Specification"),
        ("11_System_Qualification_Test/02_SYS5_System_Qualification_Test_Results.md", "PART4-11-SYSQTRES", "Part 4, Clause 9", "SYS.5", "System Qualification Test Results"),
        ("12_Safety_Validation/01_Safety_Validation_Report.md", "PART4-12-VAL", "Part 4, Clause 10", "N/A", "Safety Validation Report"),
        ("99_Supporting_Processes/01_Traceability_Matrix.md", "PART8-01-TRACE", "Part 8, Clause 9", "SUP.10", "Traceability Matrix"),
        ("99_Supporting_Processes/02_Configuration_Management.md", "PART8-02-CONFIG", "Part 8, Clause 5", "SUP.8", "Configuration Management"),
        ("99_Supporting_Processes/03_Change_Management.md", "PART8-03-CHANGE", "Part 8, Clause 6", "SUP.10", "Change Management"),
        ("99_Supporting_Processes/04_Documentation_Management.md", "PART8-04-DOC", "Part 8, Clause 10", "SUP.9", "Documentation Management"),
    ]

    for filepath, doc_id, iso_ref, aspice_ref, title in simple_templates:
        full_path = base_path / filepath

        if full_path.exists():
            print(f"⏭️  Skipped (already exists): {filepath}")
            skipped_count += 1
            continue

        simple_template = generate_header(doc_id, iso_ref, aspice_ref, title)
        simple_template += f"""## 1. 문서 목적

**[TODO]** 본 문서의 목적을 작성하세요.

---

## 2. 주요 내용

**[TODO]** ISO 26262 {iso_ref} 및 ASPICE {aspice_ref} 요구사항에 따라 내용을 작성하세요.

---

## 3. Traceability

**[TODO]** 추적성 매트릭스를 작성하세요.

| 상위 문서 | 본 문서 | 하위 문서 |
|-----------|---------|-----------|
| [TODO] | [TODO] | [TODO] |

---
"""
        simple_template += generate_footer()

        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(simple_template)

        print(f"✅ Created: {filepath}")
        created_count += 1

    print(f"\n" + "="*60)
    print(f"✅ 생성 완료: {created_count}개 파일")
    print(f"⏭️  건너뜀: {skipped_count}개 파일 (이미 존재)")
    print(f"📊 총 문서: {created_count + skipped_count}개")
    print("="*60)

if __name__ == "__main__":
    main()

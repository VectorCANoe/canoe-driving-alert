# 최종 제출 골격 고정안 (Final Structure Lock)

**문서 목적**
- 중간/최종 제출용 문서가 빠르게 읽히고, 심사자가 바로 판단할 수 있는 구조를 유지하도록 골격을 고정한다.
- SoT 원문(루트 `00~07`)은 그대로 유지하고, 제출본(`tmp/submission/final-docs`)만 reviewer-facing 구조로 단순화한다.

---

## 1) 골격 근거 (레퍼런스 기반)

아래 기준을 교차 적용해 골격을 고정한다.

1. 프로젝트 샘플 형식 (표 중심, 판단 항목 우선)
- `reference/standards/Project Result_Sample/01.md`
- `reference/standards/Project Result_Sample/03.md`
- `reference/standards/Project Result_Sample/0301.md`
- `reference/standards/Project Result_Sample/0302.md`
- `reference/standards/Project Result_Sample/0303.md`
- `reference/standards/Project Result_Sample/0304.md`
- `reference/standards/Project Result_Sample/05.md`
- `reference/standards/Project Result_Sample/06.md`
- `reference/standards/Project Result_Sample/07.md`

2. 프로세스/안전 프레임
- `reference/standards/Automotive_SPICE_PAM_31_EN.pdf`
- `reference/standards/ISO_26262-1_2018.pdf`

3. 멘토링 해석(가독성 우선)
- `docs/meeting-notes/MET_40_2026.03.03.txt`
- `docs/meeting-notes/MET_41_2026.03.07.txt`

---

## 2) 최종 제출 문서 계층 (고정)

### L0: 프로젝트 이해 계층
- 파일:
  - `00_Project_Overview.md`
  - `02_Concept_design.md`
- 목적: 프로젝트 구조와 핵심 시나리오를 빠르게 이해하게 한다.
- 규칙: 그림과 핵심 규칙만 유지하고 내부 운영 설명은 넣지 않는다.

### L1: 설계 본문 계층
- 파일:
  - `01_Requirements.md`
  - `03_Function_definition.md`
  - `0301_SysFuncAnalysis.md`
  - `0302_NWflowDef.md`
  - `0303_Communication_Specification.md`
  - `0304_System_Variables.md`
  - `04_SW_Implementation.md`
- 목적: `What -> How` 및 설계 책임 구간을 설명한다.
- 규칙: 공식 표준 양식 중심, reviewer-facing 문장 우선

### L2: 검증 계층
- 파일:
  - `05_Unit_Test.md`
  - `06_Integration_Test.md`
  - `07_System_Test.md`
- 목적: 시험 관점의 검증 근거를 제시한다.
- 규칙: 목적, 조건, 기대결과, 판정 기준을 표 안에서 바로 읽을 수 있어야 한다.

### Appendix: 요청 시 제시 계층
- 폴더:
  - `governance/*`
- 포함 문서:
  - `00d_HARA_Worksheet.md`
  - `00e_ECU_Naming_Standard.md`
  - `00f_CAN_ID_Allocation_Standard.md`
- 목적: 안전, 명명, ID 정책의 세부 근거를 제공한다.

---

## 3) 문서 공통 골격 규칙 (고정)

모든 본편 문서는 아래 원칙을 따른다.

1. 문서 헤더
- `Document ID / Version / Date / Status`

2. 공식 표 우선
- reviewer가 실제로 보는 핵심 판단 정보는 상단 공식 표에 직접 들어가야 한다.
- 하단 보강표 의존을 최소화한다.

3. 문장 원칙
- 짧은 평문 문장 사용
- 한 문장에 독립 판단 기준 1개 유지
- 내부 변수명/모듈명은 공식 표에서 남용하지 않는다.

4. 추적 원칙
- 제출본은 추적 가능해야 하지만, 매핑표를 과도하게 전면에 드러내지 않는다.
- 상세 trace는 SoT와 개발 문서에서 유지한다.

---

## 4) 가독성 가드레일 (고정)

1. 동일 의미 중복표 금지
2. Safety Goal ID, VC ID 같은 내부 관리 표식은 제출본에서 과도하게 전면화하지 않는다.
3. 요구사항 ID는 단순 순번 기반으로 유지하고, 기능 분류는 번호가 아니라 문서 구조와 Part로 표현한다.
4. 실측 미완료 항목은 `Planned/Ready`로 남기고, 미완료 사유는 별도 운영 문서에서 관리한다.

---

## 5) 최종 제출 읽기 순서 (권장)

1. `00_Project_Overview.md`
2. `02_Concept_design.md`
3. `01_Requirements.md`
4. `03 -> 0301 -> 0302 -> 0303 -> 0304`
5. `04_SW_Implementation.md`
6. `05 -> 06 -> 07`
7. 필요 시 `governance/00d -> 00e -> 00f`

---

## 6) 운영 결정

- `tmp/submission/final-docs`를 최종 제출 편집본 기준 폴더로 고정한다.
- 제출 본편은 `00~07`만 유지한다.
- `00_MASTER_*`, `00b`, `00c`, `00g`는 내부 참고용으로 `mid-docs`에만 유지한다.
- 원문 SoT 수정이 발생하면 동일 변경을 `final-docs`에 후행 반영한다.

---

## 7) 실행 고정 규칙 (엑셀 변환 포함)

1. 단일 입력원
- 제출 엑셀 생성 시 입력 경로는 `tmp/submission/final-docs`로 고정한다.

2. 워크북 포함 파일
- `00_Project_Overview.md`
- `01_Requirements.md`
- `02_Concept_design.md`
- `03_Function_definition.md`
- `0301_SysFuncAnalysis.md`
- `0302_NWflowDef.md`
- `0303_Communication_Specification.md`
- `0304_System_Variables.md`
- `04_SW_Implementation.md`
- `05_Unit_Test.md`
- `06_Integration_Test.md`
- `07_System_Test.md`

3. 워크북 제외 파일
- `README_SUBMISSION_DOCSET.md`
- `00_FINAL_STRUCTURE_LOCK.md`
- `governance/*` (요청 시 별도 부록)

4. 구조 변경 통제
- 포함/제외 파일셋 변경은 문서팀 합의 후 `00_FINAL_STRUCTURE_LOCK.md`와 `README_SUBMISSION_DOCSET.md`를 동시에 갱신한다.

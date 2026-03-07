# 최종 제출 골격 고정안 (Final Structure Lock)

**문서 목적**
- 중간/최종 제출용 문서가 “전문성은 유지하면서 빠르게 읽히는 구조”를 일관되게 유지하도록 골격을 고정한다.
- SoT 원문(루트 `00~07`)은 그대로 유지하고, 제출본(`tmp/submission/final-docs`)만 가독성 최적화한다.

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

## 2) 최종 문서 계층 (고정)

### L0: 평가자 빠른 이해 계층
- 파일:
  - `00_MASTER_Project_Framework.md`
  - `00_MASTER_Governance_Summary.md`
  - `02_Concept_design.md`
- 목적: 5분 내 프로젝트 파악
- 규칙: 장문 설명 금지, 결정/범위/제약/상태만 유지

### L1: 설계 본문 계층
- 파일:
  - `01_Requirements.md`
  - `03_Function_definition.md`
  - `0301_SysFuncAnalysis.md`
  - `0302_NWflowDef.md`
  - `0303_Communication_Specification.md`
  - `0304_System_Variables.md`
  - `04_SW_Implementation.md`
- 목적: `What -> How` 및 추적 연결 판단
- 규칙: 표 중심 + 핵심 규칙 중심(설명은 최소)

### L2: 검증 계층
- 파일:
  - `05_Unit_Test.md`
  - `06_Integration_Test.md`
  - `07_System_Test.md`
- 목적: Pass/Fail 증빙 판단
- 규칙: 테스트 케이스-근거-판정 결과가 한 화면에서 확인 가능해야 함

### Appendix: 요청 시 제시 계층
- 폴더:
  - `governance/*`
- 목적: 정책 상세 근거(00c/00d/00e/00f/00g 원본 축소본)

---

## 3) 문서 공통 골격 규칙 (고정)

모든 본편 문서는 아래 순서를 유지한다.

1. 문서 헤더
- `Document ID / Version / Date / Status`

2. L0 Quick Read 블록 (최대 8줄)
- 목적
- 이번 문서의 결정사항
- 입력/출력(또는 연계 문서)
- 현재 상태(`Active`, `Pre-Activation`, `Planned`)

3. 핵심 표 (판단용)
- 문서 목적에 맞는 대표 표 1~2개를 최상단 유지

4. 추적 연결 표 (필수)
- `Req -> Func -> Flow -> Comm -> Var -> Code -> Test` 중 해당 문서 책임 구간을 명시

5. 상세/예외/Legacy
- 본문 마지막으로 배치(평가자 1차 읽기 방해 금지)

---

## 4) 가독성 가드레일 (고정)

1. 본문 원칙
- 한 문장에 독립 판단 기준 1개만 유지
- 모호어 최소화(`적절히`, `충분히`)하고 조건/수치 우선

2. 표 원칙
- 동일 의미 중복표 금지
- 대표표(본문) + 상세표(후행) 2단 구조 유지

3. 용어 원칙
- 상위 체인 문서: 논리명 우선 (`EMS_ALERT`)
- 구현/하위 매핑: 내부 모듈명 허용 (`*_TX`, `*_RX`)

4. 상태 원칙
- 실측 미완료 항목은 `Planned/Ready`로만 유지
- 완료/대기 혼합 상태는 문서 하단 “폐쇄 보류” 블록에서 통합 관리

---

## 5) 최종 제출 읽기 순서 (권장)

1. `00_MASTER_Project_Framework.md`
2. `00_MASTER_Governance_Summary.md`
3. `02_Concept_design.md`
4. `01_Requirements.md`
5. `03 -> 0301 -> 0302 -> 0303 -> 0304`
6. `04_SW_Implementation.md`
7. `05 -> 06 -> 07`

---

## 6) 운영 결정

- `tmp/submission/final-docs`를 최종 제출 편집본 기준 폴더로 고정한다.
- `tmp/submission/docs`는 이전 제출본 기준(레거시)으로 남기되, 신규 편집은 `final-docs`에서만 수행한다.
- 원문 SoT 수정이 발생하면 동일 변경을 `final-docs`에 동기화하고, 동기화 이력은 `README_SUBMISSION_DOCSET.md`에 기록한다.

---

## 7) 실행 고정 규칙 (엑셀 변환 포함)

1. 단일 입력원
- 제출 엑셀 생성 시 입력 경로는 `tmp/submission/final-docs`로 고정한다.

2. 워크북 포함 파일
- `00_MASTER_Project_Framework.md`
- `00_MASTER_Governance_Summary.md`
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

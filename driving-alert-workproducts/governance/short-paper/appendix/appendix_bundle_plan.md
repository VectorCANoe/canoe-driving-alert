# Appendix Bundle Plan

## 1. 목적

본 문서는 소논문 제출 시 함께 첨부할 부록·별첨 문서의 범위와 구성을 고정하기 위한 계획 문서이다.

핵심 원칙은 다음과 같다.

1. 본문 부록은 논문 주장과 계산식을 직접 받치는 최소 범위만 포함한다.
2. 계약 전문과 검증 전문은 별도 supplementary PDF로 분리한다.
3. 별첨은 raw dump가 아니라 reviewer-facing 정리본으로 제공한다.

## 2. 외부 레퍼런스 기준

부록과 별첨의 구분은 다음 공개 가이드를 참고한다.

- IEEE Access Submission Guidelines  
  https://ieeeaccess.ieee.org/authors/submission-guidelines/  
  - 본문은 IEEE template 기준으로 유지한다.
  - 20페이지를 넘는 상세 내용은 supplementary material로 분리할 수 있다.
- IEEE Editorial Style Manual for Authors  
  https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf  
  - supplementary material은 본문과 별도로 관리할 수 있다.
  - 본문은 standalone으로 읽혀야 하고, supplementary는 보강 자료여야 한다.
- Springer journal instructions example  
  https://media.springer.com/full/springer-instructions-for-authors-assets/pdf/13280_Ambio%20Instructions%20for%20authors_November%202021.pdf  
  - Supplementary Information은 main article과 분리된 별도 자료로 제공한다.
  - 별첨은 Figure/Table numbering을 본문과 분리해 운용할 수 있다.

## 3. 권장 제출 구조

### 3.1 본문 Appendix

본문 안에 직접 두는 부록은 다음 한정 범위가 적절하다.

- Appendix A. 핵심 계산식 및 지표 정의
  - V2X 선택 규칙
  - 긴급 접근 위험도
  - TTC
  - 핵심 정량 지표 `N1`, `N2`, `N3` 집계식

이 부록은 main paper 내부에 유지한다.

### 3.2 Supplementary PDF Bundle

별첨은 하나의 PDF bundle로 묶는 구성이 가장 안정적이다.

권장 파일명:

- `supplementary_appendix_bundle.pdf`

권장 내부 구성:

1. Cover Page
2. Table of Contents
3. Supplementary Note S1. Safety and Traceability Basis
4. Supplementary Note S2. Runtime Contract Set
5. Supplementary Note S3. Verification Contract Set
6. Supplementary Note S4. Diagnostic and Observability Set

## 4. 포함 문서 선정

본 별첨은 축소형 curated set이 아니라, 논문과 발표 자료에서 직접 참조 가능한 계약·검증 문서를 폭넓게 포함하는 방향으로 운용한다.

### 4.1 S1. Safety and Traceability Basis

논문 본문의 안전성과 검증 추적성을 직접 받치는 문서만 포함한다.

- `project_v_model_traceability_map` (appendix reviewer-facing summary)
- [00d_HARA_Worksheet.md](/Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/00d_HARA_Worksheet.md)
- [00g_Master_Test_Matrix.md](/Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/00g_Master_Test_Matrix.md)

추가 포함:

- [00e_ECU_Naming_Standard.md](/Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/00e_ECU_Naming_Standard.md)
- [00f_CAN_ID_Allocation_Standard.md](/Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/00f_CAN_ID_Allocation_Standard.md)

선정 이유:

- V-모델 overview는 현재 active baseline 기준으로 `00/01/03/030x/04/05/06/07` 문서 체인을 한 장에서 설명한다.
- HARA는 위험 시나리오와 안전 목표의 출발점이다.
- `00g_Master_Test_Matrix`는 프로젝트의 Test Matrix 역할을 수행하며, 요구사항에서 단위시험·통합시험·시스템시험으로 이어지는 추적성을 보여준다.
- ECU naming과 CAN ID allocation은 PPT 부록과 별첨에서 아키텍처와 인터페이스 설명을 보강하는 표준 문서로 사용한다.

### 4.2 S2. Runtime Contract Set

논문이 주장하는 V2X-ADAS 경고 구조를 직접 설명하는 계약 문서를 포함한다.

추가 포함:

- `appendix/source/architecture/vehicle_ecu_architecture_and_interaction_reference.md`
- `canoe/docs/architecture/master_book/ECU_METADATA_BOOK_2026-03-28.pdf`
- `canoe/docs/architecture/master_book/ACTION_FLOW_INDEX_2026-03-28.md`
- `canoe/docs/architecture/master_book/ECU_ACTION_FLOW_MATRIX_2026-03-28.md`
- `canoe/docs/architecture/master_book/ECU_CARD_INDEX_2026-03-28.md`
- `canoe/docs/architecture/master_book/SIGNAL_FLOW_INDEX_2026-03-28.md`

기본 포함:

- [communication-matrix.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/communication-matrix.md)
- [owner-route.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/owner-route.md)
- [layer-separation-policy.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/layer-separation-policy.md)
- [ethernet-interface.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/ethernet-interface.md)
- [multibus-policy.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/multibus-policy.md)
- [panel-sysvar-contract.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/panel-sysvar-contract.md)
- [ethernet-backbone.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/ethernet-backbone.md)

선정 이유:

- `Vehicle ECU Architecture and Interaction Reference`는 V2X-ADAS-CGW-출력 계층을 한 권의 읽기 레이어로 정리한 공식 architecture reference다.
- 본문이나 발표 자료에서 축약된 그림만 사용할 때, appendix reviewer는 이 reference를 통해 전체 ECU 구조와 행동 흐름을 빠르게 복원할 수 있다.
- action-flow index, ECU-flow matrix, ECU-card index, signal-flow index는 appendix drill-down 순서를 고정하는 데 필요하다.
- `communication-matrix`는 active runtime sender/consumer와 backbone contract를 보여준다.
- `owner-route`는 V2X, ADAS, CGW, 출력 계층의 ownership 경계를 설명한다.
- `layer-separation-policy`는 business semantics, transport, validation layer를 분리하는 기준 문서다.
- `ethernet-interface`는 CAN/Ethernet 경계 설명에 직접 필요하다.

### 4.3 S3. Verification Contract Set

논문의 검증 구조와 정량 지표 해석을 직접 받치는 문서만 포함한다.

- [oracle.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/verification/oracle.md)
- [acceptance-criteria.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/verification/acceptance-criteria.md)
- [test-asset-mapping.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/verification/test-asset-mapping.md)
- [execution-guide.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/verification/execution-guide.md)

- [evidence-policy.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/verification/evidence-policy.md)

선정 이유:

- `oracle`과 `acceptance-criteria`는 시험 판정 기준의 핵심이다.
- `test-asset-mapping`은 `05/06/07`과 executable asset 사이의 브리지다.
- `execution-guide`는 시험 수행 표면을 정리한다.

### 4.4 S4. Diagnostic and Observability Set

진단이 논문 핵심 주제는 아니지만, 관측 경로를 설명하기 위한 별첨으로는 가치가 있다.

- [diagnostic-matrix.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/diagnostic-matrix.md)
- [diagnostic-sysvar-contract.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/contracts/diagnostic-sysvar-contract.md)

- [diagnostic-seam-design.md](/Users/juns/code/work/mobis/PBL/canoe/docs/Kor/verification/diagnostic-seam-design.md)

선정 이유:

- 본문에서 diag는 주제가 아니라 관측 계층이다.
- 따라서 별첨에서는 상태와 경계 조건을 독립적으로 관측하는 구조를 보강하는 정도로 한정한다.

## 5. PDF 작성 원칙

각 supplementary note는 개별 Markdown dump를 그대로 나열하지 않고 아래 형식을 갖는 reviewer-facing bundle로 재편집한다.

1. 제목
2. 목적
3. 본 논문과의 관련성
4. 핵심 표/그림
5. 원문 계약 전문
6. source path / version / date

권장 표기:

- Supplementary Note S1, S2, S3, S4
- Figure S1, Table S1 형식의 별도 번호 체계

## 6. 한국어/영어 운용 원칙

- reviewer-facing PDF는 한국어 문서를 기본으로 한다.
- 표지 또는 머리말에 canonical source path를 영어 경로로 병기한다.
- 기술 식별자, ECU명, signal명, asset ID는 원문 표기를 유지한다.

## 7. 다음 단계

1. `appendix/source/`에 원문 복제본 유지
2. `appendix/tex/`에 bundle TeX와 generated TeX 유지
3. `supplementary_appendix_bundle.tex` 생성
4. S1~S4 cover page와 section skeleton 생성
5. selected docs를 reviewer-facing LaTeX로 이식
6. 최종 PDF bundle 생성

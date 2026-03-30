# Appendix Workspace

이 폴더는 소논문 본문과 별도로 제출하거나 부록으로 첨부할 계약·검증 문서 묶음을 관리한다.

## 목적

- 본문을 직접 받치는 핵심 부록 항목을 정리한다.
- 심사자가 별첨 PDF로 확인할 계약·검증 문서를 구조화한다.
- Markdown 원문을 reviewer-facing LaTeX/PDF로 전환하기 위한 기준선을 고정한다.

## 원칙

- 본문 부록은 최소화하고, 핵심 계약 전문은 별첨 PDF로 분리한다.
- 별첨은 `governance`와 `canoe/docs/Kor`의 reviewer-facing 문서를 우선 사용한다.
- 한글 별첨을 기본으로 하되, 표지에 영어 canonical source path를 병기한다.
- raw 작업 메모나 archive 이력은 별첨 본문에 직접 넣지 않는다.

## 문서

- `appendix_bundle_plan.md`
  - 별첨 구성안
  - 포함 문서 선정 기준
  - 권장 PDF 묶음 구조
- `source/`
  - `architecture/`
    - `vehicle_ecu_architecture_and_interaction_reference.md`
    - `ECU_METADATA_BOOK_2026-03-28.md`
    - `ECU_METADATA_BOOK_2026-03-28.pdf`
    - `ACTION_FLOW_INDEX_2026-03-28.md`
    - `ECU_ACTION_FLOW_MATRIX_2026-03-28.md`
    - `ECU_CARD_INDEX_2026-03-28.md`
    - `SIGNAL_FLOW_INDEX_2026-03-28.md`
    - `ECU_GROUP_NETWORK_VIEW_2026-03-28.md`
    - official architecture reference mirror for appendix reuse
  - `governance/`
  - `contracts/`
  - `verification/`
  - `diagnostic/`
  - 별첨에 들어갈 원문 복제본
  - `governance/project_v_model_traceability_map.*`
  - 프로젝트 V-모델 reviewer-facing 요약본과 figure source
- `tex/`
  - `supplementary_appendix_bundle.tex`
  - `build_appendix_bundle.sh`
  - `generated/`
  - reviewer-facing bundle TeX와 생성물

## Build

```bash
cd /Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/short-paper/appendix/tex
./build_appendix_bundle.sh
```

# PPT Workspace

이 폴더는 소논문/포스터와 별도로, 발표용 PPT 구성안과 시각자료 배치 기준을 관리한다.

## 목적

- 소논문보다 넓은 범위에서 프로젝트 전체 프로세스를 설명한다.
- 무엇을 설계했는가보다, 무엇을 경험했고 어떤 기준선과 운영 구조를 구축했는가를 전달한다.
- 발표 슬라이드별 핵심 메시지, 근거 문서, 권장 이미지 구성을 고정한다.

## 원칙

- 발표는 `문제 인식 -> 설계 선택 -> 구현 경험 -> 시험 체계 -> 운영 자동화 -> 배운 점` 흐름으로 구성한다.
- 소논문의 계산식과 핵심 로직은 유지하되, PPT에서는 전체 프로세스와 경험이 먼저 보이게 한다.
- 수치 결과는 실제 근거가 있는 항목만 사용한다. 미확정 성능 수치 대신 구축 결과와 실행 증거를 우선 제시한다.
- 한 슬라이드에는 핵심 메시지 하나만 두고, 시각자료는 1~2개 이내로 제한한다.

## 문서

- `ppt_storyboard.md`
  - 발표 전체 구조
  - 슬라이드별 목적, 핵심 메시지, 근거 문서, 권장 시각자료
- `ppt_asset_guide.md`
  - 실제 PPT 편집 시 사용할 이미지/도식 가이드
- `assets/`
  - 실제로 바로 넣을 수 있는 SVG 자산 팩
- `driving_alert_process_presentation.tex`
  - 실제 발표용 Beamer 원고
- `build_presentation.sh`
  - PDF 빌드 스크립트

## Source Priority

- 프로젝트 개요: `00_Project_Overview.md`
- 구현 구조: `04_SW_Implementation.md`
- 시험 체계: `05_Unit_Test.md`, `06_Integration_Test.md`, `07_System_Test.md`
- 추적 구조: `governance/00d_HARA_Worksheet.md`, `governance/00g_Master_Test_Matrix.md`
- 소논문 요약: `paper/short_paper_draft.md`
- 포스터 요약: `poster/poster_session_draft.md`

## Build

```bash
cd /Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/short-paper/ppt
./build_presentation.sh
```

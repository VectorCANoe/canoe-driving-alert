# tmp Workspace Guide

이 폴더는 문서팀 작업 산출물의 운영 공간이다.

핵심 원칙:
- SoT(원문)는 루트 `00~07`에서만 관리한다.
- `tmp`는 운영/협업/제출 편집본 용도다.
- 활성 문서만 유지하고 불필요한 스냅샷은 삭제한다.
- 사람용 문서 언어는 `tmp/00_문서_언어_운영원칙.md`를 따른다.

## 1) Active (지금 보는 경로)

- 협업 보드: `tmp/change-orders/TEAM_SYNC_BOARD.md`
- 멘토링 체크: `tmp/mentoring/Mentoring_MET40.md`, `tmp/mentoring/Mentoring_MET41.md`
- 제출 편집본: `tmp/submission/final-docs/`
- 제출 엑셀: `tmp/submission/excel/`
- 증빙 인덱스: `tmp/reports/M40_EVIDENCE_INDEX.md`

## 2) Submission 운영 규칙

- 편집은 `tmp/submission/final-docs/`에서만 수행
- 제출 패키징 기준은 `tmp/submission/README.md`를 따른다

## 3) 폴더 역할

- `assets/current`: 문서 본문에서 참조하는 최신 이미지
- `assets/source`: 다이어그램 원본(drawio)
- `change-orders`: 개발팀/문서팀 전달 및 동기화 문서
- `mentoring`: 멘토링 분석 및 체크리스트
- `reports`: 현재 사이클 실행/증빙 인덱스
- `work-notes`: 내부 메모 인덱스(활성은 `id`만 유지)
- `work-notes/id`: CAN ID 설계 초안/매핑 템플릿
- `archive`: 과거 산출물 보관

## 4) 금지/주의

- SoT 원문(`00~07`) 직접 축약/삭제 금지
- `tmp` 정리 시 추적 근거 문서 삭제 금지
- 경로 이동이 필요한 경우 README/가이드 참조 경로를 함께 갱신

# tmp 폴더 구조 가이드

본 폴더는 작업 중간 산출물/운영 메모를 보관한다.

## 디렉터리

- `assets/current`: 본문 문서에서 직접 참조하는 최신 이미지
- `assets/source`: 다이어그램 원본(drawio 등)
- `mentoring`: 멘토링 분석/액션 문서
- `change-orders`: 개발팀 전달용 변경지시/이관 문서
- `work-notes`: 작업 메모, 계획, 가이드 문서
- `quality/reports`: 품질 점검 리포트 산출물
- `quality/templates`: 품질 점검 템플릿
- `archive/pending_cleanup`: 레거시/초안 보관본(삭제 전 임시 보관)

## 운영 원칙

- 문서 본문에서 참조하는 파일은 `assets/current`에 둔다.
- 신규 임시 문서는 목적에 맞는 하위 폴더에 저장한다.
- 삭제 여부가 불확실한 자료는 `archive/pending_cleanup`로 먼저 이동한다.

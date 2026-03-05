> TEMP NOTE (STALE)
> 이 문서는 참고용 임시 메모입니다. 공식 SoT는 `driving-situation-alert/00e_ECU_Naming_Standard.md`, `driving-situation-alert/00f_CAN_ID_Allocation_Standard.md` 및 정식 체인 문서(`01/03/0301/0302/0303/0304/04/05/06/07`)입니다.
> 임시 문서와 SoT가 충돌하면 SoT를 우선 적용합니다.

# tmp 폴더 구조 가이드

본 폴더는 작업 중간 산출물/운영 메모를 보관한다.

## 디렉터리

- `assets/current`: 본문 문서에서 직접 참조하는 최신 이미지
- `assets/source`: 다이어그램 원본(drawio 등)
- `mentoring`: 멘토링 분석/액션 문서
- `change-orders`: 개발팀 전달용 변경지시/이관 문서
- `work-notes`: 작업 메모, 계획, 가이드 문서
- `onboarding`: 팀 온보딩용 쉬운 설명서(3/3/5, 중재 규칙, 게이트, FAQ)
- `quality/reports`: 품질 점검 리포트 산출물
- `quality/templates`: 품질 점검 템플릿
- `archive/pending_cleanup`: 레거시/초안 보관본(삭제 전 임시 보관)

## 운영 원칙

- 문서 본문에서 참조하는 파일은 `assets/current`에 둔다.
- 신규 임시 문서는 목적에 맞는 하위 폴더에 저장한다.
- 삭제 여부가 불확실한 자료는 `archive/pending_cleanup`로 먼저 이동한다.

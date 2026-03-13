# Assets Workspace Index

이 폴더는 문서 본문과 제출본에서 참조하는 이미지 자산을 관리한다.

## Structure

- `current/`
  - 현재 문서에서 직접 참조하는 최신 이미지
- `source/`
  - drawio 등 편집 가능한 원본

## Working Rule

- 문서 본문에는 `current/` 자산만 연결한다.
- 수정 가능한 원본은 `source/`에 유지하고, 최종 반영본은 `current/`로 갱신한다.

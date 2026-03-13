# Reports Index

이 폴더는 증빙 인덱스와 문서-코드 정합 리포트를 관리한다.

## Folder Policy

- `active/`: 현재 사이클에서 참조하는 리포트
- `history/`: 종료된 사이클 리포트

## Active Files (`active/`)

- `M40_EVIDENCE_INDEX.md`
  - 멘토 open item 기준 증빙 경로 인덱스
- `Doc_Code_Sync_Report.md`
  - 문서-코드 정합 상태 점검 리포트
  - `scripts/gates/doc_code_sync_gate.py` 실행 시 재생성되는 산출물
  - Git tracked 정본이 아니라 local/CI generated output으로 취급

## Operation Rules

1. 신규 리포트는 기본 `active/`에 둔다.
2. 사이클 종료 후 재사용하지 않는 리포트는 `history/`로 이동한다.
3. 대용량 실행 산출물은 실행 경로(`canoe/tmp/reports/verification/` 등)에 두고, 여기서는 인덱스/요약만 유지한다.

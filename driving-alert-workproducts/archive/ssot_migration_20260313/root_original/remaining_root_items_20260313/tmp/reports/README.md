# Reports Index

이 폴더는 현재 사이클의 증빙 인덱스와 문서-코드 정합 리포트를 둔다.

## Active Files

- `M40_EVIDENCE_INDEX.md`
  - 멘토 open item 기준 증빙 경로 인덱스
- `Doc_Code_Sync_Report.md`
  - 문서-코드 정합 상태 점검 리포트
  - `scripts/gates/doc_code_sync_gate.py`가 매 실행마다 다시 생성하는 산출물이다.
  - Git tracked 정본이 아니라 local/CI generated output으로 취급한다.

## Working Rule

- 이 폴더는 결과 파일 자체보다 인덱스/요약 문서에 집중한다.
- 대용량 실행 산출물은 각 실행 경로(`canoe/tmp/reports/verification/` 등)에 두고, 여기서는 참조만 유지한다.
- `Doc_Code_Sync_Report.md`는 필요 시 재생성하고, 저장소에는 경로/규칙만 유지한다.

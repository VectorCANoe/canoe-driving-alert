# Final Closeout Checklist

이 문서는 최종 제출 직전 Dev1, Dev2, 문서팀이 같은 종료 기준으로 확인하기 위한 단일 체크리스트다.

## 1) 공통 종료 기준

- `TMP_HANDOFF.md`가 여전히 `FRESH` 상태인지 확인
- SoT 체인(`01 -> 03 -> 0301/0302/0303/0304 -> 04 -> 05/06/07`)의 버전/헤더가 현재 제출본과 정합한지 확인
- `tmp/submission/final-docs/` 실제 파일셋이 현재 제출 범위와 일치하는지 확인
- `Req -> Func -> Flow -> Comm -> Var -> Code -> UT/IT/ST` 추적 연결이 끊기지 않았는지 확인

## 2) Dev1 체크

- CANoe runtime baseline에서 신규 must-fix defect가 없는지 확인
- native CANoe Test Unit PoC 자산이 최신 상태인지 확인
- GUI-first 대상(`canoe/cfg/*.cfg`, `*.cfg.ini`, `*.stcfg`)을 스크립트로 건드리지 않았는지 확인
- Ethernet cutover backlog와 current-cycle fix를 혼동하지 않았는지 확인

## 3) Dev2 체크

- `SDV Operator` 제품 경계가 유지되는지 확인
- CLI/TUI가 현재 실행 기준(`doctor`, `verify quick`, `gate all` 등)에서 동작하는지 확인
- 결과 산출 포맷 정책이 `JSON + MD` 기본, `CSV` 선택으로 유지되는지 확인
- 최종 패키징 범위가 runtime project 전체가 아니라 product surface 기준인지 확인

## 4) 문서팀 체크

- `04/05/06/07`에 최신 구현/증빙 상태가 반영됐는지 확인
- `tmp/submission/final-docs/` 편집본이 루트 SoT와 어긋나지 않는지 확인
- `tmp/submission/README.md`와 `mid-docs` 보관본이 현재 제출 구조를 설명하는지 확인
- 내부 운영 문서와 제출 문서를 섞지 않았는지 확인

## 5) 증빙 체크

- `05_Unit_Test.md`에 UT 증빙 상태가 반영됐는지 확인
- `06_Integration_Test.md`에 IT 증빙 상태가 반영됐는지 확인
- `07_System_Test.md`에 ST 증빙 상태가 반영됐는지 확인
- 캡처, 로그, 리포트 경로가 실제 파일 또는 실행 경로와 연결되는지 확인

## 6) 제출 직전 체크

- `tmp/submission/excel/`의 제출용 엑셀만 유지되는지 확인
- 제출 제외 파일이 `final-docs` 본편에 섞이지 않았는지 확인
- 팀 보드의 open item 중 제출을 막는 항목이 남아 있지 않은지 확인

## 7) 현재 해석

- Dev1: runtime must-do code fix는 종료, native proof 안정화와 defect 대응만 잔존
- Dev2: operator/TUI/CLI/packaging 자산 계속 진행
- 문서팀: `04/05/06/07`와 제출 편집본 최종 마감

## 8) 참조 문서

- `driving-situation-alert/TMP_HANDOFF.md`
- `driving-situation-alert/tmp/change-orders/TEAM_SYNC_BOARD.md`
- `driving-situation-alert/tmp/change-orders/FINAL_PHASE_TEAM_SPLIT_2026-03-08.md`
- `canoe/AGENT/`
- `driving-situation-alert/tmp/submission/README.md`
- `driving-situation-alert/tmp/submission/mid-docs/`

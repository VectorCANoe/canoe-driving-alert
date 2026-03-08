# 결과 해석

## 판정 체계

- `PASS`
  - 명령이 정상 종료되었고 핵심 결과가 기대 범위에 있습니다.
- `WARN`
  - 실행은 끝났지만 추가 조치가 필요합니다.
  - 예: measurement stopped, missing marker, PREPARED_PARTIAL
- `FAIL`
  - 실행 자체가 실패했거나 핵심 경로가 끊겼습니다.

## 주요 결과 카드

### Last Result

- 가장 최근 실행의 최종 판정
- 상세 사유
- 연결된 증빙 경로

### Run Insight

- 현재 단계
- 병목 1줄
- 다음 액션 1줄

### COM Runtime

- CANoe COM attach 상태
- measurement 상태
- doctor 기반 핵심 런타임 확인 결과

### Tier Readiness

- `UT / IT / ST` 별 marker / filled / scored 상태
- `run_readiness.json` 기준으로 표시

### Batch Snapshot

- `dev2_batch_report.json` 기준
- phase / status / pass-fail 요약

## 증빙 경로

주요 산출물은 아래 경로에 생성됩니다.

- `canoe/tmp/reports/verification/doctor_report.json`
- `canoe/tmp/reports/verification/run_readiness.json`
- `canoe/tmp/reports/verification/dev2_batch_report.json`
- `canoe/logging/evidence/<UT|IT|ST>/<run-id>/...`

## 권장 확인 순서

1. Logs에서 실행 흐름 확인
2. Results에서 verdict 확인
3. COM Runtime과 Tier Readiness 확인
4. 필요한 경우 증빙 파일을 직접 열어 문서에 연결

# 결과 해석

운영 원칙:

- `canoe/tmp/reports/verification`는 실행 중간 결과를 쌓는 staging 영역입니다.
- reviewer/Jenkins 기준 최종 보관은 `artifacts/verification_runs/<run_id>/<phase>/`만 봅니다.
- staging 결과는 Git에 커밋하지 않습니다.

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
- `pre`에서는 advisory gate 실패가 `WARN`으로 남을 수 있습니다.
- `full`에서는 같은 항목이 `FAIL`이 될 수 있습니다.

### Surface Evidence Bundle

- reviewer-facing 결과 묶음
- runtime module 이름이 아니라 `BCM / IVI / CLUSTER / ADAS / V2X / ...` 기준으로 표시
- `surface_evidence_bundle.json/md`와 `surface/<bundle_key>/bundle.*`를 기준으로 해석
- 각 surface bundle에는 다음이 함께 들어갑니다.
  - `mapping_status`
  - `req_ids`
  - `test_case_ids`
  - `scenario_ids`
  - `native_test_assets`
  - `doc_refs`

### Execution Manifest

- 실행 인스턴스 식별자와 reviewer-facing 식별자를 함께 묶는 최종 manifest입니다.
- `run_id`는 이번 한 번의 실행 묶음을 식별합니다.
- `Req / TestCase / Surface ECU / Scenario`는 고정 traceability 키입니다.
- 즉 OEM식으로 보면:
  - `run_id` = execution key
  - `Req/TestCase/Surface/Scenario` = stable review key
  - `phase policy` = 이번 실행에서 무엇이 blocking인지 정의하는 verdict policy

### Surface Evidence Bundle

- reviewer-facing 결과 묶음
- runtime module 이름이 아니라 `BCM / IVI / CLUSTER / ADAS / V2X / ...` 기준으로 표시
- `surface_evidence_bundle.json/md`와 `surface/<bundle_key>/bundle.*`를 기준으로 해석

## 증빙 경로

주요 산출물은 아래 경로에 생성됩니다.

- staging:
  - `canoe/tmp/reports/verification/*`
- `canoe/tmp/reports/verification/doctor_report.json`
- `canoe/tmp/reports/verification/run_readiness.json`
- `canoe/tmp/reports/verification/dev2_batch_report.json`
- `canoe/tmp/reports/verification/dev2_batch_report.junit.xml`
- `canoe/tmp/reports/verification/surface_evidence_bundle.json`
- `canoe/tmp/reports/verification/surface_evidence_bundle.md`
- `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.json`
- `canoe/tmp/reports/verification/surface/<bundle_key>/bundle.md`
- `canoe/logging/evidence/<UT|IT|ST>/<run-id>/...`

- final archive:
  - `artifacts/verification_runs/<run-id>/<phase>/reports/*`
  - `artifacts/verification_runs/<run-id>/<phase>/surface/<bundle_key>/*`
  - `artifacts/verification_runs/<run-id>/<phase>/native_reports/**/*`
  - `artifacts/verification_runs/<run-id>/<phase>/evidence/<UT|IT|ST>/**/*`
  - `artifacts/verification_runs/<run-id>/<phase>/manifests/artifact_manifest.json`
  - `artifacts/verification_runs/<run-id>/<phase>/manifests/execution_manifest.json`

`dev2_batch_report.junit.xml`은 Jenkins 수집용 ingress 포맷입니다.

## 권장 확인 순서

1. Logs에서 실행 흐름 확인
2. Results에서 verdict 확인
3. COM Runtime과 Tier Readiness 확인
4. 필요한 경우 증빙 파일을 직접 열어 문서에 연결

## 제품 안에서 바로 하는 작업

Verification Console 안에서는 아래 흐름을 바로 사용할 수 있습니다.

- 결과 보기
  - `Results` 화면에서 verdict / insight / surface bundle / execution timeline 확인
- 산출물 열기
  - `artifact open --target batch-report`
  - `artifact open --target surface-bundle`
  - `artifact open --target execution-manifest --latest`
- 원본 계약 파일 열기
  - `artifact open --target surface-inventory`
  - `artifact open --target traceability-profile`
  - `artifact open --target artifact-layout`
  - `artifact open --target results-doc`
- 산출물 정리
  - `artifact clean --scope staging`
  - `artifact clean --scope staging --yes`

즉, 결과를 본 뒤 같은 제품 표면에서 산출물과 원본 계약 파일까지 바로 따라갈 수 있어야 합니다.
